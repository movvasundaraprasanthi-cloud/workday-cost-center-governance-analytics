-- Workday Cost Center Governance and Labor Spend Analytics
-- Illustrative SQL compatible with standard analytic SQL patterns.

-- 1. Effective-dated cost center validation
SELECT
    t.transaction_id,
    t.transaction_month,
    t.cost_center_id,
    c.cost_center_name,
    c.effective_start,
    c.effective_end,
    'Cost center inactive on transaction date' AS exception_reason
FROM labor_transactions t
LEFT JOIN cost_centers c ON t.cost_center_id = c.cost_center_id
WHERE c.cost_center_id IS NULL
   OR t.transaction_month < c.effective_start
   OR t.transaction_month > c.effective_end;

-- 2. Worker allocation reconciliation
SELECT
    worker_id,
    effective_month,
    ROUND(SUM(allocation_pct), 2) AS allocation_total,
    CASE
        WHEN ROUND(SUM(allocation_pct), 2) = 100 THEN 'PASS'
        ELSE 'EXCEPTION'
    END AS allocation_status
FROM worker_allocations
WHERE active_flag = 'Y'
GROUP BY worker_id, effective_month
HAVING ROUND(SUM(allocation_pct), 2) <> 100;

-- 3. Monthly labor spend variance and threshold control
SELECT
    transaction_month,
    cost_center_id,
    SUM(actual_labor_cost) AS actual_labor_cost,
    SUM(budget_labor_cost) AS budget_labor_cost,
    SUM(actual_labor_cost) - SUM(budget_labor_cost) AS variance_dollars,
    ROUND(
        100.0 * (SUM(actual_labor_cost) - SUM(budget_labor_cost))
        / NULLIF(SUM(budget_labor_cost), 0), 2
    ) AS variance_pct
FROM labor_transactions
GROUP BY transaction_month, cost_center_id
HAVING ABS(SUM(actual_labor_cost) - SUM(budget_labor_cost)) > 20000
    OR ABS(100.0 * (SUM(actual_labor_cost) - SUM(budget_labor_cost))
        / NULLIF(SUM(budget_labor_cost), 0)) > 10;

