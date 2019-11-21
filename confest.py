from collections import Counter
from faker import Faker

from elasticsearch_types.livesearch import (
    LiveSearchContextsDoc,
    LiveSearchSuggestDoc,
    LiveSearchDoc,
    ELASTICSEARCH_HOST_URL,
    ELASTICSEARCH_AUTOCOMPLETE_INDEX,
)

fake = Faker()

PLOT_DIR = "/plots/"


@pytest.fixture
def get_host_url():
    return ELASTICSEARCH_HOST_URL


@pytest.fixture
def get_autocomplete_index():
    return ELASTICSEARCH_AUTOCOMPLETE_INDEX


# @pytest.fixture
# def create_livesearch_suggest(create_livesearch_contexts):
#     def _create(object_type, **kwargs):
#         document = LiveSearchSuggestDoc(input=kwargs.get("name") or fake.name(), weight=kwargs.get("weight") or 1)
#         contexts = create_livesearch_contexts(object_type, **kwargs)

#         document.add_contexts(contexts)

#         return document

#     return _create


# @pytest.fixture
# def make_org_livesearch_suggestion_from_es_doc(client):
#     def _make(doc):
#         return client.LiveSearchSuggestion(
#             org=client.LiveSearchOrg(
#                 id_org=doc["id_org"],
#                 id_company=doc["id_company"],
#                 id_investor=doc["id_investor"],
#                 name=doc["name"],
#                 url=doc["url"],
#             )
#         )

#     return _make
