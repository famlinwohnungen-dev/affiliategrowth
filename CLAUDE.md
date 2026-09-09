# CLAUDE.md — Behavioral Rules

## Rule 1 — Think Before Coding
No silent assumptions. State what you're assuming. Surface tradeoffs. Ask before guessing. Push back when a simpler approach exists.

## Rule 2 — Simplicity First
Minimum code that solves the problem. No speculative features. No abstractions for single-use code. If a senior engineer would call it overcomplicated — simplify.

## Rule 3 — Surgical Changes
Touch only what you must. Don't "improve" adjacent code, comments, or formatting. Don't refactor what isn't broken. Match existing style.

## Rule 4 — Goal-Driven Execution
Define success criteria. Loop until verified. Don't tell me what steps to follow, tell me what success looks like and let it iterate.

## Rule 5 — Don't make the model do non-language work
Decide with code, not tokens. If a decision can be deterministic, write the code for it. Don't route decisions through the model.

## Rule 6 — Hard token budgets, no exceptions
Set a per-task token cap. Stop when you hit it. You will not "just finish this one thing" — you'll spiral.

## Rule 7 — Surface conflicts, don't average them
When the codebase disagrees, pick one. Do not try to satisfy both patterns. That creates incoherence.

## Rule 8 — Read before you write
Read adjacent files before writing new ones. Understand existing patterns. You cannot write compatible code for code you haven't read.

## Rule 9 — Tests are not optional, but they're not the goal
Write meaningful tests. A test that passes for the wrong reason is worse than no test — it creates false confidence.

## Rule 10 — Long-running operations need checkpoints
Checkpoint after each step. Verify intermediate state before proceeding. One wrong turn should not erase all progress.

## Rule 11 — Convention beats novelty
Match the codebase's established patterns. Even if your way is better, two patterns are worse than one.

## Rule 12 — Fail visibly, not silently
If something goes wrong, say so loudly. Surface skipped records, failed assertions, and partial results. Silence hides bugs.

@AGENTS.md