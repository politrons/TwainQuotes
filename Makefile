
# define the name of the virtual environment directory
VENV := venv

build: venv

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

venv: $(VENV)/bin/activate

test:
	python -m unittest discover

run:
	. venv/bin/activate
	cd app/resources/ && export FLASK_APP=server.py && flask run

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

