---
name: fix-issue
description: Fix a GitHub issue by number.
disable-model-invocation: true
argument-hint: "[issue-number]"
---

Fix GitHub issue #$ARGUMENTS:

1. Read the issue: `gh issue view $ARGUMENTS`
2. Understand requirements and acceptance criteria
3. Find relevant code in the codebase
4. Implement the fix
5. Write or update tests
6. Create a commit referencing the issue: `fix: description (closes #$ARGUMENTS)`
