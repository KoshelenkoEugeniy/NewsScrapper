import tkinter as tk
from controller import handle_generate_summary, handle_search
from urllib.parse import urlparse
from tkinter import messagebox, scrolledtext
import threading
import itertools
import time

spinner_running = False

def is_valid_url(text):
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def launch_app():
    root = tk.Tk()
    root.title("News Summarizer & Semantic Search")

    spinner_label = tk.Label(root, text="", fg="blue")
    spinner_label.pack()

    url_label = tk.Label(root, text="Enter a news article URL or search term:")
    url_label.pack(anchor='w', padx=(24,8))

    url_frame = tk.Frame(root)
    url_frame.pack(padx=24, pady=8, fill=tk.X)

    url_entry = tk.Entry(url_frame, width=80)
    url_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

    def clear_url():
        url_entry.delete(0, tk.END)
        output_box.config(state=tk.NORMAL)
        output_box.delete(1.0, tk.END)

    clear_button = tk.Button(url_frame, text="Clear", command=clear_url)
    clear_button.pack(side=tk.LEFT, padx=(8, 0))

    def start_spinner():
        def rotate():
            for c in itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]):
                if not spinner_running:
                    break
                spinner_label.config(text=f"Loading {c}")
                time.sleep(0.1)

        threading.Thread(target=rotate, daemon=True).start()

    def stop_spinner():
        global spinner_running
        spinner_running = False
        spinner_label.config(text="")

    def async_task(task):
        global spinner_running
        spinner_running = True
        start_spinner()

        def run():
            try:
                task()
            finally:
                stop_spinner()

        threading.Thread(target=run, daemon=True).start()

    def on_generate():
        url = url_entry.get().strip()
        output_box.config(state=tk.NORMAL)
        output_box.delete(1.0, tk.END)

        if not url:
            messagebox.showerror("Input Error", "Please enter a URL.")
            return
        if not is_valid_url(url):
            messagebox.showerror("Input Error", "Please enter a valid URL.")
            return

        async_task(lambda: handle_generate_summary(url, output_box))

    def on_search():
        query = url_entry.get().strip()
        output_box.config(state=tk.NORMAL)
        output_box.delete(1.0, tk.END)

        if not query:
            messagebox.showerror("Input Error", "Please enter search text.")
            return

        async_task(lambda: handle_search(query, output_box))

    button_frame = tk.Frame(root)
    button_frame.pack()

    tk.Button(button_frame, text="Generate Summary", command=on_generate, width=20, height=2).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Search", command=on_search, width=20, height=2).pack(side=tk.LEFT, padx=5)

    output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, state=tk.NORMAL)
    output_box.pack(padx=24, pady=8, fill=tk.BOTH, expand=True)

    root.mainloop()