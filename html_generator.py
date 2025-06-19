import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import re

def generate_html(account_id, percentage, amount=None):
    lines = [
        f'<link href="{account_id}" rel="operates at {percentage:.1f}">',
        f'<link href="warmup progress={percentage:.1f}" rel="stylesheet">'
    ]
    if amount and int(amount) > 0:
        lines.append(f'<<link href=To warmup account, a minimum deposit of {amount} INR is required>')
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head> 
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <meta name="theme-color" content="#000000">
 <link rel="icon" href="/favicon.ico">
 "\n " {.join(lines)} 
 <link rel="manifest" href="/manifest.json">
 <link rel="stylesheet" href="/style/main.css">
 <script defer src="/js/240.js"></script>
 <script>console.log("Loaded at {percentage:.1f} for id {account_id}");</script>
 <script type="module" src="/modules/popup.mjs"></script>
</head>
<body>
 <div id="app-root"></div>
 <!-- Page initialized -->
 <script src="/assets/ui.js"></script>
</body>
</html>"""
    return html_template

def highlight_html(text_widget):
    text_widget.tag_config('tag', foreground='#FF5555')
    text_widget.tag_config('attr', foreground='#55FF55')
    text_widget.tag_config('value', foreground='#FFFF55')
    text_widget.tag_config('comment', foreground='#AAAAAA')
    text_widget.tag_config('symbol', foreground='#FFFFFF')

    content = text_widget.get("1.0", tk.END)
    for tag in text_widget.tag_names():
        text_widget.tag_remove(tag, "1.0", tk.END)

    patterns = [
        (r'(</?[a-zA-Z]+)(?:\s|>)', 'tag'),
        (r'\s([a-zA-Z-]+)=', 'attr'),
        (r'="([^"]*)"', 'value'),
        (r'<!--.*?-->', 'comment'),
        (r'[<>="/]', 'symbol')
    ]

    for pattern, tag in patterns:
        for match in re.finditer(pattern, content):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            text_widget.tag_add(tag, start, end)

def save_to_file(html_content):
    file_path = filedialog.asksaveasfilename(defaultextension=".html",
                                             filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
                                             title="Сохранить HTML файл")
    if file_path:
        try:
            with open(file_path, 'w') as file:
                file.write(html_content)
            messagebox.showinfo("Успех", f"Файл успешно сохранён:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

def show_result():
    account_id = entry_id.get()
    percentage = entry_percent.get()
    amount = entry_amount.get()
    if not account_id or not percentage:
        messagebox.showerror("Ошибка", "Поля ID аккаунта и Процент должны быть заполнены")
        return
    try:
        percentage_float = float(percentage)
    except ValueError:
        messagebox.showerror("Ошибка", "Процент должен быть числом")
        return

    result_window = tk.Toplevel(root)
    result_window.title("Результат")
    result_window.configure(bg='#333333')

    text = scrolledtext.ScrolledText(result_window, bg='#333333', fg='white',
                                     font=('Courier', 10), insertbackground='white', wrap=tk.NONE)
    text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    html_code = generate_html(account_id, percentage_float, amount if amount else None)
    text.insert(tk.END, html_code)
    highlight_html(text)

    if amount:
        try:
            amount_int = int(amount)
            if amount_int > 1000:
                tk.Label(result_window,
                         text=f"Для увеличения прогрева аккаунта минимальная сумма {amount_int} рупий",
                         bg='#333333', fg='#FF5555', font=('Arial', 12, 'bold')).pack(pady=10)
        except ValueError:
            pass

root = tk.Tk()
root.title("HTML генератор для разведки")
root.configure(bg='#444444')
root.minsize(400, 250)

button_style = {'bg': '#555555', 'fg': 'white',
                'activebackground': '#666666',
                'activeforeground': 'white',
                'relief': tk.GROOVE, 'borderwidth': 2}
entry_style = {'bg': '#555555', 'fg': 'white',
               'insertbackground': 'white',
               'relief': tk.SUNKEN, 'borderwidth': 2}

tk.Label(root, text="ID аккаунта:", bg='#444444', fg='white').grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_id = tk.Entry(root, **entry_style)
entry_id.grid(row=0, column=1, padx=5, pady=5, sticky='we')

tk.Label(root, text="Процент:", bg='#444444', fg='white').grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_percent = tk.Entry(root, **entry_style)
entry_percent.grid(row=1, column=1, padx=5, pady=5, sticky='we')

tk.Label(root, text="Сумма (необязательно):", bg='#444444', fg='white').grid(row=2, column=0, padx=5, pady=5, sticky='e')
entry_amount = tk.Entry(root, **entry_style)
entry_amount.grid(row=2, column=1, padx=5, pady=5, sticky='we')
root.columnconfigure(1, weight=1)

submit_btn = tk.Button(root, text="Сгенерировать HTML", command=show_result,
                       bg='#5A5AFF', fg='white', font=('Arial', 10, 'bold'))
submit_btn.grid(row=3, column=0, columnspan=2, pady=15, sticky='we')
root.mainloop()
