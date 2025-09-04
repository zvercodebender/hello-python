from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    y = 0
    x = 1 / y
    return "Hello Digital.ai!<br><h1>#GoTeam!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
