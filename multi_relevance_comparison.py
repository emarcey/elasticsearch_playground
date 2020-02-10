from openpyxl import Workbook
from const import ELASTICSEARCH_HOST_URL, HEADER, TERRY_TERMS
from json import dumps
from requests import post
from datetime import datetime

# from org_old_vs_new import make_new_query
from relevance_experiments import *
from relevance_experiments_tiered_news import *
from collections import defaultdict


def write_results(wb, iss_response, example_query, query_description, sheet_number):
    ws = wb.create_sheet()
    ws.append(["Query Description:", query_description])
    ws.append(["Query JSON:", example_query])
    ws.append(
        [
            "search term",
            "ranking",
            "score",
            "Company Name",
            "URL",
            "id_cbi_entity",
            "description",
            "profile views",
            "mosaic_overall",
            "last funding date",
            "news article count",
            "org_total_equity_funding",
            "org_num_fundings",
            "org_num_deals",
            "number of investors",
            "expert collections",
        ]
    )
    ws.title = f"Query {sheet_number}"
    for search_term, new_hits in iss_response.items():
        new_hits = iss_response[search_term]
        for i in range(0, len(new_hits)):
            row = []
            new_hit = [i + 1, "none", "none", "none", "none", "none", "none", "none", "none", "none", "none", "none"]
            if len(new_hits) >= i + 1:
                new_hit = new_hits[i]
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


def run_search_terms(query_builder, search_terms):
    out = {}
    for search_term in search_terms:
        query = query_builder(search_term, 0, 25)
        query_json = dumps(query)
        query_resp = post(f"{ELASTICSEARCH_HOST_URL}/org-read/_search", headers=HEADER, data=query_json)
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
                search_term,
                id_row,
                score,
                data.get("org_name", ""),
                data.get("org_url", ""),
                data.get("id_org", ""),
                data.get("org_description", ""),
                data.get("org_page_views", ""),
                data.get("org_mosaic_overall", ""),
                data.get("org_last_funding_funding_date", ""),
                data.get("org_news_article_count", ""),
                data.get("org_total_equity_funding", ""),
                data.get("org_num_fundings", ""),
                data.get("org_num_deals", ""),
                len(data.get("org_investor", [])),
                str(data.get("expert_collection_names", [])),
            ]
            out[search_term].append(row)
            id_row += 1
    return out


def main():
    query_builders = [
        (make_current_prd_query, "Curent prd query"),
        (make_news_desc_tf_idf_times_equity_funding, "(News tf_idf + description tf_idf) * total equity funding"),
        (
            make_news_desc_tf_idf_times_ln_equity_funding,
            "(News tf_idf + description tf_idf) * ln(total equity funding)",
        ),
        (
            make_news_desc_tf_idf_times_sqrt_equity_funding,
            "(News tf_idf + description tf_idf) * sqrt(total equity funding)",
        ),
        (
            make_news_1_5_x_desc_tf_idf_times_ln_equity_funding,
            "(News tf_idf + (1.5 * description tf_idf)) * ln(total equity funding)",
        ),
        (
            make_news_desc_expert_collection_times_ln_equity_funding,
            "(News tf_idf + description tf_idf + expert collection name tf_idf) * ln(total equity funding)",
        ),
        (
            make_0_5_x_news_desc_expert_collection_times_ln_equity_funding,
            "((0.5 * News tf_idf) + description tf_idf + expert collection name tf_idf) * ln(total equity funding)",
        ),
        (
            make_0_5_x_news_desc_flattened1_expert_collection_times_ln_equity_funding,
            "((0.5 * News tf_idf) + description tf_idf + expert collection name flattened to 1) * ln(total equity funding)",
        ),
        (
            make_0_2_x_news_desc_flattened1_expert_collection_times_ln_equity_funding,
            "((0.2 * News tf_idf) + description tf_idf + expert collection name flattened to 1) * ln(total equity funding)",
        ),
        (
            make_description_tf_idf_news_tfidf_collection_tf_idf_X_ln_equity_funding_X_ln_num_collections,
            "(News tf_idf + description tf_idf + expert collection name tf_idf) * ln(total equity funding) * ln(number of expert collections)",
        ),
        (
            make_description_tf_idf_0_5_x_news_tfidf_collection_tf_idf_X_ln_equity_funding_X_ln_num_collections,
            "((0.5 * News tf_idf) + description tf_idf + expert collection name tf_idf) * ln(total equity funding) * ln(number of expert collections)",
        ),
        (
            make_description_tf_idf_news_tfidf_flattened1_collection_X_ln_equity_funding_X_ln_num_collections,
            "(News tf_idf + description tf_idf + expert collection name lattened to 1) * ln(total equity funding) * ln(number of expert collections)",
        ),
        # TIERED NEWS
        (
            tiered_news_make_news_desc_tf_idf_times_equity_funding,
            "(Tiered News tf_idf + description tf_idf) * total equity funding",
        ),
        (
            tiered_news_make_news_desc_tf_idf_times_ln_equity_funding,
            "(Tiered News tf_idf + description tf_idf) * ln(total equity funding)",
        ),
        (
            tiered_news_make_news_desc_tf_idf_times_sqrt_equity_funding,
            "(Tiered News tf_idf + description tf_idf) * sqrt(total equity funding)",
        ),
        (
            tiered_news_make_news_1_5_x_desc_tf_idf_times_ln_equity_funding,
            "(Tiered News tf_idf + (1.5 * description tf_idf)) * ln(total equity funding)",
        ),
        (
            tiered_news_make_news_desc_expert_collection_times_ln_equity_funding,
            "(Tiered News tf_idf + description tf_idf + expert collection name tf_idf) * ln(total equity funding)",
        ),
        (
            tiered_news_make_0_5_x_news_desc_expert_collection_times_ln_equity_funding,
            "((0.5 * Tiered News tf_idf) + description tf_idf + expert collection name tf_idf) * ln(total equity funding)",
        ),
        (
            tiered_news_make_0_5_x_news_desc_flattened1_expert_collection_times_ln_equity_funding,
            "((0.5 * Tiered News tf_idf) + description tf_idf + expert collection name flattened to 1) * ln(total equity funding)",
        ),
        (
            tiered_news_make_0_2_x_news_desc_flattened1_expert_collection_times_ln_equity_funding,
            "((0.2 * Tiered News tf_idf) + description tf_idf + expert collection name flattened to 1) * ln(total equity funding)",
        ),
        (
            tiered_news_make_description_tf_idf_news_tfidf_collection_tf_idf_X_ln_equity_funding_X_ln_num_collections,
            "(Tiered News tf_idf + description tf_idf + expert collection name tf_idf) * ln(total equity funding) * ln(number of expert collections)",
        ),
        (
            tiered_news_make_description_tf_idf_0_5_x_news_tfidf_collection_tf_idf_X_ln_equity_funding_X_ln_num_collections,
            "((0.5 * Tiered News tf_idf) + description tf_idf + expert collection name tf_idf) * ln(total equity funding) * ln(number of expert collections)",
        ),
        (
            tiered_news_make_description_tf_idf_news_tfidf_flattened1_collection_X_ln_equity_funding_X_ln_num_collections,
            "(Tiered News tf_idf + description tf_idf + expert collection name lattened to 1) * ln(total equity funding) * ln(number of expert collections)",
        ),
    ]
    search_terms = TERRY_TERMS
    wb = Workbook()
    i = 1
    for query_builder, description in query_builders:
        print(f"Running query {description}")
        es_responses = run_search_terms(query_builder, search_terms)
        es_results = process_iss_results(es_responses)
        example_query = dumps(query_builder("searchTerm", 0, 25))
        write_results(wb, es_results, example_query, description, i)
        i += 1
    timestamp = datetime.now().strftime("%Y-%d-%m_%H_%M_%s")
    print("saving excel file")
    wb.save(f"SearchResults_{timestamp}.xlsx")


if __name__ == "__main__":
    main()
