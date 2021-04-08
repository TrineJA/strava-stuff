PIPENV ?= PYTHONPATH=src pipenv run

get-data:
	$(PIPENV) python src/get_data.py

start-jupyter:
	$(PIPENV) jupyter contrib nbextension install && \
	pipenv run jupyter nbextensions_configurator enable && \
	pipenv run jupyter nbextension enable collapsible_headings/main && \
	pipenv run jupyter notebook

streamlit-local:
	$(PIPENV) streamlit run app/ride_viewer.py

heroku-local:
	$(PIPENV) heroku local web
