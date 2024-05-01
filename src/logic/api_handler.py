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

    def setup(self, config):
        self.api_url = config["urls"]["api"]
        self.healthcheck = config["endpoints"]["healthcheck"]
        self.api_version = config["endpoints"]["api_version"]
        self.launcher_download = config["endpoints"]["launcher_download"]
        self.launcher_version = config["endpoints"]["launcher_version"]
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
        return requests.get(self.api_url + self.image + image)


api_handler = ApiHandler()
