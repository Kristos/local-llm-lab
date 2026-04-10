# Cross-Machine Workflow

How code flows between the Mac (editor) and the Windows box (GPU worker).

## Topology

```
MacBook (editor)          GitHub              Windows 5070Ti (worker)
   edit code ──push──▶  main branch  ◀──pull──  run training
   review results        artifacts            push models/results
```

## Day-to-day

### On the Mac (edit + push)

```bash
cd ~/projects/local-llm-lab
# edit scripts, configs, datasets
git add -A && git commit -m "feat: add auction-corpus dataset"
git push origin main
```

### On the Windows box (pull + run)

```cmd
cd C:\Users\krist\projects\local-llm-lab
git pull origin main

:: Activate venv
C:\Users\krist\projects\local-llm-lab-venv\Scripts\activate.bat

:: Run training
python scripts/smoke-test.py
```

### Via SSH from the Mac

```bash
# Pull latest
ssh krist@100.78.110.82 "cd C:\Users\krist\projects\local-llm-lab & git pull origin main"

# Run a script
ssh krist@100.78.110.82 "C:\Users\krist\projects\local-llm-lab-venv\Scripts\python.exe C:\Users\krist\projects\local-llm-lab\scripts\check-env.py"
```

## Gotchas

### Line endings

Git is configured with `core.autocrlf=true` on Windows (default). Python scripts work fine either way. If you see `\r` errors in shell scripts:

```bash
# On Mac, before pushing:
git config core.autocrlf input
```

### Venv is NOT in the repo

The venv at `C:\Users\krist\projects\local-llm-lab-venv` is machine-local and gitignored. After a fresh clone on a new machine, recreate it following `docs/setup-windows.md`.

### Don't git pull during a training run

If a training job is writing to `training/<experiment>/output/`, a `git pull` that touches those files can corrupt the run. Check first:

```cmd
:: Is anything running?
tasklist /fi "imagename eq python.exe" | findstr python
```

### Model weights are NOT in the repo

Trained GGUF files go to `~/.kristosclaw/models/` (served by llama-server) or `training/<experiment>/output/` (local to the machine). Both are gitignored. Share models via the Windows box's filesystem or a separate upload step.

### SSH shell is CMD, not bash

The Windows SSH server drops you into CMD. For PowerShell:

```bash
ssh krist@100.78.110.82 "powershell -Command \"Get-Process python\""
```

For multi-line scripts, write a `.bat` or `.ps1` file and execute it:

```bash
ssh krist@100.78.110.82 "powershell -ExecutionPolicy Bypass -File C:\Users\krist\projects\local-llm-lab\scripts\train.ps1"
```
