FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install docker flask
ENV SERVER_ID=0
CMD ["sh", "-c", "python load_balancer.py & python server.py"]
