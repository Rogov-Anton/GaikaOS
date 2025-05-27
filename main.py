#!/usr/bin/env python3

from os import system


class FileSystem:
    def __init__(self):
        self.files = []  # корневой каталог
        self.names = []  # строки с именами существующих файлов

    def make_directory(self, name: str, path: str):
        parts = path.split('/')
        current_dir: Directory = self  # текущая дериктория
        idx = 0

        if path == '/':  # создать директорию в корневом каталоге
            if name not in self.names:
                self.files.append(Directory(name))
                self.names.append(name)
                return ''
            else:
                return f"mkdir: cannot create directory '{name}': File exists"

        while len(parts) > idx:
            for elem in current_dir.files:  # перебор по файлам в текущей директории
                if isinstance(elem, Directory) and elem.name == parts[idx]:
                    current_dir = elem
                    idx += 1
                    break
            else:
                return f"mkdir: cannot create directory ‘{path}’: No such file or directory"
        else:
            if name in current_dir.names:
                return f'mkdir: cannot create directory ‘{name}’: File exists'
            else:
                current_dir.files.append(Directory(name))
                current_dir.names.append(name)
                return ''

    def list_directory(self, path: str):
        parts = path.split('/')
        current_dir: Directory = self  # текущая дериктория
        idx = 0

        if path == '/':  # вывести список директорий в корневом каталоге
            return self.files
        while len(parts) > idx:
            for elem in current_dir.files:
                if isinstance(elem, Directory) and elem.name == parts[idx]:
                    current_dir = elem
                    idx += 1
                    break
            else:
                return 'Error'
        else:
            return current_dir.files

    def write_file(self, text: str, path: str):

        parts = path.split('/')
        current_dir: Directory = self
        idx = 0

        while len(parts) - 1 > idx:
            for elem in current_dir.files:
                if isinstance(elem, Directory) and elem.name == parts[idx]:
                    current_dir = elem
                    idx += 1
                    break
            else:
                return 'unable to create a file: no such directory'
        else:
            name_of_file = parts[-1]
            for elem in current_dir.files:
                if isinstance(elem, File) and elem.name == name_of_file:
                    elem.text = text
                elif isinstance(elem, Directory) and elem.name == name_of_file:
                    return 'unable to create a file: it\'s a directory'
            else:
                current_dir.files.append(File(name_of_file, text))

    def read_file(self, path: str):

        parts = path.split('/')
        current_dir: Directory = self
        idx = 0

        while len(parts) - 1 > idx:
            for elem in current_dir.files:
                if isinstance(elem, Directory) and elem.name == parts[idx]:
                    current_dir = elem
                    idx += 1
                    break
            else:
                return f'cat: {path}: no such file or directory'
        else:
            name_of_file = parts[-1]
            for elem in current_dir.files:
                if isinstance(elem, File) and elem.name == name_of_file:
                    return elem.text
                elif isinstance(elem, Directory) and elem.name == name_of_file:
                    return f'cat: {path}: it\'s a directory'
            else:
                return f'cat: {path}: no such file or directory'

    def remove_file(self, path):

        parts = path.split('/')
        current_dir: Directory = self
        idx = 0

        while len(parts) - 1 > idx:
            for elem in current_dir.files:
                if isinstance(elem, Directory) and elem.name == parts[idx]:
                    current_dir = elem
                    idx += 1
                    break
            else:
                return f'rm: {path}: no such file or directory'
        else:
            name_of_file = parts[-1]
            for elem in current_dir.files:
                if isinstance(elem, File) and elem.name == name_of_file:
                    del elem
                elif isinstance(elem, Directory) and elem.name == name_of_file:
                    return f'rm: unable to delete `{path}`: This is the directory'
            else:
                return f'rm: {path}: no such file or directory'


class Directory:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.names = []


class File:
    def __init__(self, name, text):
        self.name = name
        self.text = text

    def __del__(self):
        return


def print_quide():
    quide = '''
    Создание каталога:
        mkdir {имя_каталога} {путь_до_каталога}
        Чтобы создать каталог в корневом каталоге в качестве пути до каталаго нужно указать /

    Просмотр содержимого каталога:
        ls {путь_до_каталога}
        Чтобы просмотреть содержимое в корневом каталоге в качестве пути до каталаго нужно указать /
        Синим цветом будут обозначены каталоги, белым - файлы
    
    Создание/запись файла:
        write {текст_для_записи} {путь_до_файла}
        Пример:
            write Hello World! dir/file -- запишет строку 'Hello World!' в файл, находящийся в каталоге dir,
            или создаст его, если его не существует
    
    Чтение файла:
        cat {путь_до_файла}
        Пример:
            cat dir/file -- выведет на экран содержимое файла file, который находится в каталоге dir

    fetch - Вывести информацию о системе
    
    clear - Очистить экран

    exit - Выход из системы (также можно использовать q)
    '''
    print(quide)
    print()


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
        "OS   GaikaOS",
        "VER  0.0.0.2",
        "HST  GaikaPC"
    ]

    for art_line, info_line in zip(ascii_art, info_text):
        print(f"{blue_color}{art_line}{reset_color}   {info_line}")


def execute_command(filesystem: FileSystem, text):  # Функция для выполнения команд

    parts = text.split()

    if text == 'man':
        print_quide()
        return
    if not parts:
        return

    command = parts[0]
    if command == 'mkdir':
        result = filesystem.make_directory(parts[1], parts[2])
        if result != '':
            print(result)

    elif command == 'ls':
        if text.strip() == 'ls':
            print(filesystem.list_directory('/'))
            return
        result = filesystem.list_directory(parts[1])
        if result == 'Error':
            print(f"ls: cannot access '{parts[1]}': No such file or directory")
        else:
            for elem in result:
                if isinstance(elem, Directory):
                    print(f"\033[34m{elem.name}\033[0m")
                else:
                    print(elem.name)

    elif command == 'write':
        result = filesystem.write_file(' '.join(parts[1:len(parts) - 1]), parts[-1])
        if result is not None:
            print(result)

    elif command == 'cat':
        result = filesystem.read_file(parts[1])
        print(result)
    elif command == 'rm':
        result = filesystem.remove_file(parts[1])
        print(result)
    elif command == 'clear':
        system('clear')
    elif command == 'fetch':
        print_fetch()
    else:
        print(f"{parts[0]}: command not found")


def main():
    print()
    print('Welcome to GaikaOS!')
    print('Type `man` to get guide.\n')
    filesystem = FileSystem()
    command = input('-> ')
    while command not in ('q', 'exit'):
        execute_command(filesystem, command)
        command = input('-> ')


if __name__ == '__main__':
    main()
