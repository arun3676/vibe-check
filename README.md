# 🌌 Cosmic Vibe Check 2025

A personalized AI-powered cosmic personality quiz that reveals your unique cosmic identity based on your actual choices.

## ✨ Features

- **AI-Powered Analysis**: Uses OpenAI to generate authentic personality readings based on your specific quiz answers
- **Age-Appropriate Questions**: Tailored questions and styling for different age groups (18-24, 25-34, 35-44, 45-54, 55+)
- **Beautiful Cosmic UI**: Stunning space-themed interface with animations and responsive design
- **Social Energy Analysis**: Extroversion/Introversion breakdown with visual progress bars
- **Shareable Results**: Screenshot-friendly personality results perfect for social media

## 🚀 Live Demo

[Try the Cosmic Vibe Check](https://your-streamlit-app-url.streamlit.app)

## 🛠️ Setup

### Option 1: Run Locally

1. Clone the repository:
```bash
git clone https://github.com/yourusername/vibe-check.git
cd vibe-check
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
   - Create `.streamlit/secrets.toml`
   - Add: `OPENAI_API_KEY = "your-api-key-here"`

4. Run the app:
```bash
cd cosmic-vibe-check
streamlit run app.py
```

### Option 2: Deploy on Streamlit Cloud

1. Fork this repository
2. Connect to Streamlit Cloud
3. Add your OpenAI API key in Streamlit Cloud secrets:
   - Key: `OPENAI_API_KEY`
   - Value: Your OpenAI API key
4. Deploy!

## 📁 Project Structure

```
vibe-check/
├── cosmic-vibe-check/
│   ├── app.py                 # Main Streamlit application
│   ├── data/
│   │   ├── personalities.json # Personality type definitions
│   │   ├── questions.json     # Age-specific quiz questions
│   │   └── slang.json        # Age-appropriate language
│   └── requirements.txt      # Python dependencies
├── .streamlit/
│   └── secrets.toml          # API keys (local only)
└── requirements.txt          # Root dependencies
```

## 🎯 How It Works

1. **Welcome**: Enter your name and age group
2. **Quiz**: Answer 5 age-appropriate questions
3. **AI Analysis**: OpenAI analyzes your specific choices
4. **Results**: Get your unique cosmic personality with:
   - Personality name based on your answers
   - Hidden traits and insights
   - Social energy breakdown
   - Compatibility analysis
   - Personalized advice

## 🔧 Configuration

The app uses OpenAI's GPT-3.5-turbo model to generate personality analyses. Make sure you have:

- A valid OpenAI API key
- Sufficient API credits
- Internet connection for AI analysis

## 🎨 Features

- **Responsive Design**: Works perfectly on mobile and desktop
- **Age-Specific Styling**: Different visual themes for each age group
- **Smooth Animations**: Cosmic-themed animations and transitions
- **Progress Tracking**: Visual progress bars throughout the quiz
- **Error Handling**: Graceful fallbacks for API issues

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the [MIT License](LICENSE). 