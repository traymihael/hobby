from flask import Flask, render_template
from line_analysis.analyse import used_data

app = Flask(__name__)


@app.route('/')
def index():
    partner = "test_talk.txt"
    context = used_data(partner)
    return render_template('index.html', context=context)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
