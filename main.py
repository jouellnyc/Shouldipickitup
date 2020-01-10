#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

main.py - interface into flask and mongodb.
- This script takes in a zip code from Flask/app.py or via cmd line, and then
determines the right Craiglist URL by qurying 'Zips' or 'AltZips' in MongoDB.
It then returns the free items (see below) associated with that MongoDB doc.

- If there is no data for the zip entered, S.F data will be returned
- If MongoDB is down S.F data will be returned (if data was crawled and loaded)

-This script requires the mongodb helper module.

-This file can also be imported as a module and contains the following
functions:

    * main - the main function of the script

TBD: Input validation.
"""

import logging

import pymongo
from pymongo.errors import ConnectionFailure

from lib import mongodb
from lib import pickleme

=======
from pymongo.errors import ServerSelectionTimeoutError

def main(zip):
    """
    Send data to flask template for display after querying MongoDB.

    Parameters
    ----------
    zip : str
        zip code the user entered - inbound from Flask or from cmd line.

    Returns
    -------
    all_posts
        A [list] of all the local posts in the free sections
    all_links
        A [list] of all the local posts in the free sections
    city
        [str] - the city associated with the zip (for display only)
    state
        [str] - the state associated with the zip (for display only)

    start_lat
    start_lng    to be used to calculate distance (disabled for now)

    """
    start_lat = "40.6490763"
    start_lng = "-73.9762069"

    start_lat = "29.5964"
    start_lng = "-82.2178"

    fall_back_url = "https://sfbay.craigslist.org/d/free-stuff/search/zip"

    try:

        raise IOError
        """ Given a zip, find the Craigslist Url """
        city, state, url, Items, Urls = \
            mongodb.lookup_craigs_url_citystate_and_items_given_zip(zip)
        city, state = city.capitalize(), state.upper()
        all_posts = Items.values()
        all_links = Urls.values()
        all_links = enumerate(all_links, start = 1)
        return all_posts, all_links, city, state

<<<<<<< HEAD
    except (ConnectionFailure, ValueError, KeyError) as e:

        #TBD - log error to log - we handled it - move on
=======
    except (ValueError, ConnectionRefusedError, KeyError, ServerSelectionTimeoutError) as e:

        craigs_list_url = "https://sfbay.craigslist.org"
>>>>>>> 6f6d65e63798a527865dd61ca3ebc88a693630db
        city, state = (
            (f"Sorry didn't find data for {zip}, here's items for " f"San Francisco "),
            "CA",
        )

<<<<<<< HEAD
        try:
            pickled   = pickleme.load(file="data/sf.pickle")
            all_posts = list(pickled['$set']['Items'].values())
            all_links = list(pickled['$set']['Urls'].values())
            all_links = enumerate(all_links, start = 1)
        except (IOError, KeyError, TypeError):
            print ("Pickle data error")
            #TBD - logging.exception or error to log - we handled it - move on
            #Sms/page out
            all_posts = ['Items Error'] * 3
            all_links = [fall_back_url] * 3
            all_links = enumerate(all_links, start = 1)
            return all_posts, all_links, city, state
        else:
            return all_posts, all_links, city, state

    except Exception as e:
        print("Unexpected Error", e)
=======
        all_posts = []
        all_links = []
        return all_posts, all_links, city, state

    except Exception as e:

        #logging.exception('Bad:, Caught an unexpected error')
        raise
>>>>>>> 6f6d65e63798a527865dd61ca3ebc88a693630db

    else:
        print("Debug:", craigs_list_url, city, state, items)

        """ Given the free items, see:                      """
        """ 1) How far away?                                """
        """ 2) How much on Ebay                             """
        """ 3) How much for a Lyft                          """



if __name__ == "__main__":

    import sys

    try:
        zip = sys.argv[1]
    except IndexError as e:
        print("Did you specify a zip?")
        sys.exit()

    try:
        print("Main", main(zip))
    except Exception as e:
        print("Error Main: ", e)
