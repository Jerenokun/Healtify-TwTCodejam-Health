from tkinter.ttk import Notebook, Treeview
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
from plyer import notification
from datetime import datetime, date
import json as j


class App:
    stopwatch_time_var = 0
    stopwatch_running = False
    timer_inputted_time = 0
    timer_started = False
    timer_time_var = 0
    timer_running = False

    def __init__(self, master):
        self.master = master
        self.master.geometry("900x500")
        self.master.title("Healtify")
        self.master.resizable(False, False)
        self.master["bg"] = "grey90"
        Label(
            master,
            text="Healtify",
            font="Arial 21",
            bg="grey75",
            width=50,
            relief="groove",
        ).pack(pady=10)

    def create_main_frames(self):
        self.timer_stopwatch_frame = Frame(
            self.master,
            width=600,
            height=300,
            bg="grey95",
            relief="groove",
            borderwidth=2,
        )
        self.timer_stopwatch_frame.place(x=250, y=110)
        self.timer_stopwatch_frame.pack_propagate(False)
        self.daily_remind_frame = Frame(
            self.master,
            width=600,
            height=300,
            bg="grey97",
            relief="groove",
            borderwidth=2,
        )
        self.daily_remind_frame.pack_propagate(False)
        self.daily_remind_frame.place(x=250, y=110)
        self.appointment_frame = Frame(
            self.master,
            width=600,
            height=300,
            bg="grey97",
            relief="groove",
            borderwidth=2,
        )
        self.appointment_frame.pack_propagate(False)
        self.appointment_frame.place(x=250, y=110)

    def create_main_buttons(self):
        Button(
            self.master,
            text="Doctor\nAppointments",
            width=15,
            height=3,
            font="Arial 15 bold",
            relief="groove",
            bg="#FF3340",
            fg="white",
            command=lambda: self.raise_frame(self.appointment_frame),
        ).place(x=50, y=110)
        Button(
            self.master,
            text="Timer/\nstopwatch",
            width=15,
            height=3,
            font="Arial 15 bold",
            relief="groove",
            bg="#FfD55C",
            fg="white",
            command=lambda: self.raise_frame(self.timer_stopwatch_frame),
        ).place(x=50, y=210)
        Button(
            self.master,
            text="Daily reminders",
            width=15,
            height=3,
            font="Arial 15 bold",
            relief="groove",
            bg="#3CAEA3",
            fg="white",
            command=lambda: self.raise_frame(self.daily_remind_frame),
        ).place(x=50, y=310)

    def create_appointment_tab_widgets(self):
        Label(
            self.appointment_frame,
            text="Appointments",
            font="Arial 13 bold",
            bg="#FF3340",
            fg="white",
            relief="groove",
            width=20,
        ).pack(pady=5)
        self.appointment_entry = Entry(
            self.appointment_frame, width=30, font="Arial 12", relief="groove"
        )
        self.appointment_entry.pack(pady=20)
        self.warning_entry_label = Label(
            self.appointment_frame,
            font="Arial 10",
            text="this field needs to be answered",
            fg="red",
            bg="grey97",
        )
        self.warning_time_label = Label(
            self.appointment_frame,
            font="Arial 10",
            text="the time must be least\n5 minutes ahead",
            fg="red",
            bg="grey97",
        )
        self.Add_button = Button(
            self.appointment_frame,
            text="Add",
            relief="groove",
            width=7,
            command=self.appointments_add,
        ).place(x=180, y=85)
        self.edit_button = Button(
            self.appointment_frame,
            text="Edit",
            relief="groove",
            width=7,
            command=self.appointments_edit,
        ).place(x=265, y=85)
        self.Date_entry = DateEntry(
            self.appointment_frame,
            day=int(datetime.now().strftime("%d")),
            month=int(datetime.now().strftime("%m")),
            year=int(datetime.now().strftime("%Y")),
            state="readonly",
        )
        self.Date_entry.place(x=450, y=55)
        self.delete_button = Button(
            self.appointment_frame,
            text="Remove",
            relief="groove",
            width=7,
            command=self.appointments_delete,
        ).place(x=350, y=85)
        self.apppointment_scrollbar = Scrollbar(self.appointment_frame)
        self.apppointment_scrollbar.place(x=565, y=125, width=20, height=150)
        self.appointment_table = Treeview(
            self.appointment_frame,
            yscrollcommand=self.apppointment_scrollbar.set,
            height=6,
        )
        self.apppointment_scrollbar.config(command=self.appointment_table.yview)
        self.appointment_table["columns"] = ("Status", "Appointments", "Date", "Time")
        self.appointment_table.column("#0", width=0, minwidth=0)
        self.appointment_table.column("Status", anchor="center", width=100, minwidth=40)
        self.appointment_table.column(
            "Appointments", anchor="center", width=250, minwidth=120
        )
        self.appointment_table.column("Date", anchor="center", width=90, minwidth=110)
        self.appointment_table.column("Time", anchor="center", width=90, minwidth=110)
        self.appointment_table.heading("#0", text="Label")
        self.appointment_table.heading("Status", text="Status")
        self.appointment_table.heading("Appointments", text="Appointments")
        self.appointment_table.heading("Date", text="Date")
        self.appointment_table.heading("Time", text="Time")
        self.appointment_table.place(x=30, y=125)
        self.appointment_hour_spinbox = Spinbox(
            self.appointment_frame,
            font="Arial 10",
            width=2,
            from_=0,
            to=23,
            wrap=True,
            format="%02.0f",
            state="readonly",
        )
        self.appointment_hour_spinbox.place(x=470, y=80)
        self.appointment_min_spinbox = Spinbox(
            self.appointment_frame,
            font="Arial 10",
            width=2,
            from_=0,
            to=59,
            wrap=True,
            format="%02.0f",
            state="readonly",
        )
        self.appointment_min_spinbox.place(x=500, y=80)

    def create_timer_stopwatch_tab_widgets(self):
        Label(
            self.timer_stopwatch_frame,
            text="Timer and stopwatch",
            font="Arial 13 bold",
            bg="#FfD55C",
            fg="white",
            width=20,
            relief="groove",
        ).pack(pady=5)
        self.timer_stopwatch_nb = Notebook(
            self.timer_stopwatch_frame, width=570, height=200
        )
        self.timer_tab = Frame(
            self.timer_stopwatch_frame, width=570, height=200, bg="grey98"
        )
        self.stopwatch_tab = Frame(
            self.timer_stopwatch_frame, width=570, height=200, bg="grey98"
        )
        self.timer_stopwatch_nb.add(self.timer_tab, text="Timer")
        self.timer_stopwatch_nb.add(self.stopwatch_tab, text="Stopwatch")
        self.stopwatch_label = Label(
            self.stopwatch_tab,
            text="00:00:00.00",
            width=10,
            height=1,
            font="Arial 50 bold",
            bg="#808080",
            fg="white",
            relief="groove",
        )
        self.stopwatch_label.pack(pady=30)
        self.timer_stopwatch_nb.focus_set()
        self.timer_stopwatch_nb.pack()
        self.start_stop_stopwatch_button = Button(
            self.stopwatch_tab,
            text="start/stop",
            width=8,
            height=1,
            font="Arial 10",
            relief="groove",
            command=self.start_or_stop_stopwatch,
        )
        self.start_stop_stopwatch_button.place(x=190, y=120)
        self.reset_stopwatch_button = Button(
            self.stopwatch_tab,
            text="reset",
            width=8,
            height=1,
            font="Arial 10",
            relief="groove",
            state="disabled",
            command=self.reset_stopwatch,
        )
        self.reset_stopwatch_button.place(x=300, y=120)
        self.timer_hours_spinbox = Spinbox(
            self.timer_tab,
            font="Arial 40",
            width=2,
            from_=0,
            to=23,
            wrap=True,
            format="%02.0f",
            state="readonly",
            disabledbackground="#808080",
            readonlybackground="#808080",
            disabledforeground="grey90",
            fg="white",
            buttonbackground="#808080",
            relief="groove",
            bd=2,
        )
        self.timer_hours_spinbox.place(x=130, y=40)
        self.timer_mins_spinbox = Spinbox(
            self.timer_tab,
            font="Arial 40",
            width=2,
            from_=0,
            to=59,
            wrap=True,
            format="%02.0f",
            state="readonly",
            disabledbackground="#808080",
            readonlybackground="#808080",
            disabledforeground="grey90",
            fg="white",
            buttonbackground="#808080",
            relief="groove",
            bd=2,
        )
        self.timer_mins_spinbox.place(x=238, y=40)
        self.timer_secs_spinbox = Spinbox(
            self.timer_tab,
            font="Arial 40",
            width=2,
            from_=0,
            to=59,
            wrap=True,
            format="%02.0f",
            state="readonly",
            disabledbackground="#808080",
            readonlybackground="#808080",
            disabledforeground="grey90",
            fg="white",
            buttonbackground="#808080",
            relief="groove",
            bd=2,
        )
        self.timer_secs_spinbox.place(x=340, y=40)
        self.timer_start_button = Button(
            self.timer_tab,
            text="start/stop",
            width=7,
            font="Arial 10",
            relief="groove",
            command=self.start_or_stop_timer,
        )
        self.timer_start_button.place(x=185, y=120)
        self.timer_reset_button = Button(
            self.timer_tab,
            text="reset",
            width=7,
            font="Arial 10",
            relief="groove",
            command=self.reset_timer,
        )
        self.timer_reset_button.place(x=310, y=120)

    def create_daily_remind_tab_widgets(self):
        Label(
            self.daily_remind_frame,
            text="Reminders",
            width=15,
            font="Arial 13 bold",
            relief="groove",
            bg="#3CAEA3",
            fg="white",
        ).place(x=40, y=5)
        self.daily_remind_entry = Entry(self.daily_remind_frame, width=25)
        self.daily_remind_entry.place(x=40, y=45)
        self.daily_remind_hour_spinbox = Spinbox(
            self.daily_remind_frame,
            font="Arial 11",
            width=2,
            from_=0,
            to=23,
            wrap=True,
            format="%02.0f",
            state="readonly",
        )
        self.daily_remind_hour_spinbox.place(x=80, y=70)
        self.daily_remind_min_spinbox = Spinbox(
            self.daily_remind_frame,
            font="Arial 11",
            width=2,
            from_=0,
            to=59,
            wrap=True,
            format="%02.0f",
            state="readonly",
        )
        self.daily_remind_min_spinbox.place(x=120, y=70)
        self.daily_remind_add_button = Button(
            self.daily_remind_frame,
            width=5,
            text="add",
            font="Arial 10",
            relief="groove",
            command=self.daily_remind_add,
        ).place(x=30, y=100)
        self.daily_remind_edit_button = Button(
            self.daily_remind_frame,
            width=5,
            text="edit",
            font="Arial 10",
            relief="groove",
            command=self.daily_remind_edit,
        ).place(x=90, y=100)
        self.daily_remind_remove_button = Button(
            self.daily_remind_frame,
            width=5,
            text="remove",
            font="Arial 10",
            relief="groove",
            command=self.daily_remind_remove,
        ).place(x=150, y=100)
        self.daily_remind_mark_as_taken_button = Button(
            self.daily_remind_frame,
            width=11,
            text="Mark as taken",
            font="Arial 10",
            relief="groove",
            command=self.daily_remind_mark_as_taken,
        ).place(x=340, y=250)
        self.daily_remind_scrollbar = Scrollbar(self.daily_remind_frame)
        self.daily_remind_scrollbar.place(x=565, y=15, height=250)
        self.daily_remind_table = Treeview(
            self.daily_remind_frame,
            yscrollcommand=self.daily_remind_scrollbar.set,
            height=10,
        )
        self.daily_remind_scrollbar.config(command=self.daily_remind_table.yview)
        self.daily_remind_table["columns"] = (
            "Status",
            "Medications",
            "Time of the day",
        )
        self.daily_remind_table.column("#0", width=0, minwidth=0)
        self.daily_remind_table.column("Status", anchor="center", width=80, minwidth=80)
        self.daily_remind_table.column(
            "Medications", anchor="center", width=100, minwidth=40
        )
        self.daily_remind_table.column(
            "Time of the day", anchor="center", width=150, minwidth=90
        )
        self.daily_remind_table.heading("#0", text="")
        self.daily_remind_table.heading("Status", text="Status")
        self.daily_remind_table.heading("Medications", text="Medications")
        self.daily_remind_table.heading("Time of the day", text="Time of the day")
        self.daily_remind_table.place(x=230, y=10)

    def load_save_data(self):
        with open("data.json", "r") as f:
            contents = j.load(f)
            for item in contents["appointments_data"]:
                item_status = item[0]
                item_name = item[1]
                item_date = item[2]
                item_time = item[3]
                self.appointment_table.insert(
                    parent="",
                    iid=len(self.appointment_table.get_children()),
                    index=END,
                    text="",
                    values=(item_status, item_name, item_date, item_time),
                )
            for item in contents["daily_remind_data"]:
                item_status = item[0]
                item_name = item[1]
                item_time = item[2]
                self.daily_remind_table.insert(
                    parent="",
                    iid=len(self.daily_remind_table.get_children()),
                    index=END,
                    text="",
                    values=(item_status, item_name, item_time),
                )

    def run(self):
        self.master.after(1000, self.update_appointments_table)
        self.master.after(1000, self.update_timer)
        self.master.after(10, self.update_stopwatch)
        self.master.after(1000, self.update_daily_remind_table)
        self.master.mainloop()

    def raise_frame(self, frame):
        frame.tkraise()

    def start_or_stop_timer(self):
        self.timer_time_var = (
            int(self.timer_hours_spinbox.get()) * 3600
            + int(self.timer_mins_spinbox.get()) * 60
            + int(self.timer_secs_spinbox.get())
        )
        self.timer_running = (
            0 if self.timer_running else 0 if self.timer_time_var == 0 else 1
        )
        if not self.timer_started:
            self.timer_inputted_time = self.timer_time_var
            if self.timer_time_var > 0:
                self.timer_started = True

    def start_or_stop_stopwatch(self):
        self.stopwatch_running = 0 if self.stopwatch_running else 1

    def reset_timer(self):
        minutes, seconds = divmod(self.timer_inputted_time, 60)
        hours, minutes = divmod(minutes, 60)
        self.timer_running = False
        self.timer_started = False
        self.timer_inputted_time = 0
        self.timer_hours_spinbox["state"] = "normal"
        self.timer_mins_spinbox["state"] = "normal"
        self.timer_secs_spinbox["state"] = "normal"
        self.timer_hours_spinbox.delete(0, "end")
        self.timer_hours_spinbox.insert(0, str(hours).zfill(2))
        self.timer_mins_spinbox.delete(0, "end")
        self.timer_mins_spinbox.insert(0, str(minutes).zfill(2))
        self.timer_secs_spinbox.delete(0, "end")
        self.timer_secs_spinbox.insert(0, str(seconds).zfill(2))
        self.timer_hours_spinbox["state"] = "readonly"
        self.timer_mins_spinbox["state"] = "readonly"
        self.timer_secs_spinbox["state"] = "readonly"

    def reset_stopwatch(self):
        self.stopwatch_time_var = 0
        self.stopwatch_running = False
        self.stopwatch_label["text"] = "00:00:00.00"
        self.reset_stopwatch_button["state"] = "disabled"

    def check_entry_is_valid(self, edit=False):
        self.valid = False
        self.warning_entry_label.configure(text="this field needs to be answered")
        time_now = (
            int(datetime.now().strftime("%M")) + int(datetime.now().strftime("%H")) * 60
        )
        time_inp = (
            int(self.appointment_min_spinbox.get())
            + int(self.appointment_hour_spinbox.get()) * 60
        )

        def add_entry_warning():
            self.warning_entry_label.place(x=205, y=32)
            self.valid = False

        def remove_entry_warning():
            self.warning_entry_label.pack_forget()
            self.valid = True

        def add_time_warning():
            self.warning_time_label.place(x=433, y=15)
            self.valid = False

        def remove_time_warning():
            self.warning_time_label.place_forget()
            self.valid = True

        if self.appointment_entry.get().split():
            self.warning_entry_label.place_forget()
            date_now = date.today()
            date_inp = datetime.strptime(self.Date_entry.get(), "%m/%d/%y").date()
            if date_inp > date_now:
                if edit:
                    if self.appointment_table.selection():
                        remove_entry_warning()
                    else:
                        self.warning_entry_label.configure(
                            text="select an appointment to be edited"
                        )
                        add_entry_warning()
                else:
                    remove_time_warning()
            elif date_inp == date_now:
                print("yes")
                if time_inp - time_now >= 5:
                    if edit:
                        if self.appointment_table.selection():
                            remove_time_warning()
                        else:
                            self.warning_entry_label.configure(
                                text="select an appointment to be edited"
                            )
                            add_entry_warning()
                    else:
                        remove_time_warning()
                else:
                    add_time_warning()
            else:
                add_time_warning()
        else:
            add_entry_warning()
        return self.valid

    def appointments_add(self):
        if self.check_entry_is_valid():
            appointment_name = self.appointment_entry.get()
            appointment_date = self.Date_entry.get()
            appointment_time = f"{self.appointment_hour_spinbox.get()}:{self.appointment_min_spinbox.get()}"
            appointment_data = [
                "pending",
                appointment_name,
                appointment_date,
                appointment_time,
            ]
            appointment_iid = len(self.appointment_table.get_children())
            self.appointment_table.insert(
                parent="", iid=appointment_iid, index=END, values=appointment_data
            )
            with open("data.json", "r") as f:
                contents = j.load(f)
                contents["appointments_data"].append(appointment_data)
            with open("data.json", "w") as f:
                f.write(j.dumps(contents, indent=4))

    def appointments_delete(self):
        with open("data.json", "r") as f:
            contents = j.load(f)
        selection = self.appointment_table.selection()
        if selection:
            selection = selection[0]
            table_data = self.appointment_table.get_children()
            selection_index = table_data.index(selection)
            answer = messagebox.askyesno(
                "Delete appointment",
                "are you sure you want to delete this appointment?\nthis cannot be undone",
            )
            if answer:
                contents["appointments_data"].pop(selection_index)
                self.appointment_table.delete(self.appointment_table.selection())
        else:
            messagebox.showinfo("Unable to delete", "nothing was selected")
        with open("data.json", "w") as f:
            f.write(j.dumps(contents, indent=4))

    def appointments_edit(self):
        with open("data.json") as f:
            contents = j.load(f)
        if self.check_entry_is_valid(edit=True):
            print("yes")
            selection = self.appointment_table.selection()[0]
            table_data = self.daily_remind_table.get_children()
            selection_index = table_data.index(selection)
            appointment_name = self.appointment_entry.get()
            appointment_date = self.Date_entry.get()
            appointment_time = f"{self.appointment_hour_spinbox.get()}:{self.appointment_min_spinbox.get()}"
            appointment_data = [
                "pending",
                appointment_name,
                appointment_date,
                appointment_time,
            ]
            contents["appointments_data"][selection_index] = appointment_data
            self.appointment_table.item(
                self.appointment_table.selection(), values=appointment_data
            )
        with open("data.json", "w") as f:
            f.write(j.dumps(contents, indent=4))

    def daily_remind_add(self):
        with open("data.json", "r") as f:
            contents = j.load(f)
        if self.daily_remind_entry.get():
            daily_remind_medications_name = self.daily_remind_entry.get()
            daily_remind_medications_time = f"{self.daily_remind_hour_spinbox.get()}:{self.daily_remind_min_spinbox.get()}"
            daily_remind_medications_data = [
                "not yet taken",
                daily_remind_medications_name,
                daily_remind_medications_time,
            ]
            daily_remind_medications_iid = len(self.daily_remind_table.get_children())
            contents["daily_remind_data"].append(daily_remind_medications_data)
            self.daily_remind_table.insert(
                parent="",
                iid=daily_remind_medications_iid,
                index=END,
                text="",
                values=daily_remind_medications_data,
            )
        else:
            messagebox.showinfo("Unable to add", "Entrybox is empty")
        with open("data.json", "w") as f:
            f.write(j.dumps(contents, indent=4))

    def daily_remind_edit(self):
        with open("data.json", "r") as f:
            contents = j.load(f)
        print(self.daily_remind_table.selection())
        selection = self.daily_remind_table.selection()
        if selection:
            if self.daily_remind_entry.get():
                selection = selection[0]
                table_data = self.daily_remind_table.get_children()
                selection_index = table_data.index(selection)
                daily_remind_medication_name = self.daily_remind_entry.get()
                daily_remind_medication_time = f"{self.daily_remind_hour_spinbox.get()}:{self.daily_remind_min_spinbox.get()}"
                daily_remind_medication_data = [
                    "not yet taken",
                    daily_remind_medication_name,
                    daily_remind_medication_time,
                ]
                contents["daily_remind_data"][
                    selection_index
                ] = daily_remind_medication_data
                self.daily_remind_table.item(
                    self.daily_remind_table.selection(),
                    values=daily_remind_medication_data,
                )
            else:
                messagebox.showinfo("Unable to edit", "Entrybox is empty")
        else:
            messagebox.showinfo("Unable to edit", "Nothing was selected")
        with open("data.json", "w") as f:
            f.write(j.dumps(contents, indent=4))

    def daily_remind_remove(self):
        with open("data.json", "r") as f:
            contents = j.load(f)
        selection = self.daily_remind_table.selection()
        if selection:
            selection = selection[0]
            table_data = self.daily_remind_table.get_children()
            selection_index = table_data.index(selection)
            answer = messagebox.askyesno(
                "Delete Reminder",
                "Are you sure you want to delete this reminder?\nThis cannot be undone",
            )
            if answer:
                contents["daily_remind_data"].pop(selection_index)
                self.daily_remind_table.delete(self.daily_remind_table.selection())
        else:
            messagebox.showinfo("Unable to delete", "Nothing was selected")
        with open("data.json", "w") as f:
            f.write(j.dumps(contents, indent=4))

    def daily_remind_mark_as_taken(self):
        with open("data.json", "r") as f:
            contents = j.load(f)
        selection = self.daily_remind_table.selection()[0]
        if selection:
            daily_remind_status = self.daily_remind_table.item(selection, "values")[0]
            table_data = self.daily_remind_table.get_children()
            selection_index = table_data.index(selection)
            daily_remind_medications_data = self.daily_remind_table.item(
                self.daily_remind_table.selection(), "values"
            )
            daily_remind_medication_name = daily_remind_medications_data[1]
            daily_remind_medication_time = daily_remind_medications_data[2]
            daily_remind_medication_data = [
                "Taken",
                daily_remind_medication_name,
                daily_remind_medication_time,
            ]
            contents["daily_remind_data"][
                selection_index
            ] = daily_remind_medication_data
            self.daily_remind_table.item(
                self.daily_remind_table.selection(), values=daily_remind_medication_data
            )
        else:
            messagebox.showinfo("Unable to edit", "Nothing was selected")
        with open("data.json", "w") as f:
            f.write(j.dumps(contents, indent=4))

    def update_appointments_table(self):
        table = self.appointment_table.get_children()
        for item_num in range(0, len(table)):
            item_data = self.appointment_table.item(table[item_num], "values")
            item_status = item_data[0]
            item_name = item_data[1]
            item_date = item_data[2]
            item_time = item_data[3]
            if item_status == "pending" and (
                item_date < datetime.now().strftime("%#D")
                or item_time <= datetime.now().strftime("%H:%M")
                and item_date == datetime.now().strftime("%#D")
            ):
                with open("data.json", "r") as f:
                    contents = j.load(f)
                contents["appointments_data"][item_num] = (
                    "started",
                    item_name,
                    item_date,
                    item_time,
                )
                notification.notify(
                    title=f"your appointment, {item_name}, has started",
                    app_name="health app",
                    toast=True,
                )
                self.appointment_table.item(
                    table[item_num], values=("started", item_name, item_date, item_time)
                )
                with open("data.json", "w") as f:
                    f.write(j.dumps(contents, indent=4))
        self.master.after(1000, self.update_appointments_table)

    def update_timer(self):
        if self.timer_running:
            self.timer_hours_spinbox["state"] = "normal"
            self.timer_mins_spinbox["state"] = "normal"
            self.timer_secs_spinbox["state"] = "normal"
            if self.timer_time_var > 0:
                self.timer_time_var -= 1
                minutes, seconds = divmod(self.timer_time_var, 60)
                hours, minutes = divmod(minutes, 60)
                self.timer_hours_spinbox.delete(0, "end")
                self.timer_hours_spinbox.insert(0, str(hours).zfill(2))
                self.timer_mins_spinbox.delete(0, "end")
                self.timer_mins_spinbox.insert(0, str(minutes).zfill(2))
                self.timer_secs_spinbox.delete(0, "end")
                self.timer_secs_spinbox.insert(0, str(seconds).zfill(2))
                self.timer_hours_spinbox["state"] = "disabled"
                self.timer_mins_spinbox["state"] = "disabled"
                self.timer_secs_spinbox["state"] = "disabled"
            else:
                messagebox.showinfo("Healtify", "The timer has ended")
                self.timer_hours_spinbox["state"] = "readonly"
                self.timer_mins_spinbox["state"] = "readonly"
                self.timer_secs_spinbox["state"] = "readonly"
                self.timer_running = False
                self.timer_started = False
                self.timer_inputted_time = 0
        else:
            minutes, seconds = divmod(self.timer_time_var, 60)
            hours, minutes = divmod(minutes, 60)
        self.master.after(1000, self.update_timer)

    def update_stopwatch(self):
        if self.stopwatch_running:
            seconds, miliseconds = divmod(self.stopwatch_time_var, 100)
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            time_text = f"{hours:02}:{minutes:02}:{seconds:02}.{miliseconds:02}"
            self.stopwatch_label["text"] = time_text
            self.reset_stopwatch_button["state"] = "normal"
            self.stopwatch_time_var += 1
        self.master.after(10, self.update_stopwatch)

    def update_daily_remind_table(self):
        table_data = self.daily_remind_table.get_children()
        for item in range(len(table_data)):
            with open("data.json", "r") as f:
                contents = j.load(f)
            item_data = self.daily_remind_table.item(table_data[item], "values")
            item_status = item_data[0]
            item_medication = item_data[1]
            item_time = item_data[2]
            if (
                item_time <= datetime.now().strftime("%H:%M")
                and item_status == "not yet taken"
            ):
                self.daily_remind_table.item(
                    item, values=("notified", item_medication, item_time)
                )
                contents["daily_remind_data"][item] = [
                    "notified",
                    item_medication,
                    item_time,
                ]
                notification.notify(
                    title=f"Don't forget to take {item_medication}!",
                    message="Take your medication",
                    app_name="Healtify",
                    toast=True,
                )
            with open("data.json", "w") as f:
                f.write(j.dumps(contents, indent=4))
        self.master.after(1000, self.update_daily_remind_table)


if __name__ == "__main__":
    main = Tk()
    app = App(main)
    app.create_main_frames()
    app.create_main_buttons()
    app.create_appointment_tab_widgets()
    app.create_daily_remind_tab_widgets()
    app.create_timer_stopwatch_tab_widgets()
    app.load_save_data()
    app.run()
