#!/bin/bash
cd "$(dirname "$0")"/..

DATASET_DIR="/data/dataset"

# Build environment
docker build -f ./test.Dockerfile -t tglang_test .

# Build libtglang-tester
docker run --rm -it -v `pwd`/../libtglang.so:/build/libtglang/libtglang.so -v `pwd`:/app tglang_test \
    bash -c "cd /app && mkdir -p build/libtglang-tester && cd build/libtglang-tester && cmake ../../libtglang-tester && make"

# Run testing script
docker run --rm -it -v `pwd`/../libtglang.so:/build/libtglang/libtglang.so \
    -v `pwd`/data:/data -v `pwd`:/app --cpus 8 tglang_test \
    bash -c "/app/scripts/tester.sh | tee /data/report/test_results.csv"

# Run analysis script
python ./scripts/analyse.py ./data/report/test_results.csv | tee ./data/report/test_results_analysis.txt