NAME=$(shell basename $(PWD))

PYTHON:=3.12

DOCKER=docker run \
	   --rm -it \
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
	uv run pytest --cov=nornir_napalm --cov-report=term-missing -vs ${ARGS} .
	uv run pytest --nbval -vs ${ARGS} docs/source/tutorials

.PHONY: format
format:
	uv run ruff format --check .

.PHONY: ruff
ruff:
	uv run ruff check .

.PHONY: mypy
mypy:
	uv run mypy .

.PHONY: tests
tests: format ruff mypy pytest
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
