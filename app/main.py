from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<html><body>Hello Cloudbees!<br><h1>#OSU!</h1></body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
