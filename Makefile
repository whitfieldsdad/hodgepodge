default: clean requirements.txt

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "._*" -delete

requirements.txt:
	poetry export -f requirements.txt --without-hashes > requirements.txt

test:
	poetry run python3 -m unittest discover -s tests -p "*.py"
	poetry run python3 -m coverage report
	poetry run python3 -m coverage html

.PHONY: default clean requirements.txt
