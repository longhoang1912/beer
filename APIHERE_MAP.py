import requests
import json


def get_apikey(file):
    with open(file, "rt") as f:
        api_key = f.read()
    return api_key


def check_beer(file_token, url):
    param = {
        "apiKey": get_apikey(file_token),
        "in": "circle:21.01595,105.82301;r=2000",
        "q": 'beer+bia+bar',
        "limit": 50,
    }
    r = requests.get(url, params=param)
    result = {"type": "FeatureCollection",
              "features": []
              }
    nearbeer = r.json()
    for i in nearbeer["items"]:
        lat = i["position"]["lat"]
        lng = i["position"]["lng"]
        data = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lng, lat]},
            "properties": {"Address": i["address"]["label"],
                           "name": i["title"]},
        }
        result["features"].append(data)
    with open("pymi_beer.geojson", "wt", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    return result


def main():
    file = "token.text"
    url = "https://discover.search.hereapi.com/v1/discover"
    for i in check_beer(file, url)["features"]:
        print(i)
    print('link to my map :'
          'https://github.com/longhoang1912/ex9/blob/map/pymi_beer.geojson')


if __name__ == "__main__":
    main()
