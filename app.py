#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
app.py - Main Flask application file

- This script is the WSGI form parser/validator.

- This script requires Flask to be installed.

- It expects to be passed:
    - zip # from nginx html form

- It sends all returnables to return flask's render_template

- Credit/Refs:
https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
https://stackoverflow.com/questions/12551526/cast-flask-form-value-to-int
https://docs.gunicorn.org/en/stable/settings.html#logger-class
https://medium.com/@trstringer/logging-flask-and-gunicorn-the-manageable-way-2e6f0b8beb2f
https://stackoverflow.com/questions/58464052/request-to-flask-application-does-not-get-through-to-docker-container

TBD: - Add js input validation
     - Add cool look ahead form query
"""

import logging

import flask
from flask import Flask
from flask import request
from flask import render_template

import main

logname = "shouldipickit.app.log"
logging.basicConfig(
    filename=logname,
    level="INFO",
    format="%(levelname)s %(asctime)s %(module)s   \
                     %(process)d   %(message)s",
)

app = Flask(__name__)
app.debug = True 
verbose = True


@app.route("/forms/", methods=["POST", "GET"])
def get_data():
    """
    Return a view to Flask with relevant details

    zip comes in as a 'str' from the Flash HTML form  and most easily is tested
    by casting to 'int'. zip is then queried @mongodb and returns HTML
    """
    try:
        post_data = request.form
        zip = request.form.get("zip")
        try:
            if len(str(zip)) != 5:
                raise ValueError
            elif zip[0] == 0:
                int(zip[1:])
            else:
                int(zip)
        except (TypeError, ValueError):
        #Not Numeric/Didn't send "zip="
            if verbose:
                logging.error(f"Invalid POST data: {post_data} : nota5digitzip")
            return render_template("nota5digitzip.html")
    except Exception as e:
        msg = f"Bug: POST data:{post_data}, Error: {str(e)}"
        logging.exception(msg)
        flask.abort(500)
    else:
        zip = str(zip)
        if verbose:
            logging.info(f"POST data: {post_data}")
        all_posts, all_links, all_cust, city, state = main.main(zip)
        len_items = len(all_posts)
        return render_template(
            "craig_list_local_items.html",
            zip=zip,
            city=city,
            state=state,
            all_posts=all_posts,
            len_items=len_items,
            all_links=all_links,
            all_cust=all_cust,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
