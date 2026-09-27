# Synthetic Workday Reporting Artifacts

## Purpose and Boundary

These are illustrative analysis artifacts, not exported tenant configuration. They demonstrate how a Business Analyst could document a Workday reporting/control enhancement. All labels, IDs, and logic are synthetic.

## 1. Custom Report Specification: Cost Center Governance Scorecard

| Attribute | Specification |
| --- | --- |
| Business purpose | Enable Finance, HR Operations, and Workday Support to identify cost-center governance defects and labor-spend variance before period close. |
| Report grain | One row per accounting month, cost center, and company. |
| Primary data domains | Cost Center Organization, Worker Costing Allocation, labor ledger activity, and finance worktags. |
| Prompts | As-of date; accounting period; company; cost center hierarchy; region; program. |
| Key fields | Cost center ID/name, parent cost center, effective dates, Company, Region, Program, Ledger Account, actual, budget, variance $, variance %, review flag. |
| Security expectation | Finance/HR/Workday Support access should be role-based and limited to the data needed for each operational responsibility. |
| Distribution | Monthly publication after reconciliation; high-severity exceptions routed before close. |

## 2. Calculated-Field Logic: Cost Center Active on Transaction Date

**Name:** `CF_Cost_Center_Active_On_Transaction_Date`  
**Purpose:** Identify labor activity posted to a cost center that is not active for the accounting date.

```text
IF Transaction Date >= Cost Center Effective Start
AND Transaction Date <= Cost Center Effective End
THEN "Valid"
ELSE "Exception"
```

**Business rule:** An `Exception` result routes to Workday Support, with the transaction ID retained for remediation traceability. In a production implementation, final configuration names and available fields would be validated in the client tenant.

## 3. Worktag / Integration Mapping Specification

| Source or payload field | Target analytical field | Validation |
| --- | --- | --- |
| Company reference | `company` | Required; valid company worktag. |
| Cost Center reference | `cost_center_id` | Required; valid and effective-dated on posting date. |
| Region reference | `region` | Required for regional reporting. |
| Ledger Account reference | `ledger_account` | Required for labor-spend classification. |
| Accounting date | `transaction_month` | Must map to the approved reporting period. |
| Amount | `actual_labor_cost` | Numeric, signed, reconciled to source total. |

## 4. Acceptance Test Scenarios

| Scenario | Expected result |
| --- | --- |
| Active cost center with all required worktags | Included in scorecard with no governance exception. |
| Transaction posted after cost-center end date | High-severity effective-dating exception, linked to transaction ID. |
| Active cost center references missing parent | High-severity hierarchy exception, linked to the cost-center ID. |
| Worker allocation totals 90% | High-severity allocation exception, linked to worker ID and effective period. |
| Company, Region, or Ledger Account missing | Medium-severity required-worktags exception, linked to transaction ID. |

## 5. Change Control

1. Finance owns KPI definitions and threshold approvals.
2. HR Operations owns worker-costing corrections.
3. Workday Support owns hierarchy/effective-dating triage and configuration analysis.
4. Changes to report logic require versioned requirements, test evidence, and named business approval.
