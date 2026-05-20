from airport import *
import matplotlib.pyplot as plt
import os

if __name__ == "__main__":
    print("="*60)
    print("TEST VERSIÓN 1 - AIRPORT MANAGEMENT")
    print("="*60)
    
    # ==========================================
    # 1. Test crear aeropuerto y SetSchengen
    # ==========================================
    print("\n📌 1. Probando Airport() y SetSchengen()")
    print("-" * 40)
    
    airport1 = Airport("LEBL", 41.297445, 2.0832941)
    SetSchengen(airport1)
    PrintAirport(airport1)
    
    airport2 = Airport("KJFK", 40.641766, -73.780968)
    SetSchengen(airport2)
    PrintAirport(airport2)
    
    # ==========================================
    # 2. Test LoadAirports
    # ==========================================
    print("\n📌 2. Probando LoadAirports('Airports.txt')")
    print("-" * 40)
    
    airports = LoadAirports("Airports.txt")
    print(f"   ✅ Aeropuertos cargados: {len(airports)}")
    
    if airports:
        print(f"   Primer aeropuerto: {airports[0].icaoCode}")
        print(f"   Último aeropuerto: {airports[-1].icaoCode}")
        
        # Verificar que LEBL está
        lebl = None
        for airp in airports:
            if airp.icaoCode == "LEBL":
                lebl = airp
                break
        
        if lebl:
            print(f"   ✅ LEBL encontrado: lat={lebl.latitude}, lon={lebl.longitude}")
        else:
            print("   ⚠️ LEBL no encontrado en el archivo")
    
    # ==========================================
    # 3. Test AddAirport y RemoveAirport
    # ==========================================
    print("\n📌 3. Probando AddAirport() y RemoveAirport()")
    print("-" * 40)
    
    count_before = len(airports)
    
    # Añadir aeropuerto nuevo
    test_airport = Airport("TEST", 40.0, -80.0)
    result = AddAirport(airports, test_airport)
    print(f"   AddAirport(TEST): {'✅ Añadido' if result else '❌ Falló'}")
    print(f"   Aeropuertos: {count_before} → {len(airports)}")
    
    # Intentar añadir duplicado
    result = AddAirport(airports, test_airport)
    print(f"   AddAirport(TEST duplicado): {'✅ No añadido' if not result else '❌ Debería fallar'}")
    
    count_before = len(airports)

    # Eliminar aeropuerto
    result = RemoveAirport(airports, "TEST")
    print(f"   RemoveAirport(TEST): {'✅ Eliminado' if result else '❌ Falló'}")
    print(f"   Aeropuertos: {count_before} → {len(airports)}")
    
    # ==========================================
    # 4. Test SaveSchengenAirports
    # ==========================================
    print("\n📌 4. Probando SaveSchengenAirports()")
    print("-" * 40)
    
    SaveSchengenAirports(airports, "SchengenAirports.txt")
    
    if os.path.exists("SchengenAirports.txt"):
        with open("SchengenAirports.txt", "r") as f:
            lines = f.readlines()
        print(f"   ✅ Archivo creado: {len(lines)} aeropuertos Schengen guardados")
    else:
        print("   ❌ Error: No se creó el archivo")
    
    # ==========================================
    # 5. Test PlotAirports
    # ==========================================
    print("\n📌 5. Probando PlotAirports()")
    print("-" * 40)
    
    fig = PlotAirports(airports, "Test - Schengen vs No Schengen")
    print("   ✅ Gráfico creado (se cierra en 10 segundos)")
    plt.ion()
    plt.show(block=False)
    plt.pause(10)
    plt.close()
    
    # ==========================================
    # 6. Test MapAirports
    # ==========================================
    print("\n📌 6. Probando MapAirports()")
    print("-" * 40)
    
    MapAirports(airports)
    
    if os.path.exists("Airports_Points.kml"):
        print("   ✅ Archivo KML creado: Airports_Points.kml")
    else:
        print("   ❌ Error: No se creó el archivo KML")
    
    # ==========================================
    # RESULTADO FINAL
    # ==========================================
    print("\n" + "="*60)
    print("🎉 TEST VERSIÓN 1 COMPLETADO")
    print("="*60)
    print("\n✅ Si no has visto errores, todas las funciones funcionan correctamente.")
    print("✅ Archivos creados: SchengenAirports.txt, Airports_Points.kml")