import requests
from parsing import fetch_post_id_and_site_from_url, url_to_shortlink
import HTMLParser


class PostData:
    def __init__(self):
        self.post_id = None
        self.post_url = None
        self.post_type = None
        self.site = None
        self.owner_url = None
        self.owner_name = None
        self.title = None


def api_get_post(post_url):
    d = fetch_post_id_and_site_from_url(post_url)
    if d is None:
        return None
    post_id, site, post_type = d
    if post_type == "answer":
        api_filter = "!1zSl_EE)(nuF4Xn(2sDLC"
        req_url = "http://api.stackexchange.com/2.2/answers/" + post_id +\
                  "?site=" + site + "&filter=" + api_filter +\
                  "&key=IAkbitmze4B8KpacUfLqkw(("
        resp_json = requests.get(req_url).json()
    else:
        assert post_type == "question"

        api_filter = "!gB6tXYzgnc3pG)x0n*03eR9*kZWXReH54Qb"
        req_url = "http://api.stackexchange.com/2.2/questions/" + post_id +\
            "?site=" + site + "&filter=" + api_filter +\
            "&key=IAkbitmze4B8KpacUfLqkw(("
        resp_json = requests.get(req_url).json()
    if 'items' not in resp_json or len(resp_json['items']) == 0:
        return False
    item = resp_json['items'][0]
    post_data = PostData()
    post_data.post_id = post_id
    post_data.post_url = url_to_shortlink(item['link'])
    post_data.post_type = post_type
    h = HTMLParser.HTMLParser()
    post_data.title = h.unescape(item['title'])
    if 'owner' in item and 'owner' is not None:
        post_data.owner_name = item['owner']['display_name']
        post_data.owner_url = item['owner']['link']
    post_data.site = site
    return post_data
