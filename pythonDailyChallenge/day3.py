import streamlit as st

st.title("Eagles Simple Calculator ➕➖✖➗")

# User inputs
num1 = st.number_input("Enter first number", format="%.2f")
num2 = st.number_input("Enter second number", format="%.2f")

# Operation selection
operation = st.radio(
    "Select operation",
    ("Add", "Subtract", "Multiply", "Divide")
)

result = None

def calculate():
    if operation == "Add":
        return num1 + num2
    elif operation == "Subtract":
        return num1 - num2
    elif operation == "Multiply":
        return num1 * num2
    elif operation == "Divide":
        if num2 != 0:
            return num1 / num2
        else:
            st.warning("Division by zero is not allowed.")
            return "Error"
    else:
        return "Invalid operation"

if st.button("Calculate"):
    result = calculate()
    if result != "Error":
        st.success(f"Result: {result}")
