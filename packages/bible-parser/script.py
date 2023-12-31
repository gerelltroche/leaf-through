from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def clean_verse(verse):
    original = verse
    cleaned = verse.replace('\xa0', ' ')
    cleaned = re.sub(r'[^\w\s.,;:\'\"!?+\-*]', '', cleaned)
    cleaned = '\n'.join(line.strip() for line in cleaned.split('\n'))

    # Find positions of * and + in the cleaned text
    note_positions = [m.start() for m in re.finditer('\*', cleaned)]
    footnote_positions = [m.start() for m in re.finditer('\+', cleaned)]

    # Remove * and + from the text
    cleaned = cleaned.replace('*', '').replace('+', '')

    return {
        'text': cleaned,
        'notes': note_positions,
        'footnotes': footnote_positions,
        'original': original
    }


def fetch_and_parse(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    bible_text = soup.find(id='bibleText')
    verses = bible_text.find_all(class_='verse') if bible_text else []

    # Create an array of objects
    verse_texts = [clean_verse(verse.get_text()) for verse in verses]

    footnotes = soup.find_all(class_='footnotes')

    footnotes_filtered = [fn for fn in footnotes if 'none' not in fn.get('class', [])]

    for footnote in footnotes_filtered:
        print(footnote)

#     $('.footnotes').not('[class*="none"]').each(function() {
#     var $footnote = $(this);
#     var $sectionHeading = $footnote.prev('.sectionHeading');

#     console.log($sectionHeading.innerText)
#     console.log($footnote)
# });

    return verse_texts

@app.route('/parse-url', methods=['POST'])
def parse_url():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        parsed_data = fetch_and_parse(url)
        return jsonify(parsed_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)