.PHONY: dev run test check clean db
.DEFAULT: help
-include .env

help: ## Display this help message
	@echo "Please use \`make <target>\` where <target> is one of"
	@awk -F ':.*?## ' '/^[a-zA-Z]/ && NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: ## Remove general artifact files
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '__pycache__' -type d | xargs rm -rf
	rm -f uv.lock

uv-init: ## Initialize uv project if not done
	uv init --app

install: ## Install dependencies from pyproject.toml / lockfile
	uv sync --frozen 

update-req: ## Add/update dependencies interactively (use uv add/remove)
	@echo "Use \`uv add <package>\` or \`uv remove <package>\` to update dependencies."
	@echo "Then run \`make install\` to sync."

run: install ## Run with dev dependencies
	uv run -- python -m streamlit run src/main.py 

