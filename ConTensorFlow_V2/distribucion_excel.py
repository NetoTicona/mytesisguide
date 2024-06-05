import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import tensorflow as tf 

#path="Mangoe_training.xlsx"
path="training_percent_real.xlsx"
#path="only_colors.xlsx"
raw_data=pd.read_excel(path, sheet_name="Sheet1")
dataset=raw_data.copy()
dataset_coy = raw_data.copy()

data_train = dataset.sample( frac=0.8 , random_state=0 )
data_test = dataset.drop( data_train.index )

#Entradas de entrenamiento -> data_train
#Salidas de entrenamiento -> train_output
#train_output = data_train.pop( "area_total" )
weight = dataset_coy.pop( "weight" )
red_values = dataset_coy.pop( "red_percent" )
green_values = dataset_coy.pop( "green_percent" )
yellow_values = dataset_coy.pop( "yellow_percent" )


print("Train Output: ")
#print( train_output )
print("data TRain")
print(data_train)

#Entradas de test -> data_test
#Salidas de test -> test_output
#test_output = data_test.pop( "area_total" )


train_stats = data_train.describe()
train_stats = train_stats.transpose()

print( "mean: ", train_stats["mean"] )
print( "STd: " ,  train_stats["std"] )

weight.hist(bins=20, figsize=(15, 10))
plt.suptitle('Histograms of Features', fontsize=16)
plt.show()

# Alternatively, you can draw KDE plots for each feature
weight.plot(kind='kde', figsize=(15, 10))
plt.suptitle('KDE Plots of Features', fontsize=16)
plt.show()