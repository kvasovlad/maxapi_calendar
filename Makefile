example:
	python example_bot.py

.PHONY: build publish

build:
	python -m build

publish:
	python -m twine upload dist/*
