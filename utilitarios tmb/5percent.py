""" prompt: "Tengo un archivo de Excel con los siguientes encabezados: 'weight', 'red_percent', 'green_percent', 'yellow_percent'. En cada fila, necesito evaluar el valor de 'yellow_percent'. Si es igual a 0, debo verificar los valores correspondientes de 'red_percent' y 'green_percent'. La suma de ambos no debe superar el 95. Si la suma no supera el 95, entonces debo reemplazar el 0por  un valor aleatorio entre 0 y 5 a 'yellow_percent' utilizando la función 'rand.normal', la cual sigue una distribución normal. El número aleatorio generado debe tener 8 decimales. Luego, debo repetir este proceso para todas las filas del archivo Excel y realizar los cambios mencionados, finalmente generando un nuevo archivo Excel con el nombre 'training_data_five.xlsx'. """
import pandas as pd
import numpy as np

# Read the Excel file
df = pd.read_excel('training_percentages_v2.xlsx')

# Iterate through each row
for index, row in df.iterrows():
    yellow_percent = row['yellow_percent']
    red_percent = row['red_percent']
    green_percent = row['green_percent']
    
    # Check if yellow_percent is 0
    if yellow_percent == 0:
        # Check if sum of red_percent and green_percent doesn't exceed 95
        if (red_percent + green_percent) <= 95:
            # Generate random value between 0 and 5 from normal distribution
            random_value = abs(np.random.normal(loc=0, scale=1)) * 5
            random_value = round(random_value, 8)  # Round to 8 decimal places
            # Replace 0 with random value
            df.at[index, 'yellow_percent'] = random_value

# Save the modified DataFrame to a new Excel file
df.to_excel('training_data_five.xlsx', index=False)