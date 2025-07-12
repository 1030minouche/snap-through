import matplotlib.pyplot as plt
import numpy as np
import math

def trier_par_deltamu(deltamu, periode):
    paires = list(zip(deltamu, periode))
    paires_triees = sorted(paires, key=lambda x: x[0])
    deltamu_trie, periode_trie = zip(*paires_triees)
    return list(deltamu_trie), list(periode_trie)

periode_T1 = [0.2, 0.137255, 0.12195122, 0.16666667, 0.2142857, 0.35]
periode_omega1 = [e/(2*math.pi) for e in periode_T1]
deltamu1 = [5.96254, 3.20629, 2.41877, 1.46249, 0.95623, 0.44997]

periode_T2 = [0.27027027, 0.2201257862, 0.194444444, 0.1818181818181818, 0.1655629139, 0.3846153846, 0.3205128205]
periode_omega2 = [e/(2*math.pi) for e in periode_T2]
deltamu2 = [1.35003, 2.19378, 3.03753, 3.88128, 4.72503, 0.22501, 0.1125]

periode_T3 = [0.357143, 0.2857143, 0.22222222, 0.2417582, 0.5652174, 0.5217393, 0.75]
periode_omega3 = [e/(2*math.pi) for e in periode_T3]
deltamu3 = [1.12499, 0.78749, 0.5625, 0.3375, 0.225, 0.16875, 0.1125]

periode_T4 = [1, 0.69444, 0.78571, 0.6, 0.625]
periode_omega4 = [e/(2*math.pi) for e in periode_T4]
deltamu4 = [0.14062, 0.19687, 0.30938, 0.47813, 0.75937]

periode_T5 = [0.4137931, 0.2580645, 0.44444, 0.5, 0.5625, 0.267857, 0.705888235]
periode_omega5 = [e/(2*math.pi) for e in periode_T5]
deltamu5 = [1.96875, 1.40625, 1.2375, 0.73125, 0.50625, 0.3375, 0.16875]

periode_T6 = [0.0638722555, 0.055888215, 0.1523178799, 0.08609271523178808, 0.09271523179]
periode_omega6 = [e/(2*math.pi) for e in periode_T6]
deltamu6 = [0.1, 0.28124, 0.50624, 0.73124, 0.95624]

deltamu1, periode_omega1 = trier_par_deltamu(deltamu1, periode_omega1)
deltamu2, periode_omega2 = trier_par_deltamu(deltamu2, periode_omega2)
deltamu3, periode_omega3 = trier_par_deltamu(deltamu3, periode_omega3)
deltamu4, periode_omega4 = trier_par_deltamu(deltamu4, periode_omega4)
deltamu5, periode_omega5 = trier_par_deltamu(deltamu5, periode_omega5)
deltamu6, periode_omega6 = trier_par_deltamu(deltamu6, periode_omega6)

deltamu_all = np.array(deltamu1 + deltamu2 + deltamu3 + deltamu4 + deltamu5 + deltamu6)
periode_all = np.array(periode_omega1 + periode_omega2 + periode_omega3 + periode_omega4 + periode_omega5 + periode_omega6)

# Régression linéaire dans l'espace log-log
log_x = np.log10(deltamu_all)
log_y = np.log10(periode_all)
coeffs = np.polyfit(log_x, log_y, 1)  # [pente, intercept]
fit_fn = np.poly1d(coeffs)

# Points pour tracer la droite de régression globale
x_fit = np.logspace(np.log10(min(deltamu_all)), np.log10(max(deltamu_all)), 100)
y_fit = 10**fit_fn(np.log10(x_fit))

# Droite de pente -0.25 pour référence
C = 0.2  # Ajuste cette constante pour mieux positionner la ligne sur le graphique
y_ref = C * x_fit**(-0.25)

# Tracé
plt.figure(figsize=(8, 4))

# Tracé des courbes des séries
plt.plot(deltamu1, periode_omega1, '-', label="série 1")
plt.plot(deltamu2, periode_omega2, '-', label="série 2")
plt.plot(deltamu3, periode_omega3, '-', label="série 3")
plt.plot(deltamu4, periode_omega4, '-', label="série 4")
plt.plot(deltamu5, periode_omega5, '-', label="série 5")
plt.plot(deltamu6, periode_omega6, '-', label="série 6")

# Tracé de la droite de régression globale
plt.plot(x_fit, y_fit, 'k--', linewidth=2, label=f"Fit global : y ∝ x^{coeffs[0]:.2f}")

# Tracé de la droite de pente -0.25
plt.plot(x_fit, y_ref, 'r--', linewidth=2, label="pente -0.25 (référence)")

# Mise en forme
plt.xscale('log')
plt.yscale('log')
plt.title("Régression globale et référence pente -0.25 (log-log)")
plt.xlabel("delta mu")
plt.ylabel("T (en unité de ω⁻¹)")
plt.grid(True, which='both', linestyle=':', linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()
