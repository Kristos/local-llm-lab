# Windows 5070Ti Setup Guide

Step-by-step setup for the training stack on the Windows GPU box (`krist@100.78.110.82`).

## Prerequisites (already installed)

- **GPU:** NVIDIA GeForce RTX 5070 Ti (16GB VRAM, Blackwell sm_120)
- **Driver:** 595.97 (CUDA runtime 13.2)
- **CUDA Toolkit:** v12.8 at `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8`
- **Git:** via Scoop at `C:\Program Files\Git`
- **llama-server:** running at `C:\AI\llama.cpp\build\bin\Release\llama-server.exe` (port 8080)

## 1. Python 3.11.9 (per-user install)

Python is installed at `C:\Users\krist\AppData\Local\Programs\Python\Python311\python.exe`.

**If you need to reinstall:**
```powershell
# Download
Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile "$env:USERPROFILE\Downloads\python-3.11.9-amd64.exe"

# Silent install — per-user, no PATH modification, no py launcher (avoids SD Forge conflict)
Start-Process -Wait -FilePath "$env:USERPROFILE\Downloads\python-3.11.9-amd64.exe" -ArgumentList '/quiet','InstallAllUsers=0','PrependPath=0','Include_launcher=0','Include_test=0'
```

**Why 3.11.9?** It's the last 3.11 release with binary installers. Unsloth + PyTorch support 3.10-3.12; 3.11 is the sweet spot for compatibility.

**Why per-user + no PATH?** Stable Diffusion Forge under `C:\AI\` has its own embedded Python. Adding our Python to system PATH or installing the py launcher could interfere with Forge's venv. We use full paths or venv activation instead.

## 2. Venv (isolated from everything)

```cmd
C:\Users\krist\AppData\Local\Programs\Python\Python311\python.exe -m venv C:\Users\krist\projects\local-llm-lab-venv
```

The venv lives at `C:\Users\krist\projects\local-llm-lab-venv`. All pip installs go here, not system-wide.

**Activate in CMD:**
```cmd
C:\Users\krist\projects\local-llm-lab-venv\Scripts\activate.bat
```

**Activate in PowerShell:**
```powershell
C:\Users\krist\projects\local-llm-lab-venv\Scripts\Activate.ps1
```

## 3. PyTorch with CUDA 12.8

```cmd
C:\Users\krist\projects\local-llm-lab-venv\Scripts\pip.exe install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

**Expected:** `torch-2.11.0+cu128`

### Gotcha: Unsloth overwrites PyTorch

Unsloth's pip dependencies pull the CPU-only torch build. **Always reinstall PyTorch CUDA after installing Unsloth:**

```cmd
C:\Users\krist\projects\local-llm-lab-venv\Scripts\pip.exe install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128 --force-reinstall --no-deps
```

## 4. Unsloth

```cmd
C:\Users\krist\projects\local-llm-lab-venv\Scripts\pip.exe install unsloth
```

Then immediately reinstall PyTorch CUDA (see gotcha above).

### Gotcha: Flash Attention 2 on Windows

Unsloth will warn: "Flash Attention 2 installation seems to be broken. Using Xformers instead." This is normal on Windows — FA2 doesn't have Windows wheels. Xformers works fine for QLoRA, no performance difference.

### Gotcha: sm_120 (Blackwell) support

The RTX 5070 Ti is sm_120 (Blackwell). PyTorch 2.11+ supports it natively. Older PyTorch versions (<2.6) will fail with "CUDA error: no kernel image is available." If you see this, upgrade PyTorch.

## 5. Verify

```cmd
C:\Users\krist\projects\local-llm-lab-venv\Scripts\python.exe scripts/check-env.py
```

Expected output:
```
local-llm-lab environment check

  [OK] Python — 3.11.9 at C:\Users\krist\projects\local-llm-lab-venv\Scripts\python.exe
  [OK] PyTorch — 2.11.0+cu128
  [OK] CUDA available — runtime 12.8
  [OK] GPU — NVIDIA GeForce RTX 5070 Ti (sm_120, 16303 MB)
  [OK] Unsloth — 2026.4.4
  [OK] Model dir writable — C:\Users\krist/.kristosclaw/models

All checks passed in <30s
```

## 6. Smoke test (optional, downloads ~1.5GB model on first run)

```cmd
C:\Users\krist\projects\local-llm-lab-venv\Scripts\python.exe scripts/smoke-test.py
```

Loads `unsloth/gemma-2-2b-bnb-4bit`, applies QLoRA adapter, runs one training step on a 10-row toy dataset. Reports GPU memory usage. Takes ~2-3 minutes on first run (model download), ~30s after.

## Installed package versions (reference)

```
torch==2.11.0+cu128
torchvision==0.26.0+cu128
torchaudio==2.11.0+cu128
unsloth==2026.4.4
transformers==5.5.0
peft==0.18.1
datasets==4.3.0
accelerate==1.13.0
bitsandbytes==0.49.2
xformers==0.0.35
```
