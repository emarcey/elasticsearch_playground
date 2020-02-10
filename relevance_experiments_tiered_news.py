def tiered_news_make_news_desc_tf_idf_times_equity_funding(query_val: str, es_from: int, es_size: int):
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
                                                    "dis_max": {
                                                        "queries": [
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_one_no_exit": {
                                                                        "boost": 0.1,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_two_no_exit": {
                                                                        "boost": 0.2,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_three_no_exit": {
                                                                        "boost": 0.3,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                        "boost": 0.4,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                        "boost": 0.5,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                        "boost": 0.6,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                        "boost": 0.7,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                        "boost": 0.8,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                        "boost": 0.9,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_ten_no_exit": {
                                                                        "boost": 1,
                                                                        "query": query_val,
                                                                    }
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


def tiered_news_make_news_desc_tf_idf_times_ln_equity_funding(query_val: str, es_from: int, es_size: int):
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
                                                    "dis_max": {
                                                        "queries": [
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_one_no_exit": {
                                                                        "boost": 0.1,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_two_no_exit": {
                                                                        "boost": 0.2,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_three_no_exit": {
                                                                        "boost": 0.3,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                        "boost": 0.4,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                        "boost": 0.5,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                        "boost": 0.6,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                        "boost": 0.7,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                        "boost": 0.8,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                        "boost": 0.9,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_ten_no_exit": {
                                                                        "boost": 1,
                                                                        "query": query_val,
                                                                    }
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


def tiered_news_make_news_desc_tf_idf_times_sqrt_equity_funding(query_val: str, es_from: int, es_size: int):
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
                                                    "dis_max": {
                                                        "queries": [
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_one_no_exit": {
                                                                        "boost": 0.1,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_two_no_exit": {
                                                                        "boost": 0.2,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_three_no_exit": {
                                                                        "boost": 0.3,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                        "boost": 0.4,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                        "boost": 0.5,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                        "boost": 0.6,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                        "boost": 0.7,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                        "boost": 0.8,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                        "boost": 0.9,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_ten_no_exit": {
                                                                        "boost": 1,
                                                                        "query": query_val,
                                                                    }
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


def tiered_news_make_news_1_5_x_desc_tf_idf_times_ln_equity_funding(query_val: str, es_from: int, es_size: int):
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
                                                    "dis_max": {
                                                        "queries": [
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_one_no_exit": {
                                                                        "boost": 0.1,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_two_no_exit": {
                                                                        "boost": 0.2,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_three_no_exit": {
                                                                        "boost": 0.3,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                        "boost": 0.4,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                        "boost": 0.5,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                        "boost": 0.6,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                        "boost": 0.7,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                        "boost": 0.8,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                        "boost": 0.9,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_ten_no_exit": {
                                                                        "boost": 1,
                                                                        "query": query_val,
                                                                    }
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


def tiered_news_make_news_desc_expert_collection_times_ln_equity_funding(query_val: str, es_from: int, es_size: int):
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
                                                    "dis_max": {
                                                        "queries": [
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_one_no_exit": {
                                                                        "boost": 0.1,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_two_no_exit": {
                                                                        "boost": 0.2,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_three_no_exit": {
                                                                        "boost": 0.3,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                        "boost": 0.4,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                        "boost": 0.5,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                        "boost": 0.6,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                        "boost": 0.7,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                        "boost": 0.8,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                        "boost": 0.9,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_ten_no_exit": {
                                                                        "boost": 1,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                        ]
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


def tiered_news_make_0_5_x_news_desc_expert_collection_times_ln_equity_funding(
    query_val: str, es_from: int, es_size: int
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
                                                    "dis_max": {
                                                        "queries": [
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_one_no_exit": {
                                                                        "boost": 0.05,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_two_no_exit": {
                                                                        "boost": 0.1,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_three_no_exit": {
                                                                        "boost": 0.15,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                        "boost": 0.2,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                        "boost": 0.25,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                        "boost": 0.3,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                        "boost": 0.35,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                        "boost": 0.4,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                        "boost": 0.45,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_ten_no_exit": {
                                                                        "boost": 0.5,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                        ]
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


def tiered_news_make_0_5_x_news_desc_flattened1_expert_collection_times_ln_equity_funding(
    query_val: str, es_from: int, es_size: int
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
                                                    "dis_max": {
                                                        "queries": [
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_one_no_exit": {
                                                                        "boost": 0.05,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_two_no_exit": {
                                                                        "boost": 0.1,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_three_no_exit": {
                                                                        "boost": 0.15,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                        "boost": 0.2,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                        "boost": 0.25,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                        "boost": 0.3,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                        "boost": 0.35,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                        "boost": 0.4,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                        "boost": 0.35,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_ten_no_exit": {
                                                                        "boost": 0.5,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                        ]
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


def tiered_news_make_0_2_x_news_desc_flattened1_expert_collection_times_ln_equity_funding(
    query_val: str, es_from: int, es_size: int
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
                                                    "dis_max": {
                                                        "queries": [
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_one_no_exit": {
                                                                        "boost": 0.02,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_two_no_exit": {
                                                                        "boost": 0.04,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_three_no_exit": {
                                                                        "boost": 0.06,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                        "boost": 0.08,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                        "boost": 0.1,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                        "boost": 0.12,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                        "boost": 0.14,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                        "boost": 0.16,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                        "boost": 0.18,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_ten_no_exit": {
                                                                        "boost": 0.2,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                        ]
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


def tiered_news_make_description_tf_idf_0_5_x_news_tfidf_collection_tf_idf_X_ln_equity_funding_X_ln_num_collections(
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
                                                    "dis_max": {
                                                        "queries": [
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_one_no_exit": {
                                                                        "boost": 0.05,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_two_no_exit": {
                                                                        "boost": 0.01,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_three_no_exit": {
                                                                        "boost": 0.15,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                        "boost": 0.2,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                        "boost": 0.25,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                        "boost": 0.3,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                        "boost": 0.35,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                        "boost": 0.4,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                        "boost": 0.45,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_ten_no_exit": {
                                                                        "boost": 0.5,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                        ]
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


def tiered_news_make_description_tf_idf_news_tfidf_collection_tf_idf_X_ln_equity_funding_X_ln_num_collections(
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
                                                    "dis_max": {
                                                        "queries": [
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_one_no_exit": {
                                                                        "boost": 0.1,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_two_no_exit": {
                                                                        "boost": 0.2,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_three_no_exit": {
                                                                        "boost": 0.3,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                        "boost": 0.4,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                        "boost": 0.5,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                        "boost": 0.6,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                        "boost": 0.7,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                        "boost": 0.8,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                        "boost": 0.9,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    "org_news_noun_phrases_tier_ten_no_exit": {
                                                                        "boost": 1,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                        ]
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


def tiered_news_make_description_tf_idf_news_tfidf_flattened1_collection_X_ln_equity_funding_X_ln_num_collections(
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
