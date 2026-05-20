import pandas as pd
import numpy as np

# Generate a realistic messy dataset
np.random.seed(42)

# Create 500 rows
n = 500

data = {
    'ID': np.arange(1, n + 1),
    'Customer_Name': ['User_' + str(i) for i in range(1, n + 1)],
    'Age': np.random.randint(18, 80, size=n).astype(float),
    'Income': np.random.normal(50000, 15000, size=n),
    'Status': np.random.choice(['Active', 'Inactive', 'Pending', None], size=n, p=[0.5, 0.2, 0.2, 0.1]),
    'SignUp_Date': pd.date_range(start='1/1/2020', periods=n, freq='D'),
    'Score': np.random.uniform(0, 100, size=n)
}

df = pd.DataFrame(data)

# Introduce Missing Values
df.loc[np.random.choice(df.index, 45, replace=False), 'Age'] = np.nan
df.loc[np.random.choice(df.index, 80, replace=False), 'Income'] = np.nan
df.loc[np.random.choice(df.index, 30, replace=False), 'Score'] = np.nan

# Introduce Duplicates
duplicates = df.sample(25)
df = pd.concat([df, duplicates], ignore_index=True)

# Introduce Outliers
df.loc[np.random.choice(df.index, 5, replace=False), 'Income'] = [500000, 600000, 550000, -10000, -20000]
df.loc[np.random.choice(df.index, 3, replace=False), 'Age'] = [150, 145, -5]

# Mess up Data Types (convert date to string, convert some IDs to string)
df['SignUp_Date'] = df['SignUp_Date'].astype(str)
df['ID'] = df['ID'].astype(str)
df.loc[10:20, 'ID'] = 'ID_STR'

# Save to CSV
df.to_csv('sample_messy_data.csv', index=False)
print("sample_messy_data.csv generated.")
