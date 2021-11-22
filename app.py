#todo: convert to single page (COMPLETE BUT NEEDS MORE TESTING)
#todo: File preview before clicking
#todo: CSS to make it pretty (easily differentiate between files, potential popup for uploading files)
#todo: Fix redirects to work with nginx
#todo: User accounts with personal folder as well as public folder
#todo: File delete within app
#todo: Move file uploads into a separate thread to prevent page hanging on large file upload

import os
from flask import Flask, render_template, request, redirect, abort, send_file
from threading import Thread

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.config['UPLOAD_PATH'] = 'uploads'
app.config['DOWNLOAD_PATH'] = '~/Downloads'

class PostReqHandler(Thread):
    def __init__(self, request):
        super(PostReqHandler, self).__init__()
        self.request = request

    def run(self):
        if self.request.files:
            file = self.request.files["file"] 
            file.save(os.path.join(app.config["UPLOAD_PATH"], file.filename))
            file.close()

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/', methods=['GET', 'POST'])
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    if request.method == "POST":
        handler = PostReqHandler(request)
        print("POST Request Handler Created...")
            
        '''
        File currently saving, but file data is completely empty.
        Most likely this is due to 'RuntimeError: Working outside of request context.' Error
        Have fun future me
        '''
        
        handler.start()
        return redirect(request.url)
    return render_template('index.html', files=files)

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    BASE_DIR = 'uploads'

    abs_path = os.path.join(BASE_DIR, req_path)

    if not os.path.exists(abs_path):
        return abort(404)

    if os.path.isfile(abs_path):
        return send_file(abs_path)

    files = os.listdir(abs_path)

if __name__=="__main__":
    app.run(host='0.0.0.0')
