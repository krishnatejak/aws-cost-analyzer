import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)