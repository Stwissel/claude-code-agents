---
name: analysis-pipeline
description: 6-layer analysis pipeline for codebase comprehension — static structure, behavioral mining, architecture recovery, decision recovery, test quality, and infrastructure analysis
---

# Analysis Pipeline

## Layer 1: Static Structure

Extract without external tools using filesystem + AST/import parsing.

### File Inventory
- Count files by extension to determine language distribution
- Identify entry points: `main.*`, `index.*`, `app.*`, route definitions, CLI handlers
- Detect frameworks from package manifests (package.json, requirements.txt, Gemfile, pom.xml, go.mod)
- Map directory structure to identify organizational patterns (by feature, by layer, by type)

### Dependency Graph
- Parse import/require/include statements to build a module dependency graph
- For JS/TS: trace `import`/`require` statements
- For Python: trace `import`/`from...import` statements
- For Java/Kotlin: trace `import` and package declarations
- Identify circular dependencies (modules that import each other, directly or transitively)
- Calculate fan-in (dependents) and fan-out (dependencies) per module

### Complexity Metrics
- Estimate cyclomatic complexity from branching statements (if/else/switch/for/while/try-catch)
- Measure file size (LOC) as a rough complexity proxy
- Count classes, functions/methods per file
- Identify god classes: files with >500 LOC or >15 public methods
- Identify god functions: functions with >50 LOC or >5 levels of nesting

### Pattern Detection
- Identify design patterns from naming conventions and structural cues:
  - Repository pattern: classes ending in `Repository`, `Repo`, `Store`, `DAO`
  - Service pattern: classes ending in `Service`, `Manager`, `Handler`
  - Controller pattern: classes ending in `Controller`, `Router`, `Handler`
  - Factory pattern: classes ending in `Factory`, `Builder`, `Creator`
  - Observer pattern: `EventEmitter`, `on()`/`emit()` patterns, `subscribe`/`publish`
- Identify architectural patterns from directory structure:
  - Layered: `controllers/`, `services/`, `models/`, `repositories/`
  - Hexagonal: `ports/`, `adapters/`, `domain/`, `application/`
  - Feature-based: directories named after business concepts
  - Microservice: multiple `package.json`/`pom.xml` in subdirectories

## Layer 2: Behavioral Analysis (Git History)

Requires git repository. Extract using `git log` parsing.

### Git Log Extraction
```bash
git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames --after="YYYY-MM-DD"
```
Use a 12-month window by default. Adjust for younger repositories.

### Hotspot Analysis
For each file, calculate:
- `change_frequency` = number of commits touching the file
- `complexity` = LOC or cyclomatic complexity estimate
- `hotspot_score` = change_frequency * complexity (normalized)

Rank files by hotspot score. Top 10% are the highest-priority files for deep-dive.

### Logical Coupling
From the git log, identify files that change together:
- `coupling_strength` = (shared_commits / total_commits_of_either_file) * 100
- Flag pairs with coupling > 30% and shared commits > 5
- High coupling between files in different modules suggests hidden dependencies

### Knowledge Risk
- Count unique authors per file/module
- `bus_factor` = number of authors who contributed >10% of commits
- Flag single-author modules (bus factor = 1) as knowledge silos
- Identify abandoned modules: no commits in >6 months

### Code Age
- For each file: months since last modification
- For each module: average age of files within it
- Stale modules (>12 months untouched) may indicate stable OR abandoned code — correlate with test coverage

## Layer 3: Architecture Recovery

### Module Clustering
- Group files by directory as the initial module hypothesis
- Validate by checking that intra-module dependencies > inter-module dependencies
- If a directory has more external than internal dependencies, it may be misplaced

### Layer Detection
- From the dependency graph, identify a dependency direction (top to bottom)
- Typical layers: Presentation > Application/Service > Domain > Infrastructure/Data
- Flag violations: lower layers depending on upper layers
- Flag skip-layer dependencies: Presentation directly accessing Data layer

### C4 Diagram Generation
- **System Context (L1)**: the system plus external actors (users, external APIs, databases)
  - Source: README, configuration files referencing external URLs/services, environment variables
- **Container (L2)**: deployable units (services, databases, message queues)
  - Source: Docker Compose, Kubernetes manifests, multiple package manifests, database configurations
- **Component (L3)**: internal modules of a single container
  - Source: directory structure, dependency graph, pattern detection from Layer 1

### Cycle Detection
- Find all strongly connected components in the dependency graph
- Report each cycle with the files involved and the dependency chain
- Prioritize cycles by: number of files involved * average hotspot score of files

## Layer 4: Decision Recovery

### ADR Detection
Search for existing decision records:
- `docs/adr/`, `docs/decisions/`, `architecture/decisions/`, `doc/arch/`
- Files matching pattern: `*adr*`, `*decision*`, `*ADR*`
- README sections titled "Decisions", "Architecture", "Design"

### Commit-Based Inference
Scan commit messages for decision-related language:
- "chose", "decided", "switched to", "migrated from", "replaced", "introduced", "refactored to"
- Large commits (>10 files) that change module structure
- Commits that add/remove dependencies (package manifest changes)

### Structural Inference
Infer decisions from what exists in the code:
- **Technology choices**: "Uses PostgreSQL" (from connection strings/ORM config), "Uses Redis for caching" (from Redis client imports)
- **Architectural style**: "Follows layered architecture" (from directory structure), "Implements hexagonal pattern" (from ports/adapters directories)
- **Testing strategy**: "Uses integration tests with testcontainers" (from test configuration)
- **Deployment model**: "Containerized with Docker" (from Dockerfile), "Deployed to Kubernetes" (from manifests)

Format each as: `Inferred: [Decision]. Evidence: [what in the code supports this]. Confidence: [high/medium/low].`

## Layer 5: Test Quality

### Basic Metrics
- Test file count vs. production file count (test-to-code ratio)
- Test framework detection from configuration (Jest, pytest, JUnit, RSpec, etc.)
- Test runner configuration analysis (coverage thresholds, parallelism settings)

### Assertion Density
Scan test files for assertion patterns:
- JS/TS: `expect(`, `assert(`, `assert.`, `.should`, `.to.`
- Python: `assert `, `self.assert`, `pytest.raises`
- Java: `assert`, `assertEquals`, `assertThat`, `verify(`
- Calculate: assertions per test function (avg, min, max)
- Flag tests with 0 assertions (assertion-free tests / smoke tests)

### Mock Analysis
- Count mock/stub/spy creation per test file
- Calculate mock-to-assertion ratio
- High mock ratio (>3 mocks per test) may indicate design coupling issues
- Flag test files where mocks outnumber assertions

### Coverage Analysis (if data available)
- Read coverage reports if present (lcov, cobertura, istanbul)
- Identify uncovered modules (0% coverage)
- Identify "coverage theater": high coverage with low assertion density

## Layer 6: Infrastructure

### CI/CD Pipeline
- Parse GitHub Actions workflows (.github/workflows/*.yml)
- Parse GitLab CI (.gitlab-ci.yml)
- Parse Jenkinsfile, CircleCI config, etc.
- Extract: stages, test commands, build commands, deployment targets, secrets usage

### Containerization
- Parse Dockerfile(s): base image, build stages, exposed ports, health checks
- Parse docker-compose.yml: services, networks, volumes, dependencies
- Parse Kubernetes manifests: deployments, services, ingress, configmaps, secrets

### Configuration Management
- Identify environment variable patterns (.env files, config/ directories)
- Detect secret management (vault references, sealed secrets, AWS SSM)
- Identify configuration per environment (dev, staging, production)

### Dependency Health
- Parse package manifests for dependency versions
- Identify pinned vs. floating versions
- Check for known lock file (package-lock.json, yarn.lock, Pipfile.lock, Gemfile.lock)
