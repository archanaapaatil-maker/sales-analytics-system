import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API.
    Returns: list of product dictionaries.
    """

    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error if request failed
        data = response.json()

        products = data.get('products', [])
        print(f"Successfully fetched {len(products)} products from API.")
        return products

    except requests.exceptions.RequestException as e:
        print(f"Error fetching products: {e}")
        return []
def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info.
    Returns: dictionary mapping product IDs to info.
    Format:
    {
        1: {'title': 'iPhone 9', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.69},
        2: {'title': 'iPhone X', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.44},
        ...
    }
    """

    product_mapping = {}

    for product in api_products:
        product_id = product.get('id')
        if product_id is not None:
            product_mapping[product_id] = {
                'title': product.get('title'),
                'category': product.get('category'),
                'brand': product.get('brand'),
                'rating': product.get('rating')
            }

    return product_mapping
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information.
    Returns: list of enriched transaction dictionaries.
    """

    enriched_transactions = []

    for t in transactions:
        try:
            # Extract numeric ID from ProductID (e.g., P101 -> 101)
            numeric_id = int(t['ProductID'][1:])

            if numeric_id in product_mapping:
                api_info = product_mapping[numeric_id]
                t['API_Category'] = api_info.get('category')
                t['API_Brand'] = api_info.get('brand')
                t['API_Rating'] = api_info.get('rating')
                t['API_Match'] = True
            else:
                t['API_Category'] = None
                t['API_Brand'] = None
                t['API_Rating'] = None
                t['API_Match'] = False

        except Exception:
            t['API_Category'] = None
            t['API_Brand'] = None
            t['API_Rating'] = None
            t['API_Match'] = False

        enriched_transactions.append(t)

    return enriched_transactions


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file in pipe-delimited format.
    """

    header = "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(header + "\n")

            for t in enriched_transactions:
                line = f"{t['TransactionID']}|{t['Date']}|{t['ProductID']}|{t['ProductName']}|{t['Quantity']}|{t['UnitPrice']}|{t['CustomerID']}|{t['Region']}|{t['API_Category']}|{t['API_Brand']}|{t['API_Rating']}|{t['API_Match']}"
                f.write(line + "\n")

        print(f"Enriched data saved to {filename}")

    except Exception as e:
        print(f"Error saving enriched data: {e}")
