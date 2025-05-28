import numpy as np


# === JOUW INPUT ===
h_0 = 1.0   # Hoogte van loslaten (in meter)
h_1 = 0.8   # Hoogte na stuiter (in meter)
radius = 0.0043     # Straal van de bal in meters
mass = 0.0367       # Massa van de bal in kg

def calculate_air_resistance_force(v, radius=radius):
    """
    Bereken luchtweerstandskracht: F_d = ½ ρ v² C_d A
    """
    rho = 1.225  # luchtdichtheid in kg/m³
    C_d = 0.47   # drag coefficient voor bol
    A = np.pi * radius**2  # frontaal oppervlak
    return 0.5 * rho * v**2 * C_d * A

def simulate_fall_and_rise(h_0, h_1, mass=mass, radius=radius, g=9.81, tol=1e-7, max_iter=10000):
    """
    Simuleer de val en de stuiter van de bal, en bereken het verlies aan energie.
    Hierbij wordt iteratief de luchtweerstand in rekening gebracht op zowel de val- als de stijgingsbeweging.
    """
    dt = 0.001  # tijdstap
    h = h_0
    v = 0  # snelheid bij het begin
    E_lucht = 0  # energieverlies door luchtweerstand

    # Simuleer de val met luchtweerstand
    while h > 0:
        F_d = calculate_air_resistance_force(v, radius)
        a = g - (F_d / mass)  # versnelling door zwaartekracht en luchtweerstand
        v += a * dt  # update snelheid
        h -= v * dt  # update hoogte
        E_lucht += F_d * abs(v * dt)  # voeg luchtweerstand toe aan totaal energieverlies

    # Snelheid bij impact
    v_impact = np.sqrt(2 * g * h_0)  # snelheid zonder luchtweerstand (idealistisch)

    # 2. Bepaal de kinetische energie bij de impact (met luchtweerstand meegerekend)
    E_kin_impact = 0.5 * mass * v_impact**2

    # 3. Iteratieve aanpak voor het berekenen van de verloren energie bij de botsing (x)
    x = 0  # beginwaarde voor het verlies door botsing
    iter_count = 0

    while iter_count < max_iter:
        # Verlies door botsing x: de kinetische energie na de botsing
        E_kin_after_bounce = E_kin_impact - x

        # Bereken de snelheid na de botsing
        v_bounce = np.sqrt(2 * E_kin_after_bounce / mass)

        # Simuleer de stijging met luchtweerstand
        h_calculated = 0
        E_lucht_iter = 0  # herberekening luchtweerstand tijdens stijging

        while v_bounce > 0.0:  # stop de simulatie als snelheid nul is
            F_d = calculate_air_resistance_force(v_bounce, radius)
            a = -g - (F_d / mass)  # versnelling door zwaartekracht en luchtweerstand
            v_bounce += a * dt  # update snelheid
            h_calculated += v_bounce * dt  # update hoogte

            E_lucht_iter += F_d * abs(v_bounce * dt)  # voeg luchtweerstand toe aan energieverlies

        # Vergelijk de berekende hoogte met de verwachte hoogte h_1
        if abs(h_calculated - h_1) < tol:
            break  # stop iteratie als de hoogte goed is

        # Pas de waarde van x aan (verhoog of verlaag afhankelijk van de berekende hoogte)

        # Deze vergrotingsfactor zorgt ervoor dat als het verschil hoog is dat de stappen groter worden
        vergrotings_factor = (1 + abs(h_calculated - h_1))
        if h_calculated > h_1:
            x += 0.0001 * vergrotings_factor  # verhoog verlies
        else:
            x -= 0.0001 * vergrotings_factor  # verlaag verlies
        

        iter_count += 1
    
    # Bereken het totale energieverlies door luchtweerstand en botsing
    E_botsing = E_kin_impact - E_kin_after_bounce
    E_verlies_totaal = E_botsing + E_lucht + E_lucht_iter


    print(f"""
energie begin impact in J   : {E_kin_impact} Joule
energie na impact in J      : {E_kin_after_bounce} Joule

verloren bij impact in J    : {E_botsing} Joule
verloren bij impact in %    : {(E_botsing / E_kin_impact) * 100:.4f} %
verloren aan luchtweerstand : {(E_lucht + E_lucht_iter):.5f} Joule


""")

    return E_botsing, E_lucht+E_lucht_iter, E_verlies_totaal, 



# === BEREKENING ===
E_botsing, E_lucht, E_verlies_totaal = simulate_fall_and_rise(h_0, h_1, mass, radius)

# === RESULTATEN ===
print(f"Totaal verloren energie (botsing + luchtweerstand): {E_verlies_totaal:.5f} J")


