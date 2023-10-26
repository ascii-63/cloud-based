#ifndef AMQP_CONNECTION_H
#define AMQP_CONNECTION_H

#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <unistd.h>
#include <chrono>
#include <thread>

#include <rabbitmq-c/amqp.h>
#include <rabbitmq-c/tcp_socket.h>

#define PATH_TO_ENV_FILE "/home/pino/AIoT_ws/cloud-based/.env"

enum EXIT_CODE : int8_t
{
    EXIT_OK = EXIT_SUCCESS,
    SOCKET_ERROR,
    LOGIN_ERROR,
    CHANNEL_ERROR,
    QUEUE_ERROR,
};

// From std::string, return a pointer to char array
char *stringToCharPtr(const std::string _inp_str);

// Get variable in '_key' field from a map<string, string>, return in string 
std::string getVariableFromKey(const std::string _key,
                               const std::map<std::string, std::string> _var_map);

class AMQP_Connection
{
public:
    std::string amqp_url;
    std::string username;
    std::string password;
    std::string hostname;
    std::string vhost;
    int port;

    std::string queue_name_str;
    int k_channel;

private:
    amqp_connection_state_t conn; // AMQP connection
    amqp_socket_t *socket;        // TCP socket for AMQP connection
    amqp_bytes_t queue_name_amqp; // Queue name, in bytes

public:
    AMQP_Connection();  // Default constructor
    ~AMQP_Connection(); // Destructor

    bool parser();                                        // Parser, from URL to user, password, host, vhost and port, path: {current_dir}/../.env
    bool parser(const std::string _path_to_env_file);     // Parser, from URL to user, password, host, vhost and port.
    int8_t connect();                                     // Crete new AMQP connection, new TCP socket, open TCP socket, login, open channel and consume to queue.
    bool send(const std::string _message);                // Send a message.
    std::string receive();                                // Receive newest message from a queue.
    void close();                                         // Close channel, connection.
    bool configFileReader(std::string _path_to_env_file); // Read .env file to get AMQP_URL, CHANNEL, QUEUE
};

#endif