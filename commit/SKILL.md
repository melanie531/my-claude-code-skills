---
name: commit
description: Create a well-formatted git commit with conventional commit style.
disable-model-invocation: true
argument-hint: "[optional message override]"
---

Create a git commit:

1. Run `git diff --staged` to see what's staged
2. If nothing staged, run `git diff` and suggest what to stage
3. Write a commit message following Conventional Commits:
   - Format: `type(scope): description`
   - Types: feat, fix, docs, style, refactor, test, chore, perf, ci
   - Keep subject line under 72 characters
   - Add body if changes need explanation
4. Show the message for approval before committing
