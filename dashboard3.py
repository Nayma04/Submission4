import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# 🏷️ Header Dashboard
st.write(
    """
    # Dashboard Projek Akhir
    Analisis data dengan Python
    """
)

# 📥 **Load Data**
day_df = pd.read_csv(r"Penyewaan_Sepeda.csv")

# 🎯 **Konversi kolom tanggal**
day_df["date"] = pd.to_datetime(day_df["date"])
min_date = day_df["date"].min()
max_date = day_df["date"].max()

# 🎛 **Sidebar Filter**
with st.sidebar:
    st.header("📅 Filter Data")
    # Data total penyewaan berdasarkan musim
    season_rentals = {
    "Musim Dingin": 471348,
    "Musim Panas": 918589,
    "Musim Gugur": 1061129,
    "Musim Semi": 841613
    }
    # Membuat filter dropdown untuk memilih musim
    selected_season = st.selectbox("Pilih Musim:", list(season_rentals.keys()))  

    # Filter Tahun
    year_option = st.radio("Pilih Tahun:", ["2011", "2012"])
    filtered_df = day_df[day_df["year"] == (0 if year_option == "2011" else 1)]

    # Filter Hari Libur
    holiday_option = st.radio("Pilih Jenis Hari:", ["Hari Libur", "Hari Biasa"])
    filtered_holiday_df = filtered_df[filtered_df["holiday"] == (1 if holiday_option == "Hari Libur" else 0)]
    
st.subheader("📅 Season")
# Menampilkan jumlah penyewaan sesuai musim yang dipilih
st.metric(label=f"Total Penyewaan - {selected_season}", value=season_rentals[selected_season])
# Menghitung total penyewaan sepeda di setiap musim
season_df = day_df.groupby("season")["cnt"].sum().reset_index()
# Mapping nama musim
season_names = {1: "Musim Dingin", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Semi"}
season_df["season_name"] = season_df["season"].map(season_names)

# Visualisasi Penyewaan Sepeda Berdasarkan Musim
st.subheader("🚲 Penyewaan Sepeda di Setiap Musim")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=season_df["season_name"], y=season_df["cnt"], palette="viridis", ax=ax)
plt.xlabel("Musim")
plt.ylabel("Jumlah Penyewaan Sepeda")
plt.title("Jumlah Penyewaan Sepeda di Setiap Musim")
st.pyplot(fig)


st.subheader("📊 Boxplot Penyewaan Sepeda Berdasarkan Musim")
# Membuat figure dan axis
fig, ax = plt.subplots(figsize=(8, 5))
# Membuat Boxplot
sns.boxplot(x="season", y="cnt", data=day_df, ax=ax, palette="Set2")
# Menambahkan label dan judul
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_title("Distribusi Penyewaan Sepeda di Setiap Musim")
st.pyplot(fig)

# 📊 Scatterplot: Windspeed vs Penyewaan Sepeda
st.subheader(f"📈 Scatter Plot: Windspeed vs Penyewaan Sepeda ({year_option})")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(
    x=filtered_df["windspeed"], 
    y=filtered_df["cnt"], 
    alpha=0.5, 
    hue=filtered_df["year"], 
    palette={0: "red", 1: "blue"},
    ax=ax
)
ax.set_xlabel("Kecepatan Angin")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_title("Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda")
plt.title(f"Jumlah Penyewaan Sepeda di Setiap Musim ({year_option})")
#ax.legend(["2011", "2012"], title="Tahun")
st.pyplot(fig)

# 📊 Heatmap Korelasi
st.subheader(f"🔥 Heatmap Korelasi ({year_option})")
heatmap_columns = ["temp", "atemp", "hum", "windspeed", "cnt"]
corr_matrix = filtered_df[heatmap_columns].corr()

fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
ax.set_title("Korelasi antar Variabel")
st.pyplot(fig)

# 📊 Stacked Bar Chart: Penyewaan Sepeda 
st.subheader(f"📊 Stacked Bar Chart: Penyewaan Sepeda ({holiday_option})")

total_casual = filtered_holiday_df["casual"].sum()
total_registered = filtered_holiday_df["registered"].sum()

fig, ax = plt.subplots(figsize=(6, 5))
ax.bar(holiday_option, total_casual, label="Casual", color="red")
ax.bar(holiday_option, total_registered, bottom=total_casual, label="Registered", color="blue")
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_title(f"Penyewaan Sepeda pada {holiday_option}")
ax.legend()
st.pyplot(fig)

# 🎻 Violin Chart: Penyewaan Sepeda 
st.subheader(f"🎻 Violin Chart: Penyewaan Sepeda ({holiday_option})")

violin_df = filtered_holiday_df.melt(id_vars=["holiday"], value_vars=["casual", "registered"],
                                     var_name="User Type", value_name="Total Penyewaan")

fig, ax = plt.subplots(figsize=(6, 5))
sns.violinplot(x="User Type", y="Total Penyewaan", data=violin_df, 
               palette={"casual": "red", "registered": "blue"}, ax=ax)

ax.set_title(f"Distribusi Penyewaan Sepeda pada {holiday_option}")
ax.set_xlabel("Jenis Pengguna")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
st.pyplot(fig)