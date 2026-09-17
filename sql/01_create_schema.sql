-- Harborline procurement star schema (SQLite dialect).
-- Equivalent objects can be created in PostgreSQL or SQL Server.

CREATE TABLE IF NOT EXISTS dim_supplier (
    supplier_id TEXT PRIMARY KEY,
    supplier_name TEXT,
    supplier_region TEXT,
    supplier_category TEXT,
    supplier_tier TEXT,
    contract_start_date TEXT,
    contract_end_date TEXT,
    sla_days INTEGER,
    payment_terms TEXT,
    primary_contact_role TEXT
);

CREATE TABLE IF NOT EXISTS dim_material (
    material_id TEXT PRIMARY KEY,
    material_description TEXT,
    category TEXT,
    standard_price REAL
);

CREATE TABLE IF NOT EXISTS dim_category (
    category_id TEXT,
    category TEXT
);

CREATE TABLE IF NOT EXISTS dim_region (
    region_id TEXT,
    region TEXT
);

CREATE TABLE IF NOT EXISTS dim_plant (
    plant_id TEXT PRIMARY KEY,
    plant_name TEXT,
    region TEXT
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    date TEXT,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name TEXT,
    year_month TEXT,
    week INTEGER,
    day_of_week TEXT,
    is_weekend INTEGER
);

CREATE TABLE IF NOT EXISTS dim_carrier (
    carrier_id TEXT PRIMARY KEY,
    carrier TEXT
);
