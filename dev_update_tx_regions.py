import csv
import requests
import json


mapping = {'Region 1': 69, 'Region 2': 70, 'Region 3': 71}
access_key = {"authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4ZGYzMzYxZWIzZWMyZjM3YzhmNDEwMjA1MzRjMTc5YWJhNWVhZmNmZmRhMDI0NWEyMmI2MDEzMWFlZjMwYzQ4Iiwic3ViIjoiOSIsImV4cCI6MTY2MTU5MDgwMCwiaXNzIjoiSGVhZHdheSIsInNjb3BlcyI6WyJkZWZhdWx0Il0sImlhdCI6MTY2MTUzMjkzOSwicm9sZXMiOlsiQVRMQVNfVVNFUiIsIlpPQ0RPQyIsIkFETUlOIiwiUFJPVklERVJfSU1QRVJTT05BVE9SIiwiUEFUSUVOVF9JTVBFUlNPTkFUT1IiLCJJTlRFUk5BTF9XRUJIT09LIiwiUEhJX1ZJRVdFUiJdfQ.X8PZFYxJGs8YwgyNnDi3NPkPzJ9QESMTL_8B7DdcvaY"}
dev_url = "http://localhost:5000/provider/"
prod_url = "https://headway.co/provider/"


def main():
    with open('dev_source.csv', 'r', encoding='utf-8-sig') as source:
        provider_data = csv.DictReader(source)
        for row in provider_data:
            provider = row["Providers Provider ID"]
            region = row["Final Region"]
            if validate_source(provider, region):
                update_region(provider, region)


def validate_source(provider, region):
    return True if provider and region in mapping else False


def reference_region(region):
    return mapping[region]


def update_region(provider_id, region):
    mapped_region = reference_region(region)
    new_region = {"providerLicenseState": {
        "providerRegionId": mapped_region}}
    json_body = json.dumps(new_region)

    try:
        res = requests.put(f"{dev_url}{provider_id}",
                           headers=access_key,
                           data=json_body)
        if res.status_code != 200:
            print(
                f"{res.status_code} Failed to update provider's {provider_id} region")
            # print(res.json())
        else:
            print(f"Successfully updated provider's {provider_id} region")
    except Exception as e:
        print(
            f"Exception: Failed to update provider's {provider_id} region.\nError: {str(e)}")


if __name__ == "__main__":
    main()
