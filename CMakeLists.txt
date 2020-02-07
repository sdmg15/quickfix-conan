cmake_minimum_required(VERSION 3.5)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/")
project(cmake_wrapper)
include("conanbuildinfo.cmake")
conan_basic_setup()
add_subdirectory("source_subfolder")
