import tkinter


#Calculator Functions
def display_text(value):
    """Used for displaying numbers"""
    current_text = text.get()
    text.set(value=current_text + value)


def display_text_op(value):
    """Used for displaying operations (Preventing duplicate operations)"""
    current_text = text.get()
    if current_text == "":
        return

    if current_text[-1] == " " or current_text[-1] == "." or current_text[-1] == "%":
        return

    text.set(value=current_text + value)

def pre_to_post(expr_string):
    """Takes an expression and runs it through the ShuntYard algorithm to get the postfix expression"""
    input_list = []
    output_list = []
    op_queue = []
    queued_string = ""
    operator_precedence = {"+": 1, "-": 1, "*": 2, "/": 2}  # Operator dictionary
    expr_string = expr_string + " "  # Adding a space so that the following loop can get all items in the string

    for token in expr_string:
        """Check if we are on a space, if not, add the token to the queued_string. Once we reach a space, output the string and reset"""
        if token != " ":
            queued_string = queued_string + token
        else:
            input_list.append(queued_string)
            queued_string = ""

    for input_item in input_list:
        try:
            """If the item is a number, output to the output list"""
            int(input_item)
            output_list.append(input_item)

        except ValueError:
            """If it is not a number"""
            if input_item in operator_precedence and len(
                    op_queue) != 0:  # Check for if the symbol is in the op dictionary

                while operator_precedence[input_item] <= operator_precedence[
                    op_queue[-1]]:  # While the operator has a lower or equal precedence to the top stack operator

                    popped_val = op_queue.pop()
                    output_list.append(popped_val)

                    if len(op_queue) == 0:  # Stop if the queue is empty
                        break
                    else:
                        continue

                op_queue.append(input_item)

            else:
                op_queue.append(input_item)

    while len(op_queue) != 0:
        """After going through the string, push the rest of the queue to the output"""
        popped_val = op_queue.pop()
        output_list.append(popped_val)

    return output_list


def post_eval(test_expr):
    """Solves postfix expressions and returns the value"""
    num_stack = []

    for i, item in enumerate(test_expr):
        try:
            """Convert numbers in postfix expression to int and add them to stack"""
            test_expr[i] = int(item)
            num_stack.append(test_expr[i])


        except ValueError:
            if item == "+":
                pop_val01 = num_stack.pop()
                pop_val02 = num_stack.pop()

                num_stack.append(pop_val02 + pop_val01)

            elif item == "-":
                pop_val01 = num_stack.pop()
                pop_val02 = num_stack.pop()

                num_stack.append(pop_val02 - pop_val01)

            elif item == "/":
                pop_val01 = num_stack.pop()
                pop_val02 = num_stack.pop()

                try:
                    num_stack.append(pop_val02 / pop_val01)
                except ZeroDivisionError:
                    return "Error"

            elif item == "*":
                pop_val01 = num_stack.pop()
                pop_val02 = num_stack.pop()

                num_stack.append(pop_val02 * pop_val01)

    return num_stack[0]


def equals():
    current_text = text.get()
    if current_text == "":
        return

    elif current_text[-1] == " " or current_text[-1] == ".":
        return


    else:
        post_fix_expr = pre_to_post(current_text)
        text.set(value= post_eval(post_fix_expr))




def reset_display():
    """Clears the display"""
    text.set(value="")


#Window Creation
window = tkinter.Tk()
icon = tkinter.PhotoImage(file="bean.png")
window.iconphoto(True, icon)
window.title("Calculator")
window.resizable(False, False)
window.config(background='#39403e')

#Display box
text = tkinter.StringVar(value="")
textbox = tkinter.Entry(window, font=('Arial', 30), textvariable=text, justify="right", state="readonly", background='#39403e', borderwidth=0, cursor="arrow")
textbox.grid(row=0, column=0, columnspan=7)


#Create button numbers 1-9
row_num = 1
text_num = 0
for i in range(3):
    col_num = 0
    row_num += 1

    for j in range(3):
        text_num += 1
        button = tkinter.Button(window,
                                text=f"{text_num}",
                                font="12",
                                border=5,
                                padx=40,
                                pady=15,
                                command=lambda n=text_num: display_text(f"{n}"))

        button.grid(column=col_num, row=row_num)
        col_num += 1


#Rest of the calculator buttons
def make_button(button_display_text: str, col: int, row: int, func, bg_color = None, fg_color = None, func_parameter=None): #Default function for button is display_text
    if func_parameter is None: #If nothing is being passed through the function
        cmd = func
    else:
        cmd = lambda: func(func_parameter)

    button_make = tkinter.Button(window,
                                 text=button_display_text,
                                 font="12",
                                 command=cmd,
                                 padx=40,
                                 pady=15,
                                 border=5,
                                 background=bg_color,
                                 foreground=fg_color)

    button_make.grid(column=col, row=row)


make_button("C", 0, 1, reset_display, func_parameter= None )
make_button("()", 1, 1,display_text_op, func_parameter=" FixMe ")
make_button("%", 2, 1, display_text_op, func_parameter=" FixMe ")
make_button("*", 3, 1, display_text_op, func_parameter=" * ")
make_button("/", 3, 2, func_parameter=" / ", func=display_text_op)
make_button("-", 3, 3, func_parameter=" - ", func=display_text_op)
make_button("+", 3, 4, func_parameter=" + ", func=display_text_op)
make_button("( - )", 0, 5, func_parameter="FixMe!", func=display_text_op)
make_button("0", 1, 5, func_parameter="0", func=display_text)
make_button(".", 2, 5, func_parameter=".", func=display_text_op)
make_button("=", 3, 5, func_parameter=None, func=equals)

window.mainloop()