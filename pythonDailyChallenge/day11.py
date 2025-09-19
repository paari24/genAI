import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="South Indian Restaurant",
    page_icon="🥞",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
    }
    
    .menu-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        text-align: center;
    }
    
    .bill-summary {
        background-color: #f8f9fa;
        border-left: 4px solid #FF6B35;
        padding: 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    
    .header-container {
        background: linear-gradient(90deg, #FF6B35 0%, #F7931E 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .order-item {
        background-color: #FFF3E0;
        border-left: 3px solid #FF6B35;
        padding: 0.75rem;
        margin: 0.25rem 0;
        border-radius: 0 6px 6px 0;
    }
    
    .menu-item-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2E2E2E;
        margin-bottom: 0.5rem;
    }
    
    .menu-item-price {
        font-size: 1.2rem;
        font-weight: 700;
        color: #FF6B35;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'order_history' not in st.session_state:
    st.session_state.order_history = []

# Simple Indian menu
MENU = {
    "Idly": {"price": 30, "emoji": "🥞"},
    "Dosa": {"price": 50, "emoji": "🥞"},
    "Vada": {"price": 25, "emoji": "🍩"},
    "Coffee": {"price": 20, "emoji": "☕"},
    "Tea": {"price": 15, "emoji": "🫖"}
}

# Indian GST
GST_RATE = 0.05  # 5% GST

def calculate_totals():
    """Calculate subtotal, GST, and total"""
    if not st.session_state.cart:
        return 0, 0, 0
    
    subtotal = sum(item['price'] * item['quantity'] for item in st.session_state.cart.values())
    gst = subtotal * GST_RATE
    total = subtotal + gst
    
    return subtotal, gst, total

def generate_invoice_data():
    """Generate invoice data for download"""
    subtotal, gst, total = calculate_totals()
    
    order_data = []
    for item_name, details in st.session_state.cart.items():
        order_data.append({
            'Item': item_name,
            'Price (₹)': f"{details['price']:.0f}",
            'Quantity': details['quantity'],
            'Total (₹)': f"{details['price'] * details['quantity']:.0f}"
        })
    
    # Add summary rows
    order_data.append({'Item': '', 'Price (₹)': '', 'Quantity': '', 'Total (₹)': ''})
    order_data.append({'Item': 'Subtotal', 'Price (₹)': '', 'Quantity': '', 'Total (₹)': f"₹{subtotal:.0f}"})
    order_data.append({'Item': 'GST (5%)', 'Price (₹)': '', 'Quantity': '', 'Total (₹)': f"₹{gst:.0f}"})
    order_data.append({'Item': 'TOTAL', 'Price (₹)': '', 'Quantity': '', 'Total (₹)': f"₹{total:.0f}"})
    
    return pd.DataFrame(order_data)

# Header
st.markdown("""
<div class="header-container">
    <h1>🏛️ Saravana Bhavan</h1>
    <p style="font-size: 1.2rem; margin: 0; opacity: 0.9;">Authentic South Indian Cuisine - Order & Billing System</p>
</div>
""", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 📋 Menu Items")
    
    # Display menu items in a clean grid
    for item_name, item_data in MENU.items():
        with st.container():
            # Clean menu item card
            col_info, col_qty, col_action = st.columns([2, 1, 1])
            
            with col_info:
                st.markdown(f"""
                <div style="padding: 1rem; background: white; border-radius: 8px; border: 1px solid #ddd; margin: 0.5rem 0;">
                    <div style="font-size: 1.1rem; font-weight: 600; color: #2E2E2E;">
                        {item_data['emoji']} {item_name}
                    </div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: #FF6B35;">
                        ₹{item_data['price']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_qty:
                # Get current quantity from cart
                current_qty = st.session_state.cart.get(item_name, {}).get('quantity', 0)
                quantity = st.number_input(
                    f"Qty",
                    min_value=0,
                    max_value=20,
                    value=current_qty,
                    key=f"qty_{item_name}",
                    label_visibility="collapsed"
                )
            
            with col_action:
                if st.button(f"Add", key=f"add_{item_name}", use_container_width=True):
                    if quantity > 0:
                        st.session_state.cart[item_name] = {
                            'price': item_data['price'],
                            'quantity': quantity
                        }
                        st.session_state[f'success_{item_name}'] = f"Added {quantity}x {item_name}"
                
                # Remove button (only show if item in cart)
                if item_name in st.session_state.cart:
                    if st.button(f"Remove", key=f"remove_{item_name}", use_container_width=True):
                        del st.session_state.cart[item_name]
                        st.session_state[f'info_{item_name}'] = f"Removed {item_name}"
            
            # Show success/info messages cleanly
            if f'success_{item_name}' in st.session_state:
                st.success(st.session_state[f'success_{item_name}'])
                del st.session_state[f'success_{item_name}']
            
            if f'info_{item_name}' in st.session_state:
                st.info(st.session_state[f'info_{item_name}'])
                del st.session_state[f'info_{item_name}']

with col2:
    st.markdown("## 🛒 Current Order")
    
    if st.session_state.cart:
        # Display cart items cleanly
        for item_name, details in st.session_state.cart.items():
            emoji = MENU[item_name]['emoji']
            st.markdown(f"""
            <div class="order-item">
                <strong>{emoji} {item_name}</strong><br>
                {details['quantity']} × ₹{details['price']} = <strong>₹{details['price'] * details['quantity']}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Calculate totals
        subtotal, gst, total = calculate_totals()
        
        # Clean bill summary
        st.markdown(f"""
        <div class="bill-summary">
            <h4 style="margin-top: 0;">💰 Bill Summary</h4>
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span>Subtotal:</span>
                <strong>₹{subtotal:.0f}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span>GST (5%):</span>
                <strong>₹{gst:.0f}</strong>
            </div>
            <hr style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; font-size: 1.2rem;">
                <span><strong>Total:</strong></span>
                <strong style="color: #FF6B35;">₹{total:.0f}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col_clear, col_process = st.columns(2)
        
        with col_clear:
            if st.button("Clear Cart", key="clear_cart_btn", use_container_width=True):
                st.session_state.cart = {}
                st.session_state['cart_cleared'] = True
        
        with col_process:
            if st.button("Process Order", key="process_order_btn", use_container_width=True, type="primary"):
                order = {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'items': dict(st.session_state.cart),
                    'total': total
                }
                st.session_state.order_history.append(order)
                st.session_state.cart = {}
                st.session_state['order_processed'] = total
        
        # Show action messages
        if 'cart_cleared' in st.session_state:
            st.success("Cart cleared!")
            del st.session_state['cart_cleared']
        
        if 'order_processed' in st.session_state:
            total_amount = st.session_state['order_processed']
            st.success(f"Order processed! Total: ₹{total_amount:.0f}")
            st.balloons()
            del st.session_state['order_processed']
        
        st.markdown("---")
        
        # Simple download options
        st.markdown("#### 📄 Download Invoice")
        if st.button("Download CSV", use_container_width=True):
            invoice_df = generate_invoice_data()
            csv = invoice_df.to_csv(index=False)
            st.download_button(
                label="💾 Get CSV File",
                data=csv,
                file_name=f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    else:
        st.info("🛒 Cart is empty. Add items from the menu!")

# Order History Analytics
if st.session_state.order_history:
    st.markdown("---")
    st.markdown("## 📊 Today's Sales Analytics")
    
    # Analytics metrics
    total_orders = len(st.session_state.order_history)
    total_revenue = sum(order['total'] for order in st.session_state.order_history)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📦 Total Orders", total_orders)
    with col2:
        st.metric("💰 Total Revenue", f"₹{total_revenue:.0f}")
    with col3:
        st.metric("📈 Avg Order Value", f"₹{avg_order_value:.0f}")
    
    # Order history chart
    if len(st.session_state.order_history) > 1:
        st.markdown("### 📈 Sales Trend")
        
        df_history = pd.DataFrame([
            {
                'Order': f"Order {i+1}",
                'Amount': order['total'],
                'Time': order['timestamp']
            }
            for i, order in enumerate(st.session_state.order_history)
        ])
        
        # Use Streamlit's built-in bar chart
        st.bar_chart(df_history.set_index('Order')['Amount'])
        
        # Show recent orders table
        st.markdown("### 📋 Recent Orders")
        display_df = df_history[['Order', 'Amount', 'Time']].copy()
        display_df['Amount'] = display_df['Amount'].apply(lambda x: f"₹{x:.0f}")
        st.dataframe(display_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 1rem;">
    <p>🏛️ Saravana Bhavan - Authentic South Indian Cuisine</p>
    <p style="font-size: 0.9rem;">Built with Streamlit | Professional Restaurant Management System</p>
</div>
""", unsafe_allow_html=True)