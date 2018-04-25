"""
Fills the application with some preliminary dashboards
to make it easier to test code in development and staging environments.
"""


from pydash_app.dashboard.dashboard import Dashboard
import pydash_app.dashboard.repository as repository
import pydash_app.user.repository as user_repository

import pydash_app.dashboard.services.fetching as fetching

def seed():
    """
    For each user, stores some preliminary debug dashboards in the datastore,
    to be used during development.
    Note: for now the two dashboards that are being returned are
    identical, apart from the url.
    """

    # Clear current Dashboards-DB.
    repository.clear_all()

    # # Fill in dashboards.
    # _dev_dashboard_urls = ['http://pydash.io/', 'http://pystach.io/']
    # _dev_endpoint_calls = [EndpointCall("foo", 0.5, datetime.now(), "0.1", "None", "127.0.0.1"),
    #                        EndpointCall("foo", 0.1, datetime.now(), "0.1", "None", "127.0.0.2"),
    #                        EndpointCall("bar", 0.2, datetime.now(), "0.1", "None", "127.0.0.1"),
    #                        EndpointCall("bar", 0.2, datetime.now() - timedelta(days=1), "0.1", "None", "127.0.0.1"),
    #                        EndpointCall("bar", 0.2, datetime.now() - timedelta(days=2), "0.1", "None", "127.0.0.1")
    #                        ]
    #
    # # Instead of storing the endpoints in a list, we generate them on the fly,
    # #  to avoid users sharing the same endpoints for now, as we'd like to have a controlled environment for every user
    # #  during this stage of development.
    # for user in user_repository.all():
    #     for url in _dev_dashboard_urls:
    #         dashboard = Dashboard(url, user.get_id())
    #         for endpoint in [Endpoint("foo", True), Endpoint("bar", True)]:
    #             dashboard.add_endpoint(endpoint)
    #         for endpoint_call in _dev_endpoint_calls:
    #             dashboard.add_endpoint_call(endpoint_call)
    #         print(f'Adding dashboard {dashboard}')
    #         add(dashboard)

    # TEST
    # from pydash_app.fetching.fetching import fetch_and_add_endpoints, fetch_and_add_historic_endpoint_calls
    #for user in user_repository.all():
    for user in [user_repository.find_by_name('W-M'), user_repository.find_by_name('Koen')]:
        dashboard = Dashboard("http://136.243.248.188:9001/dashboard",
                              "cc83733cb0af8b884ff6577086b87909",
                              user.get_id())
        print(f'Adding dashboard {dashboard}')
        repository.add(dashboard)
        print(f'Fetching remote info for dashboard {dashboard}.')
        fetching.fetch_and_update_historic_dashboard_info(dashboard.id)
    print('Seeding of dashboards is done!')
