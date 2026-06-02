PYTHON := python3
SCRIPT := metadata_remover.py
INPUT  ?= .
OUTPUT ?=

FLAGS :=
ifdef VERBOSE
  FLAGS += -v
endif
ifdef VERIFY
  FLAGS += --verify
endif
ifdef OUTPUT
  FLAGS += -o $(OUTPUT)
endif

.PHONY: help run dry-run verify test clean

help:
	@$(PYTHON) $(SCRIPT) --help

run:
	$(PYTHON) $(SCRIPT) $(INPUT) $(FLAGS)

dry-run:
	$(PYTHON) $(SCRIPT) $(INPUT) --dry-run $(FLAGS)

verify:
	$(PYTHON) $(SCRIPT) $(INPUT) --verify $(FLAGS)

test:
	@echo "=== Smoke test ===" && $(PYTHON) $(SCRIPT) --help > /dev/null && echo "PASS"
	@echo "=== Dry run ===" && mkdir -p /tmp/mr_test/sub && $(PYTHON) $(SCRIPT) /tmp/mr_test --dry-run -v && echo "PASS"
	@echo "=== Real run ===" && rm -rf /tmp/mr_test_clean && $(PYTHON) $(SCRIPT) /tmp/mr_test -v --verify && echo "PASS"
	@echo "=== Empty dir ===" && mkdir -p /tmp/mr_empty && $(PYTHON) $(SCRIPT) /tmp/mr_empty && echo "PASS"
	@echo "=== Non-existent ===" && $(PYTHON) $(SCRIPT) /tmp/mr_nonexistent 2>&1; echo "Exit: $$?"
	@echo "=== All tests done ==="

clean:
	rm -rf /tmp/mr_test /tmp/mr_test_clean /tmp/mr_empty /tmp/mr_empty_clean
