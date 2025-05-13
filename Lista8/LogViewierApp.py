from __future__ import annotations
from datetime import datetime, time
from pathlib import Path
from typing import List, Optional
import pytz
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkcalendar import DateEntry
from LogLoader import LogLoader
from HttpLog import HttpLog

UTC = pytz.utc
MISSING_VALUE_SIGN = "—"


class LogViewerGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("HTTP Log Viewer – Tkinter")
        self.geometry("1000x600")

        self.loader = LogLoader()
        self._current_logs: List[HttpLog] = []
        self._count: int = 0

        self._build_widgets()

    def _build_widgets(self) -> None:
        top_bar = ttk.Frame(self)
        top_bar.pack(fill="x", padx=10, pady=5)

        load_btn = ttk.Button(top_bar, text="Load log file…", command=self._load_file)
        load_btn.pack(side="left")

        ttk.Label(top_bar, text="From:").pack(side="left", padx=(20, 2))
        self.start_date = DateEntry(top_bar, date_pattern="yyyy-mm-dd")
        self.start_date.pack(side="left")

        ttk.Label(top_bar, text="to:").pack(side="left", padx=2)
        self.end_date = DateEntry(top_bar, date_pattern="yyyy-mm-dd")
        self.end_date.pack(side="left")

        filter_btn = ttk.Button(top_bar, text="Filter", command=self._apply_filter)
        filter_btn.pack(side="left", padx=10)

        main_pane = ttk.PanedWindow(self, orient="horizontal")
        main_pane.pack(fill="both", expand=True, padx=10, pady=5)

        master_frame = ttk.Frame(main_pane)
        self.listbox = tk.Listbox(master_frame, exportselection=False)
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        self.listbox.bind("<Up>", lambda e: (self._navigate(-1), "break"))
        self.listbox.bind("<Down>", lambda e: (self._navigate(1), "break"))

        scrollbar = ttk.Scrollbar(master_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        main_pane.add(master_frame, weight=1)

        detail_frame = ttk.Frame(main_pane, padding=16)
        self.detail_vars: dict[str, tk.StringVar] = {}

        style = ttk.Style(detail_frame)
        style.configure("Detail.TEntry", fieldbackground="white", foreground="black")

        rows_conf = [
            ("Remote host", "Remote host", 20),
            ("Identity", "Identity", 16),
            ("Username", "Username", 16),
            ("Timestamp", "Timestamp", 24),
            ("Timezone", "Timezone", 18),
            ("Method", "Method", 8),
            ("Request", "Request", 70),
            ("Response size", "Response size", 12),
            ("Referer", "Referer", 70),
            ("User-Agent", "User-Agent", 70),
        ]

        for row, (caption, key, width) in enumerate(rows_conf):
            ttk.Label(detail_frame, text=f"{caption}:").grid(
                row=row, column=0, sticky="e", pady=3, padx=(0, 6)
            )
            var = tk.StringVar(value=MISSING_VALUE_SIGN)
            self.detail_vars[key] = var
            ent = ttk.Entry(
                detail_frame,
                textvariable=var,
                state="readonly",
                width=width,
                style="Detail.TEntry",
            )
            ent.grid(row=row, column=1, sticky="w", pady=3)

        status_row = len(rows_conf)
        ttk.Label(detail_frame, text="Status code:").grid(
            row=status_row, column=0, sticky="e", pady=(12, 3), padx=(0, 6)
        )
        self.status_var = tk.StringVar(value=MISSING_VALUE_SIGN)
        self.status_lbl = tk.Label(
            detail_frame,
            textvariable=self.status_var,
            width=6,
            font=("TkDefaultFont", 10, "bold"),
            relief="groove",
            bd=2,
        )
        self.status_lbl.grid(row=status_row, column=1, sticky="w", pady=(12, 3))

        main_pane.add(detail_frame, weight=3)

        bottom_bar = ttk.Frame(self)
        bottom_bar.pack(fill="x", padx=10, pady=5)

        self.next_btn = ttk.Button(bottom_bar, text="Next", command=lambda: self._navigate(1))
        self.next_btn.pack(side="right", padx=5)

        self.prev_btn = ttk.Button(bottom_bar, text="Previous", command=lambda: self._navigate(-1))
        self.prev_btn.pack(side="right")

        self._update_nav_buttons()

    def _load_file(self) -> None:
        filepath = filedialog.askopenfilename(title="Open log file",filetypes=[("Log files", "*.log *.txt")])
        if not filepath:
            return

        try:
            self.loader.load_logs(filepath)
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to load log file:\n{exc}")
            return

        self.status_message(f"Loaded {len(self.loader)} log entries from {Path(filepath).name}")
        self._populate_master(self.loader.get_all_logs())

    def _populate_master(self, logs: List[HttpLog]) -> None:
        self._current_logs = logs
        self._count = len(logs)

        self.listbox.delete(0, tk.END)
        for log in logs:
            self.listbox.insert(tk.END, log.preview)
        self.listbox.selection_clear(0, tk.END)

        self.display_log(None)
        self._update_nav_buttons()

    def _apply_filter(self) -> None:
        if self._count == 0:
            return
        start_dt = datetime.combine(self.start_date.get_date(), time.min).replace(tzinfo=UTC)
        end_dt = datetime.combine(self.end_date.get_date(), time.max).replace(tzinfo=UTC)
        filtered = self.loader.get_filtered_logs(start_dt, end_dt)
        self._populate_master(filtered)

    def _on_select(self, _event=None) -> None:
        sel = self.listbox.curselection()
        if sel:
            idx = int(sel[0])
            self.display_log(self._current_logs[idx])
        self._update_nav_buttons()

    def display_log(self, log: Optional[HttpLog]) -> None:
        def _set(key: str, value: str | None) -> None:
            self.detail_vars[key].set(value or MISSING_VALUE_SIGN)

        if log is None:
            for var in (*self.detail_vars.values(), self.status_var):
                var.set(MISSING_VALUE_SIGN)
            self.status_lbl.config(bg=self.cget("background"))
            return

        _set("Remote host", log.remote_host)
        _set("Identity", log.identity)
        _set("Username", log.username)
        _set("Timestamp", str(log.timestamp))
        _set("Timezone", log.timezone)
        _set("Method", log.method)
        _set("Request", log.request_line_without_method)
        _set("Response size", str(log.response_size))
        _set("Referer", log.referer)
        _set("User-Agent", log.user_agent)

        code = log.status_code
        self.status_var.set(str(code))
        bg = (
            "#4CAF50" if 200 <= code < 300 else
            "#FFC107" if 300 <= code < 400 else
            "#FF9800" if 400 <= code < 500 else
            "#F44336"
        )
        self.status_lbl.config(bg=bg, fg="white")


    def _navigate(self, delta: int) -> None:
        if self._count == 0:
            return
        sel = self.listbox.curselection()
        row = int(sel[0]) if sel else -1
        target = row + delta
        if 0 <= target < self._count:
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(target)
            self.listbox.see(target)
            self.display_log(self._current_logs[target])
        self._update_nav_buttons()

    def _update_nav_buttons(self) -> None:
        sel = self.listbox.curselection()
        row = int(sel[0]) if sel else -1
        self.prev_btn["state"] = tk.NORMAL if row > 0 else tk.DISABLED
        self.next_btn["state"] = tk.NORMAL if 0 <= row < self._count - 1 else tk.DISABLED

    def status_message(self, text: str) -> None:
        self.title(f"HTTP Log Viewer – {text}")
        self.after(5000, lambda: self.title("HTTP Log Viewer – Tkinter"))



def main() -> None:
    LogViewerGUI().mainloop()


if __name__ == "__main__":
    main()
