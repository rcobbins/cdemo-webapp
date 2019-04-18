FROM centos:centos7

RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum -y update
RUN yum -y install epel-release
RUN yum -y install gcc
RUN yum -y install python36 python36-devel python36-setuptools python36-libs python36-pip
RUN yum -y install postgresql-devel postgresql-lib

COPY ./src /app

RUN pip3 install -r /app/requirements.txt

EXPOSE 5000

CMD ["python3", "/app/app.py"]
