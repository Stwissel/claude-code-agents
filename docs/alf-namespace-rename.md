# ALF Namespace Rename Plan

Standardize all agents under the `alf-` prefix for consistent namespacing.

## Naming Convention

- Directory: `alf-{agent-name}/`
- Definition file: `alf-{agent-name}.md`
- JSON output key in codebase-analyzer: `alf-{agent-name}-data.json`

## Rename Map

| Current Directory            | Current File                      | New Directory                | New File                      |
|------------------------------|-----------------------------------|------------------------------|-------------------------------|
| `accessibility-assessor/`    | `accessibility-assessor.md`       | `alf-accessibility-assessor/`| `alf-accessibility-assessor.md`|
| `atdd-developer/`           | `atdd-developer.md`               | `alf-atdd-developer/`       | `alf-atdd-developer.md`      |
| `clean-coder/`              | `clean-coder-agent.md`            | `alf-clean-coder/`          | `alf-clean-coder.md`         |
| `code-smell-detector/`      | `code-smell-detector.md`          | `alf-code-smell-detector/`  | `alf-code-smell-detector.md`  |
| `cognitive-load-analyzer/`  | `cognitive-load-analyzer.md`      | `alf-cognitive-load-analyzer/`| `alf-cognitive-load-analyzer.md`|
| `domain-driven-design/`     | `ddd-architect-agent.md`          | `alf-ddd-architect/`        | `alf-ddd-architect.md`        |
| `legacy-code-expert/`       | `legacy-code-expert.md`           | `alf-legacy-code-expert/`   | `alf-legacy-code-expert.md`   |
| `problem-analyst/`          | `problem-analyst.md`              | `alf-problem-analyst/`      | `alf-problem-analyst.md`      |
| `refactoring-expert/`       | `refactoring-expert.md`           | `alf-refactoring-expert/`   | `alf-refactoring-expert.md`   |
| `software-system-auditor/`  | `software-system-auditor.md`      | `alf-system-auditor/`       | `alf-system-auditor.md`       |
| `system-walkthrough/`       | `system-walkthrough.md`           | `alf-system-walkthrough/`   | `alf-system-walkthrough.md`   |
| `test-design-reviewer/`     | `test-design-reviewer.md`         | `alf-test-design-reviewer/` | `alf-test-design-reviewer.md` |
| `user-story-writer/`        | `user-story-writer.md`            | `alf-user-story-writer/`    | `alf-user-story-writer.md`    |

## Execution Script

Run from `~/dev/claude-code-agents/`:

```bash
#!/bin/bash
set -euo pipefail

cd ~/dev/claude-code-agents

# Renames: old_dir:old_file -> new_dir:new_file
declare -A RENAMES=(
  ["accessibility-assessor"]="alf-accessibility-assessor:accessibility-assessor.md:alf-accessibility-assessor.md"
  ["atdd-developer"]="alf-atdd-developer:atdd-developer.md:alf-atdd-developer.md"
  ["clean-coder"]="alf-clean-coder:clean-coder-agent.md:alf-clean-coder.md"
  ["code-smell-detector"]="alf-code-smell-detector:code-smell-detector.md:alf-code-smell-detector.md"
  ["cognitive-load-analyzer"]="alf-cognitive-load-analyzer:cognitive-load-analyzer.md:alf-cognitive-load-analyzer.md"
  ["domain-driven-design"]="alf-ddd-architect:ddd-architect-agent.md:alf-ddd-architect.md"
  ["legacy-code-expert"]="alf-legacy-code-expert:legacy-code-expert.md:alf-legacy-code-expert.md"
  ["problem-analyst"]="alf-problem-analyst:problem-analyst.md:alf-problem-analyst.md"
  ["refactoring-expert"]="alf-refactoring-expert:refactoring-expert.md:alf-refactoring-expert.md"
  ["software-system-auditor"]="alf-system-auditor:software-system-auditor.md:alf-system-auditor.md"
  ["system-walkthrough"]="alf-system-walkthrough:system-walkthrough.md:alf-system-walkthrough.md"
  ["test-design-reviewer"]="alf-test-design-reviewer:test-design-reviewer.md:alf-test-design-reviewer.md"
  ["user-story-writer"]="alf-user-story-writer:user-story-writer.md:alf-user-story-writer.md"
)

for old_dir in "${!RENAMES[@]}"; do
  IFS=':' read -r new_dir old_file new_file <<< "${RENAMES[$old_dir]}"

  echo "Renaming $old_dir/ -> $new_dir/"
  git mv "$old_dir" "$new_dir"

  if [[ "$old_file" != "$new_file" ]]; then
    echo "  Renaming $old_file -> $new_file"
    git mv "$new_dir/$old_file" "$new_dir/$new_file"
  fi
done

echo ""
echo "Done. Review with: git status"
echo "After-rename tasks:"
echo "  1. Update references in codebase-analyzer orchestrator (agent registry paths)"
echo "  2. Update install.sh agent paths"
echo "  3. Update README.md"
echo "  4. Update any ~/.claude/commands/ or .claude/commands/ that reference old paths"
```

## Post-Rename Updates Required

1. **Codebase Analyzer orchestrator** (`~/dev/codebase-analyzer/codebase-analyzer.md` and `~/.claude/commands/alf-analyze.md`) -- update all agent definition paths in the Agent Registry table
2. **install.sh** -- update directory references
3. **README.md** -- update agent listing
4. **Knowledge base references** -- `domain-driven-design/ddd-expert-knowledge-base.md` moves to `alf-ddd-architect/ddd-expert-knowledge-base.md`
