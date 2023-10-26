#include "amqp_connection.h"

int main()
{
    AMQP_Connection test_connection;
    test_connection.parser();
    std::cout << test_connection.amqp_url << std::endl
              << test_connection.hostname << std::endl
              << test_connection.username << std::endl
              << test_connection.password << std::endl
              << test_connection.vhost << std::endl
              << test_connection.k_channel << std::endl
              << test_connection.queue_name_str << std::endl;

    std::cout << std::endl
              << std::string(get_current_dir_name()) << std::endl;
}