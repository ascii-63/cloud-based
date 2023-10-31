cmake_minimum_required(VERSION 3.9)
project(test)

find_package(cpprestsdk REQUIRED)

add_executable(test test.cpp)
target_link_libraries(test PRIVATE cpprestsdk::cpprest)