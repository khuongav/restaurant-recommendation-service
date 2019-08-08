FROM python:3
MAINTAINER khuongav
    
RUN mkdir /source
ADD requirements.txt /source/requirements.txt
RUN pip install -r /source/requirements.txt

ADD . /source
WORKDIR /source

CMD ./scripts/run-service.sh