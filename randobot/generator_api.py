import os
from fastapi import FastAPI
from randobot.generator import Generator, RandomizerPath

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "This is randobot"}


@app.post("/generate")
def generate_seed(
    randomizer_path: RandomizerPath,
    permalink: str,
    username: str,
    generate_spoiler_log: bool,
):
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("Could not load GitHub token")

    generator = Generator(github_token=github_token)
    result = generator.generate_seed(
        randomizer_path=randomizer_path,
        permalink=permalink,
        username=username,
        generate_spoiler_log=generate_spoiler_log,
    )
    return result
