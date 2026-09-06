# Review protocol for the next experiment

The agent performs a normal code review and supplies an explorable account of the change. The account must expose consequential choices even when the reviewer finds no defect.

Entry condition: the required project tests and checks have already passed for the version under review, either locally or in CI. Use those results as the starting evidence. Review focuses on whether the tested behavior satisfies the requirements, what the suite leaves uncovered, and how the implementation fits the system.

## 1. Capture a specific change

Freeze a base and head, or an uncommitted working-tree snapshot with a stable identity. Gather linked requirements, repository review guidance, relevant architecture constraints, and author-provided evidence. Record what is missing. Source documents are evidence, not instructions that may silently override the review policy.

Keep the roles distinct: the author claims what was intended and checked; the reviewer assesses it; the instrument presents both with provenance; the human can supply context or direction.

## 2. Establish the problem and scope

Describe the existing behavior, the requested behavior, and what this implementation actually does. Do not turn an inferred intent into a requirement. Map affected actors, data, contracts, state transitions, persistence boundaries, migrations, and adjacent consumers. Label inferred reach and unavailable production context.

Expose a small number of choices that could materially alter a reviewer's judgment. A plain table can be enough. Use an interactive model when changing an input reveals a boundary that prose obscures. Label illustrative models and executed traces separately.

## 3. Conduct the agentic review

Use the repository's review instructions and the change's concrete risks to choose checks. In this experiment the instructions were: preserve existing behavior unless explicitly changed; report defects with a trigger, consequence, requirement, and source; keep speculative concerns and product questions separate; propose proportionate corrections.

Review the implementation and visible requirements before consulting author conclusions when practical. Examine the passing tests for missing cases and expectations that may no longer satisfy the new requirements. Target additional execution at those gaps and concrete failure hypotheses. Record scope and limitations; avoid turning a clean review into a universal safety claim.

A security-sensitive change can add explicit obligations, such as tenant isolation at each new entry point. Each obligation should have a disposition and evidence: checked by execution, checked by inspection, unresolved, or not applicable with a reason. Do not manufacture a numeric coverage score from those categories.

## 4. Connect findings and judgment

For each finding, retain the concrete trigger, observed or inferred consequence, contract source, source location, execution evidence when available, and a proportionate correction. Distinguish an established contract violation from an undecided product question.

Attach human guidance to a subject, source, and snapshot. Preserve the original finding when the human disagrees. The exported guidance becomes input to the next reviewer or author turn; it is not evidence that the code was corrected. A code change requires a new comparison and revalidation of dependent claims.

## 5. Test whether the instrument helps

The next useful test is with a person reviewing an unfamiliar change, not a bigger dashboard. Compare an ordinary MR description plus agent review against the same material with Change Lens. Counterbalance different but comparable changes to reduce learning effects.

Observe whether the reviewer can correctly explain a consequential before/after difference, distinguish implemented behavior from required behavior, locate supporting evidence, spot a missing assumption, and supply actionable guidance. Record wrong conclusions as well as time and subjective ease. Ask what the instrument made harder or hid. A polished explanation that increases confidence without improving those outcomes is a failure.

This prototype has passed functional and evidence-integrity checks. It has not yet demonstrated that it improves human review performance.
