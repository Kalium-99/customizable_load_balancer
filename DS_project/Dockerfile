FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask
ENV SERVER_ID=1
CMD ["python", "server.py", "load_balancer.py"]
