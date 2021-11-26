import os


class FileSystem:
    def __init__(self):
        self.absolute_path = os.getcwd()
        self.current_path = os.getcwd()

    # (chdir) - change directory
    def set_path(self, new_path):
        try:
            os.chdir(new_path)
            self.current_path = new_path
        except FileNotFoundError:
            print("The path does not exist")

    # (cwd) - current work directory
    def get_current_work_directory(self):
        return self.current_path

    # (newDir) - new directory in the current work path
    def new_directory(self, dir_name='tempDir'):
        try:
            os.mkdir(dir_name)
            print("vvDirectory", dir_name, "created ")
        except FileExistsError:
            print("vvDirectory", dir_name, "already exists")

    # (newFile) - new file in the current work path
    def new_file(self, file_name='tempFile.txt'):
        if os.path.exists(self.current_path + '/' + file_name):
            print("vvFile", file_name, "already exists")
        else:
            with open(file_name, mode='a'):
                print("vvFile", file_name, "created")

    #  (ls) - list existing files and directories in the current work path
    def list_files_and_directories(self):
        files = list(filter(os.path.isfile, os.listdir(self.current_path)))
        directories = list(filter(os.path.isdir, os.listdir(self.current_path)))

        print(directories + files)