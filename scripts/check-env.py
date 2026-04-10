#!/usr/bin/env python3
"""
Verifies the local-llm-lab training stack in under 30 seconds.
Checks: Python version, PyTorch, CUDA, GPU detection, Unsloth, writable model dir.

Exit 0 = all good. Exit 1 = first failure with labeled error.
"""

import sys
import os
import time

start = time.time()

def ok(label: str, detail: str = ""):
    print(f"  [OK] {label}" + (f" — {detail}" if detail else ""))

def fail(label: str, detail: str = ""):
    print(f"  [FAIL] {label}" + (f" — {detail}" if detail else ""), file=sys.stderr)
    sys.exit(1)

print("local-llm-lab environment check\n")

# 1. Python version
v = sys.version_info
if v.major != 3 or v.minor < 10:
    fail("Python version", f"need >=3.10, got {v.major}.{v.minor}.{v.micro}")
ok("Python", f"{v.major}.{v.minor}.{v.micro} at {sys.executable}")

# 2. PyTorch
try:
    import torch
    ok("PyTorch", torch.__version__)
except ImportError:
    fail("PyTorch", "not installed — pip install torch")

# 3. CUDA available
if not torch.cuda.is_available():
    fail("CUDA", "torch.cuda.is_available() is False — check CUDA toolkit + driver")
ok("CUDA available", f"runtime {torch.version.cuda}")

# 4. GPU detection
try:
    gpu_name = torch.cuda.get_device_name(0)
    sm = torch.cuda.get_device_capability(0)
    vram_mb = torch.cuda.get_device_properties(0).total_mem // (1024 * 1024)
    ok("GPU", f"{gpu_name} (sm_{sm[0]}{sm[1]}, {vram_mb} MB)")
except Exception as e:
    fail("GPU detection", str(e))

# 5. Unsloth
try:
    import unsloth
    ok("Unsloth", unsloth.__version__)
except ImportError:
    fail("Unsloth", "not installed — pip install unsloth")
except NotImplementedError as e:
    fail("Unsloth", f"accelerator issue: {e}")

# 6. Writable model dir
model_dir = os.path.expanduser("~/.kristosclaw/models")
os.makedirs(model_dir, exist_ok=True)
test_file = os.path.join(model_dir, ".write-test")
try:
    with open(test_file, "w") as f:
        f.write("ok")
    os.remove(test_file)
    ok("Model dir writable", model_dir)
except Exception as e:
    fail("Model dir writable", f"{model_dir} — {e}")

elapsed = time.time() - start
print(f"\nAll checks passed in {elapsed:.1f}s")
