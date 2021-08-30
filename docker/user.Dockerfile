FROM python:3.8.5-slim
WORKDIR /usr/src/app
COPY user.txt ./
RUN pip install --no-cache-dir -r user.txt
COPY ./fullchain.pem ./privkey.pem ./
COPY ./microservices/user.py ./microservices/models.py ./microservices/invokes.py ./microservices/password.py ./.env ./
CMD [ "python", "./user.py" ]