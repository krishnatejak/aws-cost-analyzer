from flask import Flask
from flask_cors import CORS
from routes import init_routes
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

init_routes(app)

@app.route('/health')
def health_check():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)