#include "amqp_connection.h"

AMQP_Connection local_client;

void setup()
{
    std::string path = std::string(get_current_dir_name());
    path = path + "/../test/.env";
    local_client.parser(path);

    std::cout << local_client.amqp_url << std::endl
              << local_client.hostname << std::endl
              << local_client.username << std::endl
              << local_client.password << std::endl
              << local_client.vhost << std::endl
              << local_client.k_channel << std::endl
              << local_client.queue_name_str << std::endl;
}

int main(int argc, const char *argv[])
{
    if (argc <= 1)
    {
        std::cerr << "No argument." << std::endl;
        return -1;
    }

    setup();
    int8_t connection_status = local_client.connect();
    if (connection_status != EXIT_CODE::EXIT_OK)
        return -1;

    std::string message = std::string(argv[1]);
    if (local_client.send(message))
        std::cout << "[x] Sended: " << message << std::endl;

    // int counter = 0;
    // for (;;)
    // {
    //     std::string message;
    //     message = "Message #" + std::to_string(counter);
    //     if (local_client.send(message))
    //         std::cout << "Sended: " << message << std::endl;

    //     message.clear();
    //     counter++;
    // }

    return 0;
}