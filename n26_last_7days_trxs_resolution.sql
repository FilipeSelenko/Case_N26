    SELECT
        t1.transaction_id,
        t1.user_id,
        t1.date,
        COUNT(t2.transaction_id) AS no_txn_last_7days
    FROM transactions_n26 AS t1
    JOIN transactions_n26 AS t2 
        ON t1.user_id = t2.user_id
        AND t2.date BETWEEN DATE(t1.date, '-6 days') AND t1.date
    GROUP BY t1.transaction_id, t1.user_id, t1.date
    ORDER BY t1.date ASC, t1.user_id