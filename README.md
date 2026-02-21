# Claude Code Skills

Personal collection of Claude Code skills for syncing across machines.

## Setup

Clone and symlink to make all skills available to Claude Code:

```bash
git clone https://github.com/melanie531/claude-code-skills.git ~/repos/claude-code-skills

# Symlink into Claude Code's personal skills directory
ln -s ~/repos/claude-code-skills ~/.claude/skills
```

To pull updates on any machine:

```bash
cd ~/repos/claude-code-skills && git pull
```

> **Note:** If `~/.claude/skills` already exists, back it up or remove it before creating the symlink.

## Skills Catalog

| Skill | Description |
|---|---|
| **algorithmic-art** | Create algorithmic art using p5.js with seeded randomness and interactive parameter exploration |
| **aws-tech-blog** | Write AWS technical blog posts (customer stories, feature launches, best practices, how-to tutorials) |
| **bedrock-agentcore** | Build, deploy, and operate AI agents on Amazon Bedrock AgentCore |
| **brand-guidelines** | Apply Anthropic's official brand colors and typography to artifacts |
| **canvas-design** | Create visual art in .png and .pdf documents using design philosophy |
| **commit** | Create well-formatted git commits with conventional commit style |
| **doc-coauthoring** | Structured workflow for co-authoring documentation, proposals, and technical specs |
| **docx** | Document creation, editing, and analysis with tracked changes, comments, and formatting |
| **explain-code** | Explain code with visual diagrams and analogies |
| **fix-issue** | Fix a GitHub issue by number |
| **frontend-design** | Create production-grade frontend interfaces with high design quality |
| **internal-comms** | Write internal communications (status reports, newsletters, FAQs, incident reports) |
| **mcp-builder** | Guide for creating MCP servers in Python (FastMCP) or Node/TypeScript |
| **pdf** | PDF manipulation: extract text/tables, create, merge/split, and handle forms |
| **pptx** | Presentation creation, editing, and analysis (.pptx) |
| **review** | Review code for bugs, security issues, and best practices |
| **skill-creator** | Guide for creating and packaging new Claude Code skills |
| **slack-gif-creator** | Create animated GIFs optimized for Slack |
| **theme-factory** | Style artifacts with 10 pre-set themes or generate custom themes on-the-fly |
| **web-artifacts-builder** | Build multi-component HTML artifacts with React, Tailwind CSS, and shadcn/ui |
| **webapp-testing** | Test local web applications using Playwright (screenshots, browser logs, UI verification) |
| **write-chapter** | Write chapters for "Architecting Generative AI Applications on AWS" |
| **xlsx** | Spreadsheet creation, editing, analysis with formulas, formatting, and visualization |

## Structure

Each skill is a directory containing at minimum a `SKILL.md` file:

```
<skill-name>/
├── SKILL.md              # Main skill instructions (required)
├── LICENSE.txt            # License (if applicable)
├── references/            # Reference documentation
├── templates/             # Templates for output
├── scripts/               # Helper scripts
└── examples/              # Example outputs
```

## Adding a New Skill

1. Create a new directory with a `SKILL.md` file:
   ```bash
   mkdir -p ~/repos/claude-code-skills/my-new-skill
   # Create SKILL.md with frontmatter (name, description) and instructions
   ```
2. Commit and push:
   ```bash
   cd ~/repos/claude-code-skills
   git add my-new-skill/
   git commit -m "Add my-new-skill"
   git push
   ```
3. Pull on other machines:
   ```bash
   cd ~/repos/claude-code-skills && git pull
   ```
