build:
	apt install python3.10
	pip3 install -r requirements.txt

run:
	uvicorn api:app --host 0.0.0.0 --port 8080