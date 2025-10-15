import json
from typing import Optional
from .generator import FakeDataGenerator, AuthenticationError

def open_fake_data_gui(username: Optional[str] = None):
    """Temporary Tkinter-based UI to generate fake data for an authenticated user.
    This is intentionally simple and modular: can be removed when main GUI is implemented.
    """
    try:
        import tkinter as tk
        from tkinter import messagebox, filedialog
    except Exception:
        raise RuntimeError("Tkinter not available")

    def _on_generate():
        try:
            cnt = int(num_entry.get() or "0")
        except ValueError:
            messagebox.showerror("Input", "Please enter a valid integer for number of records.")
            return
        loc = locale_entry.get() or None
        seed_val = seed_entry.get() or None
        seed_val = int(seed_val) if seed_val and seed_val.isdigit() else None
        gen = FakeDataGenerator(locale=loc, seed=seed_val, authenticated_user=username)
        try:
            data = gen.generate(cnt)
        except AuthenticationError as e:
            messagebox.showerror("Auth", str(e))
            return

        # show/save
        if messagebox.askyesno("Save", "Save generated data to a file?"):
            path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
            if path:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, default=str)
                messagebox.showinfo("Saved", f"Wrote {len(data)} records to {path}")
        else:
            # show JSON in a readonly window
            out = tk.Toplevel(root)
            out.title("Generated Data Preview")
            txt = tk.Text(out, wrap="none", width=80, height=20)
            txt.insert("1.0", json.dumps(data, indent=2, default=str))
            txt.configure(state="disabled")
            txt.pack(fill="both", expand=True)

    root = tk.Tk()
    root.title("Fake Data Generator — Authenticated")
    root.geometry("420x240")

    tk.Label(root, text=f"User: {username}" if username else "User: (anonymous)").pack(pady=6)
    tk.Label(root, text="Number of records:").pack()
    num_entry = tk.Entry(root)
    num_entry.insert(0, "10")
    num_entry.pack()

    tk.Label(root, text="Locale (optional):").pack()
    locale_entry = tk.Entry(root)
    locale_entry.pack()

    tk.Label(root, text="Seed (optional integer):").pack()
    seed_entry = tk.Entry(root)
    seed_entry.pack()

    tk.Button(root, text="Generate", command=_on_generate, bg="#007bff", fg="white").pack(pady=10)
    root.mainloop()


if __name__ == "__main__":
    # Allow running the temporary GUI as a module: python -m utilities.fake_data_generator.gui
    open_fake_data_gui()