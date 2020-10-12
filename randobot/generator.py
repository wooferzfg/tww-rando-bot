from datetime import datetime
from github import Github, InputFileContent
import os
import random
import string
import uuid

class Generator:
    def __init__(self, github_token):
        self.github_token = github_token

    def generate_seed(self):
        seed_name = uuid.uuid4()
        file_name = "".join(random.choice(string.ascii_uppercase) for _ in range(6))
        os.system(f"python wwrando/wwrando.py -seed={seed_name} -permalink=MS44LjAATmljZUFjY29tbW9kYXRpbmdLb3JvawAXAwYCDxDADAAAAAAAAAA=")
        permalink_file_name = f"permalink_{seed_name}.txt"
        permalink_file = open(permalink_file_name, "r")
        permalink = permalink_file.read()
        permalink_file.close()
        os.remove(permalink_file_name)

        spoiler_log_file_name = f"spoiler_log_{seed_name}.txt"
        spoiler_log_file = open(spoiler_log_file_name, "r")
        spoiler_log = spoiler_log_file.read()
        spoiler_log_file.close()
        os.remove(spoiler_log_file_name)

        timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        gh = Github(self.github_token)
        gh_auth_user = gh.get_user()
        gist = gh_auth_user.create_gist(
            public=False,
            files={f"spoiler_log_{timestamp}.txt": InputFileContent(spoiler_log)},
            description="The Wind Waker Randomizer Spoiler Log"
        )
        spoiler_log_url = gist.html_url

        return {
            "permalink": permalink,
            "file_name": file_name,
            "spoiler_log_url": spoiler_log_url
        }
