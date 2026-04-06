# Benchmark Results

## Cost per Task (USD)

| Task | Haiku 4.5 | Sonnet 4.6 | Opus 4.6 | Best Value |
|------|-----------|------------|----------|------------|
| classification | $0.000059 | $0.0002 | $0.0003 | Haiku 4.5 |
| entity_extraction | $0.0002 | $0.0007 | $0.0012 | Haiku 4.5 |
| summarization | $0.0004 | $0.0015 | $0.0025 | Haiku 4.5 |
| qa_simple | $0.000039 | $0.0001 | $0.0002 | Haiku 4.5 |
| qa_complex | $0.0005 | $0.0012 | $0.0024 | Haiku 4.5 |
| code_gen_simple | $0.0004 | $0.0013 | $0.0021 | Haiku 4.5 |
| code_review | $0.0015 | $0.0044 | $0.0073 | Haiku 4.5 |
| creative_writing | $0.0002 | $0.0009 | $0.0009 | Haiku 4.5 |
| data_analysis | $0.0013 | $0.0040 | $0.0067 | Haiku 4.5 |
| chat_reply | $0.0002 | $0.0007 | $0.0011 | Haiku 4.5 |
| **TOTAL** | $0.0048 | $0.0150 | $0.0246 | — |

## Token Usage per Task

| Task | Model | Input Tokens | Output Tokens |
|------|-------|-------------|---------------|
| classification | haiku-4.5 | 34 | 5 |
| classification | sonnet-4.6 | 34 | 5 |
| classification | opus-4.6 | 34 | 5 |
| entity_extraction | haiku-4.5 | 36 | 39 |
| entity_extraction | sonnet-4.6 | 36 | 39 |
| entity_extraction | opus-4.6 | 36 | 39 |
| summarization | haiku-4.5 | 172 | 40 |
| summarization | sonnet-4.6 | 172 | 64 |
| summarization | opus-4.6 | 172 | 64 |
| qa_simple | haiku-4.5 | 19 | 4 |
| qa_simple | sonnet-4.6 | 19 | 4 |
| qa_simple | opus-4.6 | 19 | 4 |
| qa_complex | haiku-4.5 | 39 | 99 |
| qa_complex | sonnet-4.6 | 39 | 75 |
| qa_complex | opus-4.6 | 39 | 90 |
| code_gen_simple | haiku-4.5 | 28 | 83 |
| code_gen_simple | sonnet-4.6 | 28 | 79 |
| code_gen_simple | opus-4.6 | 28 | 79 |
| code_review | haiku-4.5 | 181 | 256 |
| code_review | sonnet-4.6 | 181 | 256 |
| code_review | opus-4.6 | 181 | 256 |
| creative_writing | haiku-4.5 | 15 | 27 |
| creative_writing | sonnet-4.6 | 15 | 60 |
| creative_writing | opus-4.6 | 15 | 31 |
| data_analysis | haiku-4.5 | 61 | 256 |
| data_analysis | sonnet-4.6 | 61 | 256 |
| data_analysis | opus-4.6 | 61 | 256 |
| chat_reply | haiku-4.5 | 13 | 32 |
| chat_reply | sonnet-4.6 | 13 | 43 |
| chat_reply | opus-4.6 | 13 | 40 |

## Key Insights

- **Sonnet 4.6 costs 3.1x** more than Haiku 4.5 across all tasks
- **Opus 4.6 costs 5.1x** more than Haiku 4.5 across all tasks
- **Cheapest task on Haiku:** qa_simple at $0.000039
- **Most expensive task on Opus:** code_review at $0.0073
- **Total cost for all 10 tasks on Haiku:** $0.0048
