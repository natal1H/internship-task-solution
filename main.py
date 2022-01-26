import os
import json
from datetime import datetime

"""
@Author: Natália Holková
@Date: 26.01.2022
"""


DATA_DIR = "data/"


def get_datetime(date_str):
    """
    Function to convert datetime string to object

    :param date_str: string representing date
    :return: DateTime object
    """
    if len(time_returned_str) == 32:  # longer variant (length 32)
        res = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    else:  # shorter variant: 2021-12-02T07:05:49+00:00 (length 25)
        res = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
    return res


def calculate_median(arr):
    """
    Calculates median of an array

    :param arr: Array
    :return: Median value
    """
    arr.sort()
    arr_length = len(arr)
    middle_index = (arr_length - 1) // 2  # index of middle element
    if arr_length % 2:  # even number - take middle element of sorted array
        median = times_between_requests[middle_index]
    else:  # odd number - take average of two middle elements of sorted array
        median = (times_between_requests[middle_index] + times_between_requests[middle_index + 1]) / 2.0
    return median


if __name__ == '__main__':
    num_unique_item_requests = 0
    times_between_requests = []
    max_items = 0

    parsed_data = {}

    # iterate over all files in the directory
    for file in os.listdir(DATA_DIR):
        f = open(DATA_DIR + file)
        json_data = json.load(f)  # Load json objects from file

        # iterate over all users in the dictionary
        for key, user in json_data.items():
            # delete unimportant 'variant' part in user
            user.pop('variant', None)

            # get item_ids
            item_ids = [*user]  # unpack keys in user (item_ids)
            # iterate over all items and transform the datetime string
            for item_id in item_ids:
                num_unique_item_requests += 1  # counter for task 2
                item = user[item_id][0]
                item_request_times = []

                # Remove empty items
                if len(item) == 0:
                    user.pop(item_id, None)
                    continue

                # First request of an item - has to be done separately
                time_returned_str = item[0][0]

                # get variant and compare it for task 5
                variant = item[0][1]
                if variant == "similarInJsonList" and len(item) > max_items:
                    max_items = len(item)  # new max number of requests of variant 'similarInJsonList'

                datetime_object = previous_datetime_object = get_datetime(time_returned_str)
                item_request_times.append(datetime_object)  # list of request times for item

                # the next item requests
                for i in range(1, len(item)):
                    time_returned_str = item[i][0]
                    datetime_object = get_datetime(time_returned_str)

                    # calculate difference between requests
                    times_between_requests.append((datetime_object - previous_datetime_object).total_seconds())
                    previous_datetime_object = datetime_object  # update
                    item_request_times.append(datetime_object)
                user[item_id] = [item_request_times, variant]  # rewrite dictionary value for simpler structure

        parsed_data.update(json_data)  # Merge into one dictionary

    # Print out results
    # 1. count number of unique users in one day
    num_unique_users = len(parsed_data)
    print("Number of unique users: {}".format(num_unique_users))

    # 2. number of unique requests
    print("Number of unique requests: {}".format(num_unique_item_requests))

    # 3. average time between item_id requests
    average_request_time = sum(times_between_requests) / len(times_between_requests)
    print("Average time between item_id requests: {:.2f}s".format(average_request_time))

    # 4. median time between item_id requests
    median_time = calculate_median(times_between_requests)
    print("Median time between item_id requests: {:.2f}s".format(median_time))

    # 5. maximum number of requests per a single item_id for which the variant similarInJsonList was returned
    print("Maximum number of requests for variant similarInJsonList: {}".format(max_items))
