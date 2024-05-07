import os
from logic.api_handler import api_handler
from logic.logging_handler import logger


def check_path_exists(path):
    return os.path.exists(path)


class File_Handler:
    def __init__(self):
        self.path = ""

    def setup(self, config):
        self.path = config["path"]

    def delete(self, files):
        for file in files:
            os.remove(self.path + file)

    def move(self, files):
        for file in files:
            os.rename(self.path + file["source"] + file["name"], self.path + file["location"] + file["name"])

    def download(self, files_ids):
        for file_id in files_ids:
            file = api_handler.download_file(file_id)
            with open(self.path + file_id, "wb") as f:
                f.write(file.content)

    def rename(self, files):
        for file in files:
            name = file["name"]
            new_name = file["new_name"]
            path = file["path"]
            os.rename(self.path + path + name, self.path + path + new_name)

    def download_base_game(self, provider, content):
        if provider == "steam":
            if content["mode"] == "live":
                steamid = content["app_id"]
                os.system(f"steam://run/{steamid}")
                return True
            else:
                # todo add either STEAM logic or DepotDownloader logic here
                app_id = content["app_id"]
                depot_id = content["depot_id"]
                manifest_id = content["manifest_id"]
                pass
        elif provider == "battlenet":
            # todo add code to download bnetinstaller
            product = content["product"]
            uid = content["uid"]
            lang = content["lang"]
            pass
        elif provider == "epic":
            pass
        elif provider == "origin":
            pass
        elif provider == "uplay":
            pass
        elif provider == "web":
            pass
        else:
            return None

    def patcher(self, content):
        try:
            instructions = content["instructions"]
            provider = content["provider"]
            if provider == "steam":
                steam = content["steam"]
                app_id = steam["app_id"]
                path = "aaaaa"
                # todo on patch add relative path
            else:
                path = "bbbbb"

            path_exists = check_path_exists(path)
            if not path_exists:
                logger.log(level="error", handler="file_handler", message=f"Path does not exist: {path}")
                return False

            if "delete" in instructions:
                self.delete(instructions["delete"])
            if "move" in instructions:
                self.move(instructions["move"])
            if "download" in instructions:
                self.download(instructions["download"])
            if "rename" in instructions:
                self.rename(instructions["rename"])
            return True
        except Exception as e:
            print("Error patching game:", e)
            return False


file_handler = File_Handler()
