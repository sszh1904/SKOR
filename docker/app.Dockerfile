FROM python:3.8.5-slim
WORKDIR /usr/src/app
COPY app.txt ./
RUN pip install --no-cache-dir -r app.txt \
    && mkdir templates \
    && mkdir static
COPY ./microservices/app.py ./.env ./
COPY ./templates ./templates
COPY ./fullchain.pem ./privkey.pem ./
CMD [ "python", "./app.py" ]