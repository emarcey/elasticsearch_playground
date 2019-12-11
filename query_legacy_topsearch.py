import requests
import json

from collections import defaultdict

# from stubbed_top_search import TS_SEARCH_TERM_TO_ID_COMPANIES, TOP_SEARCH_RESPONSES
from const import TERRY_TERMS

# from concurrently_process import concurrently_process


def ts_fetch_searchterm_company_results():
    url = "https://app.cbinsights.com/api?url=/search/topsearch"
    headers = {
        "Origin": "https://app.cbinsights.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Referer": "https://app.cbinsights.com/top-search/7vrptx?tab=research",
        "cookie": "_ga=GA1.2.11412028.1554908356; driftt_aid=3023556a-a96e-4c59-9155-0946ec86590f; sliguid=eb4ae9e0-582d-4f95-b9d7-badee4f8e5f2; slirequested=true; _fbp=fb.1.1554908356627.752371478; hubspotutk=1391b12f22f4db751cfe5cb71be706a6; DFTT_END_USER_PREV_BOOTSTRAPPED=true; _pendo_visitorId.cd02c81c-5bd4-4011-5d2d-f1a81b930e1a=12c2b6f92d8f4a60de2ff488aa29e677e768c3539d498172434ced785f732221; driftt_eid=12c2b6f92d8f4a60de2ff488aa29e677e768c3539d498172434ced785f732221; cerosdomaintracking=%257B%2522user_token%2522%253A%252216b091a740118c-05ae1549279fa1-366b7e03-1fa400-16b091a740246f%2522%257D; mkjs_group_id=null; mkjs_user_id=%2212c2b6f92d8f4a60de2ff488aa29e677e768c3539d498172434ced785f732221%22; AUTHDEV=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZFVzZXIiOjIwMzYzNzIsImVtYWlsIjoiamNhcG9iaWFuY29AY2JpbnNpZ2h0cy5jb20iLCJpc0FkbWluIjp0cnVlLCJpZFBhY2thZ2UiOjQyLCJmaXJzdE5hbWUiOiIiLCJsYXN0TmFtZSI6IiIsImV4cCI6MTU3MTg2Mzc1MiwiaXNTd2l0Y2hlZCI6ZmFsc2UsImlzRXh0ZXJuYWxBZG1pbiI6ZmFsc2UsImlhdCI6MTU2NDA4Nzc1Mn0.oDSvHlp63C51kBYQvj9KdRdZLyBUNU44cXRw3RJ86uY; navigation-collapsed-state=false; _gcl_au=1.1.612716408.1567017018; navigation-expanded-map=null; _pendo_accountId.cd02c81c-5bd4-4011-5d2d-f1a81b930e1a=59362; __hssrc=1; AUTHCBI=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZFVzZXIiOjIwMzYzNzIsImVtYWlsIjoiamNhcG9iaWFuY29AY2JpbnNpZ2h0cy5jb20iLCJpc0FkbWluIjp0cnVlLCJpZFBhY2thZ2UiOjU5MzYyLCJmaXJzdE5hbWUiOiJKZWZmcmV5IiwibGFzdE5hbWUiOiJDYXBvYmlhbmNvIiwiZXhwIjoxNTc4ODU1NzY5LCJpc1N3aXRjaGVkIjpmYWxzZSwiaXNFeHRlcm5hbEFkbWluIjpmYWxzZSwiaWF0IjoxNTcxMDc5NzY5fQ.1BIxxM4jgx1hJmA4z26vqeEz3ZoHoDCyFocWf4zPm9M; AUTHSTG=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZFVzZXIiOjM1NDU2ODYsImVtYWlsIjoicG1hbGxlbGEraXNzQGNiaW5zaWdodHMuY29tIiwiaXNBZG1pbiI6ZmFsc2UsImlkUGFja2FnZSI6NjAwNzIsImZpcnN0TmFtZSI6IkNhciIsImxhc3ROYW1lIjoiQnVuIiwiZXhwIjoxNTc5MDEyNjUxLCJpc1N3aXRjaGVkIjpmYWxzZSwiaXNFeHRlcm5hbEFkbWluIjpmYWxzZSwiaWF0IjoxNTcxMjM2NjUxfQ.w5olvUHZ0Ag-VeApFBF6vA0m1WOFxO8mTkwRwy8D8pQ; NODESESSID=s%3AvFPfza33fC6lC3ouO28PuvoqfaIdXuVV.LYNoV%2BTXQEXwISTL7rCV8B38gSac8cuY4TrZ1OrmbJ4; ajs_user_id=%2212c2b6f92d8f4a60de2ff488aa29e677e768c3539d498172434ced785f732221%22; ajs_anonymous_id=%22e333d016-0592-4143-b4e4-b49c709ef6f5%22; ajs_group_id=59362; _gid=GA1.2.1960616067.1571782389; slireg=https://scout.us1.salesloft.com; driftt_sid=6c710729-71ad-4b7a-943f-789686fface1; __hstc=168719870.1391b12f22f4db751cfe5cb71be706a6.1554908356664.1571684185240.1571782390576.85; fs_uid=rs.fullstory.com`KMSM`6259936298827776:5049968864952320`24c2bade`/1599933416; _pendo_meta.cd02c81c-5bd4-4011-5d2d-f1a81b930e1a=952136277; _gat_UA-2917383-11=1; _gat=1; __hssc=168719870.9.1571782390576; __d_hsutk=true",
        "Connection": "keep-alive",
    }
    all_results = defaultdict(list)
    search_term_to_id_companies = defaultdict(list)
    for search_term in TERRY_TERMS:
        query = f'searchTerm:"{search_term}"'
        data = {
            "url": "/search/topsearch",
            "data": {
                "query": query,
                "resultTypes": [{"type": "company", "sortBy": "score", "offset": 0, "limit": 100}],
                "idQuery": "645d6f33-71cf-4725-87af-b21a4bcd024e",
            },
            "method": "POST",
        }

        data_str = json.dumps(data)
        response = requests.post(url=url, headers=headers, data=data_str)
        resp_json = response.json()
        # from IPython import embed
        # embed()
        all_results[search_term].append(resp_json)
        id_companies = [hit["idCompany"] for hit in resp_json["company"]["results"]]
        search_term_to_id_companies[search_term].extend(id_companies)
    return all_results, search_term_to_id_companies


def process_ts_results(search_term_to_resp_json):
    out = defaultdict(list)
    for search_term, resp_jsons in search_term_to_resp_json.items():
        i = 0
        for resp_json in resp_jsons:
            for hit in resp_json["company"]["results"]:
                i += 1
                row = [
                    i,
                    hit.get("score", 0),
                    hit.get("company", ""),
                    hit.get("url", ""),
                    hit.get("description", ""),
                    str(hit.get("matchType", "")),
                ]
                out[search_term].append(row)
    return out


def add_ts_results_to_worksheet(ws, search_term_to_resp_json):
    # resp is already sorted by relevance
    ws.append(["search term", "ranking", "score", "company name", "description", "id_company", "match type"])
    for search_term, resp_jsons in search_term_to_resp_json.items():
        i = 0
        for resp_json in resp_jsons:
            for hit in resp_json["company"]["results"]:
                i += 1
                row = [
                    search_term,
                    i,
                    hit.get("score"),
                    hit.get("company", ""),
                    hit.get("description", ""),
                    hit.get("idCompany", 0),
                    str(hit.get("matchType")),
                ]
                ws.append(row)
