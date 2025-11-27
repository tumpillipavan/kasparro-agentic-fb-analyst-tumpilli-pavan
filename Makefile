setup:
	python setup_project.py

run:
	python src/run.py "Analyze ROAS drop in last 7 days"

test:
	pytest -q
