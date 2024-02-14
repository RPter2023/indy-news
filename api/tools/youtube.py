import json
import time
import urllib.parse
from typing import Dict, List, Union

import requests
from pydantic import BaseModel

from lib.cache import sync_threadsafe_ttl_cache as cache


class Video(BaseModel):
    """Video model"""

    id: str
    thumbnails: List[str]
    title: str
    long_desc: Union[str, None]
    channel: str
    duration: Union[str, int]
    views: Union[str, int]
    publish_time: Union[str, int]
    url_suffix: str


def _parse_html(
    html: str, max_results: int
) -> List[Dict[str, Union[str, List[str], int, None]]]:
    results: List[Dict[str, Union[str, List[str], int, None]]] = []
    start = html.index("ytInitialData") + len("ytInitialData") + 3
    end = html.index("};", start) + 1
    json_str = html[start:end]
    data = json.loads(json_str)
    tab = None
    for tab in data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]:
        if "expandableTabRenderer" in tab.keys():
            break
    if tab is None:
        return results
    for contents in tab["expandableTabRenderer"]["content"]["sectionListRenderer"][
        "contents"
    ]:
        for video in contents["itemSectionRenderer"]["contents"]:
            res: Dict[str, Union[str, List[str], int, None]] = {}
            if "videoRenderer" in video.keys() and len(results) < int(max_results):
                video_data = video.get("videoRenderer", {})
                res["id"] = video_data.get("videoId", None)
                res["thumbnails"] = [
                    thumb.get("url", None)
                    for thumb in video_data.get("thumbnail", {}).get("thumbnails", [{}])
                ]
                res["title"] = (
                    video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
                )
                res["long_desc"] = (
                    video_data.get("descriptionSnippet", {})
                    .get("runs", [{}])[0]
                    .get("text", None)
                )
                res["channel"] = (
                    video_data.get("longBylineText", {})
                    .get("runs", [[{}]])[0]
                    .get("text", None)
                )
                res["duration"] = video_data.get("lengthText", {}).get("simpleText", 0)
                res["views"] = video_data.get("viewCountText", {}).get("simpleText", 0)
                res["publish_time"] = video_data.get("publishedTimeText", {}).get(
                    "simpleText", 0
                )
                res["url_suffix"] = (
                    video_data.get("navigationEndpoint", {})
                    .get("commandMetadata", {})
                    .get("webCommandMetadata", {})
                    .get("url", None)
                )
                results.append(res)

        if results:
            return results
    return results


@cache(ttl=3600)
def search_youtube_channel(
    channel_url: str, search_terms: str, period_days: int, max_results: int
) -> List[Dict[str, Union[str, List[str], int, None]]]:
    # calculate day and month from today minus period_days:
    today = time.time()
    period = int(period_days) * 24 * 3600
    start = today - period
    day = time.strftime("%d", time.localtime(start)).zfill(2)
    month = time.strftime("%m", time.localtime(start)).zfill(2)
    year = time.strftime("%Y", time.localtime(start))
    encoded_search = urllib.parse.quote_plus(
        f"{search_terms} after:{year}-{month}-{day}"
    )
    url = f"{channel_url}/search?hl=en&query={encoded_search}"

    html = ""
    nothing = False
    while "ytInitialData" not in html:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to get search results for {search_terms} from {channel_url}")
            nothing = True
            break
        html = response.text
        time.sleep(0.1)
    if nothing:
        return []
    results = _parse_html(html, max_results)
    return results
