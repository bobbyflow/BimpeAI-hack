# BimpeAI Hack

Shared project workspace for the BimpeAI hack build.

Repo: https://github.com/bobbyflow/BimpeAI-hack

## 60-minute team workflow

We optimise for speed, not ceremony.

1. **Split files before coding.** Avoid two people editing the same file at the same time.
2. **Branch for each task.** Example: `git checkout -b covi/api-test`.
3. **Commit every working checkpoint.** Small commits are easier to recover from.
4. **Push early.** Do not keep important work only on your laptop.
5. **Merge fast.** Open PRs into `main`; squash merge when green/working.
6. **Pull before starting new work.** `git pull --rebase origin main`.

## Fast start

```powershell
git clone https://github.com/bobbyflow/BimpeAI-hack.git
cd BimpeAI-hack
git checkout -b your-name/task-name
```

## API key setup

Never commit secrets. Put API keys in your shell only:

```powershell
$env:BIMPE_API_KEY="sk_..."
```

Optional base URL override:

```powershell
$env:BIMPE_BASE_URL="https://api.bimpe.ai/api/v1/console"
```

## Useful commands

```powershell
python scripts/bimpe_hack.py --help
python scripts/bimpe_hack.py list-workflows
```

## Conflict rule

If Git reports a conflict, stop and call it out in the team chat. Do not guess-merge demo-critical files.
