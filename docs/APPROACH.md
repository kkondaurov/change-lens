# Approach and rationale

## The problem

As implementation, debugging, planning, and review are delegated to agents, reading every changed line is an increasingly poor prerequisite for human participation. A reviewer may still know something the agent does not: a customer dependency, an operational constraint, an intended contract, or a reason a locally reasonable design does not fit the project.

The practical question is how that person finds the point where their context matters. A raw diff can require too much reconstruction. A fluent summary can hide the important distinctions. A clean test run can verify expectations that no longer match the request.

Change Lens explores an instrument alongside review that lets the human inspect the scope and behavior of a change, question the account, and supply guidance. The human does not have to follow every agent step. They should be able to engage when they choose to.

## What must remain distinct

For a specific subject, the review needs four separate accounts:

1. **Before:** what the baseline system does.
2. **Required:** what an identified task or contract asks it to do.
3. **Implemented:** what this submitted version does, including deviations from the requirement.
4. **Assessed:** what the reviewing agent checked and concluded, with evidence and limits.

“Does deleting an account remove pending deliveries?” is incomplete. It must say whether it asks about the baseline, the submitted implementation, or the desired contract. Likewise, a requirement example is not a captured response; an assertion in a test is not proof that the test ran; and a passed suite is not proof that its expectations are appropriate.

The GroupStay M4 example exposes all four accounts. M3 kept historical group totals after cancellation. M4's request changes the fields to active-room totals. M4's code still preserves old totals when the last room is cancelled. Existing tests endorse the historical behavior, but a reviewer test demonstrates the conflict. A human can then add client-compatibility context without obscuring the requirement violation.

## Begin with the whole change

The overview should cover the requested work before narrowing attention to a defect. Otherwise the most interesting finding becomes an accidental description of the entire MR.

Describe breadth through actual operations, modules, data stores, consumers, and dependencies. Describe depth through changes in semantics, state, persistence, migration, transaction boundaries, and recovery. Identify relevant unchanged components as well as changed files. Do not substitute line counts or a generic risk score for this account.

External reach is often unknown. A code snapshot may show a changed response field without revealing which deployed consumers depend on it. State that gap and attach human context to it. Do not invent a consumer inventory.

## Fit into review, whoever authored the change

The primary entry point is an existing MR. Its author need not use Change Lens, the same agent, or any agent at all. A reviewing agent can gather the diff, requirements linked from the MR or issue tracker, repository instructions, architecture material, and author evidence.

The same approach can be used before an MR exists, against a frozen local or cloud working-tree snapshot. Opening an MR is a collaboration boundary, not an essential analysis dependency.

The workflow is:

1. Identify the exact change and gather its requirements and context.
2. Establish the baseline and submitted behavior across the full scope.
3. Conduct the agent's code review under the applicable review instructions.
4. Produce an inspectable account connected to the findings and supporting evidence.
5. Let a human add context, challenge a claim, or direct a change.
6. Give that guidance to the author or reviewer. When code changes, capture the new version and revisit affected claims.

Author evidence is useful but can be absent, incomplete, or incorrect. Missing requirements remain missing; an agent's plausible reconstruction should be labelled as inference.

## Agentic review is part of the workflow

The reviewer still performs substantive engineering work: tracing code, checking contracts, investigating failure cases, and executing tests where useful. Repository-specific instructions can constrain findings, require particular security checks, or discourage speculative redesigns. The instrument should expose that review's scope and evidence, not replace it with a second generic summary.

Keep review instructions separate from reviewed content. Issue text and source comments are material to inspect; they must not silently override the reviewer's governing instructions. Treat imported code as code to inspect, not as something the UI is authorized to execute.

A finding should name a trigger, consequence, violated requirement or contract, source location, and supporting execution or inspection. An unresolved product decision or speculative concern should retain that different status. Human disagreement is recorded alongside the finding rather than silently rewriting its provenance.

A second agent can produce or check the presentation, but agent agreement is not independent proof. Shared models can share assumptions. The strongest support comes from checkable sources and targeted evidence, with clear limits on what was actually checked.

## Agent judgment and deterministic rendering

The agent decides what the change means, which assumptions matter, what to investigate, and how to represent a particular behavior. Deterministic code captures snapshots, computes diffs and hashes, validates references, renders structured content, and preserves notes.

Use the representation that fits the concrete subject. A field table may explain an API change. A state diagram may explain transitions. A request sequence with observed state may explain a failure. A diagram must identify actual states and operations; an interactive model must disclose whether it executes the implementation or merely illustrates an interpretation.

The current prototype uses source-backed tables, contract details, diffs, and recorded test evidence. It does not yet provide a general diagram grammar or agent integration.

## What we learned from the first version

The initial interface wrapped the example in editorial headings and metaphors, such as “What remains when rooms don't?” It hid concrete grounding in a secondary evidence panel and used invented simulations. The user found it less useful than a raw reviewer report: the language and structure introduced ambiguity.

The accepted revision starts from literal requirements, named operations and fields, and baseline/submitted code. Essential evidence appears with each claim. The full M4 request is represented before the cancellation finding. The user reported that this fits a review workflow much better, while reserving judgment pending deeper use.

This is a design direction, not a validated productivity claim. The next test is whether a reviewer can explain the change correctly, locate a missing assumption, and provide useful guidance with less reconstruction. See the [review protocol](../REVIEW_PROTOCOL.md) for a comparative experiment.
