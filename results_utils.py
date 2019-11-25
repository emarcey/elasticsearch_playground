from collections import defaultdict
from itertools import product
from typing import Any, Dict, List
from statistics import median
from numpy import percentile

from const import DOUBLE_LINE
from data_classes import BenchmarkResults


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


def make_table_header(columns: List[str]) -> List[str]:
    dashes: List[str] = []
    for col in columns:
        dashes.append("-" * len(col))

    return ["|".join(columns), "|".join(dashes)]


def make_individual_results_row(row: Dict[str, Any]) -> List[str]:
    query_avg = round(sum(row["query_times"]) / len(row["query_times"]), 5)
    query_median = round(median(row["query_times"]), 5)
    query_max = round(percentile(row["query_times"], 95), 5)

    calculations = [
        f"{row['num_hits']}",
        f"{len(row['query_times'])}",
        f"{query_avg}",
        f"{query_median}",
        f"{query_max}",
    ]
    return "|".join(calculations)


def make_individual_results_table(query_type: str, results: List[BenchmarkResults]) -> List[str]:
    table_by_num_vals = {}
    for result in results:
        num_hits = len(result.query_hits)
        if num_hits not in table_by_num_vals:
            table_by_num_vals[num_hits] = {"query_times": [], "num_hits": num_hits}
        table_by_num_vals[num_hits]["query_times"].extend(result.query_times)

    columns = [
        f"Num Results",
        f"Num {query_type} Hits",
        f"{query_type} Avg Time",
        f"{query_type} Median Time",
        f"{query_type} 95th Percentile",
    ]

    md_rows = make_table_header(columns)

    rows = sorted(list(table_by_num_vals.values()), key=lambda x: x["num_hits"])
    for row in rows:
        md_rows.append(make_individual_results_row(row))
    return md_rows


def make_individual_results_md(results: List[BenchmarkResults], start_header_level: int = 3) -> List[str]:
    start_header = "#" * start_header_level
    md_rows = [f"{start_header} Individual Results", DOUBLE_LINE]

    result_map: Dict[str, List[BenchmarkResults]] = defaultdict(list)
    for result in results:
        result_map[result.query_type].append(result)

    table_header = "#" * (start_header_level + 1)
    for query_type, type_results in result_map.items():

        md_rows.append(f"{table_header} {query_type}")
        md_rows.extend(make_individual_results_table(query_type, type_results))
        md_rows.append("\n")

    return md_rows


def make_comparative_results_row(row: Dict[str, Any]) -> List[str]:
    query1_avg = round(sum(row["query1_times"]) / len(row["query1_times"]), 5)
    query1_median = round(median(row["query1_times"]), 5)
    query1_max = round(percentile(row["query1_times"], 95), 5)
    query2_avg = round(sum(row["query2_times"]) / len(row["query2_times"]), 5)
    query2_median = round(median(row["query2_times"]), 5)
    query2_max = round(percentile(row["query2_times"], 95), 5)

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


def make_comparative_results_table(
    query_1_type: str,
    query_2_type: str,
    query_results_1: List[BenchmarkResults],
    query_results_2: List[BenchmarkResults],
):
    table_by_num_vals = {}
    for row in query_results_1:
        num_query1_hits = len(row.query_hits)
        if num_query1_hits not in table_by_num_vals:
            table_by_num_vals[num_query1_hits] = {"query1_times": [], "query2_times": [], "num_hits": num_query1_hits}
        table_by_num_vals[num_query1_hits]["query1_times"].extend(row.query_times)

    for row in query_results_2:
        num_query2_hits = len(row.query_hits)
        if num_query2_hits not in table_by_num_vals:
            table_by_num_vals[num_query2_hits] = {"query1_times": [], "query2_times": [], "num_hits": num_query2_hits}
        table_by_num_vals[num_query2_hits]["query2_times"].extend(row.query_times)

    columns = [
        f"Num Results",
        f"Num {query_1_type} Hits",
        f"Num {query_2_type} Hits",
        f"{query_1_type} Avg Time",
        f"{query_2_type} Avg Time",
        f"\% Decrease in Avg",
        f"{query_1_type} Median Time",
        f"{query_2_type} Median Time",
        f"\% Decrease in Median",
        f"{query_1_type} 95th Percentile",
        f"{query_2_type} 95th Percentile",
        f"\% Decrease in 95th Percentile",
    ]

    md_rows = make_table_header(columns)

    rows = sorted(list(table_by_num_vals.values()), key=lambda x: x["num_hits"])
    for row in rows:
        md_rows.append(make_comparative_results_row(row))
    return md_rows


def make_comparative_results_md(results: List[BenchmarkResults], start_header_level: int = 3) -> List[str]:
    start_header = "#" * start_header_level
    md_rows = [f"{start_header} Comparative Results"]

    results_map: Dict[str, List[BenchmarkResults]] = defaultdict(list)

    for result in results:
        results_map[result.query_type].append(result)

    table_header = "#" * (start_header_level + 1)
    for query_1, query_2 in product(results_map.values(), results_map.values()):
        query_1_type = query_1[0].query_type
        query_2_type = query_2[0].query_type
        if query_1_type == query_2_type:
            continue

        md_rows.append(f"{table_header} {query_1_type} vs {query_2_type}")
        md_rows.extend(make_comparative_results_table(query_1_type, query_2_type, query_1, query_2))
        md_rows.append(DOUBLE_LINE)

    return md_rows
