# Change Lens rework validation — 2026-09-06

## Outcome and scope

The revised implementation passed its source-integrity, functional, and responsive checks. This does not establish that a human reviews more accurately or efficiently with it. The user rejected the previous interface despite its functional QA, so the earlier “passed” result must not be interpreted as validation of review usefulness.

The previous generated visual and narrative are no longer design authority. The current specification is the user's explicit correction: ground the main view in the task, actual contracts/modules, and baseline/submitted implementation; remove cutesy language and disconnected abstractions. The supplied screenshot documents the rejected baseline. This was an intentional semantic and structural rework, not a fidelity exercise against that rejected mock.

## Source and content checks

- Two agents independently prepared source-grounded descriptions from M2/M3 and M3/M4 snapshots. M3 has five change units and eleven module/dependency entries. M4 has six change units and twelve module entries.
- Each change separates requirement, baseline, submitted implementation, and test references. Automated checks validate the milestone version, file existence, line bounds, and baseline/head fingerprints.
- A separate factual pass checked the new M4 interface and request reconstruction against source and the recorded execution. It found no material M4 inaccuracies.
- That pass found ambiguous M3 provenance: “not executed during this inspection” omitted the distinction between the later prose pass and earlier 154-test run. Revised all five M3 verification descriptions to identify the earlier execution and remaining targeted-test gaps.
- The execution table reads its measured values from the original raw `REVIEW_EVIDENCE` log. Request JSON is explicitly helper-resolved, not represented as captured network traffic.
- The M3 execution view displays actual test source. Complete test boundaries are retained without including the next test's header.
- Removed the invented scenario models and editorial headings. A module list was changed from a numbered “path” to unordered implementation changes to avoid implying an unverified execution order.
- M4's one reproduced finding remains attached to cancellation; the overview represents all six requirement areas. The API contract for payment statements includes the actual JSON example from the requirement, with its source and evidence type stated.

## Browser checks and evidence

Browser: Codex in-app browser, same local server used by the user's Chrome page. The server was already running on port 4393.

Screenshots:

- `qa/v2/overview-desktop.jpg`: M4 requirements and full comparison at 1280 × 900 CSS viewport.
- `qa/v2/room-contract-desktop.jpg`: room fields and contract details at desktop width.
The initial QA also captured two narrow-viewport images; they are omitted from the repository. The user subsequently excluded mobile and accessibility work from this desktop prototype’s scope.

Captures omit the scrollbar and may be slightly scaled by the browser capture API; they are JPEG files. Screenshots were inspected as rendered evidence against the new structural requirements. The rejected reference is not used to justify retaining its old proportions, serif heading style, or wording.

A narrow desktop check exposed a comparison table wider than its container: the implemented column required horizontal scrolling. Fixed the main comparison to use a full-width subject row followed by three aligned columns below 1100 pixels, and stacked labelled sections below 650 pixels. Rechecked: at a width of 862 pixels the comparison fits its 613-pixel content region. At 1280 pixels it uses four table columns and fits its 985-pixel content region. At 390 pixels the page width is 375 pixels; there is no page-level horizontal overflow. Source code and secondary data tables keep local horizontal scrolling when necessary.

Interactions verified:

- Select M3/M4 and navigate the revised views.
- Open a payment contract from its overview row; inspect fields and implementation references.
- Open the M3 router excerpt and compare its exact M3 → M4 diff, showing the new payment route.
- Open the M4 execution, expand the final cancellation request, and inspect the observed/required table.
- Save a temporary note on the group-totals contract, reload, and verify export preview retains request path/line and snapshot. Remove the temporary note afterward. Existing notes are not cleared.
- Select the M3 stale-revision test and inspect its actual assertions.
- Verify the M3 implementation map contains eleven entries and filter source files by a specific path.
- Open baseline group renderer source on mobile and close the native dialog using Escape.
- Browser warning/error log checked after these flows: no entries returned.

## Visual surfaces

- **Typography:** system sans-serif for prose and headings, system monospace for identifiers/source. Literal headings identify requests, contracts, and modules. No external font dependency remains.
- **Spacing and hierarchy:** a compact project header, actual task introduction, full change comparison, and explicit detail views replace the editorial narrative and generic evidence sidebar.
- **Color:** restrained neutral surfaces, green navigation, and amber labelled mismatches. Text and labels carry status independently of color.
- **Assets:** no decorative assets are needed. This is a rendered technical review, not a rasterized mock.
- **Copy:** exact names are paired with behavior descriptions; baseline, requirement, submitted code, assertions, measured outputs, and reviewer scope are distinguished. Source references appear with the claims they support.

## Automated checks

Production build passed. Nine Node tests and two Python tests passed. Node checks cover source hash consistency, changed-evidence rejection, complete source references with correct baseline/head versions, captured execution values, note provenance, and template packaging/server behavior.

These counts describe the interface rework at the time. Subsequent repository publication added a publication-integrity check, and the user then requested removal of the template hosting adapter and its four tests. The standalone project now has six Node tests and two Python tests; its build writes static output to `dist/`.

No new candidate-service execution or benchmark scoring was performed during this interface rework. The preserved M4 reproduction remains an intentionally failing test demonstrating the application defect.

## Remaining limits

This is still a curated account of two specific changes. The wording and grouping require reviewer feedback; valid links do not by themselves prove an interpretation correct. Fresh review of the wider M4 changes is incomplete. No assistive-technology audit, cross-browser matrix, or human performance comparison has been completed.

Recorded functional result: passed. This is not a human-review-performance result.
