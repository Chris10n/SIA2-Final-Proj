import json
import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Dict, Any

from generator import FakeDataGenerator


class FakeDataGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fake Data Generator")
        self.geometry("700x500")

        self.locale_var = tk.StringVar(value="en_US")
        self.seed_var = tk.StringVar(value="42")
        self.count_var = tk.IntVar(value=10)

        self._build_ui()
        self.generated: List[Dict[str, Any]] = []

    def _build_ui(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(frm)
        top.pack(fill=tk.X)

        ttk.Label(top, text="Locale:").grid(column=0, row=0, sticky=tk.W)
        ttk.Entry(top, textvariable=self.locale_var, width=12).grid(column=1, row=0, sticky=tk.W)

        ttk.Label(top, text="Seed:").grid(column=2, row=0, sticky=tk.W, padx=(10, 0))
        ttk.Entry(top, textvariable=self.seed_var, width=8).grid(column=3, row=0, sticky=tk.W)

        ttk.Label(top, text="Count:").grid(column=4, row=0, sticky=tk.W, padx=(10, 0))
        ttk.Entry(top, textvariable=self.count_var, width=6).grid(column=5, row=0, sticky=tk.W)

        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(btn_frame, text="Generate Preview", command=self.generate_preview).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Save as JSON", command=self.save_json).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text="Save as CSV", command=self.save_csv).pack(side=tk.LEFT)

        # Treeview for preview
        self.tree = ttk.Treeview(frm, columns=("name", "email", "company"), show="headings")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("company", text="Company")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    def generate_preview(self):
        try:
            locale = self.locale_var.get().strip() or None
            seed = int(self.seed_var.get()) if self.seed_var.get().strip() else None
            count = int(self.count_var.get())
        except ValueError:
            messagebox.showerror("Input error", "Seed and Count must be integers")
            return

        g = FakeDataGenerator(locale=locale, seed=seed)
        self.generated = g.generate(count)
        self._populate_tree()

    def _populate_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.generated:
            self.tree.insert("", "end", values=(row.get("name"), row.get("email"), row.get("company")))

    def save_json(self):
        if not self.generated:
            messagebox.showinfo("No data", "Generate data first")
            return
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.generated, f, indent=2, default=str)
        messagebox.showinfo("Saved", f"Wrote {len(self.generated)} records to {path}")

    def save_csv(self):
        if not self.generated:
            messagebox.showinfo("No data", "Generate data first")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        keys = list(self.generated[0].keys())
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(self.generated)
        messagebox.showinfo("Saved", f"Wrote {len(self.generated)} records to {path}")


def main():
    app = FakeDataGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
