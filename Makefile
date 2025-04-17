include .env
export

.PHONY: \
	build \
	lint \
	format \
	test \
	install \
	uninstall \
	run \
	tree

build:
	@uv run pyinstaller --onefile --distpath bin --name main --icon ./assets/icon.icns --clean --noconfirm --hidden-import=dependency_injector.errors --hidden-import=aiosqlite main.py

lint:
	@uvx ruff check .

format:
	@uvx ruff format .

test:
	@pytest

install:
	@uv pip install -e .
	@uv pip install -e '.[dev]'

uninstall:
	@uv pip uninstall .

run:
	@uv run python main.py ./test.pdf

tree:
	@tree -I 'build|__pycache__|*.egg-info'