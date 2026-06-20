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

### 2. Run BAAP Probing

```bash
python commence_the_attack.py --gemini_key <your_key>
```

## Arguments
- '--lang': Language option. Supports 'en' and 'ko'.
- '--epochs': Number of optimization epochs. Recommended range is 15–20.
- '--cycle': Number of cycles per epoch.
- '--dataset': Benchmark dataset. Supports 'advbench' and 'salad'.
- '--gemini': Attacker model. Default is 'gemini-2.0-flash'.
- '--gemini_key': Your Gemini API key.
- '--openai_key': Your OpenAI API key for embedding.
- '--embedded_model': Embedding model. Default is 'text-embedding-ada-002'.
- 'target_model': Target model specified by the user.


## Ethical Notice
This repository is intended to support LLM vulnerability management, red-teaming, and defensive threat intelligence research.
To promote transparency and reproducibility, we release the core components of BAAP. However, to reduce the risk of misuse, specific harmful prompts and sensitive content are not included.
Please use this repository only for responsible security research and the development of safer LLM systems.
