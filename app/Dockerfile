FROM python:3.10.4

WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000


#RUN python services/generate_secret.py


CMD ["uvicorn", "main:app", "--proxy-headers", "--forwarded-allow-ips", "*", "--host", "0.0.0.0", "--port", "5000"]

