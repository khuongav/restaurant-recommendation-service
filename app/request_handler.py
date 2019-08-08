# -*- coding: utf-8 -*-
import sys
import json
import logging
import traceback
from flask import Flask, jsonify, make_response, request as flask_request

from recommendation.recommender import Recommender
from common import monitor

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')

recommender = Recommender()

print
@app.route('/restaurant-recommender', methods=['POST'])
def extract_data():
    """Recommendation API"""
    try:
        if not flask_request.is_json:
            raise ValueError('Expecting a json request')
        reqs = flask_request.get_json()

        if not isinstance(reqs, list):
            reqs = [reqs]

        results = []
        for req in reqs:
            if 'place_id' not in  req:
                raise KeyError('Expecting place_id')
            if not isinstance(req['place_id'], str):
                raise ValueError('Wrong type data')
            
            place_id = req['place_id']
            recommended_places = recommender.recommend(place_id)
            results.append({'place_id': place_id, 'recommendations': recommended_places})
                

    except (ValueError, KeyError) as ex:
        return make_response(jsonify({"error": str(ex)}), 400)
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        monitor.add(monitor.RECOMMENDER_EXCEPTION,
                    message=repr(traceback.extract_tb(exc_traceback)))
        return make_response(jsonify({"error": 'Internal error'}), 500)

    return make_response(jsonify(results), 200)

if __name__ == "__main__":
    app.run('0.0.0.0', 5003, threaded=True)
