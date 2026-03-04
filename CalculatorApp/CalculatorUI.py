import tkinter
import Calculator_Logic


#CalculatorLogic initialization
Calc_Logic = Calculator_Logic.CalculatorLogic()

#Calculator Functions
def display_text(value):
    """Used for displaying numbers"""
    current_text = text.get().replace(" ", "")

    if current_text == "0" or current_text == "Error":
        text.set(value=value)
    elif current_text[-1] == ")" or current_text[-1] == "%" or current_text == str(Calc_Logic.last_answer):
        text.set(value=text.get() + " * " + value) #Using text.get() rather than current_text to preserve the spaces used for formatting.
    else:
        text.set(value=text.get() + value)

def display_text_op(value):
    """Used for displaying operations and symbols (Preventing duplicate operations and weird looking equations)"""
    current_text = text.get().replace(" ", "")
    l = (len(current_text) - 1)

    while l != 0: #For getting the last number in current text.
        if current_text[l] in Calc_Logic.operator_precedence:
            break
        else:
            l -= 1
            continue

    last_num = current_text[l+1:] #Get the last number in the equation.
    last_char = current_text[-1] #Get the last char in the equation.


    if value == ".":
        if "." in last_num: #Prevent double decimals.
            return
        else:
            text.set(value=text.get() + value)
            return


    if value == "-":
        if current_text == "0":
            text.set(value=value)
            return
        elif last_char == "-" or last_char == ".":
            return
        elif last_char == "+":
            text.set(value=text.get().replace(text.get()[-2], "-")) #change the "+" to a "-"
        elif last_char == "(" or last_char in ["*", "/"]: #No spacing if the last char were these operations.
            text.set(text.get() + value)
        else:
            text.set(value=text.get() + " " + value + " ")
            return

    if value == "%":
        if last_char.isdigit() or last_char == ")":
            text.set(value=text.get() + value)
            return
        else:
            return

    if last_char in Calc_Logic.operator_precedence:
        if last_char == value or current_text == "-" or (current_text[-1] == "-" and current_text[-2]) : #Prevents duplicates and weird "-" stuff.
            return
        else:
            try:
                if Calc_Logic.operator_precedence[last_char] == Calc_Logic.operator_precedence[value]: #check if an operator of opposite function, but equal precedence is being input.
                    text.set(value=text.get().replace(current_text[-1], value))
                    return
                elif last_char == ")":
                    text.set(value=text.get() + " " + value + " ")
                    return
            except KeyError:
                text.set(value="Error")
                return
    elif last_char == ".":
        return
    else:
        text.set(value=text.get() + " " + value + " ")
        return

def display_text_op_parnth():
    current_text = text.get().replace(" ", "")
    para_count = 0 #Keep track of the amount of "(" and ")" symbols
    l = (len(current_text) - 1)

    if current_text == "0":
        text.set(value="(")
        return

    while l != -1: #Goes through the current text and checks for the parenthesis count
        if current_text[l] == ")" or current_text[l] == "(":
            para_count += 1
            l -= 1
        else:
            l-= 1


    if para_count % 2 == 0: #If there is no need for a closing ")"
        if current_text[-1].isdigit() or current_text[-1] == "%":
            text.set(value=text.get() + " * " + "(")
            return
        elif current_text[-1] == "-":
            text.set(value=text.get() + "(")
            return
        elif current_text[-1] == ".":
            return
        else:
            text.set(value=text.get() + "(")
            return

    elif current_text[-1] == "%":
        text.set(value=text.get() + ")")

    elif not current_text[-1].isdigit(): #Should only close after a number or "%"
        return

    else:
        text.set(value=text.get() + ")")

def display_last_ans():
    current_test = text.get().replace(" ", "")
    last_ans = str(Calc_Logic.last_answer)
    if last_ans == "None":
        return
    elif current_test == "0":
        text.set(value=last_ans)
    elif current_test[-1].isdigit() or current_test[-1] == ")":
        text.set(value=text.get() + " * " + last_ans)
    elif current_test[-1] in ["+", "*", "/", "-", "("]:
        text.set(value=text.get() + last_ans)
    else:
        return

def equals():
    current_text = text.get()
    if current_text == "0":
        return

    elif current_text[-1] == " " or current_text[-1] in ["+", "-", "*"]:
        return

    else:
        parsed_string = Calc_Logic.parser(current_text) #Parse the string
        post_fix = Calc_Logic.pre_to_post(parsed_string) #Run parsed string through Shunting Yard algorithm
        ans = Calc_Logic.post_eval(post_fix) #Solve the post-Shunting Yard algorithm expression
        Calc_Logic.last_answer = ans
        text.set(value = ans)
        return


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


make_button("C", 0, 1, func=reset_display, bg_color=op_button_color)
make_button("()", 1, 1,func=display_text_op_parnth, bg_color=op_button_color)
make_button("%", 2, 1, func=display_text_op, bg_color=op_button_color,func_parameter="%")
make_button("*", 3, 1, func=display_text_op, bg_color=op_button_color, func_parameter="*")
make_button("/", 3, 2,func=display_text_op, bg_color=op_button_color, func_parameter="/")
make_button("-", 3, 3,func=display_text_op, bg_color=op_button_color, func_parameter="-")
make_button("+", 3, 4,func=display_text_op, bg_color=op_button_color,func_parameter="+")
make_button("ans", 0, 5,func=display_last_ans, bg_color=bottom_row_op_colors) #Come back later
make_button("0", 1, 5,func=display_text, bg_color=num_button_color, func_parameter="0")
make_button(".", 2, 5,func=display_text_op, bg_color=bottom_row_op_colors,func_parameter=".")
make_button("=", 3, 5,func=equals, bg_color=op_button_color)
widget_frame.pack()
window.mainloop()
