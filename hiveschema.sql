--customer_profiles
CREATE EXTERNAL TABLE customer_profiles (
    customer_id STRING,
    name STRING,
    gender STRING,
    age INT,
    city STRING,
    account_open_date TIMESTAMP,
    product_type STRING,
    customer_tier STRING,
    tenure INT,
    customer_segment STRING,
    processing_time TIMESTAMP
)
PARTITIONED BY (partition_date DATE, partition_hour INT)
STORED AS PARQUET
LOCATION '/NexaBank45';

-- credit cards billing
CREATE EXTERNAL TABLE credit_cards_billing (
    bill_id STRING,
    customer_id STRING,
    month STRING,
    amount_due DOUBLE,
    amount_paid DOUBLE,
    payment_date TIMESTAMP,
    due_date TIMESTAMP,
    late_days INT,
    fully_paid BOOLEAN,
    debt DOUBLE,
    fine DOUBLE,
    total_amount DOUBLE,
    processing_time TIMESTAMP
)
PARTITIONED BY (partition_date DATE, partition_hour INT)
STORED AS PARQUET
LOCATION '/NexaBank45';

--support tickets 
CREATE EXTERNAL TABLE support_tickets (
    ticket_id STRING,
    customer_id STRING,
    complaint_category STRING,
    complaint_date TIMESTAMP,
    severity INT,
    age INT,
    processing_time TIMESTAMP
)
PARTITIONED BY (partition_date DATE, partition_hour INT)
STORED AS PARQUET
LOCATION '/NexaBank45';


--loans table
CREATE EXTERNAL TABLE loans (
    customer_id STRING,
    loan_type STRING,
    amount_utilized INT,
    utilization_date TIMESTAMP,
    loan_reason STRING,
    age INT,
    total_cost DOUBLE,
    processing_time TIMESTAMP
)
PARTITIONED BY (partition_date DATE, partition_hour INT)
STORED AS PARQUET
LOCATION '/NexaBank45';


--transactions table
CREATE EXTERNAL TABLE transactions (
    sender STRING,
    receiver STRING,
    transaction_amount INT,
    transaction_date TIMESTAMP,
    cost DOUBLE,
    total_amount DOUBLE,
    processing_time TIMESTAMP
)
PARTITIONED BY (partition_date DATE, partition_hour INT)
STORED AS PARQUET
LOCATION '/NexaBank45';