# SAP integration concept

Harborline is not connected to a live SAP system. The mapping below is how a procurement analyst would source the same grain from SAP S/4HANA / MM, with IBP used upstream for the demand the POs satisfy.

| Harborline field | Conceptual SAP source |
| --- | --- |
| po_id / po_line_id | EKKO / EKPO |
| supplier_id | LFA1 / EKKO-LIFNR |
| material_id | EKPO-MATNR / MARA |
| plant | EKPO-WERKS |
| order_date | EKKO-BEDAT |
| promised_delivery_date | EKET-EINDT |
| actual_delivery_date | EKBE / inbound delivery GR date |
| ordered / received qty | EKPO-MENGE / EKBE WE |
| defective qty | Quality notification / QM usage decision |
| unit_price / standard_price | EKPO-NETPR / MBEW-STPRS (simulate here) |
| payment_terms | LFM1 / EKKO-ZTERM |
| SLA days | Info record / contract / custom table |

IBP would remain the planning system of record for independent demand. Harborline consumes the **execution** result: did the supplier fill the MRP-generated PO on time, in full, and in spec.

Do not present this file as evidence of production RFC, CDS, or CPI work at an employer.
