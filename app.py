import os
from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

client = genai.Client()

# Centralized prompt dictionary for consistency across routes
PROMPT_INSTRUCTIONS = {
    '1': "Explain the following concept like I am 5 years old. Use simple language, analogies, and keep it engaging.\n\nInput Text:\n",
    '2': "Provide a concise summary of the following text, highlighting the absolute key takeaways in bullet points.\n\nInput Text:\n",
    '3': "Based on the following text, generate 3 multiple-choice questions (with an answer key at the very bottom) to test comprehension.\n\nInput Text:\n",
    '4': "Based on the following topic or text, create a detailed, structured study plan with clear milestones and actionable steps.\n\nTopic/Text:\n",
    '5': "Act as an expert technical and HR recruiter. Based on the following text or topic, generate 5 challenging, thought-provoking interview questions.\n\nInput Text:\n",
    '6': "Act as a harsh venture capitalist. Critique the following pitch deck or startup idea using the Business Model Canvas. Highlight weak revenue streams, market gaps, and realistic risks. Be direct and analytical.\n\nInput Text:\n",
    '7': "Act as an expert competitive programming mentor. Analyze the following C/C++ or Java code. DO NOT rewrite the code or give the direct answer. Only provide hints regarding Big O time/space complexity, potential memory leaks, and edge cases.\n\nCode:\n"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_text():
    choice = request.form.get('choice', '0')
    user_text = request.form.get('user_text', '').strip()
    model_choice = request.form.get('model', 'gemini-3.5-flash')
    system_prompt = request.form.get('system_prompt', '').strip()

    if not user_text:
        return jsonify({'error': 'Input text cannot be empty! Please enter some text.'})

    # Build the base prompt
    base_instruction = PROMPT_INSTRUCTIONS.get(choice, "")
    full_prompt = base_instruction + user_text

    # Inject Dynamic System Prompt if provided
    if system_prompt:
        full_prompt = f"CRITICAL SYSTEM INSTRUCTIONS: {system_prompt}\n\n---\n\n{full_prompt}"

    try:
        response = client.models.generate_content(
            model=model_choice,
            contents=full_prompt
        )
        return jsonify({'result': response.text})
    except Exception as e:
        return jsonify({'error': f'AI Error: {str(e)}'})

@app.route('/compare', methods=['POST'])
def compare_modes():
    data = request.get_json() or {}
    user_text = data.get('user_text', '').strip()
    choice1 = data.get('choice1', '0')
    choice2 = data.get('choice2', '0')
    model_choice = data.get('model', 'gemini-3.5-flash')
    system_prompt = data.get('system_prompt', '').strip()

    if not user_text:
        return jsonify({'error': 'Input text cannot be empty! Please enter some text.'}), 400

    prompt1 = PROMPT_INSTRUCTIONS.get(choice1, "") + user_text
    prompt2 = PROMPT_INSTRUCTIONS.get(choice2, "") + user_text

    if system_prompt:
        system_prefix = f"CRITICAL SYSTEM INSTRUCTIONS: {system_prompt}\n\n---\n\n"
        prompt1 = system_prefix + prompt1
        prompt2 = system_prefix + prompt2

    try:
        response1 = client.models.generate_content(model=model_choice, contents=prompt1)
        response2 = client.models.generate_content(model=model_choice, contents=prompt2)

        return jsonify({
            'result1': response1.text,
            'result2': response2.text
        })
    except Exception as e:
        return jsonify({'error': f'AI Error during comparison: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)