from flask_frozen import Freezer
from aramStatAnalyzer import app  # Replace 'your_flask_app' with the name of your Flask app
import sys

freezer = Freezer(app)

# Generator for the index route
@freezer.register_generator
def index():
    yield {}

if __name__ == '__main__':
    # If running the app locally, use app.run()
    # app.run()

    # If you want to generate static files, use the following code
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run()
