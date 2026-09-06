# Sweat Bench prototype evidence digest

Source root: `sweatbench-run:v6-claude-opus5-high-01`.
Inspected read-only on 2026-09-05. This is historical evidence from the 2026-08-25 run, not a fresh execution. Log excerpts below are explicit assistant text or tool output only. No reasoning blocks were extracted. Author handoffs must remain labelled **author handoff / self-review**, never independent review.

## Milestone 3: durable operations

### Requested behavior

Source: `snapshots/milestone-3/docs/requests/03-durable-operations.md`.

- Lines 3–4: “The partner gateway retries whenever it loses a response. `operation_id`, which has so far been a reconciliation reference, must now prevent an operation from being applied twice.”
- Lines 6–8: New identifier namespace begins at deployment; no reconstruction of earlier-release records; guarantee starts with operations received by this release.
- Lines 12–19: First operation processed normally; equivalent retries return exact original result without current domain reads/changes; object order irrelevant; array order/values significant; rejections remembered; changed payload returns `operation_id_conflict`.
- Lines 21–24: Atomic record/domain commit, at-most-once concurrent effects, rejected operations preserve domain state and commit rejection record, later batch operations continue.
- Lines 26–30: Unexpected exceptions roll back, are not remembered, produce HTTP 500; restart survival required.
- Lines 32–39: Retain complete submission/type/commit order for audit, but public operation read returns only stored result.
- Lines 41–45: Replay exact revision/stale details; correcting expected revision under the same identifier is a conflicting payload.

### Author handoff and review record

Source: `logs/agent-3.jsonl:388`, assistant text: “Now a full review of the diff:”. This is evidence that the author announced a self-review, not proof of its quality or an independent review finding.

Source: `logs/agent-3.jsonl:438`, explicit assistant final text. Useful excerpts:

> `docs/requests/03-durable-operations.md` is implemented. 154 tests pass; `mix precommit` (warnings-as-errors compile, format, full suite) is clean.

> An applied operation and its record commit in one transaction, so an attempt that loses the race for an identifier also loses its domain changes. A rejection rolls back the domain and then commits its record on its own, and the batch continues. Unexpected exceptions propagate untouched: the operation rolls back, nothing is remembered, the request 500s.

> I also verified durability out-of-band with a real `mix phx.server` on a file database: submit, kill the server, restart, resubmit — same result returned, group created once.

> Existing tests reused `operation_id` across differing payloads [...] I gave those submissions distinct identifiers. One test changed semantically: `apply_hotel_credit` "follows the revision contract" previously submitted an identical payload twice expecting applied-then-stale; the second now needs its own identifier to still be a fresh attempt.

> `docs/API.md` is unchanged. It was not updated for request 02 either [...] so the request documents appear to be the intended delta record.

Interpretation: strong presentation material for distinguishing a behavior change, altered tests, and author interpretation of documentation policy. Leaving API docs unchanged is an author decision, not a sourced project instruction or demonstrated defect by itself.

Independent corroboration of *historical author test execution*: `logs/agent-3.jsonl:437`, tool result contains `Result: 154 passed`. Earlier results at lines 387 and 420 also say 154 passed. This is the author-controlled local test suite, separate from evaluator private cases.

### Historical evaluator outcome

Source: `reports/milestone-3.json`.

- Top-level `status`: `failed`.
- `expected_private_cases`: 29; `tests`: 27 passed, 2 failed.
- `system_checks`: `idempotency-restart` passed (1/1).
- `summary`: 28/30 combines 29 private cases and one system check. Do not call it 28/30 private tests.
- `family_summary`: 3/3. Core families `durable-idempotency`, `occ-durability`, and `m3-restart` all passed.
- Failing private cases: `GroupStay.Private.HotelCreditTest::test credit consumes earliest expiry first and restored credit keeps its origin`; `...::test equal-expiry lots are consumed by source operation identifier`.

Source: `logs/evaluate-3.log`, assertion excerpts:

- First failure expected `cancel-b`, 3800 remaining cents, expiry `2028-04-30`; actual had same source and cents but expiry `2028-05-01`.
- Second expected `cancel-z`, 3800 remaining cents, expiry `2028-03-31`; actual had same source and cents but expiry `2028-04-01`.
- Log states `Result: 27/29 passed`, `Failed: 2 tests`.

**Important interpretation:** failure names mention consumption ordering, but the shown assertion mismatch is the expiry date. Do not narrate this as observed wrong lot order. `reports/milestone-2.json` already has the same two named failures (summary 22/24), so M3's top-level failure is not evidence of a newly introduced M3 regression. It is an inherited failing outcome; identifying the precise implementation cause requires separate code review.

## Milestone 4: a strong second example for human judgment

Source request: `snapshots/milestone-4/docs/requests/04-room-accounting-and-payment-reductions.md`.

- Lines 3–6: Organizers reduce blocks without whole cancellation; finance corrects overstated cash; preserve operation durability.
- Lines 10–11: “Expose the room-level lodging and deposit amounts already used to calculate the group requirement. Group totals are sums of the active rooms.”
- Lines 24–31: New room fields enumerated as status, deposit due, cash paid, credit paid. “The group's lodging, due, paid, and outstanding totals describe active rooms only.”
- Lines 16–22: Migration carries old funding into an unattributed senior block; cash then credit lots in consumption order; before durable-record funding in commit order; aggregate balances must not change.
- Lines 38–53: Partial cancellation is all-or-nothing on distinct active rooms; settle selected rooms only; group cancels when none active remain; `cancel_group` otherwise follows existing contract.
- Lines 61–64: Reductions can move only held cash from the specific payment, in reverse fill order.
- Lines 100–137: Chargebacks reclassify dispositions, revoke credit entitlement, account for shortfall, preserve other groups' state and original payment stored result.
- Lines 160–168: Payment statement dispositions reconcile to recorded amount and other views; prior funding without durable payment identifier cannot be addressed.

### Explicit author judgment calls

Source: `logs/agent-4.jsonl:901`, assistant final text:

> Request 04 is implemented and the full suite passes (233 tests, `mix precommit` clean).

> **Room fields**: the request's prose mentions "room-level lodging and deposit amounts" but its bullet list enumerates exactly four new fields. I followed the bullet list, so rooms do not expose a `lodging_cents`.

> **Totals on a fully cancelled group**: "totals describe active rooms only" would zero out a cancelled group's `lodging_total_cents`/`deposit_due_cents`/`cash_paid_cents`, contradicting request 02's delivered behavior (an existing test asserts a cancelled group keeps `cash_paid_cents: 8500`) and "`cancel_group` … otherwise follows its existing contract". I recompute totals over active rooms while the group is active and freeze them at cancellation. Room-level amounts stay attributed to cancelled rooms, so they still sum to the frozen group total.

This is particularly good material for an instrument: show requirement statements, author-chosen interpretation, before/after behavior, and human opportunity to resolve precedence. Do not automatically accept the author's claim of contradiction without inspection of request 02. Do not call the historical evaluator a determination of stakeholder intent.

Historical tool output `logs/agent-4.jsonl:900` corroborates `Result: 233 passed` in the author local suite.

### Historical evaluator outcome

Source: `reports/milestone-4.json`.

- 48/50 private tests passed; same two hotel-credit tests failed.
- System checks `payment-reduction-upgrade` and `room-history-upgrade` both passed (2/2).
- Aggregate `summary`: 50/52; top-level status failed.
- Family summary: 9/9; Core 8/8 and Judgment 1/1 (`judgment-r2-room-history`). This is a family result, not universal policy/intent validation.
- The M4 evaluation log repeats the same two expiry date mismatches as M3.

### Recommended use

M3 is a bounded workflow/replay example with strong historical positive evidence, a distinction between inherited failures and new behavior, and author decisions about test changes/documentation. M4 is a broader accounting example with explicit unresolved/contestable requirement interpretation, suited to an intervention panel and room-allocation view. If only one example is implemented first, M3 can be primary and M4 a small second case illustrating human judgment rather than an equally deep review.
