import numpy as np
import matplotlib.pyplot as plt
import re

 
# AUTO KONVERSI & ERROR HANDLING
def input_float(prompt):
    while True:
        try:
            # ubah koma jadi titik agar tidak error
            val = input(prompt).replace(",", ".")
            return float(val)
        except ValueError:
            print(" Input tidak valid. Harap masukkan format angka.")


# Logika perhitungan
def hitung_molaritas():
    print("\n--- Hitung Molaritas ---")
    massa = input_float("Massa (g): ")
    Mr = input_float("Mr (g/mol): ")
    V = input_float("Volume (L): ")

    n = massa / Mr
    M = n / V

    print(f"=> Molaritas = {M:.4f} M")


def hitung_pengenceran():
    print("\n--- Hitung Pengenceran ---")
    M1 = input_float("M1 (Molaritas awal): ")
    V1 = input_float("V1 (Volume awal): ")
    M2 = input_float("M2 (Molaritas target): ")

    V2 = (M1 * V1) / M2  # M1V1 = M2V2

    print(f"=> V2 (Volume akhir) = {V2:.4f}")


def hitung_pH():
    print("\n--- Hitung pH Asam/Basa Kuat ---")
    H = input_float("[H+] atau [OH-] (mol/L): ")

    # Asumsi user memasukkan [H+] untuk mencari pH langsung
    pH = -np.log10(H)
    print(f"=> Nilai -log(konsentrasi) = {pH:.4f}")


def hitung_mr_otomatis():
    print("\n--- Kalkulator Mr Otomatis ---")
    print("Catatan: Gunakan huruf kapital untuk unsur (contoh: H2O, Na2SO4). Belum mendukung tanda kurung.")
    rumus = input("Masukkan rumus kimia: ")

    # Database Ar
    Ar = { 'H': 1.0, 'He': 4.0,'Li': 6.9, 'Be': 9.0, 'B': 10.8, 'C': 12.0, 'N': 14.0, 'O': 16.0, 'F': 19.0, 'Ne': 20.2,'Na': 23.0, 'Mg': 24.3, 'Al': 27.0, 'Si': 28.1, 'P': 31.0, 'S': 32.1, 'Cl': 35.5, 'Ar': 40.0,'K': 39.1, 'Ca': 40.1, 'Sc': 45.0, 'Ti': 47.9, 'V': 50.9, 'Cr': 52.0, 'Mn': 54.9, 'Fe': 55.8,'Co': 58.9, 'Ni': 58.7, 'Cu': 63.5, 'Zn': 65.4, 'Ga': 69.7, 'Ge': 72.6, 'As': 74.9, 'Se': 79.0,'Br': 79.9, 'Kr': 83.8,'Rb': 85.5, 'Sr': 87.6, 'Y': 88.9, 'Zr': 91.2, 'Nb': 92.9, 'Mo': 96.0, 'Tc': 98.0, 'Ru': 101.1,'Rh': 102.9, 'Pd': 106.4, 'Ag': 107.9, 'Cd': 112.4, 'In': 114.8, 'Sn': 118.7, 'Sb': 121.8,'Te': 127.6, 'I': 126.9, 'Xe': 131.3,'Cs': 132.9, 'Ba': 137.3, 'La': 138.9, 'Ce': 140.1, 'Pr': 140.9, 'Nd': 144.2, 'Pm': 145.0,'Sm': 150.4, 'Eu': 152.0, 'Gd': 157.3, 'Tb': 158.9, 'Dy': 162.5, 'Ho': 164.9, 'Er': 167.3,'Tm': 168.9, 'Yb': 173.0, 'Lu': 175.0,'Hf': 178.5, 'Ta': 180.9, 'W': 183.8, 'Re': 186.2, 'Os': 190.2, 'Ir': 192.2, 'Pt': 195.1,'Au': 197.0, 'Hg': 200.6, 'Tl': 204.4, 'Pb': 207.2, 'Bi': 209.0, 'Po': 209.0, 'At': 210.0,'Rn': 222.0,'Fr': 223.0, 'Ra': 226.0, 'Ac': 227.0, 'Th': 232.0, 'Pa': 231.0, 'U': 238.0, 'Np': 237.0,'Pu': 244.0, 'Am': 243.0, 'Cm': 247.0, 'Bk': 247.0, 'Cf': 251.0, 'Es': 252.0, 'Fm': 257.0,'Md': 258.0, 'No': 259.0, 'Lr': 262.0,'Rf': 267.0, 'Db': 270.0, 'Sg': 271.0, 'Bh': 270.0, 'Hs': 277.0, 'Mt': 278.0, 'Ds': 281.0,'Rg': 282.0, 'Cn': 285.0, 'Nh': 286.0, 'Fl': 289.0, 'Mc': 290.0, 'Lv': 293.0, 'Ts': 294.0,'Og': 294.0 }

    try:
        unsur_atom = re.findall(r'([A-Z][a-z]?)(\d*)', rumus)
        Mr_total = 0
        for unsur, jumlah in unsur_atom:
            jumlah = int(jumlah) if jumlah else 1
            Mr_total += Ar[unsur] * jumlah

        print(f"\n=> Mr {rumus} = {Mr_total:.2f} g/mol")

    except KeyError as e:
        print(f"\n Error: Unsur {e} belum ada di database Ar.")

def hitung_ph_buffer():
    print("\n--- Kalkulator pH Buffer ---")
    print("1. Buffer Asam (Asam lemah + Basa konjugasi)")
    print("2. Buffer Basa (Basa lemah + Asam konjugasi)")
    tipe = input("Pilih tipe buffer: ")

    if tipe == "1":
        Ka = input_float("Masukkan Ka: ")
        mol_asam = input_float("Mol asam lemah: ")
        mol_garam = input_float("Mol basa konjugasi (garam): ")

        pH = -np.log10(Ka) + np.log10(mol_garam / mol_asam)
        print(f"\n=> pH Buffer Asam = {pH:.4f}")

    elif tipe == "2":
        Kb = input_float("Masukkan Kb: ")
        mol_basa = input_float("Mol basa lemah: ")
        mol_garam = input_float("Mol asam konjugasi (garam): ")

        pOH = -np.log10(Kb) + np.log10(mol_garam / mol_basa)
        pH = 14 - pOH
        print(f"\n=> pH Buffer Basa = {pH:.4f}")
    else:
        print("\n❌ Pilihan tidak valid.")


def hitung_gas_ideal():
    print("\n--- Hukum Gas Ideal (PV = nRT) ---")
    print("Kosongkan (tekan Enter) pada 1 variabel yang ingin dihitung.")

    R = 0.08206  # L.atm/(mol.K)
    print(f"Konstanta Gas (R) = {R} L.atm/(mol.K)\n")

    P_str = input("Tekanan P (atm)   : ").replace(",", ".")
    V_str = input("Volume V (L)      : ").replace(",", ".")
    n_str = input("Jumlah Mol n      : ").replace(",", ".")
    T_str = input("Suhu T (Kelvin)   : ").replace(",", ".")

    try:
        if P_str == "":
            V, n, T = float(V_str), float(n_str), float(T_str)
            P = (n * R * T) / V
            print(f"\n=> Tekanan (P) = {P:.4f} atm")
        elif V_str == "":
            P, n, T = float(P_str), float(n_str), float(T_str)
            V = (n * R * T) / P
            print(f"\n=> Volume (V) = {V:.4f} L")
        elif n_str == "":
            P, V, T = float(P_str), float(V_str), float(T_str)
            n = (P * V) / (R * T)
            print(f"\n=> Jumlah Mol (n) = {n:.4f} mol")
        elif T_str == "":
            P, V, n = float(P_str), float(V_str), float(n_str)
            T = (P * V) / (n * R)
            print(f"\n=> Suhu (T) = {T:.4f} K")
        else:
            print("\n❌ Kamu harus mengosongkan tepat 1 variabel untuk dihitung!")
    except ValueError:
        print("\n❌ Error: Pastikan input yang dimasukkan adalah angka.")


def pereaksi_pembatas():
    print("\n--- Stoikiometri & Pereaksi Pembatas ---")
    print("Reaksi: aA + bB -> Produk")

    a = input_float("Koefisien zat A (a): ")
    mol_A = input_float("Mol awal zat A: ")

    b = input_float("Koefisien zat B (b): ")
    mol_B = input_float("Mol awal zat B: ")

    # Menentukan rasio untuk mencari pereaksi pembatas
    rasio_A = mol_A / a
    rasio_B = mol_B / b

    print("\n--- Hasil ---")
    if rasio_A < rasio_B:
        print("=> Zat A adalah Pereaksi Pembatas.")
        mol_bereaksi_B = (b / a) * mol_A
        print("=> Zat A habis bereaksi.")
        print(f"=> Zat B bersisa: {mol_B - mol_bereaksi_B:.4f} mol")
    elif rasio_B < rasio_A:
        print("=> Zat B adalah Pereaksi Pembatas.")
        mol_bereaksi_A = (a / b) * mol_B
        print("=> Zat B habis bereaksi.")
        print(f"=> Zat A bersisa: {mol_A - mol_bereaksi_A:.4f} mol")
    else:
        print("=> Kedua zat habis bereaksi (campuran ekuivalen / stoikiometris).")


def menu_kalkulator():
    while True:
        print("\n=== CHEMICAL CALCULATOR ===")
        print("1. Molaritas")
        print("2. Pengenceran")
        print("3. pH Asam/Basa Kuat")
        print("4. Mr Otomatis")
        print("5. pH Buffer")
        print("6. Hukum Gas Ideal (PV=nRT)")
        print("7. Pereaksi Pembatas")
        print("0. Kembali")

        pilih = input("Pilih: ")

        if pilih == "1":
            hitung_molaritas()
        elif pilih == "2":
            hitung_pengenceran()
        elif pilih == "3":
            hitung_pH()
        elif pilih == "4":
            hitung_mr_otomatis()
        elif pilih == "5":
            hitung_ph_buffer()
        elif pilih == "6":
            hitung_gas_ideal()
        elif pilih == "7":
            pereaksi_pembatas()
        elif pilih == "0":
            break
        else:
            print("❌ Pilihan tidak valid.")


 
# INDIKATOR TITRASI
 

def rekomendasi_indikator(pH_eq):
    indikator = [
        ("Metil Jingga", 3.1, 4.4),
        ("Bromkresol Hijau", 3.8, 5.4),
        ("Metil Merah", 4.4, 6.2),
        ("Bromtimol Biru", 6.0, 7.6),
        ("Fenol Merah", 6.8, 8.4),
        ("Fenolftalein", 8.2, 10.0),
        ("Alizarin Kuning", 10.1, 12.0)
    ]

    return [nama for nama, low, high in indikator if low <= pH_eq <= high]


 
# TITRASI STRONG-STRONG
def titrasi_strong_strong():
    print("\n--- Titrasi Asam Kuat vs Basa Kuat ---")
    Ma = input_float("M asam: ")
    Va = input_float("V asam (mL): ") / 1000
    Mb = input_float("M basa: ")

    Vb = np.linspace(0, 2*Va, 10000)
    pH = []       
    n_asam = Ma * Va

    for v in Vb:
        n_basa = Mb * v
        Vtot = Va + v

        if n_basa < n_asam:
            H = (n_asam - n_basa) / Vtot
            pH.append(-np.log10(H))
        elif abs(n_basa - n_asam):
            pH.append(7)
        else:
            OH = (n_basa - n_asam) / Vtot
            pH.append(14 + np.log10(OH))

    dpH = np.gradient(pH, V)  # turunan numerik
    idx = np.argmax(dpH)

    Ve = V[idx]
    pH_eq = pH[idx]

    print(f"\n=> Titik ekuivalen ≈ {Ve*1000:.2f} mL")
    print(f"=> pH ekuivalen ≈ {7}")

    indikator = rekomendasi_indikator(pH_eq)

    if indikator:
        print("=> Indikator yang cocok:")
        for i in indikator:
            print("   -", i)
    else:
        print("=> Tidak ada indikator ideal di rentang ini.")



 
# TITRASI WEAK ACID
def titrasi_weak_acid():
    print("\n--- Titrasi Asam Lemah vs Basa Kuat ---")
    Ka = input_float("Ka: ")
    Ma = input_float("M asam: ")
    Va = input_float("V asam (mL): ") / 1000
    Mb = input_float("M basa: ")

    pKa = -np.log10(Ka)
    Vb = np.linspace(0, 2*Va, 200)
    pH = []
    n_asam = Ma * Va

    for v in Vb:
        n_basa = Mb * v
        Vtot = Va + v

        if n_basa == 0:
            H = np.sqrt(Ka * Ma)
            pH.append(-np.log10(H))

        elif n_basa < n_asam:
            HA = n_asam - n_basa
            A = n_basa
            pH.append(pKa + np.log10(A/HA))

        elif abs(n_basa - n_asam) < 1e-6:
            Cb = n_asam / Vtot
            Kb = 1e-14 / Ka
            OH = np.sqrt(Kb * Cb)
            pH.append(14 + np.log10(OH))

        else:
            OH = (n_basa - n_asam) / Vtot
            pH.append(14 + np.log10(OH))

    return Vb, pH


 
# TITRASI WEAK BASE
def titrasi_weak_base():
    print("\n--- Titrasi Basa Lemah vs Asam Kuat ---")
    Kb = input_float("Kb: ")
    Mb = input_float("M basa: ")
    Vb_awal = input_float("V basa (mL): ") / 1000
    Ma = input_float("M asam: ")

    pKb = -np.log10(Kb)
    Va = np.linspace(0, 2*Vb_awal, 200)
    pH = []
    n_basa = Mb * Vb_awal

    for v in Va:
        n_asam = Ma * v
        Vtot = Vb_awal + v

        if n_asam == 0:
            OH = np.sqrt(Kb * Mb)
            pH.append(14 + np.log10(OH))

        elif n_asam < n_basa:
            B = n_basa - n_asam
            BH = n_asam
            pOH = pKb + np.log10(BH/B)
            pH.append(14 - pOH)

        elif abs(n_asam - n_basa) < 1e-6:
            Ca = n_basa / Vtot
            Ka = 1e-14 / Kb
            H = np.sqrt(Ka * Ca)
            pH.append(-np.log10(H))

        else:
            H = (n_asam - n_basa) / Vtot
            pH.append(-np.log10(H))

    return Va, pH


 
# ANALISIS EKUIVALEN & PLOT
def analisis(V, pH):
    # Menampilkan Grafik
    plt.figure(figsize=(8, 5))
    plt.plot(V*1000, pH, color='b', linewidth=2, label="Kurva pH")
    plt.axvline(Ve*1000, color='r', linestyle='--', label=f"Titik Ekuivalen ({Ve*1000:.1f} mL)")
    plt.axhline(pH_eq, color='g', linestyle='--', alpha=0.5)
    plt.xlabel("Volume Penitrasi (mL)")
    plt.ylabel("pH")
    plt.title("Kurva Titrasi Asam-Basa")
    plt.legend()
    plt.grid(True)
    plt.show()


 
# MENU TITRASI
def menu_titrasi():
    while True:
        print("\n=== SIMULASI TITRASI ===")
        print("1. Asam kuat - basa kuat")
        print("2. Asam lemah - basa kuat")
        print("3. Basa lemah - asam kuat")
        print("0. Kembali")

        pilih = input("Pilih: ")

        if pilih == "1":
            V, pH = titrasi_strong_strong()
            analisis(V, pH)
        elif pilih == "2":
            V, pH = titrasi_weak_acid()
            analisis(V, pH)
        elif pilih == "3":
            V, pH = titrasi_weak_base()
            analisis(V, pH)
        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid.")


 
# MAIN MENU
def main():
    print("="*40)
    print("  SELAMAT DATANG DI KALKULATOR KIMIA")
    print("="*40)

    while True:
        print("\n=== MAIN MENU ===")
        print("1. Chemical Calculator")
        print("2. Kurva Titrasi")
        print("0. Keluar")

        pilih = input("Pilih: ")

        if pilih == "1":
            menu_kalkulator()
        elif pilih == "2":
            menu_titrasi()
        elif pilih == "0":
            print("\nTerima kasih telah menggunakan kalkulator kimia ini! Sampai jumpa.")
            break
        else:
            print(" Pilihan tidak valid.")


if __name__ == "__main__":
    main()