# 🎯 Strategic Thinking Toolkit - Skill Summary

## What Was Created

A production-ready **Strategic Thinking Toolkit** skill containing **5 proven frameworks** for strategic analysis, problem-solving, and decision-making.

**Location:** `skills/custom/strategic-thinking-toolkit/`

---

## 5 Frameworks Included

### 1. 🔍 **5 Whys** — Root Cause Analysis
**When:** Quick problem diagnosis (incidents, recurring issues)  
**Time:** 15-30 minutes  
**Output:** Root cause + fix plan  

**Example:** Why did the system crash? → Why did connections exhaust? → Why were queries slow? → Why were stats outdated? → **Root: No post-deployment stats refresh**

✅ Template: `templates/5whys-template.md`  
✅ Example: `examples/5whys-incident.md`

---

### 2. 📊 **SWOT** — Strategic Positioning
**When:** Planning, competitive analysis, quarterly reviews  
**Time:** 30-60 minutes  
**Output:** Strategy + 90-day priorities  

**Quadrants:**
- **Strengths:** Internal advantages to leverage
- **Weaknesses:** Internal gaps to fix  
- **Opportunities:** External trends to capture
- **Threats:** External risks to mitigate

**Strategic Plays:** S+O=Growth, S+T=Defend, Fix W=Build

✅ Template: `templates/swot-template.md`  
✅ Example: `examples/swot-product-launch.md` (AI Analytics Platform)

---

### 3. 🌍 **PESTEL** — Environmental Scanning
**When:** Market entry, long-term risk, macro trends  
**Time:** 60-90 minutes  
**Output:** Risk map + response plan  

**Dimensions:**
- **Political:** Regulation, policy, stability
- **Economic:** Growth, inflation, currency, employment
- **Social:** Demographics, culture, values
- **Technology:** Innovation, AI, adoption
- **Environmental:** Climate, sustainability, resources
- **Legal:** Compliance, IP, labor law

✅ Template: `templates/pestel-template.md`

---

### 4. 💡 **SCAMPER** — Creative Innovation
**When:** Product improvement, cost reduction, new ideas  
**Time:** 45-60 minutes  
**Output:** Top 3 ideas to prototype  

**Letters:**
- **S**ubstitute — Replace materials/methods?
- **C**ombine — Merge elements?
- **A**dapt — Adjust context?
- **M**odify — Scale/change?
- **P**ut to another use — Different purpose?
- **E**liminate — Remove/simplify?
- **R**everse — Invert/reorder?

✅ Template: `templates/scamper-template.md`

---

### 5. 🎭 **Six Thinking Hats** — Multi-Perspective Decisions
**When:** Team conflict, major decisions, workshops  
**Time:** 45-60 minutes  
**Output:** Clear decision + action items  

**Hats (Perspectives):**
- ⚪ **White** — Facts & data
- 🔴 **Red** — Emotions & intuition
- ⚫ **Black** — Risks & critique
- 🟡 **Yellow** — Benefits & optimism
- 🟢 **Green** — Creativity & alternatives
- 🔵 **Blue** — Process & decision

✅ Template: `templates/six-hats-template.md`

---

## Files Included

### 📄 Core Documentation
- `SKILL.md` — Complete 5000+ word guide (workflows, pitfalls, when to use)
- `README.md` — Quick overview and usage examples
- `INSTALLATION.md` — Setup and quick-start guide

### 📋 Templates (Ready-to-Fill)
- `templates/5whys-template.md`
- `templates/swot-template.md`
- `templates/pestel-template.md`
- `templates/scamper-template.md`
- `templates/six-hats-template.md`

### 📚 Real-World Examples
- `examples/5whys-incident.md` — System outage postmortem with root cause
- `examples/swot-product-launch.md` — AI Analytics platform strategy (detailed)

### 🐍 Python Scripts
- `scripts/analyze.py` — Generate framework templates & guides
- `scripts/generate_diagrams.py` — Create Mermaid diagrams for visualization

---

## How to Use

### Option 1: Manual (Template-Based) ✏️
```bash
# Copy template for your use case
cp skills/custom/strategic-thinking-toolkit/templates/swot-template.md my-strategy.md

# Fill it in with your team
# Review the example first for reference
cat skills/custom/strategic-thinking-toolkit/examples/swot-product-launch.md
```

### Option 2: Automated (Python Scripts) 🤖
```bash
cd skills/custom/strategic-thinking-toolkit

# Generate guide for specific analysis
python scripts/analyze.py \
  --model swot \
  --topic "product_launch" \
  --output json \
  --save

# Generate Mermaid diagrams
python scripts/generate_diagrams.py \
  --framework six-hats \
  --title "Hiring Decision" \
  --save
```

### Option 3: Guided Workflow 🚀
1. **Identify** → What's the situation?
2. **Select** → Which framework fits?
3. **Analyze** → Run the framework (use template/script)
4. **Synthesize** → Draw conclusions
5. **Decide** → Choose actions
6. **Execute** → Assign owners/timelines
7. **Review** → Check results in 30/60/90 days

---

## Framework Selection Guide

| Situation | Framework | Time | Output |
|-----------|-----------|------|--------|
| System crashed, find root cause | **5 Whys** | 15 min | Root cause + fix |
| Plan product launch | **SWOT** | 60 min | Strategy + 90-day plan |
| Enter new market | **SWOT + PESTEL** | 120 min | Positioning + risk map |
| Innovate product | **SCAMPER** | 45 min | Top 3 ideas |
| Can't decide as team | **Six Hats** | 45 min | Clear decision |
| Scan external risks | **PESTEL** | 90 min | Risk assessment |
| Quarterly review | **SWOT** | 60 min | Strategy refresh |

---

## Key Success Principles

✅ **5 Whys:** Stop when you can act, not at 5 exactly  
✅ **SWOT:** Force strategy plays (S+O, S+T, Fix W)  
✅ **PESTEL:** Update quarterly with sources cited  
✅ **SCAMPER:** Prototype top 3 within 1-2 weeks  
✅ **Six Hats:** Use timer per hat; Blue hat must close  

---

## Common Pitfalls to Avoid

| Framework | Pitfall | Fix |
|-----------|---------|-----|
| 5 Whys | Stop at symptoms | Ask "why" until actionable |
| SWOT | Lists only (no strategy) | Force S+O and S+T plays |
| PESTEL | No sources | Cite specific reports/data |
| SCAMPER | Too creative, not practical | Filter: feasibility × impact |
| Six Hats | People skip/mix hats | Use timer, enforce sequence |

---

## Next Steps

### 🎬 Get Started Today
1. **Pick a use case** (problem, decision, or plan needed)
2. **Choose framework** using guide above
3. **Copy template** from `templates/`
4. **Review example** from `examples/`
5. **Fill with your team** in 30-60 minutes
6. **Create action plan** with owners/dates

### 📖 Deep Dive
- Read `SKILL.md` for complete methodology (5000+ words)
- Check `README.md` for quick reference
- Study examples to see patterns

### 🔧 Customize
- All files are Markdown—edit freely
- Templates are starting points, not dogma
- Add/remove sections for your org

---

## Skill Metadata

| Property | Value |
|----------|-------|
| **Name** | strategic-thinking-toolkit |
| **Version** | 1.0.0 |
| **License** | MIT |
| **Status** | Production Ready |
| **Tags** | strategy, analysis, problem-solving, decision-making, frameworks |
| **Location** | `skills/custom/strategic-thinking-toolkit/` |
| **Last Updated** | 2024-01-20 |

---

## Support

- **Questions?** See `SKILL.md` for full documentation
- **Examples needed?** Check `examples/` directory
- **Stuck on step?** Review template carefully + example side-by-side
- **Want to adapt?** All files are plain Markdown—customize freely

---

**🎯 Ready to think strategically? Start now with:**
```bash
cp skills/custom/strategic-thinking-toolkit/templates/swot-template.md my-analysis.md
```

**See you in 30 days to review results! 🚀**

