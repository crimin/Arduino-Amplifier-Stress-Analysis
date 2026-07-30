import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt
from sklearn.cluster import KMeans

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------
df = pd.read_csv(
    "HalfBridgetest.txt",
    names=["timestamp", "volts"],
    sep=",",
    engine="python",
    skip_blank_lines=True
)

df["volts"] = pd.to_numeric(df["volts"], errors="coerce")
df["volts"] = df["volts"].iloc[10:]
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna()

# ----------------------------------------------------
# CONSTANTS
# ----------------------------------------------------
def ina125_gain(Rg_ohms):
    return 4 + (60000 / Rg_ohms)

GAIN = ina125_gain(100)   # ~604
E_exc = 5.0
GF    = 2.0

# ----------------------------------------------------
# REMOVE OFFSET USING REAL BASELINE
# ----------------------------------------------------
baseline = df["volts"].iloc[0:300].mean()
df["volts_corr"] = df["volts"] - baseline
df["Vr"] = df["volts_corr"]

# ----------------------------------------------------
#. STRAIN FROM AMPLIFIED SIGNAL
# ----------------------------------------------------
df["strain"] = (2.0 * df["Vr"]) / (GF * E_exc * GAIN)
df["strain_filt"] = medfilt(df["strain"], kernel_size=5)

# ----------------------------------------------------
# BEAM GEOMETRY
# ----------------------------------------------------
E_beam = 210e9
L      = 0.30
x_g    = 0.035

b = 13/1000
h = 3.0/1000

I = (b * h**3) / 12.0
y_neutral = h / 2.0

# ----------------------------------------------------
# STRESS & MOMENT
# ----------------------------------------------------
df["stress"] = E_beam * df["strain_filt"]
df["moment_gauge"] = df["stress"] * I / y_neutral
df["moment_Nmm"] = df["moment_gauge"] * 1000

# ----------------------------------------------------
# SMOOTH MOMENT FOR PLATEAU DETECTION
# ----------------------------------------------------
df["moment_smooth"] = df["moment_Nmm"].rolling(
    window=500, center=True, min_periods=1
).mean()

# ----------------------------------------------------
# K-MEANS PLATEAU DETECTION (TOP 10% FLAT SAMPLES)
# ----------------------------------------------------
moment_vals = df["moment_smooth"].values
deriv = np.abs(np.gradient(moment_vals))

# Select the flattest 10% of samples
flat_threshold = np.percentile(deriv, 10)
flat_mask = deriv <= flat_threshold

moment_flat = moment_vals[flat_mask].reshape(-1, 1)

# K-means on only the flattest samples
kmeans = KMeans(n_clusters=7, n_init=20, random_state=42)
labels = kmeans.fit_predict(moment_flat)

# Cluster medians
cluster_medians = np.array([
    np.median(moment_flat[labels == i]) for i in range(7)
])

# Sort by value
cluster_medians_sorted = np.sort(cluster_medians)

# Assign plateaus
M_0g, M_24g, M_48g, M_72g, M_96g, M_120g, M_144g = cluster_medians_sorted

measured_moment = cluster_medians_sorted


# ----------------------------------------------------
# ANALYTICAL MOMENT
# ----------------------------------------------------
loads_g = np.array([0, 24, 48, 72, 96, 120, 144])
loads_N = (loads_g / 1000.0) * 9.81

moment_analytical = loads_N * (L - x_g) * 1000

# ----------------------------------------------------
# CALIBRATION FITS
# ----------------------------------------------------
X = np.array([0, 24, 48, 72, 96, 120, 144])
y = measured_moment

poly1 = np.polyfit(X, y, 1)
poly2 = np.polyfit(X, y, 2)
poly3 = np.polyfit(X, y, 3)

f1 = np.poly1d(poly1)
f2 = np.poly1d(poly2)
f3 = np.poly1d(poly3)

force_range = np.linspace(min(X), max(X), 300)

# ----------------------------------------------------
# PLOT: Calibration Curve
# ----------------------------------------------------
plt.figure(figsize=(10, 6))
plt.scatter(X, y, color="blue", label="Measured Moment", s=60)
plt.plot(X, moment_analytical, 'o', color="orange", label="Analytical Moment", markersize=8)
plt.plot(force_range, f1(force_range), label="Straight Line Fit", linewidth=2)
plt.xlabel("Applied Force (gram)")
plt.ylabel("Moment at Gauge (N·mm)")
plt.title("Calibration Curve: Moment vs Applied Force")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
plt.savefig("HalfBridgeCalCurve.png")

# ----------------------------------------------------
# PLOT: Moment Time Series
# ----------------------------------------------------
plt.figure(figsize=(14, 8))
plt.plot(df["timestamp"], df["moment_smooth"], color="red", linewidth=2)
plt.xlabel("Time")
plt.ylabel("Moment (N·mm)")
plt.title("Time-Series: Plateau Detection (Moment)")
plt.grid(True)
plt.tight_layout()
plt.show()
plt.savefig("halfBridgeMomentPlateau.png")

# ----------------------------------------------------
# PLOT: Strain Time Series
# ----------------------------------------------------
plt.figure(figsize=(14, 8))
plt.plot(df["timestamp"], df["strain_filt"], color="blue", linewidth=2)
plt.xlabel("Time")
plt.ylabel("Strain (ε)")
plt.title("Time-Series: Strain")
plt.grid(True)
plt.tight_layout()
plt.show()

# ----------------------------------------------------
# PLOT: Raw INA125 Output
# ----------------------------------------------------
plt.figure(figsize=(14, 8))
plt.plot(df["timestamp"], df["volts"], color="green", linewidth=2)
plt.xlabel("Time")
plt.ylabel("INA125 Output (V)")
plt.title("Time-Series: Raw INA125 Output")
plt.grid(True)
plt.tight_layout()
plt.show()
