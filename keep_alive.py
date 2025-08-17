from flask import Flask
import os
from threading import Thread

app = Flask(__name__)

@app.get("/")
def root():
    return "OK — Userbot running!"

def _run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

def keep_alive():
    t = Thread(target=_run, daemon=True)
    t.start()
