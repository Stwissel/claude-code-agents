---
name: narrative-structure
description: Storytelling techniques for system walkthroughs — story arc, ADR-style decision narratives, Diataxis content typing, and organic "why" integration
---

# Narrative Structure

## The System Story Arc

Every walkthrough follows a 5-act narrative structure. This is not a rigid template — it's a thinking tool for organizing information into a memorable flow.

### Act 1: SETTING (2-3 slides)
Establish context before any technical detail.

Questions to answer:
- What problem does this system solve? For whom?
- What existed before this system? What was the pain point?
- What constraints shaped the design? (team size, timeline, compliance, scale requirements)

Tone: accessible to non-technical stakeholders. No jargon. Focus on the human problem.

Example opening:
> "Our e-commerce platform processes 50,000 orders daily for small business owners who previously managed orders through spreadsheets. Built by a team of 4 engineers in 2024 under SOC2 compliance requirements, it replaced a manual workflow that caused 3-5% order errors monthly."

### Act 2: CHARACTERS (3-5 slides)
Introduce the key components as characters with motivations.

For each major component:
- **Name**: the component/service name
- **Role**: what it does in one sentence
- **Motivation**: why it exists (what problem it solves that nothing else does)
- **Relationships**: who it talks to and why

Do not dump all components at once. Introduce them in order of relevance to the story.

Example:
> "The **Payment Engine** is the system's financial gatekeeper. It exists because integrating with 4 different payment providers (Stripe, PayPal, bank transfer, invoice) required a unified interface that shields the rest of the system from provider-specific complexity. It communicates with the Order Service (to confirm payments) and the Notification Service (to trigger receipts)."

### Act 3: CONFLICT (2-3 slides)
Present the technical challenges and trade-offs that drove design decisions.

Frame as genuine tensions, not solved problems:
- "We needed real-time updates BUT our budget constrained us to a shared PostgreSQL instance"
- "SOC2 required audit logging BUT logging everything would have 10x'd our storage costs"
- "The team wanted microservices BUT we only had 4 engineers"

This is where architecture becomes interesting — the constraints that made the design non-obvious.

### Act 4: RESOLUTION (5-8 slides)
Show how the architecture addresses each conflict. This is the technical core of the walkthrough.

For each significant decision, use the ADR pattern:

```markdown
**Context**: [The forces at play — constraints, requirements, team situation]
**Decision**: [What was chosen]
**Consequences**: [What became easier AND what became harder]
```

Connect decisions to each other: "Because we chose X for [reason], we then needed Y for [follow-on reason]."

### Act 5: EPILOGUE (2-3 slides)
Honest assessment of current state.

- Known technical debt and why it exists
- Known risks (knowledge silos, architectural violations, dependency concerns)
- Evolution path: what the team plans to change and why
- What a new developer should watch out for

## Weaving "Why" Organically

The most common failure in system walkthroughs is presenting "what" without "why." The fix is structural: never describe a component, pattern, or decision without immediately following with its rationale.

### Pattern: What-Because-Consequence

For every technical fact, apply this 3-part structure:

1. **What**: The factual description ("We use Redis for session storage")
2. **Because**: The rationale ("Because sessions need sub-millisecond reads and we needed to share state across 3 API instances")
3. **Consequence**: The trade-off ("This means sessions are lost on Redis restart, so we implemented session recovery via JWT refresh tokens")

### Pattern: Decision Chains

Connect decisions into causal chains rather than presenting them as isolated choices:

> "We chose **PostgreSQL** for its relational modeling strength and ACID guarantees, which the financial domain required. This led us to choose **SQLAlchemy** as our ORM for its mature migration support (Alembic). The ORM's session management complexity then drove our decision to implement the **Repository pattern**, isolating data access behind a clean interface."

### Pattern: Constraint-Driven Narrative

When the rationale isn't documented, frame it as constraint-driven:

> "Inferred: The team chose a monolithic deployment despite having 4 distinct services. This likely reflects the team size constraint (4 engineers) — operating 4 separate deployments would have consumed significant ops overhead. Evidence: all services share a single Dockerfile and deploy as one container."

## Diataxis Content Typing

Tag each section of the walkthrough with its Diataxis type. This prevents the most common documentation failure: mixing explanation with reference.

### Type Rules

| Type | Purpose | Tone | What to Include | What to Exclude |
|------|---------|------|-----------------|-----------------|
| **Explanation** | Understanding, the "why" | Conversational, connecting | Context, rationale, trade-offs, analogies | Exact command syntax, exhaustive API lists |
| **Reference** | Facts, the "what" | Neutral, precise | Exact names, types, configurations, metrics | Opinions, rationale, narrative |
| **Tutorial** | Learning, guided experience | Supportive, step-by-step | Concrete worked examples, expected output | Abstract theory, comprehensive coverage |
| **How-To** | Task completion | Direct, goal-oriented | Steps to achieve outcome, prerequisites | Background theory, alternative approaches |

### Slide Type Assignments

| Slide Section | Primary Type | Secondary Type |
|---------------|-------------|----------------|
| System purpose and context | Explanation | — |
| Architecture overview | Explanation | Reference (diagram) |
| Design decisions | Explanation | — |
| Component deep-dives | Explanation + Reference | — |
| Data flow sequences | Tutorial (worked example) | — |
| Test strategy | Explanation | Reference (metrics) |
| Infrastructure/deployment | Reference | Explanation (why this topology) |
| Getting started | Tutorial | How-To |
| API/config details | Reference | — |
| Risk assessment | Explanation | Reference (metrics) |

## Decision Documentation Format

### For Documented Decisions (ADRs found in repo)

Preserve the original ADR content. Present as:

```markdown
## Decision: [Title] (Documented)

**Status**: [from ADR]
**Context**: [from ADR]
**Decision**: [from ADR]
**Consequences**: [from ADR]
```

### For Inferred Decisions

Clearly label as inferred with evidence and confidence:

```markdown
## Decision: [Title] (Inferred)

**Evidence**: [What in the code supports this inference]
**Confidence**: [High/Medium/Low]
**Context**: [Reconstructed from code and constraints]
**Decision**: [What was likely chosen]
**Consequences**: [Observable effects in the codebase]
```

### Confidence Levels for Inferred Decisions

- **High**: Multiple structural signals align (e.g., framework choice + directory structure + configuration all point to the same decision)
- **Medium**: One clear signal with supporting context (e.g., package.json shows the choice, but no documentation explains why)
- **Low**: Single indirect signal (e.g., directory naming suggests a pattern but could be coincidental)

## Progressive Disclosure in Narrative

Structure the narrative in 3 tiers:

### Tier 1: The Overview (every audience)
- System purpose and business context
- High-level architecture (C4 System Context)
- 3-5 most important design decisions
- Key risks and getting started

### Tier 2: The Detail (developers, tech leads)
- Component deep-dives for major modules
- Data flow sequences with worked examples
- Test strategy and quality metrics
- Infrastructure and deployment topology
- Technical debt assessment

### Tier 3: The Deep-Dive (architects, auditors)
- Code-level walkthroughs of critical paths
- Dependency analysis with coupling metrics
- AI code validation findings
- Fitness function compliance
- Full hotspot analysis with behavioral data

The full deck includes all 3 tiers. The overview deck includes only Tier 1.
