import enum
import os
import random
import re
import string
from datetime import datetime

import shortuuid
from github import Auth, Github, InputFileContent


class ArgFormat(enum.Enum):
    V110 = "-noui -seed={seed_name} -permalink={permalink}"
    V111 = "--noui --dry --seed={seed_name} --permalink={permalink}"
    VS7 = "--noui --dry --seed={seed_name} --permalink={permalink} --modifiers={modifiers}"
    RS14 = "--randobot --noui --dry --seed={seed_name} --permalink={permalink}"


class Generator:
    def __init__(self, github_token: str):
        self.github_token = github_token

    def generate_seed(
        self,
        randomizer_path: str,
        permalink: str,
        username: str,
        generate_spoiler_log: bool,
        modifiers: str = "",
        args_format: ArgFormat = ArgFormat.V110,
    ) -> dict[str, str | None]:
        trimmed_name = re.sub(r"\W+", "", username)[:12]
        random_suffix = shortuuid.ShortUUID().random(length=10)
        seed_name = f"{trimmed_name}{random_suffix}"
        file_name = "".join(random.choice(string.digits) for _ in range(6))

        os.system(
            f"/venv/{randomizer_path}/bin/python {randomizer_path}/wwrando.py "
            + args_format.value.format(seed_name=seed_name, permalink=permalink, modifiers=modifiers)
        )

        permalink_file_name = f"permalink_{seed_name}.txt"
        with open(permalink_file_name, "r") as permalink_file:
            permalink = permalink_file.read()
        os.remove(permalink_file_name)

        seed_hash_file_name = f"seed_hash_{seed_name}.txt"
        with open(seed_hash_file_name, "r") as seed_hash_file:
            seed_hash = seed_hash_file.read()
        os.remove(seed_hash_file_name)

        if generate_spoiler_log:
            spoiler_log_file_name = f"spoiler_log_{seed_name}.txt"
            with open(spoiler_log_file_name, "r") as spoiler_log_file:
                spoiler_log = spoiler_log_file.read()
            os.remove(spoiler_log_file_name)

            timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            auth = Auth.Token(self.github_token)
            gh = Github(auth=auth)
            gh_auth_user = gh.get_user()
            gist = gh_auth_user.create_gist(
                public=False,
                files={f"spoiler_log_{timestamp}.txt": InputFileContent(spoiler_log)},
                description="The Wind Waker Randomizer Spoiler Log",
            )
            spoiler_log_url = gist.html_url
        else:
            spoiler_log_url = None

        return {
            "file_name": file_name,
            "permalink": permalink,
            "seed_hash": seed_hash,
            "spoiler_log_url": spoiler_log_url,
        }
