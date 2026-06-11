import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH    = os.path.join(BASE_DIR, "hospital.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "visualizations")
os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

BLUE_PALETTE = ["#2E86AB", "#A8DADC", "#457B9D", "#1D3557", "#E63946", "#F4A261"]
SINGLE_BLUE  = "#2E86AB"
LINE_COLOR   = "#1D3557"


# ── Chart 1: Patients by Medical Condition ─────────────────────────────────
df1 = pd.read_sql_query("""
    SELECT medical_condition, COUNT(*) AS total_patients
    FROM hospital_patients
    GROUP BY medical_condition
    ORDER BY total_patients DESC
""", conn)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(df1["Medical_Condition"], df1["total_patients"],
              color=BLUE_PALETTE[:len(df1)], edgecolor="white", linewidth=0.8)

for bar in bars:
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 50,
            f"{int(bar.get_height()):,}",
            ha="center", va="bottom", fontsize=10, fontweight="bold", color="#333333")

ax.set_title("Patient Distribution by Medical Condition",
             fontsize=15, fontweight="bold", pad=16)
ax.set_xlabel("Medical Condition", fontsize=12, labelpad=10)
ax.set_ylabel("Number of Patients", fontsize=12, labelpad=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_ylim(0, df1["total_patients"].max() * 1.15)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(axis="x", labelsize=11)
ax.tick_params(axis="y", labelsize=10)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/patients_by_condition.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved: patients_by_condition.png")


# ── Chart 2: Patients by Age Group ─────────────────────────────────────────
df2 = pd.read_sql_query("""
    SELECT age_group, COUNT(*) AS total_patients
    FROM hospital_patients
    GROUP BY age_group
    ORDER BY age_group
""", conn)

fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(df2["Age_Group"], df2["total_patients"],
              color=["#A8DADC", "#457B9D", "#2E86AB", "#1D3557"],
              edgecolor="white", linewidth=0.8, width=0.55)

for bar in bars:
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 120,
            f"{int(bar.get_height()):,}",
            ha="center", va="bottom", fontsize=11, fontweight="bold", color="#333333")

total = df2["total_patients"].sum()
for i, (bar, val) in enumerate(zip(bars, df2["total_patients"])):
    pct = val / total * 100
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() / 2,
            f"{pct:.1f}%",
            ha="center", va="center", fontsize=10, color="white", fontweight="bold")

ax.set_title("Patient Distribution by Age Group",
             fontsize=15, fontweight="bold", pad=16)
ax.set_xlabel("Age Group", fontsize=12, labelpad=10)
ax.set_ylabel("Number of Patients", fontsize=12, labelpad=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_ylim(0, df2["total_patients"].max() * 1.18)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(axis="both", labelsize=11)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/patients_by_age_group.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved: patients_by_age_group.png")


# ── Chart 3: Average Billing by Insurance Provider ─────────────────────────
df3 = pd.read_sql_query("""
    SELECT insurance_provider,
           ROUND(AVG(billing_amount), 2) AS avg_billing
    FROM hospital_patients
    GROUP BY insurance_provider
    ORDER BY avg_billing DESC
""", conn)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(df3["Insurance_Provider"][::-1], df3["avg_billing"][::-1],
               color=BLUE_PALETTE[:len(df3)], edgecolor="white", linewidth=0.8)

for bar in bars:
    ax.text(bar.get_width() + 50,
            bar.get_y() + bar.get_height() / 2,
            f"${bar.get_width():,.2f}",
            va="center", ha="left", fontsize=10, fontweight="bold", color="#333333")

ax.set_title("Average Billing by Insurance Provider",
             fontsize=15, fontweight="bold", pad=16)
ax.set_xlabel("Average Billing Amount (USD)", fontsize=12, labelpad=10)
ax.set_ylabel("Insurance Provider", fontsize=12, labelpad=10)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${int(x):,}"))
ax.set_xlim(0, df3["avg_billing"].max() * 1.15)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(axis="both", labelsize=11)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/billing_by_insurance.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved: billing_by_insurance.png")


# ── Chart 4: Patient Admissions by Year ────────────────────────────────────
df4 = pd.read_sql_query("""
    SELECT admission_year, COUNT(*) AS total_patients
    FROM hospital_patients
    GROUP BY admission_year
    ORDER BY admission_year
""", conn)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df4["Admission_Year"].astype(str), df4["total_patients"],
        marker="o", color=LINE_COLOR, linewidth=2.5,
        markersize=8, markerfacecolor="#E63946", markeredgecolor="white",
        markeredgewidth=1.5)

ax.fill_between(df4["Admission_Year"].astype(str), df4["total_patients"],
                alpha=0.1, color=LINE_COLOR)

for x, y in zip(df4["Admission_Year"].astype(str), df4["total_patients"]):
    ax.text(x, y + 130, f"{int(y):,}",
            ha="center", va="bottom", fontsize=10, fontweight="bold", color="#333333")

ax.set_title("Patient Admissions by Year",
             fontsize=15, fontweight="bold", pad=16)
ax.set_xlabel("Year", fontsize=12, labelpad=10)
ax.set_ylabel("Number of Patients", fontsize=12, labelpad=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_ylim(0, df4["total_patients"].max() * 1.18)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(axis="both", labelsize=11)
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/admissions_by_year.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved: admissions_by_year.png")


conn.close()
print("\nAll visualizations saved to:", os.path.abspath(OUTPUT_DIR))
