from collections import defaultdict
from datetime import datetime
from openpyxl import Workbook
from os import path
from pandas import DataFrame, concat, read_excel
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


from const import RESULTS_SHEET, MASTER_RESULTS_FILE, RNMI_RESULTS_DIR, RNMI_SOURCE_DIR, EXCLUDED_TERMS


TAXONOMY_RESULTS_FILE = "/Users/emarcey/python/elasticsearch_playground/search_relevance_testing.xlsx"


def get_results_files(dirpath: str) -> List[str]:
    return [str(p) for p in sorted(Path(dirpath).iterdir(), key=path.getmtime)]


def _format_id_org(id_org: Any) -> str:
    if id_org == "N/A":
        return "N/A"
    if isinstance(id_org, float):
        return int(id_org)
    return id_org


def make_compound_key(row: Dict[str, Any]) -> str:
    return f"{row['search_term']}||||{_format_id_org(row['id_org'])}"


def split_compound_key(key: str) -> Tuple[str, str]:
    vals = key.split("||||")
    return vals[0], vals[1]


def read_master(filename: str, sheet_name: str, excluded_terms: Set[str]) -> Dict[str, Any]:
    master_results_df = read_excel(filename, sheet_name=sheet_name).dropna(subset=["quality"]).fillna("")

    master_results_dict: Dict[str, Any] = defaultdict(dict)
    for _, row in master_results_df.iterrows():
        if row["search_term"].lower() in excluded_terms:
            continue
        master_results_dict[make_compound_key(row)] = dict(row)

    return master_results_dict


def update_rnmi_results(
    filename: str, sheet_name: str, master_results_dict: Dict[str, Any], excluded_terms: Set[str]
) -> Dict[str, Any]:
    results_sheet = read_excel(filename, sheet_name=sheet_name)

    current_dict = results_sheet[
        [
            "search term",
            "Current id_org",
            "Current match quality",
            "Current Reason Cat",
            "Current Reason",
            "Current org_name",
        ]
    ].rename(
        columns={
            "search term": "search_term",
            "Current id_org": "id_org",
            "Current org_name": "org_name",
            "Current match quality": "match",
            "Current Reason Cat": "Reason Cat",
            "Current Reason": "Reason",
        }
    )
    new_dict = results_sheet[
        ["search term", "New id_org", "New match quality", "New Reason Cat", "New Reason", "New org_name",]
    ].rename(
        columns={
            "search term": "search_term",
            "New id_org": "id_org",
            "New org_name": "org_name",
            "New match quality": "match",
            "New Reason Cat": "Reason Cat",
            "New Reason": "Reason",
        }
    )
    taxonomy_all = concat([current_dict, new_dict]).dropna(subset=["match"]).fillna("")

    for _, row in taxonomy_all.iterrows():
        if not isinstance(row["match"], str):
            continue

        if isinstance(row["id_org"], str):
            continue

        if row["search_term"].lower() in excluded_terms:
            continue

        master_results_dict[make_compound_key(row)] = {
            "search_term": row["search_term"],
            "id_org": _format_id_org(row["id_org"]),
            "org_name": row["org_name"],
            "quality": row["match"].replace("IU", "").strip().upper(),
            "reason_cat": row["Reason Cat"],
            "reason": row["Reason"],
        }

    return master_results_dict


def write_rnmi_results(results_sheet_name: str, results: DataFrame) -> None:
    wb = Workbook()
    ws = wb.get_active_sheet()
    ws.title = results_sheet_name
    ws.append(["search_term", "id_org", "org_name", "quality", "reason_cat", "reason"])

    for row in sorted(results.values(), key=lambda x: (x["search_term"], x["id_org"])):
        ws.append(
            [row["search_term"], row["id_org"], row["org_name"], row["quality"], row["reason_cat"], row["reason"]]
        )

    timestamp = datetime.now().strftime("%Y-%d-%m_%H_%M_%s")
    wb.save(f"{RNMI_RESULTS_DIR}/rnmi_results_{timestamp}.xlsx")


def main():
    results_files = get_results_files(RNMI_SOURCE_DIR)
    master_results_dict = read_master(MASTER_RESULTS_FILE, RESULTS_SHEET, EXCLUDED_TERMS)

    for results_file in results_files:
        print(f"results_file: {results_file}")
        master_results_dict = update_rnmi_results(results_file, RESULTS_SHEET, master_results_dict, EXCLUDED_TERMS)

    write_rnmi_results(RESULTS_SHEET, master_results_dict)


if __name__ == "__main__":
    main()
