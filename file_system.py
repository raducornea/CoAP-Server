import os
import server_gui as gui
import server_logic as server


class FileSystem:
    absolute_path = os.getcwd()  # project path
    current_path = os.getcwd()  # working path for file system operations
    allowed_commands = ['chdir', 'cwd', 'newDir', 'newFile', 'ls']  # commands to check

    # initiates / resests attributes
    @classmethod
    def __init__(cls):
        cls.current_path = cls.absolute_path

    # (chdir) - change directory
    @classmethod
    def set_path(cls, new_path):
        try:
            os.chdir(new_path)
            cls.current_path = new_path
        except FileNotFoundError:
            print("The path does not exist")

    # (cwd) - current work directory
    @classmethod
    def get_current_work_directory(cls):
        return cls.current_path

    # (newDir) - new directory in the current work path
    @staticmethod
    def new_directory(dir_name='tempDir'):
        try:
            os.mkdir(dir_name)
            message = "Directory " + dir_name + " created"
            send_message_to_listeners(message)
            print(message)
        except FileExistsError:
            message = "Directory " + dir_name + " already exists"
            send_message_to_listeners(message)
            print(message)

    # (newFile) - new file in the current work path
    @classmethod
    def new_file(cls, file_name='tempFile.txt'):
        if os.path.exists(cls.current_path + '/' + file_name):
            message = "File " + file_name + " already exists"
            send_message_to_listeners(message)
            print(message)
        else:
            with open(file_name, mode='a'):
                message = "File " + file_name + " created"
                send_message_to_listeners(message)
                print(message)

    # (ls) - list existing files and directories in the current work path
    @classmethod
    def list_files_and_directories(cls):
        files = list(filter(os.path.isfile, os.listdir(cls.current_path)))
        directories = list(filter(os.path.isdir, os.listdir(cls.current_path)))

        print(directories + files)

    # (rename) - changes file/directory name to a new one
    @classmethod
    def rename(cls, old_name='', new_name=''):
        if old_name == '' or new_name == '':
            message = 'Please put both old and new name'
            send_message_to_listeners(message)
            print(message)
        else:
            message = old_name + ' changed to ' + new_name
            send_message_to_listeners(message)
            print(message)
            os.rename(old_name, new_name)


def send_message_to_listeners(message):
    gui.GUI.console(message)
    server.Logic.set_data(message)
