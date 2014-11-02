from flask import Flask, render_template, request
import time
import datetime
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/citation', methods=['POST'])
def show_cite():
    url = request.form['url']    # get the url from the form

    # check which service the input is
    if 'youtube' in url:
        # the service is youtube
        service = 'YouTube'
        id  = url.split('?v=', 1)[1] # get the video id

        # get the json for the video
        data  = requests.get('https://gdata.youtube.com/feeds/api/videos/' + id + '?v=2&alt=json')
        entry = data.json()['entry']

        # get video meta
        name  = entry['author'][0]['name']['$t']
        title = entry['title']['$t']
        embed = entry['yt$accessControl'][4]['permission']
        date  = entry['published']['$t']

        # get a friendly date
        date = time.mktime(datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z').timetuple())
        date = datetime.datetime.fromtimestamp(int(date)).strftime('%d %b. %Y')
    elif 'vimeo' in url:
        # the service is vimeo
        service = 'Vimeo'
        id  = url.rsplit('/', 1)[1] # get only the id from the url

        # get the json for the video
        data  = requests.get('https://vimeo.com/api/v2/video/' + id + '.json')
        entry = data.json()[0]

        # get video meta
        name  = entry['user_name']
        title = entry['title']
        embed = entry['embed_privacy']
        date  = entry['upload_date']

        # get a friendly date
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        date = date.strftime('%d %b. %Y')
    else:
        # the service cannot be found
        service = 'unknown'
        return 'Cannot find the service from the url. Make sure the url is correct.'

    # check if the tweet isn't from a company
    if 'company' not in request.form:
        # the name is a real person
        name = name.rsplit(None, 1)[-1] + ', '  + name.rsplit(' ', 1)[0]

    todays_date = datetime.date.today().strftime('%d %b. %Y')

    return render_template(
        'generated.html',
        name=name,
        title=title,
        date=date,
        todays_date=todays_date,
        id=id,
        service=service,
        embed=embed
    )


if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 5000)
