#include <iostream>
#include <string.h>

// #include <amqp.h>
// #include <amqp_tcp_socket.h>

#include <rabbitmq-c/amqp.h>
#include <rabbitmq-c/tcp_socket.h>

// #define THIS_AMQP_URL "amqps://slbnkadk:yjICj6LodkqaxgCG2rDIjvqJQ5Ihoo_u@gerbil.rmq.cloudamqp.com/slbnkadk"
// #define THIS_HOSTNAME "gerbil.rmq.cloudamqp.com"
// #define THIS_USERNAME "slbnkadk"
// #define THIS_PASSWORD "yjICj6LodkqaxgCG2rDIjvqJQ5Ihoo_u"
// #define THIS_VHOST "slbnkadk"

#define THIS_AMQP_URL "amqp://guest:guest@localhost/guest"
#define THIS_HOSTNAME "localhost"
#define THIS_USERNAME "guest"
#define THIS_PASSWORD "guest"
#define THIS_VHOST "/"

#define THIS_AMQP_PORT AMQP_PROTOCOL_PORT
#define QUEUE_NAME "default"

const char *amqp_url = THIS_AMQP_URL;
const char *amqp_hostname = THIS_HOSTNAME;
const char *amqp_queue_name = QUEUE_NAME;

const amqp_channel_t k_channel = 1;

enum EXIT_CODE
{
    SUCCESS = EXIT_SUCCESS,
    SOCKET_ERROR,
    LOGIN_ERROR,
    CHANNEL_ERROR,
};

void messageProcess(const std::string _message)
{
    if (_message.empty())
        return;
    std::cout << _message << std::endl;
}

int main(int argc, char const *const *argv)
{
    amqp_connection_state_t conn = amqp_new_connection(); // Create a new AMQP (Advanced Message Queuing Protocol) connection state
    amqp_socket_t *socket = amqp_tcp_socket_new(conn);    // Create a new TCP socket for the AMQP connection
    if (!socket)
    {
        std::cerr << "Failed to create new socket." << std::endl;
        return EXIT_CODE::SOCKET_ERROR;
    }

    int status = amqp_socket_open(socket, amqp_hostname, (int)THIS_AMQP_PORT); // Open a socket connection to the RabbitMQ server
    // if (status != AMQP_STATUS_OK)
    if (status)
    {
        std::cerr << "Failed to open socket with AMQP Host: " << status << std::endl;
        return EXIT_CODE::SOCKET_ERROR;
    }

    amqp_rpc_reply_t login_reply = amqp_login(conn, THIS_VHOST, 0, AMQP_DEFAULT_FRAME_SIZE, 0, AMQP_SASL_METHOD_PLAIN,
                                              THIS_USERNAME, THIS_PASSWORD); // Login into the RabbitMQ server
    if (login_reply.reply_type != AMQP_RESPONSE_NORMAL)
    {
        std::cerr << "Failed to login to AMQPCloud: " << login_reply.reply_type << std::endl;

        ///* Debug path */
        // if (login_reply.reply.id == AMQP_CHANNEL_CLOSE_METHOD)
        //     std::cerr << "AMQP_CHANNEL_CLOSE_METHOD" << std::endl;
        // else if (login_reply.reply.id == AMQP_CONNECTION_CLOSE_METHOD)
        // {
        //     std::cerr << "AMQP_CONNECTION_CLOSE_METHOD" << std::endl;
        //     amqp_connection_close_t *temp = (amqp_connection_close_t *)(login_reply.reply.decoded);

        //     int size = temp->reply_text.len;
        //     for (int i = 0; i < size; i++)
        //     {
        //         std::cout << (char)(temp->reply_text.len);
        //     }
        //     std::cout << std::endl;
        // }

        return EXIT_CODE::LOGIN_ERROR;
    }

    /**************************************/

    amqp_channel_open(conn, k_channel);
    amqp_rpc_reply_t channel_reply = amqp_get_rpc_reply(conn);
    if (channel_reply.reply_type != AMQP_RESPONSE_NORMAL)
    {
        std::cerr << "Failed to open channel: " << login_reply.reply_type << std::endl;
        return EXIT_CODE::CHANNEL_ERROR;
    }

    amqp_bytes_t queue_name(amqp_cstring_bytes(amqp_queue_name));
    amqp_queue_declare(conn, k_channel, queue_name, false, false, false, false, amqp_empty_table);
    amqp_basic_consume(conn, k_channel, queue_name, amqp_empty_bytes, false, true, false, amqp_empty_table);

    /**************************************/

    for (;;)
    {
        amqp_maybe_release_buffers(conn);

        amqp_envelope_t envelope;
        amqp_consume_message(conn, &envelope, nullptr, 0);

        std::string message = std::string((char *)envelope.message.body.bytes, (int)envelope.message.body.len);

        messageProcess(message);

        amqp_destroy_envelope(&envelope);
    }

    /**************************************/

    amqp_channel_close(conn, k_channel, AMQP_REPLY_SUCCESS);
    amqp_connection_close(conn, AMQP_REPLY_SUCCESS);
    amqp_destroy_connection(conn);

    return 0;
}