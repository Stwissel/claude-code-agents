---
name: slide-architecture
description: Marp slide deck structure — 7-section organization, Arc42+C4 mapping, Mermaid diagram templates, cognitive load checklist, and Marp formatting conventions
---

# Slide Architecture

## Marp Frontmatter

Every slide deck starts with:

```markdown
---
marp: true
theme: default
paginate: true
header: "System Walkthrough: {Project Name}"
footer: "Generated {date} | Atlas System Walkthrough Agent"
style: |
  section { font-size: 24px; }
  h1 { font-size: 36px; color: #2d3748; }
  h2 { font-size: 28px; color: #4a5568; }
  .columns { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  .tag { font-size: 14px; color: #718096; font-style: italic; }
  .inferred { color: #b7791f; font-style: italic; }
  .documented { color: #276749; }
---
```

## Slide Separator

Use `---` on its own line between slides. Add `<!-- presenter notes -->` for additional context.

## The 7 Sections

### Section 1: THE STORY (3-5 slides) — Tier 1

| Slide | Content | Diagram |
|-------|---------|---------|
| Title | Project name, one-line description, date, team | — |
| The Problem | Business context, users, pain point being solved | — |
| System Context | System in its environment with actors and external systems | C4Context |
| Key Numbers | File count, language distribution, team size, age, test count | — |

### Section 2: THE ARCHITECTURE (5-8 slides) — Tier 1-2

| Slide | Content | Diagram |
|-------|---------|---------|
| Container Overview | Main building blocks with technology choices | C4Container |
| Architecture Style | Pattern used (layered, hexagonal, microservice) and why | flowchart |
| Key Decision 1 | ADR-style: Context > Decision > Consequences | — |
| Key Decision 2 | ADR-style: Context > Decision > Consequences | — |
| Key Decision 3 | ADR-style: Context > Decision > Consequences | — |
| Data Flow | Primary request path through the system step by step | sequenceDiagram |
| Cross-Cutting | Auth, logging, error handling, validation patterns | — |

### Section 3: THE CODE (5-10 slides) — Tier 2

| Slide | Content | Diagram |
|-------|---------|---------|
| Module Map | All modules with responsibilities and dependency arrows | graph TD |
| Module Deep-Dive 1 | Hotspot #1: structure, purpose, key classes, why it matters | C4Component |
| Module Deep-Dive 2 | Hotspot #2: same structure | C4Component |
| Module Deep-Dive 3 | Hotspot #3: same structure | C4Component |
| Patterns & Conventions | Design patterns used, naming conventions, code organization rules | — |
| Dependencies | Key dependency relationships, cycles if any, coupling concerns | graph LR |

### Section 4: THE QUALITY (3-5 slides) — Tier 2

| Slide | Content | Diagram |
|-------|---------|---------|
| Test Strategy | Framework, approach (unit/integration/e2e split), philosophy | — |
| Test Metrics | Coverage %, assertion density, test-to-code ratio, mock ratio | — |
| Code Health | Top 5 hotspots (complexity x change frequency), technical debt estimate | — |
| Quality Risks | Low-coverage modules, assertion-free tests, high-coupling areas | — |

### Section 5: THE INFRASTRUCTURE (3-5 slides) — Tier 2

| Slide | Content | Diagram |
|-------|---------|---------|
| Build & Deploy | CI/CD pipeline overview, stages, triggers | flowchart LR |
| Deployment Topology | Where services run, how they communicate | C4Deployment or graph |
| Configuration | Environment management, secrets, feature flags | — |
| Observability | Logging, monitoring, alerting (if present) | — |

### Section 6: THE RISKS (2-3 slides) — Tier 1-2

| Slide | Content | Diagram |
|-------|---------|---------|
| Technical Debt | Known debt items ranked by hotspot score, estimated impact | — |
| Knowledge Risks | Single-author modules, abandoned areas, missing documentation | — |
| AI Code Assessment | (If applicable) Validation findings for AI-generated code | — |

### Section 7: GETTING STARTED (2-3 slides) — Tier 1

| Slide | Content | Diagram |
|-------|---------|---------|
| Dev Setup | Prerequisites, install steps, run commands | — |
| First Steps | Suggested exploration path, key entry points for common tasks | — |
| Where to Get Help | Documentation locations, key people/channels, this walkthrough | — |

## Mermaid Diagram Templates

### C4 System Context
```
C4Context
    title System Context - {Project Name}
    Person(user, "{User Type}", "{Description}")
    System(sys, "{System Name}", "{Core responsibility}")
    System_Ext(ext1, "{External System}", "{What it provides}")
    Rel(user, sys, "{Uses}")
    Rel(sys, ext1, "{Interaction}")
```

### C4 Container
```
C4Container
    title Container View - {Project Name}
    Person(user, "{User}")
    Container(api, "{API Name}", "{Technology}", "{Responsibility}")
    Container(web, "{Frontend}", "{Technology}", "{Responsibility}")
    ContainerDb(db, "{Database}", "{Technology}", "{What it stores}")
    Container(queue, "{Message Queue}", "{Technology}", "{Purpose}")
    Rel(user, web, "{Uses}")
    Rel(web, api, "{Calls}", "HTTPS/JSON")
    Rel(api, db, "{Reads/Writes}")
    Rel(api, queue, "{Publishes}")
```

### Sequence Diagram (Data Flow)
```
sequenceDiagram
    participant U as User
    participant A as API Gateway
    participant S as Service
    participant D as Database
    U->>A: POST /resource
    A->>S: validate + process
    S->>D: persist
    D-->>S: confirmation
    S-->>A: result
    A-->>U: 201 Created
```

### Module Dependency Graph
```
graph TD
    A[Module A] --> B[Module B]
    A --> C[Module C]
    B --> D[Module D]
    C --> D
    B -.->|circular| C
    style B fill:#ff9999
```
Use `fill:#ff9999` (red) for hotspots. Use `-.->` (dashed) for problematic dependencies.

## Cognitive Load Checklist

Before finalizing the deck, verify every slide passes:

- [ ] Max 7 bullet points per slide (group into sub-lists if more needed)
- [ ] One concept per slide (don't mix architecture decisions with API reference)
- [ ] Each slide opens with a 1-sentence summary of its key point
- [ ] Diagrams appear before their textual explanation
- [ ] Lists use semantic grouping (not arbitrary ordering)
- [ ] Diataxis types are not mixed within a single slide
- [ ] Every abstract concept has a concrete example (worked example effect)
- [ ] Decision rationale ("why") accompanies every "what"
- [ ] Presenter notes provide additional depth without cluttering the slide
- [ ] Total top-level sections: exactly 7

## Slide Template

```markdown
---

## {Section} > {Topic}

{One-sentence summary of this slide's key point}

{Diagram or visual element if applicable}

{2-4 bullet points or short paragraphs}

{Why this matters / the decision behind it}

<!--
Presenter notes: additional context, detailed metrics,
links to relevant code files, caveats
-->

---
```

## Quick Overview Variant

The overview deck includes only Tier 1 slides (~10-15 total):

1. Title slide
2. The Problem (business context)
3. System Context diagram
4. Key Numbers
5. Container Overview diagram
6. Top 3 Design Decisions (1 slide each)
7. Data Flow (primary path)
8. Top 3 Risks
9. Getting Started
10. Where to Get Help

Skip: module deep-dives, test metrics, infrastructure details, code-level analysis.
