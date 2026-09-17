# Power Automate flow — Supplier OTIF Alert

Independent Procurement Analytics Project using a synthetic procurement dataset.

This is a build guide for a Microsoft Power Automate **Scheduled cloud flow**. Capture screenshots in your own tenant. Do **not** add fabricated screenshots to `automation/` or `dashboard/screenshots/`.

## Screenshot checklist (capture yourself)

1. `01_flow_trigger.png` — Recurrence trigger
2. `02_get_supplier_data.png` — Get rows / Excel / SQL
3. `03_filter_otif.png` — Filter array OTIF < 90%
4. `04_condition.png` — Condition `length > 0`
5. `05_send_email.png` — Outlook or Teams
6. `06_test_run.png` — Successful test
7. `07_alert_email.png` — Received message

## Steps

1. **Trigger** — Recurrence, weekly, Monday 07:30, time zone of the buying desk.
2. **Data source** — One of:
   - Excel Online (Business) on `supplier_scorecard.csv` in SharePoint
   - SQL Server / PostgreSQL `vw_corrective_action_candidates`
   - Power BI REST / DAX query against the published dataset
3. **Filter array** — `@less(item()?['otif_pct'], 0.90)` (or `otifAlert/100` if you parameterize).
4. **Condition** — If filtered array is empty, terminate succeeded with “no alerts”. Else **Apply to each**.
5. **Select** dynamic fields: supplier_name, otif_pct, po_lines, late_only_pct, fill_rate, defect_rate, avg_lead_time_variance, risk_band, recommended_action. Do not hard-code values in the template.
6. **Send an email (V2)** or **Post message in a chat or channel** using `email_templates.md`.
7. **Error handling** — Configure run after / Scope: on failure, email the integration mailbox “Harborline OTIF alert failed to refresh”.
8. **Recipients** — Procurement managers DL. Not personal addresses in the flow definition.
9. **Security** — Service account with least privilege to the scorecard file; no guest sharing of the synthetic vendor file outside the team.
10. **Testing** — Duplicate the flow, point at a sandbox sheet with one row at 0.81 OTIF, run once, confirm the body is dynamic, then delete the sandbox connection.

Harborline’s **OTIF alerts** page is the local preview of the same message.
