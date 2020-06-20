# For Converts university names to place id.
import requests
import settings
import pandas as pd
import dask.dataframe as dd

BASE_URL = "https://maps.googleapis.com/maps/api/place/details/json?"
REQUEST_URL = BASE_URL + "place_id={}&fields={}&key=" + settings.ApiKey
REQUESTDETAILS = "formatted_address,photo,geometry"


def get_place(countryCode, universityName, domain, placeID):
    print(universityName)
    try:
        res = (requests.get(REQUEST_URL.format(placeID, REQUESTDETAILS))).json()['result']
    except KeyError:
        return ["N,N,N,N"]
    output = []

    # Adds Lat, Long coordinates as string
    output.append(res['geometry']['location']['lat'])
    output.append(res['geometry']['location']['lng'])

    # Add address
    output.append(res['formatted_address'])

    # Photo  reference only if possible
    try:
        output.append(res['photos'][0]['photo_reference'])

        try:
            output.append(res['photos'][0]['html_attributions'][0])
        except:
            output.append("NA")


    except:
        output.append("NA")
        output.append("NA")

    # Lat,Long,Address,PhotoRef,Photoattrib
    return output


if __name__ == '__main__':

    fileName = "./place_ids_added.csv"
    #
    df = pd.read_csv(fileName, skiprows=0)
    #
    data = df
    ddata = dd.from_pandas(data, npartitions=15)
    res = ddata.map_partitions(lambda df: df.apply((lambda row: get_place(*row)), axis=1)).compute(scheduler="threads")



    df = pd.concat([df,res],axis=1)


    df.to_csv("finaloutput.csv", index=False)
