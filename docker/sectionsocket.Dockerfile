FROM python:3.8.5-slim
WORKDIR /usr/src/app
COPY socket.txt ./
RUN pip install --no-cache-dir -r socket.txt
COPY ./fullchain.pem ./privkey.pem ./
COPY ./microservices/sectionSocket.py ./.env ./
CMD [ "python", "./sectionSocket.py" ]