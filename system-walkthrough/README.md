# System Walkthrough Agent

An AI agent that analyzes codebases and produces narrative-driven, slide-based presentations (Marp Markdown) covering design, architecture, code, testing, and infrastructure — explaining not just what the system does but why it was built that way.

## Purpose

The system-walkthrough agent addresses two converging problems:

1. **Developer onboarding**: developers spend 58% of their time on program comprehension (Code Compass, 2024). New developers take 3-6 months to reach full productivity without structured onboarding.
2. **AI code validation**: AI now produces 30-50% of enterprise code, with 45% failing security tests. Teams need structured ways to audit and understand AI-generated codebases.

The agent produces slide decks that walk teams through a system's purpose, architecture, key decisions, code organization, quality metrics, and risks — organized as a narrative that explains the "why" behind every "what."

## When to Use

Use this agent when:
- Onboarding new developers who need to understand a codebase
- Preparing a system walkthrough presentation for a team
- Auditing AI-generated code (Cursor, Copilot, Claude Code, Devin) for quality and coherence
- Documenting a system's architecture and design decisions after the fact
- Reviewing a codebase before a major refactoring effort
- Validating that an AI coding agent produced well-structured, maintainable code

## What It Produces

| Output File | Description |
|---|---|
| `{project}-walkthrough.md` | Full Marp slide deck (23-39 slides) covering all 7 sections |
| `{project}-overview.md` | Quick overview deck (10-15 slides) for rapid understanding |
| `{project}-analysis.json` | Raw analysis data: metrics, dependencies, hotspots |
| `{project}-decisions.md` | Recovered/inferred design decisions in ADR format |

## The 7-Section Slide Structure

| # | Section | Slides | Content |
|---|---------|--------|---------|
| 1 | **The Story** | 3-5 | Business problem, users, system context diagram, key numbers |
| 2 | **The Architecture** | 5-8 | Container diagram, design decisions (ADR format), data flow, cross-cutting concerns |
| 3 | **The Code** | 5-10 | Module map, hotspot deep-dives, patterns, dependency analysis |
| 4 | **The Quality** | 3-5 | Test strategy, coverage + assertion density, technical debt hotspots |
| 5 | **The Infrastructure** | 3-5 | CI/CD pipeline, deployment topology, configuration management |
| 6 | **The Risks** | 2-3 | Technical debt, knowledge silos, AI code assessment (if applicable) |
| 7 | **Getting Started** | 2-3 | Dev setup, first steps, where to get help |

## 6-Layer Analysis Pipeline

The agent performs analysis in 6 layers:

1. **Static Structure** — File inventory, import/dependency graph, complexity metrics, pattern detection
2. **Behavioral** — Git history mining for hotspots (complexity x change frequency), logical coupling, knowledge risk (bus factor), code age
3. **Architecture Recovery** — Module clustering, layer detection, cycle detection, C4 diagram generation
4. **Decision Recovery** — ADR detection, commit message analysis, structural inference of design decisions
5. **Test Quality** — Assertion density, mock ratio, test-to-code ratio, coverage analysis
6. **Infrastructure** — CI/CD pipeline parsing, containerization analysis, configuration patterns

## Narrative Approach

The walkthrough follows a 5-act story arc:

1. **Setting** — What problem does this system solve? For whom? What existed before?
2. **Characters** — What are the key components? What roles do they play? Why do they exist?
3. **Conflict** — What technical challenges drove the design? What trade-offs were faced?
4. **Resolution** — How does the architecture address each challenge? What decisions were made and why?
5. **Epilogue** — What are the known limitations? What technical debt exists? What's the evolution path?

Design decisions are presented using the ADR pattern (Context > Decision > Consequences) and are clearly labeled as either "Documented" (found in repo) or "Inferred" (deduced from code structure).

## AI Code Validation

When analyzing AI-generated codebases, the agent applies additional validation:

| Dimension | What It Checks |
|---|---|
| Architectural Coherence | Module boundaries, layer discipline, pattern consistency |
| Decision Rationale Gaps | Technology choices without documented reasoning |
| Test Effectiveness | Assertion density, mock ratio, circular verification patterns |
| Security Patterns | Input validation, auth checks, secret management |
| Consistency | Error handling, logging, configuration, naming conventions |
| Over-Engineering | Unnecessary abstractions, pattern overkill, deep hierarchies |

Produces a Health Score (0-10) summarizing codebase quality across all dimensions.

## Skills

This agent includes 5 skill documents (`skills/system-walkthrough/`):

- **analysis-pipeline.md** — Detailed techniques for the 6-layer analysis: static parsing, git mining, architecture recovery, decision inference, test quality metrics, infrastructure analysis
- **narrative-structure.md** — Story arc construction, ADR-style decision documentation, Diataxis content typing, progressive disclosure tiers
- **slide-architecture.md** — Marp formatting, 7-section slide templates, Mermaid diagram templates (C4, sequence, flowchart), cognitive load checklist
- **code-validation.md** — AI code risk profile, 6 validation dimensions with checklists, health score computation
- **comprehension-models.md** — Cognitive science foundations: 5 program comprehension models (Brooks, Pennington, Letovsky, Von Mayrhauser, Soloway), information foraging theory, Miller's Law, Sweller's cognitive load theory, developer question taxonomy

## Examples

The `examples/` folder contains two sample walkthrough outputs:

### express-api-walkthrough/
A walkthrough of a small Express.js REST API, showing the full deck structure with:
- System context and container diagrams (Mermaid)
- Design decisions framed as narratives
- Hotspot analysis identifying the payment service as highest-risk module
- Test quality assessment with assertion density metrics

### ai-generated-fastapi/
A walkthrough of an AI-generated FastAPI application, demonstrating the AI code validation dimension:
- Architecture coherence assessment
- Flagged issues: low assertion density, god classes, inconsistent error handling
- Health Score computation with per-dimension breakdown

## Research

The `docs/` folder contains the comprehensive research that informed this agent's design:

- **system-walkthrough-agent-comprehensive-research.md** — Master synthesis document (144+ sources) covering cognitive comprehension models, documentation frameworks (Arc42, C4, Diataxis), slide tools, AI code validation, and the proposed agent architecture

## Converting Slides

The agent outputs Marp Markdown. To convert to other formats:

```bash
# Install Marp CLI
npm install -g @marp-team/marp-cli

# Convert to PDF
marp project-walkthrough.md --pdf

# Convert to PowerPoint
marp project-walkthrough.md --pptx

# Convert to HTML
marp project-walkthrough.md

# Serve with live preview
marp project-walkthrough.md --server
```

## Related Agents

This agent works well in combination with:
- **cognitive-load-analyzer** — Get a quantitative CLI score before generating the walkthrough
- **code-smell-detector** — Deep-dive into code quality issues flagged by the walkthrough
- **test-design-reviewer** — Detailed Farley Index assessment for test suites identified as problematic

## Agent Pipeline: System Understanding

```
Codebase → system-walkthrough → Presentation Deck + Analysis Data
                                       ↓
                              cognitive-load-analyzer → CLI Score
                              code-smell-detector → Smell Report
                              test-design-reviewer → Farley Score
```

## Agent Definition

- `system-walkthrough.md` — The full agent definition

## Attribution

This agent has been created with the agentic framework [nWave](https://nwave.ai).
