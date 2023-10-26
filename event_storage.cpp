/*
    Receive event logs from RabbitMQ server on AMQP-Cloud,
    Display, and store it into PostgreSQL Database
*/

#include "amqp_connection.h"
#include "database.h"

#include <vector>

AMQP_Connection cloud_consumer;

std::vector<std::string> event_vector;
std::map<std::string, std::string> event_timestamp_map;

bool cloudConsumerSetup()
{
    bool result = cloud_consumer.parser();
    if (!result)
    {
        std::cerr << "Failed to setup cloud consumer." << std::endl;
        return false;
    }

    int8_t connect_result = cloud_consumer.connect();
    if (connect_result != EXIT_CODE::EXIT_OK)
    {
        std::cerr << "Failed to setup cloud consumer." << std::endl;
        return false;
    }

    return true;
}

std::string getTimestampFromEventLog(const std::string _logs)
{
    std::string timestamp;
    return timestamp;
}

void eventListener()
{
    for (;;)
    {
        std::string newest_message;
        newest_message = cloud_consumer.receive();
        if (newest_message.empty())
            continue;
        std::cout << newest_message << std::endl
                  << std::endl;

        event_vector.push_back(newest_message);

        // std::string timestamp = getTimestampFromEventLog(newest_message);
        // event_timestamp_map[timestamp] = newest_message;
    }
}

int main()
{
    if (!cloudConsumerSetup())
        return -1;
    std::cout << "Ready to receive event logs!" << std::endl
              << std::endl;

    eventListener();

    return 0;
}
