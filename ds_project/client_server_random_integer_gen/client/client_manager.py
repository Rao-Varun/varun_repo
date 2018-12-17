import _thread
import time
from utils.http_handler import HttpHandler
from utils.gui_handler import GuiHandler
from utils.socket_handler import SocketHandler
from random import randint


class ClientManager(object):
    def __init__(self):
        self.socket_handler = SocketHandler()
        self.gui_handler = GuiHandler()
        self.http_handler = HttpHandler()
        self.user_button = {"send integer": self._generate_random_number}
        self.rand_int = None
        pass

    def perform_client_application(self):
        """
        Main function to perform client application.
        Application sends integer to server application and expects to wait or sleep for the number of seconds specified by integer.

        Function performs following tasks
        1) Establishes socket connection with client
        2) Initialize gui. Gui contains 2 buttons
            1 button to quit the application.
            other to generate a random integer between 5 to 15 and send it to server

        :return: None
        """
        self._establish_socket_connection()
        _thread.start_new_thread(self._send_client_name_and_random_number_to_client, ())
        self.gui_handler.init_client_auth_gui(quit_button_command=self._terminate_pgm, user_buttons_dict=self.user_button)

    def _send_client_name_and_random_number_to_client(self):
        """
        Function to send client name and random numbers to server.

        Function performs following steps:
        1) Gets client name from user
        2) Generates random number and sends it to server.

        :return: None
        """
        try:
            self._get_client_name_from_user_and_send_to_server()
            self.gui_handler.modify_text_in_frames_for_gui("info :: Client connected to Server")
            self._get_number_from_user_and_send_to_server()
        except:
            err_message = "info :: Error in sending message to Server.\n Message might not have reached Server"
            self.gui_handler.modify_text_in_frames_for_gui(err_message)

    def _communicate_with_server(self, message, sleep_int):
        """
        Function to communicate with server.

        performs the following steps.
        1) send http encoded message (integer) to server.
        2) Receive response message from server.
        3) Decode the message and get the original message
        3) display that message on gui

        :param message: string containing integer between 5 to 15 which is encoded in http.
        :return: None
        """
        self.socket_handler.send_message_to_server(message)
        print("client sleeping")
        time.sleep(sleep_int)
        message = self.socket_handler.receive_message_from_server()
        message = self.http_handler.http_response_decode(message)
        print(message)
        self.gui_handler.modify_text_in_frames_for_gui("Server response :: {}".format(message))


    def _generate_random_number(self):
        """
        Function to generate random integer between 5 to 15

        :return: integer between 5 to 15
        """
        self.rand_int = randint(5, 15)

    def _establish_socket_connection(self):
        """
         function to establish socket connection and connects with server.

         Function performs the following steps.
         1) Create client socket
         2) Connect to server

        :return: None
        """
        self.socket_handler.create_client_socket()
        self.socket_handler.connect_to_server()

    def _terminate_pgm(self):
        """
        Function to terminate the application. Called when quit button on gui.
        Function performs the following steps.
        1)Send message that Client is exiting.
        2)Terminate the client socket.
        3)Exit application
        :return: None
        """
        try:
            encoded_message = self.http_handler.http_request_encode("sleep_time", 900)
            self.socket_handler.send_message_to_server(encoded_message)
        except:
            print("Server socket terminated...")
        self.socket_handler.terminate_socket()
        exit(0)

    def _encode_number_with_http(self, sleep_int):
        """
        Function to encode message to http.
        :param sleep_int: Integer that is to encoded to http.
        :return: string containing http encoded message.
        """
        return str(sleep_int)

    def _get_client_name_from_user_and_send_to_server(self):
        """
        Function to send to client name to server.

        Function performs the following steps:

        1)Get client name from user
        2)Encode name in http format
        3)Send the encoded message to server

        :return:
        """

        while self.gui_handler.text_box_value is None:
            pass
        encoded_message = self.http_handler.http_request_encode("client_name", self.gui_handler.text_box_value)
        self.socket_handler.send_message_to_server(encoded_message)

    def _get_number_from_user_and_send_to_server(self):
        """
                Function to generate an integer, encode it in http, and send it to server.

                Function performs the following steps
                1) Generate random integer 'n' between 5 to 15.
                2) Encode 'n' in http.
                3) Send http request message to server. Wait for it sleep 'n' seconds and get response from server.

                :return: None
        """
        while True:
            while self.rand_int is None:
                pass
            message = self.http_handler.http_request_encode("sleep_int", self.rand_int)
            self.gui_handler.modify_text_in_frames_for_gui("info :: Sending message to server ::\n<<\n{}\n>>".format(str(message)))
            self._communicate_with_server(message, self.rand_int)
            self.rand_int = None



if __name__ == "__main__":
    ClientManager().perform_client_application()
