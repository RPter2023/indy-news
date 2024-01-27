FROM python:3.11
WORKDIR /app
COPY requirements-prod.txt /app/
RUN pip install -r requirements-prod.txt
COPY . /app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
EXPOSE 8080