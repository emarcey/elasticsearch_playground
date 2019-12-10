from collections import defaultdict
from itertools import combinations
from typing import Any, Dict, List, Optional, Tuple, Union
from statistics import median
from numpy import percentile

from const import DOUBLE_LINE
from data_classes import BenchmarkResults


def make_setup_index_print(index: str, index_overrides: Optional[List[Optional[str]]] = None) -> str:
    index_line = f"* __Index__: {index}"
    if not index_overrides:
        return f"* __Index__: {index}"

    indexes_used: List[str] = []
    for index_override in index_overrides:
        index_used = index
        if index_override is not None:
            index_used = index_override
        indexes_used.append(index_used)
    return f"* __Index__: {', '.join(indexes_used)}"


def make_setup_print(
    env: str,
    index: str,
    es_from,
    es_size: int,
    num_iterations: int,
    num_clauses: int = 0,
    queries: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
    index_overrides: Optional[List[Optional[str]]] = None,
):
    lines = [
        "## Testing Parameters",
        f"* __Env__: {env}",
        make_setup_index_print(index, index_overrides),
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


def get_avg_median_95th(times: List[float]) -> Tuple[Union[str, float], Union[str, float], Union[str, float]]:
    num_times = len(times)
    if num_times == 0:
        return "N/A", "N/A", "N/A"
    return num_times, round(sum(times) / num_times, 5), round(median(times), 5), round(percentile(times, 95), 5)


def make_individual_results_row(row: Dict[str, Any]) -> List[str]:
    num_times, query_avg, query_median, query_max = get_avg_median_95th(row["query_times"])
    calculations = [
        f"{row['num_hits']}",
        f"{num_times}",
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
    query_1_num_times, query1_avg, query1_median, query1_max = get_avg_median_95th(row["query1_times"])
    query_2_num_times, query2_avg, query2_median, query2_max = get_avg_median_95th(row["query2_times"])

    avg_differ = "N/A"
    median_differ = "N/A"
    max_differ = "N/A"
    if query_1_num_times > 0 and query_2_num_times > 0:
        avg_differ = make_differ_with_emphasis(query1_avg, query2_avg)
        median_differ = make_differ_with_emphasis(query1_median, query2_median)
        max_differ = make_differ_with_emphasis(query1_max, query2_max)

    calculations = [
        f"{row['num_hits']}",
        f"{len(row['query1_times'])}",
        f"{len(row['query2_times'])}",
        f"{query1_avg}",
        f"{query2_avg}",
        f"{avg_differ}",
        f"{query1_median}",
        f"{query2_median}",
        f"{median_differ}",
        f"{query1_max}",
        f"{query2_max}",
        f"{max_differ}",
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
    comparisons_seen = set()
    for query_1, query_2 in combinations(results_map.values(), 2):
        query_1_type = query_1[0].query_type
        query_2_type = query_2[0].query_type
        if query_1_type == query_2_type:
            continue

        md_rows.append(f"{table_header} {query_1_type} vs {query_2_type}")
        md_rows.extend(make_comparative_results_table(query_1_type, query_2_type, query_1, query_2))
        md_rows.append(DOUBLE_LINE)

    return md_rows
