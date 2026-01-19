def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions.
    Returns: float (total revenue)
    """

    total = 0.0
    for t in transactions:
        try:
            total += t['Quantity'] * t['UnitPrice']
        except Exception:
            continue

    return total
def region_wise_sales(transactions):
    """
    Analyzes sales by region.
    Returns: dictionary with region statistics.
    Format:
    {
        'North': {
            'total_sales': 450000.0,
            'transaction_count': 15,
            'percentage': 29.13
        },
        'South': { ... }
    }
    """

    region_stats = {}
    total_revenue = calculate_total_revenue(transactions)

    for t in transactions:
        region = t['Region']
        amount = t['Quantity'] * t['UnitPrice']

        if region not in region_stats:
            region_stats[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }

        region_stats[region]['total_sales'] += amount
        region_stats[region]['transaction_count'] += 1

    # Calculate percentages
    for region, stats in region_stats.items():
        stats['percentage'] = (stats['total_sales'] / total_revenue * 100) if total_revenue > 0 else 0

    # Sort by total_sales descending
    sorted_stats = dict(sorted(region_stats.items(), key=lambda x: x[1]['total_sales'], reverse=True))

    return sorted_stats
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold.
    Returns: list of tuples in format:
    [(ProductName, TotalQuantity, TotalRevenue), ...]
    """

    product_stats = {}

    for t in transactions:
        product = t['ProductName']
        amount = t['Quantity'] * t['UnitPrice']

        if product not in product_stats:
            product_stats[product] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }

        product_stats[product]['total_quantity'] += t['Quantity']
        product_stats[product]['total_revenue'] += amount

    # Convert to list of tuples
    product_list = [
        (product, stats['total_quantity'], stats['total_revenue'])
        for product, stats in product_stats.items()
    ]

    # Sort by total_quantity descending
    product_list.sort(key=lambda x: x[1], reverse=True)

    # Return top n products
    return product_list[:n]
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns.
    Returns: dictionary of customer statistics.
    Format:
    {
        'C001': {
            'total_spent': 95000.0,
            'purchase_count': 3,
            'avg_order_value': 31666.67,
            'products_bought': ['Laptop', 'Mouse', 'Keyboard']
        },
        'C002': { ... }
    }
    """

    customer_stats = {}

    for t in transactions:
        customer = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        product = t['ProductName']

        if customer not in customer_stats:
            customer_stats[customer] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }

        customer_stats[customer]['total_spent'] += amount
        customer_stats[customer]['purchase_count'] += 1
        customer_stats[customer]['products_bought'].add(product)

    # Calculate average order value and convert products to list
    for customer, stats in customer_stats.items():
        if stats['purchase_count'] > 0:
            stats['avg_order_value'] = stats['total_spent'] / stats['purchase_count']
        else:
            stats['avg_order_value'] = 0.0
        stats['products_bought'] = list(stats['products_bought'])

    # Sort by total_spent descending
    sorted_stats = dict(sorted(customer_stats.items(), key=lambda x: x[1]['total_spent'], reverse=True))

    return sorted_stats
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date.
    Returns: dictionary sorted by date.
    Format:
    {
        '2024-12-01': {
            'revenue': 125000.0,
            'transaction_count': 8,
            'unique_customers': 6
        },
        '2024-12-02': { ... }
    }
    """

    trend = {}

    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']
        customer = t['CustomerID']

        if date not in trend:
            trend[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': set()
            }

        trend[date]['revenue'] += amount
        trend[date]['transaction_count'] += 1
        trend[date]['unique_customers'].add(customer)

    # Convert unique_customers set to count
    for date, stats in trend.items():
        stats['unique_customers'] = len(stats['unique_customers'])

    # Sort by date (chronologically)
    sorted_trend = dict(sorted(trend.items(), key=lambda x: x[0]))

    return sorted_trend
def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue.
    Returns: tuple (date, revenue, transaction_count)
    Example: ('2024-12-15', 185000.0, 12)
    """

    daily_stats = daily_sales_trend(transactions)

    peak_day = None
    peak_revenue = 0.0
    peak_transactions = 0

    for date, stats in daily_stats.items():
        if stats['revenue'] > peak_revenue:
            peak_day = date
            peak_revenue = stats['revenue']
            peak_transactions = stats['transaction_count']

    return (peak_day, peak_revenue, peak_transactions)
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales.
    Returns: list of tuples in format:
    [(ProductName, TotalQuantity, TotalRevenue), ...]
    """

    product_stats = {}

    for t in transactions:
        product = t['ProductName']
        amount = t['Quantity'] * t['UnitPrice']

        if product not in product_stats:
            product_stats[product] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }

        product_stats[product]['total_quantity'] += t['Quantity']
        product_stats[product]['total_revenue'] += amount

    # Filter products below threshold
    low_products = [
        (product, stats['total_quantity'], stats['total_revenue'])
        for product, stats in product_stats.items()
        if stats['total_quantity'] < threshold
    ]

    # Sort by total_quantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products

