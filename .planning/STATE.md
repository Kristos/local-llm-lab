---
project: local-llm-lab
status: initialized
current_milestone: v0.1
current_phase: 1
last_activity: 2026-04-08
---

# State: local-llm-lab

## Status

Project bootstrapped 2026-04-08. Active milestone: v0.1 Training Infra Setup. No phase started yet — Phase 1 (Windows Environment) is the next action.

## Current Position

- **Milestone:** v0.1 — Training Infra Setup
- **Phase:** 1 — Windows Environment (not started)
- **Plans:** none yet

## Plans

| Phase | Plans | Status |
|---|---|---|
| 1. Windows Environment | 0/? | Pending |
| 2. Repo Templates | 0/? | Pending |
| 3. Smoke Test + Docs | 0/? | Pending |

## Decisions Locked

- **Hardware split:** training on Windows 5070Ti (CUDA, sm_120). MacBook Pro 2017 home server is out of scope (Radeon Pro 555 is unusable for ML). Edits on dev MacBook, push/pull via GitHub.
- **Framework:** Unsloth only (CUDA-only is fine, GPU is on Windows).
- **Base model:** Gemma 4 family. Smoke test targets Gemma-4-2B specifically.
- **Acceptance criterion for v0.1:** end-to-end smoke test runs in <5 min on Windows, exits 0, reports >0% GPU utilization. Cold-clone install in <30 min.
- **Out of v0.1:** real training runs, dataset curation pipelines, multiple base models, GGUF export, kc integration, observability — all v0.2+.

## Tech Debt

None yet — fresh project.

## Next Action

Plan Phase 1 once user is ready. The Windows environment setup is mostly documentation work + a small `check-env.py` script — likely 2-3 plans.

## Related Projects

- **kristos-claw** (`~/projects/kristos-claw/`) — the consumer of trained models. v1.5 Homelab Agent will use `local-llm-lab` outputs as the inference backend for scheduled agent runs. Integration point: the Windows llama.cpp server endpoint (`100.78.110.82:8080/v1`).
