from multi_compare_queries import compare_queries
from data_classes import Query, QueryParams
from const import SEARCH_TERMS, HEADER, URL_PARAMS
from request_utils import update_refresh_interval


def get_funding_query(value: str, es_from: int, es_size: int):
    return {
        "_source": {
            "includes": [
                "id_org",
                "org_logo_url",
                "org_url",
                "id_company",
                "id_investor",
                "org_description",
                "org_name",
                "org_company_name",
                "org_investor_name",
                "org_url",
                "id_org",
                "org_description",
                "id_org",
                "org_id_taxonomy_industry",
                "org_taxonomy_industry",
                "org_id_address_country",
                "org_address_country",
                "org_total_funding",
                "org_investor.id_org",
                "org_investor.id_company",
                "org_investor.org_name",
                "org_investor.id_investor",
                "org_last_exit_funding_id_round",
                "org_last_exit_funding_round",
            ]
        },
        "explain": False,
        "from": es_from,
        "size": es_size,
        "query": {
            "bool": {
                "filter": {
                    "range": {"id_company": {"from": "0", "include_lower": False, "include_upper": True, "to": None}}
                },
                "must": {
                    "bool": {
                        "should": [
                            {
                                "constant_score": {
                                    "boost": 22,
                                    "filter": {"match": {"org_name.keyword": {"query": value}}},
                                }
                            },
                            {
                                "constant_score": {
                                    "boost": 9,
                                    "filter": {
                                        "dis_max": {
                                            "queries": [
                                                {"match_phrase": {"org_name": {"query": value}}},
                                                {"prefix": {"search_term_org_url_no_exits.keyword": value}},
                                                {
                                                    "match_phrase": {
                                                        "search_term_org_description_no_name_no_exits": {
                                                            "query": value,
                                                            "slop": 5,
                                                        }
                                                    }
                                                },
                                            ]
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
                                                        "search_term_org_competitor_no_exits": {"query": value}
                                                    }
                                                },
                                                {"prefix": {"search_term_org_competitor_url_no_exits.keyword": value}},
                                            ]
                                        }
                                    },
                                }
                            },
                            {
                                "constant_score": {
                                    "boost": 3,
                                    "filter": {"prefix": {"search_term_org_investor_name_no_exits.keyword": value}},
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
                                                        "org_news_noun_phrases_tier_one_no_exit": {"query": value}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.85,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_two_no_exit": {"query": value}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.5,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_three_no_exit": {"query": value}
                                                    }
                                                },
                                            }
                                        },
                                        {
                                            "constant_score": {
                                                "boost": 0.15,
                                                "filter": {
                                                    "match_phrase": {
                                                        "org_news_noun_phrases_tier_four_no_exit": {"query": value}
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
        "size": 25,
        "sort": [{"_score": {"order": "desc"}}, {"org_last_funding_funding_date": {"order": "desc"}}],
    }


def main():
    num_iterations = 70
    # max_pages = 5
    num_search_terms = 20
    es_sizes = [25]  # 25, 50]
    query = Query("Funding Query", get_funding_query)
    qp = QueryParams(
        es_sizes=es_sizes,
        base_url="http://elasticsearch-prd.cbinsights.com:9200",
        index="funding-company-read",
        es_from=0,
        num_iterations=num_iterations,
        params=URL_PARAMS,
        header=HEADER,
    )
    refresh_interval = -1
    print("running refresh interval", refresh_interval)
    qp.refresh_interval = refresh_interval
    # update_refresh_interval(qp.base_url, qp.index, refresh_interval)
    compare_queries([query], SEARCH_TERMS[:num_search_terms], qp, f"refresh_interval_{refresh_interval}")
    update_refresh_interval(qp.base_url, qp.index, 1)


if __name__ == "__main__":
    main()
