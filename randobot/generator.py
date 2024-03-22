import base64
import enum
import os
import random
import re
import string
import struct
from datetime import datetime

import shortuuid
from github import Auth, Github, InputFileContent


class ArgFormat(enum.Enum):
    V110 = '-noui -seed={seed_name} -permalink={permalink}'
    V111 = '--noui --dry --seed={seed_name} --permalink={permalink}'
    RS14 = '--randobot --noui --dry --seed={seed_name} --permalink={permalink}'


class Generator:
    def __init__(self, github_token):
        self.github_token = github_token

    def generate_seed(self, randomizer_path, permalink, username, generate_spoiler_log,
                      args_format: ArgFormat = ArgFormat.V110):
        trimmed_name = re.sub(r'\W+', '', username)[:12]
        random_suffix = shortuuid.ShortUUID().random(length=10)
        seed_name = f"{trimmed_name}{random_suffix}"
        file_name = "".join(random.choice(string.digits) for _ in range(6))

        os.system(
            f"/venv/{randomizer_path}/bin/python {randomizer_path}/wwrando.py " +
            args_format.value.format(seed_name=seed_name, permalink=permalink)
        )

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
            auth = Auth.Token(self.github_token)
            gh = Github(auth=auth)
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

    @staticmethod
    def encode_permalink(version, seed, bit_array):
        # NOTE: This function only works with the official 1.10 version of the randomizer!

        # Start the permalink with the version number and seed name
        permalink = b""
        permalink += version
        permalink += b"\0"
        permalink += seed
        permalink += b"\0"

        # Unpack the bytes object as a bit array
        bit_array = bit_array[::-1]
        bytes_array = [bit_array[i : i + 8] for i in range(0, len(bit_array), 8)]
        for byte in bytes_array:
            byte = int("".join(byte[::-1]), 2)
            permalink += struct.pack(">B", byte)

        return base64.b64encode(permalink).decode("ascii")

    @staticmethod
    def decode_permalink(base64_encoded_permalink):
        # NOTE: This function only works with the official 1.10 version of the randomizer!

        # Decode permalink into a bytes object
        permalink = base64.b64decode(base64_encoded_permalink)

        # Split the permalink into the version, seed name, and option bits
        version, seed, options_bytes = permalink.split(b"\0", 2)

        # Unpack the option bytes object as a bit array
        option_bytes = struct.unpack(f">{'B'*len(options_bytes)}", options_bytes)
        bit_array = []
        for byte in option_bytes:
            bit_array.extend(list(bin(byte)[2:].zfill(8))[::-1])
        bit_array = bit_array[::-1]

        return version, seed, bit_array

    @staticmethod
    def apply_ra_modifier(base_permalink, modifier):
        # NOTE: This function only works with the official 1.10 version of the randomizer!

        # Convert the permalink to a bit array
        version, seed, bit_array = Generator.decode_permalink(base_permalink)

        # Modify bit array depending on modifier
        match modifier:
            case "4drm":
                bit_array[87] = "0"
                bit_array[88] = "1"
                bit_array[89] = "1"
            case "nosword":
                bit_array[98] = "0"
                bit_array[99] = "1"
            case "der":
                bit_array[142] = "0"
                bit_array[143] = "0"
                bit_array[144] = "1"
            case "keys":
                bit_array[145] = "1"
            case "tingle":
                bit_array[149] = "1"
            case "expen":
                bit_array[151] = "1"
            case "subs":
                bit_array[156] = "1"
            case "minis":
                bit_array[160] = "1"
            case "combat":
                bit_array[164] = "1"

        # Encode updated bit array back into a permalink
        updated_permalink = Generator.encode_permalink(version, seed, bit_array)

        return updated_permalink

    @staticmethod
    def update_hint_distribution_for_ra(base_permalink):
        # NOTE: This function only works with the official 1.10 version of the randomizer!

        # Convert the permalink to a bit array
        version, seed, bit_array = Generator.decode_permalink(base_permalink)

        # Set the number of location hints to 8
        bit_array[119] = "1"
        bit_array[120] = "0"
        bit_array[121] = "0"
        bit_array[122] = "0"

        # Set the number of barren hints to 5
        bit_array[123] = "0"
        bit_array[124] = "1"
        bit_array[125] = "0"
        bit_array[126] = "1"

        # Encode updated bit array back into a permalink
        updated_permalink = Generator.encode_permalink(version, seed, bit_array)

        return updated_permalink
