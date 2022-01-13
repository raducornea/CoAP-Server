import os
import server_gui as gui
import server_logic as server


class FileSystem:
    # commands to check
    allowed_commands = ['chdir', 'cwd', 'newDir', 'newFile', 'ls', 'rename', 'delete', 'move', 'disconnect']
    absolute_path = os.getcwd()  # project path
    current_path = os.getcwd()  # working path for file system operations

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
            # message = cls.current_path
            message = 0
            return message
        except FileNotFoundError:
            # message = "The path does not exist"
            message = 1
            return message

    # (cwd) - current work directory
    @classmethod
    def get_current_work_directory(cls):
        return cls.current_path

    # (newDir) - new directory in the current work path
    @classmethod
    def new_directory(cls, dir_name='tempDir'):
        # if the cwd path root differs from the allowed path (absolute path), DO NOT ALLOW IT TO CREATE
        if not cls.current_path.startswith(cls.absolute_path):
            # message = f"Operation not Allowed Here. Please use the allowed path as the start of the working directory"
            message = 0
            return message

        try:
            os.mkdir(dir_name)
            # message = "Directory " + dir_name + " created"
            message = 1
            return message
        except FileExistsError:
            # message = "Directory " + dir_name + " already exists"
            message = 2
            return message

    # (newFile) - new file in the current work path
    @classmethod
    def new_file(cls, file_name='tempFile.txt'):
        # if the cwd path root differs from the allowed path (absolute path), DO NOT ALLOW IT TO CREATE
        if not cls.current_path.startswith(cls.absolute_path):
            # message = f"Operation not Allowed Here. Please use the allowed path as the start of the working directory"
            message = 0
            return message

        if os.path.exists(cls.current_path + '/' + file_name):
            # message = "File " + file_name + " already exists"
            message = 2
            return message
        else:
            with open(file_name, mode='a'):
                # message = "File " + file_name + " created"
                message = 1
                return message

    # (ls) - list existing files and directories in the current work path
    @classmethod
    def list_files_and_directories(cls):
        files = list(filter(os.path.isfile, os.listdir(cls.current_path)))
        directories = list(filter(os.path.isdir, os.listdir(cls.current_path)))
        return directories, files

    # (rename) - changes file/directory name to a new one
    @classmethod
    def rename(cls, old_name='', new_name=''):
        # if the cwd path root differs from the allowed path (absolute path), DO NOT ALLOW IT TO RENAME
        if not cls.current_path.startswith(cls.absolute_path):
            message = f"Operation not Allowed Here. Please use the allowed path as the start of the working directory."
            return message

        if old_name == '' or new_name == '':
            message = 'Please put both old and new name'
            return message
        else:
            message = old_name + ' changed to ' + new_name

            try:
                os.rename(old_name, new_name)
            except FileNotFoundError:
                message = "File/Folder " + old_name + " not found"
                return message
            except FileExistsError:
                message = "File/Folder " + old_name + " already exists"
                return message

            return message

    @classmethod
    # (delete) - removes file/directory
    def delete(cls, target):
        # if the cwd path root differs from the allowed path (absolute path), DO NOT ALLOW IT TO REMOVE
        if not cls.current_path.startswith(cls.absolute_path):
            message = f"Operation not Allowed Here. Please use the allowed path as the start of the working directory."
            return message

        path = os.path.join(cls.current_path, target)
        try:
            os.remove(path)
        except FileNotFoundError:
            message = f"{target} not found"
            return message
        # os.remove -> can remove only files
        except PermissionError:
            # os.rmdir -> can remove folders
            os.rmdir(path)
            message = f"{target} successfully removed"
            return message

        message = f"{target} successfully removed"
        return message

    @classmethod
    # (move) - moves file/directory to destination
    def move(cls, path, target):
        # if the location differs from the allowed path (absolute path), DO NOT ALLOW IT TO REMOVE
        if not path.startswith(cls.absolute_path):
            message = f"Operation not Allowed Here. Please use the allowed path as the start of the working directory."
            return message

        # if the file/directory exists already in directory
        files = list(filter(os.path.isfile, os.listdir(path)))
        directories = list(filter(os.path.isdir, os.listdir(path)))
        if target in directories or target in files:
            message = f"{target} already exists in new Path"
            return message

        # if the file/directory does not exist in cwd
        files, directories = cls.list_files_and_directories()
        if target not in directories and target not in files:
            message = f"{target} does not Exist in Current Work Directory"
            return message

        os.rename(f"{cls.get_current_work_directory()}\\{target}", f"{path}\\{target}")
        message = f"{target} successfully moved to {cls.get_current_work_directory()}"
        return message

    # print(fs.new_directory('Folder'))
    # print(fs.new_file('File.txt'))
    # print(fs.set_path('C:\\Users\\Radu\\Desktop'))

    # print(fs.rename('File', 'File2.txt'))
    # print(fs.rename('File.txt', 'File2.txt'))
    # print(fs.rename('Fold', 'Folder2'))
    # print(fs.rename('Folder', 'FolderNew'))
    #
    # print(fs.set_path('C:\\Users\\Radu\\Desktop\\RC-Proiect\\FolderNew'))
    # print(fs.delete('FolderNew'))
    #
    # print(fs.set_path(r'C:\Users\Radu\Desktop\RC-Proiect'))
    # directories, files = fs.list_files_and_directories()
    # print(directories)
    # print(files)
    #
    # print(fs.move(r'C:\Users\Radu\Desktop\RC-Proiect\Folder', 'File2.txt'))