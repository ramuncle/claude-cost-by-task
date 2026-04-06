#!/usr/bin/env python3
"""Benchmark Claude API cost per task type across Haiku 4.5, Sonnet 4.6, and Opus 4.6."""

import argparse
import json
import time
from datetime import datetime, timezone

import anthropic

MODELS = {
    "haiku-4.5": {
        "id": "claude-haiku-4-5",
        "input_cost_per_mtok": 1.00,
        "output_cost_per_mtok": 5.00,
    },
    "sonnet-4.6": {
        "id": "claude-sonnet-4-6",
        "input_cost_per_mtok": 3.00,
        "output_cost_per_mtok": 15.00,
    },
    "opus-4.6": {
        "id": "claude-opus-4-6",
        "input_cost_per_mtok": 5.00,
        "output_cost_per_mtok": 25.00,
    },
}

TASKS = {
    "classification": {
        "prompt": "Classify the following review as positive or negative. Reply with just the label.\n\nReview: The pizza was late but tasty.",
        "max_tokens": 16,
    },
    "entity_extraction": {
        "prompt": "Extract the name, role, and company from the following text. Return JSON.\n\nText: Sarah Chen, CTO at DataFlow Inc.",
        "max_tokens": 64,
    },
    "summarization": {
        "prompt": (
            "Summarize the following paragraph in one sentence.\n\n"
            "Cloud computing has transformed how businesses operate by providing on-demand "
            "access to computing resources over the internet. Instead of maintaining expensive "
            "physical servers, companies can now rent virtual machines, storage, and networking "
            "capacity from providers like AWS, Google Cloud, and Azure. This shift has enabled "
            "startups to launch with minimal upfront infrastructure costs and has allowed "
            "enterprises to scale their operations dynamically based on demand. The pay-as-you-go "
            "model means organizations only pay for what they use, reducing waste and improving "
            "cost efficiency. However, cloud adoption also introduces challenges around data "
            "security, vendor lock-in, and managing complex multi-cloud environments. Despite "
            "these concerns, the global cloud market continues to grow rapidly, with spending "
            "expected to exceed $1 trillion by 2028."
        ),
        "max_tokens": 64,
    },
    "qa_simple": {
        "prompt": "What is the capital of Japan? Answer in one word.",
        "max_tokens": 16,
    },
    "qa_complex": {
        "prompt": (
            "A farmer has 17 sheep. All but 9 die. How many sheep are left? "
            "Think step by step, then give the final answer."
        ),
        "max_tokens": 128,
    },
    "code_gen_simple": {
        "prompt": "Write a Python function to compute the nth Fibonacci number iteratively. Just the function, no explanation.",
        "max_tokens": 256,
    },
    "code_review": {
        "prompt": (
            "Review the following Python code for bugs and suggest fixes.\n\n"
            "```python\n"
            "def merge_sorted(a, b):\n"
            "    result = []\n"
            "    i = j = 0\n"
            "    while i < len(a) and j < len(b):\n"
            "        if a[i] <= b[j]:\n"
            "            result.append(a[i])\n"
            "            i += 1\n"
            "        else:\n"
            "            result.append(b[j])\n"
            "            j += 1\n"
            "    # BUG: remaining elements not appended\n"
            "    return result\n"
            "\n"
            "def find_max(lst):\n"
            "    max_val = 0  # BUG: fails for negative numbers\n"
            "    for item in lst:\n"
            "        if item > max_val:\n"
            "            max_val = item\n"
            "    return max_val\n"
            "```"
        ),
        "max_tokens": 256,
    },
    "creative_writing": {
        "prompt": "Write a haiku about software debugging.",
        "max_tokens": 64,
    },
    "data_analysis": {
        "prompt": (
            "Given the following CSV data, describe the key trends you observe.\n\n"
            "month,revenue,users\n"
            "Jan,12000,150\n"
            "Feb,14500,180\n"
            "Mar,13200,170\n"
            "Apr,17800,220\n"
            "May,21000,290"
        ),
        "max_tokens": 256,
    },
    "chat_reply": {
        "prompt": "How are you doing today?",
        "max_tokens": 128,
    },
}


def compute_cost(input_tokens: int, output_tokens: int, model_key: str) -> float:
    """Compute cost in USD given token counts and model pricing."""
    pricing = MODELS[model_key]
    input_cost = (input_tokens / 1_000_000) * pricing["input_cost_per_mtok"]
    output_cost = (output_tokens / 1_000_000) * pricing["output_cost_per_mtok"]
    return input_cost + output_cost


def run_task(client: anthropic.Anthropic, model_id: str, prompt: str, max_tokens: int):
    """Send a single task to the API and return the response."""
    response = client.messages.create(
        model=model_id,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return response


def run_benchmark(dry_run: bool = False, output_file: str = "results.json"):
    """Run the full benchmark suite."""
    results = {
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "dry_run": dry_run,
            "models": {k: v["id"] for k, v in MODELS.items()},
            "pricing": {
                k: {
                    "input_per_mtok": v["input_cost_per_mtok"],
                    "output_per_mtok": v["output_cost_per_mtok"],
                }
                for k, v in MODELS.items()
            },
        },
        "tasks": {},
    }

    client = None if dry_run else anthropic.Anthropic()

    for task_name, task_config in TASKS.items():
        print(f"\n{'='*60}")
        print(f"Task: {task_name}")
        print(f"{'='*60}")
        results["tasks"][task_name] = {}

        for model_key, model_info in MODELS.items():
            print(f"  Model: {model_key} ({model_info['id']})")

            if dry_run:
                print(f"    [DRY RUN] Would send: {task_config['prompt'][:80]}...")
                print(f"    [DRY RUN] max_tokens={task_config['max_tokens']}")
                results["tasks"][task_name][model_key] = {
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost_usd": 0.0,
                    "dry_run": True,
                }
                continue

            start = time.time()
            response = run_task(
                client, model_info["id"], task_config["prompt"], task_config["max_tokens"]
            )
            elapsed = time.time() - start

            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            cost = compute_cost(input_tokens, output_tokens, model_key)

            results["tasks"][task_name][model_key] = {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost_usd": cost,
                "latency_s": round(elapsed, 2),
                "response_preview": response.content[0].text[:100],
            }

            print(f"    Tokens: {input_tokens} in / {output_tokens} out")
            print(f"    Cost: ${cost:.6f}")
            print(f"    Latency: {elapsed:.2f}s")

            # Brief pause to avoid rate limiting
            time.sleep(0.5)

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {output_file}")
    return results


def main():
    parser = argparse.ArgumentParser(description="Benchmark Claude API cost by task type")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be sent without making API calls",
    )
    parser.add_argument(
        "--output",
        default="results.json",
        help="Output JSON file (default: results.json)",
    )
    args = parser.parse_args()
    run_benchmark(dry_run=args.dry_run, output_file=args.output)


if __name__ == "__main__":
    main()
