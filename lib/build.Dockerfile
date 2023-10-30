FROM debian:10

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y g++ wget make git libssl-dev xxd && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Build CMake (required for tensorflow)
RUN cd /build/ && wget https://github.com/Kitware/CMake/releases/download/v3.18.3/cmake-3.18.3.tar.gz && \
    tar -xvf cmake-3.18.3.tar.gz && \
    cd cmake-3.18.3 && \
    ./bootstrap && \
    make -j && \
    make install

# Build TensorFlow Lite from source
RUN git clone https://github.com/tensorflow/tensorflow.git tensorflow_src && \
    cd tensorflow_src && \
    git checkout v2.14.0

RUN mkdir tflite_build && \
    cd tflite_build && \
    cmake ../tensorflow_src/tensorflow/lite/c && \
    cmake --build . -j
