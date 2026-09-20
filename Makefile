.PHONY: help setup check check-archive lint test fmt new gallery check-gallery serve clean

# ------------------------------------------------------------
# Config
# ------------------------------------------------------------
UV ?= uv
# Every check runs through $(RUN). Override it to use an already-synced
# interpreter instead of uv, e.g. `make check RUN="env PATH=.venv/bin:$$PATH"`.
RUN ?= $(UV) run
# check-archive needs the pinned orbit-research; see pyproject.toml.
RUN_ARCHIVE ?= $(UV) run --extra research
export ASTROLABE_DATA_DIR := $(CURDIR)/_data/physics/astrolabe
# macOS: /tmp is a symlink; principia's record checkers refuse temp paths that
# resolve outside the owner root, so hand them the real temp directory.
export TMPDIR := $(shell python3 -c 'import os,tempfile;print(os.path.realpath(tempfile.gettempdir()))')

# ------------------------------------------------------------
# Help
# ------------------------------------------------------------
help:
	@echo "Observatory Make Targets"
	@echo ""
	@echo "  make setup          uv sync and the pre-commit hook"
	@echo "  make check          The gate: _scripts/check.py, ruff, pytest over _lib/"
	@echo "  make check-archive  principia's own checker over the frozen _archive/principia (not part of check)"
	@echo "  make new KIND=R TITLE=\"...\"   Allocate the next id and scaffold a record (KIND=Q|H|T|R)"
	@echo "  make lint           ruff"
	@echo "  make test           pytest over _lib/"
	@echo "  make fmt            ruff format"
	@echo "  make gallery        Regenerate _lib/gallery/index.html from every research/<R>/code/<sim>/sim.json"
	@echo "  make check-gallery  Fail if that catalogue is stale"
	@echo "  make serve [PORT=8000]   Static server at the repository root for the sims and chapters"
	@echo "  make clean          Remove caches (never touches data/ or output/)"

# ------------------------------------------------------------
# Setup
# ------------------------------------------------------------
setup:
	$(UV) sync
	$(UV) run pre-commit install

# ------------------------------------------------------------
# The gate
# ------------------------------------------------------------
check:
	$(RUN) python _scripts/check.py
	$(RUN) ruff check .
	$(RUN) pytest -q

# principia's lock, unchanged, over the frozen archive. Read-only and optional.
check-archive:
	$(RUN_ARCHIVE) ./_scripts/check-theory.sh

lint:
	$(RUN) ruff check .

fmt:
	$(RUN) ruff format .

test:
	$(RUN) pytest -q

# ------------------------------------------------------------
# Records
# ------------------------------------------------------------
new:
	./_scripts/new.sh --kind "$(KIND)" --title "$(TITLE)"

# ------------------------------------------------------------
# Sims
# ------------------------------------------------------------
gallery:
	$(RUN) python _lib/tools/build-gallery.py

check-gallery:
	$(RUN) python _lib/tools/build-gallery.py --check

# Serves the repository root so sims resolve ../../../../_lib/web.
serve:
	./_lib/tools/serve.sh $(PORT)

# ------------------------------------------------------------
# Clean
# ------------------------------------------------------------
clean:
	rm -rf .pytest_cache .ruff_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
