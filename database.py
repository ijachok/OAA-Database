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
    
    # values: list of column values
    
    if table_name not in database:
        print(f"Table '{table_name}' does not exist.")
        return
    
    table = database[table_name]
    columns = table['columns']

    if len(values) < len(columns):
        print(f"Values for {len(columns) - len(values)} columns are missing")
        return
    elif len(values) > len(columns):
        print(f"Extra {len(values) - len(columns)} values are present")
        return
    
    row = {columns[i]: values[i] for i in range(len(columns))}
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
insert_into_table("employees", [1, "Alice", "Manager", 75000, "HR"])
insert_into_table("employees", [1, "Alice", "Manager", 75000, "HR", 1111])
insert_into_table("employees", [2, "Bob", "Developer", 85000, "IT"])
insert_into_table("employees", [3, "Charlie", "Analyst", 65000, "Finance"])
insert_into_table("employees", [4, "Diana", "Developer", 90000, "IT"])
insert_into_table("employees", [5, "Eve", "Intern", 30000, "Marketing"])
insert_into_table("employees", [6, "Frank", "Designer", 70000, "Creative"])
insert_into_table("employees", [7, "Grace", "Manager", 80000, "Sales"])
insert_into_table("employees", [8, "Hank", "Support", 45000, "Customer Service"])
insert_into_table("employees", [9, "Ivy", "HR Specialist", 55000, "HR"])
insert_into_table("employees", [10, "Jack", "Technician", 60000, "Maintenance"])

# Print the 'employees' table data to verify
print('table:')
print_table(database['employees']['data'])
print('Alices')
print_pretty_table(database['employees']['index']['name']['Alice'])
print('managers')
print_table(database['employees']['index']['position']['Manager'])
