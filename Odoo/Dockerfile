FROM nodered/node-red:latest

USER root

# Instalar Python y pip
RUN apk add --update python3 py3-pip

# Instalar el módulo cryptography
RUN pip3 install cryptography

USER node-red
