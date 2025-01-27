import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import uuid

###############################################################
# Number of participants to simulate (Max of 1,000,000 for CSV)
N = 100000
###############################################################


def generate_survey_data(num_records=100):
    current_date = datetime(2025, 1, 27)

    def generate_datetime():
        days_back = random.randint(0, 4)  # Generate dates within last 4 days
        hours = random.randint(0, 23)
        minutes = random.randint(0, 59)
        seconds = random.randint(0, 59)
        return current_date - timedelta(days=days_back, hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))

    data = []
    for _ in range(num_records):
        start_date = generate_datetime()
        duration = random.randint(50, 1000)  # Duration between 50-1000 seconds
        end_date = start_date + timedelta(seconds=duration)
        record = {
            'StartDate': start_date,
            'EndDate': end_date,
            'Status': np.random.choice(['IP Address', 'Survey Preview'], p=[0.8, 0.2]),
            'Progress': 100,
            'Duration (in seconds)': duration,
            'Finished': True,
            'RecordedDate': end_date + timedelta(seconds=1),
            'ResponseId': f"R_{uuid.uuid4().hex[:16]}",
            'DistributionChannel': np.random.choice(['anonymous', 'preview'], p=[0.8, 0.2]),
            'UserLanguage': 'EN',
            'Q_RecaptchaScore': round(random.uniform(0.1, 1.0), 1),
            'Q_RelevantIDDuplicate': np.random.choice([True, False], p=[0.8, 0.2]),
            'Q_RelevantIDDuplicateScore': random.randint(85, 100) if random.random() < 0.8 else 0,
            'Q_RelevantIDFraudScore': random.randint(0, 30) if random.random() < 0.8 else 0,
            'Q_RelevantIDLastStartDate': start_date - timedelta(hours=5),
            'Q1': 'I Agree',
            'Q2.1': np.random.choice(['I understand and I\'m ready to work with Paul', ''], p=[0.6, 0.4]),
            'Q2.2': np.random.choice(['I understand and I am ready to work with the robot', ''], p=[0.4, 0.6]),
            'Q13_First Click': round(random.uniform(4, 16), 3),
            'Q13_Last Click': round(random.uniform(10, 42), 3),
            'Q13_Page Submit': None,  # Will be set just after
            'Q13_Click Count': random.randint(1, 14),
        }

        # Set Page Submit to be slightly higher than Last Click
        record['Q13_Page Submit'] = round(record['Q13_Last Click'] + 0.003, 3)

        # Generate ordering attention check (Q4_1, Q4_2, Q4_3)
        record.update({f'Q4_{i}': i for i in range(1, 4)})

        # Generate Q5 responses (1-6 scale)
        record.update({f'Q5_{i}': random.randint(1, 6) for i in range(1, 13)})

        # Generate Q6 responses (1-7 scale)
        record.update({f'Q6_{i}': random.randint(1, 7) for i in range(1, 12)})

        # Generate Q7 responses (1-5 scale)
        record.update({f'Q7_{i}': random.randint(1, 5) for i in range(1, 6)})

        # SC0 (either 2 or 14)
        record['SC0'] = np.random.choice([2, 14], p=[0.4, 0.6])

        # Scenario
        record['Scenario'] = np.random.choice(['Anthropomorphic', 'Technical'], p=[0.6, 0.4])

        data.append(record)

    df = pd.DataFrame(data)
    return df


# Generate sample data
df = generate_survey_data(N)  # Generate N records
print(df.head())

# Export to CSV
df.to_csv('generated_survey_data.csv', index=False)