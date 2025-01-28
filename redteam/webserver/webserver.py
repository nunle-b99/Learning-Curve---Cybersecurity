from flask import Flask, request, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Ordner für die Speicherung der hochgeladenen Dateien
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Funktion zur Überprüfung der Dateierweiterung
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Überprüfen, ob die Datei im Request enthalten ist
        if 'file' not in request.files:
            flash('Kein Dateiteil im Request')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Überprüfen, ob der Benutzer keine Datei ausgewählt hat
        if file.filename == '':
            flash('Keine ausgewählte Datei')
            return redirect(request.url)
        
        # Wenn die Datei erlaubt ist, wird sie gespeichert
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Sichere Dateinamen
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Sicherstellen, dass der Upload-Ordner existiert
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            file.save(upload_path)  # Datei speichern
            
            return f"Datei erfolgreich hochgeladen: {filename}"

@app.route('/download/<filename>')
def download_file(filename):
    return f"Herunterladen der Datei: {filename}"

if __name__ == '__main__':
    app.run(debug=True)
