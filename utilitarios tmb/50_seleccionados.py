"Tengo un archivo de Excel con los siguientes encabezados: 'weight', 'red_percent', 'green_percent', 'yellow_percent' y 'exportable'. tengo 870 filas , ahora necesto que se escojan aleatoriamente  50 filas cuyo valor 'exportable' sea 1 y otros 50 cuyo valor de  'exportable' sea 0"

import pandas as pd

# Load the Excel file into a DataFrame
df = pd.read_excel('order_training_percentages_v2.xlsx')

# Select 50 rows where 'exportable' is 0
exportable_zero = df[df['exportable'] == 0].sample(n=50, random_state=1)

# Select another 50 rows where 'exportable' is 1
exportable_one = df[df['exportable'] == 1].sample(n=50, random_state=1)

# Concatenate the two sets of selected rows
selected_rows = pd.concat([exportable_zero, exportable_one])

# Write the selected rows to a new Excel file
selected_rows.to_excel('fisty_selecteds.xlsx', index=False)
selected_rows.to_csv('fisty_selecteds.csv', index=False)