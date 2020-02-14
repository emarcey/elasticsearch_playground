from hashids import Hashids


def get_profile_url(id_company):
    prefix = "https://app.cbinsights.com/profiles/c"
    hashids = Hashids("CBI Profiles")
    suffix = hashids.encode(id_company)
    url = f"{prefix}/{suffix}"
    return url
