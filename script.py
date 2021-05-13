import re
from collections import deque


class SmartCalculator:
    def __init__(self):
        self.variables = {}

    def addition(self, entry):
        numbers = (int(num) for num in entry.split())
        print(sum(numbers))

    def analyze(self, string):
        numbers = re.split(r'[+-]+', string)
        signs = re.split(r'\d+', string)
        unary = True if not numbers[0] else False
        numbers = [num.strip() for num in numbers if num]
        signs = [sign.strip() for sign in signs if sign]
        for i in range(len(signs)):
            if '+' in signs[i]:
                signs[i] = '+'
            elif '-' in signs[i]:
                signs[i] = '-' if len(signs[i]) % 2 else '+'
        if unary:
            for i in range(len(signs)):
                if signs[i] == '+':
                    numbers[i] = int(numbers[i])
                elif signs[i] == '-':
                    numbers[i] = -int(numbers[i])
        else:
            numbers[0] = int(numbers[0])
            for i in range(len(signs)):
                if signs[i] == '+':
                    numbers[i + 1] = int(numbers[i + 1])
                elif signs[i] == '-':
                    numbers[i + 1] = int(numbers[i + 1]) * -1
        return numbers

    def check(self, string):
        if string == '':
            return 'empty'
        if string in ('/help', '/exit'):
            return string
        elif string.startswith('/'):
            return 'Unknown command'
        elif not re.match(r'[\d+ -]+', string) or string.rstrip()[-1] in ('+', '-'):
            return 'Invalid expression'
        return string

    def check2(self, string):
        if string == '':
            return 'empty'
        if string in ('/help', '/exit'):
            return string
        elif string.startswith('/'):
            return 'Unknown command'
        elif '=' not in string and '+' not in string and '-' not in string:
            if not re.match(r'\w+', string):
                return 'Invalid identifier'
            else:
                if string in self.variables:
                    print(self.variables[string])
                    return
                else:
                    return 'Unknown variable'
        elif '=' in string:
            arr = string.split('=')
            if len(arr) != 2:
                return 'Invalid assignment'
            ident, assign = [item.strip() for item in arr]
            if not re.match(r'[a-zA-Z]+$', ident):
                return 'Invalid identifier'
            if not re.match(r'\d+$', assign) and assign not in self.variables:
                return 'Invalid assignment'
            if re.match(r'\d+', assign):
                self.variables[ident] = assign
            else:
                self.variables[ident] = self.variables[assign]
        else:
            numbers = re.split(r'[+-]+', string)
            for number in numbers:
                if not re.match(r'\d+', number.strip()):
                    if number.strip() in self.variables:
                        string = string.replace(number.strip(), self.variables[number.strip()])
                    else:
                        return 'Unknown variable'
            return string

    def parantheses(self, string):
        if '(' in string or ')' in string:
            left, right = 0, 0
            for letter in string:
                if letter == '(':
                    left += 1
                if letter == ')':
                    right += 1
            return left == right
        return True

    def multiples(self, string):
        if re.search(r'\*{2,}', string) is not None:
            return 'Invalid expression'
        if re.search(r'/{2,}', string) is not None:
            return 'Invalid expression'
        if re.search(r'\+{2,}', string):
            start, end = re.search(r'\+{2,}', string).span()
            part = '+' * (end - start)
            string = string.replace(part, '+')
        if re.search(r'-{2,}', string):
            start, end = re.search(r'-{2,}', string).span()
            part = '-' * (end - start)
            string = string.replace(part, '-' if (end - start) % 2 else '+')
        return string

    def check3(self, string):
        if string == '':
            return 'empty'
        if not self.parantheses(string):
            return 'Invalid expression'
        multi = self.multiples(string)
        if multi == 'Invalid expression':
            return 'Invalid expression'
        else:
            string = multi
        if string in ('/help', '/exit'):
            return string
        elif string.startswith('/'):
            return 'Unknown command'
        elif '=' not in string and '+' not in string and '-' not in string and '*' not in string and '/' not in string:
            if not re.match(r' *\w+', string):
                return 'Invalid identifier'
            else:
                if string in self.variables:
                    print(self.variables[string])
                    return
                elif string.isdigit():
                    return string
                else:
                    return 'Unknown variable'
        elif '=' in string:
            arr = string.split('=')
            if len(arr) != 2:
                return 'Invalid assignment'
            ident, assign = [item.strip() for item in arr]
            if not re.match(r' *[a-zA-Z]+$', ident):
                return 'Invalid identifier'
            if not re.match(r'\d+$', assign) and assign not in self.variables:
                return 'Invalid assignment'
            if re.match(r'\d+', assign):
                self.variables[ident] = assign
            else:
                self.variables[ident] = self.variables[assign]
        else:
            numbers = re.split(r'[+/*()-]+', string)
            for number in numbers:
                if number.strip() and not re.match(r'\d+', number.strip()):
                    if number.strip() in self.variables:
                        string = string.replace(number.strip(), self.variables[number.strip()])
                    else:
                        return 'Unknown variable'
            return string

    def form(self, string):
        numbers = [item.strip() for item in re.split(r'[-+/*]', string)]
        signs = [item.strip() for item in re.split(r'\(*\d+\)*', string) if item]
        result = []
        if len(numbers) > len(signs):
            result.append(numbers[0])
            numbers = numbers[1:]
        for i in range(len(signs)):
            result.append(signs[i])
            result.append(numbers[i])
        return ' '.join(result)

    def to_postfix(self, string):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '(': 0, ')': 0}
        stack = deque()
        postfix = []
        elements = string.replace('(', '( ').replace(')', ' )').split()
        for element in elements:
            if re.match(r'\d+', element):
                postfix.append(element)
            else:
                if element == '(':
                    stack.append(element)
                elif element == ')':
                    while stack[-1] != '(':
                        postfix.append(stack.pop())
                    stack.pop()
                else:
                    if len(stack) == 0:
                        stack.append(element)
                    elif stack[-1] == '(' or precedence[element] > precedence[stack[-1]]:
                        stack.append(element)
                    else:
                        while len(stack) > 0 and (
                                stack[-1] not in '()' or precedence[stack[-1]] >= precedence[element]):
                            postfix.append(stack.pop())
                        stack.append(element)
        while len(stack) > 0:
            postfix.append(stack.pop())
        return ' '.join(postfix)

    def postfix_sol(self, string):
        solution = deque()
        elements = string.split()
        for element in elements:
            if element.isdigit():
                solution.append(element)
            else:
                a = solution.pop()
                b = solution.pop()
                if element == '+':
                    op = int(a) + int(b)
                elif element == '-':
                    op = int(b) - int(a)
                elif element == '*':
                    op = int(a) * int(b)
                elif element == '/':
                    op = int(b) // int(a)
                solution.append(str(op))
        return solution.pop()

    def loop2(self):
        while True:
            entry = self.check3(input())
            if entry == 'empty':
                continue
            if entry in (
            'Unknown command', 'Invalid identifier', 'Invalid assignment', 'Unknown variable', 'Invalid expression'):
                print(entry)
                continue
            if not entry:
                pass
            elif entry == '/help':
                print('The program calculates the sum of numbers')
            elif entry == '/exit':
                print('Bye!')
                break
            else:
                entry = self.form(entry)
                if re.match(r' ?(\+|-)? ?\d+$', entry):
                    if '+' in entry:
                        print(entry.split()[-1])
                    elif '-' in entry:
                        print('-' + entry.split()[-1])
                    else:
                        print(entry)
                    continue
                postfix = self.to_postfix(entry)
                result = self.postfix_sol(postfix)
                print(result)

    def loop(self):
        while True:
            entry = self.check2(input())
            if entry == 'empty':
                continue
            if entry in ('Unknown command', 'Invalid identifier', 'Invalid assignment', 'Unknown variable'):
                print(entry)
                continue
            if not entry:
                pass
            elif entry == '/help':
                print('The program calculates the sum of numbers')
            elif entry == '/exit':
                print('Bye!')
                break
            else:
                array = self.analyze(entry)
                print(sum(array))


calculator = SmartCalculator()
calculator.loop2()