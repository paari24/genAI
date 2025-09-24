import streamlit as st
import time
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False
        self.laps = []
        self.last_lap_time = 0
    
    def start(self):
        if not self.is_running:
            self.start_time = time.time() - self.elapsed_time
            self.is_running = True
    
    def stop(self):
        if self.is_running:
            self.elapsed_time = time.time() - self.start_time
            self.is_running = False
    
    def reset(self):
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False
        self.laps = []
        self.last_lap_time = 0
    
    def lap(self):
        if self.is_running:
            current_time = time.time() - self.start_time
            lap_time = current_time - self.last_lap_time
            self.laps.append({
                'lap_number': len(self.laps) + 1,
                'lap_time': lap_time,
                'total_time': current_time,
                'timestamp': datetime.datetime.now()
            })
            self.last_lap_time = current_time
            return lap_time
        return None
    
    def get_elapsed_time(self):
        if self.is_running:
            return time.time() - self.start_time
        return self.elapsed_time

def format_time(seconds):
    """Format time in HH:MM:SS.mmm format"""
    if seconds is None:
        return "00:00:00.000"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    milliseconds = int((secs - int(secs)) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{int(secs):02d}.{milliseconds:03d}"

def main():
    st.set_page_config(
        page_title="Ultimate Stopwatch",
        page_icon="⏱️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for premium styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #667eea, #764ba2, #f093fb, #f5576c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 300% 300%;
        animation: gradient 3s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    .time-display {
        font-family: 'Courier New', monospace;
        font-size: 5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 3px solid #4ECDC4;
    }
    .control-button {
        border-radius: 50px !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        padding: 1rem 2rem !important;
        margin: 0.5rem !important;
        transition: all 0.3s ease !important;
    }
    .control-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }
    .lap-item {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: white;
        border-left: 5px solid #4ECDC4;
    }
    .stat-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2a5298;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 3px solid #4ECDC4;
        padding-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize stopwatch in session state
    if 'stopwatch' not in st.session_state:
        st.session_state.stopwatch = Stopwatch()
    
    # Header
    st.markdown('<div class="main-header">⏱️ ULTIMATE STOPWATCH</div>', unsafe_allow_html=True)
    
    # Main layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Time display
        elapsed = st.session_state.stopwatch.get_elapsed_time()
        st.markdown(f'<div class="time-display">{format_time(elapsed)}</div>', unsafe_allow_html=True)
        
        # Control buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("▶️ START", key="start", use_container_width=True, 
                        type="primary" if not st.session_state.stopwatch.is_running else "secondary",
                        disabled=st.session_state.stopwatch.is_running):
                st.session_state.stopwatch.start()
                st.rerun()
        
        with col2:
            if st.button("⏸️ STOP", key="stop", use_container_width=True,
                        type="primary" if st.session_state.stopwatch.is_running else "secondary",
                        disabled=not st.session_state.stopwatch.is_running):
                st.session_state.stopwatch.stop()
                st.rerun()
        
        with col3:
            if st.button("⏹️ RESET", key="reset", use_container_width=True,
                        type="secondary"):
                st.session_state.stopwatch.reset()
                st.rerun()
        
        with col4:
            if st.button("⏱️ LAP", key="lap", use_container_width=True,
                        type="primary" if st.session_state.stopwatch.is_running else "secondary",
                        disabled=not st.session_state.stopwatch.is_running):
                st.session_state.stopwatch.lap()
                st.rerun()
        
        # Statistics cards
        st.markdown('<div class="section-header">📊 Performance Metrics</div>', unsafe_allow_html=True)
        
        if st.session_state.stopwatch.laps:
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            
            with stat_col1:
                fastest_lap = min(lap['lap_time'] for lap in st.session_state.stopwatch.laps)
                st.markdown(f'''
                <div class="stat-card">
                    <div>🏃 Fastest Lap</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">{format_time(fastest_lap)}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with stat_col2:
                slowest_lap = max(lap['lap_time'] for lap in st.session_state.stopwatch.laps)
                st.markdown(f'''
                <div class="stat-card">
                    <div>🐢 Slowest Lap</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">{format_time(slowest_lap)}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with stat_col3:
                avg_lap = sum(lap['lap_time'] for lap in st.session_state.stopwatch.laps) / len(st.session_state.stopwatch.laps)
                st.markdown(f'''
                <div class="stat-card">
                    <div>📈 Average Lap</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">{format_time(avg_lap)}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with stat_col4:
                total_laps = len(st.session_state.stopwatch.laps)
                st.markdown(f'''
                <div class="stat-card">
                    <div>🔢 Total Laps</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">{total_laps}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Lap time visualization
            st.markdown('<div class="section-header">📈 Lap Time Analysis</div>', unsafe_allow_html=True)
            
            lap_df = pd.DataFrame(st.session_state.stopwatch.laps)
            fig = px.line(lap_df, x='lap_number', y='lap_time', 
                         title='Lap Time Progression', markers=True)
            fig.update_layout(
                xaxis_title='Lap Number',
                yaxis_title='Lap Time (seconds)',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Lap history
        st.markdown('<div class="section-header">📝 Lap History</div>', unsafe_allow_html=True)
        
        if st.session_state.stopwatch.laps:
            # Create a scrollable container for laps
            lap_container = st.container()
            with lap_container:
                for lap in reversed(st.session_state.stopwatch.laps):
                    lap_time = format_time(lap['lap_time'])
                    total_time = format_time(lap['total_time'])
                    timestamp = lap['timestamp'].strftime("%H:%M:%S")
                    
                    st.markdown(f'''
                    <div class="lap-item">
                        <div style="font-size: 1.2rem; font-weight: bold;">Lap {lap['lap_number']}</div>
                        <div>Lap Time: <strong>{lap_time}</strong></div>
                        <div>Total: {total_time}</div>
                        <div style="font-size: 0.8rem; opacity: 0.8;">{timestamp}</div>
                    </div>
                    ''', unsafe_allow_html=True)
        else:
            st.info("No laps recorded yet. Click 'LAP' while timing to record laps.")
        
        # Session summary
        st.markdown('<div class="section-header">💾 Session Summary</div>', unsafe_allow_html=True)
        
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.metric("Current Status", 
                     "RUNNING" if st.session_state.stopwatch.is_running else "STOPPED",
                     delta="Active" if st.session_state.stopwatch.is_running else "Inactive")
        
        with summary_col2:
            st.metric("Laps Recorded", len(st.session_state.stopwatch.laps))
        
        # Export functionality
        if st.session_state.stopwatch.laps:
            lap_df = pd.DataFrame(st.session_state.stopwatch.laps)
            csv = lap_df.to_csv(index=False)
            
            st.download_button(
                label="📥 Export Lap Data",
                data=csv,
                file_name=f"stopwatch_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # Real-time updates
    if st.session_state.stopwatch.is_running:
        time.sleep(0.01)  # Small delay for smooth updates
        st.rerun()
    
    # Instructions
    with st.expander("ℹ️ How to Use This Stopwatch", expanded=False):
        st.markdown("""
        **Features:**
        - **Precision Timing**: Millisecond accuracy with professional time formatting
        - **Lap Recording**: Track individual lap times while the main timer runs
        - **Real-time Analytics**: Visualize your performance with charts and statistics
        - **Data Export**: Download your lap data for further analysis
        
        **Controls:**
        - **START**: Begin timing
        - **STOP**: Pause the timer
        - **RESET**: Clear all timing data and laps
        - **LAP**: Record a lap time while timing is active
        
        **Pro Tips:**
        - Use laps to track intervals during workouts or experiments
        - Monitor your performance with the live lap time chart
        - Export data for detailed analysis in spreadsheet software
        - The stopwatch continues running even when you navigate away!
        """)

if __name__ == "__main__":
    main()