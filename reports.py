def performance_report(rows):
    position_data = {}
    
    for row in rows:
        position = row.get('position', '')
        performance_str = row.get('performance', '')
        
        if not position or not performance_str:
            continue
            
        try:
            performance = float(performance_str)
        except ValueError:
            continue
        
        if position not in position_data:
            position_data[position] = {'total': 0.0, 'count': 0}
        
        position_data[position]['total'] += performance
        position_data[position]['count'] += 1
    
    results = []
    for position, data in position_data.items():
        if data['count'] > 0:
            average = data['total'] / data['count']
            results.append([position, round(average, 2)])
    
    results.sort(key=lambda x: (-x[1], x[0]))
    
    final_table = [['position', 'performance']]
    final_table.extend(results)
    
    return final_table

def get_report_function(report_name):
    if report_name == "performance":
        return performance_report
    else:
        raise ValueError(f"Unknown report: {report_name}")