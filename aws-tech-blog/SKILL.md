---
name: aws-tech-blog
description: "Write high-quality AWS technical blog posts following the style and structure of the AWS Machine Learning Blog. Supports four blog types: Customer Stories (co-written with customers showcasing real implementations), Feature Launch/Announcements (new AWS capabilities with code samples and IAM policies), Best Practices/Thought Leadership (numbered recommendations with practical guidance), and How-To/Tutorials (step-by-step implementation guides). Use when asked to: write an AWS blog, draft a technical blog post, create a customer story, write a feature announcement, write best practices, or author content for the AWS blog platform."
---

# AWS Technical Blog Writer

## Workflow

1. **Determine blog type** — Ask the user or infer from context:
   - **Customer Story**: A company solved a problem with AWS (see `references/blog-types.md` § Customer Story)
   - **Feature Launch**: Announcing or explaining a new AWS feature (see `references/blog-types.md` § Feature Launch)
   - **Best Practices**: Prescriptive guidance with numbered recommendations (see `references/blog-types.md` § Best Practices)
   - **How-To/Tutorial**: Step-by-step implementation guide (see `references/blog-types.md` § How-To)

2. **Gather inputs** — Collect from the user:
   - Topic and AWS services involved
   - Target audience and technical level (200/300/400)
   - Key technical details, architecture, code samples
   - For customer stories: company name, problem, solution, results, quotes
   - Author names and bios

3. **Read the relevant reference files**:
   - `references/blog-types.md` for the structure template of the chosen blog type
   - `references/style-guide.md` for tone, formatting, and conventions

4. **Draft the blog** following the structure template exactly

5. **Self-review checklist** before delivering:
   - [ ] Title follows the naming pattern for the blog type
   - [ ] Opening paragraph establishes context (not "In today's...")
   - [ ] Thesis paragraph present ("In this post, we explore...")
   - [ ] H2/H3 hierarchy is clean and descriptive
   - [ ] AWS services linked and properly named on first mention
   - [ ] Architecture diagram has text description
   - [ ] Code samples have language identifiers and inline comments
   - [ ] Conclusion has: summary, key takeaways, call to action, resource links
   - [ ] About the Authors section included
   - [ ] No marketing superlatives ("revolutionary", "game-changing")

## Key Conventions

**Opening**: Lead with business context, industry trend, or market data — never "In today's rapidly evolving..."

**Thesis**: Always include "In this post, we explore..." paragraph with bulleted scope.

**Service naming**: Full name on first mention with hyperlink ("Amazon Bedrock AgentCore"), shortened after ("AgentCore").

**Bold label pattern**: `* **Label**: Explanation...` for feature lists and takeaways.

**Customer quotes**: Blockquote with italic, attribution on separate line.

**Diagrams**: Always follow with "The preceding figure illustrates..." and numbered workflow steps.

**Conclusion**: Summary → bullet takeaways → call to action → "For more information" links → references list.

## Output Format

Produce a single markdown file. Use `blog-title.md` as the filename. Structure:

```
## [Category]

# Title

by [Authors] on [Date] in [Categories]

[Body sections per blog type template]

---

### About the authors

[Author bios]
```

## References

- `references/blog-types.md` — Detailed structure templates for each of the 4 blog types
- `references/style-guide.md` — Tone, formatting, headings, code blocks, tables, naming conventions
