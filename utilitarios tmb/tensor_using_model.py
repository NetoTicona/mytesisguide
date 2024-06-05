import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import tensorflow as tf 

path_json = "carrera_32_64_32_1.json" #Esta God
path_h5 = "carrera_32_64_32_1.h5"

with open(path_json, "r") as json_file:
    loaded_model_json = json_file.read()

loaded_model = tf.keras.models.model_from_json(loaded_model_json)
loaded_model.load_weights(path_h5)
path="fisty_selecteds.xlsx"

raw_data=pd.read_excel(path, sheet_name="Sheet1")
dataset=raw_data.copy()
data_train = dataset.sample( frac=0.0001 , random_state=0 )
data_test = dataset.drop( data_train.index )
data_test_copy = data_test.copy()
test_output = data_test.pop( "exportable" )

test_input = data_test

output_Est = loaded_model.predict( test_input )

df = pd.DataFrame({ "Reales" : test_output }) 
#df["weights"] = weights
df["Estimados"] = output_Est
print(df)

plt.scatter( test_output , output_Est )
plt.xlabel("Valores Reales")
plt.ylabel("Valores Estimados")

plt.grid()
plt.show()