# AWS Blog Types and Structures

## 1. Customer Story

Showcases how a customer solved a real business problem using AWS services. Co-written with the customer.

### Structure

1. **Title**: "{Action verb}ing {outcome}: {Company}'s journey with {Technology} and {AWS Service}"
2. **Byline**: Authors (AWS + customer), date, categories (include "Customer Solutions")
3. **Co-authorship note**: *"This post is cowritten with {Name} from {Company}."*
4. **Opening paragraph**: Industry trend or market data (cite reports/stats). State the common challenges.
5. **Customer introduction**: Who is the customer, what they do, scale (numbers), the specific problem.
6. **Thesis paragraph**: "In this blog post, we explore how {Company} built... We cover three key aspects:" followed by a bulleted list of 3 aspects.
7. **Section: Foundation/Prerequisites** (H2): What the customer had in place before the solution. Anti-patterns to avoid. Best practices for the foundation layer.
8. **Section: Technical Implementation** (H2): How they built it. Sub-sections (H3) for each component. Architecture decisions with rationale. Code concepts or configurations (not necessarily full code).
9. **Section: Architecture Diagram** (H2): High-level solution architecture with numbered workflow steps.
10. **Section: Why {AWS Service}** (H2): Why they chose the specific AWS service. Bullet list of benefits with bold labels. Customer quote as blockquote.
11. **Section: Results and Impact** (H2): Business outcomes, metrics, who benefits and how.
12. **Section: Conclusion and Key Takeaways** (H2): Summary paragraph. Bulleted key takeaways (4-5) with bold labels. Call to action with links. References as bullet list.
13. **About the Authors**: Photo + bio for each author.

### Customer Quote Format

```markdown
> *"Quote text here"*
>
> *– Name, Title at Company*
```

### Key Takeaway Format

```markdown
* **Invest in X**: Explanation of why and how...
* **Use Y for Z**: Explanation...
```

---

## 2. Feature Launch / Announcement

Announces a new AWS feature or capability with technical depth on how to use it.

### Structure

1. **Title**: "{Verb} {benefit} using {new feature} on {AWS Service} with {partner/model}"
2. **Byline**: Authors, date, categories (include "Announcements", level like "Advanced (300)")
3. **Opening paragraph**: Business context — why organizations need this capability. Current challenges.
4. **Feature announcement paragraph**: "We are excited to announce..." or "To address this need, we introduced..." Describe what the feature does at a high level.
5. **Thesis paragraph**: "In this post, we explore how {feature} works, the benefits it offers... and how you can implement it..."
6. **Section: Core Functionality** (H2): How the feature works technically. Sub-sections (H3) for each concept (e.g., Understanding X, Routing, Monitoring, Security).
7. **Section: Implementation** (H2): Code samples (Python, JSON). Step-by-step with numbered instructions. IAM policies if applicable.
8. **Section: Configuration/Management** (H2): Console steps with screenshots. Quota management, limits.
9. **Section: Use Cases + Comparison** (H2): Benefits as bullet list with bold labels. Comparison table of options (when to use which).
10. **Section: Conclusion** (H2): Summary of what the feature enables. Call to action: "We encourage you to try..." Links to documentation. "For more information, refer to..."
11. **About the Authors**: Photo + bio.

### Code Sample Format

- Use fenced code blocks with language identifier
- Add inline comments for key changes: `# KEY CHANGE: explanation`
- Show the minimal change needed (diff-style thinking)
- Include output/response handling

---

## 3. Best Practices / Thought Leadership

Prescriptive guidance organized as numbered recommendations.

### Structure

1. **Title**: "{Topic}: Best practices with {AWS Service}"
2. **Byline**: Authors, date, categories (include "Best Practices")
3. **Opening paragraph**: Frame the challenge. "Building production-ready X requires careful planning..."
4. **Thesis paragraph**: "This post explores {N} essential best practices for... We cover everything from {first topic} to {last topic}, with practical guidance..."
5. **Sections: One H2 per best practice**: Each section is a standalone best practice. Title is imperative: "Start small and define success clearly", "Instrument everything from day one". Each section includes: practical guidance, tables/diagrams, specific examples, do/don't comparisons.
6. **Section: Conclusion** (H2): Bullet list summarizing all practices. Map practices to specific AWS service features. Links to documentation, code samples, workshops.
7. **About the Authors**: Photo + bio.

### Best Practice Section Pattern

```
## {Imperative title}

Opening paragraph explaining the principle.

Practical guidance with specific examples.

[Table or diagram showing comparison/structure]

Concrete recommendation or anti-pattern.
```

---

## 4. How-To / Tutorial

Step-by-step guide to implement a specific solution.

### Structure

1. **Title**: "How to {achieve outcome} with {AWS Service}" or "Build {thing} using {AWS Service}"
2. **Opening**: Problem statement + what the reader will build
3. **Prerequisites**: Bullet list of what's needed
4. **Architecture Overview**: Diagram + description
5. **Step-by-step sections**: Numbered H2 sections ("Step 1: Set up...", "Step 2: Configure...")
6. **Testing/Validation**: How to verify it works
7. **Cleanup**: How to avoid ongoing charges
8. **Conclusion**: Summary + next steps + links
9. **About the Authors**
