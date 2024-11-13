# Importing standard libraries
import csv
from collections import defaultdict
from decimal import Decimal

# File paths
users_file = 'csv_files/users.csv'
transactions_file = 'csv_files/transactions.csv'

def get_active_users(users_file):
    #Reads users file and returns a set of active user IDs.
    active_users = set()
    with open(users_file, mode='r') as u_file:
        user_reader = csv.DictReader(u_file)
        for row in user_reader:
            if row['is_active'].strip().lower() == 'true':
                active_users.add(row['user_id'])
    return active_users


def process_transactions(transactions_file, active_users):
    #Processes transactions and returns aggregated data by category
    category_sums = defaultdict(Decimal)
    category_user_counts = defaultdict(set)

    with open(transactions_file, mode='r') as t_file:
        transaction_reader = csv.DictReader(t_file)
        for row in transaction_reader:
            is_blocked = row['is_blocked'].strip().lower() == 'false'
            user_id = row['user_id']

            if is_blocked and user_id in active_users:
                category_id = row['transaction_category_id']
                amount = Decimal(row['transaction_amount'])

                #Sum amounts and track unique users per category
                category_sums[category_id] += amount
                category_user_counts[category_id].add(user_id)

    #Results sorted by sum in descending order
    results = sorted(
        [(category_id, category_sums[category_id], len(category_user_counts[category_id])) 
         for category_id in category_sums],
        key=lambda x: x[1],
        reverse=True
    )

    return results

def print_results(results):
    print("transaction_category_id, sum_amount, num_users")
    for category_id, sum_amount, num_users in results:
        print(f"{category_id}, {sum_amount}, {num_users}")


def main():
    active_users = get_active_users(users_file)
    results = process_transactions(transactions_file, active_users)
    print_results(results)

#Run the main function
if __name__ == "__main__":
    main()