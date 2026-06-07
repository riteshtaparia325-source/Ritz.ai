import os
from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_model_from_dotenv

load_dotenv()
app = Flask(__name__)


client = genai.Client()

@app.route('/')
def home():
    
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_text():
    
    choice = request.form.get('choice', '0')
    user_text = request.form.get('user_text', '').strip()

    if not user_text:
        return jsonify({'error': 'Input text cannot be empty! Please enter some text.'})

    
    if choice == '1':
        instruction = "Explain the following concept like I am 5 years old. Use simple language, analogies, and keep it engaging.\n\nInput Text:\n"
        full_prompt = instruction + user_text
    elif choice == '2':
        instruction = "Provide a concise summary of the following text, highlighting the absolute key takeaways in bullet points.\n\nInput Text:\n"
        full_prompt = instruction + user_text
    elif choice == '3':
        instruction = "Based on the following text, generate 3 multiple-choice questions (with an answer key at the very bottom) to test comprehension.\n\nInput Text:\n"
        full_prompt = instruction + user_text
    elif choice == '4':
        instruction = "Based on the following topic or text, create a detailed, structured study plan with clear milestones and actionable steps.\n\nTopic/Text:\n"
        full_prompt = instruction + user_text
    elif choice == '5':
        instruction = "Act as an expert technical and HR recruiter. Based on the following text or topic, generate 5 challenging, thought-provoking interview questions.\n\nInput Text:\n"
        full_prompt = instruction + user_text
    else:
        
        full_prompt = user_text

    
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=full_prompt
        )
        return jsonify({'result': response.text})
    except Exception as e:
        return jsonify({'error': f'AI Error: {str(e)}'})

    

if __name__ == '__main__':
    
    app.run(debug=True)