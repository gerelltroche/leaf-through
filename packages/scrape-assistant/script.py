from flask import Flask, request, jsonify
import openai
from prompt_template import generate_prompt

app = Flask(__name__)

# TODO: Move to .env
openai.api_key = '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'

@app.route('/process_data', methods=['POST'])
def process_data():
    # Create a folder for the current day
    today = datetime.date.today().strftime("%Y-%m-%d")
    folder_path = f"./data/{today}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    request_data = request.get_json()
    html_data = request_data['html']
    json_data = request_data['json']

    prompt = generate_prompt(html_data, json_data)

    try:
        response = openai.Completion.create(
            engine="text-davinci-004",
            prompt=prompt,
            max_tokens=150
        )
        gpt_response = response.choices[0].text

        # Check if the response contains suggestions and save it if it does
        if "suggestions" in gpt_response.lower():
            file_name = f"{folder_path}/suggestions_{datetime.datetime.now().strftime('%H-%M-%S')}.txt"
            with open(file_name, 'w') as file:
                file.write(gpt_response)

        return jsonify({"gpt_response": gpt_response})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
