import pytest
from pytest_localserver.http import WSGIServer


@pytest.fixture
def testserver(request):
    """Defines the testserver funcarg"""
    import pydash_web
    server = WSGIServer(application=pydash_web.flask_webapp)
    server.start()
    request.addfinalizer(server.stop)
    return server
