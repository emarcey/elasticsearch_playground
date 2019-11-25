from make_compare_query import compare_queries
from const import SEARCH_TERMS, ID_ORGS

index = ""


def make_unnested_search_term_maker(search_term_field: str, search_term_values):
    def _make_unnested_search_term_query(query_val: str, es_from: int, es_size: int):
        return {
            "_source": False,
            "explain": False,
            "from": es_from,
            "size": es_size,
            "query": {
                "bool": {
                    "must": [
                        {"terms": {search_term_field: search_term_values}},
                        {
                            "bool": {
                                "should": [
                                    {
                                        "constant_score": {
                                            "boost": 22,
                                            "filter": {"match": {"search_term_org_name.keyword": {"query": query_val}}},
                                        }
                                    },
                                    {
                                        "bool": {
                                            "must_not": {
                                                "range": {
                                                    "search_term_org_num_exits": {
                                                        "from": 1,
                                                        "include_lower": True,
                                                        "include_upper": True,
                                                        "to": None,
                                                    }
                                                }
                                            },
                                            "should": [
                                                {
                                                    "constant_score": {
                                                        "boost": 9,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_name": {"query": query_val}
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "search_term_org_url.keyword": query_val
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 9,
                                                        "filter": {
                                                            "bool": {
                                                                "must": {
                                                                    "match_phrase": {
                                                                        "search_term_org_description": {
                                                                            "query": query_val,
                                                                            "slop": 5,
                                                                        }
                                                                    }
                                                                },
                                                                "must_not": {
                                                                    "match_phrase": {
                                                                        "search_term_org_name": {"query": query_val}
                                                                    }
                                                                },
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 6,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "org_competitor": {"query": query_val}
                                                                        }
                                                                    },
                                                                    {"prefix": {"competitor_url.keyword": query_val}},
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 3,
                                                        "filter": {
                                                            "prefix": {
                                                                "search_term_org_investor_name.keyword": query_val
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "nested": {
                                                        "path": "org_news_noun_phrases",
                                                        "query": {
                                                            "function_score": {
                                                                "functions": [
                                                                    {
                                                                        "field_value_factor": {
                                                                            "field": "org_news_noun_phrases.containing_org_article_percentage",
                                                                            "missing": 0,
                                                                        }
                                                                    }
                                                                ],
                                                                "query": {
                                                                    "constant_score": {
                                                                        "filter": {
                                                                            "match_phrase": {
                                                                                "org_news_noun_phrases.noun_phrase": {
                                                                                    "query": query_val
                                                                                }
                                                                            }
                                                                        }
                                                                    }
                                                                },
                                                            }
                                                        },
                                                    }
                                                },
                                            ],
                                        }
                                    },
                                ]
                            }
                        },
                    ]
                }
            },
        }

    return _make_unnested_search_term_query


def main():
    num_iterations = 50
    max_pages = 5
    num_search_terms = 25
    es_sizes = [10, 25, 50]
    max_orgs = 10000

    str_id_orgs = list(map(str, ID_ORGS))

    org_int_search_term = make_unnested_search_term_maker("org_key_int", ID_ORGS)
    org_keyword_search_term = make_unnested_search_term_maker("org_key_keyword", str_id_orgs)
    org_keyword_warm_search_term = make_unnested_search_term_maker("org_key_keyword_warm", str_id_orgs)

    compare_queries(
        "OrgKeyInt Query",
        org_int_search_term,
        "OrgKeyKeyword Query",
        org_keyword_search_term,
        SEARCH_TERMS[:num_search_terms],
        0,
        es_sizes,
        num_iterations,
        index,
        "terms_org_key_int_vs_org_key_keyword",
    )

    compare_queries(
        "OrgKeyInt Query",
        org_int_search_term,
        "OrgKeyKeyword Warm Query",
        org_keyword_warm_search_term,
        SEARCH_TERMS[:num_search_terms],
        0,
        es_sizes,
        num_iterations,
        index,
        "terms_org_key_int_vs_org_key_keyword_warm",
    )
    compare_queries(
        "OrgKeyKeyword Query",
        org_keyword_search_term,
        "OrgKeyKeyword Warm Query",
        org_keyword_warm_search_term,
        SEARCH_TERMS[:num_search_terms],
        0,
        es_sizes,
        num_iterations,
        index,
        "terms_org_key_keyword_vs_org_key_keyword_warm",
    )

    # compare_queries(
    #     "IdOrgKeyInt Query",
    #     make_unnested_search_term_query_modified_exits_id_org_sort,
    #     "IdOrgKeyKeyword Warm Query",
    #     make_unnested_search_term_query_modified_exits_id_org_keyword_warm_sort,
    #     SEARCH_TERMS[:num_search_terms],
    #     0,
    #     es_sizes,
    #     num_iterations,
    #     index,
    #     "org_key_int_vs_org_key_warm_keyword",
    # )

    # compare_queries(
    #     "IdOrgKeyKeyword Query",
    #     make_unnested_search_term_query_modified_exits_id_org_keyword_sort,
    #     "IdOrgKeyKeyword Warm Query",
    #     make_unnested_search_term_query_modified_exits_id_org_keyword_warm_sort,
    #     SEARCH_TERMS[:num_search_terms],
    #     0,
    #     es_sizes,
    #     num_iterations,
    #     index,
    #     "org_key_int_vs_org_key_keyword_warm",
    # )

    # compare_queries(
    #     "Nested Search Term Query",
    #     make_nested_search_term_query,
    #     "Nested Search Term Without NPs Query",
    #     make_nested_search_term_query_no_nps,
    #     SEARCH_TERMS[:20],
    #     0,
    #     [25],  # , 25, 50, 100],
    #     num_iterations,
    #     index,
    # )


if __name__ == "__main__":
    main()
