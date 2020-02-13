def tiered_news_make_description_tf_idf_news_bucket_frequency_collection_flat_X_ln_equity_funding(
    query_val, es_from, es_size
):
    return {
        "explain": True,
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
                                                "modifier": "ln2p",
                                            }
                                        },
                                        # {
                                        #     "field_value_factor": {
                                        #         "field": "num_expert_collections",
                                        #         "missing": 0,
                                        #         "modifier": "log2p",
                                        #     }
                                        # },
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
                                                        "boost": 1,
                                                        "functions": [
                                                            {
                                                                "field_value_factor": {
                                                                    "factor": 1,
                                                                    "field": "org_news_article_count",
                                                                    "missing": 0,
                                                                    "modifier": "log",
                                                                }
                                                            }
                                                        ],
                                                        "query": {
                                                            "dis_max": {
                                                                "queries": [
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.1,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_one_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.2,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_two_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.3,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_three_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.4,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.5,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.6,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.7,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.8,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.9,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 1,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_ten_no_exit": {
                                                                                        "query": query_val
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
                                                {
                                                    "constant_score": {
                                                        "boost": 0.5,
                                                        "filter": {
                                                            "match_phrase": {
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


def tiered_news_make_description_tf_idf_news_bucket_frequency_boost_upper_buckets_collection_flat_X_ln2p_equity_funding(
    query_val, es_from, es_size
):
    return {
        "explain": True,
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
                                                "modifier": "ln2p",
                                            }
                                        },
                                        # {
                                        #     "field_value_factor": {
                                        #         "field": "num_expert_collections",
                                        #         "missing": 0,
                                        #         "modifier": "log2p",
                                        #     }
                                        # },
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
                                                    # TODO: get 1 + log(article count)
                                                    "function_score": {
                                                        "boost": 2,
                                                        "functions": [
                                                            {
                                                                "field_value_factor": {
                                                                    "factor": 1,
                                                                    "field": "org_news_article_count",
                                                                    "missing": 0,
                                                                    "modifier": "log",
                                                                }
                                                            }
                                                        ],
                                                        "query": {
                                                            "dis_max": {
                                                                "queries": [
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.1,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_one_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.2,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_two_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.65,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_three_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.7,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.75,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.8,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.85,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.9,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.95,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 1,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_ten_no_exit": {
                                                                                        "query": query_val
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
                                                {
                                                    "constant_score": {
                                                        "boost": 0.5,
                                                        "filter": {
                                                            "match_phrase": {
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


def make_description_tf_idf_news_bucket_tfidf_X_1plog_num_articles_boost_upper_buckets_collection_flat_X_ln2p_equity_funding(
    query_val, es_from, es_size
):
    return {
        "explain": True,
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
                                                "modifier": "ln2p",
                                            }
                                        },
                                        # {
                                        #     "field_value_factor": {
                                        #         "field": "num_expert_collections",
                                        #         "missing": 0,
                                        #         "modifier": "log2p",
                                        #     }
                                        # },
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
                                                    # TODO: get 1 + log(article count)
                                                    "function_score": {
                                                        "boost_mode": "sum",
                                                        "functions": [{"weight": 1}],
                                                        "query": {
                                                            "function_score": {
                                                                "boost": 1,
                                                                "functions": [
                                                                    {
                                                                        "field_value_factor": {
                                                                            "factor": 1,
                                                                            "field": "org_news_article_count",
                                                                            "missing": 0,
                                                                            "modifier": "log",
                                                                        }
                                                                    }
                                                                ],
                                                                "query": {
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
                                                                                        "boost": 0.65,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                                        "boost": 0.7,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                                        "boost": 0.75,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                                        "boost": 0.8,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                                        "boost": 0.85,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                                        "boost": 0.9,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                                        "boost": 0.95,
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
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0.5,
                                                        "filter": {
                                                            "match_phrase": {
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


def make_description_tf_idf_news_bucket_tfidf_X_1plog_num_articles_boost_upper_buckets_collection_flat_X_ln2p_equity_funding_X_log_num_collections(
    query_val, es_from, es_size
):
    return {
        "explain": True,
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
                                                "modifier": "ln2p",
                                            }
                                        },
                                        {
                                            "field_value_factor": {
                                                "field": "num_expert_collections",
                                                "missing": 0,
                                                "modifier": "log2p",
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
                                                    # TODO: get 1 + log(article count)
                                                    "function_score": {
                                                        "boost_mode": "sum",
                                                        "functions": [{"weight": 1}],
                                                        "query": {
                                                            "function_score": {
                                                                "boost": 2,
                                                                "functions": [
                                                                    {
                                                                        "field_value_factor": {
                                                                            "factor": 1,
                                                                            "field": "org_news_article_count",
                                                                            "missing": 0,
                                                                            "modifier": "log",
                                                                        }
                                                                    }
                                                                ],
                                                                "query": {
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
                                                                                        "boost": 0.65,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                                        "boost": 0.7,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                                        "boost": 0.75,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                                        "boost": 0.8,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                                        "boost": 0.85,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                                        "boost": 0.9,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                                        "boost": 0.95,
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
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0.5,
                                                        "filter": {
                                                            "match_phrase": {
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


def make_description_tf_idf_news_bucket_tfidf_X_2x_1plog_num_articles_boost_upper_buckets_collection_flat_X_ln2p_equity_funding(
    query_val, es_from, es_size
):
    return {
        "explain": True,
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
                                                "modifier": "ln2p",
                                            }
                                        },
                                        # {
                                        #     "field_value_factor": {
                                        #         "field": "num_expert_collections",
                                        #         "missing": 0,
                                        #         "modifier": "log2p",
                                        #     }
                                        # },
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
                                                    # TODO: get 1 + log(article count)
                                                    "function_score": {
                                                        "boost_mode": "sum",
                                                        "functions": [{"weight": 1}],
                                                        "query": {
                                                            "function_score": {
                                                                "boost": 2,
                                                                "functions": [
                                                                    {
                                                                        "field_value_factor": {
                                                                            "factor": 1,
                                                                            "field": "org_news_article_count",
                                                                            "missing": 0,
                                                                            "modifier": "log",
                                                                        }
                                                                    }
                                                                ],
                                                                "query": {
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
                                                                                        "boost": 0.65,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                                        "boost": 0.7,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                                        "boost": 0.75,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                                        "boost": 0.8,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                                        "boost": 0.85,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                                        "boost": 0.9,
                                                                                        "query": query_val,
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                                        "boost": 0.95,
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
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0.5,
                                                        "filter": {
                                                            "match_phrase": {
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


def make_description_tf_idf_news_bucket_frequency_X_4x_1plog_num_articles_boost_upper_buckets_collection_flat_X_ln2p_equity_funding(
    query_val, es_from, es_size
):
    return {
        "explain": True,
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
                                                "modifier": "ln2p",
                                            }
                                        },
                                        # {
                                        #     "field_value_factor": {
                                        #         "field": "num_expert_collections",
                                        #         "missing": 0,
                                        #         "modifier": "log2p",
                                        #     }
                                        # },
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
                                                    # TODO: get 1 + log(article count)
                                                    "function_score": {
                                                        "boost_mode": "sum",
                                                        "functions": [{"weight": 1}],
                                                        "query": {
                                                            "function_score": {
                                                                "boost": 4,
                                                                "functions": [
                                                                    {
                                                                        "field_value_factor": {
                                                                            "factor": 1,
                                                                            "field": "org_news_article_count",
                                                                            "missing": 0,
                                                                            "modifier": "log",
                                                                        }
                                                                    }
                                                                ],
                                                                "query": {
                                                                    "dis_max": {
                                                                        "queries": [
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.1,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_one_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.2,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_two_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.65,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_three_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.7,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_four_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.75,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_five_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.8,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_six_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.85,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_seven_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.9,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_eight_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.95,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_nine_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 1,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_ten_no_exit": {
                                                                                                "query": query_val
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
                                                {
                                                    "constant_score": {
                                                        "boost": 0.5,
                                                        "filter": {
                                                            "match_phrase": {
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


def make_description_tf_idf_news_bucket_frequency_X_1plog_num_articles_boost_upper_buckets_collection_flat_X_ln2p_equity_funding(
    query_val, es_from, es_size
):
    return {
        "explain": True,
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
                                                "modifier": "ln2p",
                                            }
                                        },
                                        # {
                                        #     "field_value_factor": {
                                        #         "field": "num_expert_collections",
                                        #         "missing": 0,
                                        #         "modifier": "log2p",
                                        #     }
                                        # },
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
                                                    # TODO: get 1 + log(article count)
                                                    "function_score": {
                                                        "boost_mode": "sum",
                                                        "functions": [{"weight": 1}],
                                                        "query": {
                                                            "function_score": {
                                                                "boost": 2,
                                                                "functions": [
                                                                    {
                                                                        "field_value_factor": {
                                                                            "factor": 1,
                                                                            "field": "org_news_article_count",
                                                                            "missing": 0,
                                                                            "modifier": "log",
                                                                        }
                                                                    }
                                                                ],
                                                                "query": {
                                                                    "dis_max": {
                                                                        "queries": [
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.1,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_one_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.2,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_two_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.65,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_three_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.7,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_four_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.75,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_five_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.8,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_six_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.85,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_seven_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.9,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_eight_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 0.95,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_nine_no_exit": {
                                                                                                "query": query_val
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                }
                                                                            },
                                                                            {
                                                                                "constant_score": {
                                                                                    "boost": 1,
                                                                                    "filter": {
                                                                                        "match_phrase": {
                                                                                            "org_news_noun_phrases_tier_ten_no_exit": {
                                                                                                "query": query_val
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
                                                {
                                                    "constant_score": {
                                                        "boost": 0.5,
                                                        "filter": {
                                                            "match_phrase": {
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


def tiered_news_make_description_tf_idf_news_bucket_score_collection_flat_X_equity_funding_max_500(
    query_val, es_from, es_size
):
    return {
        "explain": True,
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
                                    "max_boost": 500,
                                    "functions": [
                                        {
                                            "field_value_factor": {
                                                "factor": 1,
                                                "field": "org_total_equity_funding",
                                                "missing": 1,
                                                # "modifier": "ln2p",
                                            }
                                        },
                                        # {
                                        #     "field_value_factor": {
                                        #         "field": "num_expert_collections",
                                        #         "missing": 0,
                                        #         "modifier": "log2p",
                                        #     }
                                        # },
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
                                                        "boost": 10,
                                                        "queries": [
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.1,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_one_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.2,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_two_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.3,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_three_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.4,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_four_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.5,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_five_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.6,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_six_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.7,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_seven_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.8,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_eight_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.9,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_nine_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 1,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_ten_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                        ],
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0.5,
                                                        "filter": {
                                                            "match_phrase": {
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


def tiered_news_make_description_tf_idf_news_bucket_frequency_collection_flat_X_equity_funding_max_500(
    query_val, es_from, es_size
):
    return {
        "explain": True,
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
                                    "max_boost": 500,
                                    "functions": [
                                        {
                                            "field_value_factor": {
                                                "factor": 1,
                                                "field": "org_total_equity_funding",
                                                "missing": 1,
                                                # "modifier": "ln2p",
                                            }
                                        },
                                        # {
                                        #     "field_value_factor": {
                                        #         "field": "num_expert_collections",
                                        #         "missing": 0,
                                        #         "modifier": "log2p",
                                        #     }
                                        # },
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
                                                        "boost": 1,
                                                        "functions": [
                                                            {
                                                                "field_value_factor": {
                                                                    "factor": 1,
                                                                    "field": "org_news_article_count",
                                                                    "missing": 0,
                                                                    "modifier": "log",
                                                                }
                                                            }
                                                        ],
                                                        "query": {
                                                            "dis_max": {
                                                                "queries": [
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.1,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_one_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.2,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_two_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.3,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_three_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.4,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.5,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.6,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.7,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.8,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.9,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 1,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_ten_no_exit": {
                                                                                        "query": query_val
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
                                                {
                                                    "constant_score": {
                                                        "boost": 0.5,
                                                        "filter": {
                                                            "match_phrase": {
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


def tiered_news_make_description_tf_idf_news_bucket_frequency_collection_flat_X_log2p_equity_funding(
    query_val, es_from, es_size
):
    return {
        "explain": True,
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
                                                "modifier": "log2p",
                                            }
                                        },
                                        # {
                                        #     "field_value_factor": {
                                        #         "field": "num_expert_collections",
                                        #         "missing": 0,
                                        #         "modifier": "log2p",
                                        #     }
                                        # },
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
                                                        "boost": 1,
                                                        "functions": [
                                                            {
                                                                "field_value_factor": {
                                                                    "factor": 1,
                                                                    "field": "org_news_article_count",
                                                                    "missing": 0,
                                                                    "modifier": "log",
                                                                }
                                                            }
                                                        ],
                                                        "query": {
                                                            "dis_max": {
                                                                "queries": [
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.1,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_one_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.2,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_two_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.3,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_three_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.4,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_four_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.5,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_five_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.6,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_six_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.7,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_seven_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.8,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_eight_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 0.9,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_nine_no_exit": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                        }
                                                                    },
                                                                    {
                                                                        "constant_score": {
                                                                            "boost": 1,
                                                                            "filter": {
                                                                                "match_phrase": {
                                                                                    "org_news_noun_phrases_tier_ten_no_exit": {
                                                                                        "query": query_val
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
                                                {
                                                    "constant_score": {
                                                        "boost": 0.5,
                                                        "filter": {
                                                            "match_phrase": {
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


def tiered_news_make_description_tf_idf_news_bucket_score_collection_flat_X_log2p_equity_funding(
    query_val, es_from, es_size
):
    return {
        "explain": True,
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
                                                "modifier": "log2p",
                                            }
                                        },
                                        # {
                                        #     "field_value_factor": {
                                        #         "field": "num_expert_collections",
                                        #         "missing": 0,
                                        #         "modifier": "log2p",
                                        #     }
                                        # },
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
                                                        "boost": 15,
                                                        "queries": [
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.1,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_one_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.2,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_two_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.3,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_three_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.4,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_four_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.5,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_five_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.6,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_six_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.7,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_seven_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.8,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_eight_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 0.9,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_nine_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                            {
                                                                "constant_score": {
                                                                    "boost": 1,
                                                                    "filter": {
                                                                        "match_phrase": {
                                                                            "org_news_noun_phrases_tier_ten_no_exit": {
                                                                                "query": query_val
                                                                            }
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                        ],
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 0.5,
                                                        "filter": {
                                                            "match_phrase": {
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


def tiered_news_make_news_desc_tf_idf_times_equity_funding(query_val: str, es_from: int, es_size: int):
    return {
        "explain": True,
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
        "explain": True,
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
                                                "modifier": "ln2p",
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
        "explain": True,
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
        "explain": True,
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
                                                "modifier": "ln2p",
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
        "explain": True,
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
                                                "modifier": "ln2p",
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
                                                    "match_phrase": {
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
        "explain": True,
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
                                                "modifier": "ln2p",
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
                                                    "match_phrase": {
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
        "explain": True,
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
                                                "modifier": "ln2p",
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
                                                            "match_phrase": {
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
        "explain": True,
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
                                                "modifier": "ln2p",
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
                                                            "match_phrase": {
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


def tiered_news_make_description_tf_idf_news_tfidf_collection_tf_idf_X_ln_equity_funding_X_log_num_collections(
    query_val, es_from, es_size
):
    return {
        "explain": True,
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
                                                "modifier": "ln2p",
                                            }
                                        },
                                        {
                                            "field_value_factor": {
                                                "field": "num_expert_collections",
                                                "missing": 0,
                                                "modifier": "log2p",
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
                                                                        "boost": 0.10,
                                                                        "query": query_val,
                                                                    }
                                                                }
                                                            },
                                                        ]
                                                    }
                                                },
                                                {
                                                    "match_phrase": {
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


def tiered_news_make_description_tf_idf_0_5_x_news_tfidf_collection_tf_idf_X_log_equity_funding_X_log_num_collections(
    query_val, es_from, es_size
):
    return {
        "explain": True,
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
                                                "modifier": "ln2p",
                                            }
                                        },
                                        {
                                            "field_value_factor": {
                                                "field": "num_expert_collections",
                                                "missing": 0,
                                                "modifier": "log2p",
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
                                                    "match_phrase": {
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


def tiered_news_make_description_tf_idf_news_tfidf_collection_tf_idf_X_ln_2X_equity_funding_X_ln_num_collections(
    query_val, es_from, es_size
):
    return {
        "explain": True,
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
                                                "factor": 2,
                                                "field": "org_total_equity_funding",
                                                "missing": 1,
                                                "modifier": "ln2p",
                                            }
                                        },
                                        {
                                            "field_value_factor": {
                                                "field": "num_expert_collections",
                                                "missing": 0,
                                                "modifier": "ln2p",
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
                                                    "match_phrase": {
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
