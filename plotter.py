import pandas as pd
import matplotlib.pyplot as plt

FILENAME = "measurement.csv" #вводим файл, который хотим проанализировать

data = pd.read_csv(FILENAME)

print(data.head())
print()
print(f"Количество измерений: {len(data)}")

plt.figure(figsize=(14, 7))
plt.plot(
    data["time_us"],
    data["A0"],
    label="A0"
)

plt.plot(
    data["time_us"],
    data["A1"],
    label="A1"
)

plt.xlabel("Время, мкс")
plt.ylabel("ADC")

plt.title("Аналоговые сигналы A0 и A1")

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()