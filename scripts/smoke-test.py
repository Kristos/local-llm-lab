#!/usr/bin/env python3
"""
End-to-end smoke test: load a small model via Unsloth, run one training step
on a toy dataset, report GPU memory usage. Proves the full stack works.

Expects check-env.py to pass first.
"""

import sys
import os
import time

# Monkey-patch torchvision.io.VideoReader (removed in 0.26+) before datasets imports it.
# The datasets torch_formatter tries `from torchvision.io import VideoReader` at runtime,
# which crashes with ImportError. A stub class satisfies the import without affecting anything.
import torchvision.io
if not hasattr(torchvision.io, 'VideoReader'):
    torchvision.io.VideoReader = type('VideoReader', (), {})  # type: ignore

import torch

print("local-llm-lab smoke test\n")
start = time.time()

# Verify CUDA before doing anything expensive
if not torch.cuda.is_available():
    print("[FAIL] CUDA not available — run check-env.py first", file=sys.stderr)
    sys.exit(1)

gpu_name = torch.cuda.get_device_name(0)
vram_total = getattr(torch.cuda.get_device_properties(0), 'total_memory', getattr(torch.cuda.get_device_properties(0), 'total_mem', 0)) // (1024 * 1024)
print(f"GPU: {gpu_name} ({vram_total} MB)")

# 1. Load a small model with Unsloth
print("\n[1/4] Loading model via Unsloth (this downloads on first run)...")
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/tinyllama-bnb-4bit",
    max_seq_length=512,
    load_in_4bit=True,
)
print(f"  Model loaded: {type(model).__name__}")

# 2. Apply QLoRA adapter
print("[2/4] Applying QLoRA adapter...")
model = FastLanguageModel.get_peft_model(
    model,
    r=8,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha=16,
    lora_dropout=0,
    use_gradient_checkpointing="unsloth",
)
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
total = sum(p.numel() for p in model.parameters())
print(f"  Trainable params: {trainable:,} / {total:,} ({100*trainable/total:.2f}%)")

# 3. Prepare toy dataset (10 rows inline)
print("[3/4] Preparing toy dataset...")
from datasets import Dataset

toy_data = [
    {"text": "### Instruction: What is the capital of Sweden?\n### Response: Stockholm."},
    {"text": "### Instruction: What is 2+2?\n### Response: 4."},
    {"text": "### Instruction: Who painted the Mona Lisa?\n### Response: Leonardo da Vinci."},
    {"text": "### Instruction: What color is the sky?\n### Response: Blue."},
    {"text": "### Instruction: What is the largest planet?\n### Response: Jupiter."},
    {"text": "### Instruction: What language is spoken in Brazil?\n### Response: Portuguese."},
    {"text": "### Instruction: How many continents are there?\n### Response: Seven."},
    {"text": "### Instruction: What is H2O?\n### Response: Water."},
    {"text": "### Instruction: Who wrote Hamlet?\n### Response: William Shakespeare."},
    {"text": "### Instruction: What is the speed of light?\n### Response: Approximately 300,000 km/s."},
]
dataset = Dataset.from_list(toy_data)

def tokenize(example):
    tokens = tokenizer(example["text"], truncation=True, max_length=512, padding="max_length")
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

dataset = dataset.map(tokenize, batched=True, remove_columns=["text"])
dataset.set_format("torch")
print(f"  Dataset: {len(dataset)} rows, tokenized")

# 4. One training step
print("[4/4] Running one training step...")
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="/tmp/llm-lab-smoke-test",
    max_steps=1,
    per_device_train_batch_size=2,
    logging_steps=1,
    fp16=not torch.cuda.is_bf16_supported(),
    bf16=torch.cuda.is_bf16_supported(),
    report_to="none",
    save_strategy="no",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

result = trainer.train()
loss = result.training_loss
print(f"  Training loss: {loss:.4f}")

# Report GPU usage
vram_used = torch.cuda.max_memory_allocated() // (1024 * 1024)
print(f"\n  Peak GPU memory: {vram_used} MB / {vram_total} MB ({100*vram_used/vram_total:.1f}%)")

elapsed = time.time() - start
print(f"\nSmoke test passed in {elapsed:.1f}s")
