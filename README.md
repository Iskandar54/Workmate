
## Использование

python main.py --files employees1.csv employees2.csv --report performance
<img width="554" height="191" alt="image" src="https://github.com/user-attachments/assets/edff3e04-b6e3-4339-8521-830594bbe352" />


## Тестирование

python test_all.py
<img width="997" height="406" alt="image" src="https://github.com/user-attachments/assets/b026d217-d6d9-4db2-b7c0-9ea31b8c9fbe" />


## Добавление нового отчета
###Чтобы добавить новый отчёт:
1. Создайте функцию в reports.py по образцу performance_report
2. Функция должна принимать список строк и возвращать таблицу с заголовком
3. Добавьте условие в get_report_function:

def get_report_function(report_name):
    if report_name == "performance":
        return performance_report
    elif report_name == "new_report":  # новый отчёт
        return new_report_function
    else:
        raise ValueError(f"Unknown report: {report_name}")
