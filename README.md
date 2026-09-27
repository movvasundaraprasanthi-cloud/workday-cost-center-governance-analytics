# Workday Cost Center Governance and Labor Spend Analytics

## Portfolio Project Purpose

This project models how a senior healthcare or enterprise business analyst could support Workday cost center governance, workforce costing, and monthly labor-spend reporting. It uses **synthetic data only** and is not connected to a Workday tenant or any employer system.

The project is intentionally designed as a realistic cross-functional delivery package rather than a simple dashboard. It includes business requirements, validation rules, SQL analysis, a reproducible Python pipeline, Power BI-ready outputs, a data dictionary, and an executive stakeholder readout.

## Business Problem

Finance and HR operations need trustworthy cost-center structures and labor-cost reporting. Common issues include inactive or missing parent organizations, workers allocated to expired cost centers, allocation totals that do not equal 100%, and unexplained month-over-month variance. These defects reduce reporting confidence and delay budget-owner decisions.

## Objectives

1. Validate cost-center hierarchy and effective-dated status.
2. Identify workforce allocations that do not reconcile to 100%.
3. Compare actual labor spend to budget by cost center and month.
4. Create a prioritized exception queue for Finance, HR Operations, and system owners.
5. Publish Power BI-ready scorecards with transparent KPI definitions.

## Workday-Oriented Data Model

| Concept | Illustrative use in this project |
| --- | --- |
| Cost Center Organization | Owns labor spend and budget accountability |
| Supervisory Organization | Provides manager and staffing context |
| Worktags | Company, Cost Center, Program, Region, Ledger Account |
| Effective Dating | Validates whether a cost center is active when a transaction posts |
| Worker Costing Allocation | Splits a worker's labor cost across cost centers |
| Business Process Controls | Defines review and remediation ownership for exceptions |

## Deliverables

- `docs/business_requirements.md` — requirements, acceptance criteria, scope, and control ownership.
- `docs/data_dictionary.md` — data fields, grain, and validation definitions.
- `docs/delivery_plan.md` — implementation sequence, governance, risk controls, and test approach.
- `docs/workday_reporting_artifacts.md` — synthetic report specification, calculated-field logic, and integration mapping.
- `sql/01_cost_center_governance.sql` — reusable validation and variance queries.
- `src/build_outputs.py` — generates synthetic source data, exception queues, and BI-ready scorecards.
- `data/exports/` — CSV exports ready for Power BI, Tableau, or Excel.
- `reports/executive_readout.md` — stakeholder-facing findings and recommended actions.
- `dashboards/cost_center_governance_preview.svg` — a static dashboard preview produced by the pipeline.

## Key KPIs

- Active cost-center hierarchy completeness
- Effective-dated transaction compliance
- Worker allocation reconciliation rate
- Labor spend variance to budget
- Unmapped or invalid worktag count
- Exception aging and remediation priority

## How to Run

```bash
python3 src/build_outputs.py
python3 -m unittest tests/test_output_contracts.py
```

## Interview Narrative

> I designed a synthetic Workday cost-center governance project to demonstrate how I approach finance and HR data controls. I started with business requirements and KPI definitions, modeled effective-dated cost centers and worker allocations, wrote SQL validation logic, generated a prioritized exception queue, and delivered Power BI-ready scorecards. The work demonstrates analysis and documentation capability; it does not represent access to a live Workday tenant.

## Resume-Safe Portfolio Bullet

Built a synthetic Workday cost-center governance and labor-spend analytics portfolio project using SQL, Python, reconciliation controls, business requirements, and Power BI-ready scorecards to identify hierarchy, effective-dating, allocation, and budget-variance exceptions. No employer or tenant data was used.
