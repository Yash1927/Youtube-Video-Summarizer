from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a YouTube video summarizer. Summarize the provided transcript into key bullet points, keeping it under 250 words. Focus on the most important information and use simple English. """

def extract_video_id(url):
    parse_url = urlparse(url)
    if parse_url.hostname in ["youtube.com", "www.youtube.com"]:
        return parse_qs(parse_url.query).get("v", [None])[0]
    elif parse_url.hostname == "youtu.be":
        return parse_url.path[1:]
    else: 
        return None
    
def extract_transcript(video_url):
    try:
        video_id = extract_video_id(video_url)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join(entry["text"] for entry in transcript_text)
        return transcript
    except Exception as e:
        st.error(e)

def summarizer(prompt, transcript):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt + transcript)
    return response.text

st.title("YouTube Video Summarizer")

video_link = st.text_input("Enter Video Link")

if video_link:
    video_id = extract_video_id(video_link)
    if video_id:
            st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    else:
        st.error("Invalid Video Link")


if st.button("Get Video Summary"):
    transcript = extract_transcript(video_link) 
    if transcript:
        with st.spinner("generating content"):
            summary = summarizer(prompt, transcript)
            st.markdown(summary)