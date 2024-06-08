from flask import Flask, render_template, request, send_from_directory, url_for
import os
import subprocess
import re
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
EXP_FOLDER = os.path.join(UPLOAD_FOLDER, 'exp')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXP_FOLDER'] = EXP_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(EXP_FOLDER):
    os.makedirs(EXP_FOLDER)


def extract_counts(output):
    """Extract the number of Bacterias and Fungis from the YOLOv5 output."""
    bacteria_match = re.search(r'(\d+) Bacterias', output)
    fungi_match = re.search(r'(\d+) Fungis', output)
    bacteria_count = bacteria_match.group(1) if bacteria_match else '0'
    fungi_count = fungi_match.group(1) if fungi_match else None
    return bacteria_count, fungi_count


def process_image(filepath):
    """Process an image using a YOLOv5 model and return the path to the processed image."""
    filename = os.path.basename(filepath)
    processed_image_path = os.path.join(EXP_FOLDER, filename)
    
    train_command = f"python yolov5/segment/predict.py --img 320 --weights yolov5/bestptweights/best.pt --hide-labels --source {filepath} --project {UPLOAD_FOLDER} --exist-ok "
    res = subprocess.run(train_command, shell=True, capture_output=True, text=True)
    print('RES',res.stderr,'RES /n /n /n /n')
    bacteria_count, fungi_count = extract_counts(res.stderr)
    
    if os.path.exists(processed_image_path):
        return processed_image_path, bacteria_count, fungi_count
    else:
        return None, None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            processed_image_path, bacteria_count, fungi_count = process_image(filepath)
            if processed_image_path:
                processed_image_url = url_for('processed_file', filename=filename)
                return render_template('index.html', uploaded_file=filename, processed_image_url=processed_image_url, bacteria_count=bacteria_count, fungi_count=fungi_count)
            else:
                return render_template('index.html', uploaded_file=filename, error="Processed image not found.")
    return render_template('index.html')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploads/exp/<path:filename>')
def processed_file(filename):
    return send_from_directory(app.config['EXP_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)


#def process_image(filepath):
#    train_command = f"python yolov5/segment/predict.py --img 320 --weights yolov5/bestptweights/best.pt --hide-labels --source {filepath} --project static/uploads/exp --exist-ok --name="
#    subprocess.run(train_command, shell=True)
#    
#    processed_image_path = 'exp/processed_image.jpg'
#    return url_for('serve_uploads', filename=processed_image_path)

