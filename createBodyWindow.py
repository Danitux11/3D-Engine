import tkinter as tk
from tkinter import ttk

def open_secondary_window(window):
    values = {}
    def on_done():
        if shape_var.get() == "None":
            values['Vertices'] = vertices_var.get()
            values['Edges'] = edges_var.get()
        else:
            values['Shape'] = shape_var.get()
        values['Position'] = [position_vars[i].get() for i in range(3)]
        if advanced_options_var.get():
            values['Angular Velocity'] = [angular_velocity_vars[i].get() for i in range(3)]
            values['Angular Acceleration'] = [angular_acceleration_vars[i].get() for i in range(3)]
            values['Translational Velocity'] = [translational_velocity_vars[i].get() for i in range(3)]
            values['Translational Acceleration'] = [translational_acceleration_vars[i].get() for i in range(3)]
        else:
            values['Angular Velocity'] = [0, 0, 0]
            values['Angular Acceleration'] = [0, 0, 0]
            values['Translational Velocity'] = [0, 0, 0]
            values['Translational Acceleration'] = [0, 0, 0]
        secondary_window.destroy()

    def toggle_advanced_options():
        state = tk.NORMAL if advanced_options_var.get() else tk.DISABLED
        for widgets in angular_velocity_entries + angular_acceleration_entries + translational_velocity_entries + translational_acceleration_entries:
            widgets.config(state=state)

    def toggle_shape():
        state = tk.NORMAL if shape_var.get() == "None" else tk.DISABLED
        vertices_entry.config(state=state)
        edges_entry.config(state=state)

    secondary_window = tk.Toplevel(window)
    secondary_window.title("Create New Body")

    position_vars = [tk.DoubleVar(value=0) for _ in range(3)]
    angular_velocity_vars = [tk.DoubleVar(value=0) for _ in range(3)]
    angular_acceleration_vars = [tk.DoubleVar(value=0) for _ in range(3)]
    translational_velocity_vars = [tk.DoubleVar(value=0) for _ in range(3)]
    translational_acceleration_vars = [tk.DoubleVar(value=0) for _ in range(3)]

    vertices_var = tk.StringVar()
    edges_var = tk.StringVar()
    shape_var = tk.StringVar(value="None")
    advanced_options_var = tk.BooleanVar(value=False)

    container = ttk.Frame(secondary_window)
    container.grid(row=0, column=0, padx=10, pady=10)

    ttk.Label(container, text="Shape:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    shape_menu = ttk.OptionMenu(container, shape_var, "None", "None", "Cube", "Pyramid", command=lambda _: toggle_shape())
    shape_menu.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(container, text="Vertices:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    vertices_entry = ttk.Entry(container, textvariable=vertices_var)
    vertices_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(container, text="Edges:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    edges_entry = ttk.Entry(container, textvariable=edges_var)
    edges_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(container, text="Position (x, y, z):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    position_entries = [ttk.Entry(container, textvariable=position_vars[i]) for i in range(3)]
    for i, entry in enumerate(position_entries):
        entry.grid(row=3, column=i + 1, padx=5, pady=5)

    ttk.Checkbutton(container, text="Advanced Options", variable=advanced_options_var, command=toggle_advanced_options).grid(row=4, column=0, columnspan=4, pady=10, sticky="w")

    ttk.Label(container, text="Angular Velocity (x, y, z):").grid(row=5, column=0, padx=5, pady=5, sticky="w")
    angular_velocity_entries = [ttk.Entry(container, textvariable=angular_velocity_vars[i]) for i in range(3)]
    for i, entry in enumerate(angular_velocity_entries):
        entry.grid(row=5, column=i + 1, padx=5, pady=5)

    ttk.Label(container, text="Angular Acceleration (x, y, z):").grid(row=6, column=0, padx=5, pady=5, sticky="w")
    angular_acceleration_entries = [ttk.Entry(container, textvariable=angular_acceleration_vars[i]) for i in range(3)]
    for i, entry in enumerate(angular_acceleration_entries):
        entry.grid(row=6, column=i + 1, padx=5, pady=5)

    ttk.Label(container, text="Translational Velocity (x, y, z):").grid(row=7, column=0, padx=5, pady=5, sticky="w")
    translational_velocity_entries = [ttk.Entry(container, textvariable=translational_velocity_vars[i]) for i in range(3)]
    for i, entry in enumerate(translational_velocity_entries):
        entry.grid(row=7, column=i + 1, padx=5, pady=5)

    ttk.Label(container, text="Translational Acceleration (x, y, z):").grid(row=8, column=0, padx=5, pady=5, sticky="w")
    translational_acceleration_entries = [ttk.Entry(container, textvariable=translational_acceleration_vars[i]) for i in range(3)]
    for i, entry in enumerate(translational_acceleration_entries):
        entry.grid(row=8, column=i + 1, padx=5, pady=5)

    toggle_advanced_options()

    ttk.Button(container, text="Done", command=lambda: on_done()).grid(row=9, column=0, columnspan=4, pady=10)
    window.wait_window(secondary_window)
    return values