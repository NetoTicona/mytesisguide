import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from sklearn.metrics import roc_curve, auc , confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import seaborn as sns




path_json = "carrera_32_64_32_1.json" #Esta God
path_h5 = "carrera_32_64_32_1.h5"

with open(path_json, "r") as json_file:
    loaded_model_json = json_file.read()
loaded_model = tf.keras.models.model_from_json(loaded_model_json)
loaded_model.load_weights(path_h5)

#path="fisty_selecteds.xlsx"
#path="new_no_vistos.xlsx"
path="new_no_vistos_haydee.xlsx"
#path="order_training_percentages_v2.xlsx"


raw_data=pd.read_excel(path,sheet_name=0)
dataset=raw_data.copy()
dataset.head(8)

data_train = dataset.sample(frac=0.0001, random_state=0)
data_test = dataset.drop(data_train.index)

train_output = data_train.pop("exportable")
test_output = data_test.pop("exportable")

train_input = data_train
test_input  = data_test



""" Trainig xd """
""" op = tf.keras.optimizers.RMSprop(0.00001)
#modelo.compile( optimizer=op , loss=["mae"] )
loaded_model.compile(optimizer=op, loss="binary_crossentropy", metrics=["accuracy"])

loaded_model.summary()
history = loaded_model.fit(train_input, train_output, epochs=5000) """



#========== Tests con el 20% ==========//
print("Entradas: \n" , data_test )
output_Est = loaded_model.predict( test_input )

threshold = 0.5
predicted_classes = (output_Est >= threshold).astype(int)

df = pd.DataFrame({ "Reales" : test_output })
df["Estimados"] = predicted_classes
print(df)

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

# Plot learning curve (not traditional learning curve, as we lack the training phase)
# Instead, we can plot the distribution of the predicted output against the real output
plt.figure()
plt.scatter(test_output, output_Est)
plt.xlabel("Real Values")
plt.ylabel("Estimated Values")
plt.title("Learning Curve (Distribution of Predicted vs Real Values)")
plt.grid()
plt.show()


# Compute confusion matrix
cm = confusion_matrix(test_output, (output_Est >= 0.5).astype(int))

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Valores Estimados')
plt.ylabel('Valores Reales')
plt.title('Matriz de Confusión')
plt.show()


plt.scatter( test_output , output_Est )
plt.xlabel("Valores Reales")
plt.ylabel("Valores Estimados")
plt.grid()
plt.show()

output_excel_path = "output_results.xlsx"
df.to_excel(output_excel_path, index=False)
























##Guardar una red neuronal en archivos *.json y *.h5
""" path_json="carrera_32_64_32_1_xd.json"
path_h5="carrera_32_64_32_1_xd.h5"
with open(path_json,"w") as json_file:
  modelo_json=loaded_model.to_json()
  json_file.write(loaded_model_json)
json_file.close()
loaded_model.save_weights(path_h5)
print("Modelo Guardado!!!") """