#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on debian
FROM kartoza/django-base:3.7
MAINTAINER Tim Sutton<tim@kartoza.com>

#RUN  ln -s /bin/true /sbin/initctl

# Pandoc needed to generate rst dumps, uic compressor needed for django-pipeline
RUN apt-get update -y; apt-get -y --force-yes install yui-compressor gettext
RUN wget https://github.com/jgm/pandoc/releases/download/1.17.1/pandoc-1.17.1-2-amd64.deb
RUN dpkg -i pandoc-1.17.1-2-amd64.deb && rm pandoc-1.17.1-2-amd64.deb

# Added because of issue with building cryptography.io using pip
# This flag disabled rust build, but only for this particular version
# In the future, we may have to include rust toolchain in the Dockerfile
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

ADD deployment/docker/REQUIREMENTS.txt /REQUIREMENTS.txt
ADD deployment/docker/uwsgi.conf /uwsgi.conf
ADD django_project /home/web/django_project
RUN pip install -r /REQUIREMENTS.txt
RUN pip install uwsgi


# Open port 8080 as we will be running our uwsgi socket on that
EXPOSE 8080

#USER www-data

WORKDIR /home/web/django_project
CMD ["uwsgi", "--ini", "/uwsgi.conf"]
