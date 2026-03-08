# ============================================================
# MABWiser + UCB1 CON TABLA RESUMEN
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mabwiser.mab import MAB, LearningPolicy

# ------------------------------------------------------------
# 1. CARGAR LOS DATOS
# ------------------------------------------------------------
df = pd.read_csv("Ads_CTR_Optimisation.csv")

N = df.shape[0]
d = df.shape[1]
arms = list(range(d))

# ------------------------------------------------------------
# 2. CREAR MODELO
# ------------------------------------------------------------
mab = MAB(
    arms=arms,
    learning_policy=LearningPolicy.UCB1()
)

# ------------------------------------------------------------
# 3. WARM START
# ------------------------------------------------------------
initial_decisions = [i for i in range(d)]
initial_rewards = [df.iloc[i, i] for i in range(d)]

mab.fit(initial_decisions, initial_rewards)

# ------------------------------------------------------------
# 4. VARIABLES DE CONTROL
# ------------------------------------------------------------
ads_selected = []
ad_selection_counts = np.zeros(d, dtype=int)
ad_reward_sums = np.zeros(d, dtype=int)
total_reward = 0

# Registramos warm start
for ad, reward in zip(initial_decisions, initial_rewards):
    ads_selected.append(ad)
    ad_selection_counts[ad] += 1
    ad_reward_sums[ad] += reward
    total_reward += reward

# ------------------------------------------------------------
# 5. SIMULACIÓN ONLINE
# ------------------------------------------------------------
for n in range(d, N):
    # El modelo elige el anuncio actual
    ad = mab.predict()

    # Obtenemos la recompensa real del usuario n para ese anuncio
    reward = df.iloc[n, ad]

    # Registramos datos
    ads_selected.append(ad)
    ad_selection_counts[ad] += 1
    ad_reward_sums[ad] += reward
    total_reward += reward

    # Actualizamos el modelo online
    mab.partial_fit(
        decisions=[ad],
        rewards=[reward]
    )

# ------------------------------------------------------------
# 6. MÉTRICAS DERIVADAS
# ------------------------------------------------------------
observed_ctr = np.divide(
    ad_reward_sums,
    ad_selection_counts,
    out=np.zeros_like(ad_reward_sums, dtype=float),
    where=ad_selection_counts != 0
)

real_ctr = df.mean(axis=0).values

summary = pd.DataFrame({
    "ad_id": range(d),
    "times_selected_by_mabwiser": ad_selection_counts,
    "clicks_observed_by_mabwiser": ad_reward_sums,
    "observed_ctr_when_selected": observed_ctr,
    "real_ctr_in_full_dataframe": real_ctr
})

summary = summary.sort_values(by="times_selected_by_mabwiser", ascending=False)

print(summary)

# ------------------------------------------------------------
# 7. GANADOR SEGÚN EL MODELO Y SEGÚN LA VERDAD DEL DATAFRAME
# ------------------------------------------------------------
winner_by_selection = summary.iloc[0]

print("\n" + "=" * 60)
print("ANUNCIO MÁS FAVORECIDO POR MABWiser-UCB1")
print("=" * 60)
print(winner_by_selection)

best_real_idx = np.argmax(real_ctr)

print("\nMejor anuncio real del DataFrame:", best_real_idx)
print("CTR real de ese anuncio:", round(real_ctr[best_real_idx], 4))

# ------------------------------------------------------------
# 8. HISTOGRAMA
# ------------------------------------------------------------
plt.figure(figsize=(10, 5))
plt.hist(ads_selected, bins=np.arange(d + 1) - 0.5, rwidth=0.8)
plt.title("Distribución de anuncios seleccionados por MABWiser-UCB1")
plt.xlabel("ID del anuncio")
plt.ylabel("Número de selecciones")
plt.xticks(range(d))
plt.show()