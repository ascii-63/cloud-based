/*
    Receive event logs from RabbitMQ server on localhost,
    then tranfer it to RabbitMQ server on AMQP-Cloud
*/

#include "amqp_connection.h"

AMQP_Connection local_consumer;
AMQP_Connection cloud_provider;

bool localConsumerSetup()
{
    local_consumer.hostname = "localhost";
    local_consumer.username = "guest";
    local_consumer.password = "guest";
    local_consumer.vhost = "/";
    local_consumer.k_channel = 1;
    local_consumer.queue_name_str = "event";

    int8_t connect_result = local_consumer.connect();
    if (connect_result != EXIT_CODE::EXIT_OK)
    {
        std::cerr << "Failed to setup local consumer." << std::endl;
        return false;
    }

    return true;
}

bool cloudProviderSetup()
{
    bool result = cloud_provider.parser();
    if (!result)
    {
        std::cerr << "Failed to setup cloud provider." << std::endl;
        return false;
    }

    int8_t connect_result = cloud_provider.connect();
    if (connect_result != EXIT_CODE::EXIT_OK)
    {
        std::cerr << "Failed to setup cloud provider." << std::endl;
        return false;
    }

    return true;
}

int main()
{
    if (!localConsumerSetup() || !cloudProviderSetup())
        return -1;
    std::cout << "Ready to tranfer message!" << std::endl
              << std::endl;

    for (;;)
    {
        std::string message = local_consumer.receive();
        std::cout << "Received: " << message << std::endl;
        if (!cloud_provider.send(message))
        {
            std::cerr << "Failed to transfer an event message." << std::endl;
            continue;
        }
        std::cout << "[x] Sended: " << message << std::endl
                  << std::endl;
    }

    return 0;
}