# Circuit Designer Pro — Developer Guide

This document is a concise, senior-developer level guide to the Circuit Designer Pro Streamlit application. It explains purpose, features, architecture, file locations, data flows, deployment steps, testing, and operational procedures required to reproduce or migrate the app to another environment.

---

## 1. Overview

Purpose
- Circuit Designer Pro is a Streamlit-based application to design and prototype switching power circuits (Buck converters, PFC, etc.).
- It computes component values (inductors, capacitors, MOSFETs), suggests vendor components from a local component DB (or web search), and applies documented design heuristics to guide selection.

Audience
- Senior developer or engineer tasked with maintaining, extending, or migrating the app.

High-level capabilities
- Buck converter calculations and component recommendations.
- Component Library viewer and heuristics document ingestion (MS Word `.docx` / CSV / XLSX sources).
- Optional live web-scraping (Mouser) for distributor results when enabled.
- CI workflows to verify remote deployment and notify via Slack/email.

---

## 2. Key Features & Flow

1. Input UI (Buck calculator)
   - Collects V_in/V_out ranges, output power, switching frequency, ripple targets, etc.
   - Validates inputs and provides auto-fix presets.

2. Calculation Engine (`lib/calculations.py`)
   - Implements the electrical formulas to compute inductance, output/input capacitance, duty cycle, ripple currents.
   - Exposes `CircuitCalculator` and `BuckInputs` typed models used by the pages.

3. Component Suggestion Engine (`lib/component_suggestions.py`)
   - Reads component databases (MOSFET, inductors, capacitors) and applies heuristics to rank parts.
   - Heuristics are documented in assets/design_heuristics and parsed by `lib/document_analyzer.py`.
   - Can operate in local DB mode or `use_web_search` (calls `lib/web_component_scraper.py`).

4. Component DB (`lib/component_data.py`)
   - Loads data primarily from Excel (`openpyxl`) if present, otherwise falls back to CSV loaders.
   - Exposes in-memory libraries: `MOSFET_LIBRARY`, `INDUCTOR_LIBRARY`, `CAPACITOR_LIBRARY`, `INPUT_CAPACITOR_LIBRARY`.
   - `reload_component_data()` re-reads sources — used by pages to ensure fresh data.

5. Document Analyzer (`lib/document_analyzer.py`)
   - Reads `.docx` heuristics documents when `python-docx` is available and extracts selection criteria.
   - Produces machine-usable guidelines and human-readable recommendation lines used by `component_suggestions`.

6. UI Pages
   - `pages/buck_calculator.py` — main Buck converter designer (inputs, run, results, recommendations, simulation hooks).
   - `pages/component_library.py` — browse raw component DB and design documents.
   - `pages/simulation_demo.py` — optional simulation UI (LTSpice integration placeholder).

7. CI & Deployment
   - `.github/workflows/verify_streamlit_deploy.yml` — polls the published Streamlit URL and posts failures to issues/Slack and uploads debugging artifacts.
   - `.github/workflows/report_deploy_run.yml` — closes or updates issues and posts summary notifications (uses `GH_API_TOKEN`).

---

## 3. File layout (important files and folders)

Root
- `app.py` — Streamlit app entry point. Sets page layout and routes to pages.
- `requirements.txt` — Python dependencies.
- `.github/workflows/` — CI workflows.

Pages:
- `pages/buck_calculator.py`
- `pages/component_library.py`
- `pages/pfc_calculator.py` (optional)
- `pages/simulation_demo.py`

Libraries:
- `lib/component_data.py` — component DB loaders, dataclasses and library objects.
- `lib/component_suggestions.py` — recommendation and ranking logic.
- `lib/design_heuristics.py` — helper functions to list and present heuristics documents.
- `lib/document_analyzer.py` — heuristics extraction from `.docx` files.
- `lib/llm_assistant.py` — LLM assistant wrapper (optional; requires OPENAI_API_KEY).
- `lib/web_component_scraper.py` — distributor scraping for web search mode.
- `lib/component_display.py` — UI table rendering for suggestions.

Assets (primary data sources; replace/upload files here):
- `assets/component_data/` — CSV/XLSX files used by `lib/component_data` (e.g., `mosfets.csv`, `inductors.csv`, `input_capacitors.csv`, `output_capacitors.csv`).
- `assets/design_heuristics/` — subfolders `mosfets/`, `inductors/`, `capacitors/` containing `.docx` heuristics documents.
- `assets/...` — other static assets (images, example files).

Scripts:
- `scripts/` — helper scripts (push helpers, local automation).

Tests:
- `test_*.py` — pytest-based unit and integration tests.

---

## 4. Where to drop data and documentation (operational)

Component data
- Add CSV/XLSX files to `assets/component_data/`. Naming conventions:
  - `mosfets.csv` or `PowerCrux_SAFE_LINKS_EXACT_50_Si_MOSFETs_SyncBuck.xlsx`
  - `inductors.csv` or `powercrux_inductors_20parts (2).xlsx`
  - `input_capacitors.csv` / `output_capacitors.csv`
- After uploading, trigger a reload in the UI: open *Component Library* page and press **🔄 Reload Data** or call `reload_component_data()` programmatically.

Design heuristics (documents)
- Place `.docx` files in `assets/design_heuristics/<component_type>/`, e.g. `assets/design_heuristics/mosfets/MOSFET Design heuristics.docx`.
- The app reads these documents at runtime when `python-docx` is installed. Use the **Component Library → Design Docs** UI to confirm the file is recognized.

Notes on file formats
- Preferred: `.xlsx` or `.csv` for component tabular data (use the same column names seen in `lib/component_data.py`).
- Heuristics: `.docx` recommended (parser currently extracts textual lines and looks for keywords). Keep statements factual and include explicit numeric recommendations where possible (e.g., "VDS derating 50%", "RDS(on) measured at 125°C").

---

## 5. Local development — setup & run

Prerequisites
- Python 3.10+ (project tested with Python 3.14 locally)
- Git
- Recommended: Create a virtual environment

Install

```bash
python -m venv .venv
.\.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

Run locally

```bash
python -m streamlit run app.py --server.port 8501 --server.headless true
```

Notes
- If `openpyxl` is not installed the app will fall back to CSV loaders.
- If `python-docx` is not installed, heuristics `.docx` files will be ignored (the UI warns when docx not available).

---

## 6. Deploying to Streamlit Cloud

1. Create or log into https://share.streamlit.io.
2. Create a new app, point it at the repo and branch (`main`) and set the main module to `app.py`.
3. If the repo is private: grant Streamlit the GitHub App permissions for this repo or ask an org admin to approve the installation.
4. Required secrets (in Streamlit app settings) — set as needed:
   - `OPENAI_API_KEY` (optional LLM features)
   - Any other API keys used by the app's optional features
5. If you update component DB or heuristics files in the repo, commit and push; Streamlit will redeploy automatically.

Troubleshooting clone failures
- If logs show "Failed to download the sources" → re-authorize the GitHub App or make repo public temporarily to test.

---

## 7. CI / Automation

Key workflows
- `.github/workflows/verify_streamlit_deploy.yml` — post-deploy verifier that polls the Streamlit URL and uploads a debug artifact (`verify_last_response.txt`) when failures occur.
- `.github/workflows/report_deploy_run.yml` — uses `GH_API_TOKEN` to update/close failure issues and post Slack notifications.

Secrets
- `GH_API_TOKEN` — required by post-deploy report workflow for authenticated repo operations.
- Slack webhook / SMTP secrets — if using Slack/email notifications, add them to repository secrets.

How the verification works
- On push to `main`, the verify workflow polls the published `APP_URL` until success or timeout. On failure it creates/updates an issue and uploads the last HTTP response (headers + truncated body) as an artifact for debugging.

---

## 8. Tests & validation

Run unit tests

```bash
pytest -q
```

Important test areas
- `test_component_loading.py` — ensures component DB loading works across CSV/XLSX fallbacks.
- `test_calculations.py` — validates numerical formulas.
- `test_comprehensive_selection.py` — validates selection pipeline with heuristics.

When adding new component data files, run tests that exercise loaders and suggestion functions.

---

## 9. Heuristics documents — authoring guidance

- Keep heuristics factual and explicit: provide numeric derating values (e.g., "VDS derate 50%"), temperature references ("RDS(on) at 125°C"), and clear selection rules.
- Avoid marketing language. The parser extracts lines with keywords (VDS, RDS, VGS, dv/dt, qgd, qgs, SOA); include these keywords when relevant.
- Save as `.docx` for best parser compatibility.

---

## 10. Maintenance and common changes

To update component DB
- Replace / add CSV/XLSX files in `assets/component_data/` and reload in UI or call `reload_component_data()`.

To update heuristics
- Drop `.docx` files into `assets/design_heuristics/<component_type>/` and either reload via Component Library UI or restart the app.

To extend selection logic
- Update `lib/document_analyzer.py` to extract additional numeric values, then update `lib/component_suggestions.py` to consume those values in ranking logic.

To add a new page
- Add `pages/<your_page>.py` and export a `show()` function; `app.py` will import pages dynamically. Follow existing page patterns for layout and session-state usage.

---

## 11. Troubleshooting tips

- Unicode / printing issues when running tests locally: set terminal encoding to UTF-8 or ensure `sys.stdout.reconfigure(encoding='utf-8')` when printing parsed doc lines.
- Missing CSV/XLSX files: loaders fall back to hard-coded `get_fallback_*()` lists; check logs for fallback warnings.
- Streamlit Cloud clone errors: verify GitHub App permissions and repo/branch configuration.
- If web scraping fails due to rate limits: disable web search mode or provide distributor API credentials where supported.

---

## 12. Contact & ownership

- Primary repo owner: repository `main` branch. For production Streamlit app credentials and org-level approvals, coordinate with the GitHub org admin.
- When adding major changes to heuristics parsing or component selection logic, include a short design note in `PROGRESS_SUMMARY.md` describing the change and the test vector used.

---

## 13. Quick checklist to reproduce in a new environment

1. Clone repo, create virtualenv, install `requirements.txt`.
2. Place component CSV/XLSX files in `assets/component_data/`.
3. Place heuristics `.docx` in `assets/design_heuristics/<component_type>/`.
4. Set required environment variables / Streamlit secrets (if needed).
5. Run `streamlit run app.py` and validate `Component Library` → `Design Docs` shows uploaded documents.
6. Run `pytest` and verify tests pass.

---

## Appendix: Useful code entry points

- `app.py` — main app and page routing
- `lib/component_data.py` — data loaders and `reload_component_data()`
- `lib/document_analyzer.py` — heuristics extraction
- `lib/component_suggestions.py` — ranking and recommendation engine
- `pages/buck_calculator.py` — primary calculation UI and results display
- `.github/workflows/verify_streamlit_deploy.yml` — deployment verification

---

If you want, I can:
- Commit this document to the repo now (already staged here in `assets/DEVELOPER_GUIDE.md`).
- Add a short `README.md` at the repo root summarizing install & run steps for junior devs.
- Extend the heuristics parser to extract numeric fields (I can propose a patch to `lib/document_analyzer.py`).

