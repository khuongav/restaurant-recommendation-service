# -*- coding: utf-8 -*-
import ast
import pandas as pd
from common.singleton_class import Singleton

class Recommender(object, metaclass=Singleton):
    """
    A singleton class to load data and recommend items
    """

    def __init__(self):
        """
        Init the recommender
        
        Args:
            sentiment: -1 for negative classifer, 1 for positive classifier
        """
        if not Recommender._first_init:
            self.__load_recommendations()
            self.__load_cid_placeid_mapping()

    def __load_recommendations(self):
        df = pd.read_csv('data/recommendations.csv')
        df = df.dropna()
        df = df[df['recommendations'] != 'No related searches']
        place_ids = df['place_id']
        rec_strs = list(df['recommendations'])
        rec_parseds = [ast.literal_eval(rec) for rec in rec_strs]
        cids = [[pair[1] for pair in rec] for rec in rec_parseds ]
        self.placeid_recs_dict = dict(zip(place_ids, cids))
        
    def __load_cid_placeid_mapping(self):
        df = pd.read_csv('data/cid_placeid.csv')
        cids = df['cid']
        place_ids = df['place_id']
        self.cid_placeid_map = dict(zip(cids, place_ids))
        
    
    def recommend(self, place_id):
        if place_id not in self.placeid_recs_dict:
            return []
        cids = self.placeid_recs_dict[place_id]
        recommended_place_ids = [self.cid_placeid_map[cid] for cid in cids 
                                 if cid in self.cid_placeid_map]
        return recommended_place_ids

        