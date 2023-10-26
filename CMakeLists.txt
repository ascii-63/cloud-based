project(cloud-based)

set(CMAKE_CXX_STANDARD 11)
cmake_minimum_required(VERSION 3.12...3.18)

include_directories(
    ./include
)

set(AMQP_LIB_SRC ./include/amqp_connection.cpp)
add_library(amqp_lib SHARED ${AMQP_LIB_SRC})
target_link_libraries(amqp_lib
    rabbitmq
)

set(DB_LIB_SRC ./include/database.cpp)
add_library(db_lib SHARED ${AMQP_LIB_SRC})
target_link_libraries(db_lib
    amqp_lib
    rabbitmq
)

add_executable(receive_cloud ./test/receive_cloud.cpp)
target_link_libraries(receive_cloud rabbitmq)

add_executable(send_cloud ./test/send_cloud.cpp)
target_link_libraries(send_cloud rabbitmq)

# #Sample source
# add_executable(test ./test/test.cpp)
# target_link_libraries(
# test
# rabbitmq
# amqp_lib
# )

add_executable(ML_engine_sim ./test/ML_engine_sim.cpp)
target_link_libraries(
    ML_engine_sim
    rabbitmq
    amqp_lib
)

add_executable(event_transfer event_transfer.cpp)
target_link_libraries(
    event_transfer
    rabbitmq
    amqp_lib
)

add_executable(event_storage event_storage.cpp)
target_link_libraries(
    event_storage
    rabbitmq
    amqp_lib
    db_lib
)