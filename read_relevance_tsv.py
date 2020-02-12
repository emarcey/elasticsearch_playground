import csv
from collections import defaultdict


def read_tsv():
    hit_quality = defaultdict(dict)
    # {"search_term": [{"company name": "good"}, {"company name": "bad"}]}
    search_term_col = 2
    company_col = 6
    quality_col = 1
    with open("IU_review_summary.tsv") as tsvfile:
        reader = csv.reader(tsvfile, delimiter="\t")
        for row in reader:
            search_term = row[search_term_col]
            if search_term == "Search Term":
                continue
            company_name = row[company_col]
            quality = row[quality_col]
            hit_quality[search_term][company_name] = quality
    print(hit_quality)
    return hit_quality


if __name__ == "__main__":
    read_tsv()
