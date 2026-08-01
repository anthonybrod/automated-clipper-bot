# Hugging Face research — local LLM / judging models (VERBATIM AGENT REPORT)

**Source**: background research agent, 2026-08-01. Scope: structured-JSON /
function-calling models vs. Llama 3.2, local content-moderation/TOS-safety
classifiers, hook-quality text scoring, and real benchmark data on Llama
3.2 alternatives. All figures pulled live from the Hugging Face API and
model card READMEs.

**This is the agent's complete report, word for word, uncondensed.** Saved
per this project's standing rule that raw reports are preserved in full and
never summarized away. Any synthesis/evaluation of this lives separately in
`handoff_2026-08-01_evaluation.md` §5 — do not blend the two.

---

# Hugging Face Research: Local Models for the Twitch Clipper Bot Pipeline

All figures below were pulled live from the Hugging Face API (`huggingface.co/api/models/...`) and model card READMEs, not estimated. Where a claim is self-reported by the model author rather than third-party-verified, I've flagged it explicitly — several sources I checked (SEO-farm "guide" sites) either fabricated numbers or had zero citations, and I've called those out rather than passing them through.

## 1. Structured-JSON / function-calling models (vs. Llama 3.2)

| Model | HF URL | Downloads | Likes | License | What it actually is |
|---|---|---|---|---|---|
| meta-llama/Llama-3.2-3B-Instruct (baseline) | [link](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) | 1,540,941 | 2,381 | llama3.2 (free, MAU cap 700M) | **Native tool-call format is Pythonic** — `[func(arg=val)]` — **not JSON**. Card doesn't mention a JSON mode at all. |
| meta-llama/Llama-3.2-1B-Instruct | [link](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct) | 10,193,506 | 1,549 | llama3.2 | Same tool-format situation, smaller/faster. |
| Qwen/Qwen2.5-7B-Instruct | [link](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | 12,175,037 | 1,450 | **Apache-2.0** | Qwen's own blog claims materially better native JSON/structured output than Llama 3.2 at this tier; corroborated informally by several secondary sources. |
| Qwen/Qwen2.5-3B-Instruct | [link](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct) | 5,754,431 | 544 | **"qwen-research" — non-commercial, research-only** | Same size class as your current model but the license genuinely blocks commercial/monetized use. |
| Qwen/Qwen2.5-1.5B-Instruct | [link](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) | 14,076,532 | 786 | Apache-2.0 | Smaller than Llama 3.2 3B but commercially clean, unlike the 3B Qwen tier. |
| NousResearch/Hermes-2-Pro-Llama-3-8B | [link](https://huggingface.co/NousResearch/Hermes-2-Pro-Llama-3-8B) | 3,566 | 455 | llama3 | Purpose-trained "Function Calling and JSON Mode" dataset. Self-reported (Fireworks.AI-partnered eval): **90% function-calling, 84% JSON-mode accuracy.** Uses `<tools>`/`<tool_call>` chat template. |
| **NousResearch/Hermes-3-Llama-3.2-3B** | [link](https://huggingface.co/NousResearch/Hermes-3-Llama-3.2-3B) | 4,531 | 182 | llama3 | **Same base weights/size as your current Llama 3.2 3B**, full-parameter fine-tuned by Nous for function calling + strict JSON-schema output. Not in the official Ollama library — needs manual GGUF import via `bartowski/Hermes-3-Llama-3.2-3B-GGUF` + a Modelfile. The only other Ollama-listed variant is a community "abliterated" (safety-stripped) build — avoid that one. |
| Salesforce/xLAM-2-3b-fc-r | [link](https://huggingface.co/Salesforce/xLAM-2-3b-fc-r) | 814 | 16 | **CC-BY-NC-4.0, "research purposes only"** | Built on Qwen2.5; claims SOTA BFCL v3, beating GPT-4o/Claude 3.5 (self-reported, unverified by me on the live leaderboard). GGUF exists for Ollama. **License blocks commercial use — hard skip for a monetized channel.** |
| Salesforce/Llama-xLAM-2-8b-fc-r | [link](https://huggingface.co/Salesforce/Llama-xLAM-2-8b-fc-r) | 20,609 | 64 | CC-BY-NC-4.0 | Same non-commercial restriction. |
| microsoft/Phi-3.5-mini-instruct | [link](https://huggingface.co/microsoft/Phi-3.5-mini-instruct) | 1,222,803 | 999 | **MIT** | 3.8B, permissively licensed, no JSON-specific claims verified. |

**Verified-vs-fabricated check:** the one quantitative "Llama 3.2 3B JSON parse rate" figure I could source cites Llama 3.2 3B at only **47.8–56.5%** JSON parse rate (56.5% at Q8_0) and 52.2% schema compliance, vs. a stated "regression from Llama 3.1 8B" — but this comes from a single site, **ascentcore.com** (dated 2026-04-01), with no third-party citations or replication I could find. Treat as one data point, not proof. I could **not** get real numbers off the live Berkeley Function-Calling Leaderboard (gorilla.cs.berkeley.edu/leaderboard.html) for any of these small models — the current default view is dominated by large frontier models (GLM-4.5 at 0.778, Qwen3-235B variants, etc.); none of Llama 3.2/Qwen2.5/Hermes/xLAM appear in what's rendered, so I'm not going to claim a specific rank for them there.

**The more load-bearing fact than any model swap:** several independent sources agree Ollama's `format: json` (grammar/schema-constrained decoding) forces syntactically valid JSON at the token level regardless of which model is behind it — this is likely a bigger lever than swapping Llama 3.2 for something else, and worth checking whether your Ollama calls already use it before adding model complexity.

## 2. Content moderation / TOS-safety classifiers (local Fail-Closed implementation)

| Model | HF URL | Downloads | Likes | License | What it actually does |
|---|---|---|---|---|---|
| **meta-llama/Llama-Guard-3-1B** | [link](https://huggingface.co/meta-llama/Llama-Guard-3-1B) | 59,858 | 111 | llama3.2 | Generative safety classifier (not a plain text-classifier — outputs "safe"/"unsafe" + violated category as text). 13 harm categories S1–S13 (violent crime, sex crimes, CSAE, hate, self-harm, sexual content, elections, etc.). Same size class as your current Llama 3.2 1B/3B. **Pullable directly: `ollama pull llama-guard3:1b`** — first-party Ollama support confirmed. |
| meta-llama/Llama-Guard-3-8B | [link](https://huggingface.co/meta-llama/Llama-Guard-3-8B) | 137,070 | 312 | llama3.1 | Larger/more accurate variant, same category taxonomy, `ollama pull llama-guard3` (8B default). |
| meta-llama/Llama-Prompt-Guard-2-86M | [link](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M) | 98,656 | 163 | "other" | Tiny 86M jailbreak/prompt-injection detector — different job (protects your pipeline from injected text in scraped chat/clip transcripts), not a content-safety judge. Tangential, not core. |
| unitary/toxic-bert (Detoxify) | [link](https://huggingface.co/unitary/toxic-bert) | 196,138 | 227 | Apache-2.0 | Real multi-label classifier (not generative): toxic/severe_toxic/obscene/threat/insult/identity_hate, trained on Jigsaw Wikipedia comments. **Card itself warns**: "if words associated with swearing... are present, it will likely be classified as toxic, regardless of tone" — a real risk for Twitch trash-talk/banter getting over-flagged. |
| eliasalbouzidi/distilbert-nsfw-text-classifier | [link](https://huggingface.co/eliasalbouzidi/distilbert-nsfw-text-classifier) | 7,178 | 23 | Apache-2.0 | Binary safe/nsfw, 190K training examples, self-reported 98% accuracy / 0.974 F1 (on their own eval set, not independently verified). Low real-world adoption despite the good stats. |
| KoalaAI/Text-Moderation | [link](https://huggingface.co/KoalaAI/Text-Moderation) | 40,738 | 94 | CodeML OpenRAIL-M 0.1 (commercial use OK, with restrictions) | DeBERTa-v3, 9 categories (sexual, hate, violence, harassment, self-harm, sexual-minors, hate-threat, graphic-violence). **Self-disclosed weak spot**: overall validation accuracy only 74.9%, and Macro F1 just **0.326 on minority/rare categories** — i.e. weakest exactly on the severe categories (self-harm, sexual-minors) that matter most for TOS. Worth using only inside a fail-closed wrapper, not standalone. |
| Falconsai/offensive_speech_detection | [link](https://huggingface.co/Falconsai/offensive_speech_detection) | 98 | 9 | Apache-2.0 | Essentially unused (98 downloads total) — skip. |
| cardiffnlp/twitter-roberta-base-hate-latest | [link](https://huggingface.co/cardiffnlp/twitter-roberta-base-hate-latest) | 4,309 | 20 | cc-by-4.0 | Hate-speech-specific, trained on tweets (register-matched to chat/stream text), modest adoption. |

**Standout finding:** Llama-Guard-3-1B is the clean fit — same weight class as what you already run, first-party Ollama-pullable, purpose-built by Meta specifically as an input/output safety gate sitting in front of/behind an LLM, and its 13-category taxonomy maps directly onto a TOS-blur check. It slots into the already-adopted Fail-Closed Protocol as a real, free, local second opinion instead of relying solely on cloud-LLM judgment.

## 3. "Hook quality" / engagement scoring for titles/captions

**No purpose-built engagement/virality scorer exists on Hugging Face** — I searched directly and confirmed this is a genuine gap, not a case of me missing something.

Clickbait detectors do exist, but solve the **opposite** problem — they're trained to flag/penalize clickbait for news-integrity purposes, not to score positive hook effectiveness — and adoption is negligible: [valurank/distilroberta-clickbait](https://huggingface.co/valurank/distilroberta-clickbait) (539 downloads, 1 like, last updated 2022) and [Stremie/roberta-base-clickbait](https://huggingface.co/Stremie/roberta-base-clickbait) (11 downloads, 2 likes). These are effectively unused and not worth building on.

The closest usable proxies, with real traction:

| Model | HF URL | Downloads | Likes | License | Fit |
|---|---|---|---|---|---|
| cardiffnlp/twitter-roberta-base-sentiment-latest | [link](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest) | 2,637,762 | 822 | cc-by-4.0 | 3-way pos/neu/neg, trained on ~124M tweets — register matches chat/captions. |
| j-hartmann/emotion-english-distilroberta-base | [link](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base) | 553,603 | 503 | not stated on card | 7-way emotion (anger/disgust/fear/joy/neutral/sadness/**surprise**) — surprise/anger intensity is a more defensible proxy for "hook" than plain polarity, since rage/shock content is often the most engaging Twitch material. |
| distilbert-base-uncased-finetuned-sst-2-english | [link](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english) | 3,644,105 | 934 | Apache-2.0 | Binary pos/neg, trained on movie reviews — weakest register match of the three. |

**Be honest about the mismatch here**: none of these measure "hook quality" or engagement-worthiness — they measure sentiment/emotion polarity of the text itself. A highly negative or fear/surprise-coded caption isn't necessarily unengaging on Twitch (the opposite, often). None of these models were validated against real view/watch-time/engagement data, so treat any of them as a cheap pre-filter signal at best, not a real hook-quality judge — that job likely still needs the LLM (or a human-labeled fine-tune you'd have to build yourself, which doesn't exist off-the-shelf).

## 4. Verdict on Llama 3.2 vs. alternatives

Llama 3.2 3B is still enormously adopted (1.5M+ downloads on the gated repo alone) and remains the easiest path (`ollama pull llama3.2`, first-party). But for the *specific* narrow claim "reliably returns valid JSON with timestamps/scores," it is not obviously the strongest choice:

- Its own model card never mentions a JSON mode; its trained native tool-call format is Pythonic list syntax, not JSON.
- The one quantitative JSON-reliability figure found (single-source, unverified pedigree) put it at 47.8–56.5% JSON parse rate — a real, if uncorroborated, weak spot.
- Qwen2.5-7B-Instruct (Apache-2.0, 12M+ downloads) is the most credibly-reported upgrade for structured output, at the cost of a heavier model.
- NousResearch/Hermes-3-Llama-3.2-3B is the lowest-risk complement: **identical base weights and size to what you already run**, plus Nous's dedicated JSON-mode/function-calling training (self-reported 84–90% on the -2-Pro sibling), same llama3 license family (no new commercial restriction) — the tradeoff is it's not in the official Ollama library, so it needs a manual GGUF + Modelfile import rather than a one-line pull.
- Salesforce xLAM and Qwen2.5-3B are the ones to actually skip for this project specifically — both carry non-commercial/research-only licenses (CC-BY-NC-4.0 and "qwen-research" respectively) that don't fit a monetized channel, regardless of how good their self-reported benchmark numbers look.

If the team wants one concrete next step: try Ollama's `format: json` constrained decoding with the existing Llama 3.2 3B before swapping models at all — multiple independent sources agree this is what actually fixes JSON parse-rate problems in practice, more reliably than picking a different base model.
