from openpyxl import Workbook
from const import (
    ELASTICSEARCH_HOST_URL,
    HEADER,
    TERRY_TERMS,
    IU_QUALITY_MAPPING,
    SAFE_WORDS,
    IU_REVIEWED_TERMS,
    ORG_NAME_SEARCH_TERMS,
    BIG_TESTING_ROUND_SEARCH_TERMS,
)
from get_profile_url import get_profile_url
from current_prd_query import make_current_prd_query
from json import dumps
from requests import post
from datetime import datetime

# from org_old_vs_new import make_new_query
from relevance_experiments import *
from relevance_experiments_tiered_news import *
from collections import defaultdict


def write_results(ws, iss_response, example_query, query_description, sheet_number):
    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["C"].width = 20
    ws.append(["Query Description:", query_description])
    ws.append(["Query JSON:", example_query])
    ws.append([])
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


def write_summary(ws, query_summaries):
    ws.append(
        [
            "Query Number",
            "Number of Good Included",
            "Number of Good Missed",
            "Number of Bad Included",
            "Number of Bad Excluded",
        ]
    )
    for i, summary in query_summaries.items():
        ws.append(
            [str(i), summary["good_included"], summary["good_missed"], summary["bad_included"], summary["bad_excluded"]]
        )


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
    good_included = 0
    bad_included = 0
    all_good = 0
    all_bad = 0
    for search_term, results in search_term_to_results.items():
        id_row = 1
        hit_quality = IU_QUALITY_MAPPING.get(search_term, {})
        all_good += len([k for k, v in IU_QUALITY_MAPPING.get(search_term, {}).items() if v == "good"])
        all_bad += len([k for k, v in IU_QUALITY_MAPPING.get(search_term, {}).items() if v == "bad"])
        if "hits" not in results:
            print(f"ERROR WITH QUERY \n\n{results}\n\n")
            exit(0)
        for row in results["hits"]["hits"]:
            data = row["_source"]
            explain = row["_explanation"]

            description_score, news_score, cxn_name_score, funding_multiplier, num_cxn_multiplier, tier1_news, tier2_news, tier3_news, tier4_news, tier5_news, tier6_news, tier7_news, tier8_news, tier9_news, tier10_news, article_count_multiplier, name_url_score, competitor_score, investor_score = process_explain(
                explain, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            )
            score = row["_score"]
            org_name = data.get("org_name", "")
            quality = hit_quality.get(org_name)
            collections = data.get("expert_collection_names", [])
            profile_url = get_profile_url(data["id_company"])

            if quality == "good":
                good_included += 1
            elif quality == "bad":
                bad_included += 1
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
            out[search_term].append(excel_row)
            id_row += 1

    good_missed = all_good - good_included
    bad_excluded = all_bad - bad_included

    summary_data = {
        "good_included": good_included,
        "good_missed": good_missed,
        "bad_included": bad_included,
        "bad_excluded": bad_excluded,
    }
    return out, summary_data


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

        description_score, news_score, cxn_name_score, funding_multiplier, num_cxn_multiplier, tier1_news, tier2_news, tier3_news, tier4_news, tier5_news, tier6_news, tier7_news, tier8_news, tier9_news, tier10_news, article_count_multiplier, name_url_score, competitor_score, investor_score = process_explain(
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


def main():
    query_builders = [
        (make_current_prd_query, "Current prd query"),
        (
            make_description_tf_idf_tiered_news_tfidf_collection_big_flat_X_sqrt_equity_funding_X_log_num_collections,
            "(0.6 * tiered News tf_idf favoring upper tiers + description tf_idf + expert collection name flat + name or url flat + competitor flat + investor name flat) * ln(2 + total equity funding) * log(2 + number of expert collections)",
        ),
    ]
    search_terms = BIG_TESTING_ROUND_SEARCH_TERMS
    wb = Workbook()
    ws = wb.get_active_sheet()
    i = 1
    query_summaries = {}
    for query_builder, description in query_builders:
        print(f"Running query {description}")
        es_responses = run_search_terms(query_builder, search_terms)
        es_results, summary_data = process_iss_results(es_responses)
        example_query = dumps(query_builder("searchTerm", 0, 100))
        write_results(ws, es_results, example_query, description, i)
        query_summaries[i] = summary_data
        ws = wb.create_sheet()
        i += 1
    ws.title = "Query Summaries"
    write_summary(ws, query_summaries)
    # timestamp = datetime.now().strftime("%Y-%d-%m_%H_%M_%s")
    print("saving excel file")
    # wb.save(f"SearchResults_{timestamp}.xlsx")
    wb.save(f"SearchResults_TESTING_FEB_2020.xlsx")


if __name__ == "__main__":
    main()
