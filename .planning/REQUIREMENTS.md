# Requirements: local-llm-lab v0.1 — Training Infra Setup

**Defined:** 2026-04-08
**Core value:** Verified, reproducible Unsloth + Blackwell sm_120 + Gemma 4 stack on the Windows 5070Ti box, with a passing smoke test proving the GPU is actually used. Zero real training happens in v0.1 — that's v0.2.

## Milestone Theme

This is the boring-but-essential foundation. Without it, every future training run starts from "wait, why is CUDA broken again." With it, every future run starts from `python scripts/smoke-test.py && python scripts/train.py <config>`.

**Definition of done:** a clean clone of this repo on the Windows machine, plus a single setup-doc walkthrough, gets a person from zero to "Unsloth loaded Gemma-4-2B, ran one training step, GPU utilized" in under 30 minutes. The smoke test is the acceptance criterion.

## v1 Requirements (Milestone v0.1)

### Environment Setup

- [ ] **LAB-01**: Kristo can follow `docs/setup-windows.md` from a clean Windows install (or the existing 5070Ti box) to install: CUDA 12.x compatible with Blackwell sm_120, Python 3.11+, a virtual environment, PyTorch with CUDA support, and Unsloth. Each step has expected output and the gotchas Kristo hits during the install are captured inline. Setup completes in under 30 minutes from a working CUDA install (CUDA itself excluded from the timer because it's a one-time install).

- [ ] **LAB-02**: A `scripts/check-env.py` script verifies the entire stack in under 30 seconds: PyTorch sees CUDA, GPU is detected as the 5070Ti (sm_120), Unsloth imports without errors, the configured base model directory exists and is writable. Exits 0 on full success, exits 1 with a labeled error message naming the first failed check.

### Repo Structure + Templates

- [ ] **LAB-03**: A `training/gemma-4-lora/` example directory contains a complete Unsloth QLoRA config for Gemma-4-2B (LoRA rank, target modules, learning rate, batch size, max steps), a 10-row toy dataset in `datasets/toy/instruction-tiny.jsonl`, and a README.md explaining what each config field does and links to the upstream Unsloth docs.

- [ ] **LAB-04**: A `datasets/README.md` documents the dataset format (Alpaca-style JSONL: `{instruction, input, output}`), the gitignore policy (real datasets not committed; templates and toy datasets are), and how to add a new dataset directory.

### Smoke Test (the acceptance criterion)

- [ ] **LAB-05**: A `scripts/smoke-test.py` runs end-to-end on the Windows box and:
  1. Calls `check-env.py` first; aborts with the same error if the env check fails
  2. Loads Gemma-4-2B via Unsloth with QLoRA config
  3. Loads the 10-row toy dataset
  4. Runs exactly **one training step** (no full epoch; just one forward + backward pass)
  5. Reports peak GPU memory used and GPU utilization > 0%
  6. Exits 0 with a "smoke test passed" message and the wall-clock duration
  Total runtime budget: under 5 minutes from cold start (model download excluded; if the model is not cached the script downloads it and reports the download time separately).

### Cross-Machine Workflow

- [ ] **LAB-06**: A `docs/cross-machine-workflow.md` documents the MacBook → GitHub → Windows pull cycle: how to edit on Mac, push, pull on Windows, run training, push experiment configs back. Includes the exact PowerShell commands for the Windows side. Captures the gotchas around line endings, virtualenv activation, and `git pull` race conditions when a training job is mid-run.

### Documentation

- [ ] **LAB-07**: `README.md` at the repo root explains what the repo is in 2-3 paragraphs, links to the setup doc, the smoke test, and the cross-machine workflow. Includes the hardware topology diagram from PROJECT.md.

## Out of Scope

These are deliberate exclusions. Each is a real future need but does not belong in v0.1.

| Feature | Reason |
|---------|--------|
| Real training run on a real dataset | v0.2 — the whole point of v0.1 is the smoke test passes first |
| Dataset curation pipelines (HuggingFace pulls, filtering, validation) | v0.2+ |
| Multiple base models (Llama 3, Qwen, Mistral, etc.) | v0.2+ — Gemma 4 is the only target for v0.1 |
| W&B / TensorBoard logging | v0.2 — smoke test doesn't need observability |
| Checkpoint resume | v0.2 — single-step smoke test can't even checkpoint |
| GGUF export pipeline | v0.2 — the smoke test doesn't produce a model worth exporting |
| llama.cpp serving config templates | v0.2 — same reason |
| Integration with kristos-claw (calling the model from kc) | v0.2 — closes the loop |
| Ollama as an alternative serving backend | v0.3+ |
| MLX (Apple Silicon training) | Out of scope. The MacBook Pro 2017 server has AMD, not Apple Silicon. The dev MacBook is Apple Silicon but inference happens on Windows. |
| Multi-GPU training | The box has one 5070Ti |
| RLHF / DPO / ORPO | SFT first, validate the loop, then maybe |
| Pre-training from scratch | Cannot, full stop |
| Cloud training fallback (Lambda, RunPod, etc.) | The whole point is local |
| Model evaluation harnesses (LM Eval, etc.) | v0.3+ |
| Production model registry / experiment tracking beyond filesystem | v0.3+ — solo dev, FS is enough |
| Hosting on the MacBook Pro 2017 server | Hardware can't, ever |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| LAB-01 | Phase 1 | Pending |
| LAB-02 | Phase 1 | Pending |
| LAB-03 | Phase 2 | Pending |
| LAB-04 | Phase 2 | Pending |
| LAB-05 | Phase 3 | Pending |
| LAB-06 | Phase 1 | Pending |
| LAB-07 | Phase 3 | Pending |

**Coverage:**
- v0.1 requirements: 7 total
- Mapped to phases: 7 ✓
- Unmapped: 0

---
*Requirements defined: 2026-04-08*
*Baseline: working llama.cpp serving GLM-4.7-Flash on the Windows box at 100.78.110.82:8080 — we know the GPU + sm_120 build works for inference, training is the new variable.*
