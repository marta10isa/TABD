import requests
import json
import xml.etree.ElementTree as ET

#List of Concelhos
#Because the API doesn't allow for a large response (is FREE), cannot search for "Portugal", we search by concelho
concelhos = ["Açores","Aveiro","Beja","Braga","Bragança","Castelo Branco","Coimbra","Évora","Faro","Guarda","Leiria","Lisboa","Madeira","Portalegre","Porto","Santarém","Setúbal","Viana do Castelo","Vila Real","Viseu"]

def run():
  for lo in concelhos:
    #for x in range(1, 2):
      #if x==1:
    run_api(lo,True,False)
      #else:
        #run_api(lo,False,True)
      #run_api(location,restaurants,attractions)

def run_api(location,restaurants,attractions):
  #Builds the parameters to go with the API
  parameters  = {
    "locationFullName": location,
    "lastReviewDate": "2019-01-01",
    "includeRestaurants": restaurants,
    "includeAttractions": attractions,
    "includeHotels": False,
    "includeReviews": False,
    "proxyConfiguration": {
      "useApifyProxy": True
    }
  }
  #Format of the response is different (restaurants: the response is in JSON; attractions: the response is in XML)
  if attractions==True:
    resp = requests.post('https://api.apify.com/v2/acts/maxcopell~tripadvisor/run-sync-get-dataset-items?token=CkiNFG32jBkDes2HjAn7NoqEB&format=xml&memory=4096', json=parameters)
  else:
    resp = requests.post('https://api.apify.com/v2/acts/maxcopell~tripadvisor/run-sync-get-dataset-items?token=CkiNFG32jBkDes2HjAn7NoqEB&format=json&memory=4096', json=parameters)
  #Checks if everything when well with the connection
  if resp.status_code != 200:
    values = json.loads(resp.text)
    #If an error has occorred
    if "error" in values:
      print("Error with response:")
      print("Type:" + str(values["error"]["type"]))
      print("Message:" + str(values["error"]["message"]))
    #Everything when well, so we save the response in a file
    else:
      #Saving restaurants
      if restaurants==True:
        with open('./Datasets/restaurants.json') as f:
          data = json.load(f)
        data.update(resp.json())
        with open('./Datasets/restaurants.json', 'w', encoding='utf-8') as f:
            json.dump(data.json(), f, ensure_ascii=False, indent=4)
        print('Done ' + location + "restaurants")
      #Saving Attractions
      else:
        tree = ET.parse(resp.text)
        root = tree.getroot()
        with open('./Datasets/attractions.xml', 'w') as f:
          f.write(resp.text)
        print('Done ' + location + "attractions")
  #Connection not established
  else:
    print("Error with connection!")



#with open('./Datasets/test.json', 'w', encoding='utf-8') as f:
#        json.dump(resp.json(), f, ensure_ascii=False, indent=4)

run()