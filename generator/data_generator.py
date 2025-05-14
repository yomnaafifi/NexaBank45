import pandas as pd
import numpy as np
import random
import faker
import json

# Initialize Faker
fake = faker.Faker()

# Settings
NUM_CUSTOMERS = 100_000
NUM_TICKETS = 15_000
NUM_MONTHS = 2

cities = ['Cairo', 'Alexandria', 'Riyadh', 'Jeddah', 'Dubai', 'Abu Dhabi', 'Casablanca', 'Doha', 'Beirut', 'Sfax']
complaint_categories = ['Unauthorized Transaction', 'Delayed Refund', 'Card Not Working',
                        'Loan Application Rejected', 'Account Locked', 'Incorrect Charges', 'Mobile App Issues',
                        'Poor Customer Service', 'ATM Withdrawal Failed', 'KYC Verification Delay']

genders = ['Male', 'Female']
customer_tiers = ['Gold', 'Platinum', 'Silver']
product_types = ["CreditCard", "Savings", "PremiumAccount"]


# 1. Generate customer_profiles.csv
customer_profiles = {
    'customer_id': [], 'name': [], 'gender': [], 'age': [], 'city': [],
    'account_open_date': [], 'product_type': [], 'customer_tier': []
}
for i in range(1, NUM_CUSTOMERS + 1):
    customer_profiles['name'].append(fake.name())
    customer_profiles['gender'].append(random.choice(genders))
    customer_profiles['age'].append(random.randint(18, 80))
    customer_profiles['city'].append(random.choice(cities))
    customer_profiles['account_open_date'].append(fake.date_between(start_date='-10y', end_date='-1y'))
    product_type = random.choice(product_types)
    customer_profiles['product_type'].append(product_type)
    customer_tier = random.choice(customer_tiers)
    customer_profiles['customer_tier'].append(customer_tier)
    customer_profiles['customer_id'].append(f'CUST{i:06d}')

customer_profiles_df = pd.DataFrame(customer_profiles)
customer_profiles_df.to_csv('../incoming_data/customer_profiles.csv', index=False)

# 2. Generate support_tickets.csv
support_tickets = {
    'ticket_id': [], 'customer_id': [], 'complaint_category': [], 'complaint_date': [], 'severity': []
}
sampled_customers = random.sample(customer_profiles_df['customer_id'].tolist(), NUM_TICKETS)
for i, cust_id in enumerate(sampled_customers):
    support_tickets['ticket_id'].append(f'TICKET{i+1:06d}')
    support_tickets['customer_id'].append(cust_id)
    support_tickets['complaint_category'].append(random.choice(complaint_categories))
    support_tickets['complaint_date'].append(fake.date_between(start_date='-1y', end_date='today'))
    support_tickets['severity'].append(random.randint(0, 10))

support_tickets_df = pd.DataFrame(support_tickets)
support_tickets_df.to_csv('../incoming_data/support_tickets.csv', index=False)

# 3. Generate credit_cards_billing.csv (2 months)
credit_cards_billing = {
    'bill_id': [], 'customer_id': [], 'month': [], 'amount_due': [],
    'amount_paid': [], 'payment_date': []
}

for cust_id in customer_profiles_df['customer_id']:
    for month_offset in range(NUM_MONTHS):
        bill_month = pd.Timestamp('2023-01-01') + pd.DateOffset(months=month_offset)
        amount_due = round(random.uniform(10, 300), 2)
        payment_delay_days = random.choice([0, 0, 0, 1, 2, 5, 7])
        amount_paid = amount_due if payment_delay_days <= 5 else round(amount_due * random.uniform(0.8, 1.0), 2)
        payment_date = (bill_month + pd.DateOffset(days=payment_delay_days)).strftime('%Y-%m-%d')
        credit_cards_billing['bill_id'].append(f'BILL{random.randint(1000000, 9999999)}')
        credit_cards_billing['customer_id'].append(cust_id)
        credit_cards_billing['month'].append(bill_month.strftime('%Y-%m'))
        credit_cards_billing['amount_due'].append(amount_due)
        credit_cards_billing['amount_paid'].append(amount_paid)
        credit_cards_billing['payment_date'].append(payment_date)

billing_df = pd.DataFrame(credit_cards_billing)
billing_df.to_csv('../incoming_data/credit_cards_billing.csv', index=False)

# 4. Generate data for Money Transfers or Purchases
transactions_data = []
for cust_id in customer_profiles_df['customer_id']:
    transaction_amount = random.randint(1, 100)
    receiver = np.random.choice(customer_profiles_df['customer_id'])
    transactions_data.append({
        'sender': cust_id,
        'receiver': receiver,
        'transaction_amount': transaction_amount,
        'transaction_date': str(fake.date_between(start_date='-1y', end_date='today'))
    })

with open('../incoming_data/transactions.json', 'w') as f:
    json.dump(transactions_data, f, indent=4)


# 5. Generate data for loan requests
# Formal and informal message templates
messages_text_file = open("./generated_1000_friend_and_formal_messages.txt")
messages = messages_text_file.readlines()
loan_types = ["Personal Loan", "Auto Loan", "Home Loan",
              "Credit Card Loan", "Education Loan", "Business Loan",
              "Medical Loan", "Travel Loan", "Top-Up Loan", "Loan Against Deposit"]

messages_file = open("../incoming_data/loans.txt", "w")
messages_file.write("customer_id|loan_type|amount_utilized|utilization_date|loan_reason\n")

for i in range(1000):
    customer_id = np.random.choice(customer_profiles_df['customer_id'])
    loan_type = np.random.choice(loan_types)
    amount_utilized = random.randint(10, 1000)
    amount_utilized *= 1000
    utilization_date = str(fake.date_between(start_date='-1y', end_date='today'))
    loan_reason = random.choice(messages).strip()
    line = f"{customer_id}|{loan_type}|{amount_utilized}|{utilization_date}|{loan_reason}\n"
    messages_file.write(line)

messages_file.close()
