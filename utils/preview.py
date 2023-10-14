import argparse
import duckdb

def run_query(query):
    con = duckdb.connect('duck.db')
    result = con.execute(query).df()
    con.close()
    return result


def preview_table(table):
    query = f'SELECT * FROM {table} LIMIT 10'
    print(query)
    result = run_query(query)
    print(result)


def preview_data(query):
    result = run_query(query)
    print(result)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Preview data')

    parser.add_argument('--table', type=str, help='Table to preview', required=False)
    parser.add_argument('--query', type=str, help='Query to preview', required=False)

    args = parser.parse_args()

    if args.table:
        preview_table(args.table)
    
    if args.query:
        preview_data(args.query)
    
