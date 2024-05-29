install:
	pip install --no-cache  -r requirements.txt
server:
	uvicorn main:app --reload
clean:
	find . -type f -name "*.py[co]" -delete -o -type d -name "__pycache__" -delete
