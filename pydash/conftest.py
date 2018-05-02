import pytest
import pydash_app.user.repository
import pydash_app.dashboard.repository


@pytest.fixture(autouse=True)
def clean_in_memory_database(*_):
    pydash_app.user.repository.clear_all()
    pydash_app.dashboard.repository.clear_all()

