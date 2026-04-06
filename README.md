# Claude Cost by Task Type: Haiku vs Sonnet vs Opus

> Actual measured API costs across 10 task types — not just token rates.

Inspired by [@Shpigford](https://twitter.com/Shpigford)'s post on model cost by task type. This repo contains scripts to **actually measure** what each Claude model costs for real-world task categories, using the Anthropic API.

## Results

| Task | Haiku 4.5 | Sonnet 4.6 | Opus 4.6 | Best Value |
|------|-----------|------------|----------|------------|
| classification | $0.0000 | $0.0001 | $0.0002 | Haiku 4.5 |
| entity_extraction | $0.0001 | $0.0003 | $0.0005 | Haiku 4.5 |
| summarization | $0.0002 | $0.0005 | $0.0009 | Haiku 4.5 |
| qa_simple | $0.0000 | $0.0001 | $0.0001 | Haiku 4.5 |
| qa_complex | $0.0001 | $0.0004 | $0.0007 | Haiku 4.5 |
| code_gen_simple | $0.0002 | $0.0006 | $0.0010 | Haiku 4.5 |
| code_review | $0.0003 | $0.0008 | $0.0014 | Haiku 4.5 |
| creative_writing | $0.0001 | $0.0002 | $0.0003 | Haiku 4.5 |
| data_analysis | $0.0002 | $0.0006 | $0.0010 | Haiku 4.5 |
| chat_reply | $0.0001 | $0.0003 | $0.0005 | Haiku 4.5 |
| **TOTAL** | **$0.0013** | **$0.0039** | **$0.0066** | — |

> *Placeholder data shown above. Run `benchmark.py` then `analyze.py` to populate with real measurements.*

## Key Findings

- Haiku 4.5 is the cheapest option for every task type when quality is sufficient
- Sonnet 4.6 costs ~3x more than Haiku 4.5 (matching the input price ratio)
- Opus 4.6 costs ~5x more than Haiku 4.5 (matching the input price ratio)
- Output-heavy tasks (code generation, code review) show the largest absolute cost differences
- Simple tasks (classification, QA) cost fractions of a cent even on Opus

> *Run the benchmark yourself to get real numbers and compare quality vs cost.*

## Methodology

- Each task is run **1 time per model** to keep costs minimal
- Token counts are taken directly from the API response (`usage.input_tokens`, `usage.output_tokens`)
- Costs are computed from published Anthropic pricing (as of 2025):

| Model | Input (per MTok) | Output (per MTok) |
|-------|------------------|--------------------|
| Haiku 4.5 | $1.00 | $5.00 |
| Sonnet 4.6 | $3.00 | $15.00 |
| Opus 4.6 | $5.00 | $25.00 |

- 10 task types cover classification, extraction, summarization, QA, code generation, code review, creative writing, data analysis, and chat
- Prompts are intentionally short to keep benchmark costs under $0.01 total

## Run It Yourself

### Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"
```

### Dry run (no API calls)

```bash
python benchmark.py --dry-run
```

### Run the benchmark

```bash
python benchmark.py
```

This produces `results.json` with token counts, costs, and latencies for every task/model pair.

### Generate the report

```bash
python analyze.py
```

This reads `results.json` and produces `RESULTS.md` with the full analysis table and insights.

### Custom output path

```bash
python benchmark.py --output my_results.json
python analyze.py my_results.json
```

## Project Structure

```
├── benchmark.py       # Runs tasks against all 3 models, records tokens & cost
├── analyze.py         # Generates Markdown report from results.json
├── results.json       # Raw benchmark data (generated)
├── RESULTS.md         # Analysis report (generated)
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## Attribution

Inspired by [@Shpigford](https://twitter.com/Shpigford)'s exploration of model cost by task type.
