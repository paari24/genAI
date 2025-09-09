import streamlit as st

st.set_page_config(page_title="Expense Splitter", layout="centered")

st.title("🍽️ Expense Splitter")

# Choose mode
mode = st.radio("Select split mode:", ("Equal Split", "Individual Contributions"))

# Common inputs
total_amount = st.number_input("Total expense amount (₹)", min_value=0.0, step=0.5, format="%.2f")
num_people = st.number_input("Number of people", min_value=1, step=1)

if total_amount > 0 and num_people >= 1:
    if mode == "Equal Split":
        names = []
        add_names = st.checkbox("Add participant names")
        if add_names:
            for i in range(int(num_people)):
                name = st.text_input(f"Name of person {i+1}", value=f"Person {i+1}", key=f"name_{i}")
                names.append(name)
        if st.button("Calculate Equal Split"):
            per_person = total_amount / num_people
            st.write(f"**Each person pays:** ₹{per_person:.2f}")
            if names:
                st.table({name: f"₹{per_person:.2f}" for name in names})

    else:  # Individual Contributions
        st.write("Enter each person’s name and contribution:")
        contributions = {}
        cols = st.columns(3)
        for i in range(int(num_people)):
            with cols[i % 3]:
                name = st.text_input(f"Name {i+1}", value=f"Person {i+1}", key=f"cname_{i}")
                contrib = st.number_input(f"Contribution (₹)", min_value=0.0, step=0.5, format="%.2f", key=f"camt_{i}")
                contributions[name] = contrib

        if st.button("Calculate Settlements"):
            fair_share = total_amount / num_people
            total_contributed = sum(contributions.values())

            if total_contributed > total_amount:
                st.error(f"Total contributions (₹{total_contributed:.2f}) exceed total expense (₹{total_amount:.2f})")
            else:
                st.write(f"**Fair share per person:** ₹{fair_share:.2f}")
                # Prepare settlements
                owes = []
                gets = []
                settlements = []
                for name, amt in contributions.items():
                    diff = amt - fair_share
                    if diff > 0:
                        gets.append([name, diff])
                        status = f"Gets ₹{diff:.2f}"
                    elif diff < 0:
                        owes.append([name, -diff])
                        status = f"Owes ₹{-diff:.2f}"
                    else:
                        status = "Even"
                    settlements.append([name, f"₹{amt:.2f}", f"₹{fair_share:.2f}", status])

                st.subheader("Settlement Summary")
                st.table(settlements)

                # Generate optimal transactions
                owes.sort(key=lambda x: x[1], reverse=True)
                gets.sort(key=lambda x: x[1], reverse=True)
                i = j = 0
                transactions = []
                while i < len(owes) and j < len(gets):
                    debtor, debt = owes[i]
                    creditor, credit = gets[j]
                    transfer = min(debt, credit)
                    transactions.append(f"{debtor} pays ₹{transfer:.2f} to {creditor}")
                    owes[i][1] -= transfer
                    gets[j][1] -= transfer
                    if owes[i][1] == 0:
                        i += 1
                    if gets[j][1] == 0:
                        j += 1

                if transactions:
                    st.subheader("Suggested Transactions")
                    for txn in transactions:
                        st.write("•", txn)
