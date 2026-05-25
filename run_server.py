import os

import uvicorn


os.environ["DEBUG"] = "false"

print("Starting GitHub Repo Analyzer on http://127.0.0.1:8000", flush=True)
uvicorn.run("main:app", host="127.0.0.1", port=8000)
