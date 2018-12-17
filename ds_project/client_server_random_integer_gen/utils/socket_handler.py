"""
Module to handle sockets of both Client and Server.

Author: Varun Rao
UTA id: 1001681430

"""
import socket


class SocketHandler(object):

    def __init__(self, ip="127.0.0.1", port=12345):
        self.ip = ip
        self.port = port
        self.client = False
        self.server = False
        self.py_socket = None

    def create_client_socket(self):
        """
        Creates a client socket.

        steps:

        1.Creates a generic socket using socket.socket().
        2.Notes that a client socket is created by setting self.client to True

        :return:  None
        """
        self.py_socket = socket.socket()
        self.client = True


    def verify_if_client(self):
        """
        Verifies if client socket is created is created or not.

        steps:
        1.Checks if self.client is True. If False exception is raised

        :return: None
        """
        if not self.client:
            raise Exception("Client socket not created")

    def connect_to_server(self):
        """

        Function for a client socket to connect to a server.
        ip address and port must be specified while creating SocketHandler object.

        1)Function verifies if client socket is created.
        2)If yes function uses socket object's connect() to a server

        :return: None
        """
        self.verify_if_client()
        print("Client socket connecting to server")
        self.py_socket.connect((self.ip, self.port))

    def receive_message_from_server(self):
        """
        Gets message from server. Dedicated for client socket.

        1)uses socket object's recv() function to obtain.

        :return: string containing message from server
        """
        print("Fetching response...")
        message = self.py_socket.recv(2048)
        print(str(message))
        return str(message.decode("utf-8"))

    def send_message_to_server(self, message):
        """
        Function to send client message to server. Dedicated for client socket.

        1)Function uses send() of socket object.

        :param message: contains message string.

        :return: None
        """
        print("Sending message to server...")
        self.py_socket.send(message.encode())

    def terminate_socket(self):
        """

        Use to terminate both client or server socket.

        1)Uses close() function of socket object

        :return: None
        """
        if not self.client:
            print("Server socket terminating...")
        else:
            print("Client socket terminating...")
        self.py_socket.close()

    def create_server_socket(self):
        """

        Function to create a server socket and binds it to its ip.

        1)Creates socket object using socket() function of "socket" library.
        2)Bind the new socket to its ip using bind() of socket object.

        :return: None
        """
        self.server = True
        print("Creating Server socket...")
        self.py_socket = socket.socket()
        print("Binding socket")
        self.py_socket.bind(("", self.port))

    def listen_to_incoming_client_request(self, request_queue=5):
        """

        Function to listen to incoming client requests.

        1)verifies if server socket is created.
        2)uses listen() function of socket object.

        :param request_queue: number of incoming clients that are kept in queue. If exceeded, rest of the requests are
                discarded
        :return: None
        """
        self._verify_if_server()
        print("Server listening to incoming client requests")
        self.py_socket.listen(request_queue)

    def accept_incoming_client_request(self):
        """
        Accepts the request from the client. One at a time.

        1)Verifies if server socket is created.
        2)uses accept() function of socket object to accept
        :return: tuple containing client object and client address string
        """
        self._verify_if_server()
        client_obj, client_addr = self.py_socket.accept()
        print("Client request accepted from {}".format(client_addr))
        return client_obj, client_addr

    @staticmethod
    def terminate_client_connection(client_obj, client_addr=""):
        """
        Static function that terminates server socket connection with a client socket.

        1)use close() function of client object.

        :param client_obj: client object.
        :param client_addr: string containing client address.
        :return: None
        """
        print("Terminating connection with client {}".format(client_addr))
        client_obj.close()

    @staticmethod
    def send_message_to_client(message, client_obj, client_addr=""):
        """

        Static function to send server message to client.

        1)uses send() of client object to send message to client.

        :param message: message string that is to be sent to client
        :param client_obj: client object
        :param client_addr: string containing client address
        :return: None
        """
        print("Sending message to client {}\n{}".format(client_addr, message))
        client_obj.send(message.encode())

    @staticmethod
    def receive_message_from_client(client_obj, client_addr=""):
        """

        Static function to receive message from a client.

        1) uses recv() function of client object.

        :param client_obj: client object.
        :param client_addr: string containing client address.
        :return: string containing message from client
        """
        message = client_obj.recv(2048)
        print("Message received from client {}\n{}".format(client_addr, str(message)))
        return str(message.decode("utf-8"))

    def _verify_if_server(self):
        """

        Function to verify if server is created.

        1)If self.server variable is not set to True, then exception is raised.

        :return: None
        """
        if not self.server:
            raise Exception("Server server not created")



