# Writing Conventions and Style Guide

Extracted from analysis of chapters 1-5 of "Architecting Generative AI Applications on AWS".

---

## Chapter Structure Template

Every chapter follows this exact structure:

```
[Chapter Number]

[Chapter Title]

[Opening description paragraph - 50-100 words summarizing what the chapter covers
and what the reader will learn. Written in third person about the reader.]

In this chapter we're going to cover the following main topics:

- [Heading 1 title]
- [Heading 2 title]
- [Heading 3 title]
- [Heading 4 title]
- [Heading 5 title (if applicable)]

Let's get started!

[Heading 1 title]

[Content...]

[Heading 2 title]

[Content...]

...

Summary

[2-4 paragraph summary of key takeaways]

References

[1] Author, Title, URL
[2] Author, Title, URL
...
```

## Opening Description Paragraph

- Written in third person referring to reader types ("Solution architects will learn...", "Readers will understand...", "Architects will learn to...")
- States what the chapter covers and what the reader gains
- 50-100 words
- Matches the DESCRIPTION from the outline

**Example (Chapter 1)**:
> This chapter provides solution architects with essential knowledge of generative AI technologies, covering the complete spectrum from foundation models to enterprise applications. Readers will understand GenAI capabilities, explore real-world use cases across industries, and gain familiarity with the AWS GenAI ecosystem that enables scalable, production-ready implementations.

## Topic List

- Always preceded by: `In this chapter we're going to cover the following main topics:`
- Bullet list using `-` markers
- Each item matches a main heading title
- Always followed by: `Let's get started!`

## Heading Hierarchy

- **Main chapter headings**: No markdown prefix in docx (rendered as major sections). In markdown, use `#` or `##`.
- **Subheadings**: Use `###` for subsections within main headings
- **Sub-subheadings**: Use `####` with italic formatting for deeper sections (e.g., `#### *Pillar 1: Application and System Health*`)

## Tone and Voice

- **Perspective**: Written for solution architects / enterprise architects
- **Register**: Technical but accessible. Not academic, not casual.
- **Authority**: Authors write as experienced practitioners sharing knowledge. Use phrases like "For a solution architect, this means..." or "Architects must..."
- **Engagement**: Conversational transitions between sections. Use "Let's" and "we" to include the reader.
- **Stance**: Prescriptive where appropriate ("Architects must design..."), advisory elsewhere ("Organizations should consider...")

## Key Writing Patterns

### Prose-First Approach
- **Write in flowing paragraphs as the default.** This is a book, not a reference card. Explain concepts, motivations, trade-offs, and implementation guidance through connected prose.
- Reserve bullet/numbered lists for genuinely enumerable items (service lists, sequential steps, feature comparisons). Lists should be the exception (~20-30% of content), not the primary structure.
- Each paragraph should develop one idea and transition naturally to the next.
- Weave technical details into narrative rather than breaking to bullet points. Prefer "Amazon SQS provides reliable message queuing that decouples producers from consumers, enabling each tier to scale independently" over a bullet list of SQS features.
- Target ratio: ~70-80% prose paragraphs, ~20-30% lists/tables/code blocks.

### Introductory Sections
- Start with context or motivation (why this matters)
- Move from broad context to specific technical detail
- Connect back to the architect's role and decision-making

### Technical Content
- Define key terms when first introduced, using **bold** for the term
- Use bullet lists sparingly — only for genuinely enumerable items or scan-friendly comparisons
- Use numbered lists only for sequential processes or ranked items
- Include architecture diagrams referenced as `Figure N: [description]`
- Cite sources with `[N]` inline reference numbers

### AWS Services
- Always use full service names on first mention: "Amazon Bedrock", "Amazon SageMaker AI", "AWS Lambda"
- Can abbreviate after first mention in a section
- Link to AWS documentation where relevant
- Include specific metrics/numbers from AWS documentation (e.g., "up to 40% better price-performance")

### Examples and Practical Guidance
- Use concrete examples tied to real enterprise scenarios
- Include code examples or configuration snippets where applicable
- Reference specific AWS features with practical implementation notes
- Use "For example" to introduce illustrative scenarios

### Transitions Between Sections
- Brief connecting paragraph at the end of major sections
- Link current topic to next topic
- Reinforce the architectural perspective

## Formatting Conventions

- **Bold** for key terms, important concepts, and service names on first use
- *Italic* for emphasis, publication titles, and sub-subheading labels
- Bullet lists with `-` for unordered items
- Numbered lists with `1.`, `2.`, etc. for ordered/sequential items
- Code blocks with triple backticks for code/config examples
- References section at the end using `[N]` numbered format
- Figures referenced as `Figure N: [title]`

## Figure and Diagram Conventions

Existing chapters use figures extensively. Observed patterns:

### Figure Types Used in Chapters 1-5
- **Architecture diagrams**: AWS service layouts showing how components connect (e.g., 3-tier architecture, serverless inference, hub-and-spoke patterns)
- **Comparison diagrams**: Side-by-side visuals of traditional vs GenAI approaches
- **Flow diagrams**: Request/response flows, data pipelines, deployment workflows
- **Component diagrams**: Internal structure of systems (e.g., model layers, monitoring pillars)
- **Tables as figures**: Decision matrices, service comparison tables, metric summaries

### Figure Reference Format
In the text, figures are referenced as:
```
Figure N: [Descriptive title]
```

Example from Chapter 2:
> Figure N: 3-tier architecture

Example from Chapter 5:
> Figure N: Serverless GenAI inference architecture

### Figure Placement Guidelines
- Place figures immediately after the paragraph that introduces or references them
- Every figure must be referenced in the body text before it appears
- Include a brief caption below the figure
- Aim for at least 1 figure per main heading section
- Architecture overview figures typically appear near the start of a section
- Detailed component diagrams appear alongside the technical explanation

### Figure Density by Chapter Type
| Chapter Type | Figures per Chapter |
|-------------|-------------------|
| Overview/introductory (Basic) | 3-5 figures |
| Architecture/design (Intermediate) | 5-8 figures |
| Implementation/advanced | 6-10 figures (including code diagrams) |
| Well-Architected pillars | 3-5 figures |

## Content Depth by Level

| Level | Approach |
|-------|----------|
| Basic | Define concepts, explain why they matter, provide overview |
| Intermediate | Architecture patterns, AWS service selection, implementation guidance |
| Advanced | Detailed implementation, performance optimization, production considerations |

## Summary Section

- 2-4 paragraphs recapping the chapter's key points
- Follows the heading order of the chapter
- Concise but covers all major topics
- Ends by connecting to the next chapter or broader book themes
- No "In conclusion" or similar phrasing -- just starts summarizing

## References Section

- Numbered references at chapter end: `[N] Author, Title, URL`
- **Reference diversity is critical** — the book must cite authoritative sources beyond AWS:
  - AWS documentation and blog posts (service docs, user guides, architecture blogs)
  - Research papers (arXiv, ACM, IEEE — for foundational concepts, benchmarks, evaluations)
  - Industry articles and tech blogs (Martin Fowler, InfoQ, ThoughtWorks, O'Reilly, etc.)
  - Books and standards (seminal works, NIST/ISO standards where relevant)
  - Open-source projects and community resources (GitHub repos, framework docs)
- Aim for **at least 30% non-AWS references** per chapter to establish credibility
- Referenced inline with `[N]` notation
- Include author names where available for non-AWS sources (e.g., `[3] Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," arXiv:2005.11401`)

## Page Counts and Length

Chapters range from 10-45 pages. The outline specifies target page counts per chapter. As a rough guide:
- 10-15 pages ≈ 4,000-6,000 words
- 20-25 pages ≈ 8,000-10,000 words
- 28-32 pages ≈ 11,000-13,000 words
- 36-45 pages ≈ 14,000-18,000 words

## Author Attribution

Some headings in the outline have author tags `[ML]` (Melanie Li) or `[DC]` (Derrick Choo) indicating primary author responsibility. When writing, maintain a consistent voice regardless of attribution.
