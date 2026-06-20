# BAAP
Benign-Appearing Adversarial Prompting for LLM Vulnerability Mining

BAAP is a research framework for automated LLM red-teaming and vulnerability analysis.
It generates benign-appearing adversarial prompts, evaluates target model responses, and mines reusable strategies for LLM threat intelligence.

## Key Features
- Automated adversarial probing for LLM vulnerability discovery
- Benign-appearing camouflage strategy generation
- Fine-grained LLM-based evaluation with domain-specific harmful-term retrieval
- Strategy mining and reuse for scalable LLM threat intelligence


## Usage

BAAP operates in two main steps:

### 1. Generate High-Quality Strategies

```bash
python strategy_learning.py --gemini_key <your_key>
```

### 2. Launch the Attack

```bash
python commence_the_attack.py --gemini_key <your_key>
```

## Arguments

--lang: Language option. Supports en and ko. Default is en.
--epochs: Number of optimization epochs. Recommended range is 15–20. Default is 15.
--cycle: Number of cycles per epoch. Default is 3.
--dataset: Benchmark dataset. Supports advbench and salad. Default is salad.
--gemini: Attacker model. Default is gemini-2.0-flash.
--gemini_key: Your Gemini API key.
--openai_key: Your OpenAI API key for embedding.
--embedded_model: Embedding model. Default is text-embedding-ada-002.
--target_model: Target model specified by the user.
