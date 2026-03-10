from dataclasses import dataclass
import json

@dataclass
class SOKPricing():
    def __init__(self, campaignPrice: float, lowest30DayPrice: float, campaignPriceValidUntil: str, regularPrice: float, currentPrice: float, salesUnit: str, comparisonPrice: float, comparisonUnit: str, isApproximatePrice: bool, depositPrice: float, quantityMultiplier: float):
        self.campaignPrice = campaignPrice
        self.lowest30DayPrice = lowest30DayPrice
        self.campaignPriceValidUntil = campaignPriceValidUntil
        self.regularPrice = regularPrice
        self.currentPrice = currentPrice
        self.salesUnit = salesUnit
        self.comparisonPrice = comparisonPrice
        self.comparisonUnit = comparisonUnit
        self.isApproximatePrice = isApproximatePrice
        self.depositPrice = depositPrice
        self.quantityMultiplier = quantityMultiplier
    def __str__(self):
        return f"Campaign Price: {self.campaignPrice}, Lowest 30 Day Price: {self.lowest30DayPrice}, Campaign Price Valid Until: {self.campaignPriceValidUntil}, Regular Price: {self.regularPrice}, Current Price: {self.currentPrice}, Sales Unit: {self.salesUnit}, Comparison Price: {self.comparisonPrice}, Comparison Unit: {self.comparisonUnit}, Is Approximate Price: {self.isApproximatePrice}, Deposit Price: {self.depositPrice}, Quantity Multiplier: {self.quantityMultiplier}"
    def to_dict(self):
        return {
            "campaignPrice": self.campaignPrice,
            "lowest30DayPrice": self.lowest30DayPrice,
            "campaignPriceValidUntil": self.campaignPriceValidUntil,
            "regularPrice": self.regularPrice,
            "currentPrice": self.currentPrice,
            "salesUnit": self.salesUnit,
            "comparisonPrice": self.comparisonPrice,
            "comparisonUnit": self.comparisonUnit,
            "isApproximatePrice": self.isApproximatePrice,
            "depositPrice": self.depositPrice,
            "quantityMultiplier": self.quantityMultiplier
        }
    def to_json(self):
        return json.dumps(self.to_dict())