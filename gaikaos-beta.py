class FileSystem:
    def __init__(self):
        self.files = [
            Directory('bin'),
            Directory('home')
        ]  # корневой каталог
        self.names = ['bin', 'home']  # строки с именами существующих файлов

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
            return f'mkdir: unable to create directory `{path}`: No such file or directory'
        if name in directory.names:
            return f'mkdir: unable to create directory `{name}`: File exists'
        directory.files.append(Directory(name))
        directory.names.append(name)
        return True

    def list_directory(self, path: str):
        directory = self.find_directory(path)
        return directory.files


class Directory:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.names = []


class File:
    def __init__(self, name, text):
        self.name = name
        self.text = text


def execute_command(filesystem: FileSystem, text: str):
    if not text:
        return
    parts = text.split()
    command = parts[0]
    if command == 'mkdir':
        name = parts[1]
        path = parts[2]
        result = filesystem.make_directory(name, path)
        if result != True:
            print(result)
    elif command == 'ls':
        path = parts[1]
        result = filesystem.list_directory(path)
        for elem in result:
            if isinstance(elem, Directory):
                print(f"\033[34m{elem.name}\033[0m")
            else:
                print(elem.name)


filesystem = FileSystem()
R = 1
if R:
    command = input('-> ')
    while command != 'q':
        execute_command(filesystem, command)
        command = input('-> ')
else:
    command = 'mkdir home /'
    execute_command(filesystem, command)
