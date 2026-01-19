def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    Returns: list of raw lines (strings)
    """

    encodings_to_try = ['utf-8', 'latin-1', 'cp1252']
    raw_lines = []

    for enc in encodings_to_try:
        try:
            with open(filename, 'r', encoding=enc) as f:
                # Read all lines
                lines = f.readlines()

                # Skip header row (first line)
                lines = lines[1:]

                # Remove empty lines and strip spaces
                raw_lines = [line.strip() for line in lines if line.strip() != ""]

            print(f"Successfully read file using {enc} encoding.")
            return raw_lines

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

        except UnicodeDecodeError:
            # Try next encoding if this one fails
            continue

    # If none of the encodings worked
    print("Error: Could not read file with available encodings.")
    return []
def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries.
    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    """

    transactions = []
    for line in raw_lines:
        try:
            parts = [p.strip() for p in line.split('|')]

            # Skip rows with incorrect number of fields
            if len(parts) != 8:
                continue

            transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

            # Remove commas from product name
            product_name = product_name.replace(',', '')

            # Remove commas from numbers and convert types
            quantity = int(quantity.replace(',', ''))
            unit_price = float(unit_price.replace(',', ''))

            # Build dictionary
            transaction = {
                'TransactionID': transaction_id,
                'Date': date,
                'ProductID': product_id,
                'ProductName': product_name,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': customer_id,
                'Region': region
            }

            transactions.append(transaction)

        except Exception:
            # Skip any problematic line
            continue

    return transactions
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    Returns: tuple (valid_transactions, invalid_count, filter_summary)
    """

    valid_transactions = []
    invalid_count = 0

    for t in transactions:
        try:
            # Validation rules
            if not t['TransactionID'].startswith('T'):
                invalid_count += 1
                continue
            if not t['ProductID'].startswith('P'):
                invalid_count += 1
                continue
            if not t['CustomerID'].startswith('C'):
                invalid_count += 1
                continue
            if t['Quantity'] <= 0 or t['UnitPrice'] <= 0:
                invalid_count += 1
                continue
            if not t['Region']:
                invalid_count += 1
                continue

            # Passed validation
            valid_transactions.append(t)

        except Exception:
            invalid_count += 1
            continue

    # Filtering
    filtered_transactions = valid_transactions

    # Filter by region
    if region:
        filtered_transactions = [t for t in filtered_transactions if t['Region'] == region]

    # Filter by amount (Quantity * UnitPrice)
    if min_amount or max_amount:
        temp = []
        for t in filtered_transactions:
            amount = t['Quantity'] * t['UnitPrice']
            if min_amount and amount < min_amount:
                continue
            if max_amount and amount > max_amount:
                continue
            temp.append(t)
        filtered_transactions = temp

    # Build summary
    filter_summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': len(valid_transactions) - len([t for t in valid_transactions if t['Region'] == region]) if region else 0,
        'filtered_by_amount': len(valid_transactions) - len(filtered_transactions) if (min_amount or max_amount) else 0,
        'final_count': len(filtered_transactions)
    }

    return filtered_transactions, invalid_count, filter_summary


