import requests


class ApiHandler:
    def __init__(self):
        self.url = ""
        self.api_url = ""
        self.website_url = ""
        self.healthcheck = ""
        self.api_version = ""
        self.launcher = ""
        self.launcher_download = ""
        self.launcher_version = ""
        self.image = ""
        self.log_upload = ""
        self.bug_report = ""
        self.launcher_game = ""

    def setup(self, config):
        self.api_url = config["urls"]["api"]
        self.healthcheck = config["endpoints"]["healthcheck"]
        self.api_version = config["endpoints"]["api_version"]
        self.launcher_download = config["endpoints"]["launcher_download"]
        self.launcher_version = config["endpoints"]["launcher_version"]
        self.launcher_game = config["endpoints"]["launcher_game"]
        self.image = config["endpoints"]["image"]
        self.log_upload = config["endpoints"]["log_upload"]
        self.bug_report = config["endpoints"]["bug_report"]

    def get_healthcheck(self):
        return requests.get(self.api_url + self.healthcheck)

    def get_api_version(self):
        return requests.get(self.api_url + self.api_version)

    def upload_log(self, log):
        return requests.post(self.api_url + self.log_upload, json=log)

    def upload_bug_report(self, reporter, description, steps, expected, discord, email, attachments, logs, anonymous):
        data = {
            "Reporter": reporter,
            "Description": description,
            "Steps": steps,
            "Expected": expected,
            "Discord": discord,
            "Email": email,
            "Attachments": attachments,
            "Logs": logs,
            "Anonymous": anonymous
        }
        return requests.post(self.api_url + self.bug_report, json=data)

    def get_launcher_download(self):
        return requests.get(self.api_url + self.launcher_download)

    def get_launcher_version(self):
        return requests.get(self.api_url + self.launcher_version)

    def get_image(self, image):
        # todo remove placeholder code
        return requests.get("https://via.placeholder.com/150")
        return requests.get(self.api_url + self.image + image)

    def get_games(self):
        # Status shown, hidden
        return requests.get(self.api_url + self.launcher_game)

    def get_game(self, game):
        # Status online, maintenance, offline, error
        return requests.get(self.api_url + self.launcher_game + "/" + game)

    def get_patch(self, game):
        return requests.get(self.api_url + self.launcher_game + "/" + game + "/patch")

    def download_file(self, file_id):
        return requests.get(self.api_url + "/file" + file_id)


api_handler = ApiHandler()



# App get from API
# @app.route('/api/v1/launcher/game', methods=["GET"])
#         # Status shown, hidden
#         data = {
#             "games": [
#                 {
#                     "name": "Deathgarden Bloodharvest",
#                     "image": "https://via.placeholder.com/150",
#                     "status": "shown"
#                 },
#                 {
#                     "name": "VHS (Video Horror Society)",
#                     "image": "https://via.placeholder.com/150",
#                     "status": "shown"
#                 }
#             ]
#         }
#         return jsonify(data)
#     except TimeoutError:
#         return jsonify({"status": "error"})
#     except Exception as e:
#         logger.graylog_logger(level="error", handler="general-launcher-games", message=e)
#         return jsonify({"status": "error"})
#
#
# @app.route('/api/v1/launcher/game/<game>', methods=["GET"])
#         # Status online, maintenance, offline, error
#         logger.graylog_logger(level="info", handler="launcher_game", message=f"Game Req: {game}")
#         return jsonify({
#             "version": "1.0.0",
#             "image": "https://via.placeholder.com/150",
#             "description": "Placeholder description",
#             "team": "Team behind the rebirth",
#             "status": "online",
#             "origin": "https://store.steampowered.com/app/10/",
#             "official": True
#         })
#     except TimeoutError:
#         return jsonify({"status": "error"})
#     except Exception as e:
#         logger.graylog_logger(level="error", handler="general-launcher-game", message=e)
#         return jsonify({"status": "error"})