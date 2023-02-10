import os, shutil
class Metadata:
    def __init__(self, absolute_path):
        self.absolute_path = absolute_path
        self.parent_path = os.path.dirname(os.path.realpath(self.absolute_path))+"\\"
    
    def exists(self) -> bool:
        return os.path.exists(self.absolute_path)

    def get_parent_directory(self):
        return Directory(self.parent_path)

    def rename(self, new_name):
        shutil.move(self.absolute_path, self.parent_path+new_name)

    def move(self, location):
        shutil.move(self.absolute_path, location)

    def is_file(self) -> bool:
        return os.path.isfile(self.absolute_path)
    
    def is_directory(self) -> bool:
        return os.path.isdir(self.absolute_path)

class File(Metadata):
    def __init__(self, absolute_path:str):
        super().__init__(absolute_path)
        if not (os.path.isfile(absolute_path)):
            raise Exception("Not a file")
        self.full_file_name = os.path.basename(self.absolute_path)
        self.file_name, self.file_extension = os.path.splitext(self.full_file_name)
        self.directory_path = os.path.dirname(os.path.realpath(self.absolute_path))+"\\"
    
    def move(self, new_location):
        if (isinstance(new_location, str)):
            if not os.path.exists(new_location):
                print(f'{new_location} does not exist')
            super().move(new_location)
        elif (isinstance(new_location, Directory)):
            new_path = new_location.absolute_path+"\\"+self.full_file_name
            super().move(new_path)

    def rename(self, new_name):
        new_extension = new_name.rsplit('.', 1)
        if len(new_extension) == 1:
            new_name += self.file_extension
        super().rename(new_name)

    def get_extension(self) -> str:
        return self.file_extension

    def __repr__(self) -> str:
        return f'{self.full_file_name}'

class Directory(Metadata):
    def __init__(self, absolute_path:str):
        super().__init__(absolute_path)
        self.absolute_path = self.absolute_path if self.absolute_path[-1] == "\\" else self.absolute_path + "\\"
        self.folder_name = os.path.basename(self.absolute_path)

    def get_files(self) -> list:
        files = []
        for file in (next(os.walk(self.absolute_path), (None, None, []))[2]):
            file_absolute_path = self.absolute_path+"\\"+file
            files.append(File(file_absolute_path))
        return files
    
    def get_directories(self) -> list:
        directories = []
        for directory in (next(os.walk(self.absolute_path), (None, [], None))[1]):
            file_absolute_path = self.absolute_path+"\\"+directory
            directories.append(Directory(file_absolute_path))
        return directories

    def get_everything(self) -> list:
        everything = []
        everything += self.get_directories()
        everything += self.get_files()
        return everything

    def create(self) -> bool:
        if not os.path.exists(self.absolute_path):
            os.makedirs(self.absolute_path)
            return True
        return False

    def __repr__(self) -> str:
        return f'{self.folder_name}'

def retrieve(absolute_path):
    if os.path.isdir(absolute_path):  
        return Directory(absolute_path)
    elif os.path.isfile(absolute_path):  
        return File(absolute_path)
    return None