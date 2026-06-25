from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return {"message": "Hello from the Brick Oracle API", "status": 200}
