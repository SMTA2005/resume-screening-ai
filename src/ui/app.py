import streamlit as st
import requests
import time
import json
from pathlib import Path

# Page config
st.set_page_config(
    page_title="AI Resume Screener | Smart Job Matcher",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hardcoded API URL (sidebar removed as requested)
api_url = "http://localhost:8000"

# Custom CSS for futuristic interactive UI
st.markdown("""
<style>
    /* Animated gradient background */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(-45deg, #0a0f2a, #1a1f3a, #0f172a, #1e1b4b);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
  
    /* Glass card with blur and neon border */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        border-radius: 28px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        padding: 1.8rem;
        margin: 1rem 0;
    }
    .glass-card:hover {
        transform: translateY(-6px);
        border-color: rgba(99, 102, 241, 0.6);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.3);
    }
  
    /* Neon title */
    .neon-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a78bfa, #c084fc, #60a5fa);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-shadow: 0 0 20px rgba(167, 139, 250, 0.5);
        animation: glowPulse 2s infinite;
    }
    @keyframes glowPulse {
        0% { text-shadow: 0 0 5px rgba(167, 139, 250, 0.3); }
        50% { text-shadow: 0 0 25px rgba(167, 139, 250, 0.8); }
        100% { text-shadow: 0 0 5px rgba(167, 139, 250, 0.3); }
    }
  
    /* Drag & drop zone */
    .upload-zone {
        background: rgba(255, 255, 255, 0.05);
        border: 2px dashed rgba(167, 139, 250, 0.6);
        border-radius: 28px;
        padding: 2.5rem;
        text-align: center;
        transition: all 0.3s;
        cursor: pointer;
    }
    .upload-zone:hover {
        border-color: #a78bfa;
        background: rgba(167, 139, 250, 0.1);
        transform: scale(1.01);
    }
  
    /* Skill badges with 3D tilt effect */
    .skill-badge {
        display: inline-block;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 40px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.2rem;
        transition: all 0.2s;
        cursor: default;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .skill-badge:hover {
        transform: scale(1.08) translateY(-2px);
        box-shadow: 0 6px 16px rgba(139, 92, 246, 0.5);
    }
  
    /* Animated progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #3b82f6, #a78bfa, #c084fc);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
    }
    @keyframes shimmer {
        0% { background-position: 0% 0; }
        100% { background-position: 200% 0; }
    }
  
    /* Match card with pulse on hover */
    .match-card {
        background: rgba(30, 30, 60, 0.6);
        backdrop-filter: blur(8px);
        border-radius: 24px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-left: 4px solid #a78bfa;
        transition: all 0.2s;
    }
    .match-card:hover {
        background: rgba(50, 50, 90, 0.8);
        transform: translateX(8px);
        border-left-width: 8px;
    }
  
    /* Score circle animation */
    .score-circle {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: conic-gradient(#a78bfa 0deg, #2d2d5a 0deg);
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        box-shadow: 0 0 20px rgba(167, 139, 250, 0.5);
        animation: pulseRing 1.5s infinite;
    }
    @keyframes pulseRing {
        0% { box-shadow: 0 0 0 0 rgba(167, 139, 250, 0.4); }
        70% { box-shadow: 0 0 0 12px rgba(167, 139, 250, 0); }
        100% { box-shadow: 0 0 0 0 rgba(167, 139, 250, 0); }
    }
  
    /* Footer glow */
    .glow-footer {
        text-align: center;
        margin-top: 3rem;
        color: #94a3b8;
        font-size: 0.8rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Optional confetti
try:
    from streamlit_confetti import st_confetti
except ImportError:
    st_confetti = None

# Header with branding
st.markdown('<div class="neon-title">AI Resume Screener</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#a78bfa; font-size:1.2rem; font-weight:600;">Developed by Taha Ali</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#cbd5e1;">Upload resume → Instant AI job matches with interactive results</p>', unsafe_allow_html=True)

# Main upload area (empty glass box above drag & drop removed)
uploaded_file = st.file_uploader(
    "Drag & drop your resume here",
    type=["pdf", "png", "jpg", "jpeg"],
    help="PDF or image - we'll extract text using AI",
    label_visibility="visible"
)

# Add custom styling for the uploader
st.markdown("""
<style>
.stFileUploader > div {
    background: transparent !important;
}
.stFileUploader > div > div {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

if uploaded_file:
    # Animated progress
    progress_bar = st.progress(0, text="Initiating AI engine...")
    status_text = st.empty()
  
    try:
        # Step 1: Upload
        status_text.markdown("**Uploading to secure servers...**")
        progress_bar.progress(10)
      
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        submit_resp = requests.post(
            f"{api_url}/upload_resume_async",
            files=files
        )
      
        if submit_resp.status_code != 200:
            st.error(f"Upload failed: {submit_resp.text}")
            st.stop()
      
        job_data = submit_resp.json()
        job_id = job_data.get("job_id")
      
        if not job_id:
            st.error("No job ID received")
            st.stop()
      
        # Step 2: Poll with animated text
        status_text.markdown("**AI analyzing skills & experience...**")
        progress_bar.progress(25)
      
        status_url = f"{api_url}/job_status/{job_id}"
        max_attempts = 30
        attempts = 0
      
        while attempts < max_attempts:
            try:
                status_resp = requests.get(status_url, timeout=10)
                if status_resp.status_code == 200:
                    data = status_resp.json()
                    if data["status"] == "completed":
                        progress_bar.progress(100)
                        status_text.success("**Analysis complete!**")
                        result = data["result"]
                        # Confetti if top match > 80%
                        if result.get("matches") and result["matches"][0]["match_score"] > 0.8:
                            if st_confetti:
                                st_confetti()
                            st.balloons()
                        break
                    elif data["status"] == "failed":
                        st.error(f"Processing failed: {data.get('error', 'Unknown')}")
                        st.stop()
                    else:
                        # Dynamic progress messages
                        messages = ["Scanning resume...", "Matching with job database...", "Calculating scores...", "Almost there..."]
                        idx = min(attempts // 3, len(messages)-1)
                        status_text.markdown(f"{messages[idx]}")
                        progress = min(25 + (attempts * 2), 90)
                        progress_bar.progress(progress)
            except:
                pass
            attempts += 1
            time.sleep(1.5)
      
        if attempts >= max_attempts:
            st.error("Timeout – please try again")
            st.stop()
      
        # Display interactive results
        st.markdown("---")
        st.markdown("## Your Personalized Results")
      
        if result.get("matches") and len(result["matches"]) > 0:
            top = result["matches"][0]
            # Top match hero card
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:2rem;">
                <div style="font-size:1.2rem; opacity:0.9;">BEST MATCH</div>
                <div style="font-size:2.8rem; font-weight:800; margin:0.5rem;">{top['category']}</div>
                <div style="display:flex; justify-content:center; margin:1rem;">
                    <div class="score-circle" style="width:120px;height:120px;font-size:2rem;">
                        {int(top['match_score']*100)}%
                    </div>
                </div>
                <div>Matched skills: {', '.join(top.get('matched_skills', [])[:5])}</div>
            </div>
            """, unsafe_allow_html=True)
          
            # All matches with interactive cards
            st.markdown("### Top Job Roles")
            for match in result["matches"][1:]:
                with st.container():
                    st.markdown(f"""
                    <div class="match-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div><strong>{match['category']}</strong><br/>
                            <span style="font-size:0.8rem;">Matched: {', '.join(match.get('matched_skills', [])[:3])}</span>
                            </div>
                            <div style="font-size:1.8rem; font-weight:bold;">{int(match['match_score']*100)}%</div>
                        </div>
                        <div class="stProgress" style="margin-top:8px;">
                            <div style="background:rgba(255,255,255,0.2); border-radius:10px;">
                                <div style="width:{int(match['match_score']*100)}%; background:linear-gradient(90deg,#3b82f6,#a78bfa); height:8px; border-radius:10px;"></div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
      
        # Extracted skills with interactive badges
        if result.get("skills"):
            st.markdown("### Extracted Skills & Keywords")
            cols = st.columns(4)
            for i, skill in enumerate(result["skills"][:20]):
                cols[i % 4].markdown(f"<div class='skill-badge'>{skill}</div>", unsafe_allow_html=True)
      
        # Download button with hover
        st.markdown("---")
        col_down, _ = st.columns([1,3])
        with col_down:
            st.download_button(
                label="Export results as JSON",
                data=json.dumps(result, indent=2),
                file_name="resume_match_report.json",
                mime="application/json",
                use_container_width=True
            )
      
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Glowing footer
st.markdown("""
<div class="glow-footer">
    Developed by Taha Ali | Secure & Instant | ❤
</div>
""", unsafe_allow_html=True)