# Example provenance and public baseline

## Origin and scope

This repository publishes the Change Lens prototype developed with its owner, GitHub user `kkondaurov`, in September 2026. The owner explicitly requested publication of the code, rationale, and examples under a permissive license for later workplace adaptation. The original work is released under 0BSD; see the root license and third-party notices for scope.

The examples were copied from the owner's Sweat Bench v6 run `v6-claude-opus5-high-01`, produced by Claude Opus 5 at high effort on August 25, 2026. GroupStay is a fictional B2B reservation API. No workplace repository, customer data, or employer material was used to create these examples.

The import occurred on September 5, 2026. M2 is the baseline needed for the M3 review; M3 is also the baseline for M4. The snapshots are selected text files, not complete Git repositories, and the benchmark source was not modified. Framework/dependency origins are recorded in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).

| Snapshot | Imported files | SHA-256 of selected source manifest |
|---|---:|---|
| M2 | 66 | `52a8f755f1b996a0b8fef125c1c438295aef8fed34e0ba594c6e75f780ad97be` |
| M3 | 78 | `7e06f2bb41e0452875dfc4847b18ff64287c73f58639b34f21aae37e578ec6fc` |
| M4 | 93 | `bcefbb7a4c0abd29eae1de32a73a07ec76223cfc734dbcd7e5d85316f282b090` |

The manifest also records M3's 22 changed files (8 implementation, 12 tests, 2 documents) and M4's 31 (18 implementation, 11 tests, 2 documents).

## What is included

- Selected `lib`, `test`, `docs`, `config`, and `priv` text, plus `mix.exs`, `mix.lock`, `TASK.md`, and `README.md` from the three snapshots.
- Exact source text and its hashes, unified diffs, milestone identities, and requirement references.
- Explicit final assistant handoffs for M3 and M4, with the original transcript line numbers. Full agent transcripts and reasoning are excluded.
- Historical evaluator reports and selected evaluator output. The private evaluator source is not included; references to it identify historical assertions, not files available for a fresh private-suite run.
- Independent reviewer reports, the M4 reviewer test, raw captured failure output, and a runtime note.
- The curated descriptions and two desktop screenshots of the revised UI.

Browser notes, local dependencies, build products, databases, and earlier rejected mockups are excluded. The example files are review material; using the frontend never executes their Elixir code.

## Publication transformations

The local capture originally recorded personal absolute filesystem paths. Publication replaced those paths with repository-relative artifact paths or logical references:

- Snapshot locations become `public/evidence/snapshots/milestone-N/...`.
- `sweatbench-run:v6-claude-opus5-high-01` names the original run; it is not a filesystem directory or remote API.
- `isolated-review/m3` and `isolated-review/m4` name the historical scratch copies used by the reviewer; they are not required in a new checkout.
- References to `sweat-bench/evaluation/private_tests/...` are original evaluator locations whose source is not bundled.

The runtime note was rewritten with portable artifact references. The combined fresh-review JSON was rebuilt from its published report/runtime-note copies. The evidence lock and manifest were updated to these published bytes. This was a documented packaging change, not a reinterpretation of the review.

**Preserved:** all 237 snapshot files and their embedded source, hashes, fingerprints and comparisons; evaluator report values; author handoff text and line numbers; the reviewer test; and raw measured reproduction output.

[`publication.json`](../public/evidence/publication.json) records the earlier local-capture hashes, published hashes, transformations, and snapshot identities. The personal-path versions are not included. The test suite checks published hashes, standalone/embedded evidence consistency, and copied source bytes. Hashes identify artifacts; they do not establish correctness of an agent's interpretation.

## Optional reproduction of the M4 defect

The normal UI test suite does not execute GroupStay. The saved reproduction used Erlang/OTP **29.0.4** and Elixir **1.20.2** compiled for OTP 29 (mise identifier `1.20.2-otp-29`). The raw command, exit status, and environment limits are in [`reproduction-environment.md`](../public/evidence/reproduction-environment.md).

To rerun separately, install a compatible Erlang/Elixir toolchain and dependency build tools, then from the repository root:

```sh
repro_dir="$(mktemp -d)"
cp -R public/evidence/snapshots/milestone-4/. "$repro_dir/"
cp public/evidence/reviewer_active_totals_test.exs \
  "$repro_dir/test/group_stay_web/controllers/"
cd "$repro_dir"
mix deps.get
mix test test/group_stay_web/controllers/reviewer_active_totals_test.exs --seed 0
```

Select the captured runtime in the scratch directory if exact runtime reproduction is needed. Dependency installation requires network access and may compile native SQLite components. The recorded outcome is **one failing test, exit 2**: zero active rooms, but lodging 52,500 cents, deposit due 10,500, and deposit paid 1,000. A setup failure is not a successful reproduction. The service snapshots and evidence must remain unchanged; any attempted fix belongs in a separate copy.

The original candidate suites passed 154 tests in M3 and 233 in M4 before the added reviewer test. They were not rerun during publication. M4's broader payment, migration, and security behavior was not comprehensively reviewed.

## Continuing at work

Record the exact public commit you import in the company's destination repository. The `v0.1.0` tag marks the initial publication; use the current `main` branch for the standalone version after removal of the starter hosting adapter. Keep the license, applicable third-party notices, and the imported revision identifiable according to the destination's process. The project's 0BSD license does not require publication of company modifications.

This provides a public source and revision record. It is not an assignment of employee-created IP, a patent clearance, or a determination of an employer's internal approval requirements. Ownership of later work is governed by the applicable employment arrangements and law, not by this repository's README.
