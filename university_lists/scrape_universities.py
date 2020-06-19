# For Converts university names to place id.
import requests
import settings
import pandas as pd
import dask.dataframe as dd


BASE_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/"
REQUEST_URL = BASE_URL + "json?input={}&inputtype=textquery&fields=place_id&key=" + settings.ApiKey


def get_place(countryCode, universityName, domain):
    print(universityName)

    output = (requests.get(REQUEST_URL.format(universityName)).json())
    try:
        output = output['candidates'][0]['place_id']

        return output
    except:
        return "NA"




if __name__ == '__main__':
    fileName = "./world-universities.csv"
    df = pd.read_csv(fileName, skiprows=0)

    data = df
    ddata = dd.from_pandas(data, npartitions=15)
    res = ddata.map_partitions(lambda df: df.apply((lambda row: get_place(*row)), axis=1)).compute(scheduler="threads")

    df.insert(3, "placeID", res)

    df.to_csv("out.csv", index=False)
