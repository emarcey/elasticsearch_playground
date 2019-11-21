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
PLOT_DIR = "/plots/"
TABLES_DIR = "/tables/"
DOUBLE_LINE = "\n\n"


def make_filename(
    dir_name: str, num_clauses: int, es_from: int, es_size: int, num_iterations: int, file_extension: str, index: str
) -> str:
    return f"{os.getcwd()}/{dir_name}/{num_clauses}_{es_from}_{es_size}_{num_iterations}_{index}.{file_extension}"


def make_plot(
    data: Tuple[Tuple[int, float]],
    num_clauses: int,
    es_from: int,
    es_size: int,
    num_iterations: int,
    index: str,
    groups: Tuple[str],
    xlabel: str = "Number of Clauses",
    ylabel: str = "Median Query Time (ms)",
    title: str = "Number of Clauses Against Median Time",
) -> None:
    colors = ("green", "blue")

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for data, color, group in zip(data, colors, groups):
        x = [row[0] for row in data]
        y = [row[1] for row in data]
        ax.scatter(x, y, c=color, label=group)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.legend(loc=2)
    plt.savefig(make_filename(PLOT_DIR, num_clauses, es_from, es_size, num_iterations, "png", index))


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


def make_full_url(url: str, index: str) -> str:
    return f"{url}/{index}/_search"
