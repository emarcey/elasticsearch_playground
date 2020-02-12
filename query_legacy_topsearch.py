import requests
import json

from collections import defaultdict

# from stubbed_top_search import TS_SEARCH_TERM_TO_ID_COMPANIES, TOP_SEARCH_RESPONSES

# from concurrently_process import concurrently_process


def ts_fetch_searchterm_company_results(search_terms):
    url = "https://app.cbinsights.com/api?url=/search/topsearch"
    headers = {
        "Origin": "https://app.cbinsights.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Referer": "https://app.cbinsights.com/top-search/7vrptx?tab=research",
        "cookie": "_ga=GA1.2.784682544.1578415816; _gcl_au=1.1.161130111.1578415816; ajs_anonymous_id=%2254387e42-b178-4c5e-8a64-f44d2780f238%22; driftt_aid=a1bd346f-dd8c-4b7e-8ef1-0340e323f8eb; mkjs_group_id=null; sliguid=c53b4489-7094-4901-9771-6b2678ff22b5; slirequested=true; _fbp=fb.1.1578415817284.1406166665; hubspotutk=91d1c8cc283d860fa900cc47daf40974; __hssrc=1; DFTT_END_USER_PREV_BOOTSTRAPPED=true; AUTHSTG=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZFVzZXIiOjIwNzEyNjksImVtYWlsIjoiamNhcG9iaWFuY29AY2JpbnNpZ2h0cy5jb20iLCJpc0FkbWluIjp0cnVlLCJpZFBhY2thZ2UiOjQyLCJmaXJzdE5hbWUiOiJKZWZmIiwibGFzdE5hbWUiOiJDYXBvYmlhbmNvIiwiZXhwIjoxNTg2MTkxODI0LCJpc1N3aXRjaGVkIjpmYWxzZSwiaXNFeHRlcm5hbEFkbWluIjpmYWxzZSwiaWF0IjoxNTc4NDE1ODI0fQ.8aTiLSGvs1Nm6IcnCSxeH5rFN-8yobxxXXCsVcA0l3E; navigation-expanded-map=null; navigation-collapsed-state=false; ajs_user_id=%2212c2b6f92d8f4a60de2ff488aa29e677e768c3539d498172434ced785f732221%22; AUTHCBI=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZFVzZXIiOjIwMzYzNzIsImVtYWlsIjoiamNhcG9iaWFuY29AY2JpbnNpZ2h0cy5jb20iLCJpc0FkbWluIjp0cnVlLCJpZFBhY2thZ2UiOjQyLCJmaXJzdE5hbWUiOiJKZWZmcmV5IiwibGFzdE5hbWUiOiJDYXBvYmlhbmNvIiwiZXhwIjoxNTg2Mjk4ODY0LCJpc1N3aXRjaGVkIjpmYWxzZSwiaXNFeHRlcm5hbEFkbWluIjpmYWxzZSwiaWF0IjoxNTc4NTIyODY0fQ.z3Bt7zrIJ-EWdkj8pupRK4xnDXSs_Nm4ORfeZ0g0qIE; mkjs_user_id=%2212c2b6f92d8f4a60de2ff488aa29e677e768c3539d498172434ced785f732221%22; driftt_eid=12c2b6f92d8f4a60de2ff488aa29e677e768c3539d498172434ced785f732221; _gaexp=GAX1.2.h71OMAQBQGSys-y4j6qpdQ.18375.1; experimentation_subject_id=Ijk0NzZmNzEyLWRhNzAtNGVhZi05MGYxLTI5OWFjZGUwNGJhZSI%3D--7910e86ee2972eb4fb87103e502485678abab5cf; AUTHDEV=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZFVzZXIiOjIwMzYzNzIsImVtYWlsIjoiamNhcG9iaWFuY29AY2JpbnNpZ2h0cy5jb20iLCJpc0FkbWluIjp0cnVlLCJpZFBhY2thZ2UiOjQyLCJmaXJzdE5hbWUiOiJqZWZmcmV5IiwibGFzdE5hbWUiOiJjYXBvaWJhbmNvIiwiZXhwIjoxNTg4MTczMDQ2LCJpc1N3aXRjaGVkIjpmYWxzZSwiaXNFeHRlcm5hbEFkbWluIjpmYWxzZSwiaWF0IjoxNTgwMzk3MDQ2fQ.d_KDDnhMjbIHvE5p0lBTKwDBmyy17SlVC3tHzhK_Q2o; ajs_group_id=59362; NODESESSID=s%3AxA43H3uVejIqcdtImhyZWRBfQiXC9BZ2.weu5DQvthApA3G%2FsrwgikjC%2Byem5Wy1tm3K3e6uxy1k; _gid=GA1.2.1009307090.1581363468; slireg=https://scout.us1.salesloft.com; _gat_UA-2917383-11=1; _gat=1; fs_uid=rs.fullstory.com#KMSM#6156432085188608:6294329208569856#24c2bade#/1610058865; driftt_sid=75365e20-ddda-4b39-9796-03db3e42cd34; __hstc=168719870.91d1c8cc283d860fa900cc47daf40974.1578415817327.1581365627786.1581434324958.34; __hssc=168719870.1.1581434324958; __d_hsutk=true",
        "Connection": "keep-alive",
    }
    all_results = defaultdict(list)
    search_term_to_id_companies = defaultdict(list)
    for search_term in search_terms:
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
