# 🐍🔍 Python Dependency Remediation — Impact Analysis

> **Project:** `ml-pipeline`  
> **Generated:** 9/22/2026, 4:16:23 PM  
> **Extension:** Python Dependency Remediation v1.2.3  
> **Mode:** Impact Analysis (no files modified)  

## 📊 Summary

| | Metric | Value |
|---|--------|-------|
| ⚠️ | **CVEs Found** | **4** |
| 📦 | **Packages to Upgrade** | **6** |
| 💥 | **Breaking Changes** | **4** |
| 🔴 | **Critical/High** | **3** |
| 🟢 | **Python Version** | **3.13.5** |

## 🛡️ CVE Findings

> ⚠️ **4** vulnerabilities across **6** packages

| 📦 Package | Version | ➡️ Upgraded To | 🔗 CVE / Advisory | Summary |
|---------|---------|-------------|----------------|----------|
| **pydantic** | `2.0.0` | `2.13.5` | [GHSA-mr82-8j83-vxmv](https://osv.dev/vulnerability/GHSA-mr82-8j83-vxmv) | — |
|  |  |  | [PYSEC-2026-1812](https://osv.dev/vulnerability/PYSEC-2026-1812) | — |
| **scikit-learn** | `1.2.0` | `1.9.1` | [GHSA-jw8x-6495-233v](https://osv.dev/vulnerability/GHSA-jw8x-6495-233v) | — |
|  |  |  | [PYSEC-2024-110](https://osv.dev/vulnerability/PYSEC-2024-110) | — |

## 🤖 AI-Detected Breaking Changes

> **4** issue(s) detected, **0** auto-fixed

| 📄 File | Line | Package | Severity | Status | Old Code | ➡️ Replacement |
|------|------|---------|----------|--------|----------|-------------|
| bootstrap_repository_script.py | 1 | pydantic | ⚠️ High | ❌ Not Applied | `from pydantic import BaseModel, ConfigDict, Field as PydanticField` | `from pydantic import BaseModel, Field as PydanticField` |
| bootstrap_repository_script.py | 1 | sqlmodel | ⚠️ High | ❌ Not Applied | `from sqlmodel import SQLModel, Field, Relationship` | `from sqlmodel import SQLModel, Relationship &lt;br&gt; from sqlalchemy.orm import Mapped, mapped_column` |
| bootstrap_repository_script.py | 1 | sqlalchemy | ⚠️ High | ❌ Not Applied | `return session.exec(stmt).all()` | `return session.scalars(stmt).all()` |
| bootstrap_repository_script.py | 1 | numpy | 🔶 Medium | ❌ Not Applied | `transitions = np.zeros((3, 3), dtype=float)` | `transitions = np.zeros((3, 3), dtype=np.float64)` |

---

> 🐍🔒 *Python Dependency Remediation • 9/22/2026, 4:16:23 PM*
