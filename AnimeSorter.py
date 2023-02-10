from FileManager import Directory, File
import re

class AnimeFile(File):
    def __init__(self, absolute_path:str) -> bool:
        super().__init__(absolute_path)
        self.anime_title = re.sub("[\(\[].*?[\)\]]", "", file.file_name)
        episode_split = self.anime_title.rfind(" - ");
        self.anime_title, self.anime_episode = self.anime_title[:episode_split], self.anime_title[episode_split:]
        self.anime_title = self.anime_title.strip();
        
main_directory = Directory("F:\\Downloads")
for file in main_directory.get_files():
    anime = AnimeFile(file.absolute_path)
    if (anime.file_extension != ".mkv"):
        continue
    new_location = anime.parent_path+"\\"+anime.anime_title
    directory = Directory(new_location)
    if not directory.exists():
        directory.create()
    anime.move(new_location)