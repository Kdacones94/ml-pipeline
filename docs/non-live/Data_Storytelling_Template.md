---
title: "Data Story: {{title}}"
date: {{date}}
tags:
  - data-science
  - retrospective
  - narrative
  - project-log
project: "{{project_name}}"
status: in-progress # draft | in-progress | completed
author: {{author}}
---

# 📖 Data Story: {{title}}

> **Executive Summary:** *[Write a 1-2 sentence hook describing the challenge, core breakthrough, and final outcome]*

---

## 🗺️ Storyboard & Narrative Structure

```
 [1. Problem] ──► [2. Tension] ──► [3. Data Insights]
                                           │
 [6. Twist] ◄── [5. The Test] ◄── [4. Hypothesis]
      │
      ▼
 [7. Lessons Learned]
```

---

## 1. 🎯 The Problem
> **Where does the journey begin?**

* **Context:** [What business problem, operational bottleneck, or research gap prompted this work?]
* **Stakeholders Impacted:** [Who was suffering from this problem?]
* **Initial Goal:** [What did success look like at the start?]

---

## 2. ⚡ The Tension
> **What makes this hard?**

> [!warning] Core Constraints
> - **Data/Pipeline Limitations:** [e.g., missing telemetry, schema drift, unindexed tables]
> - **Technical/Resource Constraints:** [e.g., cloud budget, latency caps, compute limits]
> - **Competing Priorities:** [e.g., speed vs. accuracy, stakeholder deadlines]

---

## 3. 🔍 The Data Insights
> **What did the data reveal when you dug in?**

* **Key Finding 1:** [Primary takeaway from EDA or initial inspection]
* **Key Finding 2:** [Unexpected pattern, distribution skew, or correlation]
* **Visual Artifact:** 
  ![[Insert EDA plot, schema map, or latency graph here]]

---

## 4. 💡 The Hypothesis
> **What was your calculated bet?**

* **Proposed Solution:** [What approach did you decide to take?]
* **Trade-offs Accepted:** [What did you sacrifice? e.g., model interpretability vs. performance, offline execution vs. streaming]
* **Expected Impact:** [e.g., "Reduce pipeline runtime by 50%" or "Increase precision by 15%"]

---

## 5. 🛠️ The Test
> **How did you build and execute the solution?**

### Technical Highlights
- **Architecture / Stack:** [e.g., PySpark, DuckDB, XGBoost, Airflow]
- **Key Decision Points:** [Why specific features, algorithms, or pipelines were chosen]

> [!abstract] Implementation Code / Logic
> ```python
> # Insert key snippet or pseudo-code illustrating core logic
> def validate_payload(event):
>     pass
> ```

---

## 6. 🌀 The Unexpected Twist
> **What broke, failed, or surprised you?**

> [!failure] What Happened?
> [Describe the failure mode: data leakage, unexpected nulls, model drift, edge cases in production, etc.]

* **Root Cause Analysis:** [Why did it fail?]
* **Pivot Strategy:** [How did you adjust your approach to address the twist?]

---

## 7. 🚀 Lessons Learned
> **What is the takeaway for the broader system or team?**

- [ ] **Technical Standard:** [What new standard or constraint should be enforced moving forward?]
- [ ] **Workflow Change:** [How does this change future project planning or testing?]
- [ ] **Next Steps:** [Follow-up backlog items or future enhancements]

---

## 👥 Peer Collaboration & Discussion

> [!question] Questions for Reviewers
> 1. *Given the constraints in Section 2, would you have structured the hypothesis differently?*
> 2. *Are there edge cases in Section 6 that we haven't accounted for?*

### Links & Artifacts
* **Pull Request / Repository:** [URL or local link]
* **Dashboard / Notebook:** [URL or local link]
* **Related Notes:** [[Insert Obsidian Internal Links]]