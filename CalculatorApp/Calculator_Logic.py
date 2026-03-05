from decimal import Decimal, InvalidOperation, DivisionByZero #Precice decimal numbers

def parser(expr_string):
    expr_string = expr_string.replace(" ", "") #Remove any spaces in the string.
    grouped_items = "" # Temporary string for holding multidigit numbers and decimals before being appended to the input_list as tokens.
    input_list = []

    for i, item in enumerate(expr_string):
        if item == "-":
            if i == 0 and expr_string[i+1] != "(": #When the first number is negative, and the next item isn't an open parenthesis, group the negative and number together.
                grouped_items += item

            elif i == 0 and expr_string[i+1] == "(":
                input_list.append(item + "1")
                input_list.append("*")

            elif expr_string[i-1].isdigit() or expr_string[i-1] == ")": #Handleing if the char before the current is a number, or the end of a parenthesis. In these cases, - should be treated as an operator.
                if grouped_items == "":  # If grouped items has nothing, append directly. Preventing empty strings from being appended.
                    input_list.append(item)
                else: #When "-" is being treated as an operator, append the grouped numbers, than the operator by itself.
                    input_list.append(grouped_items)
                    input_list.append(item)
                    grouped_items = ""

            elif expr_string[i+1] == "(":
                if grouped_items == "":  # If grouped items has nothing, append directly. Preventing empty strings from being appended.
                    input_list.append(item)
                else:
                    input_list.append(grouped_items)
                    input_list.append(item + "1")
                    input_list.append("*")
                    grouped_items = ""


            else: #In any other case, "-" must be a negative number.
                grouped_items += item

        elif item == "%":
            if expr_string[i-1].isdigit():
                input_list.append("(")
                input_list.append(grouped_items)
                input_list.append("*")
                input_list.append("0.01")
                input_list.append(")")
                grouped_items = ""
            else:
                input_list.append("*")
                input_list.append("0.01")

        elif item.isdigit() or item == ".": #Adding regular numbers as well as decimal numbers.
            grouped_items += item

        else:
            if grouped_items == "": #If grouped items has nothing, append directly.
                input_list.append(item)
            else: #In any other case, we are dealing with an operator.
                input_list.append(grouped_items)
                input_list.append(item)
                grouped_items = ""

    if grouped_items: #Append anything left in the grouped items string.
        input_list.append(grouped_items)

    return input_list

class CalculatorLogic:

    def __init__(self):
        self.operator_precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "(": 0, ")": 0}
        self.last_answer = None

    def parser(self, expr_string):
        expr_string = expr_string.replace(" ", "") #Remove any spaces in the string.
        grouped_items = "" # Temporary string for holding multidigit numbers and decimals before being appended to the input_list as tokens.
        input_list = []

        for i, item in enumerate(expr_string):
            if item == "-":
                if i == 0 and expr_string[i+1] != "(": #When the first number is negative, and the next item isn't an open parenthesis, group the negative and number together.
                    grouped_items += item

                elif i == 0 and expr_string[i+1] == "(":
                    input_list.append(item + "1")
                    input_list.append("*")

                elif expr_string[i-1].isdigit() or expr_string[i-1] == ")": #Handleing if the char before the current is a number, or the end of a parenthesis. In these cases, - should be treated as an operator.
                    if grouped_items == "":  # If grouped items has nothing, append directly. Preventing empty strings from being appended.
                        input_list.append(item)
                    else: #When "-" is being treated as an operator, append the grouped numbers, than the operator by itself.
                        input_list.append(grouped_items)
                        input_list.append(item)
                        grouped_items = ""

                elif expr_string[i+1] == "(":
                    if grouped_items == "":  # If grouped items has nothing, append directly. Preventing empty strings from being appended.
                        input_list.append(item)
                    else:
                        input_list.append(grouped_items)
                        input_list.append(item + "1")
                        input_list.append("*")
                        grouped_items = ""


                else: #In any other case, "-" must be a negative number.
                    grouped_items += item

            elif item == "%":
                if expr_string[i-1].isdigit():
                    input_list.append("(")
                    input_list.append(grouped_items)
                    input_list.append("*")
                    input_list.append("0.01")
                    input_list.append(")")
                    grouped_items = ""
                else:
                    input_list.append("*")
                    input_list.append("0.01")

            elif item.isdigit() or item == ".": #Adding regular numbers as well as decimal numbers.
                grouped_items += item

            else:
                if grouped_items == "": #If grouped items has nothing, append directly.
                    input_list.append(item)
                else: #In any other case, we are dealing with an operator.
                    input_list.append(grouped_items)
                    input_list.append(item)
                    grouped_items = ""

        if grouped_items: #Append anything left in the grouped items string.
            input_list.append(grouped_items)

        return input_list


    def pre_to_post(self, input_list):
        """Takes an expression and runs it through the ShuntYard algorithm to get the postfix expression"""
        output_list = []
        op_queue = []

        for item in input_list:
            try:
                """If the item can be casted to a Decimal type, output to the output list"""
                output_list.append(Decimal(item))

            except InvalidOperation:
                """If it is not a number"""
                if item in self.operator_precedence:

                    if len(op_queue) != 0:  # Check for if the queue is empty.

                        while True:
                            if item == "(":
                                op_queue.append(item)
                                break
                            elif item == ")": #Look for "(".
                                while op_queue[-1] != "(":
                                    popped_val = op_queue.pop()
                                    output_list.append(popped_val)
                                op_queue.pop() #Remove when found to prevent issues during solving.
                                break
                            else:
                                while self.operator_precedence[item] <= self.operator_precedence[op_queue[-1]]:  # While the operator has a lower or equal precedence to the top stack operator.
                                    popped_val = op_queue.pop()
                                    output_list.append(popped_val)

                                    if len(op_queue) == 0:  # Stop if the queue is empty.
                                        break
                                    else:
                                        continue
                                op_queue.append(item)  # After checking precedences, add the item.
                                break #Break from While True loop.
                    else:
                        op_queue.append(item) #If queue is empty, add the operator to the queue.

                else:
                    return "Error" #Love a caught error :)

        while len(op_queue) != 0:
            """push the rest of the queue to the output"""
            popped_val = op_queue.pop()
            output_list.append(popped_val)

        return output_list


    def post_eval(self, output_list):
        """Solves postfix expressions and returns the value"""
        num_stack = []
        if output_list == "Error": #If pre_to_post returns an error, we do here as well.
            return "Error"

        for itm, item in enumerate(output_list):
            """Adds numbers stack and solves them 2 at a time"""
            if item not in self.operator_precedence: #If item is a number
                num_stack.append(output_list[itm])

            else:
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
                    except InvalidOperation:
                        return "Error"
                    except DivisionByZero:
                        return "Error"

                elif item == "*":
                    pop_val01 = num_stack.pop()
                    pop_val02 = num_stack.pop()

                    num_stack.append(pop_val02 * pop_val01)

                else:
                    return "Error" # :D


        answer = num_stack[0]
        answer_length = len(str(answer))

        if answer_length >= 11 and answer > 10000000: #If the answer has no decimal but is long
            for num in range(answer_length-1):
                answer = answer * Decimal(0.1)

            return f"{answer:.2f}" + f"E+{answer_length - 1}"

        elif "." in str(answer) and answer_length >= 12: #If the answer is long and contains a decimal. +1 length because the decimal counts.
            return round(answer, 4)



        else:
            return answer