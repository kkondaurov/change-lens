# Handoff for the next agent and reviewer

## Start here

Read the repository `AGENTS.md`, [README](../README.md), [approach](APPROACH.md), and [architecture](ARCHITECTURE.md). Install with `npm ci`, run the development server on `127.0.0.1:4393`, and open `?m=4&view=overview`. Run `npm run build` then `npm test` when verifying a checkout.

The user wants to continue experimenting at work. They have not yet chosen a workplace repository, MR, issue tracker integration, model backend, or deployment. Decide the next small adaptation with them in that environment. No company code or context is included here.

## Current state, September 6, 2026

- Working desktop review of GroupStay M2 → M3 and M3 → M4, with the selected sources included locally.
- Requirements, baseline behavior, submitted behavior, and review findings are distinct and directly sourced.
- Five M3 change units and eleven module entries; six M4 change units and twelve module entries.
- Actual M4 defect reproduction, test source, raw output, and runtime information are included. A statement that an earlier test ran refers to that recorded review, not a new run by whoever opens the app.
- Notes and assessments can be saved locally and exported. They are not sent to an agent or a merge request.
- The user rejected the first narrative interface and said this revision fits review much better. They still intended to take a deeper look. Do not treat this as a completed usability evaluation.
- This is a personal desktop experiment. Mobile work and accessibility audits were explicitly excluded from the current scope; prioritize technical accuracy and the desktop review experience.

## Preserve these decisions

1. Start with the real task and the whole change. A defect is one part of the review, not its organizing substitute.
2. Use exact operations, fields, contracts, and module names, with explanations of their behavior. Technical specificity alone is not sufficient if its meaning stays opaque.
3. Show the difference between what the request requires and what the implementation does. Avoid an unqualified “does” or “should.”
4. Keep author claims, reviewer inspection, executed evidence, test assertions, inference, and missing context identifiable.
5. Let the human challenge an assumption or provide context at the relevant subject. Keep source and snapshot provenance through the handoff.
6. Treat representation as a way to inspect the change. Do not reintroduce cute headings, generic risk scores, decorative diagrams, or invented simulations that imply they ran the implementation.
7. Keep the reviewing workflow independent of the author using this system. An existing MR is the primary intended entry point; local pre-MR review is also useful.
8. The agent still conducts code review under repository-specific instructions. The instrument adds a human entry point into that work.

## A useful first workplace experiment

Select one existing, unfamiliar MR with a linked task and a consequential behavior change. Gather its exact base/head, requirements, repository review instructions, relevant unchanged code, and author evidence. Let the reviewer agent perform its normal review, with findings shaped by that environment's guidance.

Adapt the renderer to present that one change alongside the existing GroupStay example. Separate case selection, source identity, contract descriptions, findings, and execution evidence from the current hardcoded `App.jsx` content. Namespace notebook storage by repository/change/snapshot before multiple real changes share an origin.

Choose the representation from the task: a contract table, state diagram, request sequence, or module map when it explains a real relationship. Do not make a universal visualization framework the first milestone. Record absent production/client context instead of filling it in.

Sit with the human reviewer. Can they explain the consequential behavior difference, distinguish requirement from implementation, locate evidence, identify a missing assumption, and provide actionable guidance? What did the instrument obscure? Use their answers to choose the next iteration. The [review protocol](../REVIEW_PROTOCOL.md) describes a more controlled comparison with an ordinary MR plus agent report.

## Known implementation work

- No GitLab/GitHub or issue-tracker adapter; importer only recognizes the captured Sweat Bench layout.
- No live agent backend or orchestration; review content was authored by agents during development.
- No generic finding or execution schema; several GroupStay facts remain embedded in React.
- No cross-snapshot claim invalidation beyond rejecting changed locked evidence files.
- No production consumer/deployment inventory, shared workspace, notebook import, or multi-user persistence.
- Source references are checked structurally; factual relevance still needs review.
- The captured M4 review is focused on cancellation. Do not describe all payment/migration paths as independently verified.

For a company continuation, record the public starting commit and license before making internal changes. Keep company material in the destination approved for it; future workplace work is not implicitly authorized for publication back to this repository.
