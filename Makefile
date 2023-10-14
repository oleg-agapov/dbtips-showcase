.PHONY: dbt-dev dbt-dev-docker

dbt-dev:
	rm -rf venv
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

dbt-docker:
	docker build --tag dbt-service .
	docker run -it --rm \
    	--network=host \
    	-v $(PWD):/app \
    	--entrypoint=bash \
    	dbt-service
