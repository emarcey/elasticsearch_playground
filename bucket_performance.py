from multi_compare_queries import compare_queries
from const import TERRY_TERMS, ELASTICSEARCH_HOST_URL
from data_classes import Query, QueryParams

from const import HEADER, URL_PARAMS

index = ""


def make_ten_bucket_query(query_val: str, es_from: int, es_size: int):
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
                                                    "search_term_org_description_no_exits": {
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
                                                "boost": 0.2,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_one_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.2,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_two_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.4,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_three_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.4,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_four_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.6,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_five_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.6,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_six_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.8,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_seven_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.8,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_eight_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 1,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_nine_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 1,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_ten_no_exit": {"query": query_val}
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


def make_five_bucket_query(query_val: str, es_from: int, es_size: int):
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
                                                    "search_term_org_description_no_exits": {
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
                                                "boost": 0.1,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_one_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.2,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_two_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.3,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_three_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.4,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_four_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.5,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_five_no_exit": {"query": query_val}
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


def make_three_bucket_query(query_val: str, es_from: int, es_size: int):
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
                                                    "search_term_org_description_no_exits": {
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
                                                "boost": 0.1,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_one_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.2,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_two_no_exit": {"query": query_val}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.3,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_three_no_exit": {"query": query_val}
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


def make_one_bucket_query(query_val: str, es_from: int, es_size: int):
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
                                                    "search_term_org_description_no_exits": {
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
                            {"match_phrase": {"all_org_news_noun_phrases_no_exit": {"query": query_val, "boost": 0.1}}},
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


def main():
    num_iterations = 25
    # num_search_terms = 25
    # es_sizes = [10, 25, 50, 100]
    es_sizes = [25]

    queries = [
        Query(query_type="10 Bucket Query", query_maker=make_ten_bucket_query, index_override="org-write"),
        Query(query_type="5 Bucket Query", query_maker=make_five_bucket_query, index_override="org-write"),
        Query(query_type="3 Bucket Query", query_maker=make_three_bucket_query, index_override="org-write"),
        Query(query_type="1 Bucket Query", query_maker=make_one_bucket_query, index_override="org-write"),
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
