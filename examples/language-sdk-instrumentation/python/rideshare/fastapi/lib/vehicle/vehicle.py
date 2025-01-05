from lib.utility.utility import group_and_count
import pandas as pd
from typing import List

dfs = pd.read_csv('./lib/data/electric_vehicles_small.csv')
df = pd.read_csv('./lib/data/electric_vehicles.csv')

def sort_and_order(use_large_dataset: bool, search_terms: list):
    if use_large_dataset:
       sorted_terms = group_and_count(df, search_terms)
    else:
        sorted_terms = group_and_count(dfs, search_terms)

    return sorted_terms
