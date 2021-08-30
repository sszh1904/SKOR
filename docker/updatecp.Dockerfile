FROM python:3.8.5-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN pip install --no-cache-dir -r http.reqs.txt
COPY ./fullchain.pem ./privkey.pem ./
COPY ./microservices/updateCP.py ./microservices/invokes.py ./.env ./
CMD [ "python", "./updateCP.py" ]