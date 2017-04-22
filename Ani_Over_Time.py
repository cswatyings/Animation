import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.basemap import Basemap

#%matplotlib inline


# Sample it down to only the DXC
lon_min, lon_max = -77.219342, -76.845121
lat_min, lat_max = 38.792209, 39.020434

bat = pd.read_csv("/Users/SiweiChen/Downloads/Batching.csv")
bat = bat.drop(['Quote Requests To Location','len'],axis = 1)

bat.columns = ['lat','lon','zip','hour','part','date','name','vendor','count']
time_groups = bat.groupby('hour')



dc1 = bat.groupby(by = ['zip','hour'])['count'].sum().reset_index()
dc1['count'] = dc1['count']/ 90.
dc2 = bat.groupby(by = ['zip','hour'])['lat','lon'].mean().reset_index()
dc2['count'] = dc1['count']
dc2 = dc2[dc2['count'] > .1]
dc2.head()



for i in range(24):
    dc2.loc[-i] = np.array([0,time_insert[i],0,0,0])
    print time_insert[i]



###########################  MAIN   ANIMATION  #############################################################
fig = plt.figure(figsize=(15,15))
ax = fig.add_subplot(111)


m = map = Basemap(
    projection='merc', 
    llcrnrlon=lon_min, 
    llcrnrlat=lat_min,
    urcrnrlon=lon_max, 
    urcrnrlat=lat_max,
    resolution='h')

m.fillcontinents(color='#191919',lake_color='#000000') # dark grey land, black lakes
m.drawmapboundary(fill_color='#222222')  
# black background
m.drawcoastlines(linewidth= .7,color = 'white')
m.drawcountries(linewidth=0.3, color="white")
m.drawcounties(linewidth=0.2, color="white")
m.drawrivers(color = 'white')
m.drawmapboundary(color = 'white')
m.drawmeridians(np.arange(-78, -76.85, 0.15),color = 'white', labels=[0,1,0,1])
m.drawparallels(np.arange(38.6, 39.1, 0.1), color = 'white', labels=[1,0,0,1])
#m.drawmapscale()



x = dc3.get_group(12)['lon'].values
y = dc3.get_group(12)['lat'].values
x, y = m(0,0)
siz = dc3.get_group(12)['count'].values

point = m.scatter(x, y,s= 0,
                  alpha = 0.5, 
                  c = 'white',zorder = 10)


'''def init():
    point.set_data([], [])
    return point,'''

def animate(i):
    
    lon = dc3.get_group(i)['lon'].values
    lat = dc3.get_group(i)['lat'].values
    siz = dc3.get_group(i)['count'].values
    xs, ys = m(lon ,lat)
    #point = plt.scatter(xs, ys,c = 'white', s=siz *100,alpha = .5)
    point.set_offsets(np.dstack((xs, ys)))
    point.set_sizes(siz*700)
    plt.title('Washington DC Metro at: %2d:00' % (i))
    
    return point,

    

#    ani = animation.FuncAnimation(fig, update_plot, frames=xrange(numframes),
#                                  fargs=(color_data, scat))
    
'''def update(frame_number):
    current_year = START_YEAR + (frame_number % (LAST_YEAR - START_YEAR + 1))
    
    temp_markers = get_temp_markers(random_cities, current_year)
    xs, ys = map(temp_markers['lon'], temp_markers['lat'])

    scat.set_offsets(np.dstack((xs, ys)))
    scat.set_color(cmap(temp_markers['color']))
    scat.set_sizes(temp_markers['size'])
    
    year_text.set_text(str(current_year))'''

# # # Construct the animation, using the update function as the animation
# # # director.
ani = animation.FuncAnimation(fig, animate,
                              interval=800, frames=24, 
                              blit = False, repeat = False)    

#output = animation.FuncAnimation(plt.gcf(), animate, init_func=init, frames=24, interval=800, blit=False, repeat=False)

ani.save('~/DCMet_Zoom.gif', writer='imagemagick')
plt.show()
