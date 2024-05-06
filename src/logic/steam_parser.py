
class SteamLibraryFoldersParser:
    def __init__(self):
        self.default_path = "C:\\Program Files (x86)\\Steam\\steamapps\\libraryfolders.vdf"
        self.custom_path = ""
        self.games = []

    def setup(self, config):
        self.custom_path = config["steam"]["custom_path"]

    def add_game(self, app_id, path):
        self.games.append({"app_id": app_id, "path": path})

    def get_games(self):
        return self.games

    def get_path(self, app_id):
        for game in self.games:
            if game["app_id"] == app_id:
                return game["path"]
        return None

    def parse(self):
        if self.custom_path == "":
            file_path = self.default_path
        else:
            file_path = self.custom_path
        current_path = None
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            current_path = ""
            for line in lines:
                if line.startswith('\t\t"path"'):
                    current_path = line.split('\t\t"path"')[1].strip()
                elif line.startswith('\t\t\t'):
                    obj = line.split('\t\t\t')[1].strip()
                    app_id = int(obj.split('"')[1])
                    self.add_game(app_id, current_path)


steam_parser = SteamLibraryFoldersParser()

if __name__ == "__main__":
    steam_parser.parse()
    print(steam_parser.get_games())
    print(steam_parser.get_path(555440))


