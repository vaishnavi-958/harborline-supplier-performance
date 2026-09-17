PYTHON ?= python3
WEB_PORT ?= 43147

.PHONY: data pipeline test web install

install:
	$(PYTHON) -m pip install -r requirements.txt
	cd web && npm install

data:
	PYTHONPATH=. $(PYTHON) scripts/generate_data.py

pipeline:
	PYTHONPATH=. $(PYTHON) scripts/run_pipeline.py

test:
	PYTHONPATH=. $(PYTHON) -m pytest -q

web:
	cd web && npm run dev -- --port $(WEB_PORT) --hostname 127.0.0.1
