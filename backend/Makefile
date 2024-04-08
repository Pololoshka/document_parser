install_pre_commit:
	pre-commit install
	pre-commit install --hook-type commit-msg
	pre-commit autoupdate

fix:
	ruff format src main.py tests
	ruff check --fix --show-fixes src main.py tests

check:
	ruff format --check src main.py tests
	ruff check src main.py tests
	mypy src main.py tests
	pytest tests
