# Datasets

Training data for local-llm-lab experiments. Real corpora are gitignored — only format docs and small samples live in the repo.

## Expected format

Unsloth and HuggingFace `datasets` expect one of these formats:

### 1. Instruction format (recommended for QLoRA)

```jsonl
{"instruction": "What is the capital of Sweden?", "output": "Stockholm."}
{"instruction": "Summarize this text: ...", "input": "The quick brown fox...", "output": "A fox jumped over a dog."}
```

- `instruction` — the prompt/question
- `input` (optional) — additional context
- `output` — the expected response

### 2. Chat format

```jsonl
{"conversations": [{"role": "user", "content": "What is 2+2?"}, {"role": "assistant", "content": "4."}]}
```

### 3. Plain text (for continued pretraining)

```jsonl
{"text": "### Instruction: What is the capital of Sweden?\n### Response: Stockholm."}
```

This is what `smoke-test.py` uses — the simplest format. Good for quick experiments.

## File naming

```
datasets/
  my-experiment/
    train.jsonl       # training split
    eval.jsonl        # evaluation split (optional, 5-10% of train)
    README.md         # what's in this dataset, where it came from, license
```

## Size guidelines

| Model size | Min training rows | Typical |
|-----------|-------------------|---------|
| 1-3B (TinyLlama, Gemma-2B) | 100 | 1k-10k |
| 7-9B (Llama 3, Gemma-7B) | 500 | 5k-50k |
| 13B+ | 1000+ | 10k-100k+ |

For QLoRA fine-tuning, quality beats quantity. 1,000 high-quality instruction pairs often outperform 50,000 noisy ones.

## Gitignore rules

Real datasets with personal or licensed data go in `datasets/` but are gitignored. The `.gitignore` at repo root should include:

```
datasets/**/train.jsonl
datasets/**/eval.jsonl
!datasets/README.md
!datasets/**/README.md
```

Small sample files (< 100 rows) used for smoke tests can be committed.
