"""  
Tengo un archivo de Excel con los siguientes encabezados: 'weight', 'red_percent', 'green_percent', 'yellow_percent', necesito crear una nueva columna llamada 'exportable' con valores 0 y 1 , el valor 1 se agrega a la respectiva fila si 'weight' es mayor o igual a 440 y el valor de 'yellow_percent' esta entre 0 y 6. Sino el valor  de 'exportable' es cero. genera un nuevo excel con el nombre 'five_result.xlsx'

"""

import pandas as pd

# Read the Excel file
#df = pd.read_excel('training_data_five.xlsx')
#df = pd.read_excel('datos_no_vistos.xlsx')
df = pd.read_excel('datos_no_vistos_cap_4.xlsx')

# Function to determine exportable value
def determine_exportable(row):
    """ if row['red_percent'] == 0: #No hay rojo es decir los verde amarelo no van!
        return 0
    elif row['red_percent'] == 0 and row['yellow_percent'] == 0: #puro verde no van!
        return 0
    elif row['weight'] >= 440 and 0 <= row['yellow_percent'] <= 6:
        return 1
    else:
        return 0 """
    
    if row['red_percent'] == 0 and row['yellow_percent'] == 0: #puro verde no van!
        return 0
    elif row['weight'] >= 440 and 0 <= row['yellow_percent'] <= 6:
        return 1
    else:
        return 0

# Apply the function to create the 'exportable' column
df['exportable'] = df.apply(determine_exportable, axis=1)

# Save the modified DataFrame to a new Excel file
df.to_excel('new_no_vistos.xlsx', index=False)
#df.to_excel('five_result.xlsx', index=False)