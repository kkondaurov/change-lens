# Independent review: GroupStay M2 → M3

## Scope and provenance

Run: `v6-claude-opus5-high-01`. Base: `public/evidence/snapshots/milestone-2`. Proposed snapshot: `public/evidence/snapshots/milestone-3` (abbreviated **M3** below). This is a fresh reviewer-agent assessment written without reading author logs, self-review, scores, or private evaluator reports. No benchmark source was changed. The snapshots were treated as a merge-request comparison.

Read `TASK.md`, product/API/runbook documents, request 03, changed application code, surrounding partner/domain handling, and the added tests. The review is bounded to durable-operation behavior; it is not a complete security or domain audit.

## Judgment

**No actionable new M3 defect identified in this review.** This is a scoped review result, not a correctness certificate. The candidate's complete suite ran in an isolated copy: **154 passed**, seed **387489**, `mix test`, exit 0. Isolated copy: `isolated-review/m3`. Dependencies were copied and compiled locally; no private tests were used.

## Before, after, and intended behavior

| Subject | Before (M2) | With M3, established by inspection/tests | Required by candidate-visible source |
|---|---|---|---|
| Retrying a payment | Identifier was a reconciliation reference; operation dispatch could apply a payment again | Identified operations check a durable record before domain dispatch; equivalent payload replays the stored result | M3 `docs/requests/03-durable-operations.md:3–19` |
| Rejected operation | Domain transaction rolled back, no durable operation result | Rejection rolls back domain work and is then remembered; subsequent retries replay the rejection | Request 03:16–24 |
| Payload changes | Operation dispatched against current state | Same ID plus different canonical payload returns `operation_id_conflict` | Request 03:15–19,41–45 |
| Read operation result | No operation-read route | `GET /api/v1/operations/:operation_id` returns stored result only, or the specified 404 | Request 03:37–39 |
| Storage footprint | No operations table | New operations table retains identifier, type, complete canonical submitted content, result, timestamps; unique identifier index | Request 03:21–35 |

## Concrete evidence and interpretation

- Replay bypasses current domain reads: M3 `lib/group_stay/partner.ex:51–65`; payload equality: `lib/group_stay/operations.ex:42–47` and `lib/group_stay/operations/payload.ex:15–29`. Applied replay, same-batch replay, and revision preservation are tested in `test/group_stay_web/controllers/idempotency_test.exs:14–30,194–230`.
- Applied effects and the remembered result are inside the same transaction: M3 `lib/group_stay/partner.ex:71–85`; collision rolls back that attempt's effects and reads the winner's record at 96–98. The unique constraint is `priv/repo/migrations/20260301000000_create_operations.exs:7–16` and `lib/group_stay/operations/record.ex:30–34`. This is static support for at-most-once effects, not an executed concurrent-race demonstration.
- Rejections use a different path: M3 `lib/group_stay/partner.ex:82–93` rolls back the domain transaction, then inserts the record. I inspected this distinction but did **not** promote it to a defect merely because it differs from the applied path. No consequential violation was demonstrated. Crash/interleaving behavior around this boundary remains untested in this review.
- Persistent audit payload and result: M3 `lib/group_stay/operations.ex:31–39`; internal commit-order read at 49–50. SQLite is the configured database; an ascending insert ID is not being assumed portable to another database with different commit-order semantics.
- Endpoint limits its response to stored result: M3 `lib/group_stay_web/controllers/operation_controller.ex:6–15`, `operation_json.ex:11`, `router.ex:14`. The canonical submitted payload remains internal.

## Review limitations

1. No concurrent HTTP retry stress test or explicit application/database-process restart was executed by this reviewer. Existing `operations_test.exs:89–95` establishes that a record is stored in the database; it does not simulate a restart. Passing the whole suite does not close these obligations.
2. Tests execute through Phoenix's connection test environment and SQLite test configuration, not a production deployment.
3. No gateway deployment, namespace switching, caller authorization, retention policy, or operational sizing was inspected. API documentation says authentication is upstream; absence of in-app authentication was not raised as a new defect.
4. This report does not claim all possible regressions were excluded.

## Human guidance opportunities

**Release coordination question:** Who verifies that the gateway actually starts a new operation-identifier namespace at deployment? Request 03:6–8 explicitly relies on it. This is an external release dependency, not a missing code requirement to invent.

**Evidence decision:** Before production sign-off, should the reviewer obtain a real concurrent retry and restart demonstration? Those are explicit guarantees, while the present reviewer evidence is serial-suite execution plus code inspection.

**Operational context question:** The new audit record retains complete submitted content without a retention limit. Request 03 requires retention; it does not specify a deletion schedule. A domain owner can provide retention requirements. Do not call the absence of an invented TTL a defect.

