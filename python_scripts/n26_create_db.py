import pandas as pd
import sqlite3

# File paths
transactions_file = 'csv_files/transactions.csv'
users_file = 'csv_files/users.csv'
db_path = 'N26_db'

def load_csv_to_dataframe(file_path):
    #Loads a CSV file into a Pandas DataFrame
    return pd.read_csv(file_path)
    

def create_database_and_tables(db_path, df_transactions, df_users):
    #Creates SQLite database and tables for transactions and users
    with sqlite3.connect(db_path) as connection:
        #Write dataframes to SQL
        df_transactions.to_sql('transactions_n26', connection, if_exists='replace', index=False)
        df_users.to_sql('users_n26', connection, if_exists='replace', index=False)

def main():
    df_transactions = load_csv_to_dataframe(transactions_file)
    df_users = load_csv_to_dataframe(users_file)
    create_database_and_tables(db_path, df_transactions, df_users)

# Run the main function
if __name__ == "__main__":
    main()
