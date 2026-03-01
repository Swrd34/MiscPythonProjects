from decimal import Decimal, InvalidOperation, DivisionByZero #Precice decimal numbers

class CalculatorLogic:

    def __init__(self):
        self.operator_precedence = {"+": 1, "-": 1, "*": 2, "/": 2}

    def pre_to_post(self, expr_string):
        """Takes an expression and runs it through the ShuntYard algorithm to get the postfix expression"""
        expr_string = expr_string.replace(" ", "") #Remove any spaces in the string
        input_list = []
        output_list = []
        op_queue = []
        grouped_items = "" #Temporary string for holding multidigit numbers and decimals before being appended to the input_list as tokens

        for i, item in enumerate(expr_string):
            if item == "-":
                if i == 0: #When the first number is negative
                    grouped_items += item

                elif expr_string[i-1].isdigit(): #Handleing if the - is an operator
                    input_list.append(grouped_items)
                    input_list.append(item)
                    grouped_items = ""
                else:
                    grouped_items += item

            elif item.isdigit() or item == ".":
                grouped_items += item
            else:
                if grouped_items == "": #If grouped items has nothing, append directly
                    input_list.append(item)
                else:
                    input_list.append(grouped_items)
                    input_list.append(item)
                    grouped_items = ""

        if grouped_items: #Append anything left in the grouped items string
            input_list.append(grouped_items)



        for item in input_list:
            try:
                """If the item is a number, output to the output list"""
                output_list.append(Decimal(item))

            except InvalidOperation:
                """If it is not a number"""
                if item in self.operator_precedence:

                    if len(op_queue) != 0:  # Check for if the symbol is in the op dictionary

                        while self.operator_precedence[item] <= self.operator_precedence[op_queue[-1]]:  # While the operator has a lower or equal precedence to the top stack operator

                            popped_val = op_queue.pop()
                            output_list.append(popped_val)

                            if len(op_queue) == 0:  # Stop if the queue is empty
                                break
                            else:
                                continue

                        op_queue.append(item) #After checking precedences, add the item
                    else:
                        op_queue.append(item) #If queue is empty

                else:
                    return "Error"

        while len(op_queue) != 0:
            """After going through the string, push the rest of the queue to the output"""
            popped_val = op_queue.pop()
            output_list.append(popped_val)

        return output_list


    def post_eval(self, test_expr):
        """Solves postfix expressions and returns the value"""
        num_stack = []
        if test_expr == "Error": #If pre_to_post returns an error, we do here as well.
            return "Error"

        for itm, item in enumerate(test_expr):
            if item not in self.operator_precedence: #If item is a number
                """Convert numbers in postfix expression to int and add them to stack"""
                num_stack.append(test_expr[itm])

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
                    return "Error"


        ans = num_stack[0]

        return ans