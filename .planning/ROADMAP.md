# Roadmap: local-llm-lab

## Milestones

- 🚧 **v0.1 Training Infra Setup** — Phases 1-3 (in progress)

## Phases

- [ ] **Phase 1: Windows Environment** — Install + verify Unsloth, CUDA 12.x for sm_120, PyTorch+CUDA, Python venv. Document setup with gotchas. Cross-machine git workflow doc. `check-env.py` validator script.
- [ ] **Phase 2: Repo Templates** — Gemma-4-2B QLoRA config, 10-row toy dataset, `training/gemma-4-lora/` worked example, `datasets/README.md` format docs.
- [ ] **Phase 3: Smoke Test + Docs** — `scripts/smoke-test.py` end-to-end (loads model, runs one training step, reports GPU usage), root README with topology diagram and quickstart.

## Phase Details

### Phase 1: Windows Environment
**Goal**: Get Unsloth + Blackwell sm_120 + CUDA + PyTorch installed on the Windows 5070Ti box, with a verifier script that proves every layer works in under 30 seconds.
**Depends on**: Nothing (first phase)
**Requirements**: LAB-01, LAB-02, LAB-06
**Success Criteria** (what must be TRUE):
  1. `docs/setup-windows.md` walks through CUDA / Python / venv / PyTorch / Unsloth install end-to-end with each step's expected output. Captures every gotcha hit during the actual install.
  2. `scripts/check-env.py` runs in <30s on the Windows box and verifies: PyTorch sees CUDA, GPU detected as 5070Ti with sm_120, Unsloth imports cleanly, model dir writable. Exits 0 on success, 1 with a labeled error on first failure.
  3. `docs/cross-machine-workflow.md` documents the MacBook → GitHub → Windows pull cycle including PowerShell commands, line-ending gotchas, virtualenv activation, and "what happens if I git pull while a training job is running".
  4. A clean clone + the setup doc gets a fresh user (or future-you) from zero to "check-env.py exits 0" in under 30 minutes (CUDA install excluded — that's a one-time thing).
**Plans**: TBD

### Phase 2: Repo Templates
**Goal**: Provide the worked example skeleton (Gemma-4-2B QLoRA) and dataset conventions so v0.2's first real training run is "fill in the blanks", not "design the structure".
**Depends on**: Phase 1 (Unsloth available to validate the config syntax)
**Requirements**: LAB-03, LAB-04
**Success Criteria** (what must be TRUE):
  1. `training/gemma-4-lora/` contains: a complete Unsloth QLoRA config for Gemma-4-2B (LoRA rank, target modules, learning rate, batch size, max steps), a `README.md` explaining each config field with links to upstream Unsloth docs, and the path the smoke test will use.
  2. `datasets/toy/instruction-tiny.jsonl` exists with exactly 10 rows in Alpaca format `{instruction, input, output}`. Hand-curated, deterministic content (not random).
  3. `datasets/README.md` documents the format, the gitignore policy (templates + toy committed; real datasets gitignored), and how to add a new dataset.
  4. The config validates: `python -c "from training.gemma_4_lora import config; print(config)"` (or equivalent) loads without error on the Windows box.
**Plans**: TBD

### Phase 3: Smoke Test + Docs
**Goal**: Ship the acceptance-criterion smoke test that proves the entire stack works end-to-end on real hardware, plus the root README that lets future-you (or anyone) understand the project in 30 seconds.
**Depends on**: Phases 1 + 2 (env + template)
**Requirements**: LAB-05, LAB-07
**Success Criteria** (what must be TRUE):
  1. `scripts/smoke-test.py` runs end-to-end on the Windows box: calls `check-env.py` first, loads Gemma-4-2B via Unsloth with the QLoRA config from Phase 2, loads the 10-row toy dataset, runs exactly one training step (one forward + backward pass), reports peak GPU memory + GPU utilization > 0%, exits 0 with wall-clock duration.
  2. Total smoke-test runtime under 5 minutes from cold start (model download time reported separately if model is not yet cached).
  3. Cold-clone test on a fresh checkout: `git clone` → `docs/setup-windows.md` → `python scripts/smoke-test.py` succeeds in <30 minutes total. This is the milestone acceptance.
  4. `README.md` at the repo root explains the project in 2-3 paragraphs, includes the hardware topology diagram, links to setup / smoke test / cross-machine docs, and shows the canonical "first run" command.
**Plans**: TBD

## Progress

| Phase | Milestone | Plans | Status | Completed |
|-------|-----------|-------|--------|-----------|
| 1. Windows Environment | v0.1 | 0/? | Not started | — |
| 2. Repo Templates | v0.1 | 0/? | Not started | — |
| 3. Smoke Test + Docs | v0.1 | 0/? | Not started | — |
