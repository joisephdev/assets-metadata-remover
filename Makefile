.PHONY: help build publish publish-test clean install uninstall test

help:
	@echo "Available targets:"
	@echo "  build          Build wheel and sdist"
	@echo "  publish        Upload to PyPI"
	@echo "  publish-test   Upload to TestPyPI"
	@echo "  clean          Remove build artifacts"
	@echo "  install        Install locally (editable)"
	@echo "  uninstall      Uninstall package"
	@echo "  test           Run smoke tests"

build: clean
	python3 -m build

publish: build
	twine upload dist/*

publish-test: build
	twine upload --repository testpypi dist/*

clean:
	rm -rf dist/ build/ src/*.egg-info

install:
	pip install -e .

uninstall:
	pip uninstall -y assets-metadata-remover

test:
	@echo "=== Smoke test ===" && assets-metadata-remover --help > /dev/null && echo "PASS"
	@echo "=== Clean dry run ===" && mkdir -p /tmp/mr_test/sub && assets-metadata-remover clean /tmp/mr_test --dry-run -v && echo "PASS"
	@echo "=== Read stub ===" && assets-metadata-remover read /tmp/mr_test && echo "PASS"
	@echo "=== All tests done ==="
