import os
from logic.api_handler import api_handler


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


file_handler = File_Handler()

# Patching instructions would look like this:
# steam = {"app_id": 480,
# "depot_id": 481,
# "manifest_id": 3183503801510301321
# }
# .\bnetinstaller.exe --prod prot --uid prometheus_test --lang enus --dir "<PATH>"
# battlenet = {
# "product": "prot",
# "uid": "prometheus_test",
# "lang": "enus"
# }
#         provider = "steam"
#         provider_value = steam
#         return jsonify({
#             "instructions": {
#                 "delete": [
#                     "path/file1",
#                     "path/sub/file2"
#                 ],
#                 "move": [
#                     {
#                         "name": "file1",
#                         "source": "path/sub/",
#                         "location": "path/sub2"
#                     }
#                 ],
#                 "download": [
#                     {
#                         "name": "game.exe",
#                         "location": "path/sub3"
#                     }
#                 ]
#             },
#             "files": [
#                 {
#                     "name": "game.exe",
#                     "id": "1238712381283"
#                 },
#                 {
#                     "name": "patch.dll",
#                     "id": "184563454568"
#                 }
#             ],
#             "provider": provider,
#             provider: provider_value
#         })
