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

from utils import (
    make_plot,
    make_plot_data,
    make_table,
    make_print,
    make_setup_print,
    make_full_url,
    DOUBLE_LINE,
    TABLES_DIR,
    ENV,
    ELASTICSEARCH_HOST_URL as URL,
)

INDEX = ""
HEADER = {"Content-Type": "application/json"}
PLOT_DIR = "/plots/"

QUERY_STRING_NAME = "Query String"
SIMPLE_QUERY_STRING_NAME = "Simple Query String"


def make_nested_query_string_query(field_name: str, query: str):
    return {"nested": {"path": "org", "query": {"query_string": {"default_field": field_name, "query": query}}}}


def make_query_string_query(field_name: str, query: str):
    return {"query_string": {"default_field": field_name, "query": query}}


def make_nested_simple_query_string_query(field_name: str, query: str):
    return {"nested": {"path": "org", "query": {"simple_query_string": {"fields": [field_name], "query": query}}}}


def make_simple_query_string_query(field_name: str, query: str):
    return {"simple_query_string": {"fields": [field_name], "query": query}}


def make_title() -> str:
    return f"Number of clauses against median time."


def make_filename(
    dir_name: str, num_clauses, es_from: int, es_size: int, num_iterations: int, file_extension: str, index: str
) -> str:
    return f"{os.getcwd()}/{dir_name}/{num_clauses}_{es_from}_{es_size}_{num_iterations}_{index}.{file_extension}"


QUERY_STRING_QUERY = {"query": {"bool": {"should": [], "minimum_should_match": 1}}}

SIMPLE_QUERY_STRING_QUERY = {"query": {"bool": {"should": [], "minimum_should_match": 1}}}


queries = [
    "revolution",
    "human",
    "artificial",
    "intelligence",
    "work",
    "software",
    "engineering",
    "time",
    "element",
    "Uber",
    "America",
    "Canada",
    "Mobile",
    "repurpose",
    "portals",
]
fields = ["tag"]


def main():
    num_iterations = 1000
    es_from_sizes = [(0, 10), (0, 50), (0, 100)]  # , (100, 1000), (1000, 1000)]
    y = 1
    for es_from, es_size in es_from_sizes:
        full_url = make_full_url(URL, INDEX)

        simple_queries = []
        query_string_queries = []

        qs_prints = []
        simple_prints = []

        qs_data_points = []
        simple_data_points = []

        x = 1
        max_num_clauses = len(queries) * len(fields)

        print(f"Iteration {y} of {len(es_from_sizes)}: {es_from} {es_size}")
        y += 1

        groups = (QUERY_STRING_NAME, SIMPLE_QUERY_STRING_NAME)

        for query, field_name in itertools.product(queries, fields):

            qs_times = []
            simple_times = []

            query_string_queries.append(make_query_string_query(field_name, query))
            qs_data = QUERY_STRING_QUERY
            qs_data["query"]["bool"]["should"] = query_string_queries
            qs_data["from"] = es_from
            qs_data["size"] = es_size
            qs_dump = json.dumps(qs_data)

            simple_queries.append(make_simple_query_string_query(field_name, query))
            simple_data = SIMPLE_QUERY_STRING_QUERY
            simple_data["query"]["bool"]["should"] = simple_queries
            simple_data["from"] = es_from
            simple_data["size"] = es_size
            simple_dump = json.dumps(simple_data)

            # if len(query_string_queries) % 10 != 5 and len(query_string_queries) != max_num_clauses:
            #     x += 1
            #     continue
            print(f"\tIteration {x} of {max_num_clauses}: {query} {field_name}")
            x += 1

            for i in range(num_iterations):
                if i % 100 == 0 and i > 0:
                    print(f"\t\ttest {i}")
                start_time = time.time()
                resp = requests.post(full_url, headers=HEADER, data=qs_dump)
                assert resp.status_code == 200
                middle_time = time.time()
                resp = requests.post(full_url, headers=HEADER, data=simple_dump)
                assert resp.status_code == 200
                end_time = time.time()

                qs_times.append((middle_time - start_time) * 1000)
                simple_times.append((end_time - middle_time) * 1000)

            qs_prints.append((len(query_string_queries), qs_times))
            simple_prints.append((len(simple_queries), simple_times))
            qs_data_points.append(make_plot_data(query_string_queries, qs_times))
            simple_data_points.append(make_plot_data(simple_queries, simple_times))

        make_plot(
            (tuple(qs_data_points), tuple(simple_data_points)),
            max_num_clauses,
            es_from,
            es_size,
            num_iterations,
            INDEX,
            groups,
        )

        with open(make_filename(TABLES_DIR, max_num_clauses, es_from, es_size, num_iterations, "md", INDEX), "w") as f:
            f.write(f"# Comparing {QUERY_STRING_NAME} and {SIMPLE_QUERY_STRING_NAME}{DOUBLE_LINE}")
            f.write(make_setup_print(ENV, INDEX, es_from, es_size, num_iterations, max_num_clauses, queries, fields))
            f.write(DOUBLE_LINE)

            f.write(f"## Queries{DOUBLE_LINE}")
            f.write(make_table(QUERY_STRING_NAME, qs_prints))
            f.write(DOUBLE_LINE)
            f.write(make_table(SIMPLE_QUERY_STRING_NAME, simple_prints))


main()
