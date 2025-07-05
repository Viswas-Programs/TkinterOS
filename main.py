import sys, os
import time

from desktop.desktop import DesktopGUI
from desktop.file_manager import FileManager
from desktop.task_bar import TaskBar
from applications.python_game import PythonGame
from applications.pybrowse import PyBrowse
from styles import button_color, button_hover_color, desktop_highlight_colors, desktop_bright_colors

class OS:
    def __init__(self) -> None:
        self.file_manager = FileManager()
        self.gui = DesktopGUI(self)
        self.task_bar = TaskBar(self, self.gui)
        self.create_variables()
        self.create_binds()
        self.load_files()
        self.run()

    
    def create_variables(self) -> None:
        self.dark_mode = False
        self.start_menu_open = False
        self.utils_menu_open = False
        self.internet_on = False
        self.document_list = []


    def create_binds(self) -> None:
        self.gui.desktop_frame.bind("<Button-1>", self.close_windows)
        self.gui.desktop_frame.bind("<Button-1>", self.get_click_position)
        self.gui.desktop_frame.bind("<Button-3>", self.create_desktop_context_menu_frame)
        self.gui.desktop_logo.bind("<Button-3>", lambda event: self.create_desktop_context_menu_frame(event, widget="logo"))
        self.gui.new_button.bind("<Enter>", self.creates_desktop_context_menu)

        self.gui.desktop_frame.bind("<B1-Motion>", self.create_selection_box)
        self.gui.desktop_frame.bind("<ButtonRelease-1>", self.delete_motion_area)


    def run(self) -> None:
        self.gui.run()

    
    def quit(self) -> None:
        sys.exit()

    
    def restart(self) -> None:
        os.execl(sys.executable, sys.executable, *sys.argv)


    def close_windows(self, event) -> None:
        self.close_start_menu()
        self.close_utils_menu()
        self.close_desktop_context_menu()

    
    def start_menu_mechanism(self) -> None:
        if not self.start_menu_open:
            self.task_bar.start_menu_frame.place(anchor="sw", relx=0, rely=0.96)
        else:
            self.task_bar.start_menu_frame.place_forget()
        self.start_menu_open = not self.start_menu_open

    
    def close_start_menu(self) -> None:
        self.task_bar.start_menu_frame.place_forget()
        self.start_menu_open = False

        self.gui.desktop_actions_frame.place_forget()

    
    def create_desktop_context_menu_frame(self, event, widget = None) -> None:
        self.close_windows(None)
        if widget == "logo":
            self.gui.desktop_actions_frame.place(x=event.x+self.gui.width/2.29, y=event.y+self.gui.height/2.63)
        else:
            self.gui.desktop_actions_frame.place(x=event.x, y=event.y)


    def creates_desktop_context_menu(self, event) -> None:
        """Opens context menu when you right click on the desktop"""
        self.desktop_actions_frame_x = self.gui.desktop_actions_frame.winfo_rootx()
        self.desktop_actions_frame_y = self.gui.desktop_actions_frame.winfo_rooty()
        self.gui.new_action_frame.place(x=self.desktop_actions_frame_x + self.gui.desktop_actions_frame.winfo_width(), y=self.desktop_actions_frame_y - self.gui.desktop_actions_frame.winfo_height())

    
    def close_desktop_context_menu(self) -> None:
        """Closes context menu when you left click on the desktop"""
        self.gui.new_action_frame.place_forget()

    
    def load_files(self):
        print(self.file_manager.file_objects)
        for file in self.file_manager.file_objects:
            self.gui.create_text_document_gui(file.pos_x, file.pos_y, file.name)


    def create_text_document(self) -> None:
        self.gui.create_text_document_gui(self.desktop_actions_frame_x, self.desktop_actions_frame_y)
        self.close_windows(None)


    def open_text_document(self) -> None:
        self.gui.create_text_document_open_gui()


    def get_click_position(self, event):
        self.x_click_pos = event.x
        self.y_click_pos = event.y


    def create_selection_box(self, event) -> None:
        """Creates a selection box on left click drag on the desktop"""
        try:
            self.gui.motion_frame.destroy()
        except:
            pass
        
        if self.y_click_pos < event.y and self.x_click_pos < event.x:
            self.gui.create_selection_box_gui(self.x_click_pos, self.y_click_pos, event.x, event.y)

        elif self.y_click_pos > event.y and self.x_click_pos > event.x:
            self.gui.create_selection_box_gui(event.x, event.y, self.x_click_pos, self.y_click_pos)

        elif self.y_click_pos > event.y and self.x_click_pos < event.x:
            self.gui.create_selection_box_gui(self.x_click_pos, event.y, event.x, self.y_click_pos)

        elif self.y_click_pos < event.y and self.x_click_pos > event.x:
            self.gui.create_selection_box_gui(event.x, self.y_click_pos, self.x_click_pos, event.y)


    def delete_motion_area(self, event) -> None:
        try:
            self.gui.motion_frame.destroy()
        except:
            pass


    def play_game(self, game:str) -> None:
        match game:
            case "python":
                PythonGame(self, self.gui.WINDOW)
            case "pybrowse":
                self.py_browse = PyBrowse(self, self.gui.WINDOW)
                self.show_pybrowse_gui()


    def get_time(self) -> str:
        current_time = time.localtime(time.time())
        current_time = time.strftime("%H:%M", current_time)
        return current_time
    
    
    def get_date(self) -> str:
        current_date = time.localtime(time.time())
        current_date = time.strftime("%d/%m/%Y", current_date)
        return current_date
    

    def utils_menu_mechanism(self) -> None:
        if not self.utils_menu_open:
            self.task_bar.utils_menu_frame.place(anchor="se", relx=1, rely=0.96)
        else:
            self.task_bar.utils_menu_frame.place_forget()
        self.utils_menu_open = not self.utils_menu_open


    def internet_mechanism(self) -> None:
        if not self.internet_on:
            self.task_bar.internet_button.configure(fg_color=button_color, hover_color=button_hover_color)
            self.task_bar.internet.configure(image=self.task_bar.internet_icon)
            self.task_bar.internet_label.configure(text="Available")
        else:
            self.task_bar.internet_button.configure(fg_color=desktop_highlight_colors, hover_color=desktop_bright_colors)
            self.task_bar.internet.configure(image=self.task_bar.no_internet_icon)
            self.task_bar.internet_label.configure(text="Wi-Fi")
        self.internet_on = not self.internet_on

    
    def close_utils_menu(self) -> None:
        self.task_bar.utils_menu_frame.place_forget()
        self.utils_menu_open = False


    def show_pybrowse_gui(self) -> None:
        if not self.internet_on:
            self.py_browse.no_internet_frame.place(anchor="center", relx=0.5, rely=0.5)
        else:
            pass


if __name__ == "__main__":
    OS().run()
