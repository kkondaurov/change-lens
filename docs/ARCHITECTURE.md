# Architecture and artifact contract

## What runs now

The application is a static React/Vite frontend. It fetches two local evidence files, checks their SHA-256 hashes against `src/provenance.js`, and renders them together with the curated account in `src/reviews.json`. The app fails loading if a locked file differs.

There is no live model call, MR connector, issue-tracker connector, job runner, shared database, or server-side review execution. The production build is static output in `dist/`, served locally with `npm run preview` or by a static web server. Running and building the application requires no hosting provider or Codex plugin.

| Component | Responsibility |
|---|---|
| `scripts/import-sweatbench.py` | Copies eligible text sources from selected milestones and their predecessors; computes content hashes and diffs; imports reports and explicit assistant handoffs. |
| `public/evidence/snapshots/` | Standalone copies of the selected source, tests, configuration, and requirements for M2, M3, M4. |
| `public/evidence/bundle.json` | Embeds the same source text and hashes, comparisons, historical evaluator results/logs, and author handoffs. |
| `public/evidence/fresh-reviews.json` | The independent reports plus the M4 reviewer test, captured execution, and runtime note. |
| `src/reviews.json` | Agent-authored description of change units, contracts, module responsibilities, sources, and verification scope. |
| `src/provenance.js` | Expected hashes and the browser's evidence-file validation. |
| `src/App.jsx` / `src/review.css` | Review views, selected source/diff dialogs, evidence displays, and notebook interactions. |
| `src/domain.js` | Source excerpt lookup and Markdown note export. |
| `tests/` | Evidence consistency, reference versions/ranges, captured values, note provenance, and importer boundaries. |

## Current structured account

This is the shape consumed by the current renderer, not a declared general interchange standard. Its contract and module fields reflect the GroupStay cases. Other changes may need different dimensions and representations, such as access rules or measurements across workloads; do not force every review into this structure. `src/reviews.json` is keyed by submitted milestone (`"3"` or `"4"`). Each review includes:

```text
id, title, summary, requestPath
baseFingerprint, headFingerprint
changes[]
  id, title, target
  before, required, after
  verification: { status, text }
  refs: { before[], requirement[], after[], tests[] }
  contract[]: { field, before, after }
  implementationSteps[]: { module, function, change, ref }
modules[]: { path, role, before, after, refs[] }
```

A source reference is `{ m, path, start, end }`, with a captured milestone and one-based inclusive line numbers. Requirement and submitted references use the head; baseline references use its predecessor. `verification.status` currently supports `inspected`, `reproduced`, and `not-verified`. The accompanying text carries the actual scope.

The name `implementationSteps` is historical. The UI renders an unordered list of implementation changes; it does not assert an executed call sequence.

The bundle's snapshot fingerprint is SHA-256 over sorted `path + NUL + file-sha256 + newline` entries. It identifies the imported text selection, not a complete repository or Git tree. The manifest reports file counts and comparison scope. Publication additionally records individual evidence-file hashes.

## Boundaries that matter

**Imported content and instructions.** The importer is a capture tool, not a review agent. It excludes reasoning blocks, dependency/build directories, databases, hidden files, and binary text. It does not detect every credential or confidential datum in eligible source, logs, or author text. New captures default to local-only; publication requires an actual content review.

**Interpretation and evidence.** Hashes and valid line ranges show that the account refers to a particular capture. They do not prove the account follows from it. Existing tests can encode the wrong requirement. Recorded author, evaluator, and reviewer results remain distinct.

**Observed execution and examples.** The M4 execution view parses `REVIEW_EVIDENCE` from the saved reviewer log. Displayed requests are resolved from test helpers; they are not packet captures. The payment-statement JSON is from the request document. The M3 view displays actual candidate assertions. None of these runs the service in the browser.

**Notebook persistence.** Notes and the M4 finding assessment are in `localStorage` under `change-lens-notebook-v1`. Each new entry records a snapshot and time. Export preserves this information. There is no synchronization or notebook import, and browser data is not part of this repository. Moving to a different origin or machine requires an explicit Markdown export for handoff.

## What still depends on GroupStay

`App.jsx` hardcodes the two milestones, labels, one M4 finding, the reproduction request sequence, selected M3 tests, and historical review summaries. `domain.js` exports those two milestones and the one finding assessment. The review reports are text, not a general finding schema. The notebook key is global to this prototype's origin, not namespaced by repository and change.

Adding a new JSON file alone will not make a new MR work. The smallest useful next implementation is to extract those assumptions into an explicit case manifest and add one workplace example, while preserving the current sample. Design a finding/evidence format from those two cases rather than pretending the current format already covers everything.

A later live integration can have the reviewing agent emit validated artifacts while doing the substantive review, with the renderer supporting both an overview for choosing where to pay attention and deeper inspection of a selected subject. Human guidance should return to the author or reviewing agent with its source context. This integration is not implemented yet.

Useful validation includes source existence, correct base/head identity, line ranges, typed evidence, explicit review scope, and stale-claim detection. Do not infer that a claim was revalidated merely because a new snapshot has loaded.

## Verification

Run `npm test` and `npm run build`. Tests run independently of the build. CI tests and builds a fresh checkout; the build produces `dist/index.html`, application assets, and the included evidence.

The Node and Python tests validate the instrument and included artifacts. They do not run the GroupStay service. The reviewer reproduction is deliberately failing evidence and is not part of the default green CI suite. Instructions for running it separately are in [PROVENANCE.md](PROVENANCE.md).
