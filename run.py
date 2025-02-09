import os
import sys

# Projenin kök dizinini Python path'ine ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps import create_app

app = create_app('development')

if __name__ == "__main__":
    app.run(debug=True)