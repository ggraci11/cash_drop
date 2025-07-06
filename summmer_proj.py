import sqlite3
import customtkinter as ctk
from tkinter import messagebox

connection = sqlite3.connect('store_resisterinfo.db')
cursor = connection.cursor()

#create table for credentials
command1 = """CREATE TABLE IF NOT EXISTS
credentials(username TEXT PRIMARY KEY, password TEXT)"""
cursor.execute(command1)

#create table for day to day records (total money, deposit, money left for register)
command2 = """CREATE TABLE IF NOT EXISTS
records(id INTEGER, date STRING PRIMARY KEY, totalMoney FLOAT, deposit FLOAT, keepInReg FLOAT)"""
cursor.execute(command2)
connection.commit()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


class LoginRegisterWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login / Register")
        self.geometry("500x300")

        self.login_label = ctk.CTkLabel(self, text="Login / Register", font=ctk.CTkFont(size=20, weight="bold"))
        self.login_label.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=5)
        ctk.CTkButton(self, text="Register", command=self.register).pack(pady=5)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        cursor.execute("SELECT * FROM credentials WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Login", "Login successful!")
            self.destroy()
            CashCountRegister().mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Register", "Please fill in both fields.")
            return

        try:
            cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)", (username, password))
            connection.commit()
            messagebox.showinfo("Register", "Account created successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Register Failed", "Username already exists.")
            


class CashCountRegister(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cash Count Register")
        self.geometry("800x800")

        self.min_register = 100.00 # would need alteration to make value adjustable

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
        ctk.CTkLabel(self, text="Cash Count Register", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

        # Create entries for each denomination
        for label, value in self.denominations.items():
            frame = ctk.CTkFrame(self)
            frame.pack(pady=3, padx=50, fill="x")

            ctk.CTkLabel(frame, text=label, width=50).pack(side="left", padx=10)
            entry = ctk.CTkEntry(frame, placeholder_text="0")
            entry.pack(side="right", padx=10, fill="x", expand=True)
            self.entries[label] = entry

        # Date entry
        date_frame = ctk.CTkFrame(self)
        date_frame.pack(pady=5, padx=50, fill="x")
        ctk.CTkLabel(date_frame, text="Date (MM-DD-YYYY):", width=50).pack(side="left", padx=10)
        self.date_entry = ctk.CTkEntry(date_frame, placeholder_text="06-27-2025")
        self.date_entry.pack(side="right", padx=10, fill="x", expand=True)

        # Save button
        ctk.CTkButton(self, text="Save", command=self.save_data).pack(pady=10)
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

        ctk.CTkButton(self, text="Logout", fg_color="gray", command=self.logout).pack(pady=10)

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
        self._last_total = total
        self._last_drop = drop_amount

    def save_data(self):
        date = self.date_entry.get().strip()
        if not date:
            return
           
        self.calculate()
        
        cursor.execute(
            "INSERT OR REPLACE INTO records (date, totalMoney, deposit, keepInReg) VALUES (?, ?, ?, ?)",
            (date, self._last_total, self._last_drop, self.min_register)
        )
        connection.commit()
        print(f"Data saved for {date}: Total: ${self._last_total}, Cash Drop: ${self._last_drop}, Keep in Register: ${self.min_register}")

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.total_label.configure(text="Total: $0.00")
        self.drop_label.configure(text="Cash Drop: $0.00")
        self.keep_label.configure(text="Keep in Register: $100.00")

    def logout(self):
        self.destroy()
        LoginRegisterWindow().mainloop()


if __name__ == "__main__":
    app = LoginRegisterWindow()
    app.mainloop()
# Close the database connection when the application exits
connection.close()