import requests

#List of Concelhos
#Because the API doesn't allow for a large response (is FREE), cannot search for "Portugal", we search by concelho
concelhos = ["Açores","Aveiro","Beja","Braga","Bragança","Castelo Branco","Coimbra","Évora","Faro","Guarda","Leiria","Lisboa","Madeira","Portalegre","Porto","Santarém","Setúbal","Viana do Castelo","Vila Real","Viseu"]

def run():
  for lo in concelhos:
    run_api(lo,True,False)
    run_api(lo,False,True)

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
    resp = requests.post('https://api.apify.com/v2/acts/maxcopell~tripadvisor/run-sync-get-dataset-items?token=8osxgdrLqTCS5ECS444mMjyWv&format=xml&memory=4096', json=parameters)
  else:
    resp = requests.post('https://api.apify.com/v2/acts/maxcopell~tripadvisor/run-sync-get-dataset-items?token=8osxgdrLqTCS5ECS444mMjyWv&format=json&memory=4096', json=parameters)
  #Checks if everything when well with the connection
  if resp.status_code != 200:
    #Saving restaurants
      if restaurants==True:
        name='./Datasets/restaurants_{}.json'.format(location)
      else:
        name='./Datasets/attractions_{}.xml'.format(location)
      with open(name, 'w', encoding='utf-8') as outfile:
        outfile.write(resp.text)
      print('Done {} {}'.format(location, "Restaurants" if restaurants==True else "Attractions"))
  #Connection not established
  else:
    print("Error with connection!")

run()
