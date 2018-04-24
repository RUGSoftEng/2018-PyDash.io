from flask import send_from_directory

from pydash_web.static import static


@static.route('/service-worker.js')
def serve_worker():
    return send_from_directory('../../pydash-front/build', 'service-worker.js')


@static.route('/', defaults={'path': ''})
@static.route('/<path:path>')
def serve_react(path):
    return send_from_directory('../../pydash-front/build', 'index.html')
