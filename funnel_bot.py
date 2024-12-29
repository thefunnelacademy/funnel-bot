from flask import Flask, request, jsonify, send_from_directory
import openai
import os

app = Flask(__name__)

# Use an environment variable for the API key
openai.api_key = os.getenv('OPENAI_API_KEY', 'default-placeholder-key')

@app.route('/')
def home():
    return "Welcome to the Funnel Builder Bot!"

@app.route('/generate_content', methods=['POST'])
def generate_content():
    data = request.get_json()

    page_type = data.get('page_type', 'squeeze')
    goal = data.get('goal', 'lead generation')
    product = data.get('product', 'a product')
    audience = data.get('audience', 'an audience')

    # Generate content using OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a copywriting assistant specialized in creating funnel pages. "
                        "Generate content based on the provided input."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Create a {page_type} page for {goal}. The product is {product}, "
                        f"and the target audience is {audience}. Provide a compelling copy."
                    )
                }
            ]
        )

        funnel_content = response['choices'][0]['message']['content']
        return jsonify({"page_type": page_type, "content": funnel_content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to serve ai-plugin.json
@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
    return send_from_directory('.', 'ai-plugin.json', mimetype='application/json')

# Route to serve openapi.json
@app.route('/.well-known/openapi.json')
def serve_openapi():
    return send_from_directory('.', 'openapi.json', mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
