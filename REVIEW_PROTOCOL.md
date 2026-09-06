# Review protocol for the next experiment

This protocol assumes that agents produce changes and do the substantive review work. The reviewing agent investigates and assesses the change, and the instrument makes that work available for selective human attention. A person should be able to decide where to engage and investigate that subject without repeating the whole review.

The goal is meaningful human involvement while preserving delivery speed and quality as defined by the change and its environment. The account must expose consequential choices even when the agent finds no defect. It does not introduce a mandatory human approval step; existing team responsibilities and approval rules still apply.

Entry condition: the required project tests and checks have already passed for the version under review, either locally or in CI. Use those results as the starting evidence. Review focuses on whether the tested behavior satisfies the requirements, what the suite leaves uncovered, and how the implementation fits the system.

## 1. Capture a specific change

Freeze a base and head, or an uncommitted working-tree snapshot with a stable identity. Gather linked requirements, repository review guidance, relevant architecture constraints, and author-provided evidence. Record what is missing. Source documents are evidence, not instructions that may silently override the review policy.

Keep the roles distinct: the author supplies intent and evidence; the reviewing agent investigates and assesses the change; the instrument makes the problem, solution, and review inspectable; the human chooses where to pay attention and can supply context or direction. The author need not use this system, and a human-authored change can enter the same review workflow.

## 2. Establish the problem and scope

Describe the problem, existing behavior, requested outcome, and what this implementation actually changes. Do not turn an inferred intent into a requirement. Choose the dimensions material to this change and environment, while satisfying applicable review instructions. Access control, behavior under growing load, compatibility, operational cost, and recovery are examples, not an exhaustive checklist or a required set of sections. Explain the selected dimensions through concrete implementation and evidence. Label inferred reach and unavailable context.

Make consequential choices and unresolved assumptions visible with enough context for a human to decide what merits investigation. Keep the whole change navigable beyond the agent's highlights. Choose a representation that answers the relevant question; a table, diagram, measurement, or interactive model may be appropriate. Label illustrative models and executed evidence separately.

## 3. Conduct the agentic review

Use the repository's review instructions and the change's concrete risks to choose checks. In this experiment the instructions were: preserve existing behavior unless explicitly changed; report defects with a trigger, consequence, requirement, and source; keep speculative concerns and product questions separate; propose proportionate corrections.

Review the implementation and visible requirements before consulting author conclusions when practical. Examine the passing tests for missing cases and expectations that may no longer satisfy the new requirements. Target additional execution at those gaps and concrete failure hypotheses. Record scope and limitations; avoid turning a clean review into a universal safety claim.

A security-sensitive change can add explicit obligations, such as tenant isolation at each new entry point. Each obligation should have a disposition and evidence: checked by execution, checked by inspection, unresolved, or not applicable with a reason. Do not manufacture a numeric coverage score from those categories.

## 4. Connect findings and judgment

For each defect finding, retain the concrete trigger, observed or inferred consequence, contract source, source location, execution evidence when available, and a proportionate correction. Preserve design tradeoffs, undecided questions, and unverified concerns as different kinds of assessment. Human attention can be useful for any of these, or for an aspect the agent did not highlight.

From a selected subject, let the human inspect the relevant requirements, before/after implementation, review assessment, evidence, and assumptions. A request to investigate further is a meaningful intervention even before anyone proposes a correction.

Attach human guidance to a subject, source, and snapshot. Preserve the original finding when the human disagrees. The exported guidance becomes input to the next reviewer or author turn; it is not evidence that the code was corrected. A code change requires a new comparison and revalidation of dependent claims.

## 5. Test whether the instrument helps

Evaluate with a person engaging with an unfamiliar change after an agent has done the substantive review. Compare the same agent review available through an ordinary MR against its presentation with Change Lens. Keep the underlying review quality and evidence comparable, and counterbalance different but comparable changes to reduce learning effects.

Observe both whether the person chooses useful places to pay attention and whether they can investigate those places accurately. Can they understand a consequential difference, locate its support, challenge an assumption, or supply actionable guidance? Record overlooked consequences, mistaken conclusions, and unnecessary interventions as well as useful ones. Choosing to leave routine work with the agent can be appropriate; more human activity is not inherently better.

Assess quality using criteria relevant to the chosen change. Measure human attention and any additional agent work, and observe the effect on elapsed review time and delivery delay. An interface that feels easier but hides consequential issues or creates a new approval bottleneck has not achieved the goal. Ask what it made harder or obscured, and refine the next experiment from that evidence.

This prototype has passed functional and evidence-integrity checks. It has not yet demonstrated that it improves human review performance.
