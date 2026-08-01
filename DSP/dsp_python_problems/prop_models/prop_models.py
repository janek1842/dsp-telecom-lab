import numpy as np

def free_space_loss(distance_km, freq_ghz):
    """Free Space Path Loss dB"""
    fspl = 20 * np.log10(distance_km) + 20 * np.log10(freq_ghz) + 92.45
    return fspl

def okumura_hata_loss(distance_km, freq_mhz, station_height, ue_height):
    """Okumura Hata Loss dB"""
    a_hm = (1.1 * np.log10(freq_mhz) - 0.7) * ue_height - (1.56 * np.log10(freq_mhz)-0.8)
    l_db = (69.55 + 26.16 * np.log10(freq_mhz) - 13.82 * np.log10(station_height)
    - a_hm + (44.9 - 6.55 * np.log10(station_height)) * np.log10(distance_km))
    return l_db

def itu_r_p1238(d_m, f_ghz, N_floors=0, environment='office'):
    """
    ITU-R P.1238 - Indoor)
    """

    env_params = {
        'office': {'N': 28, 'Lf': 15, 'b': 4},  # Biuro
        'residential': {'N': 28, 'Lf': 4, 'b': 4},  # Dom/Mieszkanie
        'commercial': {'N': 22, 'Lf': 6, 'b': 3}  # Centrum handlowe
    }
    p = env_params[environment]

    if N_floors == 0:
        floor_loss = 0
    else:
        floor_loss = p['Lf'] + (N_floors - 1) * p['b']

    pl = 20 * np.log10(f_ghz * 1000) + p['N'] * np.log10(d_m) + floor_loss - 28
    return pl


def sui_model(d_m, f_mhz, hb_m, hm_m, terrain_category='B'):
    """Stanford University Interim (SUI) Model (2 - 11 GHz) """

    d0 = 100.0

    params = {
        'A': {'a': 4.6, 'b': 0.0075, 'c': 12.6, 's': 8.2, 'gamma_a': 20.0},
        'B': {'a': 4.0, 'b': 0.0065, 'c': 10.8, 's': 9.0, 'gamma_a': 10.8},
        'C': {'a': 3.6, 'b': 0.0050, 'c': 20.0, 's': 8.2, 'gamma_a': 20.0}
    }
    p = params[terrain_category]

    gamma = p['a'] - p['b'] * hb_m + p['c'] / hb_m
    lambda_m = 3e8 / (f_mhz * 1e6)
    A = 20 * np.log10(4 * np.pi * d0 / lambda_m)

    Xf = 6.0 * np.log10(f_mhz / 2000.0)

    if terrain_category in ['A', 'B']:
        Xh = -10.8 * np.log10(hm_m / 2.0)
    else:
        Xh = -20.0 * np.log10(hm_m / 2.0)

    pl = A + 10 * gamma * np.log10(d_m / d0) + Xf + Xh
    return pl