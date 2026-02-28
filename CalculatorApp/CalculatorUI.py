import tkinter
from decimal import Decimal #Precice decimal numbers

#Calculator Functions
def display_text(value):
    """Used for displaying numbers"""
    current_text = text.get()

    if current_text == "0":
        text.set(value=value)
    else:
        text.set(value=current_text + value)


def display_text_op(value):
    """Used for displaying operations (Preventing duplicate operations and weird looking equations)"""
    current_text = text.get()

    if value == "-": #specific for handling (-)
        if current_text == "0":
            text.set(value=value)
        elif current_text[-1].isdigit() or current_text[-2] in ["/", "*"]:
            text.set(value=current_text + " " + value + " ")

    if current_text[-1] == " " or current_text[-1] == "." or current_text[-1] == "-":
        return


    else:
        text.set(value=current_text + value)
        return

def display_text_op_parnth(value):
    pass

def equals():
    current_text = text.get()
    if current_text == "0":
        return

    elif current_text[-1] == " " or not current_text[-1].isdigit():
        return


    else:
        post_fix_expr = Calc_Logic.pre_to_post(current_text)
        text.set(value= Calc_Logic.post_eval(post_fix_expr))


def reset_display():
    """Clears the display"""
    text.set(value="0")


#Window Creation
window = tkinter.Tk()
icon = tkinter.PhotoImage(file="bean.png")
window.iconphoto(True, icon)
window.title("Calculator.py")
window.resizable(False, False)

widget_frame = tkinter.Frame(window)

#Display box
text = tkinter.StringVar(value="0")
textbox = tkinter.Label(widget_frame, font=('Arial', 28), textvariable=text, background='white', cursor="arrow", width=14, justify="right", anchor="e", state="active")
textbox.grid(row=0, column=0, columnspan=4, sticky="nsew")



#button properties(0-9)
num_button_color = "#262526"
num_button_width = 1
num_button_height = 2
num_button_pad_y = 20



#General button properties
button_text_color = "#ffffff"
text_font = 12
op_button_color = "#f5a52f"
bottom_row_op_colors = "#351b4a"
right_column_height = 3



#Create button numbers 1-9
row_num = 1
text_num = 0
for i in range(3):
    col_num = 0
    row_num += 1

    for j in range(3):
        text_num += 1
        button = tkinter.Button(widget_frame,
                                text=f"{text_num}",
                                font=('Arial', text_font),
                                border=1,
                                pady=num_button_pad_y,
                                activebackground=num_button_color,
                                background=num_button_color,
                                fg=button_text_color,
                                activeforeground=button_text_color,
                                command=lambda n=text_num: display_text(f"{n}"))


        button.grid(column=col_num, row=row_num, sticky="nsew") #Sticky makes the button fill entire grid()
        button.config(height = num_button_height, width = num_button_width)
        col_num += 1


#Rest of the calculator buttons
def make_button(button_display_text: str,
                col: int,
                row: int,
                func,
                bg_color,
                text_color = button_text_color,
                y_padding = 10,
                width = 1,
                height = 0,
                func_parameter=None): #Default function for button is display_text

    if func_parameter is None: #If nothing is being passed through the function
        cmd = func
    else:
        cmd = lambda: func(func_parameter)

    button_make = tkinter.Button(widget_frame,
                                 text=button_display_text,
                                 font=('Arial', text_font),
                                 command=cmd,
                                 pady=y_padding,
                                 border=1,
                                 activebackground=bg_color,
                                 background=bg_color,
                                 foreground=text_color,
                                 activeforeground=button_text_color
                                 )

    button_make.grid(column=col, row=row, sticky="nsew")
    button_make.config(width=width, height=height)


make_button("C", 0, 1, func=reset_display, bg_color=op_button_color, func_parameter= None )
make_button("()", 1, 1,func=display_text_op, bg_color=op_button_color, func_parameter=" ( ")
make_button("%", 2, 1, func=display_text_op, bg_color=op_button_color,func_parameter=" FixMe ")
make_button("*", 3, 1, func=display_text_op, bg_color=op_button_color, func_parameter=" * ")
make_button("/", 3, 2,func=display_text_op, bg_color=op_button_color, func_parameter=" / ")
make_button("-", 3, 3,func=display_text_op, bg_color=op_button_color, func_parameter=" - ")
make_button("+", 3, 4,func=display_text_op, bg_color=op_button_color,func_parameter=" + ")
make_button("( - )", 0, 5,func=display_text_op, bg_color=bottom_row_op_colors,func_parameter="-")
make_button("0", 1, 5,func=display_text, bg_color=num_button_color, func_parameter="0")
make_button(".", 2, 5,func=display_text_op, bg_color=bottom_row_op_colors,func_parameter=".")
make_button("=", 3, 5,func=equals, bg_color=op_button_color,func_parameter=None)
widget_frame.pack()
window.mainloop()
