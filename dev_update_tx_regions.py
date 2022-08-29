import csv
import requests
import json


mapping = {'Region 1': 69, 'Region 2': 70, 'Region 3': 71}
access_key = {"authorization": "bearer abc123"}
dev_url = "http://localhost:5000/provider/"
prod_url = "https://api.headway.co/provider/"
test_file = "dev_source.csv"
prod_file = "BCSBTX Region Mapping.csv"


def main():
    with open(prod_file, 'r', encoding='utf-8-sig') as source:
        provider_data = csv.DictReader(source)
        row_count = 0
        for row in provider_data:
            provider = row["Providers Provider ID"]
            region = row["Final Region"]
            if validate_source(provider, region):
                print(provider, region, mapping[region])
                update_region(provider, region)
            else:
                print(f"{provider} - {region} - validation failed")
            row_count += 1
            print(f"Cycle: {row_count}")
            # if row_count >= 1050:
            #     break


def validate_source(provider, region):
    return True if provider and region in mapping else False


def reference_region(region):
    return mapping[region]


def update_region(provider_id, region):
    mapped_region = reference_region(region)
    new_region = {"providerLicenseState": {
        "providerRegionId": mapped_region}}
    json_body = json.dumps(new_region)
    print(f"{prod_url}{provider_id}")
    try:
        res = requests.put(f"{prod_url}{provider_id}",
                           headers=access_key,
                           data=json_body)
        if res.status_code != 200 and res.status_code != 210:
            print(
                f"{res.status_code} - {provider_id} - {region} - Failed to update provider's {provider_id} region")
            # print(res.json())
        else:
            print(
                f"{res.status_code} - {provider_id} - {region} - Successfully updated provider's {provider_id} region")
    except Exception as e:
        print(
            f"{res.status_code} - {provider_id} - {region} - Exception: Failed to update provider's {provider_id} region.\nError: {str(e)}")


if __name__ == "__main__":
    main()
