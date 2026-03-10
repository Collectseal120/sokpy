import json
from dataclasses import dataclass
from .pricing import SOKPricing


@dataclass
class SOKProduct:
    def __init__(self, product_id: str, sokId: str, name: str, price: float, availability: str, pricing: SOKPricing, basicQuantityUnit: str, comparisonPrice: float, comparisonUnit: str, priceUnit: str, isAgeLimitedByAlcohol: bool, frozen: bool, packagingLabelCodes: list[str], brandName: str, packagingLabels: list[str], slug: str):
        self.product_id = product_id
        self.sokId = sokId
        self.name = name
        self.price = price
        self.availability = availability
        self.pricing = pricing
        self.basicQuantityUnit = basicQuantityUnit
        self.comparisonPrice = comparisonPrice
        self.comparisonUnit = comparisonUnit
        self.priceUnit = priceUnit
        self.isAgeLimitedByAlcohol = isAgeLimitedByAlcohol
        self.frozen = frozen
        self.packagingLabelCodes = packagingLabelCodes
        self.brandName = brandName
        self.packagingLabels = packagingLabels
        self.slug = slug

    def __str__(self):
        return f"Product ID: {self.product_id}, SOK ID: {self.sokId}, Name: {self.name}, Price: {self.price}, Availability: {self.availability}, Pricing: {self.pricing}, Basic Quantity Unit: {self.basicQuantityUnit}, Comparison Price: {self.comparisonPrice}, Comparison Unit: {self.comparisonUnit}, Price Unit: {self.priceUnit}, Is Age Limited By Alcohol: {self.isAgeLimitedByAlcohol}, Frozen: {self.frozen}, Packaging Label Codes: {self.packagingLabelCodes}, Brand Name: {self.brandName}, Packaging Labels: {self.packagingLabels}, Slug: {self.slug}"
    def to_dict(self):
        return {
            "product_id": self.product_id,
            "sokId": self.sokId,
            "name": self.name,
            "price": self.price,
            "availability": self.availability,
            "pricing": self.pricing.to_dict(),
            "basicQuantityUnit": self.basicQuantityUnit,
            "comparisonPrice": self.comparisonPrice,
            "comparisonUnit": self.comparisonUnit,
            "priceUnit": self.priceUnit,
            "isAgeLimitedByAlcohol": self.isAgeLimitedByAlcohol,
            "frozen": self.frozen,
            "packagingLabelCodes": self.packagingLabelCodes,
            "brandName": self.brandName,
            "packagingLabels": self.packagingLabels,
            "slug": self.slug
        }
    def to_json(self):
        return json.dumps(self.to_dict())