import os
import pickle
import tkinter
from tkinter import filedialog


def create_directory(path):
    """
    Create directory if it does not exists.
    :param path: path of the directory
    :return: False if directory already exists, True otherwise
    """
    if os.path.exists(path):
        return False
    os.makedirs(path)
    return True


def list_files(directory, extension='', *, full_path=True, search_subdirectories=False):
    """
    Get all files in a given directory with the given file extension.
    :param directory: directory containing the files
    :param extension: file extension (e.g. '.txt')
    :param full_path: True to return full paths, False to return file names only
    :param search_subdirectories: whether files in subdirectories are returned
    :return: list of files in the given directory
    """
    if search_subdirectories:
        temp = [os.path.join(path, file) for (path, names, file_names) in os.walk(directory) for file in file_names]
        return [i for i in temp if i.endswith(extension)]
    return [f'{directory}/{file}' if full_path else file for file in os.listdir(directory)
            if file.endswith(extension)]


def list_directories(directory):
    """
    Get all immediate subdirectories.
    :param directory: the directory containing the subdirectories
    :return: full paths of all the immediate subdirectories
    """
    return [f'{directory}/{subdirectory}' for subdirectory in os.listdir(directory)
            if os.path.isdir(f'{directory}/{subdirectory}')]


def pickle_dump(variable, path):
    """
    Save a variable as pickle.
    :param variable: variable to be saved
    :param path: path of the pickle
    :return: None
    """
    with open(path + '.pickle', 'wb') as handle:
        pickle.dump(variable, handle, protocol=pickle.HIGHEST_PROTOCOL)


def pickle_load(path):
    """
    Load variable from a pickle file.
    :param path: path of the pickle file
    :return: variable contained in the pickle file
    """
    with open(path, 'rb') as handle:
        return pickle.load(handle)


def select_directory(message=None):
    """
    GUI support for selecting a directory.
    :param message: message to be displayed on the directory selection window
    :return: path of the directory, None if nothing is selected
    """
    if message:
        print(message)
    root = tkinter.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, title=message)
    root.destroy()
    if directory:
        return directory
    return None


def select_file(message=None, extension='*'):
    """
    GUI support for selecting a file.
    :param message: message to be displayed on the file selection window
    :param extension: file extension for filtering (e.g. '.txt')
    :return: path of the file, None if nothing is selected
    """
    if message:
        print(message)
    root = tkinter.Tk()
    root.withdraw()
    file = filedialog.askopenfilename(parent=root, title=message, filetypes=[("", extension)])
    root.destroy()
    if file:
        return file
    return None


def select_files(message=None, extension='*'):
    """
    GUI support for selecting multiple files.
    :param message: message to be displayed on the file selection window
    :param extension: file extension for filtering (e.g. '.txt')
    :return: list of paths of the file, None if nothing is selected
    """
    if message:
        print(message)
    root = tkinter.Tk()
    root.withdraw()
    files = filedialog.askopenfilenames(parent=root, title=message, filetypes=[("", extension)])
    root.destroy()
    if files:
        return files
    return None
