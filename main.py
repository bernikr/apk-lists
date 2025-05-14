from datetime import datetime
from importlib import reload

import requests
from bs4 import BeautifulSoup, Tag
from flask import Flask, render_template
import operator

app = Flask(__name__)


@app.route("/")
def index() -> tuple[str, int]:
    return "", 401


@app.route("/s3/<index>")
def s3(index: str) -> str:
    base_url = f"https://{index}/"
    res = requests.get(base_url, timeout=5)
    soup = BeautifulSoup(res.text, "lxml-xml")
    files = [
        {c.name: c.text for c in f.children if isinstance(c, Tag)}
        for f in soup.find_all("Contents")
        if isinstance(f, Tag)
    ]
    files = [
        (f["Key"], f"{base_url}{f['Key']}")
        for f in sorted(files, key=operator.itemgetter("LastModified"), reverse=True)
        if f["Key"].endswith(".apk")
    ]
    return render_template("list.html", files=files)


if __name__ == "__main__":
    app.run(debug=True)  # noqa: S201
