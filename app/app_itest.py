# -*- coding: utf-8 -*-

import json
import unittest
import requests

def get_response(data):
    url = 'http://localhost:5003/restaurant-recommender'
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response


class TestRestResponses(unittest.TestCase):
    """Test class."""

    def test1(self):
        """Test send single missing field data"""
        data = {}
        response = get_response(data)
        content = json.loads(response.content)
        self.assertTrue(response.status_code == 400)
        self.assertTrue(content == {'error': "'Expecting place_id'"})
        
        
    def test2(self):
        """Test send single wrong type data"""
        data = {'place_id': 12345}
        response = get_response(data)
        content = json.loads(response.content)
        self.assertTrue(response.status_code == 400)
        self.assertTrue(content == {'error': 'Wrong type data'})
        
        
    def test3(self):
        """Test send batch data"""
        data = [{'place_id': 'ChIJEyLo-zE92jERXFAj_RC82Kk'},
                {'place_id': 'ChIJ4SgyUwsZ2jERPRgInXK4lfk'},
                {'place_id': 'teecoin'}]
        response = get_response(data)
        content = json.loads(response.content)

        self.assertTrue(response.status_code == 200)
        self.assertTrue(set(['ChIJD-tE5DE92jERY__E3dSxaFQ', 'ChIJB1W_8TE92jERrsGFhrd_riQ', 
                             'ChIJgUQQ-0o92jERPHIApGme2Co', 'ChIJ-wXsS7si2jER6wYY-i4eKS4']).\
                                    issubset(content[0]['recommendations']))
        self.assertTrue(set(['ChIJ46FyKPIa2jERZkGT5Pwt_Dw', 'ChIJf31qKJcZ2jERB5VfEczd6gQ']).\
                                    issubset(content[1]['recommendations']))
        self.assertTrue(content[2]['recommendations'] == [])

if __name__ == '__main__':
    unittest.main()