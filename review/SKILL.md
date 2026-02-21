---
name: review
description: Review code for bugs, security issues, and best practices. Use when asked to review code, check for issues, or audit a file.
---

Review the code and check for:

1. **Bugs** - Logic errors, off-by-one, null/undefined, race conditions
2. **Security** - Injection, XSS, hardcoded secrets, insecure defaults
3. **Performance** - N+1 queries, unnecessary allocations, missing indexes
4. **Readability** - Naming, complexity, dead code, missing error handling

Format: list issues as `[SEVERITY] file:line - description`. Severity: CRITICAL, WARNING, INFO.
End with a summary: total issues found, overall assessment.
