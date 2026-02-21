---
name: write-chapter
description: >
  Write new chapters for the book "Architecting Generative AI Applications on AWS".
  Follows the established outline, writing conventions, and chapter structure from
  existing chapters 1-5. Use when asked to write, draft, or continue writing a
  chapter, generate chapter content, or produce book sections. Also use when asked
  to review or revise existing chapter drafts for consistency with the book's style.
---

# Write Chapter

Write chapters for "Architecting Generative AI Applications on AWS" by Melanie Li and Derrick Choo (Packt Publishing). Chapters 1-5 exist. Chapters 6-23 need to be written.

## Workflow

Writing a chapter involves these steps:

1. Identify the target chapter and plan sections
2. Load the outline and conventions references
3. Research current AWS documentation for accuracy
4. Draft the chapter incrementally, one heading at a time
5. Generate or place figures
6. Assemble and output as .docx file

### Step 1: Identify the Target Chapter and Plan Sections

Determine which chapter to write from the user's request. If ambiguous, ask which chapter number (6-23). Reference [book-outline.md](references/book-outline.md) for the full outline.

After identifying the chapter, create a **section plan** — a list of all the sections to write, based on the outline's headings and sub-topics. Present this plan to the user before writing, showing:
- Each main heading and its sub-topics
- Estimated word count per heading (divide the chapter's total target evenly, weighted by complexity)
- Which figures/diagrams are needed per section
- The writing order (sequential, heading by heading)

### Step 2: Load References

Read both reference files to understand the chapter requirements and writing style:
- [book-outline.md](references/book-outline.md) — chapter description, headings, skills learned, page count, difficulty level
- [writing-conventions.md](references/writing-conventions.md) — chapter structure template, tone, formatting rules

### Step 3: Deep Research Before Writing

**Do not start writing until research is complete.** Each chapter must be grounded in diverse, authoritative sources — not just AWS documentation. Run broad research across multiple source types to gather technical depth, real-world perspectives, and academic rigor.

#### 3a. Broad Web Research (scripts/web_search.py and scripts/deep_research.py)

Use the bundled research scripts to search the open web for each major heading topic:

```bash
# Quick search on a specific topic
python3 scripts/web_search.py "topic query" --max-results 10

# Deep research across academic, blog, industry, and general sources
python3 scripts/deep_research.py "topic 1" "topic 2" "topic 3" --output /tmp/ch_NN_research.json
```

For each chapter heading, search for:
- **Academic papers** (arXiv, Google Scholar) — foundational concepts, evaluation frameworks, benchmarks
- **Tech blogs and articles** (Martin Fowler, ThoughtWorks, InfoQ, Medium, dev.to) — architecture patterns, real-world experiences
- **Industry reports** (Gartner, Forrester, McKinsey) — enterprise adoption, trends, case studies
- **Open-source projects** (GitHub) — reference implementations, tools, frameworks
- **Conference talks and whitepapers** — emerging best practices

After running searches, use `WebFetch` to read the most relevant pages in detail and extract key insights, statistics, and quotable findings.

#### 3b. AWS Documentation Research

Use the AWS knowledge tools for AWS-specific accuracy:
- `mcp__aws-knowledge__aws___search_documentation` — search across AWS docs, blogs, and guides
- `mcp__aws-knowledge__aws___read_documentation` — read specific AWS doc pages in full
- Verify service names, features, pricing models, and recent updates

#### 3c. Compile Research Brief

Before writing, compile a research brief listing the key references found for each heading:
- At least 3-5 non-AWS references per chapter (research papers, industry blogs, books, standards)
- At least 5-8 AWS references per chapter (docs, blogs, whitepapers)
- Save the brief to `/tmp/chapter_NN_research_brief.md` for reference during writing

#### Reference Diversity Requirements

The References section at chapter end must include a mix of source types:
- **AWS documentation** — official service docs, user guides
- **AWS blog posts** — architecture blogs, ML blogs, compute blogs
- **Research papers** — arXiv, ACM, IEEE papers on relevant topics
- **Industry articles** — tech blogs (Martin Fowler, InfoQ, etc.), vendor-neutral analysis
- **Books and standards** — seminal books, industry standards (NIST, ISO, etc.)

Aim for at least 30% non-AWS references. This gives the book credibility beyond being an AWS marketing document.

### Step 4: Draft the Chapter Incrementally

**Chapters are too long to write in a single output.** Write one main heading at a time, appending each section to a working markdown file.

#### Incremental Writing Process

1. **Start the file** — Write the chapter opening (number, title, description, topic list, "Let's get started!") and save to `/tmp/chapter_NN_draft.md`
2. **Write Heading 1** — Draft the full content for the first main heading with all its sub-sections. Append to the draft file.
3. **Write Heading 2** — Draft the next heading. Append to the draft file.
4. **Continue** — Repeat for each remaining heading. Each append should write 1,500-3,000 words covering one main heading thoroughly.
5. **Write Summary and References** — Append the Summary section (2-4 paragraphs) and the References list.
6. **Confirm progress** — After each heading, briefly tell the user which sections are done and which remain.

Use this pattern for appending to the draft:
```bash
cat >> /tmp/chapter_NN_draft.md << 'SECTION_EOF'
[section content here]
SECTION_EOF
```

#### Word Count Targets per Heading

Distribute the chapter's total word count across headings based on the outline. For a 30-page chapter (~12,000 words) with 4 headings:
- Opening + topic list: ~300 words
- Each heading: ~2,500-3,000 words (adjust based on sub-topic count)
- Summary: ~400 words
- References: ~200 words

If a heading has many sub-topics in the outline, allocate more words. If it is an overview heading, allocate fewer.

#### Content Guidelines

- Write for the difficulty level specified in the outline (Basic / Intermediate / Advanced)
- Target the page count from the outline (rough guide: 1 page ≈ 400 words)
- Cover all headings and sub-topics listed in the outline for that chapter
- Address all "skills learned" items — the reader should gain each skill by chapter end
- Use concrete enterprise examples tied to AWS services
- Cite sources with `[N]` inline, list in References section
- Use **bold** for key terms on first use
- Maintain the prescriptive-but-advisory tone: "Architects must..." / "Organizations should consider..."
- Always use full AWS service names on first mention (Amazon Bedrock, Amazon SageMaker AI, etc.)

#### Prose-First Writing Style

Write in **flowing paragraphs** as the primary format — this is a book, not a slide deck. Convey information through narrative prose that explains concepts, connects ideas, and guides the reader through the architect's thought process.

- **Default to paragraphs.** Explain concepts, patterns, trade-offs, and guidance in connected prose. Each paragraph should develop one idea and transition naturally to the next.
- **Reserve bullet/numbered lists for**: genuinely enumerable items (e.g., 5 specific AWS services), sequential steps in a process, or comparison/feature lists where scanning is more useful than reading. Lists should be the exception, not the default structure.
- **Avoid "list-heavy" sections** where every subsection is just a bold term followed by a bullet list. Instead, weave the explanation into flowing text. For example, instead of listing 4 bullet points about a pattern, write 2-3 paragraphs that explain the pattern, its motivation, and how to implement it on AWS.
- **Use inline examples** within paragraphs rather than breaking to a list. e.g., "Services such as Amazon SQS and Amazon EventBridge can decouple the components, allowing each to scale independently" rather than a bullet list of services.
- **Target ratio**: Roughly 70-80% prose paragraphs, 20-30% lists/tables/code. If a section is mostly bullets, rewrite the core content as paragraphs and keep only truly list-worthy items as lists.

#### Consistency with Existing Chapters

- Read any existing chapters that are referenced or built upon by the target chapter
- The existing chapters are in the working directory as `chapter_01.docx` through `chapter_05.docx`
- Convert with `pandoc chapter_NN.docx -o /tmp/chNN.md` to read
- Avoid repeating content already covered; reference earlier chapters instead (e.g., "As discussed in Chapter 3...")

### Step 5: Generate or Place Figures

Chapters need visual figures — architecture diagrams, flow charts, comparison tables, and system diagrams. Handle figures using this priority order:

#### Option A: Generate Diagrams (Preferred When Possible)

For architecture diagrams, flowcharts, and system diagrams, generate them programmatically:

1. **Mermaid diagrams** — Write Mermaid syntax in a `.mmd` file, then render:
   ```bash
   npx -y @mermaid-js/mermaid-cli mmdc -i diagram.mmd -o figure_N.png -t neutral -b white -w 1200
   ```
   Good for: flowcharts, sequence diagrams, component diagrams, state diagrams, class diagrams.

2. **Python with matplotlib/diagrams** — For custom architecture diagrams:
   ```bash
   pip install diagrams matplotlib
   python3 generate_figure.py
   ```
   The `diagrams` library can create AWS architecture diagrams using official AWS icons.

3. **HTML/CSS rendered to image** — For comparison tables or styled visual content, create an HTML file and convert:
   ```bash
   npx -y puppeteer-html2img --input figure.html --output figure_N.png --width 1200
   ```

After generating, reference the image in the markdown draft:
```markdown
![Figure N: Description of the diagram](figures/figure_N.png)

Figure N: Description of what the diagram shows
```

Store generated figures in a `figures/` directory in the working directory:
```bash
mkdir -p /Users/mmelli/Documents/personal/book/figures
```

#### Option B: Descriptive Placeholders (When Generation Is Not Feasible)

For complex diagrams that cannot be reliably generated (hand-drawn style, highly custom layouts), insert a detailed placeholder that an illustrator or the author can use to create the final figure:

```markdown
<!-- FIGURE PLACEHOLDER
Figure N: [Title]
Type: [Architecture diagram / Flowchart / Comparison table / Sequence diagram / System diagram]
Description: [Detailed description of what the figure should show]
Components:
- [Component 1]: [What it represents and its position]
- [Component 2]: [What it represents and its position]
- [Arrow/Connection 1]: [From → To, what it represents]
Layout: [Left-to-right / Top-to-bottom / Hub-and-spoke / etc.]
AWS Services shown: [List specific AWS service icons to include]
Notes: [Any additional visual guidance]
-->

*Figure N: [Title] — [One-sentence description for the reader]*
```

#### Figure Planning

During Step 1 (section planning), identify all figures needed for the chapter:
- Architecture overview diagrams (1-2 per chapter)
- Component/service interaction diagrams (1-3 per major heading)
- Comparison tables for decision-making sections
- Flow diagrams for process/workflow sections
- At minimum, aim for **1 figure per main heading** to break up text and aid comprehension

Number figures sequentially within each chapter: Figure 1, Figure 2, etc.

### Step 6: Assemble and Output as .docx

After all sections and figures are complete:

1. **Review the full draft** — Read `/tmp/chapter_NN_draft.md` end-to-end and check for:
   - Smooth transitions between sections
   - Consistent terminology
   - No duplicate content
   - All outline headings and skills covered
   - Figure references match actual figures
2. **Convert to .docx** — Use pandoc with figure embedding:
   ```bash
   cd /Users/mmelli/Documents/personal/book
   pandoc /tmp/chapter_NN_draft.md -o chapter_NN.docx --resource-path=figures
   ```
3. **Save** as `chapter_NN.docx` in the working directory (e.g., `chapter_06.docx`)

## Partial Chapter Writing

If the user asks to write only specific sections or headings within a chapter:
1. Load the same references
2. Write only the requested sections
3. Maintain the same heading hierarchy and style
4. Note where the section fits within the full chapter structure

## Chapter Review Mode

If the user asks to review or revise an existing chapter draft:
1. Read the draft chapter
2. Load writing-conventions.md
3. Check structure compliance (opening, topic list, headings, summary, references)
4. Check tone and style consistency
5. Verify AWS service accuracy against current documentation
6. Provide specific revision suggestions or apply edits directly
