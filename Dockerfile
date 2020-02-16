FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /

# Installing gcc, g++ and libffi is needed for package bcrypt
# deleting libre-ssl and installing openssl is needed for package cryptography
# and make is needed for installing package PyNaCl
RUN apk update & apk upgrade \
    # && apk del libressl-dev \ 
    # && apk add gcc g++ libffi-dev openssl-dev make \
    && pip3 install -r requirements.txt \
    && mkdir /code 

COPY . /code/

WORKDIR /code