from datetime import datetime
from openpyxl import Workbook
from query_legacy_topsearch import ts_fetch_searchterm_company_results, process_ts_results
from const import ELASTICSEARCH_HOST_URL, HEADER, TERRY_TERMS
from json import dumps
from requests import post
from org_old_vs_new import make_new_query
from collections import defaultdict


def write_results(iss_response, old_search_response):
    wb = Workbook()
    ws = wb.get_active_sheet()
    for search_term, old_hits in old_search_response.items():
        ws.title = search_term
        ws.append([f"search term: {search_term}"])
        ws.append(
            [
                "legacy",
                "legacy",
                "legacy",
                "legacy",
                "legacy",
                "legacy",
                "new",
                "new",
                "new",
                "new",
                "new",
                "new",
                "new",
                "new",
                "new",
                "new",
                "new",
                "new",
                "new",
            ]
        )
        ws.append(
            [
                "ranking",
                "score",
                "Company Name",
                "URL",
                "description",
                "match type",
                "ranking",
                "score",
                "Company Name",
                "URL",
                "description",
                "profile views",
                "mosaic_market",
                "mosaic_momentum",
                "mosaic_money",
                "mosaic_overall",
                "last funding date",
                "news article count",
                "noun phrases",
            ]
        )
        new_hits = iss_response[search_term]
        for i in range(0, 100):
            row = []
            old_hit = [i + 1, "none", "none", "none", "none", "none"]
            new_hit = [
                i + 1,
                "none",
                "none",
                "none",
                "none",
                "none",
                "none",
                "none",
                "none",
                "none",
                "none",
                "none",
                "none",
            ]
            if len(old_hits) >= i + 1:
                old_hit = old_hits[i]
            if len(new_hits) >= i + 1:
                new_hit = new_hits[i]
            row.extend(old_hit)
            row.extend(new_hit)
            try:
                ws.append(row)
            except Exception:
                new_row = []
                for s in row:
                    if isinstance(s, str):
                        new_row.append(s.encode("unicode_escape").decode("utf-8"))
                    else:
                        new_row.append(s)
                ws.append(new_row)
        ws = wb.create_sheet()
    timestamp = datetime.now().strftime("%Y-%d-%m_%H_%M_%s")
    print("saving excel file")
    wb.save(f"SearchResults_{timestamp}.xlsx")


def run_search_terms(query_builder, search_terms):
    out = {}
    for search_term in search_terms:
        query = query_builder(search_term, 0, 100)
        query_resp = post(f"{ELASTICSEARCH_HOST_URL}/org-write/_search", headers=HEADER, data=dumps(query))
        out[search_term] = query_resp.json()
    return out


def process_iss_results(search_term_to_results):
    out = defaultdict(list)
    # print("search_term_to_results", search_term_to_results)
    for search_term, results in search_term_to_results.items():
        id_row = 1
        for row in results["hits"]["hits"]:
            data = row["_source"]
            score = row["_score"]
            row = [
                id_row,
                score,
                data.get("org_name", ""),
                data.get("org_url", ""),
                data.get("org_description", ""),
                data.get("org_page_views", ""),
                data.get("org_mosaic_market", ""),
                data.get("org_mosaic_momentum", ""),
                data.get("org_mosaic_money", ""),
                data.get("org_mosaic_overall", ""),
                data.get("org_last_funding_funding_date", ""),
                data.get("org_news_article_count", ""),
                str(data.get("all_org_news_noun_phrases", "")),
            ]
            out[search_term].append(row)
            id_row += 1
    return out


def main():
    top_search_responses, _ = ts_fetch_searchterm_company_results()
    ts_results = process_ts_results(top_search_responses)
    es_responses = run_search_terms(make_new_query, TERRY_TERMS)
    es_results = process_iss_results(es_responses)
    write_results(es_results, ts_results)


if __name__ == "__main__":
    main()
