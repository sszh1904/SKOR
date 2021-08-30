FROM python:3.8.5-slim
WORKDIR /usr/src/app
COPY user.txt ./
RUN pip install --no-cache-dir -r user.txt
COPY ./fullchain.pem ./privkey.pem ./
COPY ./microservices/account.py ./microservices/invokes.py ./microservices/password.py ./microservices/emailHandling.py ./.env ./
CMD [ "python", "./account.py" ]