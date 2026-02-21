# Software System Auditor Agent

An AI agent that audits software systems against regulatory compliance frameworks, producing one separate evidence-anchored audit report per selected regulation with findings mapped to specific controls, compliance scores, and remediation guidance.

## Purpose

The software-system-auditor addresses a growing challenge: as AI agents write more code autonomously, responsibility, ownership, and accountability over that code do not diminish -- especially in highly-regulated industries. Teams need a systematic way to assess compliance posture against multiple regulatory frameworks simultaneously, with cross-framework mapping so overlapping requirements are audited once and traced everywhere.

The agent presents all supported frameworks for multi-selection, runs a 7-phase gated audit workflow, and produces one dedicated report per selected regulation -- each with framework-specific control IDs, compliance scores, and actionable remediation guidance.

## When to Use

Use this agent when:
- Assessing a codebase's compliance posture against one or more regulatory frameworks
- Preparing for a formal audit by identifying gaps and collecting evidence
- Evaluating security posture across multiple overlapping standards
- Generating framework-specific remediation plans with prioritized actions
- Verifying that previously identified findings have been remediated
- Onboarding a new project into a regulated environment

## Supported Frameworks

| Framework | Full Name | Focus Area |
|---|---|---|
| **SOX** | Sarbanes-Oxley Act | IT controls over financial reporting |
| **SOC 2** | Service Organization Controls | Trust Service Criteria (security, availability, processing integrity, confidentiality, privacy) |
| **GDPR** | General Data Protection Regulation | EU data protection and privacy |
| **HIPAA** | Health Insurance Portability and Accountability Act | Healthcare data protection (ePHI) |
| **PCI DSS 4.0** | Payment Card Industry Data Security Standard | Payment card data security |
| **NIST CSF 2.0** | Cybersecurity Framework | General cybersecurity risk management |
| **ISO 27001:2022** | Information Security Management | International information security standard |
| **FedRAMP** | Federal Risk and Authorization Management | US federal cloud security |
| **CCPA/CPRA** | California Consumer Privacy Act | California privacy regulations |
| **DORA** | Digital Operational Resilience Act | EU financial sector operational resilience |
| **NIS2** | Network and Information Security Directive | EU critical infrastructure cybersecurity |
| **CMMC 2.0** | Cybersecurity Maturity Model Certification | US DoD contractor cybersecurity |

## 7-Phase Audit Workflow

| Phase | Name | Purpose |
|---|---|---|
| 1 | **SCOPE** | Present frameworks for user selection, detect tech stack, determine applicable controls |
| 2 | **DISCOVER** | Inventory codebase, map architecture, identify security-sensitive paths and audit artifacts |
| 3 | **COLLECT** | Gather evidence across 13 audit dimensions with file:line references |
| 4 | **ANALYZE** | Apply rules, cross-reference findings, classify severity (Critical/High/Medium/Low/Informational) |
| 5 | **SYNTHESIZE** | Map findings to selected frameworks, compute per-framework compliance scores |
| 6 | **REPORT** | Generate one separate report per selected regulation |
| 7 | **VERIFY** | (Optional) Re-check previous findings and assess remediation status |

Each phase has a gate that must be satisfied before proceeding to the next.

## 13 Audit Dimensions

| # | Dimension | What It Covers |
|---|---|---|
| 1 | Access Control | Authentication, authorization (RBAC/ABAC), MFA, session management |
| 2 | Encryption | At rest, in transit, key management, certificate handling |
| 3 | Audit Logging | Log completeness, tamper protection, retention, SIEM integration |
| 4 | Change Management | Code review, CI/CD gates, deployment controls, approval workflows |
| 5 | Vulnerability Management | Dependency CVEs, secret scanning, security testing |
| 6 | Data Protection | PII/PHI handling, data classification, retention, consent |
| 7 | Incident Response | Response plans, breach notification, escalation procedures |
| 8 | Backup & Recovery | Backup configuration, DR plans, RTO/RPO definitions |
| 9 | Supply Chain | SBOM, dependency provenance, license compliance |
| 10 | Configuration Security | IaC scanning, secrets in repos, container security |
| 11 | API Security | Authentication, input validation, rate limiting, contract testing |
| 12 | Secure SDLC | Code review practices, testing coverage, security testing integration |
| 13 | Third-Party Risk | Dependency maintenance status, vendor oversight |

## Cross-Framework Compliance Mapping

A key architectural feature: when a single finding (e.g., missing MFA) applies to multiple selected frameworks, it appears in each relevant report mapped to that framework's specific control IDs. Evidence is collected once and traced everywhere.

The highest-overlap controls across all 12 frameworks:

| Control | Frameworks Covered |
|---|---|
| Access Control & MFA | 11/12 |
| Encryption in Transit | 10/12 |
| Encryption at Rest | 10/12 |
| Third-Party Risk Management | 10/12 |
| Incident Response | 10/12 |
| Audit Logging | 9/12 |

## Skills

This agent includes three skill documents (`skills/software-system-auditor/`):

- **regulatory-frameworks.md** -- Detailed control areas, applicable articles/requirements, evidence checklists, and audit checks for all 12 supported frameworks
- **audit-methodology.md** -- Severity classification (5 levels), risk scoring formula, confidence levels, finding format (10 required fields), evidence collection grep patterns, compliance scoring, report template, and large codebase strategies
- **cross-framework-mapping.md** -- 15-control x 12-framework mapping matrix with framework-specific control IDs for 9 major control areas, overlap analysis, and mapping usage instructions

## Examples

The `audit-reports/` folder contains example reports from auditing this repository against 4 frameworks:

### SOC 2 Audit
- `audit-reports/2026-02-21-soc2-audit-report.md` -- Findings mapped to Trust Service Criteria (CC6.x, CC7.x, CC8.x)

### PCI DSS 4.0 Audit
- `audit-reports/2026-02-21-pci-dss-audit-report.md` -- Findings mapped to PCI DSS 4.0 Requirements (Req 2.x through Req 12.x)

### ISO 27001:2022 Audit
- `audit-reports/2026-02-21-iso-27001-audit-report.md` -- Findings mapped to Annex A controls (A.5.x through A.8.x)

### DORA Audit
- `audit-reports/2026-02-21-dora-audit-report.md` -- Findings mapped to DORA Articles (Art. 5 through Art. 15)

## Research

The `docs/research/` folder contains the comprehensive research that informed this agent's design:

- **software-system-auditing-agent-comprehensive-research.md** -- 95-source research document covering 12 regulatory frameworks, 13 audit dimensions, AI-powered audit agent architecture, cross-framework compliance mapping, LLM hallucination risk mitigation, token economics, and legal liability considerations. Reviewed and approved by nw-researcher-reviewer with all quality dimensions scoring above 0.80.

## Commands

| Command | Description |
|---|---|
| `*audit` | Execute the full 7-phase audit workflow (SCOPE through REPORT) |
| `*verify` | Execute Phase 7 only: verify remediation of previous findings |
| `*audit-security` | Security-focused audit (access control, encryption, vulnerability management, configuration) |
| `*audit-supply-chain` | Supply chain-focused audit (dependencies, SBOM, license compliance, provenance) |

## Report Output

Reports are written to:
```
{project-root}/audit-reports/{YYYY-MM-DD}-{framework-id}-audit-report.md
```

Framework IDs: `sox`, `soc2`, `gdpr`, `hipaa`, `pci-dss`, `nist-csf`, `iso-27001`, `fedramp`, `ccpa`, `dora`, `nis2`, `cmmc`

## Related Agents

This agent works well in combination with:
- **system-walkthrough** -- Understand the system's architecture before auditing
- **cognitive-load-analyzer** -- Assess code complexity as an input to maintainability audit dimensions
- **code-smell-detector** -- Deep-dive into code quality issues flagged during the audit
- **test-design-reviewer** -- Assess test quality for the Secure SDLC audit dimension

## Agent Pipeline: Compliance Auditing

```
Codebase --> software-system-auditor --> Framework Selection (multi-select)
                                                |
                                   SCOPE > DISCOVER > COLLECT > ANALYZE > SYNTHESIZE > REPORT
                                                |
                                   One report per selected regulation
```

## Agent Definition

- `software-system-auditor.md` -- The full agent definition

## Attribution

This agent has been created with the agentic framework [nWave](https://nwave.ai).
