from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    prompt = request.form['prompt']
    result = subprocess.run(['python', 'query_data.py', prompt], capture_output=True, text=True)
    answer = result.stdout
    
    # Remove the "Response: " prefix from the answer
    if answer.startswith("Response: "):
        answer = answer[len("Response: "):]
    
    # Process sources to only show filenames and remove duplicates
    if 'Sources:' in answer:
        answer_text, sources_text = answer.split('Sources:')
        sources_list = sources_text.strip().split(',')
        filenames = set()
        for source in sources_list:
            filename = source.split(':')[0].split('\\')[-1].strip()
            filenames.add(filename)
        sources_clean = ', '.join(sorted(filenames))
    else:
        answer_text = answer
        sources_clean = ''

    return render_template('index.html', prompt=prompt, answer=answer_text.strip(), sources=sources_clean)

if __name__ == '__main__':
    app.run(debug=True)