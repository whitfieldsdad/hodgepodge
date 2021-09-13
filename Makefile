all: clean test code-coverage build

clean:
	rm -rf dist

update-dependencies:
	poetry update
	poetry export -f requirements.txt -o requirements.txt --without-hashes
	poetry show --tree

 test:
	poetry run coverage run -m pytest

code-coverage:
	poetry run coverage report

install:
	poetry install

build: test
	poetry build

release: build
	poetry publish
