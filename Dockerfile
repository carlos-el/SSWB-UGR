FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /

# Installing gcc, g++ and libffi is needed for package bcrypt
# deleting libre-ssl and installing openssl is needed for package cryptography
# and make is needed for installing package PyNaCl
# installing zlib-dev, jpeg-dev, build.deps, build-base and linux-headers is needed for Pillow
RUN apk update & apk upgrade \
    # && apk del libressl-dev \ 
    # && apk add gcc g++ libffi-dev openssl-dev make \
    && apk add --no-cache jpeg-dev zlib-dev \
    && apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip3 install -r requirements.txt \
    && mkdir /code 

COPY . /code/

WORKDIR /code