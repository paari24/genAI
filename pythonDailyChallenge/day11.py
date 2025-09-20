import streamlit as st
import pandas as pd
import datetime
import csv
import base64
from fpdf import FPDF
import tempfile
import os

# Set page configuration
st.set_page_config(
    page_title="Restaurant Order & Billing App",
    page_icon="🍔",
    layout="wide"
)

# Restaurant menu
MENU_ITEMS = {
    "Burgers": {
        "Classic Cheeseburger": 8.99,
        "Bacon Deluxe": 10.99,
        "Veggie Burger": 9.99,
        "Chicken Burger": 9.49
    },
    "Pizza": {
        "Margherita": 12.99,
        "Pepperoni": 14.99,
        "Vegetarian": 13.99,
        "Supreme": 16.99
    },
    "Salads": {
        "Caesar Salad": 7.99,
        "Greek Salad": 8.49,
        "Garden Salad": 6.99
    },
    "Drinks": {
        "Coca-Cola": 2.49,
        "Iced Tea": 2.99,
        "Coffee": 2.99,
        "Orange Juice": 3.49
    },
    "Desserts": {
        "Chocolate Cake": 5.99,
        "Cheesecake": 6.49,
        "Ice Cream": 4.99
    }
}

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'RESTAURANT INVOICE', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(order_data, total_amount):
    pdf = PDF()
    pdf.add_page()
    
    # Invoice header
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Invoice Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1)
    pdf.cell(0, 10, f'Order ID: #{hash(str(order_data) + str(datetime.datetime.now())) % 10000:04d}', 0, 1)
    pdf.ln(10)
    
    # Order items
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(60, 10, 'Item', 1)
    pdf.cell(40, 10, 'Quantity', 1)
    pdf.cell(40, 10, 'Price', 1)
    pdf.cell(40, 10, 'Total', 1)
    pdf.ln()
    
    pdf.set_font('Arial', '', 12)
    for item, details in order_data.items():
        pdf.cell(60, 10, item, 1)
        pdf.cell(40, 10, str(details['quantity']), 1)
        pdf.cell(40, 10, f"${details['price']:.2f}", 1)
        pdf.cell(40, 10, f"${details['total']:.2f}", 1)
        pdf.ln()
    
    # Total
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f'Total Amount: ${total_amount:.2f}', 0, 1, 'R')
    
    # Thank you message
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 12)
    pdf.cell(0, 10, 'Thank you for your order!', 0, 1, 'C')
    
    return pdf

def main():
    st.title("🍔 Restaurant Order & Billing App")
    st.markdown("---")
    
    # Initialize session state for order
    if 'order' not in st.session_state:
        st.session_state.order = {}
    if 'customer_name' not in st.session_state:
        st.session_state.customer_name = ""
    if 'table_number' not in st.session_state:
        st.session_state.table_number = ""
    
    # Layout: Menu on left, Order summary on right
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📋 Menu")
        
        # Display menu by category
        for category, items in MENU_ITEMS.items():
            st.subheader(f"🍽️ {category}")
            
            for item, price in items.items():
                col_item, col_price, col_qty = st.columns([3, 1, 1])
                
                with col_item:
                    st.write(f"**{item}**")
                
                with col_price:
                    st.write(f"${price:.2f}")
                
                with col_qty:
                    quantity = st.number_input(
                        f"Qty_{item.replace(' ', '_')}",
                        min_value=0,
                        max_value=20,
                        value=0,
                        key=f"qty_{item}"
                    )
                    
                    if quantity > 0:
                        st.session_state.order[item] = {
                            'price': price,
                            'quantity': quantity,
                            'total': price * quantity
                        }
                    elif item in st.session_state.order:
                        del st.session_state.order[item]
    
    with col2:
        st.header("🛒 Your Order")
        
        # Customer information
        st.subheader("Customer Info")
        st.session_state.customer_name = st.text_input("Name", st.session_state.customer_name)
        st.session_state.table_number = st.text_input("Table Number", st.session_state.table_number)
        
        # Display order summary
        if st.session_state.order:
            st.subheader("Order Summary")
            
            order_df = pd.DataFrame.from_dict(st.session_state.order, orient='index')
            order_df = order_df.reset_index().rename(columns={'index': 'Item'})
            
            # Display order items
            for index, row in order_df.iterrows():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{row['Item']}**")
                with col2:
                    st.write(f"×{row['quantity']}")
                with col3:
                    st.write(f"${row['total']:.2f}")
            
            # Calculate totals
            subtotal = order_df['total'].sum()
            tax_rate = 0.08  # 8% tax
            tax = subtotal * tax_rate
            total = subtotal + tax
            
            st.markdown("---")
            st.write(f"**Subtotal:** ${subtotal:.2f}")
            st.write(f"**Tax (8%):** ${tax:.2f}")
            st.write(f"**Total:** ${total:.2f}")
            
            # Bill actions
            st.markdown("---")
            st.subheader("Bill Actions")
            
            if st.button("💳 Generate Bill", use_container_width=True):
                # Create bill summary
                bill_data = {
                    'customer_name': st.session_state.customer_name,
                    'table_number': st.session_state.table_number,
                    'order_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'items': st.session_state.order,
                    'subtotal': subtotal,
                    'tax': tax,
                    'total': total
                }
                
                st.session_state.bill_data = bill_data
                st.success("Bill generated successfully!")
            
            # Download options
            if 'bill_data' in st.session_state:
                # CSV Download
                csv_data = []
                for item, details in st.session_state.bill_data['items'].items():
                    csv_data.append([
                        item,
                        details['quantity'],
                        details['price'],
                        details['total']
                    ])
                
                csv_df = pd.DataFrame(csv_data, columns=['Item', 'Quantity', 'Price', 'Total'])
                csv = csv_df.to_csv(index=False)
                
                st.download_button(
                    label="📄 Download CSV Invoice",
                    data=csv,
                    file_name=f"invoice_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # PDF Download
                pdf = create_pdf(st.session_state.bill_data['items'], st.session_state.bill_data['total'])
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile:
                    pdf.output(tmpfile.name)
                    with open(tmpfile.name, "rb") as f:
                        pdf_bytes = f.read()
                
                st.download_button(
                    label="📋 Download PDF Invoice",
                    data=pdf_bytes,
                    file_name=f"invoice_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                # Clear order button
                if st.button("🗑️ Clear Order", use_container_width=True):
                    st.session_state.order = {}
                    st.session_state.customer_name = ""
                    st.session_state.table_number = ""
                    if 'bill_data' in st.session_state:
                        del st.session_state.bill_data
                    st.rerun()
        
        else:
            st.info("🛒 Your cart is empty. Select items from the menu to get started!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <p>Restaurant Order & Billing App • Built with Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()