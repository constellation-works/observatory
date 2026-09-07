.PHONY: help setup check check-lineage check-theory check-records check-layout check-gallery lint test experiment fmt clean

# ------------------------------------------------------------
# Config
# ------------------------------------------------------------
UV ?= uv
NEB ?= neb
export NEBULA_ROOT := $(CURDIR)/knowledgebase/lineage
THEORY := knowledgebase/theory
# macOS: /tmp is a symlink; the record checkers refuse temp paths that resolve outside
# the owner root, so hand them the real temp directory.
export TMPDIR := $(shell python3 -c 'import os,tempfile;print(os.path.realpath(tempfile.gettempdir()))')

# ------------------------------------------------------------
# Help
# ------------------------------------------------------------
help:
	@echo "Observatory Make Targets"
	@echo ""
	@echo "  make setup          uv sync, pre-commit hook, verify neb finds the corpus"
	@echo "  make check          Full gate: lineage + theory + layout + lint + tests"
	@echo "  make check-lineage  neb check over knowledgebase/lineage"
	@echo "  make check-theory   principia's lock over knowledgebase/theory"
	@echo "  make check-records  immutable research records under knowledgebase/theory/research"
	@echo "  make check-layout   experiments and studies keyed by node id; no data in git"
	@echo "  make check-gallery  orrery sim catalog (experiments/physics/_orrery/lab/gallery) is current"
	@echo "  make lint           ruff"
	@echo "  make test           pytest"
	@echo "  make experiment DOMAIN=<d> ID=<node-id>   Scaffold experiments/<d>/<id>/ from the template"
	@echo "  make fmt            ruff format"
	@echo "  make clean          Remove caches (never touches _data or _outputs)"

# ------------------------------------------------------------
# Setup
# ------------------------------------------------------------
setup:
	$(UV) sync
	$(UV) run pre-commit install
	@$(NEB) check >/dev/null && echo "neb sees the corpus at $(NEBULA_ROOT)"

# ------------------------------------------------------------
# Quality
# ------------------------------------------------------------
check: check-lineage check-theory check-records check-layout check-gallery lint test

check-lineage:
	$(NEB) check

# principia's lock: claim registry, ledger, links to studies and orrery sims.
check-theory:
	$(UV) run --extra research ./_scripts/check-theory.sh

# The immutable research records under $(THEORY)/research; needs the pinned orbit-research.
check-records:
	cd $(THEORY) && $(UV) run --extra research python scripts/corpus_records.py check
	cd $(THEORY) && $(UV) run --extra research python scripts/wide_binary_records.py check

check-layout:
	./_scripts/check-layout.sh

# orrery's generated sim catalog must match lab/sims.
check-gallery:
	$(UV) run python experiments/physics/_orrery/lab/tools/build-gallery.py --check

lint:
	$(UV) run ruff check .

fmt:
	$(UV) run ruff format .

test:
	$(UV) run --extra research pytest -q

# ------------------------------------------------------------
# Scaffold
# ------------------------------------------------------------
experiment:
	./_scripts/new-experiment.sh "$(DOMAIN)" "$(ID)"

# ------------------------------------------------------------
# Clean
# ------------------------------------------------------------
clean:
	rm -rf .pytest_cache .ruff_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
