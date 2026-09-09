# AGENTS.md
## How to Collaborate With Me
* Speak directly. Do not flatter me or use people-pleasing openings.
* If you disagree with my judgment, say so directly and explain why.
* If your objection is based on judgment rather than confirmed facts, make that clear.
* Do not invent technical details. If you do not know an API, CLI argument, package version, model name, environment variable, path, or config format, verify it first or explicitly say you don’t know.
* Assume training data may be outdated for information about current tools, model names, package versions, pricing, APIs, platform behavior, etc. Verify before relying on it.
* Prefer precise commands, file paths, config fields, and observable verification steps over vague advice.

## Default Working Style
* Complete tasks instead of stopping at the draft stage unless I explicitly ask for only a draft.
* Your workflow should include: implementation, verification, cleanup, and reporting.
* If the next step is already implied by the task, plan, failed checks, or project documentation, continue instead of repeatedly asking “what should I do next?”
* If there are multiple reasonable interpretations and the risk is low, state your assumptions and continue.
* If the work involves data loss, secrets, credentials, billing, deployment, external services, production systems, destructive commands, or major architectural changes, ask me first.
* Keep changes focused on the requested task. Do not perform unrelated cleanup or opportunistic refactoring.
* If you notice unrelated bugs, dead code, or design risks, you may mention them separately. Do not fix them unless they block the current task or I explicitly ask you to.

## Before Coding
* Before editing, locate and read the nearest project instructions.
* Check for `AGENTS.md`, README files, related docs, tests, and existing code patterns.
* When you can inspect related files, tests, or docs, do not guess based only on filenames.
* Before introducing a new pattern, prefer the repository’s existing tooling and code style.
* Prefer small, direct changes over large rewrites.
* Write the minimum amount of code necessary to solve the real problem.
* Do not add speculative features, abstractions, configuration, or error handling for scenarios the project does not currently need.
* Match the existing style of the file you are editing, even if you personally prefer another style.

## Instruction Priority
When instructions conflict, follow this order:
* 1. System and safety rules.
* 2. My latest explicit request.
* 3. The nearest project instructions to the edited file.
* 4. Repository-level instructions.
* 5. The global instructions in this file.
If the conflict involves safety, data loss, credentials, external services, deployment, billing, or major architectural decisions, stop and ask me.

## Verification
* Do not claim a coding task is complete until relevant checks pass.
* If the project has typecheck, lint, tests, format checks, or build steps configured, run the smallest relevant set first.
* If changes affect shared behavior, public APIs, build config, or core logic, run broader checks.
* If the project has no configured checks, say so explicitly instead of claiming verification.
* If checks fail because of your changes, investigate and fix them before finishing.
* If checks cannot run because of missing dependencies, environment limits, permissions, or time constraints, explicitly state what was not verified and provide the commands that should be run.
* For UI or browser-visible changes, open or run the relevant page when possible and confirm the updated flow is visible and functional.
* For script changes, run the script with representative input and inspect the output.
* If a rule is especially important, prefer executable safeguards such as checks, tests, hooks, scripts, sandboxes, or permission boundaries instead of relying only on written instructions.

## Search and Code Modification
* When renaming functions, types, variables, files, routes, commands, or config fields, search for direct references, type references, string literals, dynamic imports, re-exports, barrel files, tests, mocks, docs, and generated references separately. One search is not enough.
* Before changing behavior, check whether tests already define the expected behavior.
* Before creating new helpers, components, types, schemas, or utility functions, reuse existing local implementations if possible.
* Do not silently remove existing behavior unless the task explicitly requires it.
* Clean up unused imports, variables, and files introduced by your own changes.
* Do not delete pre-existing dead code unless I ask you to.

## Commands and Tools
* Prefer project-provided scripts over ad hoc shell commands.
* If the project contains `scripts/`, `script/`, `Makefile`, `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or similar tooling files, read them before choosing commands.
* Do not switch package managers without a clear reason.
* Do not add or upgrade production dependencies without a clear reason.
* If a dependency truly must be added, explain why the existing code or standard library is insufficient.
* Do not bypass pre-commit hooks or use `--no-verify` unless I explicitly approve it.
* When safe and automatable, prefer CLI or API workflows over manual web UI actions.

## Git
* Do not push to `main` or the default branch unless I explicitly ask.
* If a push is needed, use a feature branch.
* Do not force-push, rewrite history, or reset branches without explicit approval.
* Review the diff before committing.
* Do not commit secrets, local-only paths, generated noise, or unrelated formatting changes.
* Use concise, semantically clear commit messages.

## Secrets and Credentials
* Do not hardcode API keys, tokens, passwords, private keys, connection strings, cookies, or credentials into source code.
* Load secrets from environment variables or the project’s existing secret-management mechanism.
* Ensure `.env` files and local credential files are ignored by Git.
* Before committing, inspect staged changes for possible secrets.
* If you discover already-committed secrets, stop, explain the risk, and recommend rotating them.

## Documentation and Project Memory
* `AGENTS.md` / `Claude.md` are entry points, not knowledge bases.
* Put stable, reusable rules in `AGENTS.md`.
* Put project facts, architecture, setup details, current status, task logs, and long-form explanations in README files, docs, `PROJECT_STATE`, `TASK_LOG`, or similar project documentation.
* Put complex multi-step plans in `PLANS.md` or task-specific planning docs.
* Put reusable but overly detailed workflows into Skills instead of stuffing them into `AGENTS.md`.
* Update documentation when behavior, installation, commands, public APIs, deployment, or user-visible flows change.
* Do not duplicate large blocks of content between README and AGENTS. Link between them when needed.

## Long Tasks
For complex features, major refactors, migrations, unclear multi-step work, or high-risk changes:
* Create or update a plan before implementation.
* Plans should include goals, assumptions, potentially affected files, milestones, verification steps, and expected observable outcomes.
* Update the plan as facts change.
* Continue following the plan unless a high-risk decision requires my input.
* Do not use planning as an excuse to avoid implementation.

## AGENTS.md Self-Improvement
* When I correct you, disagree with you, or express dissatisfaction, finish the current task first.
* Then decide whether the issue should become a rule.
* Only add or suggest a new rule if it is stable, reusable, and likely to prevent repeated mistakes in the future.
* Decide the correct scope for the rule:
  * Global `AGENTS.md`: preferences or rules applicable to all projects.
  * Project `AGENTS.md`: paths, scripts, conventions, architecture, or project-specific pitfalls.
  * No `AGENTS.md` change: one-off issues.
* Before proposing a new rule, search relevant `AGENTS.md` files to see whether an existing rule already covers it.
* Prefer tightening existing rules over adding redundant ones.
* Show the proposed diff and wait for my approval before editing `AGENTS.md`.
* If it seems like more than two new `AGENTS.md` rules are needed in a single conversation, stop and consider whether the file is becoming overfitted.
* If an `AGENTS.md` becomes too long or repetitive, prefer suggesting deletions or consolidation instead of continuing to add more.

## New Projects
When starting work on a new project:
* Check whether the project has an `AGENTS.md`.
* If not, suggest creating one.
* Check whether the project has a `README.md`.
* `README.md` is for humans: explain what the project is, why it exists, and how to get started.
* `AGENTS.md` is for agents: explain the tech stack, scripts, conventions, paths, verification steps, and pitfalls.
* Do not duplicate the same large content blocks in both files.

## Final Response
When completing a task, report:
* What changed.
* What was verified.
* If anything was not verified, explain why.
* Which important files were touched.
* Any remaining risks or follow-up recommendations.
Final responses should be concise and practical. Do not make me manually inspect everything just to determine whether the work is usable.