import time
import pyroscope
import os
from datetime import datetime
import pandas as pd

# How much time mutex_lock() takes relative to search_radius()
MUTEX_LOCK_MULTIPLIER = 2

# How much time check_driver_availability() takes relative to search_radius()
DRIVER_AVAILABILITY_MULTIPLIER = 0.5

def mutex_lock(n):
    i = 0
    start_time = time.time()
    while time.time() - start_time < n * MUTEX_LOCK_MULTIPLIER:
        i += 1

def check_driver_availability(n):
    i = 0
    start_time = time.time()
    while time.time() - start_time < n * DRIVER_AVAILABILITY_MULTIPLIER:
        i += 1

    # Every 4 minutes this will artificially create make requests in eu-north region slow
    # this is just for demonstration purposes to show how performance impacts show up in the
    # flamegraph

    force_mutex_lock = datetime.today().minute * 4 % 8 == 0
    if os.getenv("REGION") == "eu-north" and force_mutex_lock:
        mutex_lock(n)


def find_nearest_vehicle(n, vehicle):
    with pyroscope.tag_wrapper({ "vehicle": vehicle}):
        i = 0
        start_time = time.time()
        while time.time() - start_time < n:
            i += 1
        if vehicle == "car":
            check_driver_availability(n)

def group_and_count(df: pd.DataFrame, groupby_terms: list[str]) -> str:
    """
    Groups the DataFrame by the specified terms and counts the occurrences.

    Parameters:
    df (pd.DataFrame): The pandas DataFrame to be grouped.
    groupby_terms (list): The list of column names to group by.

    Returns:
    str: A JSON string with the counts of each group.
    """
    tag = "_".join(groupby_terms)
    with pyroscope.tag_wrapper({ "groupby": tag}):
        result = df.groupby(groupby_terms).size().reset_index(name='Count')
        result_json = result.to_json(orient='records')
        return result_json