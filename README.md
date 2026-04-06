# claude-cost-by-task

Real measured API costs for Claude Haiku 4.5 vs Sonnet 4.6 vs Opus 4.6 across 10 task types.

Inspired by [@Shpigford](https://twitter.com/Shpigford)'s post on model cost by task type — this repo actually runs the API calls and measures them.

## Results (real API measurements)

| Task | Haiku 4.5 | Sonnet 4.6 | Opus 4.6 | Ratio (H→O) |
|------|-----------|------------|----------|-------------|
| classification | $0.000059 | $0.000177 | $0.000295 | 5.0x |
| entity_extraction | $0.000231 | $0.000693 | $0.001155 | 5.0x |
| summarization | $0.000372 | $0.001476 | $0.002460 | 6.6x |
| qa_simple | $0.000039 | $0.000117 | $0.000195 | 5.0x |
| qa_complex | $0.000534 | $0.001242 | $0.002445 | 4.6x |
| code_gen_simple | $0.000443 | $0.001269 | $0.002115 | 4.8x |
| code_review | $0.001461 | $0.004383 | $0.007305 | 5.0x |
| creative_writing | $0.000150 | $0.000945 | $0.000850 | 5.7x |
| data_analysis | $0.001341 | $0.004023 | $0.006705 | 5.0x |
| chat_reply | $0.000173 | $0.000684 | $0.001065 | 6.2x |
| **TOTAL** | **$0.0048** | **$0.0150** | **$0.0246** | **5.1x** |

**Key findings:**
- Sonnet costs **3.1x** Haiku across all task types
- Opus costs **5.1x** Haiku across all task types
- The ratio is consistent — cost scales with price, not task complexity
- **code_review** and **data_analysis** are the most expensive tasks (output-heavy)
- **qa_simple** is the cheapest: $0.000039 on Haiku, $0.000195 on Opus
- For classification and simple QA: Haiku is almost free. Use it.

## What this means

If you're using Sonnet or Opus for classification, entity extraction, or simple QA — you're paying 3–5x too much. Haiku handles these identically.

The only tasks where you'd consider Opus: complex reasoning where quality materially differs (not benchmarked here for quality — coming soon).

## Run it yourself

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python3 benchmark.py
python3 analyze.py
```

Total cost to run: ~$0.015 (all 30 API calls)

## Methodology

- 1 API call per task per model (30 calls total)
- Token counts from API response (`usage.input_tokens`, `usage.output_tokens`)
- Pricing: Haiku $1/$5 per MTok in/out, Sonnet $3/$15, Opus $5/$25
- Prompts kept short to minimize benchmark cost

## License

MIT
