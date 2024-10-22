from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Initialize Groq client
groq_client = Groq(api_key = "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")

#groq_endpoint = "https://api.groq.dev/chat/completions"

# Define the supported languages
supported_languages = ["Cobol", "Delphi", "Vb.net"]
supported_languages2 = ["Python", "Java", "C#s","C","C++17","Swift"]

@app.route('/')
def index():
    return render_template('index.html', languages=supported_languages, languages2=supported_languages2)

@app.route('/convert', methods=['POST'])
def convert():
    input_language = request.form['input-language']
    output_language = request.form['output-language']
    input_code = request.form['input-code']

    # Construct the chat message for Groq
    message = {
        "role": "user",
        "content": f"Translate the given {input_language} code to {output_language} code:\n\n{input_code}"
    }

    # Send the message to Groq for completion
    completion = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[message],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Extract code from the completion response
    output_code = ""
    for chunk in completion:
        output_code += chunk.choices[0].delta.content or ""

    return output_code

@app.route('/summary', methods=['POST'])
def summary():
    input_code = request.form['input-code']

    # Construct the chat message for Groq
    message = {
        "role": "user",
        "content": f"Generate a summary for the following code:\n\n{input_code}"
    }

    # Send the message to Groq for completion
    completion = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[message],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Extract summary from the completion response
    summary = ""
    for chunk in completion:
        summary += chunk.choices[0].delta.content or ""

    return jsonify({'summary': summary})

@app.route('/validate', methods=['POST'])
def validate():
    input_language = request.form['input-language']
    input_code = request.form['input-code']

    # Construct the chat message for Groq
    message = {
        "role": "user",
        "content": f"Check for errors in the following {input_language} code and explain if any:\n\n{input_code}"
    }

    try:
        # Send the message to Groq for completion
        completion = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[message],
            temperature=1,
            max_tokens=2048,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Extract validation message from the completion response
        validation_message = ""
        for chunk in completion:
            validation_message += chunk.choices[0].delta.content or ""

        return jsonify({'message': validation_message.strip()})
    except Exception as e:
        return jsonify({'error': str(e)})



if __name__ == '__main__':
    app.run(debug=True)
