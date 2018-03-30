FROM ubuntu:latest

WORKDIR /user/home
RUN apt-get update
RUN apt-get install -y python3

COPY run.sh /user/home/run.sh
COPY run_sol.sh /user/home/run_sol.sh
