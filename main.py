import argparse
import sys
import tabulate
from reports import get_report_function
from read_csv import read_csv_files

def main():
    parser = argparse.ArgumentParser(description="Generate reports from CSV files")
    parser.add_argument("--files", "-f", nargs="+", required=True, help="CSV file paths")
    parser.add_argument("--report", "-r", required=True, help="Report name")
    
    args = parser.parse_args()
    
    all_rows = []
    for file_path in args.files:
        file_rows = read_csv_files([file_path])
        all_rows.extend(file_rows)
    
    if len(all_rows) == 0:
        print("No data found")
        sys.exit(1)
    
    report_func = get_report_function(args.report)
    report_data = report_func(all_rows)
    
    print(tabulate.tabulate(report_data, headers='firstrow', 
                            floatfmt=".2f", showindex=range(1, len(report_data))))
    
    return 0

if __name__ == "__main__":
    main()