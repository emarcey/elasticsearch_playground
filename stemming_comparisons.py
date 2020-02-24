from datetime import datetime
from hashids import Hashids
import json
from openpyxl import Workbook
import os
import requests
import time
from typing import Any, Callable, Dict, List, Tuple

from const import IU_QUALITY_MAPPING, DIFFERENCES_SEARCH_TERMS
from stemming_search_term_query import make_search_term_body


URL = "http://elasticsearch-prd.cbinsights.com:9200/org-read/_analyze"
HEADERS = {"Content-Type": "application/json"}

LIGHT_ENGLISH_STEMMER = "light_english"
MINIMAL_ENGLISH_STEMMER = "minimal_english"
STEM_DIR = "stemming_results"


def get_profile_url(id_company):
    prefix = "https://app.cbinsights.com/profiles/c"
    hashids = Hashids("CBI Profiles")
    suffix = hashids.encode(id_company)
    url = f"{prefix}/{suffix}"
    return url


def make_search_url(index: str) -> str:
    return f"http://elasticsearch-prd.cbinsights.com:9200/{index}/_search"


def compare_result_ranks(
    phrases: List[str], all_hits_1: List[Dict[str, Any]], name_1: str, all_hits_2: List[Dict[str, Any]], name_2: str
) -> Dict[str, List[Dict[str, Any]]]:

    all_results: Dict[str, List[Dict[str, Any]]] = {}
    all_summaries: Dict[str, Dict[str, Any]] = {}

    for phrase in phrases:

        hits_1 = all_hits_1[phrase]
        hits_2 = all_hits_2[phrase]
        num_hits_1 = len(hits_1)
        num_hits_2 = len(hits_2)

        summary = {
            "num_hits_1": num_hits_1,
            "num_hits_2": num_hits_2,
            "num_same_rank": 0,
            "num_same_orgs": 0,
        }

        hits_2_ranks: Dict[str, int] = {}
        j = 0
        while j < num_hits_2:
            hit_2 = hits_2[j]
            hits_2_ranks[hit_2["_id"]] = j + 1
            j += 1

        min_hits = min(num_hits_1, num_hits_2)
        max_hits = max(num_hits_1, num_hits_2)

        results: List[Dict[str, Any]] = []

        i = 0
        while i < min_hits:
            hit_1 = hits_1[i]
            hit_2 = hits_2[i]

            hits_match = hit_1["_id"] == hit_2["_id"]
            if hits_match:
                summary["num_same_rank"] += 1

            other_rank = hits_2_ranks.get(hit_1["_id"], "N/A")
            if other_rank != "N/A":
                summary["num_same_orgs"] += 1

            results.append(
                {"rank": i + 1, name_1: hit_1, name_2: hit_2, "hits_match": hits_match, f"{name_2} rank": other_rank,}
            )
            i += 1

        if num_hits_1 > min_hits:
            while i < num_hits_1:
                hit_1 = hits_1[i]
                results.append({"rank": i + 1, name_1: hit_1, "hits_match": False, f"{name_2} rank": "N/A"})
                i += 1

        if num_hits_2 > min_hits:
            while i < num_hits_2:
                hit_2 = hits_2[i]
                results.append({"rank": i + 1, name_2: hit_2, "hits_match": False, f"{name_2} rank": "N/A"})
                i += 1

        all_results[phrase] = results

        summary["prop_same_rank"] = "N/A"
        summary["prop_same_orgs"] = "N/A"
        if max_hits > 0:
            summary["prop_same_rank"] = round((summary["num_same_rank"] / max_hits), 2)
            summary["prop_same_orgs"] = round((summary["num_same_orgs"] / max_hits), 2)
        all_summaries[phrase] = summary

    return all_results, all_summaries


def format_ranked_hit(phrase: str, ranked_hit: Dict[str, Any], name_1: str, name_2: str) -> List[str]:
    hit_1 = ranked_hit.get(name_1, {})
    hit_2 = ranked_hit.get(name_2, {})

    hit_1_source = hit_1.get("_source", {})
    hit_2_source = hit_2.get("_source", {})
    return [
        phrase,
        ranked_hit["rank"],
        hit_1.get("_id", "N/A"),
        hit_1_source.get("org_name", "N/A"),
        hit_2.get("_id", "N/A"),
        hit_2_source.get("org_name", "N/A"),
        ranked_hit["hits_match"],
        ranked_hit[f"{name_2} rank"],
    ]


def write_result_ranks(ws, all_results: Dict[str, List[Dict[str, Any]]], name_1: str, name_2: str) -> None:
    ws.append(
        [
            "search term",
            "rank",
            f"{name_1} id_org",
            f"{name_1} org_name",
            f"{name_2} id_org",
            f"{name_2} org_name",
            "hits match",
            f"{name_2} rank",
        ]
    )
    for phrase, results in all_results.items():
        for result in results:
            ws.append(format_ranked_hit(phrase, result, name_1, name_2))


def compare_result_ids(
    phrases: List[str], hits_1: List[Any], hits_2: List[Any]
) -> Dict[str, Tuple[Dict[str, Any], Dict[str, Any]]]:
    results: Dict[str, Tuple[Dict[str, Any], Dict[str, Any]]] = {}
    for phrase in phrases:
        hit_1 = hits_1[phrase]
        hit_2 = hits_2[phrase]
        docs_1 = {hit["_id"]: hit for hit in hit_1}
        docs_2 = {hit["_id"]: hit for hit in hit_2}

        missing_1 = {}
        for idDocument, hit in docs_1.items():
            if idDocument not in docs_2:
                missing_1[idDocument] = hit

        missing_2 = {}
        for idDocument, hit in docs_2.items():
            if idDocument not in docs_1:
                missing_2[idDocument] = hit

        results[phrase] = (missing_1, missing_2)
    return results


def get_hits_from_es(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    return response["hits"]["hits"]


def query_es(index: str, phrases: List[str], size: int) -> Dict[str, List[Dict[str, Any]]]:
    url = make_search_url(index)
    results: Dict[str, List[Dict[str, Any]]] = {}
    print(f"Querying index: {index}")
    for phrase in phrases:
        print(f"\tQuerying phrase: {phrase}")
        request = make_search_term_body(phrase, size)
        resp = requests.post(url=url, data=json.dumps(request), headers=HEADERS)
        if resp.status_code != 200:
            raise Exception(f"Bad response: {resp.json()} {request}")
        results[phrase] = get_hits_from_es(resp.json())

    return results


def write_summary(ws, phrase_summaries, name_1, name_2):
    ws.append(
        [
            "phrase",
            f"{name_1} Num Results",
            f"{name_1} Num Results",
            "Num same rank",
            "Prop Same Rank",
            "Num same orgs",
            "Prop Same Orgs",
        ]
    )

    rows = []
    overall_summary = {"num_hits_1": 0, "num_hits_2": 0, "num_same_rank": 0, "num_same_orgs": 0}
    for phrase, summary in phrase_summaries.items():
        rows.append(
            [
                phrase,
                summary["num_hits_1"],
                summary["num_hits_2"],
                summary["num_same_rank"],
                summary["prop_same_rank"],
                summary["num_same_orgs"],
                summary["prop_same_orgs"],
            ]
        )
        overall_summary["num_hits_1"] += summary["num_hits_1"]
        overall_summary["num_hits_2"] += summary["num_hits_2"]
        overall_summary["num_same_rank"] += summary["num_same_rank"]
        overall_summary["num_same_orgs"] += summary["num_same_orgs"]

    overall_summary["prop_same_rank"] = round((overall_summary["num_same_rank"] / overall_summary["num_hits_1"]), 2)
    overall_summary["prop_same_orgs"] = round((overall_summary["num_same_orgs"] / overall_summary["num_hits_1"]), 2)

    ws.append(
        [
            "Overall",
            overall_summary["num_hits_1"],
            overall_summary["num_hits_2"],
            overall_summary["num_same_rank"],
            overall_summary["prop_same_rank"],
            overall_summary["num_same_orgs"],
            overall_summary["prop_same_orgs"],
        ]
    )
    for row in rows:
        ws.append(row)


def build_explain(ws, results: Dict[str, List[Dict[str, Any]]]) -> None:
    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["C"].width = 20

    ws.append(
        [
            "search term",
            "ranking",
            "Company Name",
            "description",
            "company url",
            "profile url",
            "IU Quality",
            "score",
            "description_score",
            "news_score",
            "cxn_name_score",
            "funding_multiplier",
            "num_cxn_multiplier",
            "name/url score",
            "competitor score",
            "investor score",
            "expert collections",
            "number of expert collections",
            "org_total_equity_funding",
            "tier1_news_score",
            "tier2_news_score",
            "tier3_news_score",
            "tier4_news_score",
            "tier5_news_score",
            "tier6_news_score",
            "tier7_news_score",
            "tier8_news_score",
            "tier9_news_score",
            "tier10_news_score",
            "article_count_multiplier",
            "id_cbi_entity",
            "profile views",
            "mosaic_overall",
            "last funding date",
            "news article count",
            "org_num_fundings",
            "org_num_deals",
            "number of investors",
        ]
    )

    for search_term, result in results.items():
        id_row = 1
        for hit in result:
            explain = hit["_explanation"]
            data = hit["_source"]

            hit_quality = IU_QUALITY_MAPPING.get(search_term, {})

            (
                description_score,
                news_score,
                cxn_name_score,
                funding_multiplier,
                num_cxn_multiplier,
                tier1_news,
                tier2_news,
                tier3_news,
                tier4_news,
                tier5_news,
                tier6_news,
                tier7_news,
                tier8_news,
                tier9_news,
                tier10_news,
                article_count_multiplier,
                name_url_score,
                competitor_score,
                investor_score,
            ) = process_explain(explain, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

            score = hit["_score"]
            org_name = data.get("org_name", "")
            collections = data.get("expert_collection_names", [])
            profile_url = get_profile_url(data["id_company"])
            quality = hit_quality.get(org_name)

            excel_row = [
                search_term,
                id_row,
                org_name,
                data.get("org_description", ""),
                data.get("org_url", ""),
                profile_url,
                quality,
                score,
                description_score,
                news_score,
                cxn_name_score,
                funding_multiplier,
                num_cxn_multiplier,
                name_url_score,
                competitor_score,
                investor_score,
                str(collections),
                len(collections),
                data.get("org_total_equity_funding", ""),
                tier1_news,
                tier2_news,
                tier3_news,
                tier4_news,
                tier5_news,
                tier6_news,
                tier7_news,
                tier8_news,
                tier9_news,
                tier10_news,
                article_count_multiplier,
                data.get("id_org", ""),
                data.get("org_page_views", ""),
                data.get("org_mosaic_overall", ""),
                data.get("org_last_funding_funding_date", ""),
                data.get("org_news_article_count", ""),
                data.get("org_num_fundings", ""),
                data.get("org_num_deals", ""),
                len(data.get("org_investor", [])),
            ]
            ws.append(excel_row)
            id_row += 1


def process_explain(
    explain,
    description_score,
    news_score,
    cxn_name_score,
    funding_multiplier,
    num_cxn_multiplier,
    tier1_news,
    tier2_news,
    tier3_news,
    tier4_news,
    tier5_news,
    tier6_news,
    tier7_news,
    tier8_news,
    tier9_news,
    tier10_news,
    article_count_multiplier,
    name_url_score,
    competitor_score,
    investor_score,
):
    details = explain.get("details", [])
    for detail in details:
        description = detail["description"]
        if "weight(search_term_org_description_no_exit" in description:
            description_score = detail["value"]

        # Note: this will break if you use other dis_max queries besides for news
        elif "weight(all_org_news_noun_phrases_no_exit" in description or description == "max of:":
            news_score = detail["value"]

        elif "weight(expert_collection_names" in description or "ConstantScore(expert_collection_names" in description:
            cxn_name_score = detail["value"]

        elif "field value function" in description and "org_total_equity_funding" in description:
            funding_multiplier = detail["value"]

        elif "field value function" in description and "num_expert_collections" in description:
            num_cxn_multiplier = detail["value"]
        elif "org_news_noun_phrases_tier_one_no_exit" in description:
            tier1_news = detail["value"]
        elif "org_news_noun_phrases_tier_two_no_exit" in description:
            tier2_news = detail["value"]
        elif "org_news_noun_phrases_tier_three_no_exit" in description:
            tier3_news = detail["value"]
        elif "org_news_noun_phrases_tier_four_no_exit" in description:
            tier4_news = detail["value"]
        elif "org_news_noun_phrases_tier_five_no_exit" in description:
            tier5_news = detail["value"]
        elif "org_news_noun_phrases_tier_six_no_exit" in description:
            tier6_news = detail["value"]
        elif "org_news_noun_phrases_tier_seven_no_exit" in description:
            tier7_news = detail["value"]
        elif "org_news_noun_phrases_tier_eight_no_exit" in description:
            tier8_news = detail["value"]
        elif "org_news_noun_phrases_tier_nine_no_exit" in description:
            tier9_news = detail["value"]
        elif "org_news_noun_phrases_tier_ten_no_exit" in description:
            tier10_news = detail["value"]
        elif "field value function: log(doc['org_news_article_count']" in description:
            article_count_multiplier = detail["value"]
        elif "ConstantScore(search_term_org_name_no_exits" in description:
            name_url_score = detail["value"]
        elif "ConstantScore(search_term_org_investor_name_no_exits" in description:
            investor_score = detail["value"]
        elif "ConstantScore(search_term_org_competitor_no_exits" in description:
            competitor_score = detail["value"]

        (
            description_score,
            news_score,
            cxn_name_score,
            funding_multiplier,
            num_cxn_multiplier,
            tier1_news,
            tier2_news,
            tier3_news,
            tier4_news,
            tier5_news,
            tier6_news,
            tier7_news,
            tier8_news,
            tier9_news,
            tier10_news,
            article_count_multiplier,
            name_url_score,
            competitor_score,
            investor_score,
        ) = process_explain(
            detail,
            description_score,
            news_score,
            cxn_name_score,
            funding_multiplier,
            num_cxn_multiplier,
            tier1_news,
            tier2_news,
            tier3_news,
            tier4_news,
            tier5_news,
            tier6_news,
            tier7_news,
            tier8_news,
            tier9_news,
            tier10_news,
            article_count_multiplier,
            name_url_score,
            competitor_score,
            investor_score,
        )
    return (
        description_score,
        news_score,
        cxn_name_score,
        funding_multiplier,
        num_cxn_multiplier,
        tier1_news,
        tier2_news,
        tier3_news,
        tier4_news,
        tier5_news,
        tier6_news,
        tier7_news,
        tier8_news,
        tier9_news,
        tier10_news,
        article_count_multiplier,
        name_url_score,
        competitor_score,
        investor_score,
    )


def main() -> None:
    search_terms = DIFFERENCES_SEARCH_TERMS[:3]
    old_index = "org-read"
    new_index = "org-23"
    size = 25

    output = []

    wb = Workbook()
    ws = wb.get_active_sheet()

    old_results = query_es(old_index, search_terms, size)
    new_results = query_es(new_index, search_terms, size)

    result_ranks, result_summaries = compare_result_ranks(
        search_terms, old_results, LIGHT_ENGLISH_STEMMER, new_results, MINIMAL_ENGLISH_STEMMER
    )
    ws.title = "summaries"
    write_summary(ws, result_summaries, LIGHT_ENGLISH_STEMMER, MINIMAL_ENGLISH_STEMMER)

    ws = wb.create_sheet()
    ws.title = "result_ranks"
    write_result_ranks(ws, result_ranks, LIGHT_ENGLISH_STEMMER, MINIMAL_ENGLISH_STEMMER)

    ws = wb.create_sheet()
    ws.title = f"{LIGHT_ENGLISH_STEMMER} explain"
    build_explain(ws, old_results)

    ws = wb.create_sheet()
    ws.title = f"{MINIMAL_ENGLISH_STEMMER} explain"
    build_explain(ws, new_results)

    timestamp = datetime.now().strftime("%Y-%d-%m_%H_%M_%s")
    wb.save(f"{STEM_DIR}/SearchResults_{timestamp}.xlsx")


if __name__ == "__main__":
    main()
