# sokpy

A Python wrapper for the SOK (S-Group) API, providing easy access to store information, product data, and pricing from Finnish S-Group stores.

## Features

- **Store Management**: Retrieve information about S-Group stores by brand or location
- **Product Information**: Get detailed product data including pricing, availability, and specifications
- **Pricing Data**: Access current prices, campaign prices, and historical pricing information
- **Category Browsing**: Browse products by categories within specific stores

## Installation

```bash
pip install sokpy
```

## Quick Start

```python
from sokpy import SOKAPI

# Initialize the API
api = SOKAPI()

# Get a product by ID
product = api.get_product_by_id("some-product-id")
print(f"Product: {product.name}")
print(f"Price: {product.price} €")

# Get stores by brand
stores = api.get_stores_by_brand("S-Market")
for store in stores[:5]:  # Show first 5 stores
    print(f"Store: {store.name} - {store.location}")

# Get a specific store
store = api.get_store_by_id("some-store-id")
print(f"Store: {store.name}")
print(f"Opening hours: {store.weeklyOpeningHours}")
```

## API Reference

### SOKAPI

The main API class for interacting with SOK services.

#### Methods

- `get_product_by_id(product_id: str) -> SOKProduct`: Retrieve a product by its ID
- `get_all_stores() -> dict`: Get all stores organized by brand
- `get_stores_by_brand(brand: str) -> list[SOKStore]`: Get stores for a specific brand
- `get_store_by_id(store_id: str) -> SOKStore`: Get a specific store by ID

### SOKProduct

Represents a product with detailed information.

#### Attributes

- `product_id`: Unique product identifier
- `sokId`: SOK-specific product ID
- `name`: Product name
- `price`: Current price
- `availability`: Product availability status
- `pricing`: SOKPricing object with detailed pricing information
- `basicQuantityUnit`: Unit of measurement
- `comparisonPrice`: Price per comparison unit
- `comparisonUnit`: Unit for price comparison
- `priceUnit`: Unit for pricing
- `isAgeLimitedByAlcohol`: Whether the product is age-restricted
- `frozen`: Whether the product is frozen
- `packagingLabelCodes`: List of packaging label codes
- `brandName`: Brand name
- `packagingLabels`: List of packaging labels
- `slug`: URL slug for the product

### SOKPricing

Contains detailed pricing information for a product.

#### Attributes

- `campaignPrice`: Current campaign price
- `lowest30DayPrice`: Lowest price in the last 30 days
- `campaignPriceValidUntil`: Campaign validity date
- `regularPrice`: Regular price
- `currentPrice`: Current price
- `salesUnit`: Unit for sales
- `comparisonPrice`: Price for comparison
- `comparisonUnit`: Unit for comparison
- `isApproximatePrice`: Whether price is approximate
- `depositPrice`: Deposit price
- `quantityMultiplier`: Quantity multiplier

### SOKStore

Represents a store with location and product information.

#### Attributes

- `store_id`: Unique store identifier
- `slug`: URL slug
- `name`: Store name
- `brand`: Store brand (e.g., "S-Market", "Prisma")
- `domains`: List of domains
- `location`: Street address
- `postcode`: Postal code
- `postcodeName`: City name
- `weeklyOpeningHours`: Opening hours for each day
- `categories`: SOKCategories object for browsing products

#### Methods

- `get_filtered_products(slug: str, limit: int = 10) -> list[SOKProduct]`: Get products from a specific category

## Examples

### Finding Stores Near You

```python
api = SOKAPI()

# Get all Prisma stores
prisma_stores = api.get_stores_by_brand("Prisma")
print(f"Found {len(prisma_stores)} Prisma stores")

# Display store information
for store in prisma_stores[:3]:
    print(f"{store.name} - {store.location}, {store.postcode} {store.postcodeName}")
```

### Product Price Comparison

```python
api = SOKAPI()

product = api.get_product_by_id("example-product-id")

if product.pricing:
    pricing = product.pricing
    print(f"Product: {product.name}")
    print(f"Regular Price: {pricing.regularPrice} €")
    print(f"Current Price: {pricing.currentPrice} €")
    if pricing.campaignPrice:
        print(f"Campaign Price: {pricing.campaignPrice} € (valid until {pricing.campaignPriceValidUntil})")
    print(f"Lowest 30-day Price: {pricing.lowest30DayPrice} €")
```

### Browsing Store Categories

```python
api = SOKAPI()
store = api.get_store_by_id("example-store-id")

# Get products from a specific category
dairy_products = store.get_filtered_products("maito-tuotteet", limit=20)
for product in dairy_products:
    print(f"{product.name}: {product.price} €")
```

or

```python
api = SOKAPI()
store = api.get_store_by_id("example-store-id")

#Get products from a specific category
chewing_gums = store.categories.karkit_ja_suklaat.purukumit.products()

for product in chewing_gums:
    print(f"{product.name}: {product.price} €")
```

## Requirements

- Python 3.7+
- requests
- beautifulsoup4

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This package is not officially affiliated with S-Group or SOK. Use responsibly and in accordance with S-Group's terms of service.
