from make_compare_query import compare_queries, compare_query_preference_with_pagination
from const import SEARCH_TERMS


def make_funding_query(query_val: str, es_from: int, es_size: int):
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
                                        "nested": {
                                            "path": "org.org",
                                            "query": {
                                                "constant_score": {
                                                    "boost": 22,
                                                    "filter": {
                                                        "match": {"org.org.org_name.keyword": {"query": query_val}}
                                                    },
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
                                        "nested": {
                                            "path": "org.org",
                                            "query": {
                                                "constant_score": {
                                                    "boost": 9,
                                                    "filter": {
                                                        "bool": {
                                                            "must_not": {
                                                                "range": {
                                                                    "org.org.org_num_exits": {
                                                                        "from": 1,
                                                                        "include_lower": True,
                                                                        "include_upper": True,
                                                                        "to": None,
                                                                    }
                                                                }
                                                            },
                                                            "should": [
                                                                {
                                                                    "match_phrase": {
                                                                        "org.org.org_name": {"query": query_val}
                                                                    }
                                                                },
                                                                {"prefix": {"org.org.org_url.keyword": query_val}},
                                                            ],
                                                        }
                                                    },
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
                                        "nested": {
                                            "path": "org.org",
                                            "query": {
                                                "constant_score": {
                                                    "boost": 9,
                                                    "filter": {
                                                        "bool": {
                                                            "must": {
                                                                "match_phrase": {
                                                                    "org.org.org_description": {
                                                                        "query": query_val,
                                                                        "slop": 5,
                                                                    }
                                                                }
                                                            },
                                                            "must_not": [
                                                                {
                                                                    "match_phrase": {
                                                                        "org.org.org_name": {"query": query_val}
                                                                    }
                                                                },
                                                                {
                                                                    "range": {
                                                                        "org.org.org_num_exits": {
                                                                            "from": 1,
                                                                            "include_lower": True,
                                                                            "include_upper": True,
                                                                            "to": None,
                                                                        }
                                                                    }
                                                                },
                                                            ],
                                                        }
                                                    },
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
                                            "boost": 6,
                                            "filter": {
                                                "bool": {
                                                    "must_not": {
                                                        "range": {
                                                            "org.org.org_num_exits": {
                                                                "from": 1,
                                                                "include_lower": True,
                                                                "include_upper": True,
                                                                "to": None,
                                                            }
                                                        }
                                                    },
                                                    "should": [
                                                        {"match_phrase": {"org.org_competitor": {"query": query_val}}},
                                                        {"prefix": {"org.competitor_url.keyword": query_val}},
                                                    ],
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
                                        "nested": {
                                            "path": "org.org_investor",
                                            "query": {
                                                "constant_score": {
                                                    "boost": 3,
                                                    "filter": {
                                                        "prefix": {"org.org_investor.org_name.keyword": query_val}
                                                    },
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
                                        "nested": {
                                            "path": "org.org_news_noun_phrases",
                                            "query": {
                                                "function_score": {
                                                    "functions": [
                                                        {
                                                            "field_value_factor": {
                                                                "field": "org.org_news_noun_phrases.containing_org_article_percentage",
                                                                "missing": 0,
                                                            }
                                                        }
                                                    ],
                                                    "query": {
                                                        "constant_score": {
                                                            "filter": {
                                                                "match_phrase": {
                                                                    "org.org_news_noun_phrases.noun_phrase": {
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
                                }
                            },
                        ]
                    }
                }
            }
        },
        "sort": [
            {"_score": {"order": "desc"}},
            # {
            #     "org.org_last_funding.funding_date": {
            #         "nested": {"nested": {"path": "org.org_last_funding"}, "path": "org"},
            #         "order": "desc",
            #     }
            # },
            # {"org.org.org_num_deals": {"nested": {"nested": {"path": "org.org"}, "path": "org"}, "order": "desc"}},
            {"_id": {"order": "asc"}},
        ],
    }


def make_funding_modified_exits_query(query_val: str, es_from: int, es_size: int):
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
                                        "nested": {
                                            "path": "org.org",
                                            "query": {
                                                "constant_score": {
                                                    "boost": 22,
                                                    "filter": {
                                                        "match": {"org.org.org_name.keyword": {"query": query_val}}
                                                    },
                                                }
                                            },
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
                                                "nested": {
                                                    "path": "org.org",
                                                    "query": {
                                                        "range": {
                                                            "org.org.org_num_exits": {
                                                                "from": 1,
                                                                "include_lower": True,
                                                                "include_upper": True,
                                                                "to": None,
                                                            }
                                                        }
                                                    },
                                                }
                                            },
                                        }
                                    },
                                    "should": [
                                        {
                                            "nested": {
                                                "path": "org",
                                                "query": {
                                                    "nested": {
                                                        "path": "org.org",
                                                        "query": {
                                                            "constant_score": {
                                                                "boost": 9,
                                                                "filter": {
                                                                    "bool": {
                                                                        "should": [
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org.org.org_name": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "prefix": {
                                                                                    "org.org.org_url.keyword": query_val
                                                                                }
                                                                            },
                                                                        ]
                                                                    }
                                                                },
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
                                                    "nested": {
                                                        "path": "org.org",
                                                        "query": {
                                                            "constant_score": {
                                                                "boost": 9,
                                                                "filter": {
                                                                    "bool": {
                                                                        "must": {
                                                                            "match_phrase": {
                                                                                "org.org.org_description": {
                                                                                    "query": query_val,
                                                                                    "slop": 5,
                                                                                }
                                                                            }
                                                                        },
                                                                        "must_not": {
                                                                            "match_phrase": {
                                                                                "org.org.org_name": {"query": query_val}
                                                                            }
                                                                        },
                                                                    }
                                                                },
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
                                                        "boost": 6,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "org.org_competitor": {"query": query_val}
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "org.competitor_url.keyword": query_val
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
                                            "nested": {
                                                "path": "org",
                                                "query": {
                                                    "nested": {
                                                        "path": "org.org_investor",
                                                        "query": {
                                                            "constant_score": {
                                                                "boost": 3,
                                                                "filter": {
                                                                    "prefix": {
                                                                        "org.org_investor.org_name.keyword": query_val
                                                                    }
                                                                },
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
                                                    "nested": {
                                                        "path": "org.org_news_noun_phrases",
                                                        "query": {
                                                            "function_score": {
                                                                "functions": [
                                                                    {
                                                                        "field_value_factor": {
                                                                            "field": "org.org_news_noun_phrases.containing_org_article_percentage",
                                                                            "missing": 0,
                                                                        }
                                                                    }
                                                                ],
                                                                "query": {
                                                                    "constant_score": {
                                                                        "filter": {
                                                                            "match_phrase": {
                                                                                "org.org_news_noun_phrases.noun_phrase": {
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
            {
                "org.org_last_funding.funding_date": {
                    "nested": {"nested": {"path": "org.org_last_funding"}, "path": "org"},
                    "order": "desc",
                }
            },
            {"org.org.org_num_deals": {"nested": {"nested": {"path": "org.org"}, "path": "org"}, "order": "desc"}},
            {"_id": {"order": "asc"}},
        ],
    }


def make_funding_query_exits_exists(query_val: str, es_from: int, es_size: int):
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
                                        "nested": {
                                            "path": "org.org",
                                            "query": {
                                                "constant_score": {
                                                    "boost": 22,
                                                    "filter": {
                                                        "match": {"org.org.org_name.keyword": {"query": query_val}}
                                                    },
                                                }
                                            },
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
                                                "nested": {
                                                    "path": "org.org",
                                                    "query": {"exists": {"field": "org.org.org_num_exits"}},
                                                }
                                            },
                                        }
                                    },
                                    "should": [
                                        {
                                            "nested": {
                                                "path": "org",
                                                "query": {
                                                    "nested": {
                                                        "path": "org.org",
                                                        "query": {
                                                            "constant_score": {
                                                                "boost": 9,
                                                                "filter": {
                                                                    "bool": {
                                                                        "should": [
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org.org.org_name": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "prefix": {
                                                                                    "org.org.org_url.keyword": query_val
                                                                                }
                                                                            },
                                                                        ]
                                                                    }
                                                                },
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
                                                    "nested": {
                                                        "path": "org.org",
                                                        "query": {
                                                            "constant_score": {
                                                                "boost": 9,
                                                                "filter": {
                                                                    "bool": {
                                                                        "must": {
                                                                            "match_phrase": {
                                                                                "org.org.org_description": {
                                                                                    "query": query_val,
                                                                                    "slop": 5,
                                                                                }
                                                                            }
                                                                        },
                                                                        "must_not": {
                                                                            "match_phrase": {
                                                                                "org.org.org_name": {"query": query_val}
                                                                            }
                                                                        },
                                                                    }
                                                                },
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
                                                        "boost": 6,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "org.org_competitor": {"query": query_val}
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "org.competitor_url.keyword": query_val
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
                                            "nested": {
                                                "path": "org",
                                                "query": {
                                                    "nested": {
                                                        "path": "org.org_investor",
                                                        "query": {
                                                            "constant_score": {
                                                                "boost": 3,
                                                                "filter": {
                                                                    "prefix": {
                                                                        "org.org_investor.org_name.keyword": query_val
                                                                    }
                                                                },
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
                                                    "nested": {
                                                        "path": "org.org_news_noun_phrases",
                                                        "query": {
                                                            "function_score": {
                                                                "functions": [
                                                                    {
                                                                        "field_value_factor": {
                                                                            "field": "org.org_news_noun_phrases.containing_org_article_percentage",
                                                                            "missing": 0,
                                                                        }
                                                                    }
                                                                ],
                                                                "query": {
                                                                    "constant_score": {
                                                                        "filter": {
                                                                            "match_phrase": {
                                                                                "org.org_news_noun_phrases.noun_phrase": {
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
            {
                "org.org_last_funding.funding_date": {
                    "nested": {"nested": {"path": "org.org_last_funding"}, "path": "org"},
                    "order": "desc",
                }
            },
            {"org.org.org_num_deals": {"nested": {"nested": {"path": "org.org"}, "path": "org"}, "order": "desc"}},
            {"_id": {"order": "asc"}},
        ],
    }


def make_funding_query_org_vc_backed_instead_of_exits(query_val: str, es_from: int, es_size: int):
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
                                        "nested": {
                                            "path": "org.org",
                                            "query": {
                                                "constant_score": {
                                                    "boost": 22,
                                                    "filter": {
                                                        "match": {"org.org.org_name.keyword": {"query": query_val}}
                                                    },
                                                }
                                            },
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
                                                "nested": {
                                                    "path": "org.org",
                                                    "query": {"term": {"org.org.org_vc_backed": "true"}},
                                                }
                                            },
                                        }
                                    },
                                    "should": [
                                        {
                                            "nested": {
                                                "path": "org",
                                                "query": {
                                                    "nested": {
                                                        "path": "org.org",
                                                        "query": {
                                                            "constant_score": {
                                                                "boost": 9,
                                                                "filter": {
                                                                    "bool": {
                                                                        "should": [
                                                                            {
                                                                                "match_phrase": {
                                                                                    "org.org.org_name": {
                                                                                        "query": query_val
                                                                                    }
                                                                                }
                                                                            },
                                                                            {
                                                                                "prefix": {
                                                                                    "org.org.org_url.keyword": query_val
                                                                                }
                                                                            },
                                                                        ]
                                                                    }
                                                                },
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
                                                    "nested": {
                                                        "path": "org.org",
                                                        "query": {
                                                            "constant_score": {
                                                                "boost": 9,
                                                                "filter": {
                                                                    "bool": {
                                                                        "must": {
                                                                            "match_phrase": {
                                                                                "org.org.org_description": {
                                                                                    "query": query_val,
                                                                                    "slop": 5,
                                                                                }
                                                                            }
                                                                        },
                                                                        "must_not": {
                                                                            "match_phrase": {
                                                                                "org.org.org_name": {"query": query_val}
                                                                            }
                                                                        },
                                                                    }
                                                                },
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
                                                        "boost": 6,
                                                        "filter": {
                                                            "bool": {
                                                                "should": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "org.org_competitor": {"query": query_val}
                                                                        }
                                                                    },
                                                                    {
                                                                        "prefix": {
                                                                            "org.competitor_url.keyword": query_val
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
                                            "nested": {
                                                "path": "org",
                                                "query": {
                                                    "nested": {
                                                        "path": "org.org_investor",
                                                        "query": {
                                                            "constant_score": {
                                                                "boost": 3,
                                                                "filter": {
                                                                    "prefix": {
                                                                        "org.org_investor.org_name.keyword": query_val
                                                                    }
                                                                },
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
                                                    "nested": {
                                                        "path": "org.org_news_noun_phrases",
                                                        "query": {
                                                            "function_score": {
                                                                "functions": [
                                                                    {
                                                                        "field_value_factor": {
                                                                            "field": "org.org_news_noun_phrases.containing_org_article_percentage",
                                                                            "missing": 0,
                                                                        }
                                                                    }
                                                                ],
                                                                "query": {
                                                                    "constant_score": {
                                                                        "filter": {
                                                                            "match_phrase": {
                                                                                "org.org_news_noun_phrases.noun_phrase": {
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
            {
                "org.org_last_funding.funding_date": {
                    "nested": {"nested": {"path": "org.org_last_funding"}, "path": "org"},
                    "order": "desc",
                }
            },
            {"org.org.org_num_deals": {"nested": {"nested": {"path": "org.org"}, "path": "org"}, "order": "desc"}},
            {"_id": {"order": "asc"}},
        ],
    }


def make_funding_query_no_sort(query_val: str, es_from: int, es_size: int):
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
                                        "nested": {
                                            "path": "org.org",
                                            "query": {
                                                "constant_score": {
                                                    "boost": 22,
                                                    "filter": {
                                                        "match": {"org.org.org_name.keyword": {"query": query_val}}
                                                    },
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
                                        "nested": {
                                            "path": "org.org",
                                            "query": {
                                                "constant_score": {
                                                    "boost": 9,
                                                    "filter": {
                                                        "bool": {
                                                            "must_not": {
                                                                "range": {
                                                                    "org.org.org_num_exits": {
                                                                        "from": 1,
                                                                        "include_lower": True,
                                                                        "include_upper": True,
                                                                        "to": None,
                                                                    }
                                                                }
                                                            },
                                                            "should": [
                                                                {
                                                                    "match_phrase": {
                                                                        "org.org.org_name": {"query": query_val}
                                                                    }
                                                                },
                                                                {"prefix": {"org.org.org_url.keyword": query_val}},
                                                            ],
                                                        }
                                                    },
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
                                        "nested": {
                                            "path": "org.org",
                                            "query": {
                                                "constant_score": {
                                                    "boost": 9,
                                                    "filter": {
                                                        "bool": {
                                                            "must": {
                                                                "match_phrase": {
                                                                    "org.org.org_description": {
                                                                        "query": query_val,
                                                                        "slop": 5,
                                                                    }
                                                                }
                                                            },
                                                            "must_not": [
                                                                {
                                                                    "match_phrase": {
                                                                        "org.org.org_name": {"query": query_val}
                                                                    }
                                                                },
                                                                {
                                                                    "range": {
                                                                        "org.org.org_num_exits": {
                                                                            "from": 1,
                                                                            "include_lower": True,
                                                                            "include_upper": True,
                                                                            "to": None,
                                                                        }
                                                                    }
                                                                },
                                                            ],
                                                        }
                                                    },
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
                                            "boost": 6,
                                            "filter": {
                                                "bool": {
                                                    "must_not": {
                                                        "range": {
                                                            "org.org.org_num_exits": {
                                                                "from": 1,
                                                                "include_lower": True,
                                                                "include_upper": True,
                                                                "to": None,
                                                            }
                                                        }
                                                    },
                                                    "should": [
                                                        {"match_phrase": {"org.org_competitor": {"query": query_val}}},
                                                        {"prefix": {"org.competitor_url.keyword": query_val}},
                                                    ],
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
                                        "nested": {
                                            "path": "org.org_investor",
                                            "query": {
                                                "constant_score": {
                                                    "boost": 3,
                                                    "filter": {
                                                        "prefix": {"org.org_investor.org_name.keyword": query_val}
                                                    },
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
                                        "nested": {
                                            "path": "org.org_news_noun_phrases",
                                            "query": {
                                                "function_score": {
                                                    "functions": [
                                                        {
                                                            "field_value_factor": {
                                                                "field": "org.org_news_noun_phrases.containing_org_article_percentage",
                                                                "missing": 0,
                                                            }
                                                        }
                                                    ],
                                                    "query": {
                                                        "constant_score": {
                                                            "filter": {
                                                                "match_phrase": {
                                                                    "org.org_news_noun_phrases.noun_phrase": {
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
                                }
                            },
                        ]
                    }
                }
            }
        },
        "sort": [
            {"_score": {"order": "desc"}},
            # {
            #     "org.org_last_funding.funding_date": {
            #         "nested": {"nested": {"path": "org.org_last_funding"}, "path": "org"},
            #         "order": "desc",
            #     }
            # },
            # {"org.org.org_num_deals": {"nested": {"nested": {"path": "org.org"}, "path": "org"}, "order": "desc"}},
            {"org.org.id_org": {"nested": {"nested": {"path": "org.org"}, "path": "org"}, "order": "asc"}},
        ],
    }


def main():
    num_iterations = 50
    max_pages = 5
    num_search_terms = 10
    es_sizes = [25]  # 25, 50]

    compare_queries(
        "Current Funding Query",
        make_funding_query,
        "No Sort Funding Query",
        make_funding_query_no_sort,
        SEARCH_TERMS[:num_search_terms],
        0,
        es_sizes,
        num_iterations,
        "",
    )

    # compare_queries(
    #     "Current Funding Query",
    #     make_funding_query,
    #     "Funding VC Backed Query",
    #     make_funding_query_org_vc_backed_instead_of_exits,
    #     SEARCH_TERMS,
    #     0,
    #     [25],
    #     num_iterations,
    #     "",
    # )

    # compare_query_preference_with_pagination(
    #     "Current Funding Query",
    #     make_funding_query,
    #     SEARCH_TERMS[:20],
    #     0,
    #     [25],
    #     num_iterations,
    #     "",
    #     max_pages,
    # )


if __name__ == "__main__":
    main()
