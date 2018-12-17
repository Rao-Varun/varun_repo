import _thread
import time
import datetime as dt
from utils.http_handler import HttpHandler
from utils.gui_handler import GuiHandler
from utils.socket_handler import SocketHandler


class ServerManager(object):

    def __init__(self):
        self.gui_handler = GuiHandler()
        self.socket_handler = SocketHandler()
        self.threads = list()
        self.http_handler = HttpHandler()
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
        2) if message contains value 900 then connection with client is terminated.
        3) if value is between 5 to 15, then server sleeps for time specified in value.


        :param client_obj: client object
        :param client_addr: tuple containing client ip and port number.
        :return: None
        """
        self.gui_handler.modify_text_in_frames_for_gui(
            "info :: Server connected to client :: {}".format(str(client_addr)))
        client_name = self._get_client_name(client_obj, client_addr)
        while True:
            sleep_time = self._get_sleep_time_from_client(client_obj, client_addr)
            if "900" in sleep_time:
                self._terminate_socket_connection_with_client(client_obj, client_addr, client_name)
                break
            else:
                self._perform_sleep_operation_for_client(int(sleep_time), client_obj, client_addr, client_name)

    def _decode_http_message(self, message):
        """

        :param message:
        :return:
        """
        return message

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

    def _get_sleep_time_from_client(self, client_obj, client_addr):
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
        decoded_message = self.http_handler.http_request_decode(message)
        return decoded_message[1]

    def _perform_sleep_operation_for_client(self, sleep_time, client_obj, client_addr, client_name):
        """
        Function to make server sleep for value specified by client.

        :param sleep_time: integer specifying the number of seconds server has to sleep for.
        :param client_obj: client object
        :param client_addr: tuple containing client ip and client port number.
        :return:
        """
        self.gui_handler.modify_text_in_frames_for_gui(
            "info :: received int {0} from client {1}.\nSleeping for {0} sec".format(str(sleep_time),
                                                                                     str(client_name) + str(
                                                                                         client_addr)))
        time.sleep(sleep_time)
        self.gui_handler.modify_text_in_frames_for_gui(
            "info :: Slept {}sec for client {}.".format(str(sleep_time), str(client_name) + str(client_addr)))
        decoded_message = self.http_handler.http_response_encode(
            "Slept {}sec for client {}.".format(str(sleep_time), str(client_name) + str(client_addr)))
        self.gui_handler.modify_text_in_frames_for_gui(
            "Sending  message to client {}\n<<\n{}\n>>.".format(str(client_name) + str(client_addr), decoded_message))
        self.socket_handler.send_message_to_client(decoded_message, client_obj, client_addr)

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
        decoded_message = self.http_handler.http_request_decode(message)
        print("client name :: {}".format(str(decoded_message)))
        if "900" in decoded_message[1]:
            self._terminate_socket_connection_with_client(client_obj, client_addr)
        self.gui_handler.modify_text_in_frames_for_gui(
            "info :: connected to {}{}".format(decoded_message[1], str(client_addr)))
        return decoded_message[1]


if __name__ == "__main__":
    ServerManager().perform_server_application()
