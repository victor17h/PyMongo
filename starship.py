import pymongo
import requests
import logging

logging.basicConfig(level=logging.DEBUG)

client = pymongo.MongoClient()
db = client.starwars
collection = db.starships
collection.drop()

# Extract data from URL amd append each page to a list (each page is a nested list)
results = []
for page in range(1, 5):
    url = 'https://swapi.dev/api/starships/.json?page=%s' % page
    data = requests.get(url).json()
    # y = db.starships.insert_many(data['results'])
    # print(data)
    results.append(data['results'])

# x = db.starships.find({},{'name':1, 'pilots':1})

# Remove outer list
output = []


def remove_nesting(pilot):
    for i in pilot:
        if type(i) == list:
            remove_nesting(i)
        else:
            output.append(i)


remove_nesting(results)
logging.debug(output)


# Select pilots
pilots = []


def selected_pilots(pilot):
    for i in pilot:
        if 'pilots' in i:
            for j in i['pilots']:
                pilots.append(j)
    #print(pilots)
    return remove_nesting


selected_pilots(output)

# Get pilot API
names = []


def request_pilot(pilot):
    for i in pilot:
        response = requests.get(i).json()
        names.append(response['name'])
    return names


logging.debug(request_pilot(pilots))


# Create list of pilot ids
id_list = []
for i in names:
    # avoid using for loop by finding the cursor object [0][index]
    id_list.append(db.characters.find({'name': i}, {'_id': 1})[0]['_id'])

logging.debug(id_list)

#  Url for ids


def url_id(ids, out):
    for ship in out:
        for pilot in range(len(ship['pilots'])):
            ship['pilots'][pilot] = ids[pilots.index(ship['pilots'][pilot])]
    return out


logging.debug(url_id(id_list, output))

# Insert data in MongoDB


def insert_data(final):
    delete = collection.drop()
    insert = db.starships.insert_many(final)


insert_data(output)
