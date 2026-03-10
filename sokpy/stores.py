import sok.categories as categories
from .query_hashes import PRODUCT_SEARCH_HASH
from dataclasses import dataclass
from .pricing import SOKPricing
from .products import SOKProduct
import json

@dataclass
class SOKStore:
    def __init__(self,api: "SOKAPI", store_id: str, slug: str, name: str, brand: str, domains: list[str], location: str, postcode: str, postcodeName: str, weeklyOpeningHours: list[object]): # type: ignore
        self.api = api
        self.store_id = store_id
        self.slug = slug
        self.name = name
        self.brand = brand
        self.domains = domains
        self.location = location
        self.postcode = postcode
        self.postcodeName = postcodeName
        self.weeklyOpeningHours = weeklyOpeningHours
        self.categories = categories.SOKCategories(self)


    def get_filtered_products(self, slug: str, limit: int = 10) -> list[SOKProduct]:
        variables = {
            "facets":[
                {"key":"brandName","order":"asc"},
                {"key":"labels"}
            ],
            "from":0,
            "limit":limit,
            "queryString":"",
            "slug": slug,
            "storeId": self.store_id,
            "fetchSponsoredContent":True,
            "includeAgeLimitedByAlcohol":True,
            "useRandomId":True
        }

        response = self.api._request("RemoteFilteredProducts", variables, PRODUCT_SEARCH_HASH)
        products = []

        for product_data in response["data"]["store"]["products"]["productListItems"]:
            product = self.create_product(product_data["product"])
            products.append(product)

        all_product_count = response["data"]["store"]["products"]["total"]
        product_count = len(response["data"]["store"]["products"]["productListItems"])
        for i in range(limit, all_product_count, limit):
            variables["from"] = i
            response = self.api._request("RemoteFilteredProducts", variables, PRODUCT_SEARCH_HASH)
            product_count += len(response["data"]["store"]["products"]["productListItems"])
            for product_data in response["data"]["store"]["products"]["productListItems"]:
                product = self.create_product(product_data["product"])
                products.append(product)
            print(f"Got {product_count} / {all_product_count} products for store {self.name}")
        return products


    def create_product(self, product_data: dict) -> SOKProduct:
        pricing_data = product_data["pricing"]
        pricing = SOKPricing(pricing_data["campaignPrice"], pricing_data["lowest30DayPrice"], pricing_data["campaignPriceValidUntil"], pricing_data["regularPrice"], pricing_data["currentPrice"], pricing_data["salesUnit"], pricing_data["comparisonPrice"], pricing_data["comparisonUnit"], pricing_data["isApproximatePrice"], pricing_data["depositPrice"], pricing_data["quantityMultiplier"])
        return SOKProduct(
            product_id=product_data["id"],
            sokId=product_data["sokId"],
            name=product_data["name"],
            price=product_data["price"],
            availability=product_data["availability"],
            pricing=pricing,
            basicQuantityUnit=product_data["basicQuantityUnit"],
            comparisonPrice=product_data["comparisonPrice"],
            comparisonUnit=product_data["comparisonUnit"],
            priceUnit=product_data["priceUnit"],
            isAgeLimitedByAlcohol=product_data["isAgeLimitedByAlcohol"],
            frozen=product_data["frozen"],
            packagingLabelCodes=product_data["packagingLabelCodes"],
            brandName=product_data["brandName"],
            packagingLabels=product_data["packagingLabels"],
            slug=product_data["slug"]
        )
    def to_dict(self):
        return {
            "store_id": self.store_id,
            "slug": self.slug,
            "name": self.name,
            "brand": self.brand,
            "domains": self.domains,
            "location": self.location,
            "postcode": self.postcode,
            "postcodeName": self.postcodeName,
            "weeklyOpeningHours": self.weeklyOpeningHours,
            "categories": {slug: cat.to_dict() for slug, cat in self.categories.root.items()} if hasattr(self, "categories") else {}
        }
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)