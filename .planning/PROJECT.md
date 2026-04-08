# local-llm-lab

## What This Is

A personal infrastructure project for fine-tuning and serving local LLMs on the Windows 5070Ti box. The repo lives on the MacBook (edited with Claude Code / kristos-claw), pushed to GitHub, pulled on the Windows machine for execution. Outputs (GGUF weights) are served by llama.cpp on the same Windows host and consumed by `kristos-claw` as its `llamacpp` provider endpoint.

**For:** Personal research and dogfooding by Kristo. The goal is to make "fine-tune a small model on my own data, serve it, use it from kc" a one-evening operation instead of a one-weekend yak shave.

**Core value:** Close the loop between training and using local models. Every model trained here can immediately become the inference backend for kristos-claw agent runs on the home server.

## Why It Exists

Training runs need a GPU. The 5070Ti (Blackwell sm_120) can fine-tune Gemma-class models with QLoRA in reasonable time, but the toolchain is full of CUDA version traps, Windows-specific gotchas, and dependency hell. This repo captures the *working* setup so future me doesn't have to relearn it.

It also creates a clean separation:
- **kristos-claw** = the agent (consumer)
- **local-llm-lab** = the model factory (producer)
- Both are independent projects with their own GSD planning, but they share the Windows llama.cpp endpoint as the integration point.

## Hardware Topology

```
┌──────────────────────────────────────┐         ┌─────────────────────────────────┐
│ MacBook Pro 2017 (100.75.78.11)      │         │ Windows 5070Ti (100.78.110.82)  │
│ "the orchestrator"                   │         │ "the GPU worker"                │
├──────────────────────────────────────┤         ├─────────────────────────────────┤
│ - kristos-claw v1.5 agent runs       │──HTTP──▶│ - llama.cpp serving (port 8080) │
│ - MCP servers (Docker via Colima)    │  calls  │ - Unsloth training jobs         │
│ - Webhooks + cron                    │◀─gguf───│ - Model weights on local disk   │
│ - 16 GB RAM, no usable GPU           │         │ - Dataset workspace             │
└──────────────────────────────────────┘         └─────────────────────────────────┘
            ▲                                                ▲
            │ git pull                                       │ git pull
            │                                                │
       ┌────┴────────────────────────────────────────────────┴────┐
       │  MacBook (dev workstation)                               │
       │  ~/projects/local-llm-lab/   — code, scripts, docs       │
       │  ~/projects/kristos-claw/    — kc consumer               │
       └──────────────────────────────────────────────────────────┘
```

**Where things run:**
- **MacBook** — edits this repo, never trains anything
- **Windows 5070Ti** — runs every Unsloth training job, runs llama.cpp serving, owns model weights
- **MacBook Pro 2017 home server** — out of scope for this repo (orchestrator only, no LLM compute)

The 2017 MBP server has a Radeon Pro 555 (2 GB VRAM, AMD, no CUDA, no real PyTorch support on macOS). It cannot train and cannot reasonably serve LLMs. Its role in the broader ecosystem is *consuming* models that this repo produces, not running anything itself.

## Repo Layout

```
local-llm-lab/
├── .planning/              # GSD project planning
├── training/               # Per-experiment configs + scripts
│   └── gemma-4-lora/       # First worked example (v0.1 smoke test)
├── scripts/                # Reusable: env check, train wrapper, gguf export, etc.
├── datasets/               # Dataset templates + small samples (real corpora gitignored)
├── docs/                   # Setup guides, gotchas, runbooks
└── README.md
```

**Gitignored** (lives only on Windows):
- Model weights (`*.gguf`, `*.safetensors`, `checkpoints/`)
- Large datasets (`datasets/raw/`, anything over a few MB)
- W&B/TensorBoard run logs
- Python virtualenvs

## Tech Stack

| Layer | Choice | Notes |
|-------|--------|-------|
| Training framework | **Unsloth** | Fastest QLoRA on Windows + Blackwell. CUDA-only, fine since GPU is on Windows. |
| Base model targets | Gemma 4 family (1B, 2B, 4B); Qwen, Llama later | Small enough to QLoRA on a 5070Ti |
| Inference serving | llama.cpp (already deployed on Windows at 100.78.110.82:8080) | Same endpoint kristos-claw v1.4 already uses |
| Model format | HuggingFace safetensors → GGUF (Q4_K_M, Q5_K_M) | GGUF for serving via llama.cpp |
| Dataset format | JSONL with `{instruction, input, output}` schema | Standard Alpaca-style |
| Job orchestration | PowerShell scripts + manual git pull on Windows | Keep it dumb. v0.2+ might add a runner. |

## Current State

**Active:** v0.1 — Training infra setup (started 2026-04-08).

**Theme:** Get the Unsloth + Blackwell sm_120 + Gemma 4 stack installed and *verified* on the Windows box, with one passing smoke test that proves the GPU is actually being used. No real training happens in v0.1 — that's v0.2.

**Success metric:** `python scripts/smoke-test.py` on the Windows machine loads Gemma-4-2B via Unsloth, runs one training step on a 10-row toy dataset, and reports >0% GPU utilization. End to end in under 5 minutes from a clean clone.

## Next Milestone Goals — v0.2 First Real Training Run

(Not committed; scoping after v0.1 ships.)

- Take a real curated dataset (~500 rows, hand-picked for a specific task — e.g. "summarize a Slack thread", "classify an email")
- QLoRA fine-tune Gemma 4 on it
- Export to GGUF
- Deploy to the llama.cpp server replacing or alongside GLM-4.7-Flash
- Trigger a kc agent job (from kristos-claw v1.5) that uses the new model
- A/B compare against the base model

This is when the loop actually closes.

## Out of Scope (Forever or v0.3+)

- **Pre-training from scratch** — the 5070Ti can't, full stop
- **Multi-GPU training** — single 5070Ti only
- **Hosting on the MacBook Pro 2017 home server** — already explained why
- **Cloud training fallback** — the whole point is local
- **Model evaluation harnesses** (Eleuther LM Eval, etc.) — v0.3+
- **RLHF / DPO / preference tuning** — start with SFT, see if it's useful first
- **Production model registry** — solo dev, the filesystem is the registry
