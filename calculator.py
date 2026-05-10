# -*- coding: utf-8 -*-
import ast
import operator
import re

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

CURRENCY_CODES = {
    "dollar": "USD",
    "dollars": "USD",
    "usd": "USD",
    "taka": "BDT",
    "bdt": "BDT",
    "rupee": "INR",
    "rupees": "INR",
    "inr": "INR",
    "euro": "EUR",
    "euros": "EUR",
    "eur": "EUR",
    "pound": "GBP",
    "pounds": "GBP",
    "gbp": "GBP",
}


def _safe_eval(node):
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("Unsupported expression")


def _normalize_expression(text):
    replacements = {
        "plus": "+",
        "minus": "-",
        "times": "*",
        "multiply": "*",
        "multiplied by": "*",
        "into": "*",
        "divided by": "/",
        "divide": "/",
        "over": "/",
        "power": "**",
    }
    for word, symbol in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
        text = text.replace(word, symbol)
    return text


def _calculate(expression):
    expression = _normalize_expression(expression.lower())
    expression = re.sub(r"[^0-9+\-*/().\s]", "", expression)
    if not expression.strip():
        raise ValueError("Empty expression")
    return _safe_eval(ast.parse(expression, mode="eval"))


def _convert_currency(command):
    match = re.search(r"convert\s+(\d+(?:\.\d+)?)\s+(\w+)\s+to\s+(\w+)", command)
    if not match:
        return None

    amount = float(match.group(1))
    from_currency = CURRENCY_CODES.get(match.group(2))
    to_currency = CURRENCY_CODES.get(match.group(3))
    if not from_currency or not to_currency:
        return "Sorry, I do not know that currency."

    try:
        import requests

        response = requests.get(f"https://open.er-api.com/v6/latest/{from_currency}", timeout=10)
        if response.status_code != 200:
            return "Sorry, I could not get the exchange rate right now."
        rate = response.json().get("rates", {}).get(to_currency)
        if rate is None:
            return "Sorry, I could not get that exchange rate."
        result = amount * rate
        return f"{amount:g} {from_currency} is about {result:.2f} {to_currency}."
    except Exception:
        return "Sorry, I could not convert currency right now."


def handle_calculator(command):
    command = command.lower().strip()

    if command.startswith("convert "):
        response = _convert_currency(command)
        if response:
            return True, response

    if command.startswith("calculate "):
        expression = command.replace("calculate ", "", 1).strip()
    elif command.startswith("what is "):
        expression = command.replace("what is ", "", 1).strip()
        math_markers = ["+", "-", "*", "/", "plus", "minus", "times", "divided", "multiply", "over"]
        if not any(char.isdigit() for char in expression) or not any(marker in expression for marker in math_markers):
            return False, None
    else:
        return False, None

    try:
        result = _calculate(expression)
        return True, f"The answer is {result:g}."
    except Exception:
        return True, "Sorry, I could not calculate that."
