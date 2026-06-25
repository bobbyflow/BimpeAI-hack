# Contributing Fast

## Start a task

```powershell
git pull --rebase origin main
git checkout -b your-name/task-name
```

## Save work

```powershell
git status
git add .
git commit -m "Short useful message"
git push -u origin HEAD
```

## Merge work

Open a PR on GitHub into `main`. Use squash merge.

## Do not commit

- API keys
- `.env` files
- generated local state like `bimpe_agent_state.json`
- dependency folders like `node_modules/` or virtualenvs
