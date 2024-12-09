import tkinter as tk
from tkinter import ttk
import re

class Calculator:
    def __init__(self, master):
        self.master = master
        self.setup_window()
        
        self.colors = {
            'background': '#2C3E50',
            'display': '#34495E',
            'button_normal': '#3498DB',
            'button_hover': '#2980B9',
            'text_primary': '#FFFFFF',
            'text_secondary': '#ECF0F1'
        }
        
        self.expression = ""
        self.equation = tk.StringVar()
        
        self.create_ui()
        self.setup_keyboard_bindings()

    def setup_window(self):
        self.master.title("Calculator")
        self.master.geometry("400x600")
        self.master.resizable(False, False)
        self.master.configure(bg='#2C3E50')

    def setup_keyboard_bindings(self):
        self.master.bind('<Key>', self.handle_keypress)
        
        self.master.bind('<Return>', lambda e: self.button_click('='))
        self.master.bind('<BackSpace>', self.handle_backspace)
        self.master.bind('<Escape>', lambda e: self.clear())

    def handle_keypress(self, event):
        key = event.char
        
        if key in '0123456789.+-*/':
            self.press(key)
        
        elif key == '%':
            self.percentage()
        
        return 'break'

    def handle_backspace(self, event):
        if self.expression:
            self.expression = self.expression[:-1]
            self.equation.set(self.expression or '0')

    def create_ui(self):
        display_frame = self.create_display()
        display_frame.pack(pady=10, padx=10, fill='x')

        buttons_frame = self.create_buttons()
        buttons_frame.pack(pady=10, padx=10, expand=True, fill='both')

    def create_display(self):
        display_frame = tk.Frame(self.master, bg=self.colors['background'])
        
        result_display = tk.Entry(
            display_frame, 
            textvariable=self.equation, 
            font=('Arial', 24, 'bold'), 
            justify='right', 
            bg=self.colors['display'], 
            fg=self.colors['text_primary'], 
            borderwidth=0,
            readonlybackground=self.colors['display'],
            state='readonly'
        )
        result_display.pack(fill='x', expand=True)

        return display_frame

    def create_buttons(self):
        buttons_frame = tk.Frame(self.master, bg=self.colors['background'])
        
        button_layout = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for row, button_row in enumerate(button_layout):
            for col, button_text in enumerate(button_row):
                button = self.create_button(buttons_frame, button_text, row, col)
                button.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)

        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
            buttons_frame.grid_columnconfigure(i, weight=1)

        return buttons_frame

    def create_button(self, parent, text, row, col):
        button_style = {
            'text': text,
            'font': ('Arial', 18, 'bold'),
            'bg': self.colors['button_normal'],
            'fg': self.colors['text_primary'],
            'activebackground': self.colors['button_hover']
        }

        button = tk.Button(
            parent, 
            **button_style, 
            command=lambda t=text: self.button_click(t)
        )
        
        button.bind('<Enter>', lambda e, b=button: b.configure(bg=self.colors['button_hover']))
        button.bind('<Leave>', lambda e, b=button: b.configure(bg=self.colors['button_normal']))

        return button

    def button_click(self, value):
        if value == 'C':
            self.clear()
        elif value == '=':
            self.calculate()
        elif value == '±':
            self.toggle_sign()
        elif value == '%':
            self.percentage()
        else:
            self.press(value)

    def press(self, value):
        # Limit input length
        if len(self.expression) < 20:
            self.expression += str(value)
            self.equation.set(self.expression)

    def clear(self):
        self.expression = ""
        self.equation.set("0")

    def calculate(self):
        try:
            expression = self.expression.replace('÷', '/').replace('×', '*')
            
            if re.match(r'^[0-9+\-*/%. ]+$', expression):
                result = str(eval(expression))
                self.equation.set(result)
                self.expression = result
            else:
                self.equation.set("Error")
                self.expression = ""
        except Exception:
            self.equation.set("Error")
            self.expression = ""

    def toggle_sign(self):
        if self.expression and self.expression[0] == '-':
            self.expression = self.expression[1:]
        else:
            self.expression = '-' + self.expression
        self.equation.set(self.expression)

    def percentage(self):
        try:
            result = str(float(self.expression) / 100)
            self.equation.set(result)
            self.expression = result
        except:
            self.equation.set("Error")
            self.expression = ""

def main():
    root = tk.Tk()
    root.title("Advanced Calculator")
    
    try:
        root.iconbitmap('calculator_icon.ico')
    except:
        pass
    
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()