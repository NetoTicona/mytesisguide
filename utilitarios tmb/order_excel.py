import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import tensorflow as tf 

# Your existing code
path = "five_result.xlsx"
raw_data = pd.read_excel(path, sheet_name="Sheet1")
dataset = raw_data.copy()

# Sort rows based on the 'exportable' column
dataset.sort_values(by='exportable', inplace=True)

# Save the sorted DataFrame to a new Excel file
output_path = "order_training_percentages_v2_2.xlsx"
dataset.to_excel(output_path, index=False)