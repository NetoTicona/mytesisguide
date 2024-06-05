import numpy as np
import matplotlib.pyplot as plt

seed = 50
rand_state = 50

rand = np.random.RandomState(seed)

dist_list = ['uniform' , 'normal' , 'exponential' , 'lognormal' , 'chisquare' , 'beta' ]
param_list = ['-1.1' '0.1' , '1' , '0.1' ,'2' ,'0.5' , '0.9'  ]
colors_list = [ 'purple' , 'fuchsia' , 'blue' , 'black' , 'red' , 'green' ]
fig,ax = plt.subplots( nrows=2 , ncols=3 , figsize=(12,7) )
plt_ind_list = np.arange(6) + 231

for dist , plt_ind , param , colors in zip( dist_list , plt_ind_list , param_list , colors_list ):
    x
