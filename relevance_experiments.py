def make_current_prd_query(query_val: str, es_from: int, es_size: int):
    return {
        "from": es_from,
        "size": es_size,
        "query": {
            "bool": {
                "must": {
                    "bool": {
                        "should": [
                            {
                                "constant_score": {
                                    "boost": 10000000000000,
                                    "filter": {"match": {"org_name.keyword": {"query": query_val}}},
                                }
                            },
                            {
                                "function_score": {
                                    "functions": [
                                        {
                                            "field_value_factor": {
                                                "factor": 1,
                                                "field": "org_total_equity_funding",
                                                "missing": 1,
                                            }
                                        }
                                    ],
                                    "query": {
                                        "constant_score": {
                                            "boost": 1,
                                            "filter": {
                                                "bool": {
                                                    "should": [
                                                        {
                                                            "constant_score": {
                                                                "boost": 9,
                                                                "filter": {
                                                                    "bool": {
                                                                        "should": [
                                                                            {
                                                                                "match_phrase": {
                                                                                    "search_term_org_name_no_exits": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "prefix": {
                                                                                    "search_term_org_url_no_exits.keyword": query_val
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
                                                                                "search_term_org_description_no_exits": {
                                                                                    "query": query_val,
                                                                                    "slop": 5,
                                                                                }
                                                                            }
                                                                        },
                                                                        "must_not": {
                                                                            "match_phrase": {
                                                                                "org_name": {"query": query_val}
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
                                                                                    "search_term_org_competitor_no_exits": {
                                                                                        "query": query_val
                                                                                    }
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
                                                                "filter": {
                                                                    "prefix": {
                                                                        "search_term_org_investor_name_no_exits.keyword": query_val
                                                                    }
                                                                },
                                                            }
                                                        },
                                                        {
                                                            "function_score": {
                                                                "min_score": 0.15,
                                                                "query": {
                                                                    "match_phrase": {
                                                                        "all_org_news_noun_phrases_no_exit": {
                                                                            "boost": 0.1,
                                                                            "query": query_val,
                                                                        }
                                                                    }
                                                                },
                                                            }
                                                        },
                                                    ]
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
            {"org_last_funding_funding_date": {"order": "desc"}},
            {"org_num_deals": {"order": "desc"}},
            {"index_key": {"order": "asc"}},
        ],
    }


def make_news_desc_tf_idf_times_equity_funding(query_val: str, es_from: int, es_size: int):
    return {
        "from": 0,
        "size": es_size,
        "query": {
            "bool": {
                "must": {
                    "bool": {
                        "should": [
                            {
                                "constant_score": {
                                    "boost": 10000000000000,
                                    "filter": {"match": {"org_name.keyword": {"query": query_val}}},
                                }
                            },
                            {
                                "function_score": {
                                    "functions": [
                                        {
                                            "field_value_factor": {
                                                "factor": 1,
                                                "field": "org_total_equity_funding",
                                                "missing": 1,
                                            }
                                        }
                                    ],
                                    "query": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_name_no_exits": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "search_term_org_url_no_exits.keyword": query_val
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "match_phrase": {
                                                        "search_term_org_description_no_exits": {
                                                            "boost": 1,
                                                            "query": query_val,
                                                            "slop": 5,
                                                        }
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_competitor_no_exits": {
                                                                                "query": query_val
                                                                            }
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
                                                        "boost": 0,
                                                        "filter": {
                                                            "prefix": {
                                                                "search_term_org_investor_name_no_exits.keyword": query_val
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "function_score": {
                                                        "min_score": 1.5,
                                                        "query": {
                                                            "match_phrase": {
                                                                "all_org_news_noun_phrases_no_exit": {
                                                                    "boost": 1,
                                                                    "query": query_val,
                                                                }
                                                            }
                                                        },
                                                    }
                                                },
                                            ]
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
            {"org_last_funding_funding_date": {"order": "desc"}},
            {"org_num_deals": {"order": "desc"}},
            {"index_key": {"order": "asc"}},
        ],
    }


def make_news_desc_tf_idf_times_ln_equity_funding(query_val: str, es_from: int, es_size: int):
    return {
        "from": 0,
        "size": es_size,
        "query": {
            "bool": {
                "must": {
                    "bool": {
                        "should": [
                            {
                                "constant_score": {
                                    "boost": 10000000000000,
                                    "filter": {"match": {"org_name.keyword": {"query": query_val}}},
                                }
                            },
                            {
                                "function_score": {
                                    "functions": [
                                        {
                                            "field_value_factor": {
                                                "factor": 1,
                                                "field": "org_total_equity_funding",
                                                "missing": 1,
                                                "modifier": "ln1p",
                                            }
                                        }
                                    ],
                                    "query": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_name_no_exits": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "search_term_org_url_no_exits.keyword": query_val
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "match_phrase": {
                                                        "search_term_org_description_no_exits": {
                                                            "boost": 1,
                                                            "query": query_val,
                                                            "slop": 5,
                                                        }
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_competitor_no_exits": {
                                                                                "query": query_val
                                                                            }
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
                                                        "boost": 0,
                                                        "filter": {
                                                            "prefix": {
                                                                "search_term_org_investor_name_no_exits.keyword": query_val
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "function_score": {
                                                        "min_score": 1.5,
                                                        "query": {
                                                            "match_phrase": {
                                                                "all_org_news_noun_phrases_no_exit": {
                                                                    "boost": 1,
                                                                    "query": query_val,
                                                                }
                                                            }
                                                        },
                                                    }
                                                },
                                            ]
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
            {"org_last_funding_funding_date": {"order": "desc"}},
            {"org_num_deals": {"order": "desc"}},
            {"index_key": {"order": "asc"}},
        ],
    }


def make_news_desc_tf_idf_times_sqrt_equity_funding(query_val: str, es_from: int, es_size: int):
    return {
        "from": 0,
        "size": es_size,
        "query": {
            "bool": {
                "must": {
                    "bool": {
                        "should": [
                            {
                                "constant_score": {
                                    "boost": 10000000000000,
                                    "filter": {"match": {"org_name.keyword": {"query": query_val}}},
                                }
                            },
                            {
                                "function_score": {
                                    "functions": [
                                        {
                                            "field_value_factor": {
                                                "factor": 1,
                                                "field": "org_total_equity_funding",
                                                "missing": 1,
                                                "modifier": "sqrt",
                                            }
                                        }
                                    ],
                                    "query": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_name_no_exits": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "search_term_org_url_no_exits.keyword": query_val
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "match_phrase": {
                                                        "search_term_org_description_no_exits": {
                                                            "boost": 1,
                                                            "query": query_val,
                                                            "slop": 5,
                                                        }
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_competitor_no_exits": {
                                                                                "query": query_val
                                                                            }
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
                                                        "boost": 0,
                                                        "filter": {
                                                            "prefix": {
                                                                "search_term_org_investor_name_no_exits.keyword": query_val
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "function_score": {
                                                        "min_score": 1.5,
                                                        "query": {
                                                            "match_phrase": {
                                                                "all_org_news_noun_phrases_no_exit": {
                                                                    "boost": 1,
                                                                    "query": query_val,
                                                                }
                                                            }
                                                        },
                                                    }
                                                },
                                            ]
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
            {"org_last_funding_funding_date": {"order": "desc"}},
            {"org_num_deals": {"order": "desc"}},
            {"index_key": {"order": "asc"}},
        ],
    }


def make_news_1_5_x_desc_tf_idf_times_ln_equity_funding(query_val: str, es_from: int, es_size: int):
    return {
        "from": 0,
        "size": es_size,
        "query": {
            "bool": {
                "must": {
                    "bool": {
                        "should": [
                            {
                                "constant_score": {
                                    "boost": 10000000000000,
                                    "filter": {"match": {"org_name.keyword": {"query": query_val}}},
                                }
                            },
                            {
                                "function_score": {
                                    "functions": [
                                        {
                                            "field_value_factor": {
                                                "factor": 1,
                                                "field": "org_total_equity_funding",
                                                "missing": 1,
                                                "modifier": "ln1p",
                                            }
                                        }
                                    ],
                                    "query": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_name_no_exits": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "search_term_org_url_no_exits.keyword": query_val
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "match_phrase": {
                                                        "search_term_org_description_no_exits": {
                                                            "boost": 1.5,
                                                            "query": query_val,
                                                            "slop": 5,
                                                        }
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_competitor_no_exits": {
                                                                                "query": query_val
                                                                            }
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
                                                        "boost": 0,
                                                        "filter": {
                                                            "prefix": {
                                                                "search_term_org_investor_name_no_exits.keyword": query_val
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "function_score": {
                                                        "min_score": 1.5,
                                                        "query": {
                                                            "match_phrase": {
                                                                "all_org_news_noun_phrases_no_exit": {
                                                                    "boost": 1,
                                                                    "query": query_val,
                                                                }
                                                            }
                                                        },
                                                    }
                                                },
                                            ]
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
            {"org_last_funding_funding_date": {"order": "desc"}},
            {"org_num_deals": {"order": "desc"}},
            {"index_key": {"order": "asc"}},
        ],
    }


def make_news_desc_expert_collection_times_ln_equity_funding(search_val: str, es_from: int, es_size: int):
    return {
        "from": es_from,
        "size": es_size,
        "query": {
            "bool": {
                "must": {
                    "bool": {
                        "should": [
                            {
                                "constant_score": {
                                    "boost": 10000000000000,
                                    "filter": {"match": {"org_name.keyword": {"query": search_val}}},
                                }
                            },
                            {
                                "function_score": {
                                    "functions": [
                                        {
                                            "field_value_factor": {
                                                "factor": 1,
                                                "field": "org_total_equity_funding",
                                                "missing": 1,
                                                "modifier": "ln1p",
                                            }
                                        }
                                    ],
                                    "query": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_name_no_exits": {
                                                                                "query": search_val
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "search_term_org_url_no_exits.keyword": search_val
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "match_phrase": {
                                                        "search_term_org_description_no_exits": {
                                                            "boost": 1,
                                                            "query": search_val,
                                                            "slop": 5,
                                                        }
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_competitor_no_exits": {
                                                                                "query": search_val
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "search_term_org_competitor_url_no_exits.keyword": search_val
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "prefix": {
                                                                "search_term_org_investor_name_no_exits.keyword": search_val
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "function_score": {
                                                        "min_score": 1.5,
                                                        "query": {
                                                            "match_phrase": {
                                                                "all_org_news_noun_phrases_no_exit": {
                                                                    "boost": 1,
                                                                    "query": search_val,
                                                                }
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "match": {
                                                        "expert_collection_names": {"boost": 1, "query": search_val}
                                                    }
                                                },
                                            ]
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
            {"org_last_funding_funding_date": {"order": "desc"}},
            {"org_num_deals": {"order": "desc"}},
            {"index_key": {"order": "asc"}},
        ],
    }


def make_0_5_x_news_desc_expert_collection_times_ln_equity_funding(search_val: str, es_from: int, es_size: int):
    return {
        "from": es_from,
        "size": es_size,
        "query": {
            "bool": {
                "must": {
                    "bool": {
                        "should": [
                            {
                                "constant_score": {
                                    "boost": 10000000000000,
                                    "filter": {"match": {"org_name.keyword": {"query": search_val}}},
                                }
                            },
                            {
                                "function_score": {
                                    "functions": [
                                        {
                                            "field_value_factor": {
                                                "factor": 1,
                                                "field": "org_total_equity_funding",
                                                "missing": 1,
                                                "modifier": "ln1p",
                                            }
                                        }
                                    ],
                                    "query": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_name_no_exits": {
                                                                                "query": search_val
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "search_term_org_url_no_exits.keyword": search_val
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "match_phrase": {
                                                        "search_term_org_description_no_exits": {
                                                            "boost": 1,
                                                            "query": search_val,
                                                            "slop": 5,
                                                        }
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_competitor_no_exits": {
                                                                                "query": search_val
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "search_term_org_competitor_url_no_exits.keyword": search_val
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "prefix": {
                                                                "search_term_org_investor_name_no_exits.keyword": search_val
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "function_score": {
                                                        "min_score": 0.75,
                                                        "query": {
                                                            "match_phrase": {
                                                                "all_org_news_noun_phrases_no_exit": {
                                                                    "boost": 0.5,
                                                                    "query": search_val,
                                                                }
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "match": {
                                                        "expert_collection_names": {"boost": 1, "query": search_val}
                                                    }
                                                },
                                            ]
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
            {"org_last_funding_funding_date": {"order": "desc"}},
            {"org_num_deals": {"order": "desc"}},
            {"index_key": {"order": "asc"}},
        ],
    }


def make_0_5_x_news_desc_flattened1_expert_collection_times_ln_equity_funding(
    search_val: str, es_from: int, es_size: int
):
    return {
        "from": es_from,
        "size": es_size,
        "query": {
            "bool": {
                "must": {
                    "bool": {
                        "should": [
                            {
                                "constant_score": {
                                    "boost": 10000000000000,
                                    "filter": {"match": {"org_name.keyword": {"query": search_val}}},
                                }
                            },
                            {
                                "function_score": {
                                    "functions": [
                                        {
                                            "field_value_factor": {
                                                "factor": 1,
                                                "field": "org_total_equity_funding",
                                                "missing": 1,
                                                "modifier": "ln1p",
                                            }
                                        }
                                    ],
                                    "query": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_name_no_exits": {
                                                                                "query": search_val
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "search_term_org_url_no_exits.keyword": search_val
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "match_phrase": {
                                                        "search_term_org_description_no_exits": {
                                                            "boost": 1,
                                                            "query": search_val,
                                                            "slop": 5,
                                                        }
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_competitor_no_exits": {
                                                                                "query": search_val
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "search_term_org_competitor_url_no_exits.keyword": search_val
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "prefix": {
                                                                "search_term_org_investor_name_no_exits.keyword": search_val
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "function_score": {
                                                        "min_score": 0.75,
                                                        "query": {
                                                            "match_phrase": {
                                                                "all_org_news_noun_phrases_no_exit": {
                                                                    "boost": 0.5,
                                                                    "query": search_val,
                                                                }
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 1,
                                                        "filter": {
                                                            "match": {
                                                                "expert_collection_names": {
                                                                    "boost": 1,
                                                                    "query": search_val,
                                                                }
                                                            }
                                                        },
                                                    }
                                                },
                                            ]
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
            {"org_last_funding_funding_date": {"order": "desc"}},
            {"org_num_deals": {"order": "desc"}},
            {"index_key": {"order": "asc"}},
        ],
    }


def make_0_2_x_news_desc_flattened1_expert_collection_times_ln_equity_funding(
    search_val: str, es_from: int, es_size: int
):
    return {
        "from": es_from,
        "size": es_size,
        "query": {
            "bool": {
                "must": {
                    "bool": {
                        "should": [
                            {
                                "constant_score": {
                                    "boost": 10000000000000,
                                    "filter": {"match": {"org_name.keyword": {"query": search_val}}},
                                }
                            },
                            {
                                "function_score": {
                                    "functions": [
                                        {
                                            "field_value_factor": {
                                                "factor": 1,
                                                "field": "org_total_equity_funding",
                                                "missing": 1,
                                                "modifier": "ln1p",
                                            }
                                        }
                                    ],
                                    "query": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_name_no_exits": {
                                                                                "query": search_val
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "search_term_org_url_no_exits.keyword": search_val
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "match_phrase": {
                                                        "search_term_org_description_no_exits": {
                                                            "boost": 1,
                                                            "query": search_val,
                                                            "slop": 5,
                                                        }
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_competitor_no_exits": {
                                                                                "query": search_val
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "search_term_org_competitor_url_no_exits.keyword": search_val
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "prefix": {
                                                                "search_term_org_investor_name_no_exits.keyword": search_val
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "function_score": {
                                                        "min_score": 0.3,
                                                        "query": {
                                                            "match_phrase": {
                                                                "all_org_news_noun_phrases_no_exit": {
                                                                    "boost": 0.2,
                                                                    "query": search_val,
                                                                }
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 1,
                                                        "filter": {
                                                            "match": {
                                                                "expert_collection_names": {
                                                                    "boost": 1,
                                                                    "query": search_val,
                                                                }
                                                            }
                                                        },
                                                    }
                                                },
                                            ]
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
            {"org_last_funding_funding_date": {"order": "desc"}},
            {"org_num_deals": {"order": "desc"}},
            {"index_key": {"order": "asc"}},
        ],
    }


def make_description_tf_idf_0_5_x_news_tfidf_collection_tf_idf_X_ln_equity_funding_X_ln_num_collections(
    query_val, es_from, es_size
):
    return {
        "from": es_from,
        "size": es_size,
        "query": {
            "bool": {
                "must": {
                    "bool": {
                        "should": [
                            {
                                "constant_score": {
                                    "boost": 10000000000000,
                                    "filter": {"match": {"org_name.keyword": {"query": query_val}}},
                                }
                            },
                            {
                                "function_score": {
                                    "functions": [
                                        {
                                            "field_value_factor": {
                                                "factor": 1,
                                                "field": "org_total_equity_funding",
                                                "missing": 1,
                                                "modifier": "ln1p",
                                            }
                                        },
                                        {
                                            "field_value_factor": {
                                                "field": "num_expert_collections",
                                                "missing": 1,
                                                "modifier": "ln1p",
                                            }
                                        },
                                    ],
                                    "query": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_name_no_exits": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "search_term_org_url_no_exits.keyword": query_val
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "match_phrase": {
                                                        "search_term_org_description_no_exits": {
                                                            "boost": 1,
                                                            "query": query_val,
                                                            "slop": 5,
                                                        }
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_competitor_no_exits": {
                                                                                "query": query_val
                                                                            }
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
                                                        "boost": 0,
                                                        "filter": {
                                                            "prefix": {
                                                                "search_term_org_investor_name_no_exits.keyword": query_val
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "function_score": {
                                                        "min_score": 0.75,
                                                        "query": {
                                                            "match_phrase": {
                                                                "all_org_news_noun_phrases_no_exit": {
                                                                    "boost": 0.5,
                                                                    "query": query_val,
                                                                }
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "match": {
                                                        "expert_collection_names": {"boost": 1, "query": query_val}
                                                    }
                                                },
                                            ]
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
            {"org_last_funding_funding_date": {"order": "desc"}},
            {"org_num_deals": {"order": "desc"}},
            {"index_key": {"order": "asc"}},
        ],
    }


def make_description_tf_idf_news_tfidf_collection_tf_idf_X_ln_equity_funding_X_ln_num_collections(
    query_val, es_from, es_size
):
    return {
        "from": es_from,
        "size": es_size,
        "query": {
            "bool": {
                "must": {
                    "bool": {
                        "should": [
                            {
                                "constant_score": {
                                    "boost": 10000000000000,
                                    "filter": {"match": {"org_name.keyword": {"query": query_val}}},
                                }
                            },
                            {
                                "function_score": {
                                    "functions": [
                                        {
                                            "field_value_factor": {
                                                "factor": 1,
                                                "field": "org_total_equity_funding",
                                                "missing": 1,
                                                "modifier": "ln1p",
                                            }
                                        },
                                        {
                                            "field_value_factor": {
                                                "field": "num_expert_collections",
                                                "missing": 1,
                                                "modifier": "ln1p",
                                            }
                                        },
                                    ],
                                    "query": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_name_no_exits": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "search_term_org_url_no_exits.keyword": query_val
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "match_phrase": {
                                                        "search_term_org_description_no_exits": {
                                                            "boost": 1,
                                                            "query": query_val,
                                                            "slop": 5,
                                                        }
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_competitor_no_exits": {
                                                                                "query": query_val
                                                                            }
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
                                                        "boost": 0,
                                                        "filter": {
                                                            "prefix": {
                                                                "search_term_org_investor_name_no_exits.keyword": query_val
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "function_score": {
                                                        "min_score": 1.5,
                                                        "query": {
                                                            "match_phrase": {
                                                                "all_org_news_noun_phrases_no_exit": {
                                                                    "boost": 1,
                                                                    "query": query_val,
                                                                }
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "match": {
                                                        "expert_collection_names": {"boost": 1, "query": query_val}
                                                    }
                                                },
                                            ]
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
            {"org_last_funding_funding_date": {"order": "desc"}},
            {"org_num_deals": {"order": "desc"}},
            {"index_key": {"order": "asc"}},
        ],
    }


def make_description_tf_idf_news_tfidf_flattened1_collection_X_ln_equity_funding_X_ln_num_collections(
    query_val, es_from, es_size
):
    return {
        "from": es_from,
        "size": es_size,
        "query": {
            "bool": {
                "must": {
                    "bool": {
                        "should": [
                            {
                                "constant_score": {
                                    "boost": 10000000000000,
                                    "filter": {"match": {"org_name.keyword": {"query": query_val}}},
                                }
                            },
                            {
                                "function_score": {
                                    "functions": [
                                        {
                                            "field_value_factor": {
                                                "factor": 1,
                                                "field": "org_total_equity_funding",
                                                "missing": 1,
                                                "modifier": "ln1p",
                                            }
                                        },
                                        {
                                            "field_value_factor": {
                                                "field": "num_expert_collections",
                                                "missing": 1,
                                                "modifier": "ln1p",
                                            }
                                        },
                                    ],
                                    "query": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_name_no_exits": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "search_term_org_url_no_exits.keyword": query_val
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "match_phrase": {
                                                        "search_term_org_description_no_exits": {
                                                            "boost": 1,
                                                            "query": query_val,
                                                            "slop": 5,
                                                        }
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "search_term_org_competitor_no_exits": {
                                                                                "query": query_val
                                                                            }
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
                                                        "boost": 0,
                                                        "filter": {
                                                            "prefix": {
                                                                "search_term_org_investor_name_no_exits.keyword": query_val
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 1,
                                                        "filter": {
                                                            "match": {
                                                                "expert_collection_names": {
                                                                    "boost": 1,
                                                                    "query": query_val,
                                                                }
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "match": {
                                                        "expert_collection_names": {"boost": 1, "query": query_val}
                                                    }
                                                },
                                            ]
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
            {"org_last_funding_funding_date": {"order": "desc"}},
            {"org_num_deals": {"order": "desc"}},
            {"index_key": {"order": "asc"}},
        ],
    }
