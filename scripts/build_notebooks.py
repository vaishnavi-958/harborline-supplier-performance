"""Create the eight analysis notebooks."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks"


def nb(cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": cells,
    }


def md(source: str):
    return {"cell_type": "markdown", "metadata": {}, "source": [source]}


def code(source: str):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": [source]}


NOTEBOOKS = {
    "01_data_generation.ipynb": [
        md("# 01 · Data generation\n\nIndependent Procurement Analytics Project using a synthetic procurement dataset."),
        code("import sys\nsys.path.append('..')\nfrom src.data.generate_synthetic_data import generate_all\nfrom src.utils.helpers import load_config\ncfg = load_config()\nresult = generate_all(cfg)\nresult.fact_purchase_orders.head()"),
        code("print(result.fact_purchase_orders.shape)\nprint(result.dim_supplier.groupby('archetype').size())"),
    ],
    "02_data_quality.ipynb": [
        md("# 02 · Data quality"),
        code("import sys\nsys.path.append('..')\nfrom src.data.generate_synthetic_data import generate_all\nfrom src.data.validation import run_checks\nfrom src.utils.helpers import load_config\nraw = generate_all(load_config()).fact_raw\nrun_checks(raw)"),
    ],
    "03_supplier_exploration.ipynb": [
        md("# 03 · Supplier exploration"),
        code("import pandas as pd\nfrom pathlib import Path\np = Path('../data/exports/supplier_scorecard.csv')\nprint('Run the pipeline first' if not p.exists() else pd.read_csv(p).head())"),
    ],
    "04_otif_analysis.ipynb": [
        md("# 04 · OTIF\n\nOTIF = on or before promise and received ≥ ordered."),
        code("import pandas as pd\nfrom pathlib import Path\nfact = pd.read_csv('../data/processed/fact_purchase_orders.csv')\nprint(fact.otif_flag.mean())\nprint(fact.groupby('supplier_name').otif_flag.mean().sort_values().head())"),
    ],
    "05_quality_analysis.ipynb": [
        md("# 05 · Quality"),
        code("import pandas as pd\nfact = pd.read_csv('../data/processed/fact_purchase_orders.csv')\nprint((fact.defective_quantity.sum() / fact.received_quantity.sum()))\nprint(fact.groupby('supplier_name').apply(lambda d: d.defective_quantity.sum() / max(d.received_quantity.sum(), 1)).sort_values(ascending=False).head())"),
    ],
    "06_cost_analysis.ipynb": [
        md("# 06 · Cost variance\n\nStandard prices are simulated analytical inputs."),
        code("import pandas as pd\nfact = pd.read_csv('../data/processed/fact_purchase_orders.csv')\nprint(fact.actual_spend.sum() - fact.expected_spend.sum())\nprint(fact.groupby('supplier_name')[['actual_spend','expected_spend']].sum().assign(var=lambda d: d.actual_spend-d.expected_spend).sort_values('var', ascending=False).head())"),
    ],
    "07_supplier_scorecard.ipynb": [
        md("# 07 · Scorecard"),
        code("import pandas as pd\npd.read_csv('../data/exports/supplier_scorecard.csv')[['supplier_name','otif_pct','defect_rate','weighted_score','supplier_rank','risk_band']].head(12)"),
    ],
    "08_root_cause_analysis.ipynb": [
        md("# 08 · Root cause\n\nWorst scorecard supplier, 5-Why and fishbone."),
        code("import json\nfrom pathlib import Path\ndata = json.loads(Path('../web/public/data/dashboard.json').read_text())\nprint(data['rca']['supplier']['supplier_name'])\nfor step in data['rca']['five_why']:\n    print(step['level'], step['statement'][:180])"),
    ],
}

if __name__ == "__main__":
    NB.mkdir(exist_ok=True)
    for name, cells in NOTEBOOKS.items():
        (NB / name).write_text(json.dumps(nb(cells), indent=1), encoding="utf-8")
        print("wrote", name)
