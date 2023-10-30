cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

project(libtglang-tester VERSION 1.0.0 LANGUAGES C)

add_executable(libtglang-tester tglang-tester.c)

# find_library(tglang_LIBRARY tglang PATHS "${CMAKE_CURRENT_SOURCE_DIR}" NO_DEFAULT_PATH)
# target_link_libraries(libtglang-tester PRIVATE "${tglang_LIBRARY}")

target_link_libraries(libtglang-tester PRIVATE /build/libtglang/libtglang.so)
target_link_libraries(libtglang-tester PRIVATE m)
target_link_libraries(libtglang-tester PRIVATE rt)

# if (NOT WIN32)
#   if (UNIX AND NOT APPLE)
#   endif()
# else()
#   add_definitions(-D_CRT_SECURE_NO_WARNINGS)
# endif()
