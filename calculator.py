#!/usr/bin/env python3
"""
Calculator: tokenizes an infix expression, converts to postfix (RPN),
then evaluates the RPN while printing step-by-step traces.
Supports +, -, *, /, ^, parentheses, floats and unary minus.
"""

import math

# ---------- Tokenizer ----------
def tokenize(expr: str):
    tokens = []
    i = 0
    expr = expr.strip()
    while i < len(expr):
        c = expr[i]
        if c.isspace():
            i += 1
            continue
        if c.isdigit() or c == '.':
            # parse number (int or float)
            num_chars = []
            dot_count = 0
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                if expr[i] == '.':
                    dot_count += 1
                    if dot_count > 1:
                        raise ValueError("Invalid number with multiple dots")
                num_chars.append(expr[i])
                i += 1
            tokens.append(''.join(num_chars))
            continue
        # operators and parentheses
        if c in '+-*/^()':
            # unary minus detection: at start, or after '(' or another operator
            if c == '-':
                prev = tokens[-1] if tokens else None
                if prev is None or prev in ('+', '-', '*', '/', '^', '('):
                    tokens.append('u-')  # unary minus token
                else:
                    tokens.append('-')
            elif c == '+':
                # treat unary plus as no-op if it appears similarly (optional)
                prev = tokens[-1] if tokens else None
                if prev is None or prev in ('+', '-', '*', '/', '^', '('):
                    # skip unary plus (no-op)
                    pass
                else:
                    tokens.append('+')
            else:
                tokens.append(c)
            i += 1
            continue
        # unknown character
        raise ValueError(f"Unknown character {c!r} in expression")
    return tokens

# ---------- Shunting Yard (infix -> postfix) ----------
def infix_to_postfix(tokens):
    prec = {'u-': 4, '^': 3, '*': 2, '/': 2, '+': 1, '-': 1}
    assoc = {'u-': 'right', '^': 'right', '*': 'left', '/': 'left', '+': 'left', '-': 'left'}
    output = []
    opstack = []

    for tok in tokens:
        if is_number(tok):
            output.append(tok)
        elif tok in prec:
            while opstack and opstack[-1] in prec:
                top = opstack[-1]
                if (assoc[tok] == 'left' and prec[tok] <= prec[top]) or \
                   (assoc[tok] == 'right' and prec[tok] < prec[top]):
                    output.append(opstack.pop())
                else:
                    break
            opstack.append(tok)
        elif tok == '(':
            opstack.append(tok)
        elif tok == ')':
            while opstack and opstack[-1] != '(':
                output.append(opstack.pop())
            if not opstack or opstack[-1] != '(':
                raise ValueError("Mismatched parentheses")
            opstack.pop()  # remove '('
        else:
            raise ValueError(f"Unknown token in shunting yard: {tok!r}")
    while opstack:
        top = opstack.pop()
        if top in ('(', ')'):
            raise ValueError("Mismatched parentheses")
        output.append(top)
    return output

def is_number(s):
    try:
        float(s)
        return True
    except:
        return False

# ---------- Postfix evaluation with step-by-step printing ----------
def evaluate_postfix_with_steps(postfix):
    stack = []
    steps = []
    for tok in postfix:
        if is_number(tok):
            val = float(tok)
            stack.append(val)
            steps.append(f"PUSH {format_number(val)}")
        elif tok == 'u-':
            if not stack:
                raise ValueError("Unary minus with no operand")
            a = stack.pop()
            res = -a
            steps.append(f"APPLY unary - to {format_number(a)} -> {format_number(res)}")
            stack.append(res)
        else:
            # binary operator
            if len(stack) < 2:
                raise ValueError(f"Not enough operands for '{tok}'")
            b = stack.pop()  # right operand
            a = stack.pop()  # left operand
            if tok == '+':
                res = a + b
            elif tok == '-':
                res = a - b
            elif tok == '*':
                res = a * b
            elif tok == '/':
                if abs(b) < 1e-12:
                    raise ZeroDivisionError("Division by zero")
                res = a / b
            elif tok == '^':
                res = math.pow(a, b)
            else:
                raise ValueError(f"Unsupported operator {tok}")
            steps.append(f"APPLY {tok} to {format_number(a)} and {format_number(b)} -> {format_number(res)}")
            stack.append(res)
    if len(stack) != 1:
        raise ValueError("Invalid expression or leftover operands")
    return stack[0], steps

def format_number(x):
    # show as int if it's integral
    if abs(x - round(x)) < 1e-12:
        return str(int(round(x)))
    else:
        # trim trailing zeros
        s = f"{x:.12g}"
        return s

# ---------- Interactive loop ----------
def main():
    print("Step-by-step Calculator. Type 'quit' or 'exit' to leave.")
    while True:
        try:
            expr = input("\nEnter expression: ").strip()
            if expr.lower() in ('quit', 'exit'):
                print("Goodbye.")
                break
            if not expr:
                continue
            # Tokenize
            tokens = tokenize(expr)
            print("Tokens:", tokens)
            # Infix -> Postfix
            postfix = infix_to_postfix(tokens)
            print("Postfix:", postfix)
            # Evaluate with step-by-step
            result, steps = evaluate_postfix_with_steps(postfix)
            print("\nEvaluation steps:")
            for s in steps:
                print("  ", s)
            print("\nResult:", format_number(result))
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
