# Data Dictionary

| Dataset | Field | Definition |
| --- | --- | --- |
| cost_centers | cost_center_id | Unique cost-center organization identifier. |
| cost_centers | parent_cost_center_id | Parent organization for hierarchy validation. |
| cost_centers | effective_start / effective_end | Inclusive active dates for the organization. |
| worker_allocations | worker_id | Synthetic worker identifier. |
| worker_allocations | allocation_pct | Portion of labor expense charged to the cost center. |
| labor_transactions | transaction_month | Accounting month at monthly reporting grain. |
| labor_transactions | actual_labor_cost | Synthetic posted labor cost. |
| labor_transactions | budget_labor_cost | Synthetic approved budget. |
| labor_transactions | worktags | Company, Cost Center, Region, Program, and Ledger Account values. |
| exceptions | severity | High, Medium, or Low remediation priority. |
| exceptions | source_record_ids | Linked transaction, worker, or cost-center IDs supporting the finding. |
| exceptions | status | Open, in progress, resolved, or closed remediation state. |
| exceptions | created_date / due_date | Dates used to govern remediation SLA. |
| exceptions | days_open | Exception aging measured from created date to report as-of date. |
| exceptions | sla_status | Whether an open item is within its target or overdue. |

## Control Grouping

Effective-dating exceptions are grouped by cost center and accounting month when multiple transactions share the same root cause. The linked transaction IDs remain visible in `source_record_ids`, so the queue avoids duplicate operational tickets without losing auditability.

## Data Handling Note

All rows are generated. The project contains no PHI, PII, employee names, payroll data, patient data, or Workday tenant data.
