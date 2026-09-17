-- Dimension load is performed by src/database/loaders.py from CSV.
-- This script documents the intended insert pattern.

-- Example:
-- INSERT INTO dim_supplier SELECT * FROM staging_dim_supplier;
SELECT 'dim load handled by Python loaders' AS note;
