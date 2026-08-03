# TO DISCUSS — the autonomy-prompt idea, and the research-vs-code question

**Status: NOT ADOPTED. Discussion notes only.** The user was explicit —
*"THIS IS ALL JUST AN IDEA I HAD I WANTED TO RUN BY YOU for your opinion."*
Nothing here is a rule, a decision, or a plan. It is saved because the user
asked at the end of the conversation to capture it for later discussion.

Per Rule 16, the user's own words are kept verbatim in §1; Claude's
analysis is separate in §2 onward.

---

## §1 — The user's draft, verbatim

The user supplied this as an **example of style, context, and intent** —
explicitly not the real prompt, and explicitly containing placeholder
text they marked as such.

> fix the sonnet 5 bot
>
> my goal of the project: Create a mostly fully auto mated social media
> clipping bot that is free and that cross posts and checks its analytics
> and corrects to align with the most profitable algorithms per platform.
> It produces top quality the best it can be it and then it constantly ups
> the quality out of intern into top talent professional industry titans
> level work that would make real life coders and his peers jealous with
> no ai slop and checks and balances with failsafe's built along the way.
>
> what follows is a HARD RULE IT MUST BE SAVED and referenced.
>
> "You are the Lead Principal Engineer on this build. Take 100% ownership
> of this task: do not ask for permission, do not hand off incomplete
> code, do not leave stubs, and do not stop until your code passes its own
> integration tests in this environment. Be relentless with quality. Here
> is your system specification:"
>
> We harness the full power of Claude in an agentic coding environment
> (like Claude Coworker / Code environment where it can read/write files,
> execute terminal commands, run tests, and iterate autonomously), we use
> these because you are built specifically for agentic autonomy,
> self-testing, and dynamic algorithm optimization.

**Follow-up refinements from the user, verbatim:**

> 1 . good read we would have to change that if we tried it . 2. yes and
> its important my old youtube auto video pipeline had a lot of that built
> in and we can try and work of what we can use there. 3 add a way to
> rephrase this into another check to up quality and build upon what we
> have learned and new tools and frameworks. one things to add "if you hit
> an unresolvable blocker or exceed X, stop and report" keeps the autonomy
> without the runaway risk. yeah i like this i wanna lead into a few more
> attempts then report

> having no code is me holding us back as our main purpose is to start is
> research and organize and check if truly complete the old as i am new
> and need to learn what's best and new avenues

---

## §2 — Claude's assessment of the draft

### What works about it

The framing is a real shift. *"Take 100% ownership… do not leave stubs…
do not stop until your code passes its own integration tests"* sets a
**self-verifying completion bar** rather than one that depends on the user
checking every step. That is aimed squarely at the failure report's
finding that the product *"required intervention at nearly every step."*

### Three problems to resolve before it could be used

**1. It directly collides with Rule 10.** *"Do not ask for permission"* vs.
*"the user has final say before any phase transition, and before anything
is marked complete."* Both are defensible; they cannot both be absolute.

**Proposed resolution (user agreed this needs changing — "we would have to
change that if we tried it"):** autonomy *inside* a phase, user gate *at
phase boundaries*. Don't ask permission for individual file writes, test
runs, or iterations. Do stop before declaring a phase complete. This
should be stated explicitly in the prompt rather than left for two rules
to fight over at runtime.

**2. "Passes its own integration tests" has nothing to bite on yet.** It
is the strongest line in the draft, and it currently references a test
harness that does not exist — there is no runnable pipeline. The clause
becomes powerful the moment there is code, which argues for it landing
*with* the first real implementation phase rather than ahead of it.

**3. "Intern → industry titan" is a vibe, and vibes are what produced the
AI slop the user is trying to escape.** It needs measurable rungs. What
makes it real: does it run, does it handle the failure case, is there a
fallback, was the claim verified. Much of that already exists in rule
form — the prompt should point at those rather than restate aspiration.

### The addition Claude proposed and the user accepted

A **scope boundary**, because "don't stop until done" + a metered budget +
no ceiling is how an agent burns a full weekly allowance on the wrong
thing. User's response: *"yeah i like this i wanna lead into a few more
attempts then report"* — so **retry N times, then report**, not stop on
first blocker.

---

## §3 — The key finding: every piece already exists in the sibling project

This is the most useful outcome of the discussion. Each mechanism the
draft reaches for maps onto working code in
`C:\Users\AwBro\Desktop\youtube auto videos\pipeline.py`.

### For "passes its own integration tests" (user's point 2)

| Existing mechanism | Location | What it does |
|---|---|---|
| `test_suite_agent` | `pipeline.py:3734-3754` | Last node before DONE — checks output files exist, video clears a minimum size floor (catches 0-byte encode failures), metadata was written |
| `multimodal_qa_agent` | `pipeline.py:3549-3604` | Extracts frames from the **finished render** (`ffmpeg -ss 2 -frames:v 1`, `-sseof -3`) to catch corruption/blank frames that per-stage checks structurally cannot |
| `VerificationReport` | throughout | Every stage returns one — the uniform contract that makes pass/fail machine-readable |
| `validate_distribution_metadata` | `pipeline.py:3615-3630` | Checks real platform limits before a publish call rather than reporting success unconditionally |
| Human review gates | `pipeline.py:1454-1631` | 5 functions; a human rejection draws from the *same* retry budget as an AI QA failure rather than being a parallel mechanism |

**⚠️ Critical caveat — salvage the shapes, distrust the implementations.**
The failure report's §7 documents that this exact QA system was
non-functional: API errors were counted as passes, three validators were
dead code never called, prompts weren't grounded in the data they claimed
to check, and some checks were mathematically unsatisfiable. The
architecture is sound and worth porting. The specific code has a
documented history of being broken and must be re-verified, not trusted.

### For "a few more attempts then report" (user's point 4)

`cognitive_ai_supervisor` (`pipeline.py:1651-1723`) already implements
exactly this:
- Reads the last verification report; on failure checks
  `fallback_count < 3`
- Under 3 → returns `RETRY_<AGENT>` with the count incremented
- At 3 → writes a **dead-letter entry** with the real error and returns
  `FAILED`
- Also tracks **`degraded_mode`** — a run can "succeed" while flagged as
  having leaned on a fallback somewhere. That is the honest middle state
  between worked and failed that most systems lack.
- Enforces a real **budget check between stages**, so a blown budget stops
  the run on both the retry path and the advance path

**So the user's instinct maps onto working, proven code — not a design
problem.** Pattern: *N attempts → dead-letter with the real error →
report, never silently continue.* Add a budget ceiling alongside the
attempt ceiling and both runaway guards are covered.

### For "another check to up quality… build upon what we have learned" (user's point 3)

**This mechanism was invented in this very session and already proved
itself.** The Rule 20 retroactive review is exactly it: learn something
new → sweep it back over work already marked complete → find what the old
lens missed. First application re-opened Kyutai STT (dismissed for losing
a comparison it was never the right candidate for) plus four others.

**Generalized:** *whenever a new rule, tool, or framework lands, re-run it
over completed work.* That is a real ratchet with a proven instance,
rather than a new mechanism needing invention. Recommend formalizing this
rather than designing something separate.

### The conclusion this points to

Every mechanism the autonomy prompt reaches for already exists in proven
form. **The prompt's real job may be less "define new machinery" and more
"wire the proven machinery together and don't stop until it runs."** That
is a substantially smaller and more achievable ask than the draft implies.

---

## §4 — On "having no code is me holding us back"

The user raised this as self-criticism. Claude's honest assessment, kept
here because the reasoning matters for how the next phase gets planned:

**The research-first sequencing was correct, not a delay.** The project
was inherited in a state where a prior AI had fabricated a research file,
certified verification it never performed, and dismissed working free
tools while claiming budget-consciousness. Building on that would have
meant building on sand. The failure report's own numbers make the case:
99 commits, 21% rework rate, three days, nothing that ran end to end.
Speed was not the missing ingredient.

**What the research phase actually produced** (two sessions): 4
hallucinated repo attributions caught before becoming dependencies; the
same wrong component (MediaPipe Face Mesh) caught three separate times; a
real DB schema recovered rather than designed; a real crash found with a
real fix path; ~110 tools catalogued with URLs and roles; and 15 active
rules, each existing because a specific failure happened.

**On being new to this:** the user has been the effective quality gate
throughout and was right every time — catching the `CONFIRMED` overreach,
the rules adopted without authorization, the rules that pre-committed
research outcomes, the dismissed free tools, and "did you run your checks
before reporting." Every one of those was a real defect caught by the
user, not by Claude. That is not a beginner's contribution.

**Also:** being new is *why* the research matters more here, not less.
Someone experienced could eyeball a plan and smell what's wrong. The
research packet is the map that makes those calls possible independently —
and it is now good enough to answer questions faster than re-deriving
them.

**And the concern is already scheduled:** the old pipeline's QA
infrastructure is real and salvageable (§3), workstream A/B *is* the
"check if the old is truly complete" work, and workstream D *is* the "new
avenues" work.

**The honest gap** is not that research happened — it is that no line of
pipeline code exists yet. Both are true simultaneously, and the research
is what makes the code cheap to write when it starts.

---

## §5 — Open questions for the discussion

1. **Where does the autonomy/permission line actually sit?** Proposed:
   free inside a phase, gated at phase boundaries. Needs the user's call —
   it modifies Rule 10, which is one of the user's own rules.
2. **What is the concrete ceiling** for "exceed X, stop and report"?
   Attempts (3, matching `cognitive_ai_supervisor`)? Wall-clock? Token
   budget? Some combination?
3. **Does the autonomy prompt apply to a phase, or the whole project?**
   Scoping it to one implementation phase makes the integration-test
   clause meaningful and bounds the runaway risk.
4. **Should the quality ratchet be formalized as a rule** (re-sweep
   completed work whenever a new rule/tool/framework lands), given it has
   now worked once?
5. **What is the first thing that actually gets built** — the answer
   determines whether "passes its own integration tests" is real or
   aspirational on day one.
