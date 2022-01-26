import os
import json
from datetime import datetime

DATA_DIR = "data/"


if __name__ == '__main__':
    num_unique_item_requests = 0
    request_times = []
    max_items = 0

    all_data = {}
    for file in os.listdir(DATA_DIR):
        f = open(DATA_DIR + file)
        json_data = json.load(f)  # Load json objects from file

        # Iterate over all users in the dictionary
        for key, user in json_data.items():
            # delete unimportant 'variant' part in user
            user.pop('variant', None)

            # get item_ids
            item_ids = [*user]  # unpack keys in user (item_ids)
            # iterate over all items and transform the datetime string
            for item_id in item_ids:
                num_unique_item_requests += 1
                item = user[item_id][0]
                item_requests = []
                tmp_datetime_object = None

                times = []

                if len(item) == 0:
                    user.pop(item_id, None)
                    continue
                # First item
                time_returned = item[0][0]

                variant = item[0][1]
                if variant == "similarInJsonList" and len(item) > max_items:
                    max_items = len(item)

                if len(time_returned) == 32:  # longer variant (length 32)
                    datetime_object = tmp_datetime_object = datetime.strptime(time_returned, "%Y-%m-%dT%H:%M:%S.%f%z")
                else:  # shorter variant: 2021-12-02T07:05:49+00:00 (length 25)
                    datetime_object = tmp_datetime_object = datetime.strptime(time_returned, "%Y-%m-%dT%H:%M:%S%z")
                times.append(datetime_object)

                # the next item requests
                for i in range(1, len(item)):
                    time_returned = item[i][0]
                    variant = item[i][1]
                    if len(time_returned) == 32:  # longer variant (length 32)
                        datetime_object = datetime.strptime(time_returned, "%Y-%m-%dT%H:%M:%S.%f%z")
                    else:  # shorter variant: 2021-12-02T07:05:49+00:00 (length 25)
                        datetime_object = datetime.strptime(time_returned, "%Y-%m-%dT%H:%M:%S%z")

                    # calculate difference between requests
                    request_times.append((datetime_object - tmp_datetime_object).total_seconds())
                    tmp_datetime_object = datetime_object  # update
                    times.append(datetime_object)
                user[item_id] = [times, variant]

        all_data.update(json_data)  # Merge into one dictionary

    # 1. count number of unique users in one day
    num_unique_users = len(all_data)
    print("Number of unique users: {}".format(num_unique_users))

    # 2. number of unique requests
    print("Number of unique requests: {}".format(num_unique_item_requests))

    # 3. average time between item_id requests
    average_request_time = sum(request_times) / len(request_times)
    print("Average time between item_id requests: {:.2f}s".format(average_request_time))

    # 4. median time between item_id requests
    request_times.sort()
    middle_index = (len(request_times) - 1) // 2  # index of middle element
    if len(request_times) % 2:  # even number - take middle element of sorted array
        median_time = request_times[(len(request_times) - 1) // 2]
    else:  # odd number - take average of two middle elements of sorted array
        median_time = (request_times[(len(request_times) - 1) // 2] + request_times[len(request_times) // 2]) / 2.0
    print("Median time between item_id requests: {:.2f}s".format(median_time))

    # 5. maximum number of requests per a single item_id for which the variant similarInJsonList was returned
    print("Maximum number of requests for variant similarInJsonList: {}".format(max_items))
