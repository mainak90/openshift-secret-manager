FROM mainak90/python-pip:1.2

USER root

RUN mkdir -p /app/manager

WORKDIR /app/manager

COPY . .

RUN chmod -R 777 /app/manager

RUN pip install -e .

USER 1000

CMD ["sh", "-c", "--namespace $NAMESPACE"