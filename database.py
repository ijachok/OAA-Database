from prettytable import PrettyTable
from sortedcontainers import SortedDict
import time, random
from sortedcontainers import SortedDict

database = {}

def create_table(table_name, columns, indexed_columns=None):
    if table_name in database:
        print(f"Table '{table_name}' already exists.")
        return
    
    # Initialize table with columns and data
    database[table_name] = {
        'columns': columns,  # str list
        'data': [],  # list of dict
        'index': {column: SortedDict() for column in columns if column in (indexed_columns or [])}  # use SortedDict for indexed columns
    }
    print(f"Table '{table_name}' was successfully created with columns: {', '.join(columns)}.")
    if indexed_columns:
        print(f"Indexed columns: {', '.join(indexed_columns)}.") 

def insert_into_table(table_name, values):
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
    
    # Create the row from values
    row = {columns[i]: values[i] for i in range(len(columns))}
    table['data'].append(row)
    
    # Update the index for indexed columns
    for column, value in row.items():
        if column in table['index']:
            # Append row to the list of rows for this value in the index
            if value not in table['index'][column]:
                table['index'][column][value] = []
            table['index'][column][value].append(row)
    
    # print(f"Row inserted into '{table_name}': {row}")

def select_from_table_indexed(table, condition=None, order_by=None, column=True):
    selected_table = []

    # If there is a condition, apply the filtering
    if condition:
        column1, operator, value_or_column2 = condition
        if column1 not in table['columns']:
            print(f"Error: Column '{column1}' does not exist.")
            return
        
        # Compare two columns (when column=True)
        if column:  # Compare two columns
            if value_or_column2 not in table['columns']:
                print(f"Error: Column '{value_or_column2}' does not exist.")
                return

            # Filter based on operator between two columns
            def condition_filter(row):
                left_value = row[column1]
                right_value = row[value_or_column2]

                if operator == ">":
                    return str(left_value) > str(right_value)
                elif operator == "<":
                    return str(left_value) < str(right_value)
                elif operator == "=":
                    return str(left_value) == str(right_value)
                return False
            
            selected_table = [row for row in table['data'] if condition_filter(row)]

        else:  # Compare column with a value
            if column1 in table['index']:
                index = table['index'][column1]
                if operator == "=":
                    if value_or_column2 in index:
                        selected_table.extend(index[value_or_column2])  # Use extend to add multiple rows
                elif operator == ">":
                    for key in index.irange(minimum=value_or_column2,inclusive=(False, True)):
                        selected_table.extend(index[key])  # Use extend to add multiple rows
                elif operator == "<":
                    for key in index.irange(maximum=value_or_column2):
                        selected_table.extend(index[key])  # Use extend to add multiple rows

    # Sort the results if necessary
    if order_by:
        for column_name, order in reversed(order_by):  # Reverse to prioritize first columns
            selected_table.sort(key=lambda x: x[column_name], reverse=(order.upper() == "DESC"))
    
    return selected_table



def print_table(columns, table):
    # table: list of dicts with col-val pairs where each dict is a row

    print('+' + ("=" * 16 + '+') * len(columns))
    print('║' + ' ║'.join( col_name.ljust(15) for col_name in columns) + ' ║')
    print('+' + ("=" * 16 + '+') * len(columns))
    for row in table:
        print('║' + ' |'.join( str(col_value).ljust(15) for col_value in list(row.values())) + ' ║')
        print('+' + ("-" * 16 + '+') * len(columns))


def print_pretty_table(columns, table):
    # table: list of dicts with col-val pairs where each dict is a row
    prettytable = PrettyTable()
    prettytable.field_names = columns

    for row in table:
        prettytable.add_row(list(row.values()))

    print(prettytable)

def select_from_table(table, condition=None, order_by=None, column=True):
    
    # :param condition: A tuple  
    # example: ("name", ">", "Murzik") or ("age", ">", "salary").

    # :param order_by: A list of tuples
    # example: [("name", "ASC"), ("id", "DESC")].
    
    # :param column: Whether we should compare against a column (True) or a value (False)
    
    # :return: list of dicts with col-val pairs where each dict is a row

    selected_table = table["data"]
    columns = table["columns"]

    # Filter rows based on WHERE condition
    if condition:
        column1, operator, value_or_column2 = condition
        if column1 not in columns:
            print(f"Error: Column '{column1}' does not exist.")
            return

        def condition_filter(row):
            left_value = row[column1]
            # Right value can be another column or a literal
            right_value = row[value_or_column2] if column else value_or_column2

            if operator == ">":
                return str(left_value) > str(right_value)
            return False

        selected_table = [row for row in selected_table if condition_filter(row)]

    # Sort rows based on ORDER_BY clause
    if order_by:
        for column_name, order in reversed(order_by):  # Reverse to prioritize first columns
            if column_name not in columns:
                print(f"Error: Column '{column_name}' does not exist.")
                return
            selected_table.sort(key=lambda x: x[column_name], reverse=(order.upper() == "DESC"))

    # Print the result in table format
    return selected_table



    

# Example usage

if __name__ == "__main__":

    # Create a table named 'employees'
    print('CREATE employees (id, name, position, salary, department)')
    create_table("employees", ["id", "name", "position", "salary", "department"], ['salary', 'id', 'name'])
    # Populate the 'employees' table with 10 entries

    names = [
    "Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Hannah", 
    "Ian", "Jessica", "Kevin", "Laura", "Michael", "Nina", "Oliver", "Paula", 
    "Quentin", "Rachel", "Steven", "Tina"
    ]
    positions = [
        "Manager", "Developer", "Analyst", "HR Specialist", "Intern", "Team Lead", "CEO", 
        "Marketing Manager", "Sales Associate", "Data Scientist", "Software Engineer", 
        "Consultant", "Financial Advisor", "Product Manager", "IT Specialist", 
        "UX Designer", "Security Analyst", "Support Engineer", "HR Manager", "Accountant"
    ]
    salaries = [
        85000, 75000, 70000, 60000, 35000, 90000, 150000, 95000, 45000, 105000, 
        95000, 80000, 88000, 78000, 82000, 72000, 89000, 68000, 87000, 76000
    ]
    departments = [
        "HR", "IT", "Finance", "HR", "Marketing", "Management", "Executive", 
        "Marketing", "Sales", "Data Analytics", "Development", "Consulting", 
        "Finance", "Product", "IT", "Design", "Security", "Support", "HR", "Accounting"
    ]
    n = 1000000
    for i in range(n):
        insert_into_table(
            "employees", 
            [
                i, 
                random.choice(names), 
                random.choice(positions), 
                str(random.choice(salaries)), 
                random.choice(departments)
                ]
            )    

    print(f"inserted { n } random rows")

    start = time.time()
    # selected = select_from_table(
    #     database['employees'], 
    #     condition=("name", ">", "Michael"), 
    #     # order_by=[("name", "ASC"), ("id", "DESC")],
    #     column=False
        # )
    selected = select_from_table(
        database['employees'], 
        condition=("name", ">", "position"), 
        # order_by=[("name", "ASC"), ("id", "DESC")],
        column=True
        )
    end = time.time()

    start_indexed = time.time()
    # selected_indexed = select_from_table_indexed(
    #     database['employees'], 
    #     condition=("name", ">", "Michael"), 
    #     # order_by=[("name", "ASC"), ("id", "DESC")],
    #     column=False
    #     )
    selected_indexed = select_from_table_indexed(
        database['employees'], 
        condition=("name", ">", "position"), 
        # order_by=[("name", "ASC"), ("id", "DESC")],
        column=True
        )
    end_indexed = time.time()

    print(f"time taken for regular: {end - start} sec. | {len(selected)} rows")
    print(f"time taken for indexed: {end_indexed - start_indexed} sec. | {len(selected_indexed)} rows")

    # print_pretty_table(database['employees']['columns'], selected)
    # print_pretty_table(database['employees']['columns'], selected_indexed)

    # print_pretty_table(database['employees']['columns'], select_from_table(database['employees']))

    # print_pretty_table(database['employees']['columns'], select_from_table(database['employees'], condition=("name", ">", "salary"), order_by=[("name", "ASC"), ("id", "DESC")]))

    # print("Query by index 'age=30':", print_pretty_table(database['employees']['columns'], query_by_index("employees", "salary", 75000)))
