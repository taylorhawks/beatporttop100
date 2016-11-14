from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    import requests
    from bs4 import BeautifulSoup
    import json
    r = requests.get('https://www.beatport.com/top-100')
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        json_string = soup.select("#data-objects")[0].text.split('window.Playables = ')[1].split(';')[0]
        tracks = json.loads(json_string)['tracks']
        return render(request, 'mainapp/index.html', {
            "tracks": tracks
        })
    else:
        return HttpResponse('<p>Could not load from Beatport.</p>')


def detail(request, id):
    import matplotlib.pyplot as plt
    import requests
    from bs4 import BeautifulSoup
    import json
    r = requests.get('https://www.beatport.com/top-100')
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        json_string = soup.select("#data-objects")[0].text.split('window.Playables = ')[1].split(';')[0]
        track = json.loads(json_string)['tracks'][int(float(id))]
        #librosa
        import librosa as lr
        from librosa.display import specshow
        import numpy as np
        import urllib2
        import io
        import sys
        import base64
        preview = track["preview"]["mp3"]["url"]
        f=file('sample.mp3', 'w')
        url=urllib2.urlopen(preview)
        f.write(url.read(1048*1048))
        y, sr = lr.load(f.name)
        #cqt
        CQT = lr.logamplitude(lr.cqt(y, sr=sr)**2, ref_power=np.max)
        plt.subplot(1, 1, 1)
        specshow(CQT, y_axis='cqt_hz')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Constant-Q power spectrogram (Hz)')

        ###save it
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        cqtimg = "data:image/png;base64," + base64.b64encode(buf.getvalue())
        plt.close()
        #chromagram
        C = lr.feature.chroma_cqt(y=y, sr=sr)
        plt.subplot(1, 1, 1)
        specshow(C, y_axis='chroma')
        plt.colorbar()
        plt.title('Chromagram')
        ###save it
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chromagramimg = "data:image/png;base64," + base64.b64encode(buf.getvalue())
        plt.close()
        #plt.show()
        return render(request, 'mainapp/detail.html', {
            "track": track,
            "cqtimg": cqtimg,
            "chromagramimg": chromagramimg,
        })
    else:
        return HttpResponse('<p>Could not load from Beatport.</p>')
