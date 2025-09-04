import streamlit as st
import json
from llm_helper import analyze_meeting_groq, get_meeting_summary

# Page config
st.set_page_config(
    page_title="Meeting Analyzer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .success-box {
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .section-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .item-bullet {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1rem;
        margin: 0.3rem 0;
        border-radius: 25px;
        border-left: 4px solid #4facfe;
    }
    .stTextArea > div > div > textarea {
        background: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 10px;
    }
    .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Header
st.markdown("""
<div class="main-header">
    <h1>🎯 Smart Meeting Analyzer</h1>
    <p>Transform your meeting transcripts into actionable insights with AI</p>
</div>
""", unsafe_allow_html=True)

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["📝 Analyze Transcript", "📊 Quick Stats", "ℹ️ About"])

with tab1:
    # Main content area with improved layout
    col_input, col_preview = st.columns([2, 1])
    
    with col_input:
        st.markdown("### 📄 Meeting Transcript Input")
        
        # Text area for transcript input with enhanced styling
        transcript = st.text_area(
            "",
            height=400,
            placeholder="📝 Paste your meeting transcript here...\n\nExample:\nJohn: Good morning everyone, let's start with the project updates...\nSarah: The marketing campaign is on track for next Friday...",
            help="💡 Tip: Include speaker names for better analysis"
        )
        
        # Enhanced analyze button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            analyze_clicked = st.button(
                "🚀 Analyze Meeting", 
                type="primary", 
                use_container_width=True,
                help="Click to analyze your meeting transcript"
            )
    
    with col_preview:
        st.markdown("### 📈 Analysis Preview")
        if transcript.strip():
            # Show some basic stats
            word_count = len(transcript.split())
            char_count = len(transcript)
            estimated_time = word_count // 150  # Average speaking pace
            
            st.markdown(f"""
            <div class="section-card">
                <h4>📊 Transcript Stats</h4>
                <p><strong>Words:</strong> {word_count:,}</p>
                <p><strong>Characters:</strong> {char_count:,}</p>
                <p><strong>Est. Speaking Time:</strong> {estimated_time} min</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("📝 Paste your transcript to see preview stats")

    # Analysis results
    if analyze_clicked:
        if transcript.strip():
            with st.spinner("🔍 Analyzing your meeting transcript... Please wait"):
                # Progress bar for better UX
                progress_bar = st.progress(0)
                for i in range(100):
                    progress_bar.progress(i + 1)
                
                # Get analysis
                result = analyze_meeting_groq(transcript)
                progress_bar.empty()
                
                # Check if there was an error
                if "error" in result:
                    st.error(f"❌ Analysis Error: {result['error']}")
                    if "raw_response" in result:
                        with st.expander("🔍 Debug Information"):
                            st.code(result["raw_response"])
                else:
                    # Success message
                    st.markdown("""
                    <div class="success-box">
                        <h3>✅ Analysis Complete!</h3>
                        <p>Your meeting has been successfully analyzed. Review the insights below.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Enhanced results layout
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Action Items with enhanced styling
                        st.markdown("""
                        <div class="section-card">
                            <h3>📋 Action Items</h3>
                        """, unsafe_allow_html=True)

                        action_items = result.get("action_items", [])
                        if action_items:
                            for i, item in enumerate(action_items, 1):
                                # Check if item is a dict
                                if isinstance(item, dict):
                                    task = item.get("task", "No task specified")
                                    assignee = item.get("assignee", "Unassigned")
                                    deadline = item.get("deadline", "No deadline")
                                    
                                    st.markdown(f"""
                                    <div class="item-bullet" style="padding:0.8rem; margin-bottom:0.5rem;">
                                        <strong>Task {i}:</strong> {task}<br>
                                        <strong>Assignee:</strong> {assignee}<br>
                                        <strong>Deadline:</strong> {deadline}
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    # fallback if it's not a dict
                                    st.markdown(f"""
                                    <div class="item-bullet" style="padding:0.8rem; margin-bottom:0.5rem;">
                                        <strong>Task {i}:</strong> {str(item)}
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.info("No specific action items identified")

                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Deadlines
                        st.markdown("""
                        <div class="section-card">
                            <h3>⏰ Important Deadlines</h3>
                        """, unsafe_allow_html=True)
                        
                        if result.get("deadlines"):
                            for i, deadline in enumerate(result["deadlines"], 1):
                                st.markdown(f"""
                                <div class="item-bullet">
                                    <strong>{i}.</strong> {deadline}
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No specific deadlines mentioned")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col2:
                        # Decisions
                        st.markdown("""
                        <div class="section-card">
                            <h3>✅ Key Decisions</h3>
                        """, unsafe_allow_html=True)
                        
                        if result.get("decisions"):
                            for i, decision in enumerate(result["decisions"], 1):
                                st.markdown(f"""
                                <div class="item-bullet">
                                    <strong>{i}.</strong> {decision}
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No major decisions recorded")
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Participants
                        st.markdown("""
                        <div class="section-card">
                            <h3>👥 Meeting Participants</h3>
                        """, unsafe_allow_html=True)
                        
                        if result.get("participants"):
                            participant_cols = st.columns(2)
                            for i, participant in enumerate(result["participants"]):
                                with participant_cols[i % 2]:
                                    st.markdown(f"👤 **{participant}**")
                        else:
                            st.info("Participants not clearly identified")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Summary with improved readability
                    st.markdown("""
                    <div class="section-card">
                        <h3>📝 Executive Summary</h3>
                    """, unsafe_allow_html=True)
                    
                    if result.get("summary"):
                        for i, point in enumerate(result["summary"], 1):
                            # Check if point is a dictionary and extract fields
                            if isinstance(point, dict):
                                summary_text = point.get("point", point.get("summary", point.get("description", "No summary specified")))
                                category = point.get("category", "")
                                
                                category_text = f"<br><em>📂 Category:</em> {category}" if category else ""
                                
                                st.markdown(f"""
                                <div class="item-bullet">
                                    <strong>📌 Key Point {i}:</strong> {summary_text}{category_text}
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                # Clean the summary point
                                clean_point = str(point).strip("{}\"'").replace("'summary':", "").replace("'point':", "").replace("'key_point':", "")
                                st.markdown(f"""
                                <div class="item-bullet">
                                    <strong>📌 Key Point {i}:</strong> {clean_point}
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.info("Summary not available")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Raw data in collapsible section
                    with st.expander("🔍 View Raw Analysis Data", expanded=False):
                        st.json(result)
                        
                    # Download options
                    st.markdown("### 💾 Export Options")
                    col_exp1, col_exp2, col_exp3 = st.columns(3)
                    
                    with col_exp1:
                        # Create formatted text summary
                        summary_text = f"""
MEETING ANALYSIS REPORT
========================

ACTION ITEMS:
{chr(10).join(f"• {item}" for item in result.get("action_items", []))}

DEADLINES:
{chr(10).join(f"• {deadline}" for deadline in result.get("deadlines", []))}

DECISIONS:
{chr(10).join(f"• {decision}" for decision in result.get("decisions", []))}

PARTICIPANTS:
{chr(10).join(f"• {participant}" for participant in result.get("participants", []))}

SUMMARY:
{chr(10).join(f"• {point}" for point in result.get("summary", []))}
                        """
                        st.download_button(
                            "📄 Download Report",
                            summary_text,
                            "meeting_analysis.txt",
                            "text/plain"
                        )
                    
                    with col_exp2:
                        st.download_button(
                            "📊 Download JSON",
                            json.dumps(result, indent=2),
                            "meeting_analysis.json",
                            "application/json"
                        )
                    
                    with col_exp3:
                        st.button("📧 Email Report", help="Feature coming soon!")
        else:
            st.warning("⚠️ Please enter a meeting transcript to analyze.")

with tab2:
    st.markdown("### 📊 Usage Statistics")
    
    # Mock statistics (you can make these real by storing in session state)
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.metric("Meetings Analyzed", "1", "↗️")
    with col_stat2:
        st.metric("Action Items Found", "0", "→")
    with col_stat3:
        st.metric("Participants Identified", "0", "→")
    with col_stat4:
        st.metric("Time Saved", "0 min", "→")

with tab3:
    st.markdown("""
    ### 🎯 About Smart Meeting Analyzer
    
    This AI-powered tool helps you extract valuable insights from your meeting transcripts:
    
    **Features:**
    - 📋 **Action Item Extraction** - Automatically identifies tasks and assignments
    - ⏰ **Deadline Detection** - Finds important dates and timelines
    - ✅ **Decision Tracking** - Captures key decisions made during meetings
    - 👥 **Participant Identification** - Lists meeting attendees
    - 📝 **Smart Summarization** - Provides concise meeting summaries
    
    **Tips for Best Results:**
    - Include speaker names in your transcript
    - Ensure clear formatting and complete sentences
    - Include dates, times, and specific details
    - Review the raw data for additional insights
    """)

# Enhanced Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <h2>🚀 Quick Start Guide</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 📖 How to Use
    
    1. **📝 Paste Transcript**
       - Copy your meeting transcript
       - Include speaker names for better analysis
    
    2. **🔍 Analyze**
       - Click the "Analyze Meeting" button
       - Wait for AI processing
    
    3. **📊 Review Results**
       - Action items and deadlines
       - Key decisions and participants
       - Executive summary
    
    4. **💾 Export**
       - Download as text or JSON
       - Share with your team
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 💡 Pro Tips
    
    ✅ **Include speaker names**  
    ✅ **Use clear timestamps**  
    ✅ **Mention specific dates**  
    ✅ **Include action verbs**  
    ✅ **Review raw data**  
    """)
    
    st.markdown("---")
    
    # Sample transcript button
    if st.button("📄 Load Sample Transcript", use_container_width=True):
        st.info("Copy the sample transcript from the About tab and paste it in the main area!")

# Footer
st.markdown("""
---
<div style='text-align: center; color: #666;'>
    <p>Built with ❤️ using <strong>Streamlit</strong> and <strong>Groq LLM</strong></p>
    <p>Developed by <strong>Shrinivass Raju</strong> | © Smart Meeting Analyzer | Version 1.0</p>
</div>
""", unsafe_allow_html=True)