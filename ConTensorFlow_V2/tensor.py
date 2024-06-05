import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import tensorflow as tf 

#path="Mangoe_training.xlsx"
#path="training_percentages.xlsx"
#path="training_percentages_v2.xlsx"
path="order_training_percentages_v2.xlsx"
#"path="only_colors.xlsx"
raw_data=pd.read_excel(path, sheet_name="Sheet1")
dataset=raw_data.copy()

data_train = dataset.sample( frac=0.90 , random_state=0 )
data_test = dataset.drop( data_train.index )

#Entradas de entrenamiento -> data_train
#Salidas de entrenamiento -> train_output
train_output = data_train.pop( "exportable" )
print("Train Output: ")
print( train_output )
print("data TRain")
print(data_train)

#Entradas de test -> data_test
#Salidas de test -> test_output
test_output = data_test.pop( "exportable" )


train_stats = data_train.describe()
train_stats = train_stats.transpose()

print("Mean: " , train_stats["mean"] )
print( "Std: " , train_stats["std"]  )


def escala(x):
    return ( x-train_stats["mean"])/train_stats["std"]

train_input = data_train
test_input  = data_test

print("Dta train antess: ")
print( data_train )
print("----------------")
print("Data train escalada: ")
print( train_input )


modelo= tf.keras.Sequential([
    tf.keras.layers.Dense( 32 , input_shape=[4] , activation="relu" ),
    tf.keras.layers.Dense( 64 , activation="relu" ),
    tf.keras.layers.Dense( 32 , activation="relu" ),
    tf.keras.layers.Dense(1 , activation="sigmoid" )
])



op = tf.keras.optimizers.RMSprop(0.001)
#modelo.compile( optimizer=op , loss=["mae"] )
modelo.compile(optimizer=op, loss="binary_crossentropy", metrics=["accuracy"])
#modelo.compile(optimizer=op, loss="sparse_categorical_crossentropy", metrics=["accuracy"])  # Use sparse categorical crossentropy for binary classification
modelo.summary()

#Vamos a entrenar guardando el modelo en la variable history
history = modelo.fit( train_input , train_output , epochs=8000 )
#early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)
#history = modelo.fit(train_input, train_output, epochs=8000, validation_data=(test_input, test_output) )

#========== Tests con el 20% ==========//
print("Entradas: \n" , data_test )
output_Est = modelo.predict( test_input )

df = pd.DataFrame({ "Reales" : test_output }) 
df["Estimados"] = output_Est
print(df)

plt.scatter( test_output , output_Est )
plt.xlabel("Valores Reales")
plt.ylabel("Valores Estimados")

plt.grid()
plt.show()


#-------- grafica de errores por cada epoca --------//
train_mae = history.history["loss"]
epochs = range( 1 , len( train_mae ) + 1 )
plt.plot( epochs , train_mae )
plt.xlabel("Épocas")
plt.ylabel("loss")
plt.title("Loss vs Épocas")
plt.grid()
plt.show()

""" df=pd.DataFrame({ "area_spot":[2453.50] , "weighut": [52000] , "red_area":[120.0] , "green_area":[28908] , "yellow_area":[31914.0]  })
predic = modelo.predict( df )
print("La prediccion es: ", predic ) """

#============================ GUARDAMOS EL MODELO ======================
path_json1="model_trainig.json"
path_h5="model_trainig.h5"

with open( path_json1 , "w"  ) as json_file:
    modelo_json=modelo.to_json()
    json_file.write(modelo_json)

modelo.save_weights( path_h5 )
print("Se guardo el modelo!") 
