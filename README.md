# local-llm-lab

Personal infrastructure for fine-tuning and serving local LLMs on a Windows + Blackwell 5070Ti box. The repo lives on the MacBook (edited with Claude Code / kristos-claw), pushed to GitHub, pulled on the Windows machine for execution. Trained models are served by `llama.cpp` and consumed by [kristos-claw](https://github.com/Kristos/kristos-claw) as its inference backend — closing the loop between training and using local models.

**Current state:** v0.1 Training Infra Setup (in progress). The first goal is a verified Unsloth + CUDA + Gemma 4 stack with a passing smoke test. No real training happens in v0.1.

## Hardware Topology

```
┌──────────────────────────────────────┐         ┌─────────────────────────────────┐
│ MacBook Pro 2017 (100.75.78.11)      │         │ Windows 5070Ti (100.78.110.82)  │
│ "the orchestrator"                   │         │ "the GPU worker"                │
├──────────────────────────────────────┤         ├─────────────────────────────────┤
│ - kristos-claw v1.5 agent runs       │──HTTP──▶│ - llama.cpp serving (port 8080) │
│ - MCP servers (Docker via Colima)    │  calls  │ - Unsloth training jobs         │
│ - Webhooks + cron                    │◀─gguf───│ - Model weights on local disk   │
└──────────────────────────────────────┘         └─────────────────────────────────┘
            ▲                                                ▲
            │ git pull                                       │ git pull
            │                                                │
       ┌────┴────────────────────────────────────────────────┴────┐
       │  MacBook (dev workstation) — edits this repo             │
       └──────────────────────────────────────────────────────────┘
```

## Quickstart (once v0.1 ships)

```powershell
# On the Windows box:
git clone https://github.com/Kristos/local-llm-lab
cd local-llm-lab
# follow docs/setup-windows.md to install CUDA + Unsloth + venv
python scripts/check-env.py     # verifies the stack
python scripts/smoke-test.py    # one training step on a 10-row toy dataset
```

## Repo Layout

| Path | Purpose |
|---|---|
| `.planning/` | GSD project planning (PROJECT, ROADMAP, REQUIREMENTS, STATE) |
| `training/` | Per-experiment configs and training scripts |
| `scripts/` | Reusable: env check, train wrapper, gguf export |
| `datasets/` | Format docs + small samples (real corpora gitignored) |
| `docs/` | Setup guides, gotchas, runbooks |

## What this is NOT

- A scalable training cluster
- A model registry or experiment tracker (beyond the filesystem)
- A multi-GPU setup (one 5070Ti)
- A pre-training environment (the GPU can't, full stop)
- Anything that runs on the MacBook Pro 2017 home server (Radeon Pro 555 is unusable for ML)

See `.planning/REQUIREMENTS.md` for the explicit out-of-scope list.

## Related Projects

- **[kristos-claw](https://github.com/Kristos/kristos-claw)** — the consumer. Models trained here become the inference backend for kc's Phase 22+ agent runs.
