from make_compare_query import compare_queries
from const import SEARCH_TERMS

index = ""


def make_nested_search_term_query(query_val: str, es_from: int, es_size: int):
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


def make_nested_search_term_query_no_nps(query_val: str, es_from: int, es_size: int):
    return {
        "_source": False,
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


def make_unnested_search_term_query(query_val: str, es_from: int, es_size: int):
    return {
        "_source": False,
        "explain": False,
        "from": es_from,
        "size": es_size,
        "query": {
            "bool": {
                "must": {
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
                                                            {"prefix": {"search_term_org_url.keyword": query_val}},
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
                                                            {"match_phrase": {"org_competitor": {"query": query_val}}},
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
                                                    "prefix": {"search_term_org_investor_name.keyword": query_val}
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
            {"search_term_org_last_funding_date": {"order": "desc"}},
            {"search_term_org_num_deals": {"order": "desc"}},
            {"_id": {"order": "asc"}},
        ],
    }


def make_unnested_search_term_query_modified_exits(query_val: str, es_from: int, es_size: int):
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
                                "constant_score": {
                                    "boost": 22,
                                    "filter": {"match": {"search_term_org_name.keyword": {"query": query_val}}},
                                }
                            },
                            {
                                "constant_score": {
                                    "boost": 9,
                                    "filter": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "match_phrase": {
                                                        "search_term_org_name_no_exits": {"query": query_val}
                                                    }
                                                },
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
                                                    "search_term_org_description_no_name": {
                                                        "query": query_val,
                                                        "slop": 5,
                                                    }
                                                }
                                            }
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
                                                {"match_phrase": {"org_competitor_no_exits": {"query": query_val}}},
                                                {"prefix": {"competitor_url_no_exits.keyword": query_val}},
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
                                                            "org_news_noun_phrases.noun_phrase": {"query": query_val}
                                                        }
                                                    }
                                                }
                                            },
                                        }
                                    },
                                }
                            },
                        ]
                    }
                }
            }
        },
        "sort": [
            {"_score": {"order": "desc"}},
            # {"search_term_org_last_funding_date": {"order": "desc"}},
            # {"search_term_org_num_deals": {"order": "desc"}},
            {"_id": {"order": "asc"}},
        ],
    }


def make_unnested_search_term_query_modified_exits_id_org_sort(query_val: str, es_from: int, es_size: int):
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
                                "constant_score": {
                                    "boost": 22,
                                    "filter": {"match": {"search_term_org_name.keyword": {"query": query_val}}},
                                }
                            },
                            {
                                "constant_score": {
                                    "boost": 9,
                                    "filter": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "match_phrase": {
                                                        "search_term_org_name_no_exits": {"query": query_val}
                                                    }
                                                },
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
                                                    "search_term_org_description_no_name": {
                                                        "query": query_val,
                                                        "slop": 5,
                                                    }
                                                }
                                            }
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
                                                {"match_phrase": {"org_competitor_no_exits": {"query": query_val}}},
                                                {"prefix": {"competitor_url_no_exits.keyword": query_val}},
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
                                                            "org_news_noun_phrases.noun_phrase": {"query": query_val}
                                                        }
                                                    }
                                                }
                                            },
                                        }
                                    },
                                }
                            },
                        ]
                    }
                }
            }
        },
        "sort": [
            {"_score": {"order": "desc"}},
            # {"search_term_org_last_funding_date": {"order": "desc"}},
            # {"search_term_org_num_deals": {"order": "desc"}},
            {"org_key_int": {"order": "asc"}},
        ],
    }


def make_unnested_search_term_query_modified_exits_id_org_keyword_sort(query_val: str, es_from: int, es_size: int):
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
                                "constant_score": {
                                    "boost": 22,
                                    "filter": {"match": {"search_term_org_name.keyword": {"query": query_val}}},
                                }
                            },
                            {
                                "constant_score": {
                                    "boost": 9,
                                    "filter": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "match_phrase": {
                                                        "search_term_org_name_no_exits": {"query": query_val}
                                                    }
                                                },
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
                                                    "search_term_org_description_no_name": {
                                                        "query": query_val,
                                                        "slop": 5,
                                                    }
                                                }
                                            }
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
                                                {"match_phrase": {"org_competitor_no_exits": {"query": query_val}}},
                                                {"prefix": {"competitor_url_no_exits.keyword": query_val}},
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
                                                            "org_news_noun_phrases.noun_phrase": {"query": query_val}
                                                        }
                                                    }
                                                }
                                            },
                                        }
                                    },
                                }
                            },
                        ]
                    }
                }
            }
        },
        "sort": [
            {"_score": {"order": "desc"}},
            # {"search_term_org_last_funding_date": {"order": "desc"}},
            # {"search_term_org_num_deals": {"order": "desc"}},
            {"org_key_keyword": {"order": "asc"}},
        ],
    }


def make_unnested_search_term_query_modified_exits_id_org_keyword_warm_sort(query_val: str, es_from: int, es_size: int):
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
                                "constant_score": {
                                    "boost": 22,
                                    "filter": {"match": {"search_term_org_name.keyword": {"query": query_val}}},
                                }
                            },
                            {
                                "constant_score": {
                                    "boost": 9,
                                    "filter": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "match_phrase": {
                                                        "search_term_org_name_no_exits": {"query": query_val}
                                                    }
                                                },
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
                                                    "search_term_org_description_no_name": {
                                                        "query": query_val,
                                                        "slop": 5,
                                                    }
                                                }
                                            }
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
                                                {"match_phrase": {"org_competitor_no_exits": {"query": query_val}}},
                                                {"prefix": {"competitor_url_no_exits.keyword": query_val}},
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
                                                            "org_news_noun_phrases.noun_phrase": {"query": query_val}
                                                        }
                                                    }
                                                }
                                            },
                                        }
                                    },
                                }
                            },
                        ]
                    }
                }
            }
        },
        "sort": [
            {"_score": {"order": "desc"}},
            # {"search_term_org_last_funding_date": {"order": "desc"}},
            # {"search_term_org_num_deals": {"order": "desc"}},
            {"org_key_keyword_warm": {"order": "asc"}},
        ],
    }


def make_dummy_query(query_val: str, es_from: int, es_size: int):
    return {
        "_source": True,
        "explain": False,
        "from": es_from,
        "size": es_size,
        "query": {"match_phrase": {"org.org_description": {"query": query_val, "slop": 5}}},
    }


def main():
    num_iterations = 50
    max_pages = 5
    num_search_terms = 20
    es_sizes = [10, 25, 50]

    compare_queries(
        "Base Query",
        make_unnested_search_term_query_modified_exits,
        "IdOrgKeyInt Query",
        make_unnested_search_term_query_modified_exits_id_org_sort,
        SEARCH_TERMS[:num_search_terms],
        0,
        es_sizes,
        num_iterations,
        index,
        "base_vs_org_key_int",
    )

    compare_queries(
        "Base Query",
        make_unnested_search_term_query_modified_exits,
        "IdOrgKeyKeyword Query",
        make_unnested_search_term_query_modified_exits_id_org_keyword_sort,
        SEARCH_TERMS[:num_search_terms],
        0,
        es_sizes,
        num_iterations,
        index,
        "base_vs_org_key_keyword",
    )

    compare_queries(
        "Base Query",
        make_unnested_search_term_query_modified_exits,
        "IdOrgKeyKeyword Warm Query",
        make_unnested_search_term_query_modified_exits_id_org_keyword_warm_sort,
        SEARCH_TERMS[:num_search_terms],
        0,
        es_sizes,
        num_iterations,
        index,
        "base_vs_org_key_keyword_warm",
    )

    compare_queries(
        "IdOrgKeyInt Query",
        make_unnested_search_term_query_modified_exits_id_org_sort,
        "IdOrgKeyKeyword Query",
        make_unnested_search_term_query_modified_exits_id_org_keyword_sort,
        SEARCH_TERMS[:num_search_terms],
        0,
        es_sizes,
        num_iterations,
        index,
        "org_key_int_vs_org_key_keyword",
    )

    compare_queries(
        "IdOrgKeyInt Query",
        make_unnested_search_term_query_modified_exits_id_org_sort,
        "IdOrgKeyKeyword Warm Query",
        make_unnested_search_term_query_modified_exits_id_org_keyword_warm_sort,
        SEARCH_TERMS[:num_search_terms],
        0,
        es_sizes,
        num_iterations,
        index,
        "org_key_int_vs_org_key_warm_keyword",
    )

    compare_queries(
        "IdOrgKeyKeyword Query",
        make_unnested_search_term_query_modified_exits_id_org_keyword_sort,
        "IdOrgKeyKeyword Warm Query",
        make_unnested_search_term_query_modified_exits_id_org_keyword_warm_sort,
        SEARCH_TERMS[:num_search_terms],
        0,
        es_sizes,
        num_iterations,
        index,
        "org_key_int_vs_org_key_keyword_warm",
    )

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
