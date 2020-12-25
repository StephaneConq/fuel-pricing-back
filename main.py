from flask import Flask
from flask_cors import CORS

from blueprints import sync_bp, stations_bp, user_bp

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

app.register_blueprint(sync_bp, url_prefix='/api/sync')
app.register_blueprint(stations_bp, url_prefix='/api/stations')
app.register_blueprint(user_bp, url_prefix='/api/user')


@app.route('/')
def ok():
    return 'ok'


if __name__ == '__main__':
    app.run()
