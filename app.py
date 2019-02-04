from core.game import run_inquisitive_with_args

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    # app.run()
    run_inquisitive_with_args()