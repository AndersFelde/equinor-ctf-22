# sudo docker build -t limbo .
# sudo docker run -d -p 1024:1024 --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --rm -v ~/somedir:/somedir -it limbo

FROM ubuntu:22.04

RUN useradd -d /home/ept/ -m -p ept -s /bin/bash ept
RUN echo "ept:ept" | chpasswd

WORKDIR /home/ept

COPY ynetd .
COPY flag.txt /opt/flag
COPY limbo .
COPY limbo.ans .

RUN chown -R root:root /home/ept
RUN chmod  -R a+rx /home/ept
USER ept
CMD ./ynetd ./limbo
