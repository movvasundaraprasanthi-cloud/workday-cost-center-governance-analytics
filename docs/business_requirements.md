# Business Requirements

## Stakeholders

- Finance Operations: Owns budget variance review and period-close reporting.
- HR Operations: Owns worker costing allocation and organization data quality.
- Cost Center Managers: Resolve exceptions within their business area.
- Workday Support Team: Evaluates configuration, integration, and effective-dating defects.
- Data and Analytics Team: Produces governed reporting and KPI definitions.

## Functional Requirements

| ID | Requirement | Acceptance Criteria |
| --- | --- | --- |
| BR-01 | Validate that every active cost center has a valid active parent. | Exceptions identify missing, inactive, or self-referencing parents. |
| BR-02 | Validate that labor transactions post to a cost center active on the transaction date. | Every invalid transaction is included in the effective-dating exception queue. |
| BR-03 | Reconcile each worker's costing allocations. | Active allocations total 100% by worker and effective period, or an exception is generated. |
| BR-04 | Report monthly actual labor spend, budget, and variance by cost center. | Scorecard contains actual, budget, variance dollars, and variance percent. |
| BR-05 | Provide a prioritized remediation queue. | Exceptions include owner group, severity, reason, and recommended action. |
| BR-06 | Preserve transparent metric definitions. | Data dictionary documents source, grain, logic, and usage for each KPI. |
| BR-07 | Make every exception traceable to its source record or grouped source records. | Queue includes source record ID(s), does not create duplicate records for the same control failure, and explains its grouping logic. |
| BR-08 | Support operational follow-up and SLA governance. | Queue includes status, created date, due date, days open, and SLA status. |

## Control Rules

1. Cost center must be active on posting date.
2. Parent cost center cannot be blank for a non-root organization.
3. Allocation percentage must total 100% for each worker and effective month.
4. Transactions must include required finance worktags: Company, Cost Center, Ledger Account, and Region.
5. Variances over 10% or $20,000 are prioritized for Finance review.
6. Exceptions are grouped by control, cost center, and accounting period when a single remediation action addresses multiple source transactions.
7. High-severity exceptions have a five-day target; medium-severity exceptions have a ten-day target.

## Out of Scope

- Live Workday configuration or tenant administration.
- Payroll processing, payment approval, or journal posting.
- Real employee, financial, or employer data.
