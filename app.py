import streamlit as st
import json
import random
from PIL import Image
import time
import os
import openai
from typing import Dict, List, Any

from streamlit_lottie import st_lottie
import requests

# Set page configuration
st.set_page_config(
    page_title="Cosmic Vibe Check 2025",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load data from a specific file path
def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        st.error(f"Error loading {file_path}: {e}")
        return None

# Load Lottie animations from a URL
@st.cache_data
def load_lottie_url(url: str):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        return None

# Initialize OpenAI client
def initialize_openai():
    """Initialize OpenAI client with API key"""
    if 'OPENAI_API_KEY' not in st.secrets:
        st.error("OpenAI API key not found in secrets. Please add your API key to .streamlit/secrets.toml")
        return None
    
    try:
        openai.api_key = st.secrets['OPENAI_API_KEY']
        return openai
    except Exception as e:
        st.error(f"Failed to initialize OpenAI: {e}")
        return None

# Generate AI personality analysis
def generate_ai_personality(name: str, age_group: str, answers: List[str], traits: Dict[str, int]) -> Dict[str, Any]:
    """Generate truly intelligent personality analysis based on actual user choices"""
    
    client = initialize_openai()
    if not client:
        return None
    
    # Calculate intelligent introversion/extroversion percentage
    extroversion_score = traits.get('extroversion', 0)
    # Convert trait score to percentage (scores typically range from -10 to +10)
    extroversion_percentage = max(0, min(100, 50 + (extroversion_score * 5)))
    introversion_percentage = 100 - extroversion_percentage
    
    # Create detailed analysis of their specific choices
    prompt = f"""
    You are an expert personality analyst. Analyze {name}'s quiz responses to create an authentic personality reading.
    
    THEIR ACTUAL CHOICES:
    1. Viral content: "{answers[0] if len(answers) > 0 else 'N/A'}"
    2. AI companion role: "{answers[1] if len(answers) > 1 else 'N/A'}"
    3. App discovery: "{answers[2] if len(answers) > 2 else 'N/A'}"
    4. Trip preference: "{answers[3] if len(answers) > 3 else 'N/A'}"
    5. Superpower choice: "{answers[4] if len(answers) > 4 else 'N/A'}"
    
    PERSONALITY ANALYSIS:
    - Extroversion: {extroversion_score} → {extroversion_percentage}% extroverted, {introversion_percentage}% introverted
    - Creativity: {traits.get('creativity', 0)} (higher = artistic/innovative)
    - Ambition: {traits.get('ambition', 0)} (higher = driven/goal-oriented)
    - Empathy: {traits.get('empathy', 0)} (higher = caring/supportive)
    - Adaptability: {traits.get('adaptability', 0)} (higher = flexible/spontaneous)
    
    AGE GROUP: {age_group} - Use appropriate language and references
    
    Based on their ACTUAL choices and personality scores, create:
    
    1. **personality_name**: A unique 2-3 word name that reflects their specific choices (not generic types)
    2. **essence**: One sentence describing their core nature based on what they actually chose
    3. **hidden_trait**: Something surprising about them that emerges from their specific answer patterns (start with "You secretly...")
    4. **superpower**: Their unique strength based on their choices
    5. **vibe_check**: 2-4 words describing their energy
    6. **compatibility_vibes**: 2-3 types of people who would appreciate their specific qualities
    7. **personal_insight**: One personalized insight about their decision-making or values
    8. **social_energy**: One line about their {extroversion_percentage}% extroversion / {introversion_percentage}% introversion based on their choices
    
    IMPORTANT: 
    - Analyze their ACTUAL choices, don't use generic personality types
    - If they chose creative options, reflect that. If they chose social options, reflect that.
    - If they picked food/comfort choices, mention that. If tech/efficiency, mention that.
    - Make the social_energy line specific to their choices (e.g., "You're 70% extroverted because you chose viral dancing and group trips")
    - Make it feel like you truly understood their specific answers
    - Use {age_group} appropriate language
    
    Return as JSON only.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a brilliant personality analyst who creates authentic readings based on specific user choices, not generic types."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=450,
            temperature=0.7  # Balanced creativity
        )
        
        result = response.choices[0].message.content
        
        try:
            parsed = json.loads(result)
            # Add calculated percentages to the result
            parsed['extroversion_percentage'] = extroversion_percentage
            parsed['introversion_percentage'] = introversion_percentage
            return parsed
        except json.JSONDecodeError as json_error:
            # Fallback parsing if JSON fails
            fallback_result = parse_ai_response_smart(result)
            fallback_result['extroversion_percentage'] = extroversion_percentage
            fallback_result['introversion_percentage'] = introversion_percentage
            return fallback_result
            
    except Exception as e:
        st.error(f"AI analysis failed: {e}")
        return None

# ADD this smart fallback parser:
def parse_ai_response_smart(text: str) -> Dict[str, Any]:
    """Smart parser that extracts personality data from text"""
    result = {}
    lines = text.split('\n')
    
    current_key = ""
    current_value = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Look for key patterns
        if 'personality_name' in line.lower() or 'name:' in line.lower():
            current_key = 'personality_name'
            current_value = line.split(':', 1)[-1].strip().strip('"')
        elif 'essence' in line.lower():
            current_key = 'essence'
            current_value = line.split(':', 1)[-1].strip().strip('"')
        elif 'hidden_trait' in line.lower() or 'hidden' in line.lower():
            current_key = 'hidden_trait'
            current_value = line.split(':', 1)[-1].strip().strip('"')
        elif 'superpower' in line.lower():
            current_key = 'superpower'
            current_value = line.split(':', 1)[-1].strip().strip('"')
        elif 'vibe_check' in line.lower() or 'vibe' in line.lower():
            current_key = 'vibe_check'
            current_value = line.split(':', 1)[-1].strip().strip('"')
        elif 'compatibility' in line.lower():
            current_key = 'compatibility_vibes'
            current_value = line.split(':', 1)[-1].strip().strip('"')
        elif 'insight' in line.lower():
            current_key = 'personal_insight'
            current_value = line.split(':', 1)[-1].strip().strip('"')
        elif 'social_energy' in line.lower() or 'social energy' in line.lower():
            current_key = 'social_energy'
            current_value = line.split(':', 1)[-1].strip().strip('"')
        elif current_key and line and not ':' in line:
            # Continue previous value
            current_value += " " + line.strip().strip('"')
        
        if current_key and current_value:
            if current_key == 'compatibility_vibes':
                # Split compatibility into array
                result[current_key] = [v.strip() for v in current_value.split(',')]
            else:
                result[current_key] = current_value
    
    return result

# Inject cosmic-themed CSS
def inject_cosmic_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Reset and base styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Hide Streamlit branding and GitHub elements - COMPLETE REMOVAL */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    header {visibility: hidden !important;}
    .stDecoration {display: none !important;}

    /* Hide GitHub icon and Streamlit elements */
    .stApp > header {display: none !important;}
    .stApp > .main > div > .block-container > div:first-child {display: none !important;}
    iframe[title="streamlit_app"] {display: none !important;}

    /* Hide top toolbar completely */
    .stToolbar {display: none !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    div[data-testid="stDecoration"] {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}

    /* Hide GitHub corner and any branding */
    .github-corner {display: none !important;}
    .streamlit-container {border: none !important;}

    /* Remove Streamlit's default padding and margins */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin-top: 0 !important;
    }

    /* Hide any remaining Streamlit UI elements */
    .stActionButton {display: none !important;}
    button[title="View fullscreen"] {display: none !important;}
    button[kind="header"] {display: none !important;}
    
    /* Make it look like a native app */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 50%, #533483 75%, #7209b7 100%);
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Force full screen without browser UI elements showing */
    html, body {
        margin: 0 !important;
        padding: 0 !important;
        overflow-x: hidden !important;
    }
    
    /* Prevent zoom on mobile (like native apps) */
    input, select, textarea {
        font-size: 16px !important;
        touch-action: manipulation !important;
    }
    
    /* Hide mobile browser UI elements when possible */
    @media screen and (max-width: 768px) {
        .stApp {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            overflow-y: auto !important;
        }
    }
    
    /* Remove any scrollbars that might show */
    ::-webkit-scrollbar {
        width: 0px !important;
        background: transparent !important;
    }
    
    /* Smooth scrolling for mobile */
    html {
        scroll-behavior: smooth !important;
    }
    
    /* Animated stars background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #fff, transparent),
            radial-gradient(1px 1px at 40px 70px, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 90px 40px, rgba(255,255,255,0.6), transparent),
            radial-gradient(2px 2px at 130px 80px, rgba(255,255,255,0.4), transparent),
            radial-gradient(1px 1px at 160px 30px, rgba(255,255,255,0.8), transparent);
        background-repeat: repeat;
        background-size: 200px 150px, 180px 120px, 220px 140px, 250px 160px, 190px 130px;
        animation: twinkling 3s infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes twinkling {
        0% { opacity: 0.8; }
        50% { opacity: 1; }
        100% { opacity: 0.8; }
    }
    
    /* Shooting star animation */
    .shooting-star {
        position: fixed;
        top: 10%;
        right: -100px;
        width: 2px;
        height: 2px;
        background: #fff;
        border-radius: 50%;
        box-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #fff;
        animation: shootingStar 8s linear infinite;
        z-index: 1;
    }
    
    @keyframes shootingStar {
        0% {
            transform: translateX(0) translateY(0);
            opacity: 1;
        }
        70% {
            opacity: 1;
        }
        100% {
            transform: translateX(-1000px) translateY(500px);
            opacity: 0;
        }
    }
    
    /* Cosmic silhouette */
    .cosmic-silhouette {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 300px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 300'%3E%3Cpath d='M0,300 L1200,300 L1200,250 C1100,240 1000,230 900,235 C800,240 700,250 600,245 C500,240 400,225 300,235 C200,245 100,255 50,260 L0,265 Z' fill='%23000'/%3E%3C/svg%3E") bottom center/cover no-repeat;
        z-index: 1;
        pointer-events: none;
    }
    
    /* Main content area */
    .main-content {
        position: relative;
        z-index: 10;
        min-height: 100vh;
        padding: 2rem 1rem;
    }
    
    /* Glass morphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        padding: 2rem;
        margin: 1rem auto;
        max-width: 600px;
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    }
    
    /* Welcome page styles */
    .welcome-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: #fff;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 0 20px rgba(255,255,255,0.5);
        animation: fadeInUp 1s ease-out;
    }
    
    .welcome-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: rgba(255,255,255,0.8);
        text-align: center;
        margin-bottom: 3rem;
        animation: fadeInUp 1s ease-out 0.3s both;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Form elements */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #fff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #7209b7 !important;
        box-shadow: 0 0 0 2px rgba(114, 9, 183, 0.3) !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        display: flex !important;
        gap: 1rem !important;
        justify-content: center !important;
        flex-wrap: wrap !important;
    }
    
    .stRadio > div > label {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 25px !important;
        padding: 0.75rem 1.5rem !important;
        color: #fff !important;
        font-family: 'Inter', sans-serif !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stRadio > div > label:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        border-color: #7209b7 !important;
        transform: translateY(-2px) !important;
    }
    
    /* Labels */
    .form-label {
        display: block;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 500;
        color: #fff;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #7209b7, #533483) !important;
        border: none !important;
        border-radius: 25px !important;
        color: #fff !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(114, 9, 183, 0.4) !important;
        width: 100% !important;
        max-width: 300px !important;
        margin: 0 auto !important;
        display: block !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(114, 9, 183, 0.6) !important;
        background: linear-gradient(135deg, #8a2be2, #6a5acd) !important;
    }
    
    /* Quiz page styles */
    .question-container {
        text-align: center;
        animation: slideInFromSpace 0.8s ease-out;
    }
    
    @keyframes slideInFromSpace {
        from {
            opacity: 0;
            transform: translateY(-50px) scale(0.9);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    .question-number {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    .cosmic-question {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 600;
        color: #fff;
        margin-bottom: 2rem;
        line-height: 1.3;
        text-shadow: 0 0 10px rgba(255,255,255,0.3);
    }
    
    /* Fix for 18-24 age group question visibility */
    .cosmic-question.age-18_24 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #fff !important;
        margin-bottom: 2rem;
        line-height: 1.2;
        text-shadow: 0 0 15px rgba(255, 107, 107, 0.6);
        /* Remove problematic gradient text */
        background: none !important;
        -webkit-background-clip: unset !important;
        -webkit-text-fill-color: #fff !important;
        background-clip: unset !important;
    }

    /* Add a subtle gradient background instead */
    .cosmic-question.age-18_24::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(255, 142, 83, 0.1));
        border-radius: 10px;
        z-index: -1;
    }
    
    /* Option buttons */
    .option-button {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        color: #fff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        padding: 1rem 1.5rem !important;
        margin: 0.5rem 0 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
        width: 100% !important;
        text-align: left !important;
    }
    
    .option-button:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        border-color: #7209b7 !important;
        transform: translateX(10px) !important;
    }
    
    /* Progress bar */
    .cosmic-progress-container {
        width: 100%;
        height: 6px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
        margin: 2rem 0;
        overflow: hidden;
    }
    
    .cosmic-progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #7209b7, #533483, #0f3460);
        border-radius: 3px;
        transition: width 0.5s ease;
        box-shadow: 0 0 10px rgba(114, 9, 183, 0.6);
    }
    
    /* Results page styles */
    .result-card {
        text-align: center;
        animation: cosmicReveal 1.2s ease-out;
    }
    
    @keyframes cosmicReveal {
        0% {
            opacity: 0;
            transform: scale(0.8) rotateY(180deg);
        }
        50% {
            opacity: 0.5;
            transform: scale(0.9) rotateY(90deg);
        }
        100% {
            opacity: 1;
            transform: scale(1) rotateY(0deg);
        }
    }
    
    .result-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 1rem;
        text-shadow: 0 0 20px rgba(255,255,255,0.5);
    }
    
    .personality-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #7209b7, #533483, #0f3460);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
        text-shadow: 0 0 30px rgba(114, 9, 183, 0.8);
    }
    
    .personality-description {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    
    .personality-traits {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    
    .trait-tag {
        background: linear-gradient(135deg, #7209b7, #533483);
        color: #fff;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(114, 9, 183, 0.4);
    }
    
    .main-character-moment {
        margin: 2rem 0;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-character-moment h3 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        color: #fff;
        margin-bottom: 1rem;
    }
    
    .main-character-moment em {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
        font-style: italic;
        line-height: 1.5;
    }
    
    .compatibility {
        margin: 2rem 0;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .compatibility h3 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.2rem;
        color: #fff;
        margin-bottom: 1rem;
    }
    
    .compatibility-types, .red-flag-type {
        display: flex;
        gap: 0.5rem;
        justify-content: center;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
    }
    
    .compatible-type {
        background: rgba(0, 255, 127, 0.2);
        border: 1px solid rgba(0, 255, 127, 0.4);
        color: #00ff7f;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
    }
    
    .red-flag-type {
        background: rgba(255, 69, 0, 0.2);
        border: 1px solid rgba(255, 69, 0, 0.4);
        color: #ff4500;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        justify-content: center;
    }
    
    /* Floating cosmic elements */
    .cosmic-elements {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
    }
    
    .cosmic-star {
        position: absolute;
        width: 4px;
        height: 4px;
        background: #fff;
        border-radius: 50%;
        box-shadow: 0 0 10px #fff;
        animation: float 3s ease-in-out infinite;
    }
    
    .star1 { top: 20%; left: 10%; animation-delay: 0s; }
    .star2 { top: 30%; right: 15%; animation-delay: 1s; }
    .star3 { bottom: 40%; left: 20%; animation-delay: 2s; }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Age-specific question styling */
    .cosmic-question.age-18_24 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 2rem;
        line-height: 1.2;
        text-shadow: 0 0 15px rgba(255, 107, 107, 0.6);
        background: linear-gradient(135deg, #ff6b6b, #ff8e53);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .cosmic-question.age-25_34 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.6rem;
        font-weight: 600;
        color: #fff;
        margin-bottom: 2rem;
        line-height: 1.3;
        text-shadow: 0 0 12px rgba(114, 9, 183, 0.5);
    }

    .cosmic-question.age-35_44 {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 500;
        color: #fff;
        margin-bottom: 2rem;
        line-height: 1.4;
        text-shadow: 0 0 10px rgba(83, 52, 131, 0.4);
    }

    .cosmic-question.age-45_54 {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        font-weight: 500;
        color: #fff;
        margin-bottom: 2rem;
        line-height: 1.5;
        text-shadow: 0 0 8px rgba(106, 90, 205, 0.3);
    }

    .cosmic-question.age-55plus {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 400;
        color: #fff;
        margin-bottom: 2rem;
        line-height: 1.6;
        text-shadow: 0 0 6px rgba(138, 43, 226, 0.2);
    }

    /* Age-specific button styling */
    .age-18_24 .stButton > button {
        background: linear-gradient(135deg, #ff6b6b, #ff8e53) !important;
        border-radius: 20px !important;
        font-weight: 700 !important;
        text-transform: none !important;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4) !important;
    }

    .age-18_24 .stButton > button:hover {
        background: linear-gradient(135deg, #ff5252, #ff7043) !important;
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6) !important;
    }

    .age-25_34 .stButton > button {
        background: linear-gradient(135deg, #7209b7, #533483) !important;
        border-radius: 18px !important;
        font-weight: 600 !important;
    }

    .age-35_44 .stButton > button {
        background: linear-gradient(135deg, #0f3460, #533483) !important;
        border-radius: 15px !important;
        font-weight: 500 !important;
    }

    .age-45_54 .stButton > button {
        background: linear-gradient(135deg, #533483, #6a5acd) !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
    }

    .age-55plus .stButton > button {
        background: linear-gradient(135deg, #6a5acd, #8a2be2) !important;
        border-radius: 10px !important;
        font-weight: 400 !important;
    }

    /* Age-specific glass card styling */
    .age-18_24 .glass-card {
        border: 2px solid rgba(255, 107, 107, 0.3) !important;
        box-shadow: 0 8px 32px rgba(255, 107, 107, 0.2) !important;
    }

    .age-25_34 .glass-card {
        border: 1px solid rgba(114, 9, 183, 0.3) !important;
    }

    .age-35_44 .glass-card {
        border: 1px solid rgba(15, 52, 96, 0.3) !important;
    }

    .age-45_54 .glass-card {
        border: 1px solid rgba(106, 90, 205, 0.3) !important;
    }

    .age-55plus .glass-card {
        border: 1px solid rgba(138, 43, 226, 0.3) !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .welcome-title {
            font-size: 2.5rem;
        }
        
        .cosmic-question {
            font-size: 1.5rem;
        }
        
        .personality-name {
            font-size: 2rem;
        }
        
        .glass-card {
            margin: 1rem;
            padding: 1.5rem;
        }
        
        .stRadio > div {
            flex-direction: column !important;
            align-items: center !important;
        }
        
        .stRadio > div > label {
            width: 100% !important;
            max-width: 300px !important;
            text-align: center !important;
        }
        
        /* Mobile responsive adjustments for age-specific styling */
        .cosmic-question.age-18_24 {
            font-size: 1.4rem;
        }
        
        .cosmic-question.age-25_34 {
            font-size: 1.3rem;
        }
        
        .cosmic-question.age-35_44 {
            font-size: 1.2rem;
        }
        
        .cosmic-question.age-45_54 {
            font-size: 1.15rem;
        }
        
        .cosmic-question.age-55plus {
            font-size: 1.1rem;
        }
    }
    
    /* Lottie animation container */
    .lottie-container {
        margin: 2rem 0;
        display: flex;
        justify-content: center;
    }
    
    /* Error and success messages */
    .stAlert {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px) !important;
        color: #fff !important;
    }
    /* Fix invisible personality name */
    .personality-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #fff !important;
        margin-bottom: 1rem;
        text-shadow: 0 0 20px rgba(114, 9, 183, 0.6);
        text-align: center;
        line-height: 1.2;
        /* Remove problematic gradient */
        background: none !important;
        -webkit-background-clip: unset !important;
        -webkit-text-fill-color: #fff !important;
        background-clip: unset !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for the entire app
def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'
    if 'name' not in st.session_state:
        st.session_state.name = ""
    if 'age_group' not in st.session_state:
        st.session_state.age_group = ""
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'traits' not in st.session_state:
        st.session_state.traits = { 'extroversion': 0, 'creativity': 0, 'ambition': 0, 'empathy': 0, 'adaptability': 0 }
    if 'personality_type' not in st.session_state:
        st.session_state.personality_type = None
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'ai_personality' not in st.session_state:
        st.session_state.ai_personality = None

# Reset the quiz state to start over
def reset_quiz():
    st.session_state.page = 'welcome'
    st.session_state.current_question = 0
    st.session_state.traits = { 'extroversion': 0, 'creativity': 0, 'ambition': 0, 'empathy': 0, 'adaptability': 0 }
    st.session_state.personality_type = None
    st.session_state.answers = []
    st.session_state.ai_personality = None

# Update personality traits based on user's answer
def update_traits(answer_index, selected_answer):
    trait_impacts = {
        0: {"extroversion": -2, "empathy": 2},
        1: {"extroversion": -1, "creativity": 1, "empathy": 1, "adaptability": 1},
        2: {"creativity": 2, "ambition": 1, "adaptability": 1},
        3: {"extroversion": 1, "creativity": 1, "ambition": 2, "empathy": -1},
        4: {"extroversion": 2, "ambition": 1, "empathy": -2, "adaptability": -1}
    }
    impact = trait_impacts.get(answer_index, {})
    for trait, value in impact.items():
        st.session_state.traits[trait] += value
    
    # Store the actual answer text
    st.session_state.answers.append(selected_answer)

# Determine the final personality type
def determine_personality(personalities):
    if not personalities: return None
    final_traits = st.session_state.traits
    highest_trait = max(final_traits, key=final_traits.get)
    matching = [p for p in personalities if p.get('primary_trait', '').lower() == highest_trait.lower()]
    return random.choice(matching) if matching else random.choice(personalities)

# Add cosmic background elements
def add_cosmic_elements():
    st.markdown("""
    <div class="shooting-star"></div>
    <div class="cosmic-silhouette"></div>
    """, unsafe_allow_html=True)

# --- UI Rendering Functions --- #

def render_welcome_page():
    # Add cosmic background elements
    add_cosmic_elements()
    
    # Main content wrapper
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Create centered column
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        st.markdown('<h1 class="welcome-title">🌌 Beyond The Naked Eye</h1>', unsafe_allow_html=True)
        st.markdown('<p class="welcome-subtitle">Discover your cosmic personality in the vast universe of possibilities</p>', unsafe_allow_html=True)
        
        # Name Input
        st.markdown('<label class="form-label">What should we call you, stargazer?</label>', unsafe_allow_html=True)
        name = st.text_input("Name", label_visibility="collapsed", placeholder="Enter your cosmic name...", key="welcome_name")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Age Group Input
        st.markdown('<label class="form-label">What\'s your constellation age group?</label>', unsafe_allow_html=True)
        age_group = st.radio(
            "Age Group",
            options=['18-24', '25-34', '35-44', '45-54', '55+'],
            horizontal=True,
            label_visibility="collapsed"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Start Button
        if st.button("🚀 Begin Your Cosmic Journey", key="start_button"):
            if name:
                st.session_state.name = name
                st.session_state.age_group_label = age_group
                age_map = {'18-24': 18, '25-34': 25, '35-44': 35, '45-54': 45, '55+': 55}
                st.session_state.age = age_map[age_group]
                st.session_state.page = 'quiz'
                st.rerun()
            else:
                st.error("Please enter your cosmic name to begin your journey.")
                
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_quiz_page(questions, slang):
    # Add cosmic background elements
    add_cosmic_elements()
    
    q_idx = st.session_state.current_question
    
    # Get age-specific questions based on the selected age group
    age_group = st.session_state.age_group_label
    
    # Safely get questions for the selected age group or fall back to default
    try:
        age_questions = questions[age_group]
    except (KeyError, TypeError):
        # If age group not found or questions is not properly structured
        if isinstance(questions, dict) and len(questions) > 0:
            first_key = list(questions.keys())[0]
            age_questions = questions[first_key]
        else:
            st.error("No questions available. Please check the questions.json file.")
            age_questions = []
    
    if q_idx >= len(age_questions):
        st.session_state.page = 'ai_loading'
        st.rerun()
        return

    question = age_questions[q_idx]
    
    # Main content wrapper
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Create centered column
    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    with col2:
        st.markdown("<div class='glass-card question-container'>", unsafe_allow_html=True)
        
        # Question number indicator with age group styling
        age_emoji = {
            '18-24': '🔥',
            '25-34': '✨', 
            '35-44': '🌟',
            '45-54': '💫',
            '55+': '⭐'
        }
        
        age_names = {
            '18-24': 'Gen Z Vibes',
            '25-34': 'Millennial Energy',
            '35-44': 'Gen X Style', 
            '45-54': 'Experienced Wisdom',
            '55+': 'Classic Grace'
        }
        
        current_emoji = age_emoji.get(age_group, '🌌')
        current_name = age_names.get(age_group, 'Cosmic')
        
        st.markdown(f"<div class='question-number'>{current_emoji} Question {q_idx + 1} of {len(age_questions)} • {current_name}</div>", unsafe_allow_html=True)
        
        # Question text with age-appropriate styling
        question_class = f"cosmic-question age-{age_group.replace('-', '_').replace('+', 'plus')}"
        st.markdown(f'<h2 class="{question_class}">{question["text"]}</h2>', unsafe_allow_html=True)

        # Display options with age-appropriate styling
        for i, option in enumerate(question['options']):
            if st.button(option, key=f"option_{i}"):
                update_traits(i, option)
                st.session_state.current_question += 1
                if st.session_state.current_question >= len(age_questions):
                    st.session_state.page = 'ai_loading'
                st.rerun()
        
        # Custom progress bar with age-specific colors
        progress_percent = ((q_idx + 1) / len(age_questions)) * 100
        progress_colors = {
            '18-24': 'linear-gradient(90deg, #ff6b6b, #ff8e53, #7209b7)',
            '25-34': 'linear-gradient(90deg, #7209b7, #533483, #0f3460)',
            '35-44': 'linear-gradient(90deg, #0f3460, #533483, #7209b7)', 
            '45-54': 'linear-gradient(90deg, #533483, #7209b7, #8a2be2)',
            '55+': 'linear-gradient(90deg, #8a2be2, #6a5acd, #7209b7)'
        }
        
        progress_color = progress_colors.get(age_group, 'linear-gradient(90deg, #7209b7, #533483, #0f3460)')
        
        st.markdown(f"""
        <div class="cosmic-progress-container">
            <div class="cosmic-progress-bar" style="width: {progress_percent}%; background: {progress_color};"></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- AI Loading Page --- #
def render_ai_loading_page():
    """Show loading screen while AI generates personality"""
    add_cosmic_elements()
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div style="width: 60px; height: 60px; border: 4px solid rgba(255,255,255,0.1); 
                        border-top: 4px solid #7209b7; border-radius: 50%; 
                        animation: spin 1s linear infinite; margin: 0 auto 1rem;">
            </div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.2rem; 
                       color: #fff; margin-bottom: 0.5rem;">🌌 AI Oracle Consulting...</div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.9rem; 
                       color: rgba(255,255,255,0.7);">Revealing your hidden cosmic traits</div>
        </div>
        <style>
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate AI analysis
    time.sleep(2)
    ai_result = generate_ai_personality(
        st.session_state.name, 
        st.session_state.age_group_label,
        st.session_state.answers,
        st.session_state.traits
    )
    
    if ai_result:
        st.session_state.ai_personality = ai_result
        st.session_state.page = 'ai_results'
        st.rerun()
    else:
        # Create a simple fallback personality instead of going to old results
        fallback_personality = {
            "personality_name": "Cosmic Innovator",
            "essence": "You're a unique individual with your own special cosmic energy.",
            "hidden_trait": "You secretly have more potential than you realize.",
            "superpower": "Turning challenges into opportunities",
            "vibe_check": "Creative and authentic",
            "compatibility_vibes": ["Fellow Innovators", "Creative Souls"],
            "personal_insight": "Your unique choices show a thoughtful approach to life.",
            "social_energy": "You balance social energy with personal reflection perfectly.",
            "extroversion_percentage": 60,
            "introversion_percentage": 40
        }
        st.session_state.ai_personality = fallback_personality
        st.session_state.page = 'ai_results'
        st.rerun()

def render_results_page(personalities):
    # Add cosmic background elements
    add_cosmic_elements()
    
    if 'personality_type' not in st.session_state or not st.session_state.personality_type:
        st.session_state.personality_type = determine_personality(personalities)

    personality = st.session_state.personality_type
    if not personality: 
        st.error("Could not determine your cosmic personality. Please try again.")
        if st.button("Try Again", key="try_again_error"): 
            reset_quiz()
            st.rerun()
        return

    # Main content wrapper
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Create centered column layout
    col1, col2, col3 = st.columns([0.2, 3, 0.2])
    with col2:
        st.markdown('<div class="glass-card result-card">', unsafe_allow_html=True)
        
        # Results content - COMPACT VERSION
        st.markdown(f'<h1 class="result-title">The stars have aligned, {st.session_state.name}!</h1>', unsafe_allow_html=True)
        
        # FIXED: Visible personality name
        st.markdown(f'''
        <h2 style="font-family: 'Space Grotesk', sans-serif; font-size: 2.2rem; font-weight: 700; 
                   color: #fff; margin-bottom: 1rem; text-align: center; line-height: 1.2;">
            {personality.get("name", "N/A")}
        </h2>
        ''', unsafe_allow_html=True)
        
        # Compact personality traits
        st.markdown(f'''
        <div style="display: flex; gap: 0.8rem; justify-content: center; margin-bottom: 1.5rem; flex-wrap: wrap;">
            <div style="background: linear-gradient(135deg, #7209b7, #533483); color: #fff; padding: 0.4rem 1rem; 
                       border-radius: 20px; font-size: 0.85rem; font-weight: 500;">
                {personality.get("primary_trait", "").capitalize()}
            </div>
            <div style="background: linear-gradient(135deg, #7209b7, #533483); color: #fff; padding: 0.4rem 1rem; 
                       border-radius: 20px; font-size: 0.85rem; font-weight: 500;">
                {personality.get("secondary_trait", "").capitalize()}
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Compact description
        st.markdown(f'''
        <p style="font-family: 'Inter', sans-serif; font-size: 1rem; color: rgba(255,255,255,0.9); 
                  line-height: 1.5; margin-bottom: 1.5rem; text-align: center;">
            {personality.get("description", "")}
        </p>
        ''', unsafe_allow_html=True)
        
        # Compact main character moment
        st.markdown(f'''
        <div style="background: rgba(255,255,255,0.05); border-radius: 15px; padding: 1.2rem; margin-bottom: 1.5rem;">
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.1rem; color: #fff; 
                      margin-bottom: 0.8rem; text-align: center;">✨ Your Cosmic Moment ✨</h3>
            <em style="font-family: 'Inter', sans-serif; font-size: 0.95rem; color: rgba(255,255,255,0.8); 
                     font-style: italic; line-height: 1.4; display: block; text-align: center;">
                "{personality.get("main_character_moment", "")}"
            </em>
        </div>
        ''', unsafe_allow_html=True)
        
        # Compact compatibility section
        st.markdown(f'''
        <div style="background: rgba(255,255,255,0.05); border-radius: 15px; padding: 1.2rem; margin-bottom: 1.5rem;">
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 1rem; color: #fff; 
                      margin-bottom: 0.8rem; text-align: center;">🌟 Your Cosmic Compatibility</h3>
            <div style="display: flex; gap: 0.6rem; justify-content: center; flex-wrap: wrap; margin-bottom: 1rem;">
        ''', unsafe_allow_html=True)
        
        for compatible_type in personality.get('compatible_with', []):
            st.markdown(f'''
            <div style="background: rgba(0,255,127,0.2); border: 1px solid rgba(0,255,127,0.4); 
                       color: #00ff7f; padding: 0.3rem 0.8rem; border-radius: 15px; 
                       font-size: 0.8rem; text-align: center;">
                {compatible_type}
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown(f'''
            </div>
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 1rem; color: #fff; 
                      margin-bottom: 0.8rem; text-align: center;">⚠️ Your Cosmic Warning Sign</h3>
            <div style="background: rgba(255,69,0,0.2); border: 1px solid rgba(255,69,0,0.4); 
                       color: #ff4500; padding: 0.5rem 1rem; border-radius: 15px; 
                       font-size: 0.8rem; text-align: center; margin: 0 auto; display: inline-block; width: fit-content;">
                {personality.get("red_flag_type", "")}
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Share prompt
        st.markdown('''
        <div style="background: rgba(114,9,183,0.1); border-radius: 15px; padding: 1.2rem; margin-bottom: 1.5rem; text-align: center;">
            <div style="font-family: 'Inter', sans-serif; font-size: 0.9rem; color: rgba(255,255,255,0.9); 
                       line-height: 1.4; margin-bottom: 0.4rem;">
                Screenshot this cosmic reading and share your vibe! ✨
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.75rem; color: rgba(255,255,255,0.6);">
                Tag friends to discover their cosmic personality
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Compact restart button
        if st.button("✨ Take Another Cosmic Journey ✨", key="restart_button"):
            reset_quiz()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_ai_results_page():
    """Display authentic AI-generated personality results"""
    add_cosmic_elements()
    
    if not st.session_state.ai_personality:
        st.session_state.page = 'results'
        st.rerun()
        return
    
    personality = st.session_state.ai_personality
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    # MOBILE OPTIMIZED: Wider content area
    col1, col2, col3 = st.columns([0.05, 4, 0.05])
    with col2:
        st.markdown('<div class="glass-card result-card">', unsafe_allow_html=True)
        
        # MOBILE: Compact title
        st.markdown(f'''
        <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.4rem; font-weight: 700; 
                   color: #fff; margin-bottom: 0.8rem; text-align: center; line-height: 1.2;">
            ✨ {st.session_state.name}\'s Cosmic Identity ✨
        </h1>
        ''', unsafe_allow_html=True)
        
        # MOBILE: Smaller personality name
        st.markdown(f'''
        <h2 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.8rem; font-weight: 700; 
                   color: #fff; margin-bottom: 1rem; text-align: center; line-height: 1.1;
                   text-shadow: 0 0 20px rgba(114, 9, 183, 0.8);">
            {personality.get("personality_name", "Cosmic Soul")}
        </h2>
        ''', unsafe_allow_html=True)
        
        # MOBILE: Compact essence
        if personality.get("essence"):
            st.markdown(f'''
            <div style="background: linear-gradient(135deg, rgba(114, 9, 183, 0.2), rgba(83, 52, 131, 0.2)); 
                        border: 1px solid rgba(114, 9, 183, 0.4); border-radius: 15px; 
                        padding: 1rem; margin: 1rem 0; text-align: center;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1rem; font-weight: 600; 
                           color: #fff; line-height: 1.3;">
                    {personality["essence"]}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # MOBILE OPTIMIZED: Social Energy Percentage - PROPER STREAMLIT COMPONENTS
        if personality.get("extroversion_percentage") is not None:
            extro_pct = personality.get("extroversion_percentage", 50)
            intro_pct = personality.get("introversion_percentage", 50)
            
            st.markdown(f'''
            <div style="background: rgba(255, 255, 255, 0.08); border-radius: 15px; padding: 1.2rem; margin: 1.2rem 0;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.9rem; color: #fff; margin-bottom: 0.8rem; font-weight: 600; text-align: center;">
                    ⚡ Your Social Energy
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Use Streamlit's native progress components instead of raw HTML
            st.markdown("**Extroversion**")
            st.progress(extro_pct / 100, text=f"{extro_pct}%")
            
            st.markdown("**Introversion**")  
            st.progress(intro_pct / 100, text=f"{intro_pct}%")
            
            # MOBILE: Compact AI insight
            if personality.get("social_energy"):
                st.markdown(f'''
                <div style="font-family: 'Inter', sans-serif; font-size: 0.8rem; color: rgba(255, 255, 255, 0.9); 
                           line-height: 1.3; font-style: italic; text-align: center; margin: 1rem 0;">
                    💡 {personality["social_energy"]}
                </div>
                ''', unsafe_allow_html=True)
        
        # MOBILE: Compact hidden trait
        if personality.get("hidden_trait"):
            st.markdown(f'''
            <div style="background: linear-gradient(135deg, rgba(255, 107, 107, 0.25), rgba(255, 142, 83, 0.25)); 
                        border: 2px solid rgba(255, 107, 107, 0.5); border-radius: 15px; 
                        padding: 1.2rem; margin: 1.2rem 0; text-align: center; position: relative;">
                <div style="position: absolute; top: 10px; right: 15px; font-size: 1.2rem;">🔮</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1rem; color: #ff6b6b; 
                           margin-bottom: 0.8rem; font-weight: 700;">Mind = Blown 🤯</div>
                <div style="font-family: 'Inter', sans-serif; font-size: 0.9rem; color: #fff; 
                           line-height: 1.4; font-weight: 500; font-style: italic;">
                    {personality["hidden_trait"]}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # MOBILE: Single column layout for stats
        if personality.get("superpower"):
            st.markdown(f'''
            <div style="background: rgba(114, 9, 183, 0.15); border-radius: 15px; 
                       padding: 1rem; margin: 1rem 0; text-align: center;">
                <div style="font-size: 1.2rem; margin-bottom: 0.4rem;">⚡</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; 
                           color: #7209b7; margin-bottom: 0.5rem; font-weight: 600;">Your Superpower</div>
                <div style="font-family: 'Inter', sans-serif; font-size: 0.9rem; color: #fff; 
                           line-height: 1.3; font-weight: 500;">
                    {personality["superpower"]}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        if personality.get("vibe_check"):
            st.markdown(f'''
            <div style="background: rgba(0, 255, 127, 0.15); border-radius: 15px; 
                       padding: 1rem; margin: 1rem 0; text-align: center;">
                <div style="font-size: 1.2rem; margin-bottom: 0.4rem;">✨</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; 
                           color: #00ff7f; margin-bottom: 0.5rem; font-weight: 600;">Your Energy</div>
                <div style="font-family: 'Inter', sans-serif; font-size: 0.9rem; color: #fff; 
                           line-height: 1.3; font-weight: 500;">
                    {personality["vibe_check"]}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # MOBILE: Compact personal insight
        if personality.get("personal_insight"):
            st.markdown(f'''
            <div style="background: rgba(255, 255, 255, 0.08); border-radius: 15px; 
                       padding: 1.2rem; margin: 1.2rem 0; text-align: center;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.9rem; 
                           color: #fff; margin-bottom: 0.6rem; font-weight: 600;">💡 Personal Insight</div>
                <div style="font-family: 'Inter', sans-serif; font-size: 0.85rem; color: rgba(255, 255, 255, 0.9); 
                           line-height: 1.4; font-style: italic;">
                    {personality["personal_insight"]}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # MOBILE: Compact compatibility
        if personality.get("compatibility_vibes"):
            st.markdown('''
            <div style="background: rgba(255, 255, 255, 0.08); border-radius: 15px; 
                       padding: 1.2rem; margin: 1.2rem 0;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.9rem; color: #fff; 
                           margin-bottom: 0.8rem; font-weight: 600; text-align: center;">💫 You Vibe With</div>
                <div style="display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap;">
            ''', unsafe_allow_html=True)
            
            vibes = personality["compatibility_vibes"] if isinstance(personality["compatibility_vibes"], list) else [personality["compatibility_vibes"]]
            for vibe in vibes[:3]:
                st.markdown(f'''
                <div style="background: rgba(0, 255, 127, 0.2); border: 1px solid rgba(0, 255, 127, 0.4); 
                           color: #00ff7f; padding: 0.4rem 0.8rem; border-radius: 20px; 
                           font-family: 'Inter', sans-serif; font-size: 0.75rem; font-weight: 500; text-align: center;">
                    {vibe}
                </div>
                ''', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)
        
        # MOBILE: Compact share call-to-action
        st.markdown(f'''
        <div style="background: linear-gradient(135deg, rgba(114, 9, 183, 0.2), rgba(83, 52, 131, 0.1)); 
                    border: 1px solid rgba(114, 9, 183, 0.3); border-radius: 15px; 
                    padding: 1.2rem; margin: 1.5rem 0; text-align: center;">
            <div style="font-family: 'Inter', sans-serif; font-size: 0.9rem; color: rgba(255, 255, 255, 0.95); 
                       line-height: 1.4; margin-bottom: 0.4rem; font-weight: 500;">
                This reading was created by analyzing your actual choices 🎯
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.75rem; color: rgba(255, 255, 255, 0.7);">
                Screenshot & share • Tag friends to discover their cosmic identity
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # MOBILE: Compact restart button
        if st.button("🔮 Discover Another Identity", key="restart_button"):
            reset_quiz()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Main Application --- #
def main():
    # Inject our cosmic CSS
    inject_cosmic_css()
    initialize_session_state()

    # Load all required data
    questions = load_data('data/questions.json')
    personalities = load_data('data/personalities.json')
    slang = load_data('data/slang.json')

    if not all([questions, personalities, slang]):
        st.error("Failed to load essential data. The app cannot continue.")
        return

    # Page routing - FORCE AI FLOW ONLY
    if st.session_state.page == 'welcome':
        render_welcome_page()
    elif st.session_state.page == 'quiz':
        render_quiz_page(questions, slang)
    elif st.session_state.page == 'ai_loading':
        render_ai_loading_page()
    elif st.session_state.page == 'ai_results':
        render_ai_results_page()
    elif st.session_state.page == 'results':
        # FORCE REDIRECT TO AI FLOW - NO MORE OLD RESULTS!
        st.session_state.page = 'ai_loading'
        st.rerun()

if __name__ == "__main__":
    main()