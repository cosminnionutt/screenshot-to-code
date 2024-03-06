# Load environment variables first
from dotenv import load_dotenv

load_dotenv()

import os
from typing import Any, Coroutine
import asyncio

from evals.config import EVALS_DIR
from evals.core import generate_code_core
from evals.utils import image_to_data_url

STACK = "html_tailwind"


async def main():
    INPUT_DIR = EVALS_DIR + "/inputs"
    OUTPUT_DIR = EVALS_DIR + "/outputs"

    # Get all the files in the directory (only grab pngs)
    evals = [f for f in os.listdir(INPUT_DIR) if f.endswith(".png")]

    tasks: list[Coroutine[Any, Any, str]] = []
    for filename in evals:
        filepath = os.path.join(INPUT_DIR, filename)
        data_url = await image_to_data_url(filepath)
        task = generate_code_core(data_url, STACK)
        tasks.append(task)

    results = await asyncio.gather(*tasks)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename, content in zip(evals, results):
        # File name is derived from the original filename in evals
        output_filename = f"{os.path.splitext(filename)[0]}.html"
        output_filepath = os.path.join(OUTPUT_DIR, output_filename)
        with open(output_filepath, "w") as file:
            file.write(content)


asyncio.run(main())
