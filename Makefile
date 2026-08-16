.PHONY: test isolation doctor public verify

PYTHON ?= python3

test:
	$(PYTHON) -m pytest tests -q --ignore=artifacts

isolation:
	$(PYTHON) -c "from ux_app.isolation import scan_imports; hits = scan_imports(); \
print('\n'.join(hits)); raise SystemExit(1 if hits else 0)"

public:
	$(PYTHON) -c "from ux_app.isolation import scan_public_names; hits = scan_public_names(); \
print('\n'.join(hits)); raise SystemExit(1 if hits else 0)"

doctor:
	$(PYTHON) -m ux_app doctor --fail

verify: test isolation public doctor
	@echo verify: ok
