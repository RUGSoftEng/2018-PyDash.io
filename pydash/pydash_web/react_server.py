from flask import Blueprint
import os
from flask import send_from_directory

react_server = Blueprint(
    'pydash_web.react_server',
    __name__,
    # Override the static folder since this is `/static` by default, which clashes with React's file naming.
    static_folder=None)


# Serve React App
@react_server.route('/', defaults={'path': ''})
@react_server.route('/<path:path>')
def serve(path):
    print(f"SERVING REACT PATH: {path}")
    if path != "" and os.path.exists(
            os.path.abspath("../pydash-front/build/" + path)):
        print(f"Serving file that exists: {path}")
        return send_from_directory(
            os.path.abspath('../pydash-front/build'), path)
    else:
        print("Serving standard index.html")
        return send_from_directory(
            os.path.abspath('../pydash-front/build'), 'index.html')
