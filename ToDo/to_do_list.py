import os
def clear_console():
   os.system("cls")


def menu():
   print("\n\nTo add an item, enter, \"add\".\n"
         "To remove an item, enter \"remove\".\n"
         "To mark item done, enter \"done\".\n"
         "To quit, enter \"quit\".")


def print_to_do_list(to_do):
   i = 0
   for index, item in enumerate(to_do, 1):


       if to_do [i][1]:
           print(f"{index}.[X] {item[0]}")
       else:
           print(f"{index}.[] {item[0]}")
       i += 1


def mark_done(to_do):
   clear_console()
   print_to_do_list(to_do)


   print("\n\nWhich item would you like to mark as finished?")


   while True:
       try:
           item_index = int(input())


           if item_index in range(1, len(to_do)+1):
               break


           else:
               pass


       except ValueError:
           print("You must input a whole number.")


   to_do[item_index-1][1] = True






def add_item(to_do):
   clear_console()
   user_added_item = input("Input the item you wish to add: ")


   to_do.append([user_added_item, False])




def remove_item(to_do):
   clear_console()
   print_to_do_list(to_do)


   print("\n\nWhich item would you like to remove? (input item number)")


   while True:
       try:
           item_index = int(input())


           if item_index in range(1, len(to_do)+1):
               break


           else:
               pass


       except ValueError:
           print("You must input a whole number.")


   to_do.pop(item_index-1)


def input_check(choice_list: list[str]) -> str:
   while True:
       u_input = input().lower().replace(" ", "")


       if u_input in choice_list:
           return u_input
       else:
           print("Invalid entry.")


def main():
   to_do = []
   clear_console()


   user_input = input("What would you like to add to the to do list? (DONE when done): ")


   while user_input != "DONE":
       clear_console()


       print(f"Added - {user_input}.")
       to_do.append([user_input, False])


       user_input = input("What else would you like to add to the to do list? (DONE when done): ")


   while True:


       clear_console()
       print_to_do_list(to_do)
       menu()  # print menu


       user_input = input_check(["add", "remove", "done", "quit"])


       if user_input == "add":
           add_item(to_do)
       elif user_input == "remove":
           remove_item(to_do)
       elif user_input == "done":
           mark_done(to_do)
       else:
           break #End program


main()
