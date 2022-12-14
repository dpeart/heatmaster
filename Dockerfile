FROM ubuntu:latest 

ARG USERNAME=heatmaster
ARG GNAME=users
ARG USER_UID=100
ARG USER_GID=100

RUN apt-get update 
RUN apt-get -y install sudo

#RUN addgroup --gid $USER_GID $GNAME
RUN adduser --home /home/$USERNAME $USERNAME --disabled-password
RUN adduser $USERNAME sudo

RUN echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get -y install curl
RUN apt-get -y install vim
RUN pip install flask
RUN pip install playwright

USER $USERNAME

RUN playwright install-deps
RUN playwright install chromium

WORKDIR /home/$USERNAME

ADD heatmaster.py /home/$USERNAME

EXPOSE 5000

CMD ["python3","heatmaster.py"]
