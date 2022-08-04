def petsearch(text):
    import re

    petr = re.compile(r"(?i)\s(?:(?:pets?)|(animals?))\s")
    res = re.search(petr, text)
    if res:
        phrase = text[
            res.start()
            - min(res.start(), 10) : res.end()  # noqa: E203
            + min((len(text) - res.end()), 10)
        ]
        print(phrase)
        phrase = phrase.split(" ")
        for i in phrase:
            if i.lower() in ["no", "not"]:
                return False
        return True
    else:
        return None


def cleanhtml(raw_html):
    import html
    import unicodedata

    cleantext = html.unescape(raw_html)
    # cleanr = re.compile('<.*?>')
    # cleantext = re.sub(cleanr, '\n', cleantext)
    cleantext = unicodedata.normalize("NFKD", cleantext)
    return cleantext


def get_property(id):
    import json
    import requests

    r = requests.get(
        "http://api.rightmove.co.uk/api/propertyDetails?apiApplication=IPAD&propertyId={}".format(
            id
        )
    )
    data = json.loads(r.text)
    data = data["property"]
    prop = {
        "id": id,
        "price": data["price"],
        "bedrooms": data["bedrooms"],
        "address": data["address"],
        "propertyType": data["propertyType"],
        "letFurnishType": data["letFurnishType"],
        "url": data["publicsiteUrl"],
        "fullDescription": data["fullDescription"],
        "longitude": data["longitude"],
        "latitude": data["latitude"],
    }
    prop["floorplans"] = [x["url"] for x in data["floorplans"]]
    prop["photos"] = [x["url"] for x in data["photos"]]
    prop["features"] = [x["featureDescription"].strip() for x in data["features"]]
    return prop
