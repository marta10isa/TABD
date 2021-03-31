import requests
import json

concelhos = ["Açores","Aveiro","Beja","Braga","Bragança","Castelo Branco","Coimbra","Évora","Faro","Guarda","Leiria","Lisboa","Madeira","Portalegre","Porto","Santarém","Setúbal","Viana do Castelo","Vila Real","Viseu"]

def run():
  for i in concelhos:
    location=i
    restaurants=False
    attractions=False
    hotels=False
    for x in range(1, 3):
      if x==1:
        restaurants=True
      elif x==2:
        attractions=True
      else:
        hotels=True
      run_api(location,restaurants,attractions,hotels)

def run_api(location,restaurants,attractions,hotels):
  parameters  = {
    "locationFullName": location,
    "lastReviewDate": "2019-01-01",
    "includeRestaurants": restaurants,
    "includeAttractions": attractions,
    "includeHotels": hotels,
    "includeReviews": False,
    "proxyConfiguration": {
      "useApifyProxy": True
    }
  }
  resp = requests.post('https://api.apify.com/v2/acts/maxcopell~tripadvisor/run-sync-get-dataset-items?token=CkiNFG32jBkDes2HjAn7NoqEB&format=json&memory=4096', json=parameters)
  if resp.status_code != 200:
    values = json.loads(resp.text)
    if "error" in values:
      print("Error with response:")
      print("Type:" + str(values["error"]["type"]))
      print("Message:" + str(values["error"]["message"]))
    else:
      
      with open(location+'.json', 'w', encoding='utf-8') as f:
        json.dump(resp.json(), f, ensure_ascii=False, indent=4)
      print('Done')
  else:
    print("Error with connection!")

run()