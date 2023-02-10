from FileManager import Directory, File

main_directory = Directory("C:\\Users\\Admin\\Pictures\\Canon EOS R7")
for directory in main_directory.get_directories():
    raw_directory = Directory(directory.absolute_path+"\\Raw")
    raw_directory.create()
    for file in directory.get_files():
        if file.file_extension == ".CR3":
            file.move(raw_directory.absolute_path)
