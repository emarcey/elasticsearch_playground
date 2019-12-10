import requests
import time
import json
from statistics import median
import itertools
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from typing import Tuple
import os
import string
from random import randint

from elasticsearch_types.livesearch import (
    create_livesearch_org_documents,
    ELASTICSEARCH_HOST_URL,
    ELASTICSEARCH_AUTOCOMPLETE_INDEX,
)

from utils import (
    make_full_url,
    make_plot,
    make_plot_data,
    make_filename,
    make_setup_print,
    DOUBLE_LINE,
    TABLES_DIR,
    ENV,
)
from const import SAYT_NAMES

INDEX = ""
HEADER = {"Content-Type": "application/json"}
PLOT_DIR = "/plots/"
TABLES_DIR = "/tables/"

QUERY_STRING_NAME = "Query String"
SIMPLE_QUERY_STRING_NAME = "Simple Query String"
DOUBLE_LINE = "\n\n"


def make_suggest_query(query_val: str, _from: int = 0, size: int = 10):
    return {
        "from": _from,
        "size": size,
        "suggest": {
            "my_suggestor": {
                "completion": {
                    "contexts": {
                        "id_team_tag": [{"boost": 1, "context": "0"}],
                        "id_user_collection": [{"boost": 1, "context": "1"}],
                        "is_expert_collection": [{"boost": 1, "context": "true"}],
                        "object_type": [{"boost": 2, "context": "org"}],
                    },
                    "field": "suggest",
                    "fuzzy": {"fuzziness": 0, "transpositions": "true"},
                    "size": size,
                    "skip_duplicates": "false",
                },
                "prefix": query_val,
            }
        },
    }


def make_search_as_you_type_query(query_val: str, _from: int = 0, size: int = 10):
    return {
        "from": _from,
        "size": size,
        "query": {
            "script_score": {
                "script": {
                    "source": "(Math.log10(Math.max(_score,1) * 2) / Math.log10(2)) * Math.log10(Math.max(doc['page_views'].size() == 0 ? 1 : doc['page_views'].value * 10, 1) * 10)"
                },
                "query": {
                    "bool": {
                        "minimum_should_match": 1,
                        "should": [
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "multi_match": {
                                                "query": query_val,
                                                "fields": ["name_search_as_you_type*"],
                                                "boost": 2,
                                                "type": "bool_prefix",
                                            }
                                        }
                                    ],
                                    "filter": [{"match": {"object_type": "org"}}],
                                }
                            },
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "multi_match": {
                                                "query": query_val,
                                                "fields": ["name_search_as_you_type*"],
                                                "boost": 1,
                                                "type": "bool_prefix",
                                            }
                                        }
                                    ],
                                    "filter": [{"term": {"is_expert_collection": "true"}}],
                                }
                            },
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "multi_match": {
                                                "query": query_val,
                                                "fields": ["name_search_as_you_type*"],
                                                "boost": 1,
                                                "type": "bool_prefix",
                                            }
                                        }
                                    ],
                                    "filter": [{"term": {"is_expert_collection": "true"}}],
                                }
                            },
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "multi_match": {
                                                "query": query_val,
                                                "fields": ["name_search_as_you_type*"],
                                                "boost": 1,
                                                "type": "bool_prefix",
                                            }
                                        }
                                    ],
                                    "filter": [{"term": {"id_user_collection": 0}}],
                                }
                            },
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "multi_match": {
                                                "query": query_val,
                                                "fields": ["name_search_as_you_type*"],
                                                "boost": 1,
                                                "type": "bool_prefix",
                                            }
                                        }
                                    ],
                                    "filter": [{"match": {"id_team_tag": 0}}],
                                }
                            },
                        ],
                    }
                },
            }
        },
    }


def make_table(results):
    lines = [
        # f"#### {query_type}",
        "Query String|Suggest Num Results | SAYT Num Results|Suggest Avg Time|Suggest Max Time|Suggest Min Time|Suggest Median Time|SAYT Avg Time|SAYT Max Time|SAYT Min Time|SAYT Median Time",
        "------------|--------------------|-----------------|----------------|----------------|----------------|-------------------|-------------|-------------|-------------|----------------",
    ]
    for row in results:
        lines.append(make_print(row))
    return "\n".join(lines)


def make_group_table(results):
    table_by_num_vals = {}
    for row in results:
        num_suggest_hits = len(row["suggest_hits"])
        if num_suggest_hits not in table_by_num_vals:
            table_by_num_vals[num_suggest_hits] = {"suggest_times": [], "sayt_times": [], "num_hits": num_suggest_hits}

        table_by_num_vals[num_suggest_hits]["suggest_times"].extend(row["suggest_times"])
        table_by_num_vals[num_suggest_hits]["sayt_times"].extend(row["sayt_times"])

        num_sayt_hits = len(row["sayt_hits"])
        if num_sayt_hits not in table_by_num_vals:
            table_by_num_vals[num_sayt_hits] = {"suggest_times": [], "sayt_times": [], "num_hits": num_sayt_hits}

        table_by_num_vals[num_sayt_hits]["suggest_times"].extend(row["suggest_times"])
        table_by_num_vals[num_sayt_hits]["sayt_times"].extend(row["sayt_times"])

    lines = [
        # f"#### {query_type}",
        "Num Results |Suggest Avg Time|SAYT Avg Time|Avg Suggest/SAYT \%|Suggest Median Time|SAYT Median Time|Median Suggest/SAYT \%",
        "------------|----------------|-------------|-------------------|-------------------|-----------------|----------------------",
    ]
    rows = sorted(list(table_by_num_vals.values()), key=lambda x: x["num_hits"])
    for row in rows:
        lines.append(make_group_print_row(row))
    return "\n".join(lines)


def make_differ(val1, val2):
    if val1 == 0 or val2 == 0:
        return "N/A"

    return round(((val1 - val2) / val1) * 100, 5)


def make_group_print_row(row):
    suggest_avg = round(sum(row["suggest_times"]) / len(row["suggest_times"]), 5)
    suggest_median = round(median(row["suggest_times"]), 5)
    sayt_avg = round(sum(row["sayt_times"]) / len(row["sayt_times"]), 5)
    sayt_median = round(median(row["sayt_times"]), 5)

    return f"{row['num_hits']} | {suggest_avg}| {sayt_avg} | {make_differ(suggest_avg, sayt_avg)}| {suggest_median}| {sayt_median} | {make_differ(suggest_median, sayt_median)}"


def make_print(row):
    return f"{row['query_val']} | {len(row['suggest_hits'])} | {len(row['sayt_hits'])} | {round(sum(row['suggest_times'])/len(row['suggest_times']), 5)}| {round(min(row['suggest_times']), 5)}| {round(median(row['suggest_times']), 5)} | {round(sum(row['sayt_times'])/len(row['sayt_times']), 5)}| {round(max(row['sayt_times']), 5)}| {round(min(row['sayt_times']), 5)}| {round(median(row['sayt_times']), 5)}"


def main():
    num_iterations = 50
    # es_from_sizes = [(0, 10)]  # , (0, 50), (0, 100)]  # , (100, 1000), (1000, 1000)]

    groups = ("Suggest", "Search As You Type")
    es_sizes = [5, 10, 25]  # , 50, 100]
    es_from = 0
    filename = make_filename(
        TABLES_DIR, "searchasyoutype", 0, 0, num_iterations, "md", ELASTICSEARCH_AUTOCOMPLETE_INDEX
    )
    with open(filename, "w") as f:
        f.write(f"# Comparing Suggest and Search As You Type{DOUBLE_LINE}")
        f.write(make_setup_print(ENV, ELASTICSEARCH_AUTOCOMPLETE_INDEX, es_from, es_sizes, num_iterations))
        f.write(DOUBLE_LINE)
        f.write("## Results")
        f.write(DOUBLE_LINE)
    for es_size in es_sizes:
        full_url = make_full_url(ELASTICSEARCH_HOST_URL, ELASTICSEARCH_AUTOCOMPLETE_INDEX)

        x = 1
        suggest_data_points = []
        sayt_data_points = []

        results = []

        query_strings = set()
        exclude = set(string.punctuation)
        for name in SAYT_NAMES:
            for n in name.split(" "):
                s = "".join(ch for ch in n if ch not in exclude)
                if s.isdigit() or len(s) == 0:
                    continue
                # if len(s) > 4:
                # s = s[: randint(1, 3)]
                query_strings.add(s)

        for query_val in list(query_strings)[:100]:
            suggest_times = []
            sayt_times = []

            suggest_query = make_suggest_query(query_val, es_from, es_size)
            suggest_dump = json.dumps(suggest_query)
            sayt_query = make_search_as_you_type_query(query_val, es_from, es_size)
            sayt_dump = json.dumps(sayt_query)

            print(f"\tQuery value {x}: {query_val}")
            x += 1

            for i in range(num_iterations):
                if i % 100 == 0 and i > 0:
                    print(f"\t\ttest {i}")
                start_time = time.time()
                suggest_resp = requests.post(full_url, headers=HEADER, data=suggest_dump)
                assert suggest_resp.status_code == 200

                # print(f"suggest_resp: {suggest_resp.json()}")

                middle_time = time.time()
                sayt_resp = requests.post(full_url, headers=HEADER, data=sayt_dump)
                # print(f"sayt_resp: {sayt_resp.json()}")
                assert sayt_resp.status_code == 200

                end_time = time.time()

                suggest_times.append((middle_time - start_time) * 1000)
                sayt_times.append((end_time - middle_time) * 1000)

            suggest_hits = []

            for suggestions in suggest_resp.json().get("suggest", {}).get("my_suggestor", []):
                suggest_hits.extend(suggestions.get("options", []))

            sayt_hits = sayt_resp.json().get("hits", {}).get("hits", [])

            results.append(
                {
                    "query_val": query_val,
                    "suggest_hits": suggest_hits,
                    "sayt_hits": sayt_hits,
                    "suggest_times": suggest_times,
                    "sayt_times": sayt_times,
                }
            )
            suggest_data_points.append(make_plot_data(suggest_hits, suggest_times))
            sayt_data_points.append(make_plot_data(sayt_hits, sayt_times))

        # print(make_table(results))

        print(make_group_table(results))

        make_plot(
            (tuple(suggest_data_points), tuple(sayt_data_points)),
            "searchasyoutype",
            es_from,
            es_size,
            num_iterations,
            ELASTICSEARCH_AUTOCOMPLETE_INDEX,
            groups,
            xlabel="Number of Results",
        )

        with open(filename, "a") as f:
            # f.write(f"# Comparing Suggest and Search As You Type{DOUBLE_LINE}")
            # f.write(make_setup_print(ENV, ELASTICSEARCH_AUTOCOMPLETE_INDEX, es_from, es_size, num_iterations))

            f.write(f"### Using Size parameter: {es_size}")
            f.write(DOUBLE_LINE)
            f.write(make_group_table(results))
            f.write(DOUBLE_LINE)

            # f.write(f"## Queries{DOUBLE_LINE}")
            # f.write(make_table(QUERY_STRING_NAME, qs_prints))
            # f.write(DOUBLE_LINE)
            # f.write(make_table(SIMPLE_QUERY_STRING_NAME, simple_prints))

        # suggest_data_points.append(make_plot_data(query_string_queries, suggest_times))
        # sayt_data_points.append(make_plot_data(sayt_queries, sayt_times))


if __name__ == "__main__":
    main()
