# Handoff for the next agent and reviewer

## Start here

Read the repository `AGENTS.md`, [README](../README.md), [approach](APPROACH.md), and [architecture](ARCHITECTURE.md). Install with `npm ci`, run the development server on `127.0.0.1:4393`, and open `?m=4&view=overview`. Run `npm test` and `npm run build` when verifying a checkout. The application is standalone; production output goes to `dist/` with no provider-specific hosting adapter.

The user wants to continue experimenting at work. The intended workflow has agents doing both implementation and the substantive review. Change Lens gives the human a way to gauge whether and where to pay attention, then investigate a selected subject and contribute judgment or guidance. The goal is meaningful involvement while preserving delivery speed and quality across whatever dimensions matter in that environment.

The user has not yet chosen a workplace repository, MR, issue tracker integration, model backend, or deployment. Decide the next small adaptation with them in that environment. No company code or context is included here.

## Current state, September 6, 2026

- Working desktop review of GroupStay M2 → M3 and M3 → M4, with the selected sources included locally.
- Requirements, baseline behavior, submitted behavior, and review findings are distinct and directly sourced.
- Five M3 change units and eleven module entries; six M4 change units and twelve module entries.
- Actual M4 defect reproduction, test source, raw output, and runtime information are included. A statement that an earlier test ran refers to that recorded review, not a new run by whoever opens the app.
- Notes and assessments can be saved locally and exported. They are not sent to an agent or a merge request.
- The user rejected the first narrative interface and said this revision fits review much better. They still intended to take a deeper look. Do not treat this as a completed usability evaluation.
- This is a personal desktop experiment. Mobile work and accessibility audits were explicitly excluded from the current scope; prioritize technical accuracy and the desktop review experience.

## Preserve these decisions

1. Start with the real task and the whole change. Choose the relevant dimensions from the change and its environment; the GroupStay examples do not define a universal checklist. A defect is one part of the review, not its organizing substitute.
2. Use exact operations, fields, contracts, and module names, with explanations of their behavior. Technical specificity alone is not sufficient if its meaning stays opaque.
3. Show the difference between what the request requires and what the implementation does. Avoid an unqualified “does” or “should.”
4. Keep author claims, reviewer inspection, executed evidence, test assertions, inference, and missing context identifiable.
5. Support both deciding where attention is useful and investigating that subject in depth. Let the human challenge an assumption or provide context there. Keep the whole change navigable beyond the agent's highlights, and preserve source and snapshot provenance through the handoff.
6. Treat representation as a way to inspect the change. Do not reintroduce cute headings, generic risk scores, decorative diagrams, or invented simulations that imply they ran the implementation.
7. Keep the reviewing workflow independent of the author using this system. An existing MR is the primary intended entry point; local pre-MR review is also useful.
8. The agent does the substantive review under repository-specific instructions. Human participation can be selective; the instrument must not require the person to repeat that review or add a mandatory approval step to every change. Existing team approval rules remain applicable.
9. Treat passing required tests and checks as the entry condition for review, locally or in CI. Start from those results. Review their coverage and expectations, and target additional verification at concrete gaps or failure hypotheses.
10. Evaluate attention choices and investigation quality together with delivery speed and the quality criteria relevant to the change. More intervention or more time in the UI is not an outcome to optimize for.

## A useful first workplace experiment

Select one existing, unfamiliar MR whose required checks pass, with a linked task and a consequential behavior change. Gather its exact base/head, requirements, repository review instructions, relevant unchanged code, and author evidence. Let the reviewer agent perform its normal review, with findings shaped by that environment's guidance.

Adapt the renderer to present that one change alongside the existing GroupStay example. Separate case selection, source identity, contract descriptions, findings, and execution evidence from the current hardcoded `App.jsx` content. Namespace notebook storage by repository/change/snapshot before multiple real changes share an origin.

Choose the dimensions and representation from the task. A security or scaling change may need a substantially different account from the GroupStay examples; their contract tables and module maps are starting examples, not mandatory views. Extend the format where the actual case requires it. Record absent context instead of filling it in.

Sit with the human while the agent's review is available. Can they judge what merits their attention, investigate that subject, identify a missing assumption, and provide useful guidance? Can they explore something the agent did not flag? What did the instrument obscure or unnecessarily slow down? Use those observations to choose the next iteration. The [review protocol](../REVIEW_PROTOCOL.md) describes a comparison that considers quality and delay as well as human understanding.

## Known implementation work

- No GitLab/GitHub or issue-tracker adapter; importer only recognizes the captured Sweat Bench layout.
- No live agent backend or orchestration; review content was authored by agents during development.
- No generic finding or execution schema; several GroupStay facts remain embedded in React.
- No cross-snapshot claim invalidation beyond rejecting changed locked evidence files.
- No production consumer/deployment inventory, shared workspace, notebook import, or multi-user persistence.
- Source references are checked structurally; factual relevance still needs review.
- The captured M4 review is focused on cancellation. Do not describe all payment/migration paths as independently verified.

For a company continuation, record the public starting commit and license before making internal changes. Keep company material in the destination approved for it; future workplace work is not implicitly authorized for publication back to this repository.
