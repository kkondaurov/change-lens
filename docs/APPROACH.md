# Approach and rationale

## The problem

The design premise is a workflow in which agents both produce software changes and perform the substantive review: understanding the task, investigating the implementation, assessing its consequences, and checking whether the solution fits. Human participation has to work with that division of labor.

At the limit, such a workflow could become a “dark factory,” with agents implementing, reviewing, approving, and deploying changes. Teams may retain human involvement at different stages and to different degrees. Change Lens explores how people can remain meaningfully involved as more of the work is delegated.

The overarching goal is to preserve the speed of agent-driven development and the quality of its outcomes while allowing people to apply attention and judgment where useful. Quality is defined by the task and environment: security, behavior as workloads grow, reliability, usability, maintainability, and product fit are possible concerns, not a fixed list. The cost of human attention and any delay introduced by the instrument matter alongside those outcomes.

A person may know something the agents do not: a customer dependency, an operational constraint, an intended contract, or a reason an otherwise reasonable design does not fit the project. They may also want to investigate a choice or question the reviewing agent's assessment. The practical problem is finding where to engage and being able to understand that part without reconstructing the entire change first.

In the intended workflow, the required tests and checks for the submitted change have already passed, locally or in CI. That is the starting condition for review. The reviewing agent examines the requirements and the solution's wider consequences, including whether the passing tests cover the right behavior and express the right expectations.

## Decide where to pay attention, then investigate

The instrument must support two connected activities:

1. **Gauge whether and where attention is useful.** Show the problem, the extent and consequences of the change, the agent's assessment, consequential choices, and unresolved assumptions in a form a person can grasp.
2. **Investigate a selected subject.** Let the person follow that subject into its requirements, baseline and submitted behavior, implementation, review rationale, supporting evidence, and relevant checks. They should be able to ask a question, provide context, challenge a conclusion, or direct further work there.

Intervention begins with choosing to pay closer attention; it does not require an already identified defect or a request to stop the work. The whole change and review must remain navigable, including areas the agent considered routine. A human must be able to question the agent's selection of what deserves attention.

The agent carries the review workload. Human use can be selective and occasional, according to the person's judgment and the team's responsibilities. This design does not require a new human approval step for every change. Existing approval requirements remain part of the surrounding process.

## What must remain distinct

For a specific subject, the review needs four separate accounts:

1. **Before:** what the baseline system does.
2. **Required:** what an identified task or contract asks it to do.
3. **Implemented:** what this submitted version does, including deviations from the requirement.
4. **Assessed:** what the reviewing agent checked and concluded, with evidence and limits.

“Does deleting an account remove pending deliveries?” is incomplete. It must say whether it asks about the baseline, the submitted implementation, or the desired contract. A requirement example and a captured response also serve different purposes. For the already passing suite, inspect which behavior its assertions establish and whether that behavior satisfies the current requirements.

The GroupStay M4 example exposes all four accounts. M3 kept historical group totals after cancellation. M4's request changes the fields to active-room totals. M4's code still preserves old totals when the last room is cancelled. Existing tests endorse the historical behavior, but a reviewer test demonstrates the conflict. A human can then add client-compatibility context without obscuring the requirement violation.

## Begin with the whole change

The overview should cover the requested work before narrowing attention to a defect. Otherwise the most interesting finding becomes an accidental description of the entire MR.

Describe what is affected, how far the consequences reach, and how substantially the change alters the system or its assumptions. The reviewing agent chooses the dimensions that matter from the actual task, implementation, environment, and applicable review obligations. The GroupStay examples do not define a universal scope checklist.

For example, an authorization change may need an account of who gains access and which trust boundaries move. A query change may need to show how resource use and latency grow with data volume or concurrent users. A migration may center on compatibility and recovery. Other changes will need different dimensions. These are examples of choosing an account that fits the change, not required categories for every review.

Ground the selected dimensions in concrete implementation and evidence, including relevant unchanged components and assumptions about the environment. Preserve the distinction between what the agent examined and what remains unknown. Line counts or a generic risk score cannot stand in for that account.

External reach is often unknown. A code snapshot may show a changed response field without revealing which deployed consumers depend on it. State that gap and attach human context to it. Do not invent a consumer inventory.

## Fit into review, whoever authored the change

The primary entry point is an existing MR, with an agent doing the review. Although agent-produced software motivates the design, the author need not use Change Lens, the same agent, or any agent at all. The reviewing agent gathers the diff, requirements linked from the MR or issue tracker, repository instructions, relevant system context, and author evidence.

The same approach can be used before an MR exists, against a frozen local or cloud working-tree snapshot. Opening an MR is a collaboration boundary, not an essential analysis dependency.

The workflow is:

1. The agent identifies the exact change and gathers its requirements and context.
2. The agent establishes the problem, the submitted solution, and the dimensions relevant to assessing it.
3. The agent conducts the review under the applicable instructions and investigates concrete questions.
4. The instrument makes the change and review available for human orientation and deeper inspection, connected to their sources and evidence.
5. The human can decide whether and where to engage, then add context, challenge a claim, or direct further work.
6. The author or reviewing agent incorporates that guidance and reports what changed. A new code version requires revisiting affected claims.

Making the account available is not itself a blocking approval gate. How review, human participation, approval, and deployment are scheduled belongs to the team's workflow.

Author evidence is useful but can be absent, incomplete, or incorrect. Missing requirements remain missing; an agent's plausible reconstruction should be labelled as inference.

## Agentic review is part of the workflow

The reviewing agent traces the implementation, assesses relevant consequences, and chooses checks under the repository's review instructions. Existing successful CI or local test results supply baseline evidence. Additional verification addresses concrete gaps, questionable expectations, or failure hypotheses. The instrument exposes that work so a person can understand and influence selected parts of it.

Keep review instructions separate from reviewed content. Issue text and source comments are material to inspect; they must not silently override the reviewer's governing instructions. Treat imported code as code to inspect, not as something the UI is authorized to execute.

A defect finding should name a trigger, consequence, violated requirement or contract, source location, and supporting execution or inspection. Design tradeoffs, unresolved decisions, and unverified concerns should retain their different status. They can be useful points for human attention even when the agent finds no defect. Human disagreement is recorded alongside the assessment rather than silently rewriting its provenance.

A second agent can produce or check the presentation, but agent agreement is not independent proof. Shared models can share assumptions. The strongest support comes from checkable sources and targeted evidence, with clear limits on what was actually checked.

## Agent judgment and deterministic rendering

The agent decides what the change means, which assumptions matter, what to investigate, and how to represent a particular behavior. Deterministic code captures snapshots, computes diffs and hashes, validates references, renders structured content, and preserves notes.

Use the representation that fits the concrete subject and the person's question. A field table may explain an API change; a comparison of access rules may clarify a security change; measured resource use across workloads may explain scaling behavior. These are illustrative options, not a required vocabulary of views. Any representation must stay grounded in the implementation and disclose the assumptions and evidence behind it. An interactive model must identify whether it executes the implementation or illustrates an interpretation.

The current prototype uses source-backed tables, contract details, diffs, and recorded test evidence. It does not yet provide a general diagram grammar or agent integration.

## What we learned from the first version

The initial interface wrapped the example in editorial headings and metaphors, such as “What remains when rooms don't?” It hid concrete grounding in a secondary evidence panel and used invented simulations. The user found it less useful than a raw reviewer report: the language and structure introduced ambiguity.

The accepted revision starts from literal requirements, named operations and fields, and baseline/submitted code. Essential evidence appears with each claim. The full M4 request is represented before the cancellation finding. The user reported that this fits a review workflow much better, while reserving judgment pending deeper use.

This is a design direction, not a validated productivity claim. The next test is whether a person can judge where attention is useful, investigate that subject, and provide effective guidance while preserving delivery speed and the quality criteria relevant to the change. Measure missed issues and unnecessary interventions alongside human attention, review effort, and delay. See the [review protocol](../REVIEW_PROTOCOL.md) for a comparative experiment.
