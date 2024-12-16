from prettytable import PrettyTable

database = {}

def create_table(table_name, columns):
 
    if table_name in database:
        print(f"Table '{table_name}' already exists.")
        return
    
    database[table_name] = {
        'columns': columns, # str list
        'data': [], # list of dict
        'index': {column: {} for column in columns} # dist<dict<list<dict>>> dict of col_names {dict of col_name_values{list of entries}}
    }
    print(f"Table '{table_name}' was successfully created with columns: {', '.join(columns)}.")

def insert_into_table(table_name, values):
    
    # values: dict of column-value pairs
    
    if table_name not in database:
        print(f"Table '{table_name}' does not exist.")
        return
    
    table = database[table_name]
    columns = table['columns']
    
    for column in columns:
        if column not in values:
            print(f"Missing value for column '{column}'.")
            return
    
    row = {column: values[column] for column in columns}
    table['data'].append(row)
    
    # Update the index
    for column, value in row.items():
        if value not in table['index'][column]:
            table['index'][column][value] = []
        table['index'][column][value].append(row)
    
    # print(f"Row inserted into '{table_name}': {row}")

def print_table(table):
    # table: list of dicts with col-val pairs where each dict is a row

    columns = list(table[0].keys())

    print('+' + ("=" * 16 + '+') * len(columns))
    print('║' + ' ║'.join( col_name.ljust(15) for col_name in columns) + ' ║')
    print('+' + ("=" * 16 + '+') * len(columns))
    for row in table:
        print('║' + ' |'.join( str(col_value).ljust(15) for col_value in list(row.values())) + ' ║')
        print('+' + ("-" * 16 + '+') * len(columns))


def print_pretty_table(table):
    prettytable = PrettyTable()
    prettytable.field_names = list(table[0].keys())

    for row in table:
        prettytable.add_row(list(row.values()))

    print(prettytable)
    

# Example usage

# Create a table named 'employees'
create_table("employees", ["id", "name", "position", "salary", "department"])

# Populate the 'employees' table with 10 entries
insert_into_table("employees", {"id": 1, "name": "Alice", "position": "Manager", "salary": 75000, "department": "HR"})
insert_into_table("employees", {"id": 2, "name": "Bob", "position": "Developer", "salary": 85000, "department": "IT"})
insert_into_table("employees", {"id": 3, "name": "Charlie", "position": "Analyst", "salary": 65000, "department": "Finance"})
insert_into_table("employees", {"id": 4, "name": "Diana", "position": "Developer", "salary": 90000, "department": "IT"})
insert_into_table("employees", {"id": 5, "name": "Eve", "position": "Intern", "salary": 30000, "department": "Marketing"})
insert_into_table("employees", {"id": 6, "name": "Frank", "position": "Designer", "salary": 70000, "department": "Creative"})
insert_into_table("employees", {"id": 7, "name": "Grace", "position": "Manager", "salary": 80000, "department": "Sales"})
insert_into_table("employees", {"id": 8, "name": "Hank", "position": "Support", "salary": 45000, "department": "Customer Service"})
insert_into_table("employees", {"id": 9, "name": "Ivy", "position": "HR Specialist", "salary": 55000, "department": "HR"})
insert_into_table("employees", {"id": 10, "name": "Jack", "position": "Technician", "salary": 60000, "department": "Maintenance"})

# Print the 'employees' table data to verify
print('table:')
print_table(database['employees']['data'])
print('Alices')
print_pretty_table(database['employees']['index']['name']['Alice'])
print('managers')
print_table(database['employees']['index']['position']['Manager'])
