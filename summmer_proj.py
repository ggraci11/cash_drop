import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class CashCountRegister(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cash Count Register")
        self.geometry("500x600")

        self.min_register = 100.00

        self.denominations = {
            "$100": 100.0,
            "$50": 50.0,
            "$20": 20.0,
            "$10": 10.0,
            "$5": 5.0,
            "$1": 1.0,
            "Quarters": 0.25,
            "Dimes": 0.10,
            "Nickels": 0.05,
            "Pennies": 0.01
        }

        self.entries = {}

        # Heading
        ctk.CTkLabel(self, text="Cash Count Register", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        # Create entries for each denomination
        for label, value in self.denominations.items():
            frame = ctk.CTkFrame(self)
            frame.pack(pady=5, padx=10, fill="x")

            ctk.CTkLabel(frame, text=label, width=80).pack(side="left", padx=10)
            entry = ctk.CTkEntry(frame, placeholder_text="0")
            entry.pack(side="right", padx=10, fill="x", expand=True)
            self.entries[label] = entry

        # Calculate button
        ctk.CTkButton(self, text="Calculate Total", command=self.calculate).pack(pady=20)

        # Results
        self.total_label = ctk.CTkLabel(self, text="Total: $0.00")
        self.total_label.pack(pady=5)

        self.drop_label = ctk.CTkLabel(self, text="Cash Drop: $0.00")
        self.drop_label.pack(pady=5)

        self.keep_label = ctk.CTkLabel(self, text="Keep in Register: $100.00")
        self.keep_label.pack(pady=5)

        # Reset button
        ctk.CTkButton(self, text="Clear", fg_color="red", command=self.clear_entries).pack(pady=10)

    def calculate(self):
        total = 0.0
        for label, value in self.denominations.items():
            count_str = self.entries[label].get()
            try:
                count = int(count_str) if count_str else 0
                total += count * value
            except ValueError:
                self.total_label.configure(text="Invalid input.")
                return

        drop_amount = max(0.0, total - self.min_register)

        self.total_label.configure(text=f"Total: ${total:.2f}")
        self.drop_label.configure(text=f"Cash Drop: ${drop_amount:.2f}")
        self.keep_label.configure(text=f"Keep in Register: ${self.min_register:.2f}")

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.total_label.configure(text="Total: $0.00")
        self.drop_label.configure(text="Cash Drop: $0.00")
        self.keep_label.configure(text="Keep in Register: $100.00")

if __name__ == "__main__":
    app = CashCountRegister()
    app.mainloop()
