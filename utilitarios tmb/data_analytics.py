""" 2. Anasiis del data frame """
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator , TransformerMixin
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, make_scorer

X_data = pd.read_csv('fisty_selecteds.csv')
#print( X_data )

""" Variables numericas y categorias """

var_num = [ i for i in X_data.columns if X_data.dtypes[i] != 'object' ]
var_num.remove('exportable')
var_cat = [ i for i in X_data.columns if X_data.dtypes[i] == 'object' ]

print("V. Númericas: ", len(var_num) )
print("V. Categoricas: ", len(var_cat) )

""" 4. Conteo de data faltante """
missing_data = X_data.isnull().sum()
missing_data = missing_data[ missing_data > 0 ]
missing_data.sort_values( inplace=True , ascending=False )

print( missing_data )
""" -----------3 ANALSIS DE CARACTERISTICAS------------ """
""" Analsiis de la salida """
y = X_data['exportable']
print(y.describe())

""" distribucion """
#y.plot.hist()

""" Aalsisi de las carateristicas numericas """
""" Graficamos histogramsa de todas las caracteristicas """
import seaborn as sns
f = pd.melt( X_data , value_vars=var_num )
g = sns.FacetGrid( f , col="variable" , col_wrap=3 , sharex=False , sharey=False )
g = g.map( sns.histplot , "value" , kde=True )


""" Caracteristicas categorias """
# --- #

""" Diagrama de cajas """
""" Doagrama objetico con variable categoriaca """

""" Anañsis de variable numericas """
""" Mediante el uso de la materiz de correlacon """
mat_corr = X_data[var_num].corr()
plt.figure( 1 , figsize=(4,4) )
sns.heatmap( mat_corr , vmax=.85 , square=True )
#plt.show()

""" DEbemos  normalizar los datos """
""" Opcional corregir distribucion """
""" Eliminar clases con pocos datos """

""" ------------- CLASE 5- -------------- """
""" PREPROCESAMIENTO """
x_array = X_data.values[:,:-1]
y_array = X_data.values[:,-1]
print("X:", x_array.shape )
print("Y:", y_array.shape )

""" Elimianr carterisicas:no es necesario ya que vimos el diagrama heat """ 
class RemoveFeatures( BaseEstimator , TransformerMixin ):
    def __init__(self):
        self.rm_index = []

    def fit( self , x , y=None ):
        return self

    def transform( self , x , y=None ):
        x = np.delete( x , self.rm_index , axis=1 )
        return x

remf = RemoveFeatures()
x_array1 = remf.fit_transform(x_array)
print( "x_Arra1Shape: ", x_array1.shape )



""" Valores faltantes: pones el floro del word """

class MyInputer(BaseEstimator , TransformerMixin ):
    def __init__(self):
        self.num_index = []
        self.cat_index = []

        self.cat_imputer = SimpleImputer( strategy="most_frequent" )
        self.num_imputer = SimpleImputer( strategy="mean" )

    def fit( self , x , y=None ):
        self.cat_imputer.fit( x[:,self.cat_index] )
        self.num_imputer.fit( x[:,self.num_index] )
        return self

    def transform( self , x , y=None ):
        x[:,self.cat_index ] = self.cat_imputer.transform( x[: , self.cat_index ] )
        x[:,self.num_index ] = self.num_imputer.transform(x[:,self.num_index])
        return x

""" myimp = MyInputer()
x_array2 = myimp.fit_transform(x_array1)
print( x_array2.shape ) """
x_array2 = x_array1



""" Caracteristicas CAtegorias: No Hay """
""" Normalizacion: No estamos modificando la distribucion ya que una tansformacion lineal """
sscaler = StandardScaler()
print( x_array2[0] )
x_array3 = x_array2.copy()
x_array3 = sscaler.fit_transform( x_array2 )
print( x_array3[0] )

""" Caracteristicas mas importantes , numericas """
""" Ya estan seecionadas """

""" MODELOS """
""" --------------- REGRESION LINEAL GAAAaaaa--------------- """
""" lr = LinearRegression()
lr.fit( x_array3 , y_array )
print(lr.score( x_array3 , y_array  ) ) #0.3019 :/ """

from sklearn.neural_network import MLPClassifier

# Define the model
modelo = MLPClassifier(hidden_layer_sizes=(32, 64, 32), activation='relu', solver='adam', max_iter=1000)

# Train the model
modelo.fit(x_array3, y_array )
train_predictions = modelo.predict(train_input)
train_accuracy = accuracy_score(train_output, train_predictions)
print("Train Accuracy:", train_accuracy)

# Predictions on test set
test_predictions = modelo.predict(test_input)
test_accuracy = accuracy_score(test_output, test_predictions)
print("Test Accuracy:", test_accuracy)






""" Validacion cruzada """
""" scorer = make_scorer( mean_squared_error , greater_is_better=False )
mse = cross_val_score( lr , x_array3 , y_array , scoring=scorer , cv=10 )
rmse = np.sqrt( -mse ).mean()
print("RMSE: " , rmse ) """


""" METRICAS DE CLASIFICAION """
""" Accuracy  , preciios , recall vasel6 1:47:06 """
""" Curva Rock """
""" curva de apredizaje """

