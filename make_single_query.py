import requests
import time
import json
from statistics import median
import itertools
import numpy as np
import os

from const import ENV, ELASTICSEARCH_HOST_URL, HEADER, DOUBLE_LINE, TABLES_DIR, SEARCH_TERMS


def make_full_url(url: str, index: str) -> str:
    return f"{url}/{index}/_search?request_cache=false"


def make_filename(
    dir_name: str, num_clauses: int, es_from: int, es_size: int, num_iterations: int, file_extension: str, index: str
) -> str:
    return f"{os.getcwd()}/{dir_name}/{num_clauses}_{es_from}_{es_size}_{num_iterations}_{index}.{file_extension}"


def make_setup_print(
    env: str, index: str, es_from, es_size: int, num_iterations: int, num_clauses: int = 0, queries=[], fields=[]
):
    lines = [
        "## Testing Parameters",
        f"* __Env__: {env}",
        f"* __Index__: {index}",
        f"* __Number of Iterations__: {num_iterations}",
    ]

    if isinstance(es_from, int):
        lines.append(f"* __From__: {es_from}")
    else:
        lines.append(f"* __Froms__: {', '.join(map(str, es_from))}")
    if isinstance(es_size, int):
        lines.append(f"* __Size__: {es_size}")
    else:
        lines.append(f"* __Sizes__: {', '.join(map(str, es_size))}")

    if num_clauses:
        lines.append(f"* __Max Nmber of Clauses__: {num_clauses}")
    if queries:
        lines.append(f"* __Queries Used__: {', '.join(queries)}")
    if fields:
        lines.append(f"* __Fields Used__: {', '.join(fields)}")
    return "\n".join(lines)


def make_table(query_type_1: str, query_type_2: str, results):
    lines = [
        # f"#### {query_type}",
        f"Search Term |{query_type_1} Num Results | {query_type_2} Num Results|{query_type_1} Avg Time|{query_type_1} Max Time|{query_type_1} Min Time|{query_type_1} Median Time|{query_type_2} Avg Time|{query_type_2} Max Time|{query_type_2} Min Time|{query_type_2} Median Time",
        "------------|--------------------|-----------------|----------------|----------------|----------------|-------------------|-------------|-------------|-------------|----------------",
    ]
    for row in results:
        lines.append(make_print(row))
    return "\n".join(lines)


def make_group_table(query_type_1: str, query_type_2, results):
    table_by_num_vals = {}
    for row in results:
        num_query1_hits = len(row["query1_hits"])
        if num_query1_hits not in table_by_num_vals:
            table_by_num_vals[num_query1_hits] = {"query1_times": [], "query2_times": [], "num_hits": num_query1_hits}
        table_by_num_vals[num_query1_hits]["query1_times"].extend(row["query1_times"])
        # table_by_num_vals[num_query1_hits]["query2_times"].extend(row["query2_times"])

        # num_query2_hits = len(row["query2_hits"])
        # if num_query2_hits not in table_by_num_vals:
        # table_by_num_vals[num_query2_hits] = {"query1_times": [], "query2_times": [], "num_hits": num_query2_hits}

        # table_by_num_vals[num_query2_hits]["query1_times"].extend(row["query1_times"])
        # table_by_num_vals[num_query2_hits]["query2_times"].extend(row["query2_times"])

    columns = [
        f"Num Results",
        f"Num {query_type_1} Hits",
        # f"Num {query_type_2} Hits",
        f"{query_type_1} Avg Time",
        # f"{query_type_2} Avg Time",
        # f"\% Difference in Avg",
        f"{query_type_1} Median Time",
        # f"{query_type_2} Median Time",
        # f"\% Difference in Median",
        f"{query_type_1} 95th Percentile",
        # f"{query_type_2} 95th Percentile",
        # f"\% Difference in 95th Percentile",
    ]

    dashes = []
    for col in columns:
        dashes.append("-" * len(columns))

    lines = [
        # f"#### {query_type}",
        "|".join(columns),
        "|".join(dashes),
    ]
    rows = sorted(list(table_by_num_vals.values()), key=lambda x: x["num_hits"])
    for row in rows:
        lines.append(make_group_print_row(row))
    return "\n".join(lines)


def make_differ(val1, val2):
    if val1 == 0 or val2 == 0:
        return "N/A"

    return round(((val1 - val2) / val1) * 100, 5)


def make_differ_with_emphasis(val1, val2):
    val = make_differ(val1, val2)
    if val > 5:
        return f"**{val}**"
    elif val < -5:
        return f"`{val}`"
    elif val >= 0:
        return f"*{val}*"
    else:
        return val


def make_group_print_row(row):
    query1_avg = round(sum(row["query1_times"]) / len(row["query1_times"]), 5)
    query1_median = round(median(row["query1_times"]), 5)
    query1_max = round(np.percentile(row["query1_times"], 95), 5)
    # query2_avg = round(sum(row["query2_times"]) / len(row["query2_times"]), 5)
    # query2_median = round(median(row["query2_times"]), 5)
    # query2_max = round(np.percentile(row["query2_times"], 95), 5)

    calculations = [
        f"{row['num_hits']}",
        f"{len(row['query1_times'])}",
        # f"{len(row['query2_times'])}",
        f"{query1_avg}",
        # f"{query2_avg}",
        # f"{make_differ_with_emphasis(query1_avg, query2_avg)}",
        f"{query1_median}",
        # f"{query2_median}",
        # f"{make_differ_with_emphasis(query1_median, query2_median)}",
        f"{query1_max}",
        # f"{query2_max}",
        # f"{make_differ_with_emphasis(query1_max, query2_max)}",
    ]
    return "|".join(calculations)


def single_query(
    query_type_1,
    query_type_1_maker,
    query_strings,
    es_from,
    es_sizes,
    num_iterations,
    index,
    file_descrip="query_comparison",
):

    filename = make_filename(TABLES_DIR, file_descrip, 0, 0, num_iterations, "md", index)
    with open(filename, "w") as f:
        f.write(f"# Benchmarking {query_type_1} {DOUBLE_LINE}")
        f.write(make_setup_print(ENV, index, es_from, es_sizes, num_iterations))
        f.write(DOUBLE_LINE)
        f.write("## Results")
        f.write(DOUBLE_LINE)

    results = []
    for es_size in es_sizes:
        full_url = make_full_url(ELASTICSEARCH_HOST_URL, index)
        # es_from = es_size * 2
        x = 1

        for query_val in query_strings:
            query1_times = []

            query1_query = query_type_1_maker(query_val, es_from, es_size)
            query1_dump = json.dumps(query1_query)

            print(f"\tQuery value {x}: {query_val}")
            x += 1

            for i in range(num_iterations):
                if i % 100 == 0 and i > 0:
                    print(f"\t\ttest {i}")
                start_time = time.time()
                query1_resp = requests.post(full_url, headers=HEADER, data=query1_dump)
                if query1_resp.status_code != 200:
                    print(f"query1_resp: {query1_resp.json()}")
                    raise ValueError("Bad response")

                end_time = time.time()

                query1_times.append((end_time - start_time) * 1000)

            query1_hits = query1_resp.json().get("hits", {}).get("hits", [])

            results.append({"query_val": query_val, "query1_hits": query1_hits, "query1_times": query1_times})

        print(make_group_table(query_type_1, query_type_2, results))

    with open(filename, "a") as f:
        f.write(f"### Using Size parameter: {es_size}")
        f.write(DOUBLE_LINE)
        f.write(make_group_table(query_type_1, query_type_2, results))
        f.write(DOUBLE_LINE)
