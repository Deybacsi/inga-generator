import tkinter as tk
from tkinter import ttk, font
import tkinter.filedialog as fd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def update_sections_label(val):
    sections_value_label.config(text=str(int(float(val))))
    draw_fan()

def update_angle_label(val):
    angle_value_label.config(text=str(int(float(val))))
    draw_fan()

def update_belso_label(val):
    belso_value_label.config(text=str(int(float(val)*100)) + "%")
    draw_fan()    

def update_szoveg_helyzet_label(val):
    szoveg_helyzet_value_label.config(text=str(int(float(val)*100)) + "%")
    draw_fan()

def update_fontsize_label(val):
    fontsize_value_label.config(text=str(int(float(val)*100)) + "%")
    draw_fan()    

def get_system_fonts():
    return sorted(set(font.families()))

def update_font_family(event=None):
    draw_fan()

def save_figure():
    file_path = fd.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG kép", "*.png"), ("JPG kép", "*.jpg"),("PDF file", "*.pdf"), ("Minden", "*.*")]
    )
    if file_path:
        fig.savefig(file_path, bbox_inches='tight')



def draw_fan():
    num_sections = int(sections_slider.get())
    total_angle_deg = int(angle_slider.get())

    labels = [      # sortörések
        line.strip().replace("\\", "\n")
        for line in labels_text.get("1.0", tk.END).splitlines()
        if line.strip()
    ]

    header = header_entry.get()

    radius = 1
    start_angle_deg = -total_angle_deg / 2
    angles = np.linspace(
        np.deg2rad(start_angle_deg),
        np.deg2rad(start_angle_deg + total_angle_deg),
        num_sections + 1
    )

    fig.clear()
    ax = fig.add_subplot(111, polar=True)
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    ax.spines['polar'].set_visible(False)
    ax.set_ylim(0, radius*1.32)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(False)
    ax.set_title(header, va='bottom',fontsize=15, fontname=font_family_var.get())
    fig.subplots_adjust(left=0, right=1, top=0.95, bottom=0.05)  # teljes hely kitöltése


    belso_kor_tavolsag = float(belso_slider.get())  # belső kör távolsága a középponttól
    ax.plot(angles, [radius * belso_kor_tavolsag] * len(angles), color='black')
    for angle in angles:
        ax.plot([angle, angle], [radius*belso_kor_tavolsag, radius], color='black')

    text_radius = radius * float(szoveg_helyzet_slider.get())

    first_szazalek_cikk=int((sections_slider.get()-11) /2)

    # feliratok
    for i in range(num_sections):
        # Középre igazított feliratok
        angle = (angles[i] + angles[i + 1]) / 2
        angle_deg = np.rad2deg(angle)
        label = labels[i] if i < len(labels) else str(i + 1)
        rotation = 90 - angle_deg
        if rotation > 90:
            rotation += 180
        ax.text(angle, text_radius, label, ha='center', va='center', fontsize=10*float(fontsize_slider.get()), fontname=font_family_var.get(), rotation=rotation, rotation_mode='anchor')

        # szirom alakú körívek
        delta = angles[i + 1] - angles[i]
        szirom_radius = radius * np.sin(delta / 2)  # dinamikus szirom méret
        # 100 pontból álló kör polár koordinátában
        circle_theta = np.linspace(0, np.pi, 100)
        th_circ = angle + szirom_radius / radius * np.cos(-circle_theta)
        r_circ = radius + szirom_radius * np.sin(circle_theta)
        ax.plot(th_circ, r_circ, color='black', lw=1.5)

        if first_szazalek_cikk <= i <= first_szazalek_cikk + 10:
            # szirom szöveg
            szirom_text = "AA"
            ax.text(angle, radius * 1.2 + (float(angle_slider.get())-180)/3000, str((i-first_szazalek_cikk)*10), ha='center', va='center', fontsize=12, fontname=font_family_var.get())

    canvas.draw()

root = tk.Tk()
root.state('zoomed')                # ha linuxon futtatnád, akkor ezt a sort vedd ki
# root.attributes('-zoomed', True)  # helyette ezt tedd be

root.title("Ingatábla generátor")

frame = ttk.Frame(root)
frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

ttk.Label(frame, text="Fejléc:").pack()
header_entry = ttk.Entry(frame)
header_entry.insert(0, "Ingatábla")
header_entry.pack(fill=tk.X)
header_entry.bind("<KeyRelease>", lambda event: draw_fan())


angle_row = ttk.Frame(frame)
angle_row.pack(fill=tk.X)

ttk.Label(angle_row, text="Teljes nyílási szög (fok):").pack(side=tk.LEFT)
angle_slider = ttk.Scale(frame, from_=30, to=360, orient=tk.HORIZONTAL)
angle_slider.set(120)
angle_value_label = ttk.Label(angle_row, text=str(int(angle_slider.get())))
angle_value_label.pack(side=tk.LEFT, padx=5)
angle_slider.pack(fill=tk.X)
angle_slider.config(command=update_angle_label)


# ------------------- 

sections_row = ttk.Frame(frame)
sections_row.pack(fill=tk.X)
ttk.Label(sections_row, text="Körcikkek száma:").pack(side=tk.LEFT)
sections_slider = ttk.Scale(frame, from_=11, to=36, orient=tk.HORIZONTAL)
sections_slider.set(10)
sections_value_label = ttk.Label(sections_row, text=str(int(sections_slider.get())))
sections_value_label.pack(side=tk.LEFT, padx=5)
sections_slider.pack(fill=tk.X)
sections_slider.config(command=update_sections_label)  # csak most adjuk hozzá a callbacket

# -------------------

belso_row = ttk.Frame(frame)
belso_row.pack(fill=tk.X)

ttk.Label(belso_row, text="Belső kör:").pack(side=tk.LEFT)
belso_slider = ttk.Scale(frame, from_=0.1, to=0.6, orient=tk.HORIZONTAL)
belso_slider.set(0.1)
belso_value_label = ttk.Label(belso_row, text=str(int(float(belso_slider.get()) * 100)) + "%")
belso_value_label.pack(side=tk.LEFT, padx=5)
belso_slider.pack(fill=tk.X)
belso_slider.config(command=update_belso_label)

# -------------------

szoveg_row = ttk.Frame(frame)
szoveg_row.pack(fill=tk.X)

ttk.Label(szoveg_row, text="Szöveg pozíció:").pack(side=tk.LEFT)
szoveg_helyzet_slider = ttk.Scale(frame, from_=0.1, to=1.0, orient=tk.HORIZONTAL)
szoveg_helyzet_slider.set(0.8)
szoveg_helyzet_value_label = ttk.Label(szoveg_row, text=str(int(float(szoveg_helyzet_slider.get()) * 100)) + "%")
szoveg_helyzet_value_label.pack(side=tk.LEFT, padx=5)
szoveg_helyzet_slider.pack(fill=tk.X)
szoveg_helyzet_slider.config(command=update_szoveg_helyzet_label)


# -------------------

fontsize_row = ttk.Frame(frame)
fontsize_row.pack(fill=tk.X)

ttk.Label(fontsize_row, text="Betűméret:").pack(side=tk.LEFT)
fontsize_slider = ttk.Scale(frame, from_=0.5, to=2, orient=tk.HORIZONTAL)
fontsize_slider.set(1.0)
fontsize_value_label = ttk.Label(fontsize_row, text=str(int(float(fontsize_slider.get()) * 100)) + "%")
fontsize_value_label.pack(side=tk.LEFT, padx=5)
fontsize_slider.pack(fill=tk.X)
fontsize_slider.config(command=update_fontsize_label)

# -------------------

font_row = ttk.Frame(frame)
font_row.pack(fill=tk.X)
ttk.Label(font_row, text="Betűtípus:").pack(side=tk.LEFT)
font_families = get_system_fonts()
font_family_var = tk.StringVar(value="Cambria")
font_combo = ttk.Combobox(font_row, textvariable=font_family_var, values=font_families, state="readonly")
font_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
font_combo.bind("<<ComboboxSelected>>", update_font_family)

# -------------------

ttk.Label(frame, text="Feliratok (soronként):").pack()
labels_text = tk.Text(frame, height=12, width=30)
labels_text.insert("1.0", "Alma\nKörte\nSzilva\nHúsos barack\nEz egy\\sortörés")
labels_text.pack(fill=tk.X)
labels_text.bind("<KeyRelease>", lambda event: draw_fan())

# -------------------

save_row = ttk.Frame(frame)
save_row.pack(pady=(10, 0))
save_btn = ttk.Button(save_row, text="Mentés", command=save_figure)
save_btn.pack(fill=tk.X)


fig = plt.Figure(figsize=(5, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

draw_fan()
root.mainloop()