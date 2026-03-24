from airport import *
import matplotlib.pyplot as plt

airport = Airport("LEBL", 41.297445, 2.0832941)
SetSchengen(airport)
PrintAirport(airport)
LoadAirports("Airports.txt")
fig = PlotAirports(LoadAirports('Airports.txt'))
fig.show()
input()
MapAirports(LoadAirports('Airports.txt'))