VENV := .venv
PYTHON := $(VENV)/bin/python
NOTEBOOK_DIR ?= notebooks
KERNEL_NAME ?= parallax
JUPYTER_ARGS ?=
TRENDS_FILE ?= data/R03-consumer-goods/inbox/google-trends/wearable-health.csv
CONSUMER_GOODS_ARGS ?=

.PHONY: notebook consumer-goods-import
notebook:
	@test -x "$(PYTHON)" || (echo "Missing $(PYTHON); run: uv sync --group notebook" && exit 1)
	@$(PYTHON) -c "import ipykernel, notebook" || \
		(echo "Notebook dependencies are missing; run: uv sync --group notebook" && exit 1)
	@$(PYTHON) -m ipykernel install --prefix "$(VENV)" --name "$(KERNEL_NAME)" \
		--display-name "Python (parallax)"
	@$(PYTHON) -m jupyter notebook --notebook-dir "$(NOTEBOOK_DIR)" $(JUPYTER_ARGS)

consumer-goods-import:
	@test -x "$(PYTHON)" || (echo "Missing $(PYTHON); run: uv sync" && exit 1)
	@$(PYTHON) -m parallax.cli consumer-goods import-history \
		--google-trends-file "$(TRENDS_FILE)" $(CONSUMER_GOODS_ARGS)
