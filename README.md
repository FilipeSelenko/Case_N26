# Case resolution for Analytics Engineer at N26
# Resolution files:
- Task 1 (SQL): `n26_last_7days_trxs_resolution.sql`
- Task 2 (Python): `n26_query_script_resolution.py`

# Requirements:
- `Python 3.10`
- `DBeaver`

## Observations:
- The csv files were generated using the `generate_data.py` script.
- From the csv files a SQLite database was generated using pandas for querying the data. The script is `N26_db_script.py`
- Two tables were created within the database: `transactions_n26` and `users_n26`.
- The database is `N26_db`

## SQL task resolution:

### Query resolution file: `n26_last_7days_trxs_resolution.sql`

![image](https://github.com/user-attachments/assets/88c3cc9c-e278-432b-80e9-dfcfd840ef31)

Data sample: https://docs.google.com/spreadsheets/d/12SHNSRVTe_mmCmg0nV0vA5q26qmuTFB04WOhTMw_a70/edit?usp=sharing
Data test day by day: https://docs.google.com/spreadsheets/d/13qOcwGTAJfn5Xbu__C-jetdHo2Xbr1-H4UZWQ8m5mc0/edit?usp=sharing

**What would the query planner of the database need to consider in order to optimize the query?**

The creation of a composite index in the `user_id, date, transaction_id` columns would significantly increase query performance, as they would facilitate access to the relevant rows for the join and the calculation of the time filter (last 7 days), and also for the GROUP BY and ORDER BY clauses. This would avoid a full table scan, which would have a negative impact on performance and cost.

### Evidences:

- **Without index**

Time running all the rows of the table: 5 seconds:

![image](https://github.com/user-attachments/assets/a46d5f47-2090-4b56-8ef2-bb87b0234e50)


### Query plan:

![image](https://github.com/user-attachments/assets/7dc9e496-60c9-49e2-a3e8-cf19e0f5991f)

Obs:
SEARCH indicates that only a subset of the table rows are visited,
SCAN is used for a full-table scan (https://www.sqlite.org/eqp.html)


- **With index**

`CREATE INDEX idx_user_date ON transactions_n26 (user_id, date, transaction_id);`

Time running all the rows of the table: 0.373s:

![image](https://github.com/user-attachments/assets/c2ccdb7f-0544-4f68-aace-0bdaee141a46)


### Query plan:

![image](https://github.com/user-attachments/assets/22561761-cf7c-4fb3-ac64-70649da7ae94)

- When analyzing the results, we saw that the transactions table with the multiple index showed a reduction of more than 4 seconds when performing a SELECT on all the rows, bringing a significant gain in time and cost when we think of clouds whose cost is linked to execution time (i.e. BigQuery, Redshift).
- Another important point is the use of this index in the query plan, which made it easier to locate records without relying on the covering index created automatically by SQLite. Although the automatic covering index can offer benefits in some scenarios, it generally doesn't achieve the same level of performance as a customized, well-planned index.

## Python task resolution
### Script resolution file: `n26_query_script_resolution.py`

- More details inside the code

![image](https://github.com/user-attachments/assets/567faf1c-06f1-44f7-978d-ad63c79890be)

Comparison with the result of the query provided in database N26:

![image](https://github.com/user-attachments/assets/6bae567c-f543-4074-8276-8531fb680e63)
