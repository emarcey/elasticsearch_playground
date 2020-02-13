def make_current_prd_query(query_val: str, es_from: int, es_size: int):
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
