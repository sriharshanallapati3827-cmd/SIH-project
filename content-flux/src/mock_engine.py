from typing import List
from src.schemas import InputData, GeneratedOutput


def generate_mock_results(input_data: InputData) -> List[GeneratedOutput]:
    """
    Stub engine returning markdown-formatted GeneratedOutput objects.
    In Phase 4 this will be replaced by real LLM/pipeline calls.
    """
    return [
        GeneratedOutput(
            deliverable_type="Executive Summary",
            content="""## Q3 Strategic Performance Brief

**Overall Performance:** Exceeded benchmarks by **+18.4%** across all primary KPIs.

### Key Metrics

| Metric | Value | Status |
|---|---|---|
| Capital Deployed | $3.8M | ✅ Within MPRA Level 2 |
| Briefing Latency Reduction | 32% | ✅ Below threshold |
| Model Validation Datasets | 52 | ✅ Confirmed |
| Tokens Generated | 1,812 | ✅ Nominal |

### Strategic Findings

- **Autonomous pipeline throughput** scaled without proportional headcount increases, validating the multi-agent routing architecture.
- **Zero data retention** confirmed across all synthesis passes; compliance posture maintained.
- **Parallel execution** across 3 model instances reduced total wall-clock generation time to under 4 seconds per deliverable.

### Recommendation

> Accelerate multi-channel rollout in Q4, prioritising sovereign synthesis integration
> across enterprise evaluation stacks. Board presentation package ready upon request.

**Next Steps:** Schedule Q4 roadmap review. Full technical appendix available internally.""",
        ),
        GeneratedOutput(
            deliverable_type="LinkedIn Thought Leadership Post",
            content="""**The modern bottleneck isn’t intelligence — it’s data lineage and downstream execution speed.**

Our Q4 synthesis outputs demonstrate how three foundational operational shifts create measurable gains in minutes through deterministic semantic safeguards:

✅ **Autonomous Validation Logic**
Human-in-the-loop review latency drops to 8 minutes through deterministic semantic safeguards.

✅ **Resource Re-Allocation at Scale**
Engineering teams shifted 32% of operational headcount toward high-leverage agent tasks, freeing 3.4M engineering-hours annually.

✅ **Knowledge Infrastructure Hardening**
Enterprise workloads now demand strict zero-retention parameters — not open playground endpoints.

---

If your AI stack isn’t thinking in *systems*, you’re paying a compounding tax on technical agility.

*What does your validation latency look like this quarter?*

—

#AIStrategy #DataIntelligence #EnterpriseAI #OperationalExcellence #FutureOfWork""",
        ),
        GeneratedOutput(
            deliverable_type="Executive Video Script",
            content="""## 60-Second Video Script: Enterprise AI Pipeline

---

### [0:00–0:15] — Hook

> *“Your enterprise AI initiatives hit raw model capacity, not enterprise latency.*
> *When your data pipelines run in silos, your transformation stalls.”*

**Director’s note:** Open on dark data-flow visualization. Slow zoom in. No music yet.

---

### [0:15–0:40] — Solution

> *“By integrating sovereign synthesis directly into our evaluation stack,*
> *we reduced multi-team briefing latency from 48 hours to under ten minutes.*
> *That’s 3.4 million engineering resources re-allocated to multiplied capabilities.”*

**Director’s note:** Cut to split-screen: legacy workflow (red) vs. new pipeline (blue glow). Subtle motion-graphic metrics animating up.

---

### [0:40–0:60] — CTA

> *“Stop building isolated drafts. Deploy continuous intelligence.*
> *Explore our verified Q3 synthesized benchmarks at synth.internal/review.”*

**Director’s note:** Logo lock-up. URL on screen. Fade to black.

---

**Production Specs:**
- **Format:** 16:9 landscape, 4K master
- **Tone:** Confident, direct, enterprise-authoritative
- **Music:** Minimal electronic underscore, fade in at 0:10
- **B-Roll:** Data pipeline visualization, team collaboration, terminal output footage""",
        ),
        GeneratedOutput(
            deliverable_type="Strategic Advisory Memo",
            content="""## Strategic Advisory Memo
**Prepared for:** Executive Leadership (C-Suite)
**Classification:** Internal — Restricted Distribution
**Date:** Q3 Review Cycle

---

### Executive Context

Enterprise AI transformation cycles can be shortened by 61% through continuous deterministic pipelines. By automating service drafting with verified synthesis transformation protocols, experiments shift from anecdotal to systemic; cost-managing relations become multi-semantic compression.

### Operational Milestones

1. **Zero-Optic Multi-Channel Output Alignment** — `IN PROGRESS (Q4)`
2. **Multi-Channel Submitted Remedies** — `IN REVIEW`
3. **Plasma Bonus: Robal Synthetic Mediation** — `QUEUED`

### Risk Assessment

| Risk Category | Level | Mitigation |
|---|---|---|
| Data Sovereignty | Low | Zero-retention architecture confirmed |
| Model Drift | Medium | Deterministic evaluation harness active |
| Latency SLA | Low | Sub-4s per deliverable achieved |

### Recommended Actions

- **Immediate:** Ratify Q4 rollout plan at next board session.
- **30-day:** Onboard 2 additional enterprise evaluation clusters.
- **90-day:** Complete cross-functional synthesis audit across all delivery teams.

*This memo was synthesized via the Content Flux autonomous pipeline and is pending human review before external distribution.*""",
        ),
    ]
