import pandas as pd
import os
import matplotlib.pyplot as plt
import pathlib

# Path to the directory containing the data files
current_directory = pathlib.Path(__file__).parent
data_path = current_directory / "data"

# Function to calculate accuracy for a given CSV file
def calculate_accuracy(file_path):
    data = pd.read_csv(file_path)
    correct_predictions = sum(data['input_a'] + data['input_b'] == data['output'])
    total_predictions = len(data)
    accuracy = correct_predictions / total_predictions
    return accuracy

# Read each file and calculate its accuracy
accuracy_dict = {}
for file in os.listdir(data_path):
    if file.endswith(".csv"):
        file_path = os.path.join(data_path, file)
        accuracy = calculate_accuracy(file_path)
        accuracy_dict[file] = accuracy

# Sort the experiments by accuracy in descending order
sorted_accuracies = {k: v for k, v in sorted(accuracy_dict.items(), key=lambda item: item[1], reverse=True)}

print(sorted_accuracies)

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(range(len(sorted_accuracies)), list(sorted_accuracies.values()), align='center')
plt.xticks(range(len(sorted_accuracies)), list(sorted_accuracies.keys()), rotation=45, ha="right")
plt.xlabel('Experiments')
plt.ylabel('Accuracy')
plt.title('Accuracy of Addition Experiments')
plt.tight_layout()

# Save the plot to a file
save_path = current_directory / "results.png"
plt.savefig(save_path)
