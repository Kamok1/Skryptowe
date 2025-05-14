from __future__ import annotations

from datetime import datetime, time
from pathlib import Path
from typing import List, Optional

import pytz
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkcalendar import DateEntry

from Lista8.FieldKey import FieldKey
from LogLoader import LogLoader
from HttpLog import HttpLog

UTC = pytz.utc
MISSING_VALUE = "-"
DATE_PATTERN = "dd.mm.yyyy"
STRFTIME_PATTERN = DATE_PATTERN.replace("dd", "%d").replace("mm", "%m").replace("yyyy", "%Y")

class FilterBar(ttk.Frame):
    def __init__(self, parent, load_log_callback, apply_filter_callback) -> None:
        super().__init__(parent)
        self.pack(fill="x", padx=10, pady=5)
        ttk.Button(self, text="Load log file…", command=load_log_callback).pack(side="left")
        ttk.Label(self, text="From:").pack(side="left", padx=(20, 2))
        self.start_date_picker = DateEntry(self, date_pattern=DATE_PATTERN)
        self.start_date_picker.pack(side="left")
        ttk.Label(self, text="To:").pack(side="left", padx=2)
        self.end_date_picker = DateEntry(self, date_pattern=DATE_PATTERN)
        self.end_date_picker.pack(side="left")
        ttk.Button(self, text="Apply Filter", command=self._on_apply_filter).pack(side="left", padx=10)
        self._apply_filter_callback = apply_filter_callback

    def _on_apply_filter(self) -> None:
        start_datetime = datetime.combine(self.start_date_picker.get_date(), time.min).replace(tzinfo=UTC)
        end_datetime = datetime.combine(self.end_date_picker.get_date(), time.max).replace(tzinfo=UTC)
        self._apply_filter_callback(start_datetime, end_datetime)


class LogListView(ttk.Frame):
    def __init__(self, parent, selection_callback, navigation_callback) -> None:
        super().__init__(parent)
        self.pack(side="left", fill="both", expand=True)
        self.logs_listbox = tk.Listbox(self, exportselection=False)
        self.logs_listbox.pack(side="left", fill="both", expand=True)
        v_scroll = ttk.Scrollbar(self, orient="vertical", command=self.logs_listbox.yview)
        v_scroll.pack(side="right", fill="y")
        self.logs_listbox.configure(yscrollcommand=v_scroll.set)
        self.logs_listbox.bind("<<ListboxSelect>>", lambda e: selection_callback(self.logs_listbox.curselection()))
        self.logs_listbox.bind("<Up>", lambda e: (navigation_callback(-1), "break"))
        self.logs_listbox.bind("<Down>", lambda e: (navigation_callback(1), "break"))

    def update_log_previews(self, log_previews: List[str]) -> None:
        self.logs_listbox.delete(0, tk.END)
        for preview_text in log_previews:
            self.logs_listbox.insert(tk.END, preview_text)
        self.logs_listbox.selection_clear(0, tk.END)


class LogDetailView(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=4)
        self.pack(side="right", fill="both", expand=True)
        self.detail_fields: dict[FieldKey, tk.Widget] = {}
        self._build_fields()
        self._default_status_background = self.status_label.cget("background")

    def _build_fields(self) -> None:
        field_definitions = [
            (FieldKey.REMOTE_HOST, "Remote Host:", 30),
            (FieldKey.DATE, "Date:", 14),
            (FieldKey.IDENTITY, "Identity:", 20),
            (FieldKey.USERNAME, "Username:", 20),
        ]
        for row_index, (key, label_text, width) in enumerate(field_definitions):
            ttk.Label(self, text=label_text).grid(row=row_index, column=0, sticky="e")
            entry_widget = ttk.Entry(self, state="readonly", width=width)
            entry_widget.grid(row=row_index, column=1, sticky="w")
            self.detail_fields[key] = entry_widget

        time_row = ttk.Frame(self)
        time_row.grid(row=4, column=0, columnspan=2, sticky="w", padx=43)
        time_row.columnconfigure(2, weight=1)

        ttk.Label(time_row, text="Time:").grid(row=0, column=0)
        time_entry = ttk.Entry(time_row, state="readonly", width=12)
        time_entry.grid(row=0, column=1, sticky="w")
        self.detail_fields[FieldKey.TIME] = time_entry

        ttk.Label(time_row, text="Timezone:").grid(row=0, column=2)
        timezone_entry = ttk.Entry(time_row, state="readonly", width=18)
        timezone_entry.grid(row=0, column=3, sticky="w")
        self.detail_fields[FieldKey.TIMEZONE] = timezone_entry

        multi_line_fields = [
            (FieldKey.REQUEST_LINE, "Request Line:"),
            (FieldKey.REFERER, "Referer:"),
            (FieldKey.USER_AGENT, "User-Agent:"),
        ]
        for idx, (key, label_text) in enumerate(multi_line_fields, start=5):
            ttk.Label(self, text=label_text).grid(row=idx, column=0)
            text_widget = tk.Text(self, height=2, wrap="word", state="disabled", relief="solid", bd=1)
            text_widget.grid(row=idx, column=1, pady=2)
            self.detail_fields[key] = text_widget

        status_row = ttk.Frame(self)
        status_row.grid(row=8, column=0, columnspan=2, sticky="w", padx=6)
        status_row.columnconfigure(6, weight=1)

        ttk.Label(status_row, text="Status Code:").grid(row=0, column=0)

        self.status_label = tk.Label(status_row,width=6,relief="groove",bd=2)
        self.status_label.grid(row=0, column=1, sticky="w")

        ttk.Label(status_row, text="Method:").grid(row=0, column=2)
        method_entry = ttk.Entry(status_row, state="readonly", width=8)
        method_entry.grid(row=0, column=3, sticky="w")
        self.detail_fields[FieldKey.HTTP_METHOD] = method_entry

        ttk.Label(status_row, text="Size:").grid(row=0, column=4)
        size_entry = ttk.Entry(status_row, state="readonly", width=12)
        size_entry.grid(row=0, column=5, sticky="w")
        self.detail_fields[FieldKey.RESPONSE_SIZE] = size_entry

    def display_log(self, log: Optional[HttpLog]) -> None:
        def set_entry_value(entry_widget: ttk.Entry, value: Optional[str]) -> None:
            entry_widget.config(state="normal")
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, value or MISSING_VALUE)
            entry_widget.config(state="readonly")

        def set_text_value(text_widget: tk.Text, value: Optional[str]) -> None:
            text_widget.config(state="normal")
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, value or MISSING_VALUE)
            text_widget.config(state="disabled")

        if log is None:
            for widget in self.detail_fields.values():
                if isinstance(widget, ttk.Entry):
                    set_entry_value(widget, "")
            self.status_label.config(text=MISSING_VALUE)
            return

        set_entry_value(self.detail_fields[FieldKey.REMOTE_HOST], log.remote_host)
        set_entry_value(self.detail_fields[FieldKey.DATE], log.timestamp.date().strftime(STRFTIME_PATTERN))
        set_entry_value(self.detail_fields[FieldKey.IDENTITY], log.identity)
        set_entry_value(self.detail_fields[FieldKey.USERNAME], log.username)
        set_entry_value(self.detail_fields[FieldKey.TIME], log.timestamp.time().isoformat())
        set_entry_value(self.detail_fields[FieldKey.TIMEZONE], log.timezone)
        set_entry_value(self.detail_fields[FieldKey.HTTP_METHOD], log.method)
        set_entry_value(self.detail_fields[FieldKey.RESPONSE_SIZE], str(log.response_size))

        set_text_value(self.detail_fields[FieldKey.REQUEST_LINE], log.request_line_without_method)
        set_text_value(self.detail_fields[FieldKey.REFERER], log.referer)
        set_text_value(self.detail_fields[FieldKey.USER_AGENT], log.user_agent)

        status_code = log.status_code
        if 200 <= status_code < 300:
            status_color = "#4CAF50"
        elif 300 <= status_code < 400:
            status_color = "#FFC107"
        elif 400 <= status_code < 500:
            status_color = "#FF9800"
        else:
            status_color = "#F44336"

        self.status_label.config(text=str(status_code), bg=status_color, fg="white")


class NavigationBar(ttk.Frame):
    def __init__(self, parent, prev_callback, next_callback) -> None:
        super().__init__(parent)
        self.pack(fill="x", padx=10, pady=5)
        self.prev_button = ttk.Button(self, text="Poprzedni", command=lambda: prev_callback(-1))
        self.prev_button.pack(side="left")
        self.next_button = ttk.Button(self, text="Następny", command=lambda: next_callback(1))
        self.next_button.pack(side="left", padx=5)

    def update_buttons(self, current_index: int, total: int) -> None:
        self.prev_button["state"] = tk.NORMAL if current_index > 0 else tk.DISABLED
        self.next_button["state"] = tk.NORMAL if current_index < total - 1 else tk.DISABLED


class LogViewerApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("HTTP Log Viewer – Tkinter")
        self.geometry("1000x600")
        self.log_loader = LogLoader()
        self._current_logs: List[HttpLog] = []

        FilterBar(self, self._load_logs_from_file, self._apply_date_filter)

        paned = ttk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_list_view = LogListView(paned, self._handle_selection, self._handle_navigation)
        paned.add(self.log_list_view, weight=1)
        self.log_detail_view = LogDetailView(paned)
        paned.add(self.log_detail_view, weight=3)

        self.navigation_bar = NavigationBar(self, self._handle_navigation, self._handle_navigation)

    def _load_logs_from_file(self) -> None:
        file_path = filedialog.askopenfilename(title="Open log file", filetypes=[("Log files", "*.log *.txt")])
        if not file_path:
            return
        try:
            self.log_loader.load_logs(file_path)
        except Exception as error:
            messagebox.showerror("Error", f"Failed to load log file:\n{error}")
            return
        self._populate_log_list(self.log_loader.get_all_logs())
        self.title(f"HTTP Log Viewer – Loaded {len(self.log_loader)} entries from {Path(file_path).name}")

    def _populate_log_list(self, logs: List[HttpLog]) -> None:
        self._current_logs = logs
        previews = [entry.preview for entry in logs]
        self.log_list_view.update_log_previews(previews)
        self.log_detail_view.display_log(None)
        self.navigation_bar.update_buttons(-1, len(previews))

    def _apply_date_filter(self, start_datetime: datetime, end_datetime: datetime) -> None:
        filtered = self.log_loader.get_filtered_logs(start_datetime, end_datetime)
        self._populate_log_list(filtered)

    def _handle_selection(self, selection: tuple[int]) -> None:
        if not selection:
            return
        index = selection[0]
        self.log_detail_view.display_log(self._current_logs[index])
        self.navigation_bar.update_buttons(index, len(self._current_logs))

    def _handle_navigation(self, delta: int) -> None:
        selection = self.log_list_view.logs_listbox.curselection()
        current = selection[0] if selection else -1
        target = current + delta
        if 0 <= target < len(self._current_logs):
            self.log_list_view.logs_listbox.selection_clear(0, tk.END)
            self.log_list_view.logs_listbox.selection_set(target)
            self.log_list_view.logs_listbox.see(target)
            self.log_detail_view.display_log(self._current_logs[target])
            self.navigation_bar.update_buttons(target, len(self._current_logs))


def main() -> None:
    LogViewerApp().mainloop()

if __name__ == "__main__":
    main()
