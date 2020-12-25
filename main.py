from flask import Flask
from flask_cors import CORS

from blueprints import sync_bp
from blueprints.stations import stations_bp

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

app.register_blueprint(sync_bp, url_prefix='/api/sync')
app.register_blueprint(stations_bp, url_prefix='/api/stations')


@app.route('/')
def ok():
    return 'ok'


if __name__ == '__main__':
    app.run()
