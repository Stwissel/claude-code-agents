---
name: comprehension-models
description: Cognitive science foundations for presenting code information — program comprehension models, information foraging, cognitive load management, and developer question taxonomy
---

# Comprehension Models

## Why This Matters

How you present information determines whether developers build accurate mental models or just read words. The research is clear: comprehension is not a passive process — developers actively construct understanding using multiple simultaneous strategies. The walkthrough must support all of them.

## The Five Comprehension Strategies

### 1. Top-Down (Brooks, 1983)
Developer forms a hypothesis about what the code does, then seeks "beacons" to confirm or refute it.

**Agent implication**: Open every section with a clear hypothesis statement. "This module handles payment processing by coordinating between the order system and external payment providers." Then show the evidence (the beacons) that confirm this.

Beacons to surface:
- Well-named functions that reveal purpose (`processPayment`, `validateOrder`)
- Design pattern implementations (Repository classes, Factory methods)
- Stereotypical algorithmic structures (retry loops, batch processors, pub-sub handlers)

### 2. Bottom-Up (Pennington, 1987)
When code is unfamiliar, developers first trace control flow ("what does this do step by step?"), then build a functional model ("what problem does this solve?").

**Agent implication**: For unfamiliar code, present the control-flow walkthrough first (the program model), then the domain explanation (the situation model).

Slide structure for unfamiliar code:
1. "Here's what happens step by step" (sequence diagram or numbered list)
2. "Here's what this means in business terms" (domain mapping)

### 3. Opportunistic (Letovsky, 1987; Von Mayrhauser & Vans, 1995)
Developers switch between top-down and bottom-up strategies based on what they encounter. A recognized pattern triggers top-down reasoning; a confusing section triggers bottom-up analysis.

**Agent implication**: Support non-linear navigation. Each slide should be understandable on its own (with minimal context from previous slides). Cross-reference related slides by name.

### 4. Information Foraging (Lawrance et al., 2013)
Developers spend ~50% of comprehension time searching for relevant information, following "scent" cues. They abandon paths with weak scent.

**Agent implication**: Provide strong scent cues on every slide:
- Clear slide titles that tell you what you'll learn
- One-sentence summaries at the top of each slide
- Cross-references to related slides ("See: Data Flow slide for runtime behavior")
- Avoid generic titles like "Overview" — use "How Orders Flow Through the System"

### 5. Programming Plans (Soloway & Ehrlich, 1984)
Experts recognize stereotypical code patterns (programming plans) instantly. Convention violations disrupt expert comprehension.

**Agent implication**: Label recognized patterns explicitly ("This follows the Repository pattern", "This is a standard retry-with-exponential-backoff implementation"). Flag convention violations as comprehension hazards.

## The 44 Developer Questions (Sillito et al., 2006)

The walkthrough should proactively answer the most common question types:

### Finding Initial Focus Points
- "Where is [business concept] implemented?"
- "What is the entry point for [feature]?"
- "Which files are most important to understand first?"

→ Address in: Section 1 (System Context), Section 3 (Module Map)

### Building on That Focus
- "What does this class/function do?"
- "What are the inputs and outputs?"
- "What are the key data structures?"

→ Address in: Section 3 (Module Deep-Dives)

### Understanding Relationships
- "What calls this? What does this call?"
- "How do these components interact at runtime?"
- "What would break if I change this?"

→ Address in: Section 2 (Data Flow), Section 3 (Dependencies)

### Understanding Design Intent
- "Why was this designed this way?"
- "What alternatives were considered?"
- "What constraints led to this choice?"

→ Address in: Section 2 (Key Decisions), narrative throughout

### Understanding Quality and Risk
- "How well tested is this?"
- "Where are the known problems?"
- "What's safe to change?"

→ Address in: Section 4 (Quality), Section 6 (Risks)

## Cognitive Load Management

### Miller's Law: The Rule of Seven
Working memory holds ~7 items. Apply structurally:

- Max 7 top-level sections in the deck (we use exactly 7)
- Max 7 bullet points per slide
- Max 7 items in any list before grouping into sub-lists
- If a section has >7 slides, add a section-overview slide

### Sweller's Three Load Types

| Load Type | What It Is | Agent Strategy |
|-----------|------------|----------------|
| **Intrinsic** | Inherent complexity of the material | Cannot reduce, but manage through sequencing (simple first, complex later) |
| **Extraneous** | Load from poor presentation | Minimize: clear structure, consistent formatting, no decoration |
| **Germane** | Load spent building mental models | Maximize: focus attention on patterns, relationships, and rationale |

### Progressive Disclosure (Nielsen, 1995)

Present information in 3 tiers. Never more.

| Tier | Audience | What to Show |
|------|----------|-------------|
| 1 | Everyone | Purpose, context, key decisions, risks, getting started |
| 2 | Developers, tech leads | Module details, test metrics, infrastructure, dependency analysis |
| 3 | Architects, auditors | Code walkthroughs, coupling metrics, fitness functions, AI validation |

### The Worked Examples Effect

For every abstract concept, provide a concrete, annotated example.

Instead of: "The system uses the Repository pattern for data access."

Use: "The system uses the Repository pattern for data access. Here's how it works in the Order module:"
```
OrderService (driving port)
  → calls OrderRepository.save(order)     [through port interface]
    → PostgresOrderRepository implements   [adapter]
      → INSERT INTO orders ...             [actual SQL]
```

### Sequencing Rules

1. **Overview before detail**: always present the big picture before zooming in
2. **Familiar before unfamiliar**: start with recognizable patterns, then introduce novel ones
3. **Context before content**: explain why a section matters before presenting the information
4. **Concrete before abstract**: show an example before explaining the general principle
5. **Simple before complex**: present straightforward modules before convoluted ones

## Audience Adaptation

Tag each slide with its primary audience. When generating a filtered deck:

| Tag | Include For |
|-----|------------|
| `[all]` | Every variant of the deck |
| `[dev]` | Developer onboarding deck |
| `[lead]` | Tech lead / architect deck |
| `[ops]` | DevOps / SRE deck |
| `[audit]` | AI code validation / quality audit deck |
| `[exec]` | Executive / product stakeholder deck |
