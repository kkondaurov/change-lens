# Reviewer reproduction runtime

This describes the recorded M4 experiment, not an execution performed when the UI loads.

- Source: the captured milestone-4 snapshot, copied into a separate working directory (`isolated-review/m4` in the published report).
- Runtime: Erlang/OTP **29.0.4** (ERTS **17.0.4**), Elixir **1.20.2**, compiled with OTP 29, selected with mise.
- Captured command from that isolated directory: `mix test test/group_stay_web/controllers/reviewer_active_totals_test.exs --seed 0 > ../m4-reproduction.log 2>&1`.
- Test: `public/evidence/reviewer_active_totals_test.exs`.
- Raw output: `public/evidence/m4-reproduction.log`.
- Observed exit status: **2**, one test failed on the expected active-room totals assertion. The failure is the reproduced application defect, not a setup failure.
- For log capture, the filesystem sandbox initially prevented Mix's TCP-based filesystem lock (`:eperm`). The same command ran with approved access to that local lock. No code, dependency, or assertion changed to obtain the failure.
- Earlier complete suite results are in `fresh-review.md` and `fresh-review-m4.md`; the full suites were not rerun for log capture or repository packaging.

The public note replaces personal filesystem locations with artifact-relative references. See `docs/PROVENANCE.md` for instructions to reproduce from a fresh checkout.
