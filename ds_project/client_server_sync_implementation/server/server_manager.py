import _thread
import time
import datetime as dt
from json import *
from utils.http_handler import HttpHandler
from utils.gui_handler import GuiHandler
from utils.socket_handler import SocketHandler


class ServerManager(object):

    def __init__(self):
        self.ongoing_clients = list()
        self.token = 0
        self.gui_handler = GuiHandler()
        self.socket_handler = SocketHandler()
        self.threads = list()
        self.http_handler = HttpHandler()
        self.shared_value = 1
        pass

    def _accept_client_requests(self):
        """
        Function to accept requests of client.

        Performs the following steps:
        1)Accept a client connection.
        2)Assign a thread to satisfy the requests of client.
        3)perform step 1 & 2 to accept other client requests.

        :return: None
        """
        while True:
            client_obj, client_addr = self.socket_handler.accept_incoming_client_request()
            if client_obj:
                _thread.start_new_thread(self._handle_client_requests, (client_obj, client_addr))

    def perform_server_application(self):
        """
        Central function that runs the server application

        Function performs the following steps:
        1) create a working socket
        2)start new thread that manages incoming client requests.
        3)start GUI for the application with the parent thread(required for tkinter library)

        :return:None
        """
        self._establish_working_socket()
        time.sleep(2)
        _thread.start_new_thread(self._accept_client_requests, ())
        self.gui_handler.initialize_gui()

    def _establish_working_socket(self):
        """
        Function to establish to sockets.

        Function performs the following steps:
        1)create a working socket and bind it to server ip and specified port.
        2)Make server listen with its new socket for incoming client requests.

        :return: None
        """
        self.socket_handler.create_server_socket()
        self.socket_handler.listen_to_incoming_client_request(request_queue=5)

    def _handle_client_requests(self, client_obj, client_addr):
        """
        Function to handle client requests. The client sends number of seconds the server has to wait or sleep for the
        client.

        Function performs the following steps:
        1) get request message  from client.
        2) if message contains value end_connection then connection with client is terminated.
        3) obtain operation from client from client.
        4)Perform it on server value
        5)Send shared value back top clients

        :param client_obj: client object
        :param client_addr: tuple containing client ip and port number.
        :return: None
        """
        self.gui_handler.modify_text_in_frames_for_gui(
            "info :: Server connected to client :: {}".format(str(client_addr)))
        client_name = self._get_client_name(client_obj, client_addr)
        while True:
            operation_dict = self._get_operation_from_client(client_obj, client_addr)
            if "end_connection" in operation_dict:
                self._terminate_socket_connection_with_client(client_obj, client_addr, client_name)
                break
            else:
                self._obtain_shared_value_from_client(operation_dict, client_obj, client_addr, client_name)
                self._send_new_shared_value_to_client(client_obj, client_addr, client_name)

    def _send_new_shared_value_to_client(self, client_obj, client_addr, client_name):
        message = {"shared_value": self.shared_value}
        self.socket_handler.send_message_to_client(dumps(message), client_obj, client_addr)

    def _obtain_shared_value_from_client(self, operation_dict, client_obj, client_addr, client_name):
        old_shared_value = self.shared_value
        client_result = operation_dict["operation_result"]
        operation = operation_dict["operation"]
        self.shared_value = str(eval("{}{}".format(old_shared_value, operation)))
        self.gui_handler.modify_text_in_frames_for_gui(
                "Received operations {} from client {}\nclient result :: {} ".format(operation, str(client_name) +
                                                               str(client_addr), client_result))
        self.gui_handler.modify_text_in_frames_for_gui(
                "Shared value updated from {} to {} by performing {}".format(old_shared_value, self.shared_value,
                                                                             operation))

    def _terminate_socket_connection_with_client(self, client_obj, client_addr, client_name=""):
            """
            Function to terminate connection with client.

            :param client_obj: client object
            :param client_addr: tuple containing client ip and client port number
            :return: None
            """
            self.gui_handler.modify_text_in_frames_for_gui(
                "info :: Client {} has terminated connection".format(str(client_name) + str(client_addr)))
            self.socket_handler.terminate_client_connection(client_obj, client_addr)

    def _get_operation_from_client(self, client_obj, client_addr):
        """
        Function to get sleep time from client.

        Function performs the following steps:
        1)get http request message from client
        2)decode http request message and get time value.

        :param client_obj:
        :param client_addr:
        :param client_name:
        :return: integer value specifying the number of seconds server has to sleep.
        """
        message = self.socket_handler.receive_message_from_client(client_obj, client_addr)
        message = loads(message)
        return message


    def _get_client_name(self, client_obj, client_addr):
        """
            Function to get client name from client.

            Function performs following steps:

            1)Get http request message that contains the name of client
            2)Decode the message to get client name.

            :param client_obj: Client object.
            :param client_addr: tuple containing client ip string and client port integer number.
            :return: string containing client name
        """
        message = self.socket_handler.receive_message_from_client(client_obj, client_addr)
        message = loads(message)
        if "end_connection" in message:
            self._terminate_socket_connection_with_client(client_obj, client_addr)
        self.gui_handler.modify_text_in_frames_for_gui(
            "info :: connected to {}{}".format(str(message["client_name"]), str(client_addr)))
        self.socket_handler.send_message_to_client(dumps({"shared_value": self.shared_value}), client_obj,
                                                   client_addr)
        return message["client_name"]

if __name__ == "__main__":
    ServerManager().perform_server_application()
