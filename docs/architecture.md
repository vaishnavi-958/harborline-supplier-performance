# Architecture

Independent Procurement Analytics Project using a synthetic procurement dataset.

```mermaid
flowchart TD
  A[Synthetic PO generator<br/>Python · Faker · NumPy] --> B[Raw procurement files]
  B --> C[Python data validation]
  C --> D[Clean + transform]
  D --> E[(SQLite / PostgreSQL / SQL Server)]
  E --> F[SQL KPI layer]
  D --> G[Python analytics]
  G --> H[Weighted scorecard · risk · Pareto]
  F --> I[Harborline desk / Power BI dataset]
  H --> I
  I --> J[Executive · Scorecard · OTIF · Quality · Cost · Risk · Pareto]
  I --> K[Power Automate<br/>Supplier OTIF Alert]
  K --> L[Procurement manager]
  L --> M[5-Why + fishbone RCA]
  M --> N[Corrective action]
```

Complementary to a Demand Forecasting & Inventory Optimization project:

- Project 1 answers *what to buy and when*.
- Harborline answers *who delivered, at what quality and cost, and what to do next*.

Local runtime uses SQLite so the repo stays credential-free. `sql/` objects are written as views; swap the loader DSN for PostgreSQL or SQL Server without changing the grain of `fact_purchase_orders`.
