Sales Analytics System - Module 3 Assignment

 Overview
This repository contains my Python-based Sales Analytics System, developed as part of Module 3 Assignment.  
The system reads messy sales transaction data, cleans and validates it, performs detailed analysis, integrates product information from an API, and generates a comprehensive report for business insights.


Features Implemented
File Handling & Preprocessing  
  Reads sales data with encoding handling, parses transactions, and cleans invalid records.
Data Validation & Filtering  
  Ensures only valid transactions are processed, with optional filters by region or amount.
Sales Analysis
  - Overall revenue, transactions, and average order value  
  - Region-wise performance  
  - Top products and top customers  
  - Daily sales trends  
  - Low-performing products
API Integration  
  Connects to DummyJSON API to enrich product details (category, brand, rating).

Report Generation
  Creates a formatted text report (`output/sales_report.txt) with all required sections.


  Project Structure

- README.md → Project documentation  
- main.py → Main workflow script  
- utils → Helper modules  
  - file_handler.py → File I/O and preprocessing  
  - data_processor.py → Sales analysis functions  
  - api_handler.py → API integration functions  
- data  
  - sales_data.txt → Provided dataset  
- output 
  - sales_report.txt → Generated report  
- requirements.txt → Dependencies (requests library)
               

How to Run
Clone the repository:

   git clone https://github.com/archanaapaatil-maker/sales-analytics-system.git
Navigate into the folder:
cd sales-analytics-system
Install dependencies:
pip install -r requirements.txt
Run the program:
python main.py

 Outputs
Cleaned & Enriched Data → data/enriched_sales_data.txt

Comprehensive Report → output/sales_report.txt

The report includes:

Overall summary

Region-wise performance

Top 5 products

Top 5 customers

Daily sales trend

Product performance analysis

API enrichment summary
