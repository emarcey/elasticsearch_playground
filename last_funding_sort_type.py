from multi_compare_queries import compare_queries
from const import SEARCH_TERMS, ID_ORGS, ELASTICSEARCH_HOST_URL
from data_classes import Query, QueryParams

from const import HEADER, URL_PARAMS

index = ""


def make_unnested_search_term_maker(sort_field: str):
    def _make_unnested_search_term_query(query_val: str, es_from: int, es_size: int):
        return {
            "_source": False,
            "explain": False,
            "from": es_from,
            "size": es_size,
            "query": {
                "bool": {
                    "must": [
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
                        }
                    ]
                }
            },
            "sort": [{sort_field: {"order": "desc"}}],
        }

    return _make_unnested_search_term_query


def make_unnested_search_term_maker_with_sorts(sorts):
    def _make_unnested_search_term_query(query_val: str, es_from: int, es_size: int):
        return {
            "_source": False,
            "explain": False,
            "from": es_from,
            "size": es_size,
            "query": {
                "bool": {
                    "must": [
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
                        }
                    ]
                }
            },
            "sort": sorts,
        }

    return _make_unnested_search_term_query


def main():
    num_iterations = 5
    num_search_terms = 5
    es_sizes = [1, 2, 5]

    org_last_funding_date_round_day_sorter = make_unnested_search_term_maker("org_last_funding_date_round_day")

    org_last_funding_date_round_day_keyword_sorter = make_unnested_search_term_maker(
        "org_last_funding_date_round_day_keyword"
    )

    day_sorts = [
        {"org_last_funding_date_round_year_int": {"order": "desc"}},
        {"org_last_funding_date_round_month_int": {"order": "desc"}},
        {"org_last_funding_date_round_day_int": {"order": "desc"}},
    ]
    org_last_funding_date_day_list_of_ints_sorter = make_unnested_search_term_maker_with_sorts(day_sorts)

    org_last_funding_date_round_day_composite_int_sorter = make_unnested_search_term_maker(
        "org_last_funding_date_round_composite_int"
    )

    queries = [
        Query(query_type="OrgLastFundingDate Round Day Sort", query_maker=org_last_funding_date_round_day_sorter),
        Query(
            query_type="OrgLastFundingDate Round Day Keyword Sort",
            query_maker=org_last_funding_date_round_day_keyword_sorter,
        ),
        Query(
            query_type="OrgLastFundingDate Round Day List of Ints Sort",
            query_maker=org_last_funding_date_day_list_of_ints_sorter,
        ),
        Query(
            query_type="OrgLastFundingDate Round Day Composite Int Sort",
            query_maker=org_last_funding_date_round_day_composite_int_sorter,
        ),
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

    compare_queries(queries, SEARCH_TERMS[:num_search_terms], query_params)


if __name__ == "__main__":
    main()
