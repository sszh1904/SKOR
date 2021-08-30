FROM python:3.8.5-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN pip install --no-cache-dir -r http.reqs.txt
COPY ./fullchain.pem ./privkey.pem ./
COPY ./microservices/contactSkor.py ./microservices/invokes.py ./microservices/emailHandling.py ./.env ./
CMD [ "python", "./contactSkor.py" ]