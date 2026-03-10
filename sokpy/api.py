import requests
import json
from . import sok_stores
from .query_hashes import STORE_SEARCH_HASH
from .stores import SOKStore
from .products import SOKProduct
from .pricing import SOKPricing
from bs4 import BeautifulSoup


class SOKAPI:
    BASE_URL = "https://api.s-kaupat.fi/"

    def __init__(self):
        self.url = "https://api.s-kaupat.fi/"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept":"application/json",
            "Referer":"https://www.s-kaupat.fi/",
            "Origin":"https://www.s-kaupat.fi",
            "Accept-Language":"fi-FI,fi;q=0.9,en;q=0.8"
        })


    def _request(self, operation_name, variables, sha256):
        params = {
            "operationName": operation_name,
            "variables": json.dumps(variables),
            "extensions": json.dumps({
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": sha256
                }
            })
        }

        r = self.session.get(self.BASE_URL, params=params)
        r.raise_for_status()
        return r.json()

    def get_product_by_id(self,id: str) -> SOKProduct:
        url = f"https://www.s-kaupat.fi/tuote/moi/{id}"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.find("script", {"id": "__NEXT_DATA__"})
        json_data = json.loads(data.string)


        p_data = {"data": v for k, v in json_data["props"]["pageProps"]["apolloState"].items() if 'Product:{"id"' in k}
        p_data = p_data["data"]

        pricing_data = p_data["pricing"]
        pricing = None
        if pricing_data != None:
            pricing = SOKPricing(pricing_data["campaignPrice"],pricing_data["lowest30DayPrice"], pricing_data["campaignPriceValidUntil"],pricing_data["regularPrice"],pricing_data["currentPrice"], pricing_data["salesUnit"], pricing_data["comparisonPrice"], pricing_data["comparisonUnit"],pricing_data["isApproximatePrice"], pricing_data["depositPrice"],pricing_data["quantityMultiplier"])
        product = SOKProduct(p_data["id"], p_data["sokId"],p_data["name"],p_data["price"],None,pricing, p_data["basicQuantityUnit"], p_data["comparisonPrice"], p_data["comparisonUnit"], p_data["priceUnit"], p_data["isAgeLimitedByAlcohol"], p_data["frozen"], p_data["packagingLabelCodes"], p_data["brandName"], p_data["packagingLabels"], p_data["slug"])
        return product
    def get_all_stores(self) -> list[SOKStore]:
        stores = {}
        for brand in sok_stores.ALL_STORES:
            stores[brand] = self.get_stores_by_brand(brand)

        return stores

    def get_store_by_id(self, id: str) -> SOKStore:
        url = f"https://www.s-kaupat.fi/myymala/moi/{id}"

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        data = soup.find("script", {"id": "__NEXT_DATA__"})
        json_data = json.loads(data.string)

        store_data = json_data["props"]["pageProps"]["store"]
        store = SOKStore(api=self,
                        store_id=store_data["id"],
                        slug=store_data["slug"],
                        name=store_data["name"],
                        brand=store_data["brand"],
                        domains=store_data["domains"],
                        location=store_data["location"]["address"]["street"]["default"],
                        postcode=store_data["location"]["address"]["postcode"],
                        postcodeName=store_data["location"]["address"]["postcodeName"]["default"],
                        weeklyOpeningHours=store_data["weeklyOpeningHours"]
                        )
        return store


    def get_stores_by_brand(self, brand: str) -> list[SOKStore]:
        variables = {"query": None, "brand": brand, "cursor": None}

        response = self._request("RemoteStoreSearch",variables, STORE_SEARCH_HASH)

        data = response["data"]["searchStores"]
        all_store_count = data["totalCount"]
        store_count = len(data["stores"])
        stores = []
        for store_data in data["stores"]:
            store = self.make_store(store_data)
            stores.append(store)

        print(f"Found {all_store_count} stores for brand {brand}")

        while store_count < all_store_count:
            variables["cursor"] = data["cursor"]

            response = self._request("RemoteStoreSearch",variables, STORE_SEARCH_HASH)

            data = response["data"]["searchStores"]
            store_count += len(data["stores"])

            for store_data in data["stores"]:
                store = self.make_store(store_data)
                stores.append(store)
        return stores

    def make_store(self, store_data: dict) -> SOKStore:
        return SOKStore(
            api=self,
            store_id=store_data["id"],
            slug=store_data["slug"],
            name=store_data["name"],
            brand=store_data["brand"],
            domains=store_data["domains"],
            location=store_data["location"]["address"]["street"]["default"],
            postcode=store_data["location"]["address"]["postcode"],
            postcodeName=store_data["location"]["address"]["postcodeName"]["default"],
            weeklyOpeningHours=store_data["weeklyOpeningHours"]
        )

