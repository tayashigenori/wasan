#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小町算
"""

import sys

def prompt_for_input(prompt = ""):
    sys.stdout.write(prompt)
    return sys.stdin.readline().strip()

def ask_yes_or_no(message):
    res = prompt_for_input(message)
    res = res.lower()
    if res in ("y", "yes", "1", "true", "t"):
        return True
    elif res in ("n", "no", "0", "false", "f"):
        return False
    raise ValueError, "A yes or no response is required"

class KomachiZan:
    def __init__(self,):
        self.max = 9
        self.stack = []
        self.exp = ""
        # class for asking questions
        self.QA = KomachiZanQA()
        return

    def process(self,):
        for i in range(1, self.max + 1):
            i_added = False
            while i_added == False:
                i_added = self._process_one(i)

        while True:
            self._process_last()
            if len(self.stack) == 1:
                if self.stack[0] == (100, False):
                    break
                else:
                    return False
        self.show_current_status()
        return True

    """
    returns True if i is added to stack
    otherwise return False (i.e. when operator is added)
    """
    def _process_one(self, i):
        if len(self.stack) < 2:
            self.stack.append((i, True))
            return True

        self.show_current_status()
        add_operator = self.QA.ask_add_operator_or_not(self.stack)

        if add_operator == False:
            self.stack.append((i, True))
            return True

        if add_operator == True:
            operator = self.QA.ask_operator(self.stack)
            self.apply_operator(operator)
            return False
    """
    always add operator
    """
    def _process_last(self,):
        sys.stdout.write("No digit left. You have to add operator!!\n")
        self.show_current_status()
        operator = self.QA.ask_operator(self.stack)
        self.apply_operator(operator)

    def apply_operator(self, operator):
        operand2,pure2 = self.stack.pop()
        operand1,pure1 = self.stack.pop()

        if operator == "join":
            if pure1 == False or pure2 == False:
                self.show_current_status()
                raise ValueError, "You can't join!"
            self.stack.append( (operand1 * 10 + operand2, True) )
            # don't add self.exp
            return

        if operator == "+":
            self.stack.append( (operand1 + operand2, False) )
        elif operator == "-":
            self.stack.append( (operand1 - operand2, False) )
        elif operator == "*":
            self.stack.append( (operand1 * operand2, False) )
        elif operator == "/":
            self.stack.append( (operand1 / operand2, False) )
        else:
            raise ValueError, "Unsupported operator!"

        self.exp += "%s %s %s, " %(operand1, operator, operand2)

    def show_current_status(self,):
        sys.stderr.write("    current stack: %s\n" %self.stack)
        sys.stderr.write("    current expression: %s\n" %self.exp)

class KomachiZanQA:
    def __init__(self,):
        return

    def ask_add_operator_or_not(self, stack):
        message = "add operator?"
        if self.check_stack_pureness(stack) == True:
            message += " (or join)"
        message += " [y/n]\n"
        
        return ask_yes_or_no(message)

    def ask_operator(self, stack):
        allowed_operators_list = ["+", "-", "*", "/"]
        if self.check_stack_pureness(stack) == True:
            allowed_operators_list += ["join"]
        allowed_operators = str(allowed_operators_list)
        
        return prompt_for_input("which operator? %s" %allowed_operators)

    def check_stack_pureness(self, stack):
        operand1,pure1 = stack[-1]
        operand2,pure2 = stack[-2]
        return pure1 == True and pure2 == True

def main():
    KZ = KomachiZan()
    KZ.process()


if __name__ == '__main__':
    main()
