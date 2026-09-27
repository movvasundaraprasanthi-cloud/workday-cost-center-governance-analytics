"""Generate synthetic Workday-style cost-center governance analytics outputs.

This portfolio demonstration has no Workday tenant connection and no employer data.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
EXPORTS = ROOT / "data" / "exports"
REPORTS = ROOT / "reports"
DASHBOARDS = ROOT / "dashboards"
AS_OF_DATE = date(2025, 4, 30)

for directory in (RAW, EXPORTS, REPORTS, DASHBOARDS):
    directory.mkdir(parents=True, exist_ok=True)


COST_CENTERS = [
    ("CC-1000", "Corporate Services", "", "2024-01-01", "2026-12-31", "Corporate", "North"),
    ("CC-1100", "Clinical Operations", "CC-1000", "2024-01-01", "2026-12-31", "Care Delivery", "South"),
    ("CC-1200", "Digital Health", "CC-1000", "2024-01-01", "2026-12-31", "Technology", "West"),
    ("CC-1300", "Revenue Operations", "CC-1000", "2024-01-01", "2026-12-31", "Finance", "East"),
    ("CC-1400", "Legacy Support", "CC-1000", "2024-01-01", "2025-03-31", "Technology", "South"),
    # Deliberate synthetic hierarchy exception used to demonstrate the control.
    ("CC-1500", "Growth Operations", "CC-9999", "2024-01-01", "2026-12-31", "Operations", "Central"),
]


def write_csv(path: Path, rows: list[dict]) -> None:
    """Write a non-empty list of dictionary rows to a UTF-8 CSV."""
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def make_exception(
    exceptions: list[dict],
    *,
    exception_type: str,
    severity: str,
    owner_group: str,
    cost_center_id: str,
    reason: str,
    recommended_action: str,
    source_record_ids: str,
    created_days_ago: int,
) -> None:
    """Add a traceable, SLA-managed exception record to the remediation queue."""
    created_date = AS_OF_DATE - timedelta(days=created_days_ago)
    target_days = 5 if severity == "High" else 10
    due_date = created_date + timedelta(days=target_days)
    exceptions.append(
        {
            "exception_id": f"EX-{len(exceptions) + 1:03d}",
            "exception_type": exception_type,
            "severity": severity,
            "status": "Open",
            "owner_group": owner_group,
            "cost_center_id": cost_center_id,
            "reason": reason,
            "recommended_action": recommended_action,
            "source_record_ids": source_record_ids,
            "created_date": created_date.isoformat(),
            "due_date": due_date.isoformat(),
            "days_open": created_days_ago,
            "sla_status": "Overdue" if AS_OF_DATE > due_date else "Within SLA",
            "as_of_date": AS_OF_DATE.isoformat(),
        }
    )


def write_dashboard_preview(scorecard: list[dict], exceptions: list[dict]) -> None:
    """Create a dependency-free static SVG preview for the portfolio dashboard."""
    reviewed = sum(row["review_flag"] == "Review" for row in scorecard)
    actual_total = sum(float(row["actual_labor_cost"]) for row in scorecard)
    budget_total = sum(float(row["budget_labor_cost"]) for row in scorecard)
    variance = actual_total - budget_total
    within_sla = sum(row["sla_status"] == "Within SLA" for row in exceptions)
    rows = "".join(
        f'<text x="70" y="{350 + index * 31}" class="row">{item["exception_id"]} | '
        f'{item["exception_type"]} | {item["owner_group"]} | {item["sla_status"]} | {item["reason"]}</text>'
        for index, item in enumerate(exceptions)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="560" viewBox="0 0 1200 560">
<style>
  .title {{ font: 700 30px Arial, sans-serif; fill: #102a43; }}
  .sub {{ font: 16px Arial, sans-serif; fill: #486581; }}
  .label {{ font: 600 15px Arial, sans-serif; fill: #486581; }}
  .metric {{ font: 700 28px Arial, sans-serif; fill: #102a43; }}
  .row {{ font: 14px Arial, sans-serif; fill: #243b53; }}
</style>
<rect width="1200" height="560" fill="#f7fafc"/>
<text x="50" y="55" class="title">Cost Center Governance &amp; Labor Spend</text>
<text x="50" y="82" class="sub">Synthetic Workday-style portfolio dashboard | January–April 2025</text>
<g transform="translate(50 120)">
  <rect width="250" height="130" rx="12" fill="#ffffff" stroke="#d9e2ec"/>
  <text x="22" y="38" class="label">Labor spend</text><text x="22" y="82" class="metric">${actual_total:,.0f}</text>
</g>
<g transform="translate(330 120)">
  <rect width="250" height="130" rx="12" fill="#ffffff" stroke="#d9e2ec"/>
  <text x="22" y="38" class="label">Budget variance</text><text x="22" y="82" class="metric">${variance:,.0f}</text>
</g>
<g transform="translate(610 120)">
  <rect width="250" height="130" rx="12" fill="#ffffff" stroke="#d9e2ec"/>
  <text x="22" y="38" class="label">Exceptions within SLA</text><text x="22" y="82" class="metric">{within_sla}/{len(exceptions)}</text>
</g>
<g transform="translate(890 120)">
  <rect width="250" height="130" rx="12" fill="#ffffff" stroke="#d9e2ec"/>
  <text x="22" y="38" class="label">Cost-center months to review</text><text x="22" y="82" class="metric">{reviewed}</text>
</g>
<rect x="50" y="295" width="1090" height="195" rx="12" fill="#ffffff" stroke="#d9e2ec"/>
<text x="70" y="330" class="label">Prioritized exception queue</text>
{rows}
<text x="70" y="525" class="sub">Control thresholds: allocation total = 100%; inactive cost center = high severity; variance &gt; 10% or $20K = review.</text>
</svg>'''
    (DASHBOARDS / "cost_center_governance_preview.svg").write_text(svg, encoding="utf-8")


def build() -> None:
    fields = (
        "cost_center_id",
        "cost_center_name",
        "parent_cost_center_id",
        "effective_start",
        "effective_end",
        "program",
        "region",
    )
    centers = [dict(zip(fields, row)) for row in COST_CENTERS]
    write_csv(RAW / "cost_centers.csv", centers)

    allocations = [
        {"worker_id": "W-001", "effective_month": "2025-01-01", "cost_center_id": "CC-1100", "allocation_pct": 60, "active_flag": "Y"},
        {"worker_id": "W-001", "effective_month": "2025-01-01", "cost_center_id": "CC-1200", "allocation_pct": 40, "active_flag": "Y"},
        {"worker_id": "W-002", "effective_month": "2025-01-01", "cost_center_id": "CC-1300", "allocation_pct": 100, "active_flag": "Y"},
        {"worker_id": "W-003", "effective_month": "2025-01-01", "cost_center_id": "CC-1200", "allocation_pct": 70, "active_flag": "Y"},
        {"worker_id": "W-003", "effective_month": "2025-01-01", "cost_center_id": "CC-1300", "allocation_pct": 20, "active_flag": "Y"},
    ]
    write_csv(RAW / "worker_allocations.csv", allocations)

    transactions: list[dict] = []
    base = {"CC-1100": 198000, "CC-1200": 245000, "CC-1300": 162000, "CC-1400": 82000}
    factors = {"2025-01-01": 1.01, "2025-02-01": 1.03, "2025-03-01": 1.12, "2025-04-01": 0.98}
    number = 1
    for month, factor in factors.items():
        for cost_center, budget in base.items():
            actual = round(budget * factor, 2)
            center = next(row for row in centers if row["cost_center_id"] == cost_center)
            transactions.append(
                {
                    "transaction_id": f"LT-{number:04d}",
                    "transaction_month": month,
                    "cost_center_id": cost_center,
                    "company": "US01",
                    "region": center["region"],
                    "program": center["program"],
                    "ledger_account": "610100",
                    "actual_labor_cost": actual,
                    "budget_labor_cost": budget,
                }
            )
            number += 1

    # Deliberate synthetic exceptions to evidence each required control.
    transactions.append(
        {
            "transaction_id": "LT-9999",
            "transaction_month": "2025-04-01",
            "cost_center_id": "CC-1400",
            "company": "US01",
            "region": "South",
            "program": "Technology",
            "ledger_account": "610100",
            "actual_labor_cost": 22000,
            "budget_labor_cost": 0,
        }
    )
    transactions.append(
        {
            "transaction_id": "LT-9998",
            "transaction_month": "2025-04-01",
            "cost_center_id": "CC-1300",
            "company": "",
            "region": "",
            "program": "Finance",
            "ledger_account": "",
            "actual_labor_cost": 12000,
            "budget_labor_cost": 12000,
        }
    )
    write_csv(RAW / "labor_transactions.csv", transactions)

    centers_by_id = {row["cost_center_id"]: row for row in centers}
    exceptions: list[dict] = []

    for center in centers:
        parent_id = center["parent_cost_center_id"]
        if not parent_id:
            continue
        parent = centers_by_id.get(parent_id)
        if not parent:
            make_exception(
                exceptions,
                exception_type="Hierarchy",
                severity="High",
                owner_group="Workday Support",
                cost_center_id=center["cost_center_id"],
                reason=f"Active cost center references missing parent {parent_id}",
                recommended_action="Correct the parent cost center before the next hierarchy publication.",
                source_record_ids=center["cost_center_id"],
                created_days_ago=2,
            )
            continue
        parent_active = date.fromisoformat(parent["effective_start"]) <= AS_OF_DATE <= date.fromisoformat(parent["effective_end"])
        if not parent_active:
            make_exception(
                exceptions,
                exception_type="Hierarchy",
                severity="High",
                owner_group="Workday Support",
                cost_center_id=center["cost_center_id"],
                reason=f"Parent cost center {parent_id} is inactive as of {AS_OF_DATE.isoformat()}",
                recommended_action="Update the hierarchy or effective dates before the next reporting cycle.",
                source_record_ids=center["cost_center_id"],
                created_days_ago=2,
            )

    invalid_postings: dict[tuple[str, str], list[str]] = defaultdict(list)
    for transaction in transactions:
        center = centers_by_id.get(transaction["cost_center_id"])
        posted = date.fromisoformat(transaction["transaction_month"])
        if not center or posted < date.fromisoformat(center["effective_start"]) or posted > date.fromisoformat(center["effective_end"]):
            invalid_postings[(transaction["cost_center_id"], transaction["transaction_month"])].append(transaction["transaction_id"])
    for (cost_center_id, month), transaction_ids in sorted(invalid_postings.items()):
        make_exception(
            exceptions,
            exception_type="Effective dating",
            severity="High",
            owner_group="Workday Support",
            cost_center_id=cost_center_id,
            reason=f"{len(transaction_ids)} labor transaction(s) posted to an inactive cost center in {month}",
            recommended_action="Review the effective-dated assignment and correct the linked source transactions.",
            source_record_ids=", ".join(sorted(transaction_ids)),
            created_days_ago=3,
        )

    for transaction in transactions:
        missing_worktags = [
            label
            for label, field in (("Company", "company"), ("Cost Center", "cost_center_id"), ("Ledger Account", "ledger_account"), ("Region", "region"))
            if not transaction[field]
        ]
        if missing_worktags:
            make_exception(
                exceptions,
                exception_type="Required worktags",
                severity="Medium",
                owner_group="Finance Operations",
                cost_center_id=transaction["cost_center_id"] or "Unassigned",
                reason=f"Required worktags missing: {', '.join(missing_worktags)}",
                recommended_action="Populate required worktags and revalidate before publishing the scorecard.",
                source_record_ids=transaction["transaction_id"],
                created_days_ago=1,
            )

    total_by_worker = defaultdict(float)
    for allocation in allocations:
        if allocation["active_flag"] == "Y":
            total_by_worker[(allocation["worker_id"], allocation["effective_month"])] += allocation["allocation_pct"]
    for (worker_id, month), allocation_total in sorted(total_by_worker.items()):
        if allocation_total != 100:
            make_exception(
                exceptions,
                exception_type="Worker allocation",
                severity="High",
                owner_group="HR Operations",
                cost_center_id="Multiple",
                reason=f"{worker_id} allocations total {allocation_total:.0f}% for {month}",
                recommended_action="Correct worker costing allocation to 100% before period close.",
                source_record_ids=worker_id,
                created_days_ago=4,
            )

    monthly = defaultdict(lambda: {"actual": 0.0, "budget": 0.0})
    for transaction in transactions:
        key = (transaction["transaction_month"], transaction["cost_center_id"])
        monthly[key]["actual"] += float(transaction["actual_labor_cost"])
        monthly[key]["budget"] += float(transaction["budget_labor_cost"])

    scorecard = []
    for (month, cost_center), values in sorted(monthly.items()):
        variance = values["actual"] - values["budget"]
        variance_pct = 0 if not values["budget"] else round(100 * variance / values["budget"], 2)
        scorecard.append(
            {
                "transaction_month": month,
                "cost_center_id": cost_center,
                "cost_center_name": centers_by_id[cost_center]["cost_center_name"],
                "actual_labor_cost": round(values["actual"], 2),
                "budget_labor_cost": round(values["budget"], 2),
                "variance_dollars": round(variance, 2),
                "variance_pct": variance_pct,
                "review_flag": "Review" if abs(variance) > 20000 or abs(variance_pct) > 10 else "Monitor",
            }
        )

    write_csv(EXPORTS / "cost_center_labor_scorecard.csv", scorecard)
    write_csv(EXPORTS / "cost_center_exception_queue.csv", exceptions)
    write_dashboard_preview(scorecard, exceptions)

    high_severity = sum(item["severity"] == "High" for item in exceptions)
    report = f"""# Executive Readout

## Scope
Synthetic Workday-style cost-center governance and labor-spend analysis for January through April 2025.

## Results
- {len(scorecard)} monthly cost-center scorecard records generated from {len(transactions)} synthetic labor transactions.
- {len(exceptions)} prioritized governance exceptions identified; {high_severity} are high severity.
- Controls assessed: hierarchy integrity, effective dating, required worktags, worker allocation reconciliation, and budget variance.
- Each remediation record includes linked source IDs, ownership, SLA target, and aging fields.

## Recommended Actions
1. Workday Support should correct the missing hierarchy reference and inactive-cost-center postings before the next reporting publication.
2. Finance Operations should populate missing required worktags and revalidate the affected transaction.
3. HR Operations should correct allocations that do not total 100% before period close.
4. Finance should review scorecard variances above 10% or $20,000 and retain decision commentary.
5. Publish the scorecard monthly with KPI definitions, remediation ownership, due dates, and aging review.
"""
    (REPORTS / "executive_readout.md").write_text(report, encoding="utf-8")
    print(f"Generated {len(scorecard)} scorecard rows and {len(exceptions)} exceptions.")


if __name__ == "__main__":
    build()
