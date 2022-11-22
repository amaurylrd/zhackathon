from urllib import request
import json


if __name__ == "__main__":
    # pylint: disable=invalid-name, line-too-long
    url = "https://data.culture.gouv.fr/explore/dataset/festivals-global-festivals-_-pl/download?format=json&timezone=Europe/Berlin&use_labels_for_header=false"

    with request.urlopen(url) as response:
        if response.status == 200:
            if data := json.load(response):
                fixtures = []
                for festival in data:
                    if festival["fields"]:
                        fixture = {
                            "model": "zhackathon.festival",
                            "pk": festival["fields"]["identifiant"],
                            "fields": {
                                "name": festival["fields"]["nom_du_festival"],
                                "discipline": festival["fields"]["discipline_dominante"],
                                "website": festival["fields"].get("site_internet_du_festival"),
                                "period": festival["fields"].get("periode_principale_de_deroulement_du_festival"),
                                "region": festival["fields"].get("region_principale_de_deroulement"),
                                "department": festival["fields"].get("departement_principal_de_deroulement"),
                                "commune": festival["fields"].get("commune_principale_de_deroulement"),
                                "postcode": festival["fields"].get(
                                    "code_postal_de_la_commune_principale_de_deroulement"
                                ),
                            },
                        }

                        fixtures.append(fixture)

                with open("../zhackathon/fixtures/festival.json", "w+", encoding="utf-8") as file:
                    json.dump(fixtures, file, indent=4)
