FROM python:3.12-alpine
LABEL authors="Hardstyle"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "-m", "flask", "--app", "main", "run", "--host=0.0.0.0"]