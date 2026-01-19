import datetime

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report.
    """

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # 1. HEADER
            f.write("SALES ANALYTICS REPORT\n")
            f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Records Processed: {len(transactions)}\n\n")

            # 2. OVERALL SUMMARY
            total_revenue = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
            avg_order_value = total_revenue / len(transactions) if transactions else 0
            dates = [t['Date'] for t in transactions]
            date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

            f.write("# OVERALL SUMMARY\n\n")
            f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
            f.write(f"Total Transactions: {len(transactions)}\n")
            f.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
            f.write(f"Date Range: {date_range}\n\n")

            # 3. REGION-WISE PERFORMANCE
            from utils.data_processor import region_wise_sales
            region_stats = region_wise_sales(transactions)

            f.write("## REGION-WISE PERFORMANCE\n\n")
            f.write("Region | Sales | % of Total | Transactions\n")
            f.write("-------------------------------------------\n")
            for region, stats in region_stats.items():
                f.write(f"{region} | ₹{stats['total_sales']:,.2f} | {stats['percentage']:.2f}% | {stats['transaction_count']}\n")
            f.write("\n")

            # 4. TOP 5 PRODUCTS
            from utils.data_processor import top_selling_products
            top_products = top_selling_products(transactions, n=5)

            f.write("## TOP 5 PRODUCTS\n\n")
            f.write("Rank | Product | Quantity | Revenue\n")
            f.write("-----------------------------------\n")
            for i, (product, qty, revenue) in enumerate(top_products, start=1):
                f.write(f"{i} | {product} | {qty} | ₹{revenue:,.2f}\n")
            f.write("\n")

            # 5. TOP 5 CUSTOMERS
            from utils.data_processor import customer_analysis
            customer_stats = customer_analysis(transactions)
            top_customers = list(customer_stats.items())[:5]

            f.write("## TOP 5 CUSTOMERS\n\n")
            f.write("Rank | CustomerID | Total Spent | Orders\n")
            f.write("----------------------------------------\n")
            for i, (cust, stats) in enumerate(top_customers, start=1):
                f.write(f"{i} | {cust} | ₹{stats['total_spent']:,.2f} | {stats['purchase_count']}\n")
            f.write("\n")

            # 6. DAILY SALES TREND
            from utils.data_processor import daily_sales_trend
            daily_stats = daily_sales_trend(transactions)

            f.write("## DAILY SALES TREND\n\n")
            f.write("Date | Revenue | Transactions | Unique Customers\n")
            f.write("-----------------------------------------------\n")
            for date, stats in daily_stats.items():
                f.write(f"{date} | ₹{stats['revenue']:,.2f} | {stats['transaction_count']} | {stats['unique_customers']}\n")
            f.write("\n")

            # 7. PRODUCT PERFORMANCE ANALYSIS
            from utils.data_processor import find_peak_sales_day, low_performing_products
            peak_day, peak_revenue, peak_txn = find_peak_sales_day(transactions)
            low_products = low_performing_products(transactions)

            f.write("## PRODUCT PERFORMANCE ANALYSIS\n\n")
            f.write(f"Best Selling Day: {peak_day} | Revenue: ₹{peak_revenue:,.2f} | Transactions: {peak_txn}\n")
            f.write("Low Performing Products:\n")
            for product, qty, revenue in low_products:
                f.write(f"- {product}: Qty={qty}, Revenue=₹{revenue:,.2f}\n")
            f.write("\n")

            # 8. API ENRICHMENT SUMMARY
            enriched_count = sum(1 for t in enriched_transactions if t['API_Match'])
            success_rate = (enriched_count / len(enriched_transactions) * 100) if enriched_transactions else 0
            failed_products = [t['ProductName'] for t in enriched_transactions if not t['API_Match']]

            f.write("## API ENRICHMENT SUMMARY\n\n")
            f.write(f"Total Products Enriched: {enriched_count}\n")
            f.write(f"Success Rate: {success_rate:.2f}%\n")
            f.write("Products Not Enriched:\n")
            for p in failed_products:
                f.write(f"- {p}\n")

        print(f"Report saved to {output_file}")

    except Exception as e:
        print(f"Error generating report: {e}")
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data, save_enriched_data

def main():
    print("SALES ANALYTICS SYSTEM\n")

    try:
        # [1] Read sales data
        print("[1/10] Reading sales data ...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions\n")

        # [2] Parse and clean data
        print("[2/10] Parsing and cleaning data ...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records\n")

        # [3] Filter options
        print("[3/10] Filter Options Available:")
        regions = set(t['Region'] for t in transactions if t['Region'])
        amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]
        print(f"Regions: {', '.join(regions)}")
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}\n")

        choice = input("Do you want to filter data? (y/n): ").strip().lower()
        if choice == 'y':
            region = input("Enter region (or leave blank): ").strip() or None
            min_amount = input("Enter minimum amount (or leave blank): ").strip()
            max_amount = input("Enter maximum amount (or leave blank): ").strip()
            min_amount = float(min_amount) if min_amount else None
            max_amount = float(max_amount) if max_amount else None

            transactions, invalid_count, summary = validate_and_filter(transactions, region, min_amount, max_amount)
        else:
            transactions, invalid_count, summary = validate_and_filter(transactions)

        # [4] Validation summary
        print("[4/10] Validating transactions ...")
        print(f"✓ Valid: {len(transactions)} | Invalid: {invalid_count}\n")

        # [5] Data analysis
        print("[5/10] Analyzing sales data ...")
        total_revenue = calculate_total_revenue(transactions)
        print(f"✓ Total Revenue: ₹{total_revenue:,.2f}\n")

        # [6] Fetch products from API
        print("[6/10] Fetching product data from API ...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products\n")

        # [7] Enrich sales data
        print("[7/10] Enriching sales data ...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(transactions, product_mapping)
        enriched_count = sum(1 for t in enriched_transactions if t['API_Match'])
        print(f"✓ Enriched {enriched_count}/{len(enriched_transactions)} transactions\n")

        # [8] Save enriched data
        print("[8/10] Saving enriched data ...")
        save_enriched_data(enriched_transactions)
        print("✓ Saved to: data/enriched_sales_data.txt\n")

        # [9] Generate report
        print("[9/10] Generating report ...")
        generate_sales_report(transactions, enriched_transactions)
        print("✓ Report saved to: output/sales_report.txt\n")

        # [10] Complete
        print("[10/10] Process Complete!")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
