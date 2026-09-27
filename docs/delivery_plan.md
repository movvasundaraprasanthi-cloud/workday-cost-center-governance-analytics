# Delivery Plan and Governance Model

## Delivery Approach

This portfolio project follows a practical analyst-led delivery model for a Workday reporting and controls enhancement. The focus is not merely on reporting; it is on establishing measurable controls, assigned remediation ownership, and a repeatable month-end operating process.

| Phase | Analyst activities | Exit criteria |
| --- | --- | --- |
| Discovery | Facilitate Finance, HR Operations, and Workday Support workshops; document decision rights, data sources, and control thresholds. | Approved requirements and KPI definitions. |
| Design | Map current and future-state exception handling; define data grain, worktags, effective-dating rules, and ownership. | Signed-off functional specification and test scenarios. |
| Build | Develop validation SQL, scorecard logic, exception queue, and dashboard-ready dataset. | Reproducible outputs with traceable field definitions. |
| UAT | Reconcile sample outputs with Finance; validate exceptions with HR Operations and Workday Support. | UAT evidence, defects resolved or dispositioned, approval to publish. |
| Operate | Publish monthly scorecard; review high-severity exceptions before close; monitor remediation aging. | Business-as-usual calendar and control owners in place. |

## Governance and Decision Rights

| Decision | Accountable owner | Consulted partners |
| --- | --- | --- |
| Cost-center hierarchy and effective dates | Workday Support | Finance Operations, HR Operations |
| Worker costing allocation corrections | HR Operations | Cost Center Manager, Payroll/Finance |
| Budget threshold and variance commentary | Finance Operations | Cost Center Manager |
| Scorecard publication and KPI definitions | Finance Operations | Analytics, Workday Support |

## Risks and Controls

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Cost center is ended but downstream transactions still post | Incorrect reporting and late-close corrections | Validate transaction date against effective-dated organization status; route high-severity exceptions to Workday Support. |
| Worker allocations do not total 100% | Labor expense is misstated or unallocated | Reconcile allocations by worker and effective month before period close. |
| Dashboard definitions change without version control | Leadership loses trust in trends | Maintain KPI definitions, data dictionary, and change log with Finance approval. |
| Exceptions lack an owner or due date | Repeated operational defects | Require owner group, severity, recommended action, and aging in the exception queue. |

## Test Strategy

- Reconcile the total actual and budget labor spend from the scorecard to the input ledger extract.
- Test transactions on cost-center start and end dates, as well as after the end date.
- Test worker costing allocations totaling 100%, below 100%, and above 100%.
- Validate that the review flag applies when dollar or percentage threshold is exceeded.
- Obtain Finance, HR Operations, and Workday Support UAT sign-off before scheduled publication.

## Portfolio Boundary

All names, amounts, records, and outcomes in this project are synthetic. The project demonstrates analysis, documentation, validation, and reporting methods; it does not claim access to a Workday tenant or production employer data.
