import pytest
import os
import tempfile
import csv
from read_csv import read_csv_files
from reports import performance_report, get_report_function

def create_test_csv(content):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write(content)
        return f.name

def test_read_valid_csv():
    csv_content = ("name,position,performance\n"
                   "Alex,Backend Developer,4.8\n" 
                   "Maria,Frontend Developer,4.7")
    
    file_path = create_test_csv(csv_content)
    try:
        result = read_csv_files([file_path])
        assert len(result) == 2
        assert result[0]['name'] == 'Alex'
    finally:
        os.unlink(file_path)

def test_read_multiple_files():
    csv1 = """name,position,performance
              Alex,Backend,4.8"""
    
    csv2 = """name,position,performance
              Maria,Frontend,4.7"""
    
    file1 = create_test_csv(csv1)
    file2 = create_test_csv(csv2)
    try:
        result = read_csv_files([file1, file2])
        assert len(result) == 2
    finally:
        os.unlink(file1)
        os.unlink(file2)

def test_missing_required_columns():
    csv_content = """name,age,city
                     John,25,Moscow"""
    
    file_path = create_test_csv(csv_content)
    try:
        result = read_csv_files([file_path])
        assert result == []
    finally:
        os.unlink(file_path)

def test_empty_file():
    csv_content = "name,position,performance\n"
    
    file_path = create_test_csv(csv_content)
    try:
        result = read_csv_files([file_path])
        assert result == []
    finally:
        os.unlink(file_path)

def test_file_not_found():
    result = read_csv_files(['nonexistent_file.csv'])
    assert result == []

def test_skip_empty_rows():
    csv_content = ("name,position,performance\n"
                   "Alex,Backend,4.8\n"
                   "\n"
                   "Maria,Frontend,4.7")
    
    file_path = create_test_csv(csv_content)
    try:
        result = read_csv_files([file_path])
        assert len(result) == 2
    finally:
        os.unlink(file_path)

def test_performance_report_basic():
    test_data = [
        {'position': 'Backend', 'performance': '4.8'},
        {'position': 'Frontend', 'performance': '4.6'},
        {'position': 'Backend', 'performance': '4.9'},
    ]
    
    result = performance_report(test_data)
    assert result[0] == ['position', 'performance']
    assert len(result) == 3

def test_performance_report_sorting():
    test_data = [
        {'position': 'QA', 'performance': '4.5'},
        {'position': 'Backend', 'performance': '4.8'},
        {'position': 'DevOps', 'performance': '4.9'},
    ]
    
    result = performance_report(test_data)
    
    assert result[1][0] == 'DevOps' and result[1][1] == 4.9
    assert result[2][0] == 'Backend' and result[2][1] == 4.8
    assert result[3][0] == 'QA' and result[3][1] == 4.5

def test_invalid_performance_values():
    test_data = [
        {'position': 'Backend', 'performance': '4.8'},
        {'position': 'Frontend', 'performance': 'invalid'},  
        {'position': 'QA', 'performance': ''},  
        {'position': 'DevOps', 'performance': '4.9'},
        {'position': 'Mobile', 'performance': 'not_a_number'},  
    ]
    
    result = performance_report(test_data)

    assert len(result) == 3  
    
    positions = [row[0] for row in result[1:]]
    assert 'Backend' in positions
    assert 'DevOps' in positions
    assert 'Frontend' not in positions
    assert 'QA' not in positions
    assert 'Mobile' not in positions

def test_missing_position():
    test_data = [
        {'position': 'Backend', 'performance': '4.8'},
        {'performance': '4.7'}, 
        {'position': '', 'performance': '4.6'},  
        {'position': 'DevOps', 'performance': '4.9'},
        {'name': 'John', 'performance': '4.5'},  
    ]
    
    result = performance_report(test_data)
    
    assert len(result) == 3 
    
    positions = [row[0] for row in result[1:]]
    assert 'Backend' in positions
    assert 'DevOps' in positions

def test_single_position_multiple_entries():
    test_data = [
        {'position': 'Backend', 'performance': '5.0'},
        {'position': 'Backend', 'performance': '4.0'},
        {'position': 'Backend', 'performance': '3.0'},
        {'position': 'Backend', 'performance': '2.0'},
    ]
    
    result = performance_report(test_data)
    
    assert len(result) == 2  
    assert result[1][0] == 'Backend'
    assert result[1][1] == 3.5

def test_get_report_function():
    func = get_report_function('performance')
    assert func == performance_report

def test_get_unknown_report():
    try:
        get_report_function('unknown_report')
        assert False, "Should have raised ValueError"
    except ValueError:
        assert True

def test_end_to_end_flow():
    csv1 = """name,position,performance
              Alex,Backend Developer,4.8
              Maria,Frontend Developer,4.6"""
    
    csv2 = """name,position,performance
              John,Backend Developer,4.9
              Anna,Frontend Developer,4.7"""
    
    file1 = create_test_csv(csv1)
    file2 = create_test_csv(csv2)
    try:
        data = read_csv_files([file1, file2])
        assert len(data) == 4
        
        report = performance_report(data)
        assert report[0] == ['position', 'performance']
        
    finally:
        os.unlink(file1)
        os.unlink(file2)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])