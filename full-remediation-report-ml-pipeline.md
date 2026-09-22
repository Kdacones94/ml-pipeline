# 🐍🔒 Python Dependency Remediation Security Report

> **Project:** `ml-pipeline`  
> **Generated:** 9/22/2026, 4:25:38 PM  
> **Extension:** Python Dependency Remediation v1.2.3  

## 📊 Summary

| | Metric | Value |
|---|--------|-------|
| ⚠️ | **CVEs Found** | **4** |
| 📦 | **Packages Fixed** | **2** |
| ⚪ | **Tests Passed** | **0/0** |
| 💥 | **Breaking Changes** | **9** |
| 🔴 | **Critical/High** | **7** |
| 🟢 | **Python Version** | **3.13.5** |

## 🛡️ CVE Findings

> ⚠️ **4** vulnerabilities across **2** packages

| 📦 Package | Version | ➡️ Upgraded To | 🔗 CVE / Advisory | Summary |
|---------|---------|-------------|----------------|----------|
| **pydantic** | `2.0.0` | `2.13.5` | [GHSA-mr82-8j83-vxmv](https://osv.dev/vulnerability/GHSA-mr82-8j83-vxmv) | — |
|  |  |  | [PYSEC-2026-1812](https://osv.dev/vulnerability/PYSEC-2026-1812) | — |
| **scikit-learn** | `1.2.0` | `1.9.1` | [GHSA-jw8x-6495-233v](https://osv.dev/vulnerability/GHSA-jw8x-6495-233v) | — |
|  |  |  | [PYSEC-2024-110](https://osv.dev/vulnerability/PYSEC-2024-110) | — |

## 🤖 AI-Detected Breaking Changes

> **9** issue(s) detected, **9** auto-fixed

| 📄 File | Line | Package | Severity | Status | Old Code | ➡️ Replacement |
|------|------|---------|----------|--------|----------|-------------|
| bootstrap_repository_script.py | 1 | pydantic | ⚠️ High | ✅ Applied | `from pydantic import BaseModel, ConfigDict, Field as PydanticField` | `from pydantic import BaseModel, Field as PydanticField` |
| bootstrap_repository_script.py | 1 | sqlalchemy | ⚠️ High | ✅ Applied | `            return session.exec(stmt).all()` | `            return session.scalars(stmt).all()` |
| bootstrap_repository_script.py | 1 | sqlmodel | 🔶 Medium | ✅ Applied | `        SQLModel.metadata.create_all(self.engine)` | `        self.engine.execute(SQLModel.metadata.create_all(self.engine))` |
| bootstrap_repository_script.py | 1 | numpy | 🔶 Medium | ✅ Applied | `            transitions = np.zeros((3, 3), dtype=float)` | `            transitions = np.zeros((3, 3), dtype=float).tolist()` |
| clinical_and_data_models.py | 5 | pydantic | ⛔ Critical | ✅ Applied | `from pydantic import BaseModel, ConfigDict, Field as PydanticField` | `from pydantic import BaseModel, Field as PydanticField` |
| clinical_and_data_models.py | 73 | pydantic | ⛔ Critical | ✅ Applied | `    model_config = ConfigDict(from_attributes=True)` | `    class Config: orm_mode = True` |
| trainer.py | 3 | scikit-learn | ⚠️ High | ✅ Applied | `self.model = LogisticRegression()` | `self.model = LogisticRegression(solver='lbfgs')` |
| trainer.py | 22 | numpy | ⚠️ High | ✅ Applied | `X = np.array(X)` | `X = np.array(X, dtype=object)` |
| trainer.py | 23 | numpy | ⚠️ High | ✅ Applied | `y = np.array(y)` | `y = np.array(y, dtype=object)` |

## 🧪 Test Results

> ⚪ NO TESTS FOUND — No test files detected in project

| ✅ Passed | ❌ Failed | ⏭️ Skipped |
|:--------:|:--------:|:----------:|
| **0** | **0** | **0** |

---

> 🐍🔒 *Python Dependency Remediation • 9/22/2026, 4:25:38 PM*
