import _thread
import time
from json import *
from utils.http_handler import HttpHandler
from utils.gui_handler import GuiHandler
from utils.socket_handler import SocketHandler
from random import randint


class ClientManager(object):
    def __init__(self):
        self.socket_handler = SocketHandler()
        self.gui_handler = GuiHandler()
        self.http_handler = HttpHandler()
        self.user_button = {"send integer": self._wait_until_user_feeds_operation}
        self.shared_value = "1"
        self.operation_msg = ""
        self.operation_log = ""
        self.file_handler = None
        pass

    def perform_client_application(self):  #
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
        _thread.start_new_thread(self._send_client_name_and_operations_to_server, ())
        self.gui_handler.init_client_auth_gui(quit_button_command=self._terminate_pgm,
                                              user_buttons_dict=self.user_button)

    def _send_client_name_and_operations_to_server(self):
        """
        Function to send client name and random numbers to server.

        Function performs following steps:
        1) Gets client name from user
        2) Generates random number and sends it to server.

        :return: None
        """
        time.sleep(1)
        try:
            self._get_client_name_from_user_and_send_to_server()  #
            self.file_handler = open(self.client_name+".txt", "w+")
            self.gui_handler.modify_text_in_frames_for_gui("info :: Client connected to Server")  #
            self._get_operations_from_user_and_send_it_to_client()
        except:
            err_message = "info :: Error in sending message to Server.\n Message might not have reached Server"
            self.gui_handler.modify_text_in_frames_for_gui(err_message)

    def _get_initial_value_from_server(self):
        """
        Function to receive shared value from server.
        Fucntion receives json string containing shared value.
        :return:
        """
        message = self.socket_handler.receive_message_from_server()
        message_dict = loads(message)
        return str(message_dict["shared_value"])

    def _wait_until_user_feeds_operation(self):
        """
        Wait for user to input operations.
        Function performs the following steps.
        1)Execute while loop until user has given input in text box.
        :return:
        """
        self.gui_handler.text_box_value = ""
        while self.gui_handler.text_box_value == "":
            pass
        self.operation_msg = self.gui_handler.text_box_value
        self.file_handler.write("{}\n".format(self.operation_msg))
        self.gui_handler.modify_text_in_frames_for_gui(self.operation_msg)

    def _perform_operations_on_values(self):
        """
        Function to perform user provided operations on shared value.
        Eval function is used to perform operation on shared value.

        :return:
        """
        try:
            eval_statement = "{}{}".format(self.shared_value.strip(), self.operation_msg.strip())
            self.gui_handler.modify_text_in_frames_for_gui("eval_statement {}".format(eval_statement))
            result = str(eval(eval_statement))
            self.gui_handler.modify_text_in_frames_for_gui("Operation {} result ::\n{}".format(eval_statement, result))
            return result
        except Exception as err:
            self.gui_handler.modify_text_in_frames_for_gui("Operation syntax error. Invalid operation")
            self._wait_until_user_feeds_operation()
            self._perform_operations_on_values()

    def _update_result_value_to_server(self, result):
        """
        Function to send  operation result and operations to server.

        Function performs the following:
        1)create json string containing operation and operation result
        2)send it to server via socket.

        :param result:
        :return:
        """
        message_dict = {"operation": self.operation_msg.strip(),
                        "operation_result": result}
        self.socket_handler.send_message_to_server(dumps(message_dict))

    def _get_operations_from_user_and_send_it_to_client(self):
        """
        Function to get operations from user and perform it on initial value of client or server provided value
        Function performs the following tasks:
        1)Get shared value from server if that value is not client's initial value
        2)Wait until user provides operation in GUI
        3)Perform that operation on shared value
        4)Update the value and operation to server.
        :return:
        """
        while (True):
            shared_value = self._get_initial_value_from_server()
            if shared_value == self.shared_value:
                self.gui_handler.modify_text_in_frames_for_gui("Init value is 1")
            else:
                self.shared_value = shared_value
                self.gui_handler.modify_text_in_frames_for_gui(
                    "Shared value received from server :: {}".format(shared_value))
            self._wait_until_user_feeds_operation()
            result = self._perform_operations_on_values()
            self._update_result_value_to_server(result)

    def _get_operation_from_user(self):
        """
        Function to get operations from user.

        :return: integer between 5 to 15
        """
        self.operation_msg = self.gui_handler.text_box_value

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
            message = {"end_connection": True}
            self.socket_handler.send_message_to_server(dumps(message))
        except:
            print("Server socket terminated...")
        self.socket_handler.terminate_socket()
        exit(0)

    def _get_client_name_from_user_and_send_to_server(self):
        """
        Function to send to client name to server.

        Function performs the following steps:

        1)Get client name from user
        2)Encode name in http format
        3)Send the encoded message to server

        :return:
        """
        self.gui_handler.modify_text_in_frames_for_gui("Enter client name in text box.")
        while self.gui_handler.text_box_value is None:
            pass
        self.client_name = self.gui_handler.text_box_value
        message_dict = {"client_name": self.client_name}
        self.socket_handler.send_message_to_server(dumps(message_dict))


if __name__ == "__main__":
    ClientManager().perform_client_application()
