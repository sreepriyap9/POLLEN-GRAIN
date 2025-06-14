import os
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Important for flash messages

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Changed to static folder
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Load the pre-trained model with compilation
try:
    model = load_model('model.h5', compile=True)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    exit(1)

# Class names (must match your model's output)
CLASS_NAMES = [
    'arecaceae', 'anadenanthera', 'arrabidaea', 'cecropia', 'chromolaena',
    'combretum', 'croton', 'dipteryx', 'eucalipto', 'hyptis',
    'inga', 'leucaena', 'moraceae', 'myrtaceae', 'poaceae',
    'pouteria', 'psidium', 'senna', 'siparuna', 'solanum',
    'vernonia', 'virola', 'urochloa'
]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['image']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Load and preprocess image
                img = load_img(filepath, target_size=(128, 128))
                img_array = img_to_array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)
                
                # Make prediction
                pred = model.predict(img_array)
                pred_class = CLASS_NAMES[np.argmax(pred)]
                confidence = float(np.max(pred)) * 100
                
                return render_template('prediction.html', 
                                    prediction=pred_class, 
                                    confidence=round(confidence, 2),
                                    image_path=filename)
            except Exception as e:
                flash(f'Error processing image: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('Allowed file types are .png, .jpg, .jpeg', 'error')
            return redirect(request.url)
    
    return render_template('prediction.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)