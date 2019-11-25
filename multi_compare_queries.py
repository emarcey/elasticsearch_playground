from json import dumps
from requests import post
import time
from typing import Any, Dict, List, Tuple
from itertools import product

from request_utils import clear_cache, make_full_url
from results_utils import make_individual_results_md, make_comparative_results_md, make_setup_print
from file_utils import make_filename
from data_classes import Query, QueryParams, BenchmarkResults
from const import ENV, TABLES_DIR, DOUBLE_LINE


def run_query_iterations(request_body: Dict[str, Any], query_params: QueryParams) -> Tuple[List[int], List[Any]]:
    full_url = make_full_url(query_params.base_url, query_params.index)
    query_times: List[int] = []
    query_hits: List[Any] = []
    for i in range(query_params.num_iterations):
        clear_cache(query_params.base_url, query_params.index)

        start_time = time.time()
        query_resp = post(full_url, headers=query_params.header, data=dumps(request_body), params=query_params.params)
        end_time = time.time()
        if query_resp.status_code != 200:
            raise ValueError(f"Bad response: {query_resp.json()}")

        query_hits = query_resp.json().get("hits", {}).get("hits", [])
        query_times.append(end_time - start_time)
    return query_times, query_hits


def compare_queries(
    queries: List[Query], query_vals: List[str], query_params: QueryParams, file_descrip="query_comparison"
):

    if not queries:
        raise ValueError("No queries received.")

    if not query_vals:
        raise ValueError("No query_vals received.")

    filename = make_filename(TABLES_DIR, file_descrip, "md")
    with open(filename, "w") as f:
        f.write(f"# Comparing Queries{DOUBLE_LINE}")
        f.write(
            make_setup_print(
                ENV, query_params.index, query_params.es_from, query_params.es_sizes, query_params.num_iterations
            )
        )
        f.write(DOUBLE_LINE)
        f.write("## Conclusion")
        f.write(DOUBLE_LINE)
        f.write("[Add decision here]")
        f.write(DOUBLE_LINE)

    results = []
    for query, query_val, es_size in product(queries, query_vals, query_params.es_sizes):
        print(f"*" * 10)
        print(f"Query: {query.query_type}")
        print(f"Query Val: {query_val}")
        print(f"Size: {es_size}")
        print(f"*" * 10)

        query_body = query.query_maker(query_val, query_params.es_from, es_size)

        query_times, query_hits = run_query_iterations(query_body, query_params)

        results.append(
            BenchmarkResults(
                es_size=es_size,
                query_val=query_val,
                query_type=query.query_type,
                query_times=query_times,
                query_hits=query_hits,
            )
        )

    with open(filename, "a") as f:
        f.write(f"## Results")
        f.write(DOUBLE_LINE)
        f.write("\n".join(make_individual_results_md(results)))
        if len(queries) > 1:
            f.write(DOUBLE_LINE)
            f.write("\n".join(make_comparative_results_md(results)))
