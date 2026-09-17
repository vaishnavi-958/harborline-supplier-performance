# Automation design

Flow name: **Supplier OTIF Alert**.

Trigger: weekly scheduled recurrence (Monday 07:30 local), not a record-by-record webhook — OTIF is a period KPI.

Source: Power BI dataset, SharePoint Excel export (`data/exports/supplier_scorecard.csv`), or SQL view `vw_corrective_action_candidates`.

Filter: `otif_pct < 0.90` (Harborline Settings can preview a different threshold; keep the flow parameter in one place).

Action: Apply to each → send Outlook / Teams with `automation/email_templates.md`.

Error path: terminate + notify integration mailbox if the refresh or query fails.

Security: mail a procurement DL, not personal inboxes hard-coded in the flow. Do not put vendor contacts from the synthetic file into production connectors.

Testing: run with a filtered copy where one supplier is forced below 90%, then restore.
