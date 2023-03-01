FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./ /app

ENV PYTHONPATH=$PYTHONPATH:/app

COPY ./app/start-reload.sh /
RUN chmod +x /start-reload.sh 

COPY ./app/start-docker.sh /
RUN chmod +x /start-docker.sh 


# RUN wget https://github.com/vishnubob/wait-for-it/blob/master/wait-for-it.sh && cp ./wait-for-it.sh /

# RUN mv /start-reload.sh /start-docker.sh && ls