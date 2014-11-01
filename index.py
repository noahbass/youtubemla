from flask import Flask, render_template, request
import datetime
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/citation', methods=['POST'])
def show_cite():
    url = request.form['url']    # get the url from the form
    id  = url.split('?v=', 1)[1] # get the video id

    # get the json for the video
    data = requests.get('https://gdata.youtube.com/feeds/api/videos/' + id + '?v=2&alt=json')
    entry = data.json()['entry']

    # get video meta
    name        = entry['author'][0]['name']['$t']
    title       = entry['title']['$t']
    date        = entry['published']['$t']
    todays_date = datetime.date.today().strftime('%d %b. %Y')

    # check if the tweet isn't from a company
    if 'company' not in request.form:
        # set the name as it is a real person
        name = name.rsplit(None, 1)[-1] + ', '  + name.rsplit(' ', 1)[0]

    return render_template(
        'generated.html',
        name=name,
        title=title,
        date=date,
        todays_date=todays_date,
        id=id
    )


if __name__ == '__main__':
    app.debug = False
    app.run(host = 'localhost', port = 5000)
