import requests
import time
import json
from statistics import median
import itertools
import numpy as np
import os
from collections import defaultdict
from uuid import uuid5, NAMESPACE_DNS

from const import ENV, ELASTICSEARCH_HOST_URL, HEADER, DOUBLE_LINE, TABLES_DIR

URL_PARAMS = {"request_cache": "false"}


def make_full_url(url: str, index: str) -> str:
    return f"{url}/{index}/_search"


def clear_cache(url: str, index: str):
    full_url = f"{url}/{index}/_cache/clear?request=true"
    r = requests.post(full_url)
    if r.status_code != 200:
        raise Exception(f"Error clearing cache: {r.json()}")


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
        table_by_num_vals[num_query1_hits]["query2_times"].extend(row["query2_times"])

        num_query2_hits = len(row["query2_hits"])
        if num_query2_hits not in table_by_num_vals:
            table_by_num_vals[num_query2_hits] = {"query1_times": [], "query2_times": [], "num_hits": num_query2_hits}
        table_by_num_vals[num_query2_hits]["query1_times"].extend(row["query1_times"])
        table_by_num_vals[num_query2_hits]["query2_times"].extend(row["query2_times"])

    columns = [
        f"Num Results",
        f"Num {query_type_1} Hits",
        f"Num {query_type_2} Hits",
        f"{query_type_1} Avg Time",
        f"{query_type_2} Avg Time",
        f"\% Decrease in Avg",
        f"{query_type_1} Median Time",
        f"{query_type_2} Median Time",
        f"\% Decrease in Median",
        f"{query_type_1} 95th Percentile",
        f"{query_type_2} 95th Percentile",
        f"\% Decrease in 95th Percentile",
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
    query2_avg = round(sum(row["query2_times"]) / len(row["query2_times"]), 5)
    query2_median = round(median(row["query2_times"]), 5)
    query2_max = round(np.percentile(row["query2_times"], 95), 5)

    calculations = [
        f"{row['num_hits']}",
        f"{len(row['query1_times'])}",
        f"{len(row['query2_times'])}",
        f"{query1_avg}",
        f"{query2_avg}",
        f"{make_differ_with_emphasis(query1_avg, query2_avg)}",
        f"{query1_median}",
        f"{query2_median}",
        f"{make_differ_with_emphasis(query1_median, query2_median)}",
        f"{query1_max}",
        f"{query2_max}",
        f"{make_differ_with_emphasis(query1_max, query2_max)}",
    ]
    return "|".join(calculations)


def make_print(row):
    return f"{row['query_val']} {len(row['query1_hits'])} | {len(row['query2_hits'])} | {round(sum(row['query1_times'])/len(row['query1_times']), 5)}| {round(max(row['query1_times']), 5)}| {round(min(row['query1_times']), 5)}| {round(median(row['query1_times']), 5)} | {round(sum(row['query2_times'])/len(row['query2_times']), 5)}| {round(max(row['query2_times']), 5)}| {round(min(row['query2_times']), 5)}| {round(median(row['query2_times']), 5)}"


def compare_queries(
    query_type_1,
    query_type_1_maker,
    query_type_2,
    query_type_2_maker,
    query_strings,
    es_from,
    es_sizes,
    num_iterations,
    index,
    file_descrip="query_comparison",
):
    groups = (query_type_1, query_type_2)

    filename = make_filename(TABLES_DIR, file_descrip, 0, 0, num_iterations, "md", index)
    with open(filename, "w") as f:
        f.write(f"# Comparing {query_type_1} and {query_type_2}{DOUBLE_LINE}")
        f.write(make_setup_print(ENV, index, es_from, es_sizes, num_iterations))
        f.write(DOUBLE_LINE)
        f.write("## Results")
        f.write(DOUBLE_LINE)

    results = []
    for es_size in es_sizes:
        full_url = make_full_url(ELASTICSEARCH_HOST_URL, index)
        x = 1

        for query_val in query_strings:
            query1_times = []
            query2_times = []

            query1_query = query_type_1_maker(query_val, es_from, es_size)
            query1_dump = json.dumps(query1_query)
            query2_query = query_type_2_maker(query_val, es_from, es_size)
            query2_dump = json.dumps(query2_query)

            print(f"\tQuery value {x}: {query_val}")
            x += 1

            for i in range(num_iterations):
                if i % 100 == 0 and i > 0:
                    print(f"\t\ttest {i}")
                    clear_cache(ELASTICSEARCH_HOST_URL, index)
                start_time = time.time()
                query1_resp = requests.post(full_url, headers=HEADER, data=query1_dump, params=URL_PARAMS)
                if query1_resp.status_code != 200:
                    print(f"query1_resp: {query1_resp.json()}")
                    raise ValueError("Bad response")

                middle_time = time.time()
                clear_cache(ELASTICSEARCH_HOST_URL, index)
                new_start_time = time.time()
                query2_resp = requests.post(full_url, headers=HEADER, data=query2_dump, params=URL_PARAMS)
                if query2_resp.status_code != 200:
                    print(f"query2_resp: {query2_resp.json()}")
                    raise ValueError("Bad response")

                end_time = time.time()

                query1_times.append((middle_time - start_time) * 1000)
                query2_times.append((end_time - new_start_time) * 1000)

            query1_hits = query1_resp.json().get("hits", {}).get("hits", [])
            query2_hits = query2_resp.json().get("hits", {}).get("hits", [])

            results.append(
                {
                    "query_val": query_val,
                    "query1_hits": query1_hits,
                    "query2_hits": query2_hits,
                    "query1_times": query1_times,
                    "query2_times": query2_times,
                }
            )

        print(make_table(query_type_1, query_type_2, results))

        print(make_group_table(query_type_1, query_type_2, results))

    with open(filename, "a") as f:
        f.write(f"### Using Size parameter: {es_size}")
        f.write(DOUBLE_LINE)
        f.write(make_group_table(query_type_1, query_type_2, results))
        f.write(DOUBLE_LINE)


def compare_query_preference_with_pagination(
    query_type_1,
    query_type_1_maker,
    query_strings,
    es_from,
    es_sizes,
    num_iterations,
    index,
    max_pages,
    file_descrip="query_comparison",
):
    query_type_2 = f"{query_type_1} with preference"
    groups = (query_type_1, query_type_2)

    filename = make_filename(TABLES_DIR, f"{file_descrip}_{num_iterations}", 0, 0, num_iterations, "md", index)
    with open(filename, "w") as f:
        f.write(f"# Comparing {query_type_1} with and without preference{DOUBLE_LINE}")
        f.write(make_setup_print(ENV, index, es_from, es_sizes, num_iterations))
        f.write(DOUBLE_LINE)
        f.write("## Results")
        f.write(DOUBLE_LINE)

    results = defaultdict(list)
    for es_size in es_sizes:
        full_url = make_full_url(ELASTICSEARCH_HOST_URL, index)

        x = 1

        for query_val in query_strings:

            query_string_uuid = str(uuid5(NAMESPACE_DNS, "query_val"))

            query1_params = {"request_cache": "true"}
            query2_params = {"request_cache": "true", "preference": query_string_uuid}

            print(f"\tQuery value {x}: {query_val}")
            x += 1

            query1_times_dict = defaultdict(list)
            query2_times_dict = defaultdict(list)
            query1_hits_dict = defaultdict(list)
            query2_hits_dict = defaultdict(list)

            print("\t\tBase Query")
            for i in range(num_iterations):
                if i % (num_iterations // 5) == 0:
                    print(f"\t\t\ttest {i}")
                clear_cache(ELASTICSEARCH_HOST_URL, index)

                for page_num in range(max_pages):
                    es_from = page_num * es_size
                    # query1_times = []
                    # query2_times = []

                    query = query_type_1_maker(query_val, es_from, es_size)
                    query_dump = json.dumps(query)

                    if i % (num_iterations // 5) == 0:
                        print(f"\t\t\t\tPage Number: {page_num}")

                    start_time = time.time()

                    query1_resp = requests.post(full_url, headers=HEADER, data=query_dump, params=query1_params)
                    if query1_resp.status_code != 200:
                        print(f"query1_resp: {query1_resp.json()}")
                        raise ValueError("Bad response")

                    middle_time = time.time()

                    query1_times_dict[page_num].append((middle_time - start_time) * 1000)

                    query1_hits_dict[page_num] = query1_resp.json().get("hits", {}).get("hits", [])
                    if len(query1_hits_dict[page_num]) < es_size:
                        break

            print("\t\tPreference Query")
            for i in range(num_iterations):
                if i % (num_iterations // 5) == 0:
                    print(f"\t\t\ttest {i}")
                clear_cache(ELASTICSEARCH_HOST_URL, index)

                for page_num in range(max_pages):
                    es_from = page_num * es_size
                    # query1_times = []
                    # query2_times = []

                    query = query_type_1_maker(query_val, es_from, es_size)
                    query_dump = json.dumps(query)

                    if i % (num_iterations // 5) == 0:
                        print(f"\t\t\t\tPage Number: {page_num}")

                    start_time = time.time()

                    query2_resp = requests.post(full_url, headers=HEADER, data=query_dump, params=query2_params)

                    if query2_resp.status_code != 200:
                        print(f"query2_resp: {query2_resp.json()}")
                        raise ValueError("Bad response")

                    end_time = time.time()

                    query2_times_dict[page_num].append((end_time - start_time) * 1000)

                    query2_hits_dict[page_num] = query2_resp.json().get("hits", {}).get("hits", [])
                    if len(query2_hits_dict[page_num]) < es_size:
                        break

            for page_num in range(max_pages):
                results[page_num].append(
                    {
                        "query_val": query_val,
                        "query1_hits": query1_hits_dict[page_num],
                        "query2_hits": query2_hits_dict[page_num],
                        "query1_times": query1_times_dict[page_num],
                        "query2_times": query2_times_dict[page_num],
                    }
                )

            for page_num in range(max_pages):
                page_results = results[page_num]
                if not page_results:
                    continue
                print(f"#### Page Number: {page_num}")
                print(make_group_table(query_type_1, query_type_2, page_results))

        for page_num in range(max_pages):
            page_results = results[page_num]
            if not page_results:
                continue
            print(f"#### Page Number: {page_num}")
            print(make_group_table(query_type_1, query_type_2, page_results))

    with open(filename, "a") as f:
        f.write(f"### Using Size parameter: {es_size}")
        f.write(DOUBLE_LINE)
        for page_num in range(max_pages):
            page_results = results[page_num]
            if not page_results:
                continue
            f.write(f"#### Page Number: {page_num}")
            f.write(DOUBLE_LINE)
            f.write(make_group_table(query_type_1, query_type_2, page_results))
            f.write(DOUBLE_LINE)


def compare_queries_with_pagination(
    query_type_1,
    query_type_1_maker,
    query_type_2,
    query_type_2_maker,
    query_strings,
    es_from,
    es_sizes,
    num_iterations,
    index,
    max_pages,
    file_descrip="query_comparison",
):
    groups = (query_type_1, query_type_2)

    filename = make_filename(TABLES_DIR, file_descrip, 0, 0, num_iterations, "md", index)
    with open(filename, "w") as f:
        f.write(f"# Comparing {query_type_1} and {query_type_2}{DOUBLE_LINE}")
        f.write(make_setup_print(ENV, index, es_from, es_sizes, num_iterations))
        f.write(DOUBLE_LINE)
        f.write("## Results")
        f.write(DOUBLE_LINE)

    results = []
    for es_size in es_sizes:
        full_url = make_full_url(ELASTICSEARCH_HOST_URL, index)
        es_from = es_size * 2
        x = 1

        query_params = {"request_cache": "false"}

        for query_val in query_strings:

            query1_query = query_type_1_maker(query_val, es_from, es_size)
            query1_dump = json.dumps(query1_query)
            query2_query = query_type_2_maker(query_val, es_from, es_size)
            query2_dump = json.dumps(query2_query)

            print(f"\tQuery value {x}: {query_val}")
            x += 1

            query1_times_dict = defaultdict(list)
            query2_times_dict = defaultdict(list)
            query1_hits_dict = defaultdict(list)
            query2_hits_dict = defaultdict(list)

            print(f"\t\t{query_type_1}")
            for i in range(num_iterations):
                if i % (num_iterations // 5) == 0:
                    print(f"\t\t\ttest {i}")
                clear_cache(ELASTICSEARCH_HOST_URL, index)

                for page_num in range(max_pages):
                    es_from = page_num * es_size
                    # query1_times = []
                    # query2_times = []

                    query = query_type_1_maker(query_val, es_from, es_size)
                    query_dump = json.dumps(query)

                    if i % (num_iterations // 5) == 0:
                        print(f"\t\t\t\tPage Number: {page_num}")

                    start_time = time.time()

                    query1_resp = requests.post(full_url, headers=HEADER, data=query1_dump, params=query_params)
                    if query1_resp.status_code != 200:
                        print(f"query1_resp: {query1_resp.json()}")
                        raise ValueError("Bad response")

                    middle_time = time.time()

                    query1_times_dict[page_num].append((middle_time - start_time) * 1000)

                    query1_hits_dict[page_num] = query1_resp.json().get("hits", {}).get("hits", [])
                    if len(query1_hits_dict[page_num]) < es_size:
                        break

            print(f"\t\t{query_type_2}")
            for i in range(num_iterations):
                if i % (num_iterations // 5) == 0:
                    print(f"\t\t\ttest {i}")
                clear_cache(ELASTICSEARCH_HOST_URL, index)

                for page_num in range(max_pages):
                    es_from = page_num * es_size
                    # query1_times = []
                    # query2_times = []

                    query = query_type_1_maker(query_val, es_from, es_size)
                    query_dump = json.dumps(query)

                    if i % (num_iterations // 5) == 0:
                        print(f"\t\t\t\tPage Number: {page_num}")

                    start_time = time.time()

                    middle_time = time.time()
                    query2_resp = requests.post(full_url, headers=HEADER, data=query1_dump, params=query_params)

                    if query2_resp.status_code != 200:
                        print(f"query2_resp: {query2_resp.json()}")
                        raise ValueError("Bad response")

                    end_time = time.time()

                    query2_times_dict[page_num].append((end_time - middle_time) * 1000)

                    query2_hits_dict[page_num] = query2_resp.json().get("hits", {}).get("hits", [])
                    if len(query2_hits_dict[page_num]) < es_size:
                        break

            for page_num in range(max_pages):
                results[page_num].append(
                    {
                        "query_val": query_val,
                        "query1_hits": query1_hits_dict[page_num],
                        "query2_hits": query2_hits_dict[page_num],
                        "query1_times": query1_times_dict[page_num],
                        "query2_times": query2_times_dict[page_num],
                    }
                )

            for page_num in range(max_pages):
                page_results = results[page_num]
                if not page_results:
                    continue
                print(f"#### Page Number: {page_num}")
                print(make_group_table(query_type_1, query_type_2, page_results))

        print(make_table(query_type_1, query_type_2, results))

        print(make_group_table(query_type_1, query_type_2, results))

    with open(filename, "a") as f:
        f.write(f"### Using Size parameter: {es_size}")
        f.write(DOUBLE_LINE)
        f.write(make_group_table(query_type_1, query_type_2, results))
        f.write(DOUBLE_LINE)
