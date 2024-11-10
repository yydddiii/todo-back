FROM python:3.12-slim

COPY . .

RUN pip install -r lib.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

# docker build . --tag fastapi_app && docker run -p 80:80 fastapi_app