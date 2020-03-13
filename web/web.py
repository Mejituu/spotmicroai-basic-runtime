#!/Users/franferri/projects/basic-runtime/venv/bin/python3 -u

# WS server example that synchronizes state across clients


from flask import Flask, escape, request

app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'
