import uvicorn


if __name__ == "__main__":
    import os

    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")

    print(f"Starting RepoPilot AI on http://{host}:{port}", flush=True)
    uvicorn.run("main:app", host=host, port=port)
