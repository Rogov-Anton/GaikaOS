#!/usr/bin/env python3


class FileSystem:
    def __init__(self):
        self.files = []
        self.names = []

    def find_directory(self, path: str):
        if path == '/':
            return self
        parts = path.split('/')
        idx = 0
        current_dir = self

        while len(parts) > idx:
            for elem in current_dir.files:
                if isinstance(elem, Directory) and elem.name == parts[idx]:
                    current_dir = elem
                    idx += 1
                    break
            else:
                return False
        return current_dir

    def make_directory(self, name: str, path: str):
        directory = self.find_directory(path)
        if not directory:
            return f'mkdir: no such file or directory'
        for elem in directory.files:
            if (isinstance(elem, Directory) or isinstance(elem, File)) and elem.name == name:
                return f'mkdir: file exists'
        directory.files.append(Directory(name))
        directory.names.append(name)
        return True

    def list_directory(self, path: str):
        directory = self.find_directory(path)
        if not directory:
            return f'lsdir: no such file or directory'
        return directory.files

    def remove_directory(self, path: str, name: str):
        directory = self.find_directory(path)
        if not directory:
            return f'rmdir: no such file or direcotry'
        for elem in directory.files:
            if isinstance(elem, Directory) and elem.name == name:
                directory.names.remove(name)
                directory.files.remove(elem)
                return None
        else:
            return f'rmdir: no such file or direcotry'

    def make_file(self, name: str, path: str):
        directory = self.find_directory(path)
        if not directory:
            return f'touch: no such file or directory'
        for elem in directory.files:
            if isinstance(elem, Directory) and elem.name == name:
                return f'touch: it`s a directory'
            if isinstance(elem, File) and elem.name == name:
                return None
        else:
            directory.files.append(File(name, ''))
            directory.names.append(name)
            return None

    def write_file(self, text: str, path: str):
        parts = path.split('/')
        directory = self if len(parts) == 1 else self.find_directory('/'.join(parts[:len(parts) - 1]))
        name_of_file = parts[-1]
        for elem in directory.files:
            if isinstance(elem, File) and elem.name == name_of_file:
                elem.text = text
                return None
            elif isinstance(elem, Directory) and elem.name == name_of_file:
                return f'write: it`s a direcotry'
        else:
            return f'write: no such file or directory'

    def read_file(self, path: str):
        pass

class Directory:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.names = []


class File:
    def __init__(self, name, text):
        self.name = name
        self.text = text


def print_fetch():
    blue_color = "\033[34m"
    reset_color = "\033[0m"

    ascii_art = [
        "         ____     ",
        "        / __ \\    ",
        "       / /  \\ \\   ",
        "       \\ \\__/ /   ",
        "        \\____/    "
    ]

    info_text = [
        "GAIKA-FETCH",
        "-----------",
        "OS   GaikaOS-beta",
        "VER  0.0.0.2",
        "HST  GaikaPC"
    ]

    for art_line, info_line in zip(ascii_art, info_text):
        print(f"{blue_color}{art_line}{reset_color}   {info_line}")


def execute_command(filesystem: FileSystem, text: str):
    if not text:
        return
    parts = text.split()
    command = parts[0]
    if command == 'mkdir':
        name = parts[1]
        path = parts[2]
        result = filesystem.make_directory(name, path)
        if not result:
            print(result)
    elif command == 'ls':
        path = parts[1]
        result = filesystem.list_directory(path)
        if not isinstance(result, list):
            print(result)
            return
        for elem in result:
            if isinstance(elem, Directory):
                print(f"\033[34m{elem.name}\033[0m")
            else:
                print(elem.name)
    elif command == 'rmdir':
        path = parts[1]
        name = parts[2]
        result = filesystem.remove_directory(path, name)
        if not result is None:
            print(result)
    elif command == 'touch':
        path = parts[2]
        name = parts[1]
        result = filesystem.make_file(name, path)
        if not result is None:
            print(result)
    elif command == 'write':
        #   0     1     2     3
        # write Hello World! file
        text = parts[1:len(parts) - 2]
        path = parts[-1]
        result = filesystem.write_file(text, path)
        if not result is None:
            print(result)
    elif command == 'fetch':
        print_fetch()
    else:
        print('unknown command')


filesystem = FileSystem()
R = 1
if R:
    command = input('-> ')
    while command != 'q':
        execute_command(filesystem, command)
        command = input('-> ')
else:
    command = ''
    execute_command(filesystem, command)
