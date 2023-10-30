cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

project(tglang VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

set(CMAKE_CXX_FLAGS "-O3")

include_directories(/data/model) # for tflite model

include_directories(/build/tensorflow_src)
include_directories(/build/tflite_build/flatbuffers/include/)

set(LIB_SOURCES
    tglang.cpp
)

add_library(tglang SHARED ${LIB_SOURCES})

set(TFLITE_ROOT /build/tflite_build)

target_link_libraries(tglang
    dl
    ${TFLITE_ROOT}/tensorflow-lite/libtensorflow-lite.a
    ${TFLITE_ROOT}/_deps/fft2d-build/libfft2d_fftsg.a
    ${TFLITE_ROOT}/_deps/fft2d-build/libfft2d_fftsg2d.a
    ${TFLITE_ROOT}/_deps/flatbuffers-build/libflatbuffers.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_ctx.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_allocator.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_frontend.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_context_get_ctx.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_context.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_apply_multiplier.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_prepacked_cache.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_tune.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_cpuinfo.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_system_aligned_alloc.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_prepare_packed_matrices.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_trmul.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_block_map.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_denormal.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_thread_pool.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_blocking_counter.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_wait.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_kernel_avx.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_kernel_avx2_fma.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_kernel_avx512.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_pack_avx.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_pack_avx2_fma.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_pack_avx512.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_have_built_path_for_avx.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_have_built_path_for_avx2_fma.a
    ${TFLITE_ROOT}/_deps/ruy-build/ruy/libruy_have_built_path_for_avx512.a
    ${TFLITE_ROOT}/_deps/farmhash-build/libfarmhash.a
    ${TFLITE_ROOT}/_deps/xnnpack-build/libXNNPACK.a
    ${TFLITE_ROOT}/_deps/cpuinfo-build/libcpuinfo.a
    ${TFLITE_ROOT}/pthreadpool/libpthreadpool.a
)
