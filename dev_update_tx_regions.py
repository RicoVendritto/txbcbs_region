import csv
import requests
import json


mapping = {'Region 1': 69, 'Region 2': 70, 'Region 3': 71}
access_key = {"authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI1MzdiNmNlZTBiYmIyMzM5NDViNDhmMzQzZjU3OTE1YmY5ZDRiZjdkY2NkZDgwMTc2ZmRlOTQxN2NkMWE4NGQyIiwic3ViIjoiOSIsImV4cCI6MTY2MTg1MDAwMCwiaXNzIjoiSGVhZHdheSIsInNjb3BlcyI6WyJkZWZhdWx0Il0sImlhdCI6MTY2MTc4MTE1MCwicm9sZXMiOlsiQVRMQVNfVVNFUiIsIlpPQ0RPQyIsIkFETUlOIiwiUFJPVklERVJfSU1QRVJTT05BVE9SIiwiUEFUSUVOVF9JTVBFUlNPTkFUT1IiLCJJTlRFUk5BTF9XRUJIT09LIiwiUEhJX1ZJRVdFUiJdfQ.emYwK0mEFFL7hnQV_uMuvpfDy7HlKs_z7210QwETYRQ"}
dev_url = "http://localhost:5000/provider/"
prod_url = "https://headway.co/provider/"
test_file = "dev_source.csv"
prod_file = "BCSBTX Region Mapping.csv"


def main():
    with open(test_file, 'r', encoding='utf-8-sig') as source:
        provider_data = csv.DictReader(source)
        for row in provider_data:
            provider = row["Providers Provider ID"]
            region = row["Final Region"]
            if validate_source(provider, region):
                print(provider, region, mapping[region])
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
        if res.status_code != 200 and res.status_code != 210:
            print(
                f"{res.status_code} Failed to update provider's {provider_id} region]")
            # print(res.json())
        else:
            print(f"Successfully updated provider's {provider_id} region")
    except Exception as e:
        print(
            f"Exception: Failed to update provider's {provider_id} region.\nError: {str(e)}")


if __name__ == "__main__":
    main()
