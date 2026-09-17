# Power Automate integration from Power BI

1. Publish the Harborline dataset and scorecard report.
2. In Power BI, use **Alert** on a card only if you need a single-number tripwire. For a supplier list, do **not** rely on a dashboard alert — use a scheduled flow against the scorecard table / CSV / SQL view.
3. Optional: Power BI dataflow refreshes the CSV in SharePoint; the flow reads that file after refresh completes (trigger: when a file is modified, with a 10-minute delay, or Recurrence after the known refresh window).
4. Keep the 90% threshold in one environment variable shared with `config/scoring_config.yaml`.
5. Do not email synthetic `primary_contact_role` as if it were a person.
