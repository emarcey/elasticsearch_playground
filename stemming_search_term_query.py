from typing import Any, Dict


def make_search_term_body(query_val: str, size: int) -> Dict[str, Any]:
    return {
        "_source": True,
        "explain": True,
        "from": 0,
        "size": size,
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
                                                "field": "adjusted_total_equity_funding",
                                                "missing": 1,
                                                "modifier": "sqrt",
                                            }
                                        },
                                        {
                                            "field_value_factor": {
                                                "factor": 1,
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
                                                        "boost": 1,
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
                                                        "boost": 1,
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
                                                        "boost": 0.5,
                                                        "filter": {
                                                            "prefix": {
                                                                "search_term_org_investor_name_no_exits.keyword": query_val
                                                            }
                                                        },
                                                    }
                                                },
                                                {
                                                    "dis_max": {
                                                        "boost": 0.6,
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
                                                        ],
                                                    }
                                                },
                                                {
                                                    "constant_score": {
                                                        "boost": 2,
                                                        "filter": {
                                                            "match_phrase": {
                                                                "expert_collection_names": {"query": query_val}
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
