from multi_compare_queries import compare_queries
from const import TERRY_TERMS, ELASTICSEARCH_HOST_URL
from data_classes import Query, QueryParams

from const import HEADER, URL_PARAMS

index = ""


def make_new_query(query_val: str, es_from: int, es_size: int):
    return {
        "_source": True,
        "explain": False,
        "from": es_from,
        "size": es_size,
        "query": {
            "bool": {
                "filter": {"range": {"id_company": {"from": "0", "include_lower": False, "include_upper": True}}},
                "must": {
                    "bool": {
                        "should": [
                            {
                                "constant_score": {
                                    "boost": 22,
                                    "filter": {"match": {"org_name.keyword": {"query": query_val}}},
                                }
                            },
                            {
                                "constant_score": {
                                    "boost": 9,
                                    "filter": {
                                        "bool": {
                                            "should": [
                                                {"match_phrase": {"org_name": {"query": query_val}}},
                                                {"prefix": {"search_term_org_url_no_exits.keyword": query_val}},
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
                                                    "search_term_org_description_no_name_no_exits": {
                                                        "query": query_val,
                                                        "slop": 5,
                                                    }
                                                }
                                            },
                                            "must_not": {"match_phrase": {"org_name": {"query": query_val}}},
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
                                                        "search_term_org_competitor_no_exits": {"query": query_val}
                                                    }
                                                },
                                                {
                                                    "prefix": {
                                                        "search_term_org_competitor_url_no_exits.keyword": query_val
                                                    }
                                                },
                                            ]
                                        }
                                    },
                                }
                            },
                            {
                                "constant_score": {
                                    "boost": 3,
                                    "filter": {"prefix": {"search_term_org_investor_name_no_exits.keyword": query_val}},
                                }
                            },
                            {
                                "dis_max": {
                                    "queries": [
                                        {
                                            "constant_score": {
                                                "boost": 1,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_one_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.85,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_two_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.5,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_three_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.15,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_four_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                    ]
                                }
                            },
                        ]
                    }
                },
            }
        },
        "sort": [
            {"_score": {"order": "desc"}},
            {"org_last_funding_funding_date": {"order": "desc"}},
            {"index_key": {"order": "asc"}},
        ],
    }


def make_old_query(query_val: str, es_from: int, es_size: int):
    return {
        "_source": True,
        "explain": False,
        "from": es_from,
        "size": es_size,
        "query": {
            "bool": {
                "must": {
                    "bool": {
                        "should": [
                            {
                                "nested": {
                                    "path": "org",
                                    "query": {
                                        "constant_score": {
                                            "boost": 22,
                                            "filter": {"match": {"org.org_name.keyword": {"query": query_val}}},
                                        }
                                    },
                                }
                            },
                            {
                                "bool": {
                                    "must_not": {
                                        "nested": {
                                            "path": "org",
                                            "query": {
                                                "range": {
                                                    "org.org_num_exits": {
                                                        "from": 1,
                                                        "include_lower": True,
                                                        "include_upper": True,
                                                        "to": None,
                                                    }
                                                }
                                            },
                                        }
                                    },
                                    "should": [
                                        {
                                            "nested": {
                                                "path": "org",
                                                "query": {
                                                    "constant_score": {
                                                        "boost": 9,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "org.org_name": {"query": query_val}
                                                                        }
                                                                    },
                                                                    {"prefix": {"org.org_url.keyword": query_val}},
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "nested": {
                                                "path": "org",
                                                "query": {
                                                    "constant_score": {
                                                        "boost": 9,
                                                        "filter": {
                                                            "bool": {
                                                                "must": {
                                                                    "match_phrase": {
                                                                        "org.org_description": {
                                                                            "query": query_val,
                                                                            "slop": 5,
                                                                        }
                                                                    }
                                                                },
                                                                "must_not": {
                                                                    "match_phrase": {
                                                                        "org.org_name": {"query": query_val}
                                                                    }
                                                                },
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
                                                            {"match_phrase": {"org_competitor": {"query": query_val}}},
                                                            {"prefix": {"competitor_url.keyword": query_val}},
                                                        ]
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "nested": {
                                                "path": "org_investor",
                                                "query": {
                                                    "constant_score": {
                                                        "boost": 3,
                                                        "filter": {
                                                            "prefix": {"org_investor.org_name.keyword": query_val}
                                                        },
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
            }
        },
        "sort": [
            {"_score": {"order": "desc"}},
            {"org_last_funding.funding_date": {"nested": {"path": "org_last_funding"}, "order": "desc"}},
            {"org.org_num_deals": {"nested": {"path": "org"}, "order": "desc"}},
            {"_id": {"order": "asc"}},
        ],
    }


def main():
    num_iterations = 10
    # num_search_terms = 25
    es_sizes = [10, 25, 50, 100]

    queries = [
        Query(query_type="Old Query", query_maker=make_old_query, index_override="org-12"),
        Query(query_type="New Query", query_maker=make_new_query, index_override="org-16"),
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

    compare_queries(queries, TERRY_TERMS, query_params, file_descrip="old_vs_new")


if __name__ == "__main__":
    main()
