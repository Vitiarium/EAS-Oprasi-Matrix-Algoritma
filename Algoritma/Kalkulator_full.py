
import customtkinter as ctk
import numpy as np
import re
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG        = "#0f1117"
PANEL     = "#1a1d27"
CARD      = "#20232e"
ACCENT    = "#4fc3f7"
ACCENT2   = "#00e5ff"
TEXT      = "#e8eaf6"
SUBTEXT   = "#7986cb"
SUCCESS   = "#69f0ae"
WARNING   = "#ffd740"
DANGER    = "#ff5252"
BORDER    = "#2a2d3e"

FONT_TITLE  = ("Courier New", 22, "bold")
FONT_HEAD   = ("Courier New", 13, "bold")
FONT_LABEL  = ("Courier New", 11)
FONT_ENTRY  = ("Courier New", 12)
FONT_RESULT = ("Courier New", 12, "bold")
FONT_MENU   = ("Courier New", 12, "bold")

AR = {
    'H':1.008,'He':4.003,'Li':6.941,'Be':9.012,'B':10.811,'C':12.011,'N':14.007,'O':15.999,
    'F':18.998,'Ne':20.180,'Na':22.990,'Mg':24.305,'Al':26.982,'Si':28.086,'P':30.974,
    'S':32.065,'Cl':35.453,'Ar':39.948,'K':39.098,'Ca':40.078,'Sc':44.956,'Ti':47.867,
    'V':50.942,'Cr':51.996,'Mn':54.938,'Fe':55.845,'Co':58.933,'Ni':58.693,'Cu':63.546,
    'Zn':65.380,'Ga':69.723,'Ge':72.630,'As':74.922,'Se':78.971,'Br':79.904,'Kr':83.798,
    'Rb':85.468,'Sr':87.620,'Y':88.906,'Zr':91.224,'Nb':92.906,'Mo':95.950,'Tc':98.000,
    'Ru':101.070,'Rh':102.906,'Pd':106.420,'Ag':107.868,'Cd':112.414,'In':114.818,
    'Sn':118.710,'Sb':121.760,'Te':127.600,'I':126.904,'Xe':131.293,'Cs':132.905,
    'Ba':137.327,'La':138.905,'Ce':140.116,'Pr':140.908,'Nd':144.242,'Pm':145.000,
    'Sm':150.360,'Eu':151.964,'Gd':157.250,'Tb':158.925,'Dy':162.500,'Ho':164.930,
    'Er':167.259,'Tm':168.934,'Yb':173.054,'Lu':174.967,'Hf':178.490,'Ta':180.948,
    'W':183.840,'Re':186.207,'Os':190.230,'Ir':192.217,'Pt':195.084,'Au':196.967,
    'Hg':200.592,'Tl':204.383,'Pb':207.200,'Bi':208.980,'Po':209.000,'At':210.000,
    'Rn':222.000,'Fr':223.000,'Ra':226.000,'Ac':227.000,'Th':232.038,'Pa':231.036,
    'U':238.029,'Np':237.000,'Pu':244.000,'Am':243.000,'Cm':247.000,'Bk':247.000,
    'Cf':251.000,'Es':252.000,'Fm':257.000,'Md':258.000,'No':259.000,'Lr':262.000,
    'Rf':267.000,'Db':268.000,'Sg':271.000,'Bh':272.000,'Hs':270.000,'Mt':276.000,
    'Ds':281.000,'Rg':280.000,'Cn':285.000,'Nh':284.000,'Fl':289.000,'Mc':288.000,
    'Lv':293.000,'Ts':294.000,'Og':294.000,
}

INDIKATOR_LIST = [
    ("Timol Biru (asam)",   1.2,  2.8),
    ("Metil Jingga",        3.1,  4.4),
    ("Bromkresol Hijau",    3.8,  5.4),
    ("Metil Merah",         4.4,  6.2),
    ("Bromkresol Ungu",     5.2,  6.8),
    ("Bromtimol Biru",      6.0,  7.6),
    ("Fenol Merah",         6.8,  8.4),
    ("Neutral Red",         6.8,  8.0),
    ("Timol Biru (basa)",   8.0,  9.6),
    ("Fenolftalein",        8.2, 10.0),
    ("Timolftalein",        9.3, 10.5),
    ("Alizarin Kuning R",  10.1, 12.0),
    ("Indigo Karmin",      11.4, 13.0),
]

def to_float(s):
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return None

def rekomendasi_indikator(pH_eq):
    return [n for n, lo, hi in INDIKATOR_LIST if lo <= pH_eq <= hi]


def make_entry(parent, placeholder="", width=200):
    e = ctk.CTkEntry(
        parent,
        placeholder_text=placeholder,
        width=width,
        font=FONT_ENTRY,
        fg_color=CARD,
        border_color=BORDER,
        border_width=1,
        text_color=TEXT,
        placeholder_text_color=SUBTEXT,
        corner_radius=6,
        height=36,
    )
    return e

def make_label(parent, text, color=TEXT, font=FONT_LABEL):
    return ctk.CTkLabel(parent, text=text, text_color=color, font=font, anchor="w")

def make_button(parent, text, command, color=ACCENT, hover=None, width=160):
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        font=FONT_MENU,
        fg_color=color,
        hover_color=hover or ACCENT2,
        text_color="#0f1117",
        corner_radius=8,
        height=38,
        width=width,
    )

def result_box(parent):
    tb = ctk.CTkTextbox(
        parent,
        font=FONT_RESULT,
        fg_color=CARD,
        text_color=SUCCESS,
        border_color=BORDER,
        border_width=1,
        corner_radius=8,
        height=110,
        wrap="word",
    )
    return tb
def add_history(tb, text):
    tb.configure(state="normal")
    existing = tb.get("1.0", "end").strip()
    if existing:
        tb.insert("end", "\n" + "─"*36 + "\n")
    tb.insert("end", text)
    tb.configure(state="disabled")
    tb.see("end")

def history_box(parent):
    tb = ctk.CTkTextbox(
        parent,
        font=("Courier New", 10),
        fg_color=CARD,
        text_color=SUBTEXT,
        border_color=BORDER,
        border_width=1,
        corner_radius=8,
        height=90,
        wrap="word",
    )
    return tb
    

def show_result(tb, text, color=SUCCESS):
    tb.configure(state="normal", text_color=color)
    tb.delete("1.0", "end")
    tb.insert("end", text)
    tb.configure(state="disabled")


def section_title(parent, text):
    f = ctk.CTkFrame(parent, fg_color="transparent")
    f.pack(fill="x", pady=(0, 10))
    ctk.CTkLabel(f, text="◆ " + text, font=FONT_HEAD,
                 text_color=ACCENT).pack(side="left")
    ctk.CTkFrame(f, height=1, fg_color=BORDER).pack(
        side="left", fill="x", expand=True, padx=(10, 0), pady=8)


class KalkulatorPanel(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, scrollbar_button_color=BORDER,
                         scrollbar_button_hover_color=ACCENT)

        section_title(self, "Molaritas")
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", pady=4)
        self.mol_massa = make_entry(row, "Massa (g)")
        self.mol_massa.pack(side="left", padx=(0, 8))
        self.mol_mr = make_entry(row, "Mr (g/mol)")
        self.mol_mr.pack(side="left", padx=(0, 8))
        self.mol_v = make_entry(row, "Volume (L)")
        self.mol_v.pack(side="left", padx=(0, 8))
        make_button(row, "Hitung", self.hitung_molaritas, width=120).pack(side="left")
        self.mol_result = result_box(self)
        self.mol_result.pack(fill="x", pady=(4, 2))
        self.mol_history = history_box(self)
        self.mol_history.pack(fill="x", pady=(0, 16))

        section_title(self, "Pengenceran  (M₁V₁ = M₂V₂)")
        row2 = ctk.CTkFrame(self, fg_color="transparent")
        row2.pack(fill="x", pady=4)
        self.enc_m1 = make_entry(row2, "M₁ (awal)")
        self.enc_m1.pack(side="left", padx=(0, 8))
        self.enc_v1 = make_entry(row2, "V₁ (awal)")
        self.enc_v1.pack(side="left", padx=(0, 8))
        self.enc_m2 = make_entry(row2, "M₂ (target)")
        self.enc_m2.pack(side="left", padx=(0, 8))
        make_button(row2, "Hitung", self.hitung_pengenceran, width=120).pack(side="left")
        self.enc_result = result_box(self)
        self.enc_result.pack(fill="x", pady=(4, 2))
        self.enc_history = history_box(self)
        self.enc_history.pack(fill="x", pady=(0, 16))

        section_title(self, "pH Asam / Basa Kuat")
        row3 = ctk.CTkFrame(self, fg_color="transparent")
        row3.pack(fill="x", pady=4)
        self.ph_h = make_entry(row3, "[H⁺] atau [OH⁻] (mol/L)")
        self.ph_h.pack(side="left", padx=(0, 8))
        make_button(row3, "Hitung", self.hitung_ph, width=120).pack(side="left")
        self.ph_result = result_box(self)
        self.ph_result.pack(fill="x", pady=(4, 2))
        self.ph_history = history_box(self)
        self.ph_history.pack(fill="x", pady=(0, 16))

        section_title(self, "Mr Otomatis")
        row4 = ctk.CTkFrame(self, fg_color="transparent")
        row4.pack(fill="x", pady=4)
        self.mr_rumus = make_entry(row4, "Rumus kimia (contoh: H2O, Na2SO4)", width=280)
        self.mr_rumus.pack(side="left", padx=(0, 8))
        make_button(row4, "Hitung", self.hitung_mr, width=120).pack(side="left")
        self.mr_result = result_box(self)
        self.mr_result.pack(fill="x", pady=(4, 2))
        self.mr_history = history_box(self)
        self.mr_history.pack(fill="x", pady=(0, 16))

        section_title(self, "pH Buffer")
        self.buf_tipe = ctk.CTkSegmentedButton(
            self, values=["Buffer Asam", "Buffer Basa"],
            font=FONT_LABEL, fg_color=CARD,
            selected_color=ACCENT, selected_hover_color=ACCENT2,
            unselected_color=PANEL, text_color=TEXT,
            command=self.toggle_buffer)
        self.buf_tipe.set("Buffer Asam")
        self.buf_tipe.pack(anchor="w", pady=(0, 6))

        row5 = ctk.CTkFrame(self, fg_color="transparent")
        row5.pack(fill="x", pady=4)
        self.buf_k = make_entry(row5, "Ka")
        self.buf_k.pack(side="left", padx=(0, 8))
        self.buf_mol1 = make_entry(row5, "Mol asam lemah")
        self.buf_mol1.pack(side="left", padx=(0, 8))
        self.buf_mol2 = make_entry(row5, "Mol basa konjugasi")
        self.buf_mol2.pack(side="left", padx=(0, 8))
        make_button(row5, "Hitung", self.hitung_buffer, width=120).pack(side="left")
        self.buf_result = result_box(self)
        self.buf_result.pack(fill="x", pady=(4, 2))
        self.buf_history = history_box(self)
        self.buf_history.pack(fill="x", pady=(0, 16))

        section_title(self, "Gas Ideal  (PV = nRT)")
        make_label(self, "Kosongkan 1 kolom yang ingin dihitung →", SUBTEXT).pack(anchor="w", pady=(0, 4))
        row6 = ctk.CTkFrame(self, fg_color="transparent")
        row6.pack(fill="x", pady=4)
        self.gas_P = make_entry(row6, "P (atm)")
        self.gas_P.pack(side="left", padx=(0, 8))
        self.gas_V = make_entry(row6, "V (L)")
        self.gas_V.pack(side="left", padx=(0, 8))
        self.gas_n = make_entry(row6, "n (mol)")
        self.gas_n.pack(side="left", padx=(0, 8))
        self.gas_T = make_entry(row6, "T (K)")
        self.gas_T.pack(side="left", padx=(0, 8))
        make_button(row6, "Hitung", self.hitung_gas, width=120).pack(side="left")
        self.gas_result = result_box(self)
        self.gas_result.pack(fill="x", pady=(4, 2))
        self.gas_history = history_box(self)
        self.gas_history.pack(fill="x", pady=(0, 16))

        section_title(self, "Pereaksi Pembatas  (aA + bB → Produk)")
        row7 = ctk.CTkFrame(self, fg_color="transparent")
        row7.pack(fill="x", pady=4)
        self.pp_a = make_entry(row7, "Koef A")
        self.pp_a.pack(side="left", padx=(0, 8))
        self.pp_ma = make_entry(row7, "Mol A")
        self.pp_ma.pack(side="left", padx=(0, 8))
        self.pp_b = make_entry(row7, "Koef B")
        self.pp_b.pack(side="left", padx=(0, 8))
        self.pp_mb = make_entry(row7, "Mol B")
        self.pp_mb.pack(side="left", padx=(0, 8))
        make_button(row7, "Hitung", self.hitung_pp, width=120).pack(side="left")
        self.pp_result = result_box(self)
        self.pp_result.pack(fill="x", pady=(4, 2))
        self.pp_history = history_box(self)
        self.pp_history.pack(fill="x", pady=(0, 20))

    def toggle_buffer(self, val):
        if val == "Buffer Asam":
            self.buf_k.configure(placeholder_text="Ka")
            self.buf_mol1.configure(placeholder_text="Mol asam lemah")
            self.buf_mol2.configure(placeholder_text="Mol basa konjugasi")
        else:
            self.buf_k.configure(placeholder_text="Kb")
            self.buf_mol1.configure(placeholder_text="Mol basa lemah")
            self.buf_mol2.configure(placeholder_text="Mol asam konjugasi")

    def hitung_molaritas(self):
        m, mr, v = to_float(self.mol_massa.get()), to_float(self.mol_mr.get()), to_float(self.mol_v.get())
        if None in (m, mr, v) or mr == 0 or v == 0:
            show_result(self.mol_result, "⚠ Input tidak valid.", WARNING)
            return
        n = m / mr
        M = n / v
        teks = f"n = {n:.4f} mol\nMolaritas = {M:.4f} M"
        show_result(self.mol_result, teks)
        add_history(self.mol_history, teks)

    def hitung_pengenceran(self):
        m1, v1, m2 = to_float(self.enc_m1.get()), to_float(self.enc_v1.get()), to_float(self.enc_m2.get())
        if None in (m1, v1, m2) or m2 == 0:
            show_result(self.enc_result, "⚠ Input tidak valid.", WARNING)
            return
        v2 = (m1 * v1) / m2
        teks = f"V₂ = {v2:.4f} L"
        show_result(self.enc_result, teks)
        add_history(self.enc_history, teks )

    def hitung_ph(self):
        h = to_float(self.ph_h.get())
        if h is None or h <= 0:
            show_result(self.ph_result, "⚠ Input tidak valid.", WARNING)
            return
        pH = -np.log10(h)
        teks = f"pH = {pH:.4f}"
        show_result(self.ph_result, teks)
        add_history(self.ph_history, teks)

    def parse_rumus(self, rumus):
        def parse(s, i):
            hasil = {}
            while i < len(s):
                if s[i] == '(':
                    sub, i = parse(s, i + 1)
                    angka = ''
                    while i < len(s) and s[i].isdigit():
                        angka += s[i]
                        i += 1
                    mul = int(angka) if angka else 1
                    for el, jml in sub.items():
                        hasil[el] = hasil.get(el, 0) + jml * mul
                elif s[i] == ')':
                    return hasil, i + 1
                elif s[i].isupper():
                    el = s[i]
                    i += 1
                    while i < len(s) and s[i].islower():
                        el += s[i]
                        i += 1
                    angka = ''
                    while i < len(s) and s[i].isdigit():
                        angka += s[i]
                        i += 1
                    jml = int(angka) if angka else 1
                    if el not in AR:
                        raise KeyError(el)
                    hasil[el] = hasil.get(el, 0) + jml
                else:
                    raise ValueError(f"Karakter tidak valid: '{s[i]}'")
            return hasil, i

        komposisi, _ = parse(rumus, 0)
        return komposisi

    def hitung_mr(self):
        rumus = self.mr_rumus.get().strip()
        if not rumus:
            show_result(self.mr_result, "⚠ Input kosong.", WARNING)
            return
        if rumus.count('(') != rumus.count(')'):
            show_result(self.mr_result, "⚠ Tanda kurung tidak seimbang.", WARNING)
            return
        try:
            komposisi = self.parse_rumus(rumus)
            total = sum(AR[el] * jml for el, jml in komposisi.items())
            detail = "  +  ".join(f"{el}×{jml}" for el, jml in sorted(komposisi.items()))
            teks = f"Mr {rumus} = {total:.3f} g/mol\n{detail}"
            show_result(self.mr_result, teks)
            add_history(self.mr_history, teks)
        except KeyError as e:
            show_result(self.mr_result, f"⚠ Unsur {e} tidak dikenali.", WARNING)
        except ValueError as e:
            show_result(self.mr_result, f"⚠ {e}", WARNING)

    def hitung_buffer(self):
        K    = to_float(self.buf_k.get())
        mol1 = to_float(self.buf_mol1.get())
        mol2 = to_float(self.buf_mol2.get())
        if None in (K, mol1, mol2) or K <= 0 or mol1 == 0:
            show_result(self.buf_result, "⚠ Input tidak valid.", WARNING)
            return
        tipe = self.buf_tipe.get()
        if tipe == "Buffer Asam":
            pH = -np.log10(K) + np.log10(mol2 / mol1)
            teks = f"pH Buffer Asam = {pH:.4f}"
        else:
            pOH = -np.log10(K) + np.log10(mol2 / mol1)
            pH  = 14 - pOH
            teks = f"pH Buffer Basa = {pH:.4f}"
        show_result(self.buf_result, teks)
        add_history(self.buf_history, teks)

    def hitung_gas(self):
        R = 0.08206
        P_s = self.gas_P.get().strip()
        V_s = self.gas_V.get().strip()
        n_s = self.gas_n.get().strip()
        T_s = self.gas_T.get().strip()
        empty = [s == "" for s in (P_s, V_s, n_s, T_s)]
        if sum(empty) != 1:
            show_result(self.gas_result, "⚠ Kosongkan tepat 1 kolom.", WARNING)
            return
        try:
            vals = [to_float(s) if s else None for s in (P_s, V_s, n_s, T_s)]
            P, V, n, T = vals
            if empty[0]:
                res = (n * R * T) / V; teks = f"P = {res:.4f} atm"
            elif empty[1]:
                res = (n * R * T) / P; teks = f"V = {res:.4f} L"
            elif empty[2]:
                res = (P * V) / (R * T); teks = f"n = {res:.4f} mol"
            else:
                res = (P * V) / (n * R); teks = f"T = {res:.4f} K"
            show_result(self.gas_result, teks)
            add_history(self.gas_history, teks)
        except Exception:
            show_result(self.gas_result, "⚠ Input tidak valid.", WARNING)

    def hitung_pp(self):
        a, ma = to_float(self.pp_a.get()), to_float(self.pp_ma.get())
        b, mb = to_float(self.pp_b.get()), to_float(self.pp_mb.get())
        if None in (a, ma, b, mb) or a == 0 or b == 0:
            show_result(self.pp_result, "⚠ Input tidak valid.", WARNING)
            return
        rA, rB = ma / a, mb / b
        if rA < rB:
            sisa = mb - (b / a) * ma
            teks = f"Pereaksi Pembatas: Zat A\nZat B sisa: {sisa:.4f} mol"
        elif rB < rA:
            sisa = ma - (a / b) * mb
            teks = f"Pereaksi Pembatas: Zat B\nZat A sisa: {sisa:.4f} mol"
        else:
            teks = "Kedua zat habis bereaksi (stoikiometris)."
        show_result(self.pp_result, teks)
        add_history(self.pp_history, teks)


class TitrasiPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        left = ctk.CTkScrollableFrame(self, fg_color=PANEL, corner_radius=12,
                                      scrollbar_button_color=BORDER)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=0)

        section_title(left, "Titrasi Asam-Basa")

        make_label(left, "Jenis Titrasi", SUBTEXT).pack(anchor="w", pady=(0, 4))
        self.jenis = ctk.CTkSegmentedButton(
            left,
            values=["Asam Kuat\n× Basa Kuat", "Asam Lemah\n× Basa Kuat", "Basa Lemah\n× Asam Kuat","Asam Poliprotik\n× Basa Kuat", "Basa Poliprotik\n× Asam Kuat"],
            font=("Courier New", 10, "bold"),
            fg_color=CARD, selected_color=ACCENT,
            selected_hover_color=ACCENT2,
            unselected_color=CARD, text_color=TEXT,
            command=self.on_jenis_change)
        self.jenis.set("Asam Kuat\n× Basa Kuat")
        self.jenis.pack(fill="x", pady=(0, 14))

        self.entries = {}
        self.entry_frame = ctk.CTkFrame(left, fg_color="transparent")
        self.entry_frame.pack(fill="x")
        self.build_entries("strong")

        make_button(left, "⚗  Plot Titrasi", self.plot_titrasi,
                    color=ACCENT, width=200).pack(pady=14)

        self.info_box = ctk.CTkTextbox(
            left, font=FONT_RESULT, fg_color=CARD,
            text_color=SUCCESS, border_color=BORDER,
            border_width=1, corner_radius=8, height=160, wrap="word")
        self.info_box.pack(fill="x", pady=(0, 8))

        right = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=12)
        right.grid(row=0, column=1, sticky="nsew")

        self.fig, self.ax = plt.subplots(figsize=(6.5, 5.2))
        self.fig.patch.set_facecolor("#1a1d27")
        self.ax.set_facecolor("#20232e")
        self.ax.set_xlabel("Volume Penitrasi (mL)", color=TEXT, fontsize=10)
        self.ax.set_ylabel("pH", color=TEXT, fontsize=10)
        self.ax.set_title("Kurva Titrasi", color=ACCENT, fontsize=12, fontweight="bold")
        self.ax.tick_params(colors=TEXT)
        for spine in self.ax.spines.values():
            spine.set_edgecolor(BORDER)
        self.ax.grid(True, color=BORDER, linestyle="--", linewidth=0.5)
        self.ax.text(0.5, 0.5, "Plot akan muncul di sini",
                     ha="center", va="center", color=SUBTEXT,
                     fontsize=12, transform=self.ax.transAxes)
        self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

    def build_entries(self, mode):
        for w in self.entry_frame.winfo_children():
            w.destroy()
        self.entries = {}
        if mode == "strong":
            fields = [("Ma", "M Asam (M)"), ("Va", "V Asam (mL)"), ("Mb", "M Basa (M)")]
        elif mode == "weak_acid":
            fields = [("Ka", "Ka"), ("Ma", "M Asam (M)"),
                      ("Va", "V Asam (mL)"), ("Mb", "M Basa (M)")]
        elif mode == "poly_acid":
            fields = [
                ("n",  "Jumlah proton (2 atau 3)"),
                ("Ka1","Ka1"), ("Ka2","Ka2"), ("Ka3","Ka3 (isi 0 jika diprotik)"),
                ("Ma", "M Asam Poliprotik (M)"),
                ("Va", "V Asam (mL)"),
                ("Mb", "M Basa Kuat (M)"),
            ]
        elif mode == "poly_base":
            fields = [
                ("n",  "Jumlah proton (2 atau 3)"),
                ("Kb1","Kb1"), ("Kb2","Kb2"), ("Kb3","Kb3 (isi 0 jika diprotik)"),
                ("Mb", "M Basa Poliprotik (M)"),
                ("Vb", "V Basa (mL)"),
                ("Ma", "M Asam Kuat (M)"),
            ]
        else:
            fields = [("Kb", "Kb"), ("Mb", "M Basa (M)"),
                      ("Vb", "V Basa (mL)"), ("Ma", "M Asam (M)")]
        for key, ph in fields:
            make_label(self.entry_frame, ph, SUBTEXT).pack(anchor="w", pady=(6, 0))
            e = make_entry(self.entry_frame, ph, width=260)
            e.pack(fill="x")
            self.entries[key] = e

    def on_jenis_change(self, val):
        if "Kuat\n× Basa Kuat" in val:
            self.build_entries("strong")
        elif "Asam Lemah" in val:
            self.build_entries("weak_acid")
        elif "Basa Lemah" in val:
            self.build_entries("weak_base")
        elif "Asam Poliprotik" in val:
            self.build_entries("poly_acid")
        else:
            self.build_entries("poly_base")

    def get(self, key):
        return to_float(self.entries[key].get()) if key in self.entries else None

    def calc_strong(self):
        Ma, Va_mL, Mb = self.get("Ma"), self.get("Va"), self.get("Mb")
        if None in (Ma, Va_mL, Mb):
            raise ValueError("Semua input harus diisi")
        Va = Va_mL / 1000
        Ve = (Ma * Va) / Mb
        Vb = np.linspace(0, 2 * Ve, 5000)
        pH = []
        n_asam = Ma * Va
        for v in Vb:
            n_basa = Mb * v
            Vtot = Va + v
            if n_basa < n_asam:
                H = (n_asam - n_basa) / Vtot
                pH.append(-np.log10(H))
            else:
                OH = (n_basa - n_asam) / Vtot
                if OH <= 0:
                    pH.append(7.0)
                else:
                    pH.append(14 + np.log10(OH))
        pH = np.array(pH)
        idx = np.argmin(np.abs(Vb - Ve))
        pH[idx] = 7.0
        return Vb, pH

    def calc_weak_acid(self):
        Ka, Ma, Va_mL, Mb = self.get("Ka"), self.get("Ma"), self.get("Va"), self.get("Mb")
        if None in (Ka, Ma, Va_mL, Mb):
            raise ValueError("Semua input harus diisi")
        Va = Va_mL / 1000
        pKa = -np.log10(Ka)
        Ve = (Ma * Va) / Mb
        Vb = np.linspace(0, 2 * Ve, 5000)
        pH = []
        n_asam = Ma * Va
        for v in Vb:
            n_basa = Mb * v
            Vtot = Va + v
            if np.isclose(n_basa, 0):
                H = np.sqrt(Ka * Ma)
                pH.append(-np.log10(H))
            elif n_basa < n_asam:
                HA = n_asam - n_basa
                A = n_basa
                if A <= 0:
                    H = np.sqrt(Ka * Ma)
                    pH.append(-np.log10(H))
                else:
                    pH.append(pKa + np.log10(A / HA))
            elif np.isclose(n_basa, n_asam):
                Cb = n_asam / Vtot
                Kb = 1e-14 / Ka
                OH = np.sqrt(Kb * Cb)
                pH.append(14 + np.log10(OH))
            else:
                OH = (n_basa - n_asam) / Vtot
                pH.append(14 + np.log10(OH))
        return Vb, np.array(pH)

    def calc_weak_base(self):
        Kb, Mb, Vb_mL, Ma = self.get("Kb"), self.get("Mb"), self.get("Vb"), self.get("Ma")
        if None in (Kb, Mb, Vb_mL, Ma):
            raise ValueError("Semua input harus diisi")
        Vb0 = Vb_mL / 1000
        pKb = -np.log10(Kb)
        Ve = (Mb * Vb0) / Ma
        Va = np.linspace(0, 2 * Ve, 5000)
        pH = []
        n_basa = Mb * Vb0
        for v in Va:
            n_asam = Ma * v
            Vtot = Vb0 + v
            if np.isclose(n_asam, 0):
                OH = np.sqrt(Kb * Mb)
                pH.append(14 + np.log10(OH))
            elif n_asam < n_basa:
                B = n_basa - n_asam
                BH = n_asam
                if BH <= 0:
                    OH = np.sqrt(Kb * Mb)
                    pH.append(14 + np.log10(OH))
                else:
                    pOH = pKb + np.log10(BH / B)
                    pH.append(14 - pOH)
            elif np.isclose(n_asam, n_basa):
                Ca = n_basa / Vtot
                Ka = 1e-14 / Kb
                H = np.sqrt(Ka * Ca)
                pH.append(-np.log10(H))
            else:
                H = (n_asam - n_basa) / Vtot
                pH.append(-np.log10(H))
        return Va, np.array(pH)
    def calc_poly_acid(self):
        n   = int(self.get("n") or 0)
        Ka1 = self.get("Ka1")
        Ka2 = self.get("Ka2")
        Ka3 = self.get("Ka3") if n == 3 else 1.0
        Ma  = self.get("Ma")
        Va_mL = self.get("Va")
        Mb  = self.get("Mb")
        if None in (Ka1, Ka2, Ka3, Ma, Va_mL, Mb) or n not in (2, 3):
            raise ValueError("Semua input harus diisi dan n = 2 atau 3")
        Va = Va_mL / 1000
        n_asam = Ma * Va
        Ve1 = n_asam / Mb
        Ve2 = 2 * Ve1
        Ve3 = 3 * Ve1 if n == 3 else None
        V_max = (n + 1) * Ve1
        Vb = np.linspace(0, V_max, 8000)
        pKa1 = -np.log10(Ka1)
        pKa2 = -np.log10(Ka2)
        pKa3 = -np.log10(Ka3) if n == 3 else None
        pH = []
        for v in Vb:
            nb = Mb * v
            Vtot = Va + v
            if np.isclose(nb, 0):
                H = np.sqrt(Ka1 * Ma)
                pH.append(-np.log10(max(H, 1e-14)))
            elif nb < n_asam:
                HA = n_asam - nb
                A  = nb
                pH.append(pKa1 + np.log10(max(A, 1e-30) / max(HA, 1e-30)))
            elif np.isclose(nb, n_asam):
                if n == 2:
                    pH.append((pKa1 + pKa2) / 2)
                else:
                    pH.append((pKa1 + pKa2) / 2)
            elif nb < 2 * n_asam:
                HA = 2 * n_asam - nb
                A  = nb - n_asam
                pH.append(pKa2 + np.log10(max(A, 1e-30) / max(HA, 1e-30)))
            elif np.isclose(nb, 2 * n_asam):
                if n == 2:
                    Cb = n_asam / Vtot
                    Kb = 1e-14 / Ka2
                    OH = np.sqrt(Kb * Cb)
                    pH.append(14 + np.log10(max(OH, 1e-14)))
                else:
                    pH.append((pKa2 + pKa3) / 2)
            elif n == 3 and nb < 3 * n_asam:
                HA = 3 * n_asam - nb
                A  = nb - 2 * n_asam
                pH.append(pKa3 + np.log10(max(A, 1e-30) / max(HA, 1e-30)))
            elif n == 3 and np.isclose(nb, 3 * n_asam):
                Cb = n_asam / Vtot
                Kb = 1e-14 / Ka3
                OH = np.sqrt(Kb * Cb)
                pH.append(14 + np.log10(max(OH, 1e-14)))
            else:
                excess = nb - n * n_asam
                OH = excess / Vtot
                pH.append(14 + np.log10(max(OH, 1e-14)))
        return Vb, np.array(pH)

    def calc_poly_base(self):
        n   = int(self.get("n") or 0)
        Kb1 = self.get("Kb1")
        Kb2 = self.get("Kb2")
        Kb3 = self.get("Kb3") if n == 3 else 1.0
        Mb  = self.get("Mb")
        Vb_mL = self.get("Vb")
        Ma  = self.get("Ma")
        if None in (Kb1, Kb2, Kb3, Mb, Vb_mL, Ma) or n not in (2, 3):
            raise ValueError("Semua input harus diisi dan n = 2 atau 3")
        Vb0 = Vb_mL / 1000
        n_basa = Mb * Vb0
        Ve1 = n_basa / Ma
        V_max = (n + 1) * Ve1
        Va = np.linspace(0, V_max, 8000)
        pKb1 = -np.log10(Kb1)
        pKb2 = -np.log10(Kb2)
        pKb3 = -np.log10(Kb3) if n == 3 else None
        Ka1 = 1e-14 / Kb1
        Ka2 = 1e-14 / Kb2
        Ka3 = (1e-14 / Kb3) if n == 3 else None
        pKa1 = -np.log10(Ka1)
        pKa2 = -np.log10(Ka2)
        pKa3 = -np.log10(Ka3) if Ka3 else None
        pH = []
        for v in Va:
            na = Ma * v
            Vtot = Vb0 + v
            if np.isclose(na, 0):
                OH = np.sqrt(Kb1 * Mb)
                pH.append(14 + np.log10(max(OH, 1e-14)))
            elif na < n_basa:
                B  = n_basa - na
                BH = na
                pH.append(14 - (pKb1 + np.log10(max(BH, 1e-30) / max(B, 1e-30))))
            elif np.isclose(na, n_basa):
                if n == 2:
                    pH.append((pKa1 + pKa2) / 2)
                else:
                    pH.append((pKa1 + pKa2) / 2)
            elif na < 2 * n_basa:
                B  = 2 * n_basa - na
                BH = na - n_basa
                pH.append(14 - (pKb2 + np.log10(max(BH, 1e-30) / max(B, 1e-30))))
            elif np.isclose(na, 2 * n_basa):
                if n == 2:
                    Ca = n_basa / Vtot
                    H  = np.sqrt(Ka2 * Ca)
                    pH.append(-np.log10(max(H, 1e-14)))
                else:
                    pH.append((pKa2 + pKa3) / 2)
            elif n == 3 and na < 3 * n_basa:
                B  = 3 * n_basa - na
                BH = na - 2 * n_basa
                pH.append(14 - (pKb3 + np.log10(max(BH, 1e-30) / max(B, 1e-30))))
            elif n == 3 and np.isclose(na, 3 * n_basa):
                Ca = n_basa / Vtot
                H  = np.sqrt(Ka3 * Ca)
                pH.append(-np.log10(max(H, 1e-14)))
            else:
                excess = na - n * n_basa
                H = excess / Vtot
                pH.append(-np.log10(max(H, 1e-14)))
        return Va, np.array(pH)

    def plot_titrasi(self):
        jenis = self.jenis.get()
        try:
            if "Kuat\n× Basa Kuat" in jenis:
                V, pH = self.calc_strong()
            elif "Lemah\n× Basa Kuat" in jenis:
                V, pH = self.calc_weak_acid()
            elif "Asam Poliprotik" in jenis:
                V, pH = self.calc_poly_acid()
            elif "Basa Poliprotik" in jenis:
                V, pH = self.calc_poly_base()
            else:
                V, pH = self.calc_weak_base()
        except Exception as exc:
            messagebox.showerror("Error", f"Input tidak valid:\n{exc}")
            return

        dpH = np.gradient(pH, V)
        idx = np.argmax(dpH)
        Ve = V[idx]
        pH_eq = pH[idx]
        ind = rekomendasi_indikator(pH_eq)

        self.ax.cla()
        self.ax.set_facecolor("#20232e")
        self.ax.plot(V * 1000, pH, color=ACCENT, linewidth=2.5, label="Kurva pH")
        self.ax.axvline(Ve * 1000, color=DANGER, linestyle="--", linewidth=1.5,
                        label=f"Ekuivalen {Ve*1000:.2f} mL")
        self.ax.axhline(pH_eq, color=SUCCESS, linestyle=":", linewidth=1,
                        alpha=0.7, label=f"pH = {pH_eq:.2f}")
        self.ax.scatter([Ve * 1000], [pH_eq], color=WARNING, zorder=5, s=80)
        self.ax.set_xlabel("Volume Penitrasi (mL)", color=TEXT, fontsize=10)
        self.ax.set_ylabel("pH", color=TEXT, fontsize=10)
        self.ax.set_title("Kurva Titrasi Asam-Basa", color=ACCENT,
                          fontsize=12, fontweight="bold")
        self.ax.tick_params(colors=TEXT)
        for spine in self.ax.spines.values():
            spine.set_edgecolor(BORDER)
        self.ax.grid(True, color=BORDER, linestyle="--", linewidth=0.5)
        self.ax.legend(facecolor=CARD, edgecolor=BORDER,
                       labelcolor=TEXT, fontsize=9)
        self.fig.tight_layout()
        self.canvas.draw()

        ind_str = "\n".join(f"  • {i}" for i in ind) if ind else "  (tidak ada yang ideal)"
        info = (
            f"Titik Ekuivalen : {Ve*1000:.2f} mL\n"
            f"pH Ekuivalen    : {pH_eq:.2f}\n\n"
            f"Indikator cocok :\n{ind_str}"
        )
        self.info_box.configure(state="normal")
        self.info_box.delete("1.0", "end")
        self.info_box.insert("end", info)
        self.info_box.configure(state="disabled")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Kalkulator Kimia")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(fg_color=BG)

        header = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=0, height=64)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="⚗  KALKULATOR KIMIA",
            font=FONT_TITLE,
            text_color=ACCENT,
        ).pack(side="left", padx=24, pady=16)

        ctk.CTkLabel(
            header,
            text="by Python + CustomTkinter",
            font=("Courier New", 10),
            text_color=SUBTEXT,
        ).pack(side="left", pady=20)

        sidebar = ctk.CTkFrame(self, fg_color=PANEL, width=180, corner_radius=0)
        sidebar.pack(fill="y", side="left")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(sidebar, text="MENU", font=("Courier New", 10, "bold"),
                     text_color=SUBTEXT).pack(pady=(20, 8), padx=16, anchor="w")

        self.nav_buttons = {}
        for label, key in [("🧮  Kalkulator", "kalkulator"), ("📈  Titrasi", "titrasi")]:
            btn = ctk.CTkButton(
                sidebar, text=label, font=FONT_MENU,
                fg_color="transparent", hover_color=CARD,
                text_color=TEXT, anchor="w",
                corner_radius=8, height=44, width=160,
                command=lambda k=key: self.switch(k))
            btn.pack(padx=10, pady=2)
            self.nav_buttons[key] = btn

        self.content = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.content.pack(fill="both", expand=True, side="left", padx=10, pady=10)

        self.panels = {
            "kalkulator": KalkulatorPanel(self.content),
            "titrasi"   : TitrasiPanel(self.content),
        }

        self.switch("kalkulator")

    def switch(self, key):
        for k, p in self.panels.items():
            p.pack_forget()
        self.panels[key].pack(fill="both", expand=True)
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(fg_color=ACCENT, text_color="#0f1117")
            else:
                btn.configure(fg_color="transparent", text_color=TEXT)


if __name__ == "__main__":
    app = App()
    app.mainloop()
