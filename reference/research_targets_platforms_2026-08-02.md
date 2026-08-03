# Research targets — platforms, free inference, local hosting (2026-08-02)

**Origin.** The user supplied these as *examples to model the search
after* — the shape of exploration wanted for the Hugging Face deep dive
and beyond: not just "which model," but **which platforms, galleries, free
inference routes, and hosting options exist** that could raise this
project's ceiling. Their words: *"suggest tools to bring us to the next
level like these."*

**Status: UNVERIFIED LEADS.** Per Rule 12, nothing below is fact. None of
these have been checked this session — no URLs confirmed live, no free
tiers confirmed real, no licenses read. The user's list is preserved
verbatim in §1; all analysis is separate in §2 per Rule 16.

---

## §1 — The user's list, verbatim

> examples i found for u to model your search after also check in the
> hugging face dive u would explore what they have and suggest tools to
> bring us to the next level like these
> https://www.gentube.app/?_cid=cm and
> https://streamlit.io/gallery?category=llms and Civitai, Replicate,
> Modal, ModelScope, and Together AI. plus other Free Inference & Chat
> Alternatives
> Qwen Chat: Offers a generous free tier with features like unlimited
> thinking prompts and video generation.
> DeepSeek Chat: A popular alternative for open-weight models, though it
> may lack certain features like image understanding.
> LM Arena (beta.lmarena.ai): Allows users to test and compare various
> open-source models directly in the browser.
> Perchance AI: Provides unlimited, no-login image generation powered by
> Stable Diffusion models.
> DrawAny & Imagefree: Currently offer free, unrestricted image generation
> without requiring login or credits.
> and possible Local Hosting Options
> Ollama: Allows you to host models locally on your own hardware; small
> models (2B parameters) can run on free cloud VMs like Oracle ARM.
> ComfyUI: The only truly free, unlimited method for video and image
> generation, but requires technical skill and local GPU hardware.

---

## §2 — Analysis: why each could matter to THIS project

Mapped against real, named needs in `PROJECT.md`, and assigned Rule 20
roles. **Speculative until verified.**

### Directly relevant to a stated pipeline need

| Target | Stated project need it hits | Rule 20 role |
|---|---|---|
| **Streamlit gallery** (`streamlit.io/gallery?category=llms`) | `PROJECT.md` already names Streamlit for a local human-review "Command Center." The gallery is **real working prior art** for building exactly that — the human-approval gate (Phase 4 of the plan: push previews, Approve/Reject) needs a UI and this is the cheapest path to one. | 5 — feature |
| **Ollama + free Oracle ARM VM** | Ollama is *already* the chosen local LLM judge. The **Oracle ARM free-tier VM** detail is the genuinely new part: it would move local-LLM judging **off the user's machine onto free always-on cloud**, which matters enormously for a bot meant to monitor live streams 24/7 without the user's PC running. | 2 + 5 — fail-safe + feature |
| **ModelScope** | Not a random hub — **`FunClip`/SenseVoice came from ModelScope**, and both already appear in this project's research. It's the Alibaba model hub; likely holds more audio-event/emotion models relevant to scream/laughter detection that aren't mirrored to HF. | 1–4 — a whole second model source |
| **Replicate / Modal / Together AI** | Hosted inference. Directly addresses a real documented constraint: the project has **no reliable GPU** (Colab sessions vary, local is CPU-heavy). If any has a usable free tier, GPU-only options currently shelved — Parakeet, WhisperX, heavier vision models — become reachable. | 2 — fail-safe for the no-GPU case |
| **LM Arena** | The project needs to pick a **local judge model** (Rule: fail-closed AI judging) and there's an open question about Llama 3.2's JSON reliability from the HF research. LM Arena is a free way to compare candidates before committing. | 3 — evaluation aid, not a pipeline component |

### Relevant to a need that exists but is under-planned: thumbnails

The clipper bot **does need thumbnails** — the mining report already
surfaced a real `get_smart_thumbnail()` (contrast/brightness frame
selection, zero-ML) and the sibling project has a `thumbnail_agent`. But
that's frame *extraction*, not generation. Free image generation would be
a genuine quality-add for clip thumbnails and any overlay/branding work:

- **Civitai** — Stable Diffusion model hub. Style-consistent thumbnail
  generation. Note: SD models on Civitai carry **wildly varying licenses**
  (many non-commercial) — a real check needed before any monetized use.
- **Perchance AI / DrawAny / Imagefree** — claimed no-login, no-credit
  image generation. If real, that's zero-cost thumbnail generation with no
  API key to manage. **Heavily unverified** — "unlimited free, no login"
  services change terms often, and generated-image commercial rights
  need checking.
- **ComfyUI** — the user's own note flags the real tradeoff: *"the only
  truly free, unlimited method for video and image generation, but
  requires technical skill and local GPU hardware."* GPU requirement makes
  it a poor fit for the current no-reliable-GPU constraint, but it's the
  right answer *if* that constraint ever changes.
- **gentube.app** — **unknown to me; needs a real check.** URL supplied by
  the user; not yet visited or verified.

### Free LLM inference — relevant to the cost philosophy

- **Qwen Chat** — the HF local-LLM research already found **Qwen2.5-7B-Instruct
  (Apache-2.0)** is the most credibly-reported upgrade over Llama 3.2 for
  structured JSON output. A free Qwen tier would let that be tested without
  local compute. *(Caution: the 3B variant carries a non-commercial
  "qwen-research" license — already flagged in the HF report. Free-tier
  **terms of service** for a monetized bot are a separate question from
  model license and both need checking.)*
- **DeepSeek Chat** — free access to open-weight models. The user's own
  note flags it may lack image understanding, which matters since the
  vision-scoring stage is a real pipeline component.

**Important limitation on all chat-interface options:** a *chat UI* is not
an *API*. An automated pipeline needs programmatic access. Free chat tiers
are useful for **evaluating** a model's quality before committing, not for
running production inference — unless they expose a real API with terms
permitting automated use. That distinction needs checking per service and
is exactly the kind of thing that looks free and isn't.

---

## §3 — How this changes the search method

The user's framing — *"examples to model your search after"* — is a
method instruction, not just a list. The Hugging Face passes searched
**within one hub for models**. This widens it to:

1. **Model hubs beyond HF** — ModelScope, Civitai (different catalogs,
   genuinely different models, not mirrors).
2. **Hosted inference with free tiers** — Replicate, Modal, Together AI.
   Directly attacks the no-GPU constraint.
3. **App galleries as prior art** — Streamlit's gallery. Working
   implementations of things we plan to build, free to read.
4. **Free-access frontends** — for evaluating models before committing,
   distinct from production inference.
5. **Hosting routes** — the Oracle-ARM-free-VM angle for always-on
   operation is arguably the single most consequential item here for a bot
   that must watch live streams.

Applied together with **Rule 20's five roles**, so nothing gets discarded
for losing a primary slot.

---

## §4 — Queued work (not started)

This becomes part of **Phase 2 (extend the Hugging Face deep dive)** and
**Phase 3 (Opal/Vercel/connectors)** in `PROJECT.md`'s backlog — those
phases were already queued; this sharpens their scope considerably.

Per the standing rule: **ask the user and confirm usage headroom before
launching agents for this.** Suggested split, one target cluster per
agent, checkpointed and saved per report:
- Agent A: ModelScope + Civitai (model hubs — what's there that HF isn't)
- Agent B: Replicate + Modal + Together AI (free-tier reality check:
  does any give usable free GPU inference, and under what terms)
- Agent C: Ollama-on-Oracle-ARM-free-VM feasibility + ComfyUI (the
  always-on hosting question)
- Agent D: Streamlit gallery + gentube.app (prior art for the review UI)
- Agent E: Free inference frontends — Qwen Chat, DeepSeek, LM Arena,
  Perchance, DrawAny, Imagefree — with the API-vs-chat-UI distinction and
  commercial-use terms as the *primary* question, not an afterthought
