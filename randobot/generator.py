import enum
import os
import random
import re
import string
from datetime import datetime
from typing import Final

import shortuuid
from github import Auth, Github, InputFileContent


class RandomizerPath(enum.Enum):
    WWRANDO = "wwrando"
    WWRANDO_S8 = "wwrando-s8"
    WWRANDO_MINIBLINS = "wwrando-miniblins"
    WWRANDO_RANDOM_SETTINGS = "wwrando-random-settings"


class ArgFormat(enum.Enum):
    V110 = "-noui -seed={seed_name} -permalink={permalink}"
    V111 = "--noui --dry --seed={seed_name} --permalink={permalink}"
    RS14 = "--randobot --noui --dry --seed={seed_name} --permalink={permalink}"


ARG_FORMAT_FOR_RANDOMIZER_PATH: Final[dict[RandomizerPath, ArgFormat]] = {
    RandomizerPath.WWRANDO: ArgFormat.V110,
    RandomizerPath.WWRANDO_S8: ArgFormat.V111,
    RandomizerPath.WWRANDO_MINIBLINS: ArgFormat.V111,
    RandomizerPath.WWRANDO_RANDOM_SETTINGS: ArgFormat.RS14,
}


class Generator:
    def __init__(self, github_token: str):
        self.github_token = github_token

    def generate_seed(
        self,
        randomizer_path: RandomizerPath,
        permalink: str,
        prefix: str,
        generate_spoiler_log: bool,
    ) -> dict[str, str | None]:
        trimmed_prefix = re.sub(r"\W+", "", prefix)[:12]
        random_suffix = shortuuid.ShortUUID().random(length=10)
        seed_name = f"{trimmed_prefix}{random_suffix}"
        file_name = "".join(random.choice(string.digits) for _ in range(6))
        randomizer_path_str = randomizer_path.value
        args_format = ARG_FORMAT_FOR_RANDOMIZER_PATH[randomizer_path]

        os.system(
            f"/venv/{randomizer_path_str}/bin/python {randomizer_path_str}/wwrando.py "
            + args_format.value.format(seed_name=seed_name, permalink=permalink)
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
