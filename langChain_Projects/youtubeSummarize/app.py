import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()
from urllib.parse import urlparse, parse_qs
import requests
import re

# Try different import methods for youtube_transcript_api
try:
    import youtube_transcript_api
    from youtube_transcript_api import YouTubeTranscriptApi
    TRANSCRIPT_API_AVAILABLE = True
    st.sidebar.success("✅ YouTube Transcript API loaded successfully")
except ImportError as e:
    TRANSCRIPT_API_AVAILABLE = False
    st.sidebar.error(f"❌ YouTube Transcript API not available: {e}")

llm_summary = ChatOpenAI(model_name="gpt-4o", temperature=0.5, openai_api_key=os.getenv("OPENAI_API_KEY"))

prompt_summary = PromptTemplate(
    input_variables=["transcript_"],
    template="""
    Given this YouTube Video Transcript: {transcript_}
    Generate a concise summary of the video content in 3-4 sentences.
    1. Focus on key points and main ideas.
    2. Avoid unnecessary details or examples.
    3. Write in a clear and engaging manner.
    4. Use bullet points if appropriate.
    Provide the summary below:
     """)

chain = LLMChain(llm=llm_summary, prompt=prompt_summary)

st.title("YouTube Video Summarizer")

# Add debugging information
with st.expander("🔧 Debug Information"):
    st.write(f"YouTube Transcript API Available: {TRANSCRIPT_API_AVAILABLE}")
    if TRANSCRIPT_API_AVAILABLE:
        st.write(f"API Version: {getattr(youtube_transcript_api, '__version__', 'Unknown')}")
        st.write("Available methods:", [method for method in dir(YouTubeTranscriptApi) if not method.startswith('_')])

video_url = st.text_input("Enter the YouTube Video URL:")

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    if not url:
        return None
    
    # Clean the URL
    url = url.strip()
    
    # Try regex approach first (more reliable)
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # Fallback to URL parsing
    try:
        parsed_url = urlparse(url)
        
        if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            if parsed_url.path == '/watch':
                return parse_qs(parsed_url.query).get('v', [None])[0]
            elif parsed_url.path.startswith('/embed/'):
                return parsed_url.path.split('/')[2]
            elif parsed_url.path.startswith('/v/'):
                return parsed_url.path.split('/')[2]
        elif parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]
    except Exception as e:
        st.error(f"URL parsing error: {e}")
    
    return None

def get_video_transcript_method1(video_id):
    """Method 1: Direct API call"""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        return " ".join([item['text'] for item in transcript_list])
    except Exception as e:
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join([item['text'] for item in transcript_list])
        except Exception as e2:
            raise Exception(f"Method 1 failed: {str(e)}, {str(e2)}")

def get_video_transcript_method2(video_id):
    """Method 2: Using list_transcripts approach"""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to get English transcript first
        try:
            transcript = transcript_list.find_transcript(['en'])
            fetched_transcript = transcript.fetch()
            return " ".join([item['text'] for item in fetched_transcript])
        except:
            # Get first available transcript
            for transcript in transcript_list:
                try:
                    fetched_transcript = transcript.fetch()
                    return " ".join([item['text'] for item in fetched_transcript])
                except:
                    continue
    except Exception as e:
        raise Exception(f"Method 2 failed: {str(e)}")

def get_video_transcript_method3(video_id):
    """Method 3: Alternative approach using direct HTTP requests"""
    try:
        # This is a fallback method - get video info first
        import json
        
        # YouTube's internal API endpoint (this might change)
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Make a request to get the page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        
        # Look for transcript data in the page
        if 'captions' in response.text:
            st.info("Found captions data, but advanced parsing would be needed")
            return None
        else:
            raise Exception("No captions found in video page")
            
    except Exception as e:
        raise Exception(f"Method 3 failed: {str(e)}")

def get_video_transcript(video_id):
    """Get transcript with multiple fallback methods"""
    if not TRANSCRIPT_API_AVAILABLE:
        raise Exception("YouTube Transcript API is not properly installed. Please run: pip install youtube-transcript-api")
    
    errors = []
    
    # Method 1: Direct API call
    try:
        return get_video_transcript_method1(video_id)
    except Exception as e:
        errors.append(f"Method 1: {str(e)}")
    
    # Method 2: List transcripts approach
    try:
        return get_video_transcript_method2(video_id)
    except Exception as e:
        errors.append(f"Method 2: {str(e)}")
    
    # If all methods fail, provide detailed error information
    error_msg = "All transcript extraction methods failed:\n" + "\n".join(errors)
    error_msg += "\n\nPossible reasons:"
    error_msg += "\n• The video doesn't have captions/subtitles enabled"
    error_msg += "\n• The video is private, unlisted, or age-restricted"
    error_msg += "\n• The video is too new (transcripts not ready)"
    error_msg += "\n• Geographic restrictions apply"
    error_msg += "\n• The video has been deleted or is unavailable"
    
    raise Exception(error_msg)

# Installation instructions
if not TRANSCRIPT_API_AVAILABLE:
    st.error("📦 YouTube Transcript API not found!")
    st.markdown("### Installation Instructions:")
    st.code("pip install youtube-transcript-api", language="bash")
    st.markdown("### Or try:")
    st.code("pip install --upgrade youtube-transcript-api", language="bash")
    st.markdown("### Alternative installation:")
    st.code("conda install -c conda-forge youtube-transcript-api", language="bash")

if st.button("Generate Summary"):
    if not video_url.strip():
        st.warning("Please enter a valid YouTube video URL.")
    else:
        video_id = extract_video_id(video_url)
        if not video_id:
            st.error("Invalid YouTube URL. Please enter a correct URL.")
            st.info("Supported formats:")
            st.info("• https://www.youtube.com/watch?v=VIDEO_ID")
            st.info("• https://youtu.be/VIDEO_ID")
            st.info("• https://www.youtube.com/embed/VIDEO_ID")
        else:
            st.info(f"Extracted Video ID: {video_id}")
            
            if not TRANSCRIPT_API_AVAILABLE:
                st.error("Cannot proceed without YouTube Transcript API. Please install it first.")
            else:
                try:
                    with st.spinner("Fetching transcript..."):
                        transcript = get_video_transcript(video_id)
                        
                        if transcript and len(transcript) < 50:
                            st.warning("Transcript is very short. This might not be a typical video with speech content.")
                    
                    if transcript:
                        with st.spinner("Generating summary..."):
                            summary = chain.run(transcript_=transcript)
                            
                        st.markdown("### Video Summary:")
                        response = summary.replace("\n", "<br>")
                        st.markdown(response, unsafe_allow_html=True)
                        
                        # Show transcript info
                        st.markdown(f"*Transcript length: {len(transcript)} characters*")
                        
                        # Option to show full transcript
                        if st.checkbox("Show full transcript"):
                            st.text_area("Full Transcript:", transcript, height=200)
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Test with sample video
if st.button("🧪 Test with Sample Video"):
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll - known to have captions
    st.info(f"Testing with: {test_url}")
    video_id = extract_video_id(test_url)
    if video_id and TRANSCRIPT_API_AVAILABLE:
        try:
            transcript = get_video_transcript(video_id)
            st.success(f"✅ Test successful! Got {len(transcript)} characters of transcript")
        except Exception as e:
            st.error(f"❌ Test failed: {str(e)}")
    else:
        st.error("Cannot run test - API not available")