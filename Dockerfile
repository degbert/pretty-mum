FROM ubuntu:16.04

MAINTAINER David Egbert "dmegbert@us.ibm.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    pip install --upgrade pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt


EXPOSE 5000
EXPOSE 443
COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]

#docker run --name pretty-mum --rm -P -v /Users/degbert/PycharmProjects/pretty-mum:/app pretty_mum
#docker run --name pretty-mum --rm -P pretty_mum
#sudo docker run --name flask_cd --rm -p 5000:5000 --env-file vertica.list flask &>/dev/null &