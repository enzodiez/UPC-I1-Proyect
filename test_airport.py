from airport import *

airport = Airport("LEBL", 41.297445, 2.0832941)
SetSchengen(airport)
PrintAirport(airport)
LoadAirports("Airports.txt")
PlotAirports(LoadAirports('Airports.txt'))
MapAirports(LoadAirports('Airports.txt'))