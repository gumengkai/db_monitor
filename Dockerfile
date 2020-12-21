FROM centos/python-36-centos7
 
USER root
 
run yum -y install libaio.x86_64
 
RUN mkdir /usr/src/app
 
COPY . /usr/src/app
 
WORKDIR /usr/src/app
 
RUN pip install -r requirements.txt --index-url https://pypi.doubanio.com/simple
 
ENV PYTHONOPTIMIZE=1
ENV LD_LIBRARY_PATH=/usr/src/app/soft/instantclient_19_5
 
EXPOSE 8000
