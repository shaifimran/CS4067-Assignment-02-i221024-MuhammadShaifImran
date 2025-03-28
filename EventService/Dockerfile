FROM python:3.12-alpine
WORKDIR /EventService
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=event_service.py
CMD ["flask", "run","--host=0.0.0.0", "--port=5000"]
