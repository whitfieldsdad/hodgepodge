all: clean build test

clean:
	rm -rf dist

update:
	poetry show -o
	poetry update
	poetry export -f requirements.txt -o requirements.txt --without-hashes
	poetry show --tree

test:
	poetry run coverage run -m pytest --durations=0

install:
	poetry install

build:
	poetry build

release: build test
	poetry publish
