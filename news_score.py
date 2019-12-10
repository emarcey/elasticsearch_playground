from multi_compare_queries import compare_queries
from const import SEARCH_TERMS, ID_ORGS, ELASTICSEARCH_HOST_URL
from data_classes import Query, QueryParams

from const import HEADER, URL_PARAMS

index = ""


def make_score_query(query_val: str, es_from: int, es_size: int):
    return {
        "from": 0,
        "query": {
            "function_score": {
                "functions": [
                    {
                        "script_score": {
                            "script": {
                                "source": "doc['news_date'].size() == 0 ? _score/Math.log10(8640000030L) * 0.8 + 1 : ((System.currentTimeMillis() - Math.min(doc['news_date'].value.getMillis(), System.currentTimeMillis()))/86400000)<=180 ? (_score/Math.log10(1 + Math.floor(1+(System.currentTimeMillis() - Math.min(doc['news_date'].value.getMillis(), System.currentTimeMillis())))/86400000/30) * 8640000030L) * 0.8 + Math.pow(2,-0.5 * Math.floor((System.currentTimeMillis() - Math.min(doc['news_date'].value.getMillis(), System.currentTimeMillis())))/86400000/30) : (Math.log10(Math.max(_score,1) * 2) / Math.log10(2)) / Math.log10(10 + (Math.floor(System.currentTimeMillis() - doc['news_date'].value.getMillis())/86400000/30) * 8640000030L)"
                            }
                        }
                    }
                ],
                "query": {"query_string": {"fields": ["news_content^2", "news_title^1"], "query": query_val}},
            }
        },
        "sort": [{"_score": {"order": "desc"}}, {"_id": {"order": "asc"}}],
        "from": es_from,
        "size": es_size,
    }


def make_regular_query(query_val: str, es_from: int, es_size: int):
    return {
        "from": 0,
        "query": {"query_string": {"fields": ["news_content^2", "news_title^1"], "query": query_val}},
        "sort": [{"_score": {"order": "desc"}}, {"_id": {"order": "asc"}}],
        "from": es_from,
        "size": es_size,
    }


def main():
    num_iterations = 50
    num_search_terms = 25
    es_sizes = [10, 25, 50, 100]

    queries = [
        Query(query_type="Base Query", query_maker=make_regular_query),
        Query(query_type="Score Function Query", query_maker=make_score_query,),
    ]

    query_params = QueryParams(
        base_url=ELASTICSEARCH_HOST_URL,
        index=index,
        num_iterations=num_iterations,
        es_from=0,
        es_sizes=es_sizes,
        params=URL_PARAMS,
        header=HEADER,
    )

    compare_queries(queries, SEARCH_TERMS[:num_search_terms], query_params, file_descrip="news_score")


if __name__ == "__main__":
    main()
