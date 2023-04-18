FROM --platform=linux/amd64 python:3.9

RUN apt-get update
RUN apt-get install -y --no-install-recommends nginx supervisor
RUN pip3 install uwsgi

# Install application requirements
COPY ./requirements.txt /project/requirements.txt
RUN pip3 install -r /project/requirements.txt

RUN useradd --no-create-home nginx
RUN rm -r /root/.cache

# Configure Nginx
COPY nginx.conf /etc/nginx/
COPY nginx-app.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/

# install code
COPY . /project
WORKDIR /project

CMD ["/usr/bin/supervisord"]
