# kitepilot

Single-user Zerodha/Kite NSE intraday ML trading bot — monorepo scaffold (pnpm + Turborepo). This workspace will host FastAPI services, a Next.js ops UI, research/backtests, and infra.

## Quickstart

```bash
pnpm -w i
pre-commit install --install-hooks
pnpm -w run format
pnpm -w run build
```

> Conventional Commits enforced via commit-msg hook (pre-commit + commitlint).
