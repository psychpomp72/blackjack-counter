import tkinter as tk
from tkinter import messagebox
import time

class CounterApp:
    def __init__(self, master):
        self.master = master
        master.title("BlackJack Counter")
        master.geometry("500x700") # Initial window size
        master.configure(bg="#F0F0F0")

        # --- Set Minimum Size ---
        master.minsize(500, 750) # Minimum width, Minimum height

        self.current_number = 0
        self.total_presses = 0
        self.history = []

        # --- Debounce Mechanism ---
        self.last_key_press_time = {}
        self.debounce_delay_ms = 50 # Set a default debounce delay, e.g., 50ms

        # --- Keyboard Bindings (Corrected Delete Key Binding) ---
        master.bind('a', lambda event: self._debounced_action(self.plus_one, 'a'))
        master.bind('s', lambda event: self._debounced_action(self.plus_zero, 's'))
        master.bind('d', lambda event: self._debounced_action(self.minus_one, 'd'))
        master.bind('r', lambda event: self._debounced_action(self.reset_all, 'r'))
        # Corrected binding from '<e>' to '<Delete>' to match button text
        master.bind('<Delete>', lambda event: self._debounced_action(self.delete_last_history_entry, 'Delete'))


        # --- GUI Elements ---
        comic_sans_large = ("Comic Sans MS", 60, "bold")
        comic_sans_medium = ("Comic Sans MS", 20, "bold")
        comic_sans_small = ("Comic Sans MS", 14)
        comic_sans_history = ("Comic Sans MS", 12)
        comic_sans_button_small = ("Comic Sans MS", 11)

        self.number_label = tk.Label(master, text=str(self.current_number),
                                     font=comic_sans_large,
                                     bg="#4CAF50", fg="white",
                                     relief=tk.RIDGE, bd=5)
        self.number_label.pack(pady=30, ipadx=20, ipady=10)

        button_frame = tk.Frame(master, bg="#F0F0F0")
        button_frame.pack(pady=10)

        button_width = 8
        button_height = 2
        button_padx = 7

        self.plus_button = tk.Button(button_frame, text="+1", command=lambda: self._debounced_action(self.plus_one, 'a'),
                                     font=comic_sans_medium, width=button_width, height=button_height,
                                     bg="#2196F3", fg="white", activebackground="#1976D2")
        self.plus_button.pack(side=tk.LEFT, padx=button_padx)

        self.plus_zero_button = tk.Button(button_frame, text="+0", command=lambda: self._debounced_action(self.plus_zero, 's'),
                                          font=comic_sans_medium, width=button_width, height=button_height,
                                          bg="#FFC107", fg="black", activebackground="#FFA000")
        self.plus_zero_button.pack(side=tk.LEFT, padx=button_padx)

        self.minus_button = tk.Button(button_frame, text="-1", command=lambda: self._debounced_action(self.minus_one, 'd'),
                                      font=comic_sans_medium, width=button_width, height=button_height,
                                      bg="#F44336", fg="white", activebackground="#D32F2F")
        self.minus_button.pack(side=tk.LEFT, padx=button_padx)

        self.total_presses_label = tk.Label(master, text=f"Total Button Presses: {self.total_presses}",
                                             font=comic_sans_small, bg="#F0F0F0", fg="#333333")
        self.total_presses_label.pack(pady=10)

        history_frame = tk.LabelFrame(master, text="Action History", padx=10, pady=10,
                                      bg="#F8F8F8", fg="#333333", font=("Comic Sans MS", 12, "bold"))
        history_frame.pack(pady=15, fill=tk.BOTH, expand=True, padx=20)

        self.history_listbox = tk.Listbox(history_frame, height=10, font=comic_sans_history,
                                          bg="white", fg="#333333", selectbackground="#AED6F1", selectforeground="black")
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        history_scrollbar = tk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=history_scrollbar.set)

        control_button_frame = tk.Frame(master, bg="#F0F0F0")
        control_button_frame.pack(pady=10)

        self.delete_history_button = tk.Button(control_button_frame, text="Delete Last (Del Key)", command=lambda: self._debounced_action(self.delete_last_history_entry, 'Delete'),
                                               font=comic_sans_button_small, bg="#9E9E9E", fg="white", activebackground="#757575")
        self.delete_history_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(control_button_frame, text="Reset All (R)", command=lambda: self._debounced_action(self.reset_all, 'r'),
                                       font=comic_sans_button_small, bg="#607D8B", fg="white", activebackground="#455A64")
        self.reset_button.pack(side=tk.LEFT, padx=5)

    def _debounced_action(self, action_func, key_identifier):
        current_time = time.time()
        last_time = self.last_key_press_time.get(key_identifier, 0)

        if (current_time - last_time) * 1000 >= self.debounce_delay_ms:
            self.last_key_press_time[key_identifier] = current_time
            action_func()

    def _record_action(self, action_type, value_changed_by):
        # We store the state *before* the change, so we can revert it easily
        previous_number = self.current_number
        self.history.append((action_type, value_changed_by, previous_number))
        self.total_presses += 1

        # Apply the change
        self.current_number += value_changed_by

        self.update_display()
        self._update_history_listbox()

    def plus_one(self):
        self._record_action("+1", 1)

    def minus_one(self):
        self._record_action("-1", -1)

    def plus_zero(self):
        # For "+0", the value doesn't change, so we pass 0
        self._record_action("+0", 0)

    def update_display(self):
        self.number_label.config(text=str(self.current_number))
        self.total_presses_label.config(text=f"Total Button Presses: {self.total_presses}")

    def _update_history_listbox(self):
        self.history_listbox.delete(0, tk.END)
        # We need the total *after* the action for display
        for i, (action, value, prev_total) in enumerate(reversed(self.history)):
            current_total = prev_total + value
            self.history_listbox.insert(tk.END, f"{len(self.history) - i}. {action} (Total: {current_total})")
        self.history_listbox.see(0)

    def delete_last_history_entry(self):
        if not self.history:
            return

        try:
            # Pop the last action from history
            _action, value_changed_by, previous_number = self.history.pop()

            # Revert the state
            self.total_presses -= 1
            self.current_number -= value_changed_by # Subtract the value that was added

            self.update_display()
            self._update_history_listbox()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during deletion: {e}")

    def reset_all(self):
        confirm = messagebox.askyesno(
            "Confirm Reset",
            "Are you sure you want to reset everything? This will clear all history and set the number to zero."
        )
        if confirm:
            self.current_number = 0
            self.total_presses = 0
            self.history = []
            self.update_display()
            self._update_history_listbox()
            messagebox.showinfo("Reset Complete", "All data has been reset.")


root = tk.Tk()
app = CounterApp(root)
root.mainloop()