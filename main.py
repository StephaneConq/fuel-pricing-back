from flask import Flask

from blueprints import sync_bp

app = Flask(__name__)

app.register_blueprint(sync_bp, url_prefix='/api/sync')


@app.route('/')
def ok():
    return 'ok'


if __name__ == '__main__':
    app.run()
