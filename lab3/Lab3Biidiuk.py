import tkinter as tk
import random
import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# losowawnie czasu rozmowy z rozkładu normalnego

def generate_call_time(avg, deviation, minimum, maximum):
    while True:
        value = random.gauss(avg, deviation)
        if minimum <= value <= maximum:
            return int(value)


# Glówna funkcja symulacji

def run_simulation():

    S = int(inp_channels.get())
    lam = float(inp_lambda.get())
    avg = float(inp_mean.get())
    dev = float(inp_std.get())
    tmin = int(inp_min.get())
    tmax = int(inp_max.get())
    qmax = int(inp_queue.get())
    sim_time = int(inp_time.get())

    channels = [0 for _ in range(S)]
    waiting = []

    served_calls = 0
    rejected_calls = 0

    queue_history = []

    rho_hist = []
    q_hist = []
    w_hist = []

    for step in range(sim_time):

        label_time.config(text=f"Czas: {step}")

        # aktualizacja kanałów

        for i in range(len(channels)):
            if channels[i] > 0:
                channels[i] -= 1

        # obsługa kolejki

        for i in range(len(channels)):
            if channels[i] == 0 and waiting:
                channels[i] = waiting.pop(0)
                served_calls += 1

        # nowe zgłoszenia

        new_calls = np.random.poisson(lam)

        for _ in range(new_calls):

            call_time = generate_call_time(avg, dev, tmin, tmax)

            free_channel = None

            for i in range(len(channels)):
                if channels[i] == 0:
                    free_channel = i
                    break

            if free_channel is not None:
                channels[free_channel] = call_time
                served_calls += 1
            else:
                if len(waiting) < qmax:
                    waiting.append(call_time)
                else:
                    rejected_calls += 1

        queue_history.append(len(waiting))

        avg_queue = sum(queue_history) / len(queue_history)

        busy = sum(1 for x in channels if x > 0)
        rho = busy / S

        wait_time = avg_queue / lam if lam > 0 else 0

        rho_hist.append(rho)
        q_hist.append(avg_queue)
        w_hist.append(wait_time)

        label_served.config(text=f"Obsłużone: {served_calls}")

        # wizualizacja kanałów

        for i in range(len(channel_boxes)):
            if i < len(channels) and channels[i] > 0:
                channel_boxes[i].config(bg="green", text=str(channels[i]))
            else:
                channel_boxes[i].config(bg="lightgray", text="")

        window.update()

    # Wykresy

    ax_rho.clear()
    ax_q.clear()
    ax_w.clear()

    ax_rho.plot(rho_hist)
    ax_rho.set_title("ρ - intensywność ruchu")

    ax_q.plot(q_hist)
    ax_q.set_title("Q - długość kolejki")

    ax_w.plot(w_hist)
    ax_w.set_title("W - czas oczekiwania")

    canvas.draw()

    # Zapis wyników do pliku CSV

    with open("wyniki_symulacji.csv", "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(["Parametry"])
        writer.writerow(["Kanały", S])
        writer.writerow(["Lambda", lam])
        writer.writerow(["Średnia rozmowa", avg])
        writer.writerow(["Odchylenie", dev])
        writer.writerow(["Min", tmin])
        writer.writerow(["Max", tmax])
        writer.writerow(["Czas", sim_time])

        writer.writerow([])

        writer.writerow(["rho", "Q", "W"])

        for i in range(len(rho_hist)):
            writer.writerow([rho_hist[i], q_hist[i], w_hist[i]])


# Interfejs użytkownika

window = tk.Tk()
window.title("Symulator stacji bazowej")

left_panel = tk.Frame(window)
left_panel.pack(side=tk.LEFT, padx=10)


def add_input(label, default):

    tk.Label(left_panel, text=label).pack()
    e = tk.Entry(left_panel)
    e.insert(0, default)
    e.pack()

    return e


inp_channels = add_input("Kanały", "10")
inp_queue = add_input("Kolejka", "10")
inp_lambda = add_input("Lambda", "1")
inp_mean = add_input("Średnia rozmowa", "20")
inp_std = add_input("Odchylenie", "5")
inp_min = add_input("Min", "10")
inp_max = add_input("Max", "30")
inp_time = add_input("Czas symulacji", "60")

tk.Button(left_panel, text="START", command=run_simulation).pack(pady=10)

label_time = tk.Label(left_panel, text="Czas: 0")
label_time.pack()

label_served = tk.Label(left_panel, text="Obsłużone: 0")
label_served.pack()


# Wizualizacja kanałów

tk.Label(window, text="Kanały", font=("Arial", 12, "bold")).pack()

channel_frame = tk.Frame(window)
channel_frame.pack(pady=10)

channel_boxes = []

for i in range(10):
    box = tk.Label(channel_frame, width=4, height=2, bg="lightgray", relief="solid")
    box.grid(row=0, column=i, padx=2)
    channel_boxes.append(box)


# Wykresy

fig, (ax_rho, ax_q, ax_w) = plt.subplots(3, 1, figsize=(5,6))
fig.tight_layout(pad=3)

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack()

window.mainloop()