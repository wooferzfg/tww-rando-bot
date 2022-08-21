from datetime import datetime
from github import Github, InputFileContent
import os
import random
import re
import shortuuid
import string


class Generator:
    def __init__(self, github_token):
        self.github_token = github_token

    def generate_seed(self, randomizer_path, permalink, username, generate_spoiler_log):
        trimmed_name = re.sub(r'\W+', '', username)[:12]
        random_suffix = shortuuid.ShortUUID().random(length=10)
        seed_name = f"{trimmed_name}{random_suffix}"
        file_name = "".join(random.choice(string.digits) for _ in range(6))

        os.system(f"python {randomizer_path}/wwrando.py -noui -seed={seed_name} -permalink={permalink}")

        permalink_file_name = f"permalink_{seed_name}.txt"
        permalink_file = open(permalink_file_name, "r")
        permalink = permalink_file.read()
        permalink_file.close()
        os.remove(permalink_file_name)

        seed_hash_file_name = f"seed_hash_{seed_name}.txt"
        seed_hash_file = open(seed_hash_file_name, "r")
        seed_hash = seed_hash_file.read()
        seed_hash_file.close()
        os.remove(seed_hash_file_name)

        if generate_spoiler_log:
            spoiler_log_file_name = f"spoiler_log_{seed_name}.txt"
            spoiler_log_file = open(spoiler_log_file_name, "r")
            spoiler_log = spoiler_log_file.read()
            spoiler_log_file.close()
            os.remove(spoiler_log_file_name)

            timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            gh = Github(self.github_token)
            gh_auth_user = gh.get_user()
            gist = gh_auth_user.create_gist(
                public=False,
                files={f"spoiler_log_{timestamp}.txt": InputFileContent(spoiler_log)},
                description="The Wind Waker Randomizer Spoiler Log"
            )
            spoiler_log_url = gist.html_url
        else:
            spoiler_log_url = None

        return {
            "file_name": file_name,
            "permalink": permalink,
            "seed_hash": seed_hash,
            "spoiler_log_url": spoiler_log_url
        }
