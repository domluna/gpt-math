import pandas as pd
import os
import matplotlib.pyplot as plt
import pathlib
import json

# Path to the directory containing the data files
current_directory = pathlib.Path(__file__).parent
data_path = current_directory / "data"


# Function to calculate accuracy for a given CSV file
def calculate_accuracy(data: pd.DataFrame) -> float:
    predictions = []
    for _, row in data.iterrows():
        prediction = int(row["input_a"]) + int(row["input_b"]) == int(row["output"])
        predictions.append(prediction)
    accuracy = sum(predictions) / len(predictions)
    return accuracy


def calculate_carry_accuracy(data: pd.DataFrame) -> tuple[float, float]:
    carry_predictions = []
    digits_predictions = []
    for i, row in data.iterrows():
        a = int(row["input_a"])
        b = int(row["input_b"])
        p1 = (a + b) // 10 == int(row["carry"])
        p2 = (a + b) % 10 == int(row["output"])
        if not p1:
            print(f"Carry prediction failed for row {i}: {a} + {b} = {a+b}")
        if not p2:
            print(f"Digits prediction failed for row {i}: {a} + {b} = {a+b}")
        carry_predictions.append(p1)
        digits_predictions.append(p2)
    carry_accuracy = sum(carry_predictions) / len(carry_predictions)
    digits_accuracy = sum(digits_predictions) / len(digits_predictions)
    return digits_accuracy, carry_accuracy


# Read each file and calculate its accuracy
accuracy_dict = {}
for file in os.listdir(data_path):
    if file.endswith(".csv") and "carry" not in file:
        file_path = data_path / file
        data = pd.read_csv(file_path)
        accuracy = calculate_accuracy(data)
        accuracy_dict[file] = accuracy

# Sort the experiments by accuracy in descending order
sorted_accuracies = {
    k: v
    for k, v in sorted(accuracy_dict.items(), key=lambda item: item[1], reverse=True)
}

# dump this to a file
with open(current_directory / "results.json", "w") as file:
    json.dump(sorted_accuracies, file, indent=4)

with open(current_directory / "carry_results.json", "w") as file:
    data = pd.read_csv(data_path / "single_digit_carry.csv")
    digits_accuracy, carry_accuracy = calculate_carry_accuracy(data)
    accuracies = {"digits_accuracy": digits_accuracy, "carry_accuracy": carry_accuracy}
    json.dump(accuracies, file, indent=4)

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(range(len(sorted_accuracies)), list(sorted_accuracies.values()), align="center")
plt.xticks(
    range(len(sorted_accuracies)),
    list(sorted_accuracies.keys()),
    rotation=45,
    ha="right",
)
plt.xlabel("Experiments")
plt.ylabel("Accuracy")
plt.title("Accuracy of Addition Experiments")
plt.tight_layout()

# Save the plot to a file
save_path = current_directory / "results.png"
plt.savefig(save_path)
