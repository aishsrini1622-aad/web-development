import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\\Users\\aishwarya\\Downloads\\car_data\\CAR DETAILS FROM CAR DEKHO.csv")

print(df.head())
print(df.shape)
print(df.columns)

plt.hist(df['selling_price'], bins=30)
plt.show()

df['fuel'].value_counts().plot(kind='bar')
plt.show()

df['owner'].value_counts().plot(kind='bar')
plt.show()

plt.hist(df['km_driven'], bins=30)
plt.show()

df['car_age'] = 2024 - df['year']
plt.hist(df['car_age'], bins=20)
plt.show()

plt.scatter(df['km_driven'], df['selling_price'])
plt.show()
