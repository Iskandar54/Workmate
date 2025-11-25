import csv

def read_csv_files(file_paths):
    all_data = []
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                first_row = next(reader, None)
                if first_row is None:
                    continue
                    
                if 'position' not in first_row or 'performance' not in first_row:
                    print(f"Error: Missing required columns in {file_path}")
                    continue
            
                file.seek(0)
                reader = csv.DictReader(file)
                
                for row in reader:
                    if not any(row.values()):
                        continue
                    all_data.append(row)
                    
        except FileNotFoundError:
            print(f"Error: File {file_path} not found")
            continue
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue
    
    return all_data