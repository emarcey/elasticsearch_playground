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

ENV = "dev"
URL = f"http://elasticsearch-{ENV}.cbinsights.com:9200"
INDEX = "tag"
HEADER = {"Content-Type": "application/json"}
PLOT_DIR = "/plots/"
TABLES_DIR = "/tables/"

QUERY_STRING_NAME = "Query String"
SIMPLE_QUERY_STRING_NAME = "Simple Query String"
DOUBLE_LINE = "\n\n"


def make_nested_query_string_query(field_name: str, query: str):
    return {"nested": {"path": "org", "query": {"query_string": {"default_field": field_name, "query": query}}}}


def make_query_string_query(field_name: str, query: str):
    return {"query_string": {"default_field": field_name, "query": query}}


def make_nested_simple_query_string_query(field_name: str, query: str):
    return {"nested": {"path": "org", "query": {"simple_query_string": {"fields": [field_name], "query": query}}}}


def make_simple_query_string_query(field_name: str, query: str):
    return {"simple_query_string": {"fields": [field_name], "query": query}}


def make_full_url(url: str, index: str) -> str:
    return f"{url}/{index}/_search"


def make_title() -> str:
    return f"Number of clauses against median time."


def make_filename(
    dir_name: str, num_clauses: int, es_from: int, es_size: int, num_iterations: int, file_extension: str
) -> str:
    return f"{os.getcwd()}/{dir_name}/{num_clauses}_{es_from}_{es_size}_{num_iterations}.{file_extension}"


def make_plot(
    data: Tuple[Tuple[int, float]], num_clauses: int, es_from: int, es_size: int, num_iterations: int
) -> None:
    colors = ("green", "blue")
    groups = (QUERY_STRING_NAME, SIMPLE_QUERY_STRING_NAME)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for data, color, group in zip(data, colors, groups):
        x = [row[0] for row in data]
        y = [row[1] for row in data]
        ax.scatter(x, y, c=color, label=group)

    plt.title(make_title())
    plt.xlabel("Number of Clauses")
    plt.ylabel("Median Query Time (ms)")

    plt.legend(loc=2)
    plt.savefig(make_filename(PLOT_DIR, num_clauses, es_from, es_size, num_iterations, "png"))


def make_plot_data(queries, times):
    return (len(queries), median(times))


def make_table(query_type, query_prints):
    lines = [
        f"#### {query_type}",
        "Num Queries|Avg Time|Max Time|Min Time|Median Time",
        "-----------|--------|--------|--------|-----------",
    ]
    for qp in query_prints:
        lines.append(make_print(qp[0], qp[1]))
    return "\n".join(lines)


def make_print(num_queries, times):
    return f"{num_queries} | {round(sum(times)/len(times), 5)}| {round(max(times), 5)}| {round(min(times), 5)}| {round(median(times), 5)}"


def make_setup_print(
    env: str, index: str, es_from: int, es_size: int, num_iterations: int, num_clauses: int, queries, fields
):
    lines = [
        "## Testing Parameters",
        f"* __Env__: {env}",
        f"* __Index__: {index}",
        f"* __From__: {es_from}",
        f"* __Size__: {es_size}",
        f"* __Number of Iterations__: {num_iterations}",
        f"* __Max Nmber of Clauses__: {num_clauses}",
        f"* __Queries Used__: {', '.join(queries)}",
        f"* __Fields Used__: {', '.join(fields)}",
    ]
    return "\n".join(lines)


QUERY_STRING_QUERY = {"query": {"bool": {"should": [], "minimum_should_match": 1}}}

SIMPLE_QUERY_STRING_QUERY = {"query": {"bool": {"should": [], "minimum_should_match": 1}}}


queries = [
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
]
fields = [
    "org.org_company_name",
    "org.org_name",
    "org.org_investor_name",
    "org.org_description",
    "org.org_taxonomy_industry",
    "org.org_taxonomy_sector",
    "org.org_taxonomy_subindustry",
    "org.org_url",
    "org.org_address_country",
]


def main():
    num_iterations = 1000
    es_from_sizes = [(0, 10), (0, 50), (0, 100), (100, 1000), (1000, 1000)]
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

        for query, field_name in itertools.product(queries, fields):

            qs_times = []
            simple_times = []

            query_string_queries.append(make_nested_query_string_query(field_name, query))
            qs_data = QUERY_STRING_QUERY
            qs_data["query"]["bool"]["should"] = query_string_queries
            qs_data["from"] = es_from
            qs_data["size"] = es_size
            qs_dump = json.dumps(qs_data)

            simple_queries.append(make_nested_simple_query_string_query(field_name, query))
            simple_data = SIMPLE_QUERY_STRING_QUERY
            simple_data["query"]["bool"]["should"] = simple_queries
            simple_data["from"] = es_from
            simple_data["size"] = es_size
            simple_dump = json.dumps(simple_data)

            if len(query_string_queries) % 10 != 5 and len(query_string_queries) != max_num_clauses:
                x += 1
                continue
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

        make_plot((tuple(qs_data_points), tuple(simple_data_points)), max_num_clauses, es_from, es_size, num_iterations)

        with open(make_filename(TABLES_DIR, max_num_clauses, es_from, es_size, num_iterations, "md"), "w") as f:
            f.write(f"# Comparing {QUERY_STRING_NAME} and {SIMPLE_QUERY_STRING_NAME}{DOUBLE_LINE}")
            f.write(make_setup_print(ENV, INDEX, es_from, es_size, num_iterations, max_num_clauses, queries, fields))
            f.write(DOUBLE_LINE)

            f.write(f"## Queries{DOUBLE_LINE}")
            f.write(make_table(QUERY_STRING_NAME, qs_prints))
            f.write(DOUBLE_LINE)
            f.write(make_table(SIMPLE_QUERY_STRING_NAME, simple_prints))


main()
