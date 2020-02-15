NAME=$(shell basename $(PWD))

PYTHON:=3.7

DOCKER=docker run \
	   --rm -ir \
	   --name $(NAME)-tests \
	   -v $(PWD):/$(NAME) \
	   --rm $(NAME):latest

.PHONY: docker
docker:
	docker build \
	--build-arg PYTHON=$(PYTHON) \
	--build-arg NAME=$(NAME) \
	-t $(NAME):latest \
	-f Dockerfile \
	.

.PHONY: pytest
pytest:
	poetry run pytest -vs ${ARGS} .
	poetry run pytest --nbval -vs ${ARGS} docs/source/tutorials

.PHONY: black
black:
	poetry run black --check .

.PHONY: pylama
pylama:
	poetry run pylama .

.PHONY: mypy
mypy:
	poetry run mypy .

.PHONY: tests
tests: black pylama mypy pytest
.PHONY: docker-tests

.PHONY:docker-tests
docker-tests: docker
	$(DOCKER) make tests

.PHONY: jupyter
jupyter:
	docker run \
	--name $(NAME)-jupyter --rm \
	-v $(PWD):/$(NAME) \
	$(NAME):latest \
		jupyter notebook \
			--allow-root \
			--ip 0.0.0.0

.PHONY: docs
docs:
	make -C docs html
