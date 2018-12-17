import time
from tkinter import *


class GuiHandler(object):
    gui_count = 0

    def __init__(self):
        self.root = Tk()
        self.root.geometry("350x350")
        self.top_frame = None
        self.bottom_frame = None
        self.text_box_value = None
        self.submit_button = None

    def modify_text_in_frames_for_gui(self, message):
        """
        Function to add new text on gui
        :param message: new text that needs to displayed on gui
        :return: None
        """
        for line in message.split("\n"):
            self.list_box.insert(END, line)

    def init_client_auth_gui(self, quit_button_command=None, user_buttons_dict=None,):
        self._create_scroll_bar()
        self._create_entry_box()
        self._create_submit_and_quit_button(quit_button_command)
        # self.quit_button_command = quit_button_command
        # self.user_buttons_dict=user_buttons_dict
        self.root.mainloop()
        
    def initialize_gui(self, quit_button_command=None, user_buttons_dict=None, ):
        """
        Function to create gui nad initialise it.

        The GUI provides a space in GUI to display text, scroll bar, user specified buttons and quit button.
        1)create a white space to display text and a scroll bar for it.
        2)Create quit buttons and user specified buttons.
        3)initialise GUI.

        :param quit_button_command: function object that is to be executed when quit button is clicked.
        :param user_buttons_dict: dictionary containing button text as keys and its respective function objects as its
        values.
        :return: None
        """
        self._create_scroll_bar()
        self._create_buttons_in_bottom_frame(quit_button_command, user_buttons_dict)
        self.root.mainloop()

    def _create_button(self, button_name, button_command):
        """
        Function to create a button.


        :param button_name:
        :param button_command:
        :return:
        """
        button = Button(self.root, text=button_name, command=button_command)
        button.pack()

    def _create_scroll_bar(self):
        """
        Function to create a scrollbar
        Function to creates a list boxes and assigns a scroll bar to it.

        :return: None
        """
        scroll_bar = Scrollbar(self.root)
        scroll_bar.pack(side="right", fill=Y)
        self.list_box = Listbox(self.root, yscrollcommand=scroll_bar.set)
        self.list_box.pack(fill=BOTH, expand=1)
        scroll_bar.config(command=self.list_box.yview)

    def _create_buttons_in_bottom_frame(self, quit_button_command, user_buttons_dict):
        """
        Function to create buttons. Creates both quit button and user defined buttons, if specified.
        Note: Buttons are created one below the other.
        Function performs the following steps:
        1) Creates user specified buttons.
        2) Creates quit button.

        :param quit_button_command: Function object that needs to be called if quit button is clicked.
        :param user_buttons_dict: Dictionary containing name of the button(string) and function object that needs to be
                called when that button is clicked
        :return: None
        """
        self._create_user_requested_buttons(user_buttons_dict)
        if quit_button_command == None:
            quit_button_command = self.root.quit
        self._create_button("Quit", quit_button_command)

    def _create_user_requested_buttons(self, user_buttons_dict):
        """
        Function to create user specified buttons.

        :param user_buttons_dict: Dictionary containing name of the button(string) and function object that needs to be
                called when that button is clicked
        :return: None
        """
        if user_buttons_dict:
            for button in user_buttons_dict:
                self._create_button(button, user_buttons_dict[button])

    def _create_entry_box(self):
        """"""
        self.text_box = Text(self.root, height=1, width=20)
        self.text_box.pack()

    def _get_text_box_value(self):
        self.text_box_value = self.text_box.get("1.0", "end-1c")
        self.text_box.delete("1.0", "end-1c")
        # self.text_box.pack_forget()
        # self.submit_button.pack_forget()
        # self.quit_button.pack_forget()
        # self._create_buttons_in_bottom_frame(self.quit_button_command, self.user_buttons_dict)

    def _create_submit_and_quit_button(self, quit_button_command):
        self.submit_button = Button(self.root, text="Submit", command=self._get_text_box_value)
        self.submit_button.pack()
        self.quit_button = Button(self.root, text="Quit", command=quit_button_command)
        self.quit_button.pack()









