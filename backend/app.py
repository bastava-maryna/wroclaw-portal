"""entry point"""
from distutils.log import debug
from main import create_app

# from src.uni import data_loader

app = create_app()
# data_loader()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
