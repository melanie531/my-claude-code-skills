# AWS Blog Style Guide

## Tone and Voice

- **Professional but accessible**: Balance technical depth with readability. Assume the reader is technical but may not know the specific service.
- **Confident, not salesy**: State what the service does and why it matters. Avoid superlatives like "revolutionary" or "game-changing". Let the technical merits speak.
- **Active voice**: "Amazon Bedrock routes requests" not "Requests are routed by Amazon Bedrock".
- **Direct address**: Use "you" and "your" when addressing the reader. Use "we" when describing what the blog covers.
- **Present tense for capabilities**: "AgentCore Runtime provides isolation" not "AgentCore Runtime will provide".

## Opening Paragraph Patterns

**Pattern 1 — Industry trend lead (Customer Stories, Announcements)**:
"Organizations are increasingly [doing X] to [achieve Y]. As [workloads/adoption] continue to grow, organizations face new challenges in [specific challenge area]."

**Pattern 2 — Problem-first lead (Best Practices, How-Tos)**:
"Building production-ready [thing] requires careful planning and execution across [scope]. The difference between a [demo] and [production system] is [key differentiator]."

**Pattern 3 — Market data lead (Customer Stories)**:
"[Specific statistic from report]. [Second supporting statistic]. In practice, businesses face two common challenges: [bullet 1] and [bullet 2]."

## Thesis Paragraph

Every blog must include a thesis paragraph, typically the last paragraph of the introduction. Format:

"In this post, we explore [what]. We cover [N] key aspects:"
- Bullet 1
- Bullet 2
- Bullet 3

Or: "In this post, we explore how [X] works, the benefits it offers compared to [Y], and how you can implement it in your own applications."

## Headings

- **H1**: Blog title only (one per post)
- **H2**: Major sections. Use descriptive, active phrases. Examples:
  - "Setting up strong data foundations"
  - "Core functionality of global cross-Region inference"
  - "Start small and define success clearly"
- **H3**: Subsections within H2. Examples:
  - "Understanding inference profiles"
  - "Why code execution matters"
  - "CLAUDE.md (project context)"
- **H4**: Rare. Use for sub-subsections only when H3 nesting is deep.

## Formatting Conventions

### Bold
- Use for emphasis on key terms at first introduction: "**session isolation**"
- Use for label+explanation pattern: "**Stateful execution session**: AgentCore maintains..."
- Use in table headers

### Italic
- Customer quotes: *"Quote text"*
- First mention of a document or tool name: *single source of truth*

### Bullet Lists
Use for:
- Feature lists with bold labels
- Key benefits
- Prerequisites
- Key takeaways

Format: `* **Bold label** – Explanation that follows on the same line.`

Or without labels: `* Simple point without emphasis needed.`

### Numbered Lists
Use for:
- Sequential workflow steps
- Step-by-step instructions
- Ordered processes

### Tables
Use for:
- Feature comparisons (columns: Feature, Option A, Option B)
- Tool documentation (columns: Element, Purpose, Example)
- Agent definitions (columns: Component, Details)
- Always include header row

### Code Blocks
- Use fenced blocks with language identifier: ```python, ```json, ```bash
- Add inline comments for important lines
- Keep samples minimal — show only what's needed
- Include output handling when relevant

### Links
- Hyperlink on first mention of an AWS service: [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- Link to documentation for technical terms
- Use descriptive link text, not "click here"
- External links (non-AWS) are acceptable for partners, open-source projects

## Architecture Diagrams

- Always include a detailed text description (alt text) for accessibility
- Describe: components, data flow direction, numbered steps, connections
- Reference the diagram: "The following diagram illustrates..." or "As shown in the preceding figure..."
- Follow up with numbered workflow explanation

## Customer Quotes

Use blockquote format with italic:

```markdown
> *"Quote that adds business insight or validates the technical choice."*
>
> *– Full Name, Title at Company*
```

Place after the relevant technical section, not at the beginning.

## Conclusion Section

Must include:
1. **Summary sentence**: What the blog demonstrated
2. **Key takeaways or recap**: Bullet list of main points
3. **Call to action**: "Get started by exploring...", "We encourage you to try..."
4. **Resource links**: Documentation, GitHub repos, workshops, demos
5. **"For more information" links**: 3-5 relevant documentation pages

## References Section (Customer Stories)

Bullet list of key resources mentioned in the post:
```markdown
* [Service Name](URL)
* [Feature Name](URL)
```

## About the Authors Section

One paragraph per author:
- **Bold name** followed by title and company/org
- 2-3 sentences: role focus, relevant experience, prior background
- Accompany with a professional headshot

Example:
```markdown
**Melanie Li**, PhD, is a Senior Generative AI Specialist Solutions Architect at AWS based in Sydney, Australia, where her focus is on working with customers to build solutions leveraging state-of-the-art AI and machine learning tools.
```

## AWS Service Naming

- Full name on first mention: "Amazon Bedrock AgentCore"
- Can shorten on subsequent mentions: "AgentCore"
- Always capitalize AWS service names
- Use official naming: "Amazon S3" not "S3" on first mention; "Amazon Bedrock" not "Bedrock" on first mention
- Link to service page on first mention

## Common Anti-Patterns to Avoid

- Starting with "In today's rapidly evolving..." or similar cliches
- Overly long introductions before getting to the technical content
- Code samples without context or explanation
- Missing thesis paragraph
- Architecture diagrams without text descriptions
- Conclusion without actionable next steps
- Using "simple" or "easy" to describe implementation steps
- Marketing language: "revolutionary", "cutting-edge", "seamless" (unless quoting)
