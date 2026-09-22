# Legacy Unstructured CSV Analysis & Data Quality Audit

## Overview of Legacy Files

An audit of legacy dirty CSV extracts located in `data_legacy/` revealed multiple data quality issues that prevent direct ingestion without pre-cleaning.

### Summary of Identified Data Deficiencies

1. **Inconsistent Date/Time Formats**:
   - Timestamps contain mixed formats (`YYYY-MM-DD HH:MM:SS`, `MM/DD/YYYY`, and invalid dates like `2023-13-45`).
2. **Unstandardized Vital/Lab Codes**:
   - Vitals use local codes (`HR`, `PULSE`, `HEART_RATE`) rather than LOINC standard codes (`8867-4`).
3. **Non-Numeric and Outlier Values**:
   - Numeric fields contain strings (e.g., `">150"`, `"ERR"`, `"NULL"`, `"-999"`).
4. **Missing Relational Keys**:
   - Key fields (`PATIENT_ID`, `ENCOUNTER_ID`) contain empty or null values requiring fallback reconciliation.

---

## Remediation Strategies Applied by `src/data/loader.py`

- **Date Parsing**: Robust parsing with coercion to UTC `datetime`.
- **LOINC Mapping**: Code normalization dictionary mapping raw aliases to canonical LOINC identifiers.
- **Type Casting & Filtering**: Filtering invalid non-numeric strings and converting numbers to standard floating-point representation.
