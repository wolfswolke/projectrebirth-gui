import os
import shutil
from logic.api_handler import api_handler
from logic.logging_handler import logger
from logic.steam_parser import steam_parser


def check_path_exists(path):
    return os.path.exists(path)


def delete(files, base_path):
    try:
        for file in files:
            try:
                if os.path.isfile(base_path + file):
                    os.remove(base_path + file)
                else:
                    shutil.rmtree(base_path + file)
                logger.log(level="info", handler="file_handler", message=f"Deleted file: {file}")
            except FileNotFoundError:
                logger.log(level="info", handler="file_handler", message=f"File already deleted: {file}")
                pass
        return True
    except Exception as e:
        logger.log(level="error", handler="file_handler_delete", message=e)
        return False


def move(files, base_path):
    try:
        for file in files:
            os.rename(base_path + file["source"] + file["name"], base_path + file["location"] + file["name"])
            logger.log(level="info", handler="file_handler", message=f"Moved file: {file['name']}")
        return True
    except Exception as e:
        logger.log(level="error", handler="file_handler_move", message=e)
        return False


def download(files, base_path):
    try:
        for file in files:
            file_url = file["url"]
            location = file["location"]
            file_name = file["name"]
            file_data = api_handler.download_file(file_url)
            with open(base_path + location + file_name, "wb") as f:
                f.write(file_data.content)
            logger.log(level="info", handler="file_handler", message=f"Downloaded file: {file_name}")
        return True
    except Exception as e:
        logger.log(level="error", handler="file_handler_download", message=e)
        return False


def rename(files, base_path):
    try:
        for file in files:
            base_path = base_path + file["location"]
            name = file["name"]
            new_name = file["new_name"]
            try:
                os.rename(base_path + name, base_path + new_name)
            except FileNotFoundError:
                logger.log(level="info", handler="file_handler", message=f"File already renamed: {name}")
                pass
        return True
    except Exception as e:
        logger.log(level="error", handler="file_handler_rename", message=e)
        return False


def download_base_game(game_id):
    content = api_handler.get_patch(game_id).json()
    print(content)
    provider = content["provider"]
    provider_data = content["provider_data"]
    if provider == "steam":
        if provider_data["mode"] == "live":
            steamid = provider_data["app_id"]
            os.system(f"start steam://install/{steamid}")
            return True
        else:
            # todo add either STEAM logic or DepotDownloader logic here
            app_id = provider_data["app_id"]
            depot_id = provider_data["depot_id"]
            manifest_id = provider_data["manifest_id"]
            logger.log(level="info", handler="file_handler", message=f"Downloading game: {app_id} with depot: {depot_id} and manifest: {manifest_id}")
            pass
    elif provider == "battlenet":
        # todo add code to download bnetinstaller
        product = provider_data["product"]
        uid = provider_data["uid"]
        lang = provider_data["lang"]
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


class File_Handler:
    def __init__(self):
        self.path = ""

    def setup(self, config):
        self.path = config["path"]

    def patcher(self, content):
        # error codes: 0 OK, 1 base path does not exist, 2 error deleting file, 3 error moving file, 4 error downloading file, 5 error renaming file,
        # 9 UNKNOWN ERROR
        try:
            instructions = content["instructions"]
            print(instructions)
            provider = content["provider"]
            if provider == "steam":
                steam = content["steam"]
                app_id = steam["app_id"]
                path = steam_parser.get_path(app_id)
                base_path = f"{path}\\steamapps\\common\\"
            else:
                base_path = "bbbbb"

            path_exists = check_path_exists(base_path)
            if not path_exists:
                logger.log(level="error", handler="file_handler", message=f"Base path does not exist: {base_path}")
                return 1

            if "delete" in instructions:
                ret_del = delete(instructions["delete"], base_path)
                if not ret_del:
                    return 2
            if "move" in instructions:
                ret_mov = move(instructions["move"], base_path)
                if not ret_mov:
                    return 3
            if "download" in instructions:
                ret_dow = download(instructions["download"], base_path)
                if not ret_dow:
                    return 4
            if "rename" in instructions:
                ret_ren = rename(instructions["rename"], base_path)
                if not ret_ren:
                    return 5
            return 0
        except Exception as e:
            logger.log(level="error", handler="file_handler", message=e)
            return 9

    def download_base_game(self, game_id):
        return download_base_game(game_id)


file_handler = File_Handler()
