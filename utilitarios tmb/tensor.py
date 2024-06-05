import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import tensorflow as tf 
import seaborn as sns
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

path="data_for_training.xlsx"
raw_data=pd.read_excel(path, sheet_name="Sheet1")
dataset=raw_data.copy()
data_train = dataset.sample( frac=0.80 , random_state=0 )
data_test = dataset.drop( data_train.index )

train_output = data_train.pop( "exportable" )
test_output = data_test.pop( "exportable" )
train_stats = data_train.describe()
train_stats = train_stats.transpose()

train_input = data_train
test_input  = data_test

modelo= tf.keras.Sequential([
    tf.keras.layers.Dense( 32 , input_shape=[4] , activation="relu" ),
    tf.keras.layers.Dense( 64 , activation="relu" ),
    tf.keras.layers.Dense( 32 , activation="relu" ),
    tf.keras.layers.Dense(1 , activation="sigmoid" )
])


#op = tf.keras.optimizers.RMSprop(0.001)

modelo.compile(optimizer='adam', loss="binary_crossentropy", metrics=["accuracy"])

modelo.summary()


history = modelo.fit( train_input , train_output , epochs=100000 )
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

# grafico Roc
fpr, tpr, thresholds = roc_curve(test_output, output_Est)
roc_auc = auc(fpr, tpr)
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.show()


# curva de aprendizaje
plt.figure()
plt.scatter(test_output, output_Est)
plt.xlabel("Real Values")
plt.ylabel("Estimated Values")
plt.title("Learning Curve (Distribution of Predicted vs Real Values)")
plt.grid()
plt.show()