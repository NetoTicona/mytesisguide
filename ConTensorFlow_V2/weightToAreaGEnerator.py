import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

""" seed = 50
rand_state = 50

rand = np.random.RandomState(seed)

dist_list = ['uniform' , 'normal' , 'exponential' , 'lognormal' , 'chisquare' , 'beta' ]
param_list = ['-1,1','0,1' , '1' , '0,1' ,'2' ,'0.5' , '0.9'  ]
colors_list = [ 'purple' , 'fuchsia' , 'blue' , 'black' , 'red' , 'green' ]
fig,ax = plt.subplots( nrows=2 , ncols=3 , figsize=(12,7) )
plt_ind_list = np.arange(6) + 231

for dist , plt_ind , param , colors in zip( dist_list , plt_ind_list , param_list , colors_list ):
    if dist == 'normal':
        # Generate 150 new data points with a normal distribution between 420 and 650
        x = rand.normal(loc=535, scale=50, size=150)
    else:
        x = eval('rand.' + dist + '(' + param + ', 5000)')

    plt.subplot(plt_ind)
    plt.hist(x,bins=50,color=colors)
    plt.title(dist)

fig.subplots_adjust( hspace=0.4 , wspace=.3 )
plt.suptitle('Muestreo de varias distribuciones' , fontsize=20 )
plt.show() """


""" seed = 65
rand_state = 50
rand = np.random.RandomState(seed)

data = rand.normal(loc=50, scale=20, size=248)  # Mean=50, Standard deviation=20
# Clip the data to ensure it falls within the range of 0 and 100
data = np.clip(data, 0, 100)
# Round the data to 0 decimal places
#data = np.round(data, decimals=0)
# Create a DataFrame
df = pd.DataFrame(data, columns=['Data'])
# Save the DataFrame to an Excel file
df.to_excel('gre_generated_data.xlsx', index=False) """



#------------------- Lognormal -------------------""
""" seed = 50
rand_state = 50
rand = np.random.RandomState(seed)

# Generate 248 data points with a lognormal distribution between 0 and 100
data = rand.lognormal(mean=0, sigma=1, size=248)

# Scale the data to fit between 0 and 100
data = data * 100 / data.max()

# Round the data to 0 decimal places
#data = np.round(data, decimals=0)

# Create a DataFrame
df = pd.DataFrame(data, columns=['Data'])

# Save the DataFrame to an Excel file
df.to_excel('red_generated_data.xlsx', index=False) """

#-------------- uniform --------**
""" seed = 50
rand_state = 50
rand = np.random.RandomState(seed)

# Generate 248 data points with a uniform distribution between 0 and 100
data = rand.uniform(low=0, high=100, size=248)

# Round the data to 0 decimal places
#data = np.round(data, decimals=0)

# Create a DataFrame
df = pd.DataFrame(data, columns=['Data'])

# Save the DataFrame to an Excel file
df.to_excel('generated_green_data.xlsx', index=False) """


#---------------- 3 columns nornal ---------------
seed_column1 = 62
seed_column2 = 13
seed_column3 = 26  # Using the same seed as before

# Create random number generators with specified seeds
rand_column1 = np.random.RandomState(seed_column1)
rand_column2 = np.random.RandomState(seed_column2)
rand_column3 = np.random.RandomState(seed_column3)

# Generate random values for each column with normal distributions
data_column1 = rand_column1.normal(loc=50, scale=20, size=(int(0.5 * 200),))
data_column2 = rand_column2.normal(loc=50, scale=20, size=(int(0.5 * 200),))
data_column3 = rand_column3.normal(loc=50, scale=20, size=(int(0.5 * 200),))

# Clip the data to ensure it falls within the range of 0 and 100

data_column1 = np.clip(data_column1, 0, 50)
data_column2 = np.clip(data_column2, 0, 50)
data_column3 = np.clip(data_column3, 0, 50)

# Stack the columns together to form a 2D array
data_stacked = np.column_stack((data_column1 , data_column2, data_column3))

# Normalize each row so that the sum is 100 percent
data_normalized = data_stacked / data_stacked.sum(axis=1, keepdims=True) * 70

# Round the normalized data to 6 decimal places
data_rounded = np.round(data_normalized, decimals=8)

# Create a DataFrame
df = pd.DataFrame(data_rounded, columns=[ 'Column1', 'Column2', 'Column3'])

# Save the DataFrame to an Excel file
df.to_excel('generated_greenand_Red_data.xlsx', index=False)


#-------------------- pesos ----------------------
""" seed = 66
rand_state = 50

rand = np.random.RandomState(seed)

# Generate 248 data points with a normal distribution between 340 and 620
data = rand.normal(loc=480, scale=70, size=50 )
data = np.round(data, decimals=0)

# Create a DataFrame
df = pd.DataFrame(data, columns=['Data'])

# Save the DataFrame to an Excel file
df.to_excel('pesos_data.xlsx', index=False) """


#------------------ pesos 429 y 450 ------------ #
""" seed = 50
rand_state = 50

rand = np.random.RandomState(seed)

# Generate 248 data points with a uniform distribution between 429 and 451
data = rand.uniform(low=435, high=445, size=100)

# Round the data to 0 decimal places
data = np.round(data, decimals=0)

# Create a DataFrame
df = pd.DataFrame(data, columns=['Data'])

# Save the DataFrame to an Excel file
df.to_excel('pesos_data.xlsx', index=False) """