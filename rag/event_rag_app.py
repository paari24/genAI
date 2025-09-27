import os
import re
import streamlit as st
import json
import logging
from datetime import datetime, timedelta
from typing import Tuple, Optional, List, Dict
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variablesstrea
load_dotenv()

class EnhancedEventRAGSystem:
    def __init__(self):
        """Initialize the Enhanced Event RAG System with comprehensive navigation data"""
        self.embeddings = None
        self.vectorstore = None
        self.qa_chain = None
        self.search = None
        
        # Initialize components with error handling
        self._initialize_embeddings()
        self._initialize_search()
        self._initialize_with_event_data()
    
    def _initialize_embeddings(self):
        """Initialize embeddings with fallback options"""
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            logger.info("✅ Embeddings initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize embeddings: {e}")
            st.error(f"Failed to initialize embeddings: {e}")
    
    def _initialize_search(self):
        """Initialize search with proper error handling"""
        serpapi_key = os.getenv("SERPAPI_API_KEY")
        if serpapi_key:
            try:
                self.search = SerpAPIWrapper(serpapi_api_key=serpapi_key)
                logger.info("✅ Search API initialized successfully")
            except Exception as e:
                logger.warning(f"⚠️ Search API initialization failed: {e}")
                st.warning("SERP API initialization failed. Using built-in navigation data.")
        else:
            logger.info("ℹ️ SERP API key not provided - Using built-in navigation data")
    
    def _get_navigation_data(self) -> Dict[str, str]:
        """Comprehensive navigation information for Chennai locations"""
        return {
            "guindy_to_venue": """
            🧭 DIRECTIONS FROM GUINDY TO IIT MADRAS RESEARCH PARK

            📍 **Route Overview:** Guindy → Velachery → Tharamani → IIT Research Park
            📏 **Distance:** Approximately 8-10 km
            ⏱️ **Travel Time:** 25-40 minutes (depending on traffic and mode)

            🚗 **BY CAR/TAXI/AUTO:**
            1. Start from Guindy Railway Station area
            2. Head towards Guindy-Velachery Road
            3. Take the road towards Velachery (via Guindy-Velachery Main Road)
            4. Continue straight until you reach Velachery
            5. From Velachery, head towards Tharamani via Velachery-Tambaram Road
            6. Take right turn towards Tharamani Main Road
            7. Continue on Tharamani Main Road
            8. Look for IIT Madras Research Park signboard on your right
            9. Enter the campus and follow signs to E-Block/Ramanujan Hall

            🚌 **BY BUS:**
            - Take buses going to Tharamani from Guindy
            - Route numbers: 5G, 18G, 21G, 570
            - Get down at Tharamani Bus Stand
            - Take auto/walk (1 km) to IIT Research Park
            - Alternative: Take bus to Velachery, then change to Tharamani bus

            🚇 **BY METRO + BUS/AUTO:**
            1. Take Metro from Guindy to Velachery Station (Blue Line)
            2. From Velachery Metro, take bus/auto to Tharamani
            3. Buses from Velachery to Tharamani: 5G, 21G, 570
            4. Auto fare: ₹60-80 from Velachery to venue

            💰 **ESTIMATED COSTS:**
            - Auto from Guindy: ₹120-150
            - Taxi/Ola/Uber: ₹150-250
            - Bus: ₹15-25 per person
            - Metro + Bus: ₹25-35 per person

            🕐 **BEST TRAVEL TIMES:**
            - Morning (8:00-8:30 AM): Moderate traffic
            - Avoid 9:00-10:00 AM: Heavy traffic
            - Return evening: Leave by 4:00 PM to avoid peak traffic
            """,
            
            "general_navigation": """
            🗺️ **GENERAL NAVIGATION TO IIT MADRAS RESEARCH PARK**

            📍 **Venue Address:**
            Ramanujan Hall (E Block - Ground Floor)
            IIT Madras Research Park
            Tharamani, Chennai - 600113

            🚗 **FROM DIFFERENT LOCATIONS:**

            **From Airport (Chennai Airport):**
            - Distance: 12-15 km
            - Time: 30-45 minutes
            - Route: Airport → GST Road → Guindy → Velachery → Tharamani
            - Taxi fare: ₹300-400

            **From Central Railway Station:**
            - Take suburban train to Guindy (₹10)
            - Then follow Guindy to venue directions
            - Total time: 45-60 minutes

            **From Egmore:**
            - Metro to Guindy → then bus/auto to venue
            - Or direct bus to Tharamani (route 27B, 570)
            - Time: 45-60 minutes

            **From T. Nagar:**
            - Bus to Guindy/Velachery, then to Tharamani
            - Auto: ₹150-200 directly
            - Time: 30-45 minutes

            **From OMR (IT Corridor):**
            - Very convenient - Tharamani is on OMR
            - From Sholinganallur: 15 minutes
            - From Perungudi: 10 minutes
            - From Thoraipakkam: 20 minutes

            🅿️ **PARKING AT VENUE:**
            - Free parking available inside research park
            - Separate areas for 2-wheelers and 4-wheelers
            - Security check at entry gate
            - Carry ID proof for entry

            📱 **NAVIGATION APPS:**
            - Google Maps: Search "IIT Madras Research Park"
            - Use landmark: "Tharamani Main Road"
            - GPS Coordinates: 12.9916° N, 80.2336° E
            """,
            
            "public_transport": """
            🚌 **DETAILED PUBLIC TRANSPORT OPTIONS**

            **BUS ROUTES TO THARAMANI:**
            - Route 5G: Guindy → Velachery → Tharamani
            - Route 18G: T.Nagar → Guindy → Tharamani
            - Route 21G: Broadway → Guindy → Tharamani  
            - Route 570: Koyambedu → Guindy → Tharamani
            - Route 27B: Egmore → Tharamani (direct)

            **METRO CONNECTIONS:**
            - Blue Line: Take metro to Velachery station
            - From Velachery: Bus/Auto to Tharamani (3 km)
            - Green Line: Take metro to Guindy, then bus to Tharamani

            **SUBURBAN TRAINS:**
            - Get down at Guindy Railway Station
            - Multiple trains from Central/Egmore to Guindy
            - From Guindy station: 8 km to venue via bus/auto

            **AUTO/TAXI BOOKING:**
            - Ola/Uber readily available
            - Share auto stands at Guindy, Velachery
            - Pre-book for morning arrival to avoid delays

            ⏰ **TIMING RECOMMENDATIONS:**
            - Start journey by 8:00 AM for 9:00 AM event
            - Account for traffic and registration time
            - Public transport may take longer during peak hours
            """
        }
    
    def _get_event_data(self) -> Dict[str, str]:
        """Enhanced event data with comprehensive information"""
        return {
            "event_guidelines": """
            GenAI Architect - Offline Class Event Guidelines & Schedule
            
            📅 EVENT DATES & TIMING
            Day 1: Saturday, September 27, 2025 - 09:00 AM to 04:30 PM
            Day 2: Sunday, September 28, 2025 - 09:00 AM to 04:00 PM
            
            📍 VENUE INFORMATION
            Location: Ramanujan Hall (E Block - Ground Floor)
            Address: IIT Madras Research Park, Tharamani, Chennai - 600113
            
            ⏰ DETAILED SCHEDULE
            
            DAY 1 (Saturday, September 27, 2025):
            08:30 AM - 09:00 AM: Registration & Networking
            09:00 AM - 12:30 PM: General Revision and Doubt Clearing
            12:30 PM - 12:45 PM: Hackathon Introduction and Team Formation
            12:45 PM - 02:00 PM: Lunch Break with Team Networking
            02:00 PM - 04:30 PM: Design and Development Process
            
            DAY 2 (Sunday, September 28, 2025):
            09:00 AM - 11:30 AM: Design and Development Process (Continuation)
            11:30 AM - 12:45 PM: Project Review and Feedback
            12:45 PM - 02:00 PM: Lunch Break with Team Networking
            02:00 PM - 04:00 PM: Final Review and Closing Ceremony
            
            📱 SOCIAL MEDIA GUIDELINES
            - Tag: @socialeagle.ai, @dharaneetharan
            - Hashtags: #flyhighwithai #socialeagle
            - Share your learning moments and networking experiences
            
            📋 IMPORTANT REMINDERS
            - Event starts SHARP at 09:00 AM (Registration from 08:30 AM)
            - Laptop is MANDATORY for all participants
            - Mobile phones on silent mode during sessions
            - Early arrivals get networking opportunities with community members
            - This is a non-judgmental space for growth and learning
            
            🎯 SPECIAL FEATURES
            - Spark Moment Action: Cheer and clap when you have breakthrough moments
            - Collaborative hackathon with team formation
            - Networking opportunities during breaks
            - Community WhatsApp updates
            
            🚨 SAFETY & SUPPORT
            - Notify crew if feeling unwell
            - Emergency contact: 842 842 6700
            - Stay hydrated and take breaks as needed
            """,
            
            "venue_amenities": """
            🏢 VENUE FACILITIES & AMENITIES
            
            **Ramanujan Hall Features:**
            - Air-conditioned conference hall
            - Audio-visual equipment and projectors
            - High-speed WiFi connectivity
            - Comfortable seating arrangement
            - Power outlets for laptops
            - Whiteboards and presentation screens
            
            **IIT Research Park Amenities:**
            - Clean restroom facilities
            - Drinking water stations
            - Food court and cafeteria options
            - ATM and basic shopping
            - Security and visitor management
            - Accessible parking areas
            
            **Nearby Facilities:**
            - Restaurants and food outlets within 500m
            - Medical facilities nearby
            - Public transport connectivity
            - Fuel stations and ATMs
            """
        }
    
    def _initialize_with_event_data(self):
        """Initialize the system with comprehensive event and navigation data"""
        if not self.embeddings:
            st.error("Cannot initialize without embeddings")
            return
            
        try:
            # Combine all data sources
            event_data = self._get_event_data()
            navigation_data = self._get_navigation_data()
            
            # Create documents from all sources
            documents = []
            
            # Add event documents
            for key, content in event_data.items():
                documents.append(Document(
                    page_content=content,
                    metadata={"source": f"event_{key}", "type": "event_info"}
                ))
            
            # Add navigation documents
            for key, content in navigation_data.items():
                documents.append(Document(
                    page_content=content,
                    metadata={"source": f"navigation_{key}", "type": "navigation"}
                ))
            
            # Split documents
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500,  # Increased chunk size for better context
                chunk_overlap=300
            )
            chunks = text_splitter.split_documents(documents)
            
            # Create vector store
            self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
            
            # Create QA chain if OpenAI API key is available
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key:
                self.qa_chain = RetrievalQA.from_chain_type(
                    llm=OpenAI(openai_api_key=openai_key, temperature=0.1),
                    chain_type="stuff",
                    retriever=self.vectorstore.as_retriever(search_kwargs={"k": 6}),
                    return_source_documents=True
                )
                logger.info("✅ QA chain initialized with OpenAI")
            else:
                logger.info("ℹ️ Using similarity search without OpenAI")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize event data: {e}")
            st.error(f"Failed to initialize event data: {e}")
    
    def is_navigation_query(self, query: str) -> bool:
        """Enhanced navigation query detection"""
        navigation_keywords = [
            'how to reach', 'how to get', 'how to go', 'navigation', 'directions', 'route',
            'from guindy', 'from airport', 'from central', 'from egmore', 'from t nagar',
            'from omr', 'from velachery', 'from tambaram', 'from anna nagar',
            'public transport', 'metro', 'bus', 'train', 'cab', 'taxi', 'auto',
            'distance', 'travel time', 'way to', 'path to', 'driving', 'parking',
            'nearest metro', 'nearest bus stop', 'transport', 'commute'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in navigation_keywords)
    
    def is_external_query(self, query: str) -> bool:
        """Check if query requires external search"""
        external_keywords = [
            'current weather', 'today weather', 'weather forecast', 'temperature',
            'latest news', 'current news', 'live updates', 'real time',
            'hotels near', 'restaurants near', 'food near', 'accommodation',
            'traffic update', 'road closure', 'current traffic'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in external_keywords)
    
    def get_built_in_navigation_response(self, query: str) -> Tuple[str, str]:
        """Get navigation response from built-in data"""
        try:
            # Use similarity search to find relevant navigation info
            if self.vectorstore:
                # Search specifically in navigation documents
                docs = self.vectorstore.similarity_search(query, k=4)
                
                # Filter for navigation documents
                nav_docs = [doc for doc in docs if doc.metadata.get('type') == 'navigation']
                
                if nav_docs:
                    response = "### 🧭 Navigation Directions\n\n"
                    
                    # Combine relevant navigation information
                    for doc in nav_docs[:2]:  # Use top 2 most relevant
                        response += f"{doc.page_content}\n\n"
                    
                    response += "---\n💡 **Additional Tips:**\n"
                    response += "- Use Google Maps for real-time navigation\n"
                    response += "- Account for Chennai traffic during morning hours\n" 
                    response += "- Keep emergency contact handy: 842 842 6700\n"
                    response += "- Carry ID proof for research park entry"
                    
                    return response, "navigation"
                else:
                    # Fallback to general navigation if specific route not found
                    general_nav = self._get_navigation_data()['general_navigation']
                    return f"### 🧭 General Navigation Information\n\n{general_nav}", "navigation"
            else:
                return "Navigation data not available. Please check system initialization.", "error"
                
        except Exception as e:
            logger.error(f"Error in built-in navigation: {e}")
            return f"Error retrieving navigation data: {str(e)}", "error"
    
    def get_external_search_response(self, query: str) -> Tuple[str, str]:
        """Get response from SERP API for external queries"""
        if not self.search:
            # For navigation queries, fall back to built-in data
            if self.is_navigation_query(query):
                return self.get_built_in_navigation_response(query)
            else:
                return ("🔍 External search is not configured. For navigation queries, I can use built-in Chennai navigation data.", "warning")
        
        try:
            # Enhance queries with venue information
            if self.is_navigation_query(query):
                enhanced_query = f"{query} IIT Madras Research Park Tharamani Chennai directions"
            else:
                enhanced_query = query
                
            search_results = self.search.run(enhanced_query)
            
            # Format navigation results specifically
            if self.is_navigation_query(query):
                response = "### 🧭 Live Navigation Information\n\n"
                response += f"**🔍 Search Results:**\n{search_results}\n\n"
                
                # Add built-in navigation as supplementary info
                builtin_response, _ = self.get_built_in_navigation_response(query)
                response += f"\n### 📋 Built-in Navigation Guide\n\n"
                response += builtin_response.replace("### 🧭 Navigation Directions\n\n", "")
                
            else:
                response = f"### 🔍 Search Results\n\n{search_results}"
            
            return response, "external"
            
        except Exception as e:
            logger.error(f"Search API error: {e}")
            # Fallback to built-in data for navigation
            if self.is_navigation_query(query):
                return self.get_built_in_navigation_response(query)
            else:
                return f"❌ Search failed: {str(e)}", "error"
    
    def get_document_response(self, query: str) -> Tuple[str, str]:
        """Get response from document knowledge base"""
        if not self.qa_chain:
            return self.simple_similarity_search(query)
        
        try:
            result = self.qa_chain({"query": query})
            response_text = result['result'].lower()
            
            # Check if the model doesn't have the answer
            if any(phrase in response_text for phrase in [
                "i don't know", "i do not know", "no information", 
                "not provided", "not specified", "not mentioned"
            ]):
                # For navigation queries, try built-in data
                if self.is_navigation_query(query):
                    return self.get_built_in_navigation_response(query)
                elif self.is_external_query(query):
                    return self.get_external_search_response(query)
            
            # Format the response
            response = f"### 📄 Event Information\n\n{result['result']}"
            
            # Add source information
            sources = list(set([doc.metadata['source'] for doc in result['source_documents']]))
            response += f"\n\n---\n*Sources: {', '.join(sources)}*"
            
            return response, "document"
            
        except Exception as e:
            logger.error(f"QA chain error: {e}")
            return f"❌ Error processing query: {str(e)}", "error"
    
    def simple_similarity_search(self, query: str) -> Tuple[str, str]:
        """Enhanced fallback method when OpenAI API is not available"""
        if not self.vectorstore:
            return "System not properly initialized.", "error"
            
        try:
            docs = self.vectorstore.similarity_search(query, k=5)
            
            if not docs:
                return "No relevant information found.", "warning"
            
            # For navigation queries, prioritize navigation documents
            if self.is_navigation_query(query):
                nav_docs = [doc for doc in docs if doc.metadata.get('type') == 'navigation']
                if nav_docs:
                    response = "### 🧭 Navigation Information\n\n"
                    response += nav_docs[0].page_content
                    return response, "navigation"
            
            # General response formatting
            response = "### 📄 Relevant Information\n\n"
            for i, doc in enumerate(docs[:3], 1):
                content = doc.page_content[:500] if len(doc.page_content) > 500 else doc.page_content
                response += f"**{i}. {content}**\n\n"
            
            return response, "document"
            
        except Exception as e:
            logger.error(f"Similarity search error: {e}")
            return f"❌ Error in similarity search: {str(e)}", "error"
    
    def get_response(self, query: str) -> Tuple[str, str]:
        """Main method to get response using appropriate strategy"""
        try:
            # Navigation queries - prioritize built-in comprehensive data
            if self.is_navigation_query(query):
                # Try built-in navigation first (more reliable and comprehensive)
                builtin_response, builtin_type = self.get_built_in_navigation_response(query)
                
                # If external search is available, supplement with live data
                if self.search and not self.is_external_query(query):
                    try:
                        external_response, _ = self.get_external_search_response(query)
                        combined_response = builtin_response + f"\n\n### 🔍 Additional Live Information\n{external_response}"
                        return combined_response, "navigation"
                    except:
                        # If external search fails, return built-in data
                        return builtin_response, builtin_type
                else:
                    return builtin_response, builtin_type
            
            # External queries (weather, live traffic, etc.)
            elif self.is_external_query(query):
                return self.get_external_search_response(query)
            
            # Event-related queries
            else:
                return self.get_document_response(query)
                
        except Exception as e:
            logger.error(f"Error in get_response: {e}")
            return f"❌ System error: {str(e)}", "error"

# Streamlit UI
def main():
    st.set_page_config(
        page_title="GenAI Event Assistant", 
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("🎯 GenAI Architect Event Assistant")
    st.markdown("### Your comprehensive assistant for the GenAI Architect Offline Class")
    
    # Initialize session state
    if 'rag_system' not in st.session_state:
        with st.spinner("🔄 Loading comprehensive event and navigation data..."):
            st.session_state.rag_system = EnhancedEventRAGSystem()
        st.success("✅ System loaded with event data and Chennai navigation information!")
    
    # Sidebar with enhanced info
    with st.sidebar:
        st.header("📅 Event Quick Info")
        st.markdown("""
        **📅 Dates:** September 27-28, 2025  
        **⏰ Time:** 9:00 AM - 4:30 PM  
        **📍 Venue:** IIT Madras Research Park, Tharamani  
        **🎯 Status:** ✅ Comprehensive data loaded
        """)
        
        st.header("🗺️ Navigation Features")
        st.markdown("""
        ✅ **Built-in Chennai Navigation**  
        ✅ **Route from Guindy, Airport, Central**  
        ✅ **Public Transport Options**  
        ✅ **Cost & Time Estimates**  
        ✅ **Parking Information**
        """)
        
        # API status
        st.header("🔑 System Status")
        if os.getenv("OPENAI_API_KEY"):
            st.success("✅ OpenAI API: Active")
        else:
            st.warning("⚠️ OpenAI API: Using similarity search")
            
        if os.getenv("SERPAPI_API_KEY"):
            st.success("✅ SERP API: Active")
        else:
            st.info("ℹ️ SERP API: Using built-in navigation data")
    
    # Main content area
    st.subheader("💬 Ask About the Event")
    
    # Enhanced quick action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📅 Full Schedule", help="Get detailed 2-day schedule"):
            st.session_state.query = "What is the detailed schedule for both days?"
    
    with col2:
        if st.button("🧭 From Guindy", help="Directions from Guindy"):
            st.session_state.query = "How to reach the venue from Guindy? Include all transport options."
    
    with col3:
        if st.button("🚇 Public Transport", help="Bus, Metro, Train options"):
            st.session_state.query = "What are all the public transport options to reach the venue?"
    
    with col4:
        if st.button("📍 Venue Details", help="Location and facilities"):
            st.session_state.query = "Tell me about the venue location and facilities"
    
    # Second row of buttons
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        if st.button("✈️ From Airport", help="Airport to venue directions"):
            st.session_state.query = "How to reach from Chennai Airport to the venue?"
    
    with col6:
        if st.button("🅿️ Parking Info", help="Parking and entry details"):
            st.session_state.query = "What are the parking arrangements and entry requirements?"
    
    with col7:
        if st.button("💰 Travel Costs", help="Cost estimates for different modes"):
            st.session_state.query = "What are the travel costs from different parts of Chennai?"
    
    with col8:
        if st.button("📱 Event Guidelines", help="Social media and other guidelines"):
            st.session_state.query = "What are the event guidelines and social media rules?"
    
    # Query input with enhanced placeholder
    query = st.text_input(
        "Or ask your specific question:",
        key="query",
        placeholder="e.g., How to reach from T.Nagar? What buses go to Tharamani? Parking details?",
        help="Ask about navigation, schedules, venue details, or any event-related queries"
    )
    
    # Process and display response
    if query:
        with st.spinner("🔍 Finding the best information for your query..."):
            response, response_type = st.session_state.rag_system.get_response(query)
        
        st.markdown("### 🤖 Response")
        
        # Enhanced styling based on response type
        if response_type == "navigation":
            st.info(response)
            st.markdown("💡 **Pro Tip:** Screenshot this information for offline reference!")
        elif response_type == "document":
            st.success(response)
        elif response_type == "external":
            st.info(response)
        elif response_type == "warning":
            st.warning(response)
        else:
            st.error(response)
    
    # Footer with additional tips
    st.markdown("---")
    st.markdown("""
    ### 💡 Quick Tips
    - 🕐 **Arrive Early:** Registration starts at 8:30 AM
    - 💻 **Bring Laptop:** Mandatory for hands-on sessions  
    - 🆔 **Carry ID:** Required for research park entry
    - 📱 **Emergency:** Contact 842 842 6700 for support
    - 🗺️ **Navigation:** Use Google Maps with "IIT Madras Research Park" for real-time directions
    """)

if __name__ == "__main__":
    main()