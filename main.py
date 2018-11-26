# ISS Tracker uses the open notify api to plot the coordinates of the International
# Space Station
# Author: Richard Williams

import json
import urllib.request
import time
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

print("Spaceflight Tracker\n")

# Optain information for the astronauts in space
def get_people_in_space():
    temp = urllib.request.urlopen('http://api.open-notify.org/astros.json')
    astros = json.loads(temp.read())
    return astros

def get_iss_coordinates():
    """ Returns a tuple containing (time, lat, lon) using the """
    temp = urllib.request.urlopen('http://api.open-notify.org/iss-now.json')
    iss_now = json.loads(temp.read())
    iss_position = iss_now['iss_position']
    time = iss_now['timestamp']
    lat = iss_position['latitude']
    lon = iss_position['longitude']
    return (time, lat, lon)

def print_iss_coords(i):
    t = time.gmtime(int(iss_coords[0]))
    print("\nISS Coordinates")
    print("Date: {}-{}-{}".format(t.tm_year, t.tm_mon, t.tm_mday))
    print("Time: {}:{:02.0f}:{:02.0f}".format(t.tm_hour, t.tm_min, t.tm_sec))
    print("Latitude: ", iss_coords[1])
    print("Longitude: ", iss_coords[2])

def check_overhead():

    iss_position = get_iss_coordinates()


iss_coords = get_iss_coordinates()
lat = float(iss_coords[1])
lon = float(iss_coords[2])
t = time.gmtime(int(iss_coords[0]))
# tkinter gui
root = tk.Tk()
root.wm_title("ISS Tracker")

fig = Figure(figsize=(6,4), dpi = 400)

ax = fig.add_axes([0.01, 0.01, 0.98, 0.98], projection = ccrs.PlateCarree())
ax.plot(lat,lon, marker = 'o', markersize=3, color='red')
ax.set_global()
ax.stock_img()
ax.set_title("ISS Coordinates at {}:{:02.0f}:{:02.0f}".format(t.tm_hour, t.tm_min, t.tm_sec))

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

button = tk.Button(master=root, text='Quit', command=sys.exit)
button.pack(side=tk.BOTTOM)

tk.mainloop()
