from flask import render_template, flash, redirect, url_for, request
from werkzeug.utils import secure_filename
import sys, os
from app import app
from app.tilehuria.tilehuria.polygon2mbtiles import polygon2mbtiles

def scandir(dir): 
    """Walk recursively through a directory and return a list of all files in it"""
    filelist = []
    for path, dirs, files in os.walk(dir):
        for f in files:
            filelist.append(os.path.join(path, f))
    return filelist

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['polygon']
        filename = secure_filename(file.filename)
        pathname = (os.path.join('files', filename))
        file.save(pathname)
        opts = {}
        opts ['infile'] = pathname
        polygon2mbtiles(opts)
        return render_template('upload.html', uploaded_file=filename)
    else:
        return render_template('index.html', title='No file. Try again!')

@app.route('/mbtiles')
def mbtiles():
    all_files = scandir('files')
    tilesets = []
    for filename in all_files:
        (basename, extension) = os.path.splitext(filename)
        if extension == '.mbtiles':
            tilesets.append(filename)
    return render_template('mbtiles.html', title='MBTiles for download',
                           tilesets=tilesets)