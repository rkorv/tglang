FROM debian:10

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y g++ cmake make && \
    rm -rf /var/lib/apt/lists/*

