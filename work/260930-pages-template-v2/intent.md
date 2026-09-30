# Intent — Pages workflow template v2 (accepted)

Status: accepted by Ty on 30/09 (he approved the template spec and shipped claude-config PRs 9, 10 and 11).

Bring this repo's Pages workflow to the shared template: coverage checks the whole tracked tree, symlinks are refused, globs never split on spaces, and write permissions live only on the deploy job. The rollout's first repo went alone and passed its live check on 30/09; this repo follows it (the rollout list is in claude-config).
