#include "amqp_connection.h"

char *stringToCharPtr(const std::string _inp_str)
{
    const char *temp = _inp_str.c_str();
    char *result = new char[_inp_str.size() + 1];
    char character = *temp;
    int index = 0;
    while (character != '\0')
    {
        character = *(temp + index);
        *(result + index) = character;
        index++;
    }
    return result;
}

std::string getVariableFromKey(std::string _key,
                               std::map<std::string, std::string> _var_map)
{
    std::string result = "";
    if (_var_map.find(_key) != _var_map.end())
        result = _var_map[_key];

    return result;
}

/*******************************************************************************/

AMQP_Connection::AMQP_Connection() : port(AMQP_PROTOCOL_PORT)
{
}

AMQP_Connection::~AMQP_Connection()
{
}

bool AMQP_Connection::parser(const std::string _path_to_env_file)
{
    if (!configFileReader(_path_to_env_file))
    {
        std::cerr << "Failed to read .env file." << std::endl;
        return false;
    }

    char *char_url = stringToCharPtr(amqp_url);
    amqp_connection_info info;
    int result = amqp_parse_url(char_url, &info);
    if (result != AMQP_STATUS_OK)
    {
        std::cerr << "Parsing failed." << std::endl;
        return false;
    }

    username = std::string(info.user);
    password = std::string(info.password);
    hostname = std::string(info.host);
    vhost = std::string(info.vhost);

    // Exception:
    if (hostname == "localhost")
        vhost = "/";

    return true;
}

bool AMQP_Connection::parser()
{
    std::string default_path = std::string(get_current_dir_name()) + "/../.env";

    if (!configFileReader(default_path))
    {
        std::cerr << "Failed to read .env file." << std::endl;
        return false;
    }

    char *char_url = stringToCharPtr(amqp_url);
    amqp_connection_info info;
    int result = amqp_parse_url(char_url, &info);
    if (result != AMQP_STATUS_OK)
    {
        std::cerr << "Parsing failed." << std::endl;
        return false;
    }

    username = std::string(info.user);
    password = std::string(info.password);
    hostname = std::string(info.host);
    vhost = std::string(info.vhost);

    // Exception:
    if (hostname == "localhost")
        vhost = "/";

    return true;
}

int8_t AMQP_Connection::connect()
{
    conn = amqp_new_connection();       // Create a new AMQP connection state
    socket = amqp_tcp_socket_new(conn); // Create a new TCP socket for the AMQP connection
    if (!socket)
    {
        std::cerr << "Failed to create new socket." << std::endl;
        return EXIT_CODE::SOCKET_ERROR;
    }

    int status = amqp_socket_open(socket, hostname.c_str(), (int)port); // Open a socket connection to the RabbitMQ server
    if (status)
    {
        std::cerr << "Failed to open socket with AMQP Host: " << status << std::endl;
        return EXIT_CODE::SOCKET_ERROR;
    }

    /*****************************/

    amqp_rpc_reply_t login_reply = amqp_login(conn, vhost.c_str(), 0, AMQP_DEFAULT_FRAME_SIZE, 0, AMQP_SASL_METHOD_PLAIN,
                                              username.c_str(), password.c_str()); // Login into the RabbitMQ server
    if (login_reply.reply_type != AMQP_RESPONSE_NORMAL)
    {
        std::cerr << "Failed to login to AMQPCloud: " << login_reply.reply_type << std::endl;
        return EXIT_CODE::LOGIN_ERROR;
    }

    /****************************/

    amqp_channel_open(conn, k_channel);
    amqp_rpc_reply_t channel_reply = amqp_get_rpc_reply(conn);
    if (channel_reply.reply_type != AMQP_RESPONSE_NORMAL)
    {
        std::cerr << "Failed to open channel: " << login_reply.reply_type << std::endl;
        return EXIT_CODE::CHANNEL_ERROR;
    }

    /****************************/

    queue_name_amqp = amqp_bytes_t(amqp_cstring_bytes(queue_name_str.c_str()));
    amqp_queue_declare(conn, k_channel, queue_name_amqp, false, false, false, false, amqp_empty_table);
    amqp_basic_consume(conn, k_channel, queue_name_amqp, amqp_empty_bytes, false, true, false, amqp_empty_table);

    /****************************/

    std::cout << "Connect to RabbitMQ Server successful." << std::endl;
    return EXIT_CODE::EXIT_OK;
}

bool AMQP_Connection::send(const std::string _message)
{
    const char *msg_c_str = _message.c_str();
    int result = amqp_basic_publish(conn, k_channel, amqp_empty_bytes, queue_name_amqp, false, false, nullptr, amqp_cstring_bytes(msg_c_str));
    if (result != AMQP_STATUS_OK)
    {
        std::cerr << "Failed to send message to RabbitMQ server." << std::endl;
        return false;
    }
    return true;
}

std::string AMQP_Connection::receive()
{
    amqp_maybe_release_buffers(conn);
    amqp_envelope_t envelope;
    amqp_consume_message(conn, &envelope, nullptr, 0);
    std::string message = std::string((char *)envelope.message.body.bytes, (int)envelope.message.body.len);
    amqp_destroy_envelope(&envelope);

    return message;

    /***********************************/

    // amqp_frame_t frame;
    // int result = amqp_simple_wait_frame(conn, &frame);

    // if (result < 0)
    // {
    //     // Handle frame wait error
    // }

    // if (frame.frame_type != AMQP_FRAME_METHOD)
    // {
    //     return "";
    // }

    // if (frame.payload.method.id == AMQP_BASIC_DELIVER_METHOD)
    // {
    //     amqp_basic_deliver_t *delivery = (amqp_basic_deliver_t *)frame.payload.method.decoded;
    //     amqp_basic_get(conn, 1, amqp_cstring_bytes(queue_name_str.c_str()), 1);
    //     amqp_frame_t message_frame;
    //     amqp_basic_get_ok_t *get_ok;
    //     result = amqp_simple_wait_frame(conn, &message_frame);

    //     if (result < 0)
    //     {
    //         // Handle message receive error
    //     }

    //     if (message_frame.frame_type != AMQP_FRAME_METHOD)
    //     {
    //         return "";
    //     }

    //     if (message_frame.payload.method.id == AMQP_BASIC_GET_OK_METHOD)
    //     {
    //         get_ok = (amqp_basic_get_ok_t *)message_frame.payload.method.decoded;
    //         // Process the message here
            
    //     }

    //     // amqp_destroy_envelope(&envelope);
    // }
}

void AMQP_Connection::close()
{
    amqp_channel_close(conn, k_channel, AMQP_REPLY_SUCCESS);
    amqp_connection_close(conn, AMQP_REPLY_SUCCESS);
    amqp_destroy_connection(conn);
}

bool AMQP_Connection::configFileReader(std::string _path_to_env_file)
{
    std::ifstream env_file(_path_to_env_file);
    std::map<std::string, std::string> env_variables;

    if (!env_file.is_open())
    {
        std::cerr << "Failed to open .env file" << std::endl;
        return false;
    }

    std::string line;
    while (std::getline(env_file, line))
    {
        size_t equalsPos = line.find('=');
        if (equalsPos != std::string::npos)
        {
            std::string key = line.substr(0, equalsPos);
            std::string value = line.substr(equalsPos + 1);
            env_variables[key] = value;
        }
    }
    env_file.close();

    /*************************************/

    amqp_url = getVariableFromKey("AMQP_URL", env_variables);

    if (amqp_url.size() == 0)
    {
        std::cerr << "Cannot get AMQP_URL from .env file." << std::endl;
        return false;
    }

    k_channel = std::stoi(getVariableFromKey("CHANNEL", env_variables));
    if (k_channel == 0)
    {
        std::cerr << "Cannot get CHANNEL from .env file." << std::endl;
        return false;
    }

    queue_name_str = getVariableFromKey("QUEUE", env_variables);
    if (queue_name_str.size() == 0)
    {
        std::cerr << "Cannot get QUEUE from .env file." << std::endl;
        return false;
    }

    return true;
}