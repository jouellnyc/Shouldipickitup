#!/home/john/anaconda3/bin/python3.7

''' Build and load zip code data into a file or memcached and              '''
''' make available functions to return that data                           '''

''' Specifically this module only cares about zipcode to citytext:         '''
'''        '32546' => 'gainesville,FL'                                     '''
'''                                                                        '''
'''        At the moment the free zip code file has about 40k entries      '''
'''        i.e '86301'->'86305', but not '86306', so we ravage that file   '''
'''        to find the closest city given a zip and store that in          '''
'''        memcached. Note that its the closest as per the govt file       '''
'''        so may return no data. It's not the closest Craigslist          '''
'''        city/link. (Yet)                                                '''
''' NOTE:                                                                  '''
''' cities will be loaded lowercase into the local file and Memcached      '''
''' STATES will be UPPER in both                                           '''

import os
import re
import csv
import sys

import json
from pymemcache.client import base
from pymongo import MongoClient

URL = 'http://federalgovernmentzipcodes.us/download.html' # not used
my_file_name = os.path.basename(__file__)
zip_code_file = '/home/john/gitrepos/shouldipickitup/data/free-zipcode-database-Primary.no.header.csv'

def create_zips_city_state_dict_from_file(zip_code_file):
    ''' Return a dictionary with zip : (city,state) tuples  '''
    ''' give the file at URL                                '''
    print('create1')
    with open(zip_code_file) as csv_fh:
            myzips = {}
            csv_reader = csv.reader(csv_fh, delimiter=',')

            for row in csv_reader:
                zip   = row[0]
                city  = row[2]
                city  = city.lower()
                city  = "".join(city.split()) # no spaces
                state = row[3]
                state = state.upper()
                myzips[zip] = (city,state)

    return myzips

def generate_all_possible_closest_zips():
    closest_city_state = {}
    print('genall2')
    for zip in ("%.5d" % x for x in range(99999)):
        print(f"{zip}:", end='')
        city, state       = lookup_city_state_given_zip_file(zip,myzips)
        closest_city_state[zip] = (city,state)
    return closest_city_state

def generate_all_possible_closest_zips_mongodb():
    closest_city_state = []
    print('genall3')
    for zip in ("%.5d" % x for x in range(9)):
        city, state       = lookup_city_state_given_zip_file(zip,myzips)
        citytext          = f"{city},{state}"
        url =  craigzipsandurls.lookup_craigs_url_from_dict_file(citytext,web_links)
        x = {'zip': zip, 'Details': {'City': city, 'State': state},
        'craigs_local_url' : url}
        print(x)
        closest_city_state.append(x)
    return closest_city_state

def lookup_city_state_given_zip_file(zip, zip_code_dict):
    ''' Given a zipcode;  return closest city,state zipcode dictionary file '''
    closest = zip_code_dict[min(myzips.keys(), key=lambda k: abs(int(k)-int(zip)))]
    city, state = closest
    return (city,state)

def lookup_city_state_given_zip_memcached(zip):
    ''' Given a zipcode and the zipcode dictionary return closest city,state '''
    ''' as a tuple. If no hit, find the closest and cache that in memcached  '''
    #if memcached is down ConnectionRefusedError is returned
    client      =  base.Client(('localhost', 11211))
    data        = client.get(zip)

    if data is None:
        raise ValueError('No data')
    else:
        city, state = data.decode("utf-8").split(',')
        patt  = re.compile('\w+')
        city  = patt.search(city).group()
        state = patt.search(state).group()
        return (city,state)

def load_zips_to_memcached(zipcode_dict):
    ''' write all the key/values to memcached '''
    print('load3')
    client = base.Client(('localhost', 11211))
    for zip,(city,state) in zipcode_dict.items():
        client.set(zip,(city,state))

def load_zips_to_mongodb(closest_list):
    ''' write all the key/values to mongodb '''
    client = MongoClient()
    db = client.posts
    posts = db.posts
    print('load4')
    #for x in closest_list:
    #    print(x.rstrip(','))
    #    result = posts.insert_one(x.rstrip(','))
    new_result = posts.insert_many(closest_list)
    print('Multiple posts: {0}'.format(new_result.inserted_ids))
    #print(result.inserted_id)

if __name__ == "__main__":

    import sys
    import app_logger
    import craigzipsandurls

    try:
        zip = sys.argv[1]
        if sys.argv[1] == 'load':
            print('Please wait')
            #zip = sys.argv[2]
            myzips              = create_zips_city_state_dict_from_file(zip_code_file)
            web_links = craigzipsandurls.create_craigs_url_dict_from_disk()
            #closest_city_states = generate_all_possible_closest_zips()
            closest_city_states  = generate_all_possible_closest_zips_mongodb()
            load_zips_to_mongodb(closest_city_states)
            #print(lookup_city_state_given_zip_file(zip, myzips))
            #load_zips_to_memcached(closest_city_states)
            #print(lookup_city_state_given_zip_memcached(zip))
        else:
            try:
                zip = sys.argv[1]
                city,state = lookup_city_state_given_zip_memcached(zip)
                print(city,state)
            except Exception as e: #Catches ConnectionRefusedError
                print("Memcached seems down; going to file:",e)
                try:
                    city, state = lookup_city_state_given_zip_file(zip, zip_code_file)
                    city, state = city.lower(),state.lower()
                    print(city,state)
                except OSError as e:
                    print("OSError",e)
    except OSError as e:
        print("OSError",e)
    except IndexError as e:
        print("Did you specify a zip?")
