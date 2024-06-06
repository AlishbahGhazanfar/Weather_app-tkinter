#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import datetime

def create_db():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                    date TEXT,
                    location TEXT,
                    temperature INTEGER,
                    precipitation REAL
                 )''')
    conn.commit()
    conn.close()

def insert_data(date, location, temperature, precipitation):
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('INSERT INTO weather_data (date, location, temperature, precipitation) VALUES (?, ?, ?, ?)',
              (date, location, temperature, precipitation))
    conn.commit()
    conn.close()

def fetch_data():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('SELECT * FROM weather_data')
    records = c.fetchall()
    conn.close()
    return records

def update_text():
    records = fetch_data()
    display_text = '\n'.join([f"{record[0]} - {record[1]} - Temp: {record[2]} C - Precip: {record[3]} mm" for record in records])
    text_area.config(state=tk.NORMAL)
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, display_text)
    text_area.config(state=tk.DISABLED)

def export_data():
    records = fetch_data()
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not filename:
        return
    with open(filename, 'w') as f:
        for record in records:
            f.write(f"{record[0]} - {record[1]} - Temp: {record[2]} C - Precip: {record[3]} mm\n")
    messagebox.showinfo("Export Successful", "Data exported successfully!")

def add_data():
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    location = location_entry.get()
    temperature = int(temperature_entry.get())
    precipitation = float(precipitation_entry.get())
    insert_data(date, location, temperature, precipitation)
    update_text()
    location_entry.delete(0, tk.END)
    temperature_entry.delete(0, tk.END)
    precipitation_entry.delete(0, tk.END)

app = tk.Tk()
app.title("Weather Data Application")

create_db()

tk.Label(app, text="Location:").grid(row=0, column=0)
location_entry = tk.Entry(app)
location_entry.grid(row=0, column=1)

tk.Label(app, text="Temperature (C):").grid(row=1, column=0)
temperature_entry = tk.Entry(app)
temperature_entry.grid(row=1, column=1)

tk.Label(app, text="Precipitation (mm):").grid(row=2, column=0)
precipitation_entry = tk.Entry(app)
precipitation_entry.grid(row=2, column=1)

add_button = tk.Button(app, text="Add Data", command=add_data)
add_button.grid(row=3, columnspan=2)

export_button = tk.Button(app, text="Export Data", command=export_data)
export_button.grid(row=4, columnspan=2)

text_area = tk.Text(app, height=10, width=50, state=tk.DISABLED)
text_area.grid(row=5, columnspan=2)

update_text()

app.mainloop()


# In[ ]:




