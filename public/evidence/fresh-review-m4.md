# Independent focused review: GroupStay M3 → M4

## Scope and provenance

Run `v6-claude-opus5-high-01`; source snapshots are `public/evidence/snapshots/milestone-3` (**M3**) and `public/evidence/snapshots/milestone-4` (**M4**). This focused follow-up examined room cancellation and group totals against the candidate-visible request 04. It was completed without reading author logs, self-review, benchmark scores, or private evaluator reports. Parent requested particular attention to active-room totals; this is not a comprehensive independent audit of all M4 features.

## Finding: [P2] Recompute active-room totals when cancellation removes the final room

**Primary code location:** `public/evidence/snapshots/milestone-4/lib/group_stay/reservations.ex:201–206`.

**Trigger:** Open the standard two-room group, apply its 10,000-cent cash payment, cancel room A, then cancel remaining room B. Full cancellation also reaches the same problematic branch.

**Observed consequence:** No active rooms remain, and the ledger correctly holds zero cash, but `GET /api/v1/groups/group-81` retains the previous active group's lodging (52,500 cents), due (10,500), and paid (1,000) totals. Only outstanding becomes zero. Consumers are told there is lodging/deposit/paid value attributable to active rooms even though none remain.

**Why this is a requirement violation:** M4 `docs/requests/04-room-accounting-and-payment-reductions.md:10–11` says group totals sum active rooms, and line 31 explicitly requires lodging, due, paid, and outstanding totals to describe active rooms only. Lines 52–53 state that no active rooms means cancelled. The implementation deliberately retains historical totals for cancelled groups (`lib/group_stay/reservations/group.ex:6–8`) and suppresses recalculation exactly at that transition. Historical totals were M3 behavior, but the current request explicitly changes the meaning of these fields.

**Mechanism:** `reservations.ex:157–161` marks rooms cancelled and calls `update_group`; `status_after_cancelling` at 166–170 returns `status: cancelled`. `update_group` at 203–205 recomputes via `Funding.group_totals` only for active groups. `funding.ex:94–119` already has the needed active-room aggregation. `group_json.ex:22–27` exposes unchanged stored totals. The outstanding special case in `reservations/group.ex:92` masks one symptom but leaves the other totals stale.

**Proportionate correction:** Recompute group totals over active rooms even when moving to, or already in, cancelled status; keep historical information in existing settlements/payment/audit records. Update legacy expectations in the test suite and add a requirement-focused final-room/full-cancellation regression check. This is a localized correction, not a proposed architecture rewrite.

## Before / after / required

| Dimension | M3 | M4 observed | M4 required |
|---|---|---|---|
| Full cancellation totals | Preserves historical due/paid totals while outstanding is zero (`M3/lib/group_stay/reservations.ex:152–159`) | Still preserves historical totals on final cancellation | Active-room lodging, due, paid, outstanding totals all zero |
| Partial cancellation | Not supported | Remaining active rooms are correctly reflected while group remains active | Remaining active rooms only |
| Last room cancelled | Not applicable as a separate room workflow | Stops recomputing and freezes pre-final-cancellation totals | Empty active-room sum |

## Executed evidence

Work was run only in `isolated-review/m4`, an isolated source/dependency copy.

- Original candidate suite: `mix test`, **233 passed**, seed **955470**, exit 0, before adding the reviewer test.
- Reviewer-added test: `mix test test/group_stay_web/controllers/reviewer_active_totals_test.exs --seed 0`, **0/1 passed; 1 failed**, exit 2. This test only exists in the isolated copy, not the benchmark source.
- Test source: `public/evidence/reviewer_active_totals_test.exs:5–24`.

Captured values:

```json
{
  "before_last": {"status":"active","lodging_total_cents":52500,"deposit_due_cents":10500,"deposit_paid_cents":1000,"cash_paid_cents":1000,"credit_paid_cents":0,"outstanding_deposit_cents":9500},
  "after_last": {"status":"cancelled","lodging_total_cents":52500,"deposit_due_cents":10500,"deposit_paid_cents":1000,"cash_paid_cents":1000,"credit_paid_cents":0,"outstanding_deposit_cents":0},
  "active_rooms": 0,
  "ledger": {"cash_held_cents":0,"cash_refunded_cents":10000,"cash_retained_cents":0,"cash_converted_to_credit_cents":0,"cash_reduced_cents":0,"cash_charged_back_cents":0,"credit_liability_cents":0,"credit_shortfall_cents":0}
}
```

The preexisting suite can pass because `M4/test/group_stay_web/controllers/cancel_group_test.exs:21–26` asserts the old historical due/paid values, while `cancel_rooms_test.exs:72–73` checks only cancelled status and outstanding after cancelling the last room. The new requirement needs the assertions themselves to change.

## Human guidance opportunity

**Compatibility decision:** Does any real consumer need the historical totals that M3 exposed after full cancellation? The written M4 requirement is clear, so this is not a blocker to identifying the defect. A human with client context could still direct a compatibility plan or ask for historical values through an explicitly named view, rather than silently preserving old semantics under fields now defined as active-only.

## Limitations

The concrete partial-then-final cancellation defect was reproduced through Phoenix connection tests and SQLite in the isolated copy. Full cancellation reaches the same branch by inspection and is represented in the old candidate test, but no second reviewer reproduction was run. The wider M4 chargeback, legacy-funding migration, rounding, security, deployment, and concurrency requirements were not exhaustively reviewed. No benchmark score is inferred from this scoped finding.
