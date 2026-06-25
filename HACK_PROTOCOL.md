# 60-Minute Build Protocol

## Goal

Ship the smallest demoable BimpeAI workflow, then polish only if time remains.

## Branch model

- `main`: demoable state only.
- `name/task`: active work.
- PRs are fast checkpoints, not formal review ceremonies.

## Merge policy

- Prefer **squash merge**.
- Delete branch after merge.
- If a PR blocks the team, merge the smallest working subset first.

## Suggested ownership split

| Owner | Area | Files to avoid conflicts |
|---|---|---|
| Bobby | API/script integration | `scripts/bimpe_hack.py`, API notes |
| covifranklin | Demo scenario + testing transcript | markdown/txt demo docs |
| headrohit | README/pitch/demo checklist or UI wrapper | docs/UI files |

Change ownership if someone is faster in an area. The key rule is one owner per hot file.

## 60-minute timer

- 0-10 min: clone, keys, run script help, choose demo path.
- 10-35 min: build only the happy path.
- 35-45 min: test full demo once end-to-end.
- 45-55 min: fix blockers only.
- 55-60 min: freeze main, rehearse, no risky refactors.

## Emergency recovery

```powershell
# save current work
git add .
git commit -m "WIP checkpoint"
git push -u origin HEAD

# get latest main safely
git fetch origin
git checkout main
git pull --rebase origin main
```
