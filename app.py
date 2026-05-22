<<<<<<< HEAD
import os
from flask import Flask, render_template, request, redirect, url_for, session
from PIL import Image
import torch
from torchvision.models import resnet18, ResNet18_Weights
import torchvision.transforms as transforms
from torch import nn

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Upload folder
app.config["UPLOAD_FOLDER"] = "static/uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Temporary user storage (in-memory)
users = {}

# ---------------- MODEL LOADING -----------------

def load_model(model_path, device):
    model = resnet18(weights=ResNet18_Weights.DEFAULT)
    model.fc = nn.Linear(in_features=512, out_features=4)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model

device = "cuda" if torch.cuda.is_available() else "cpu"
model = load_model("./model.pth", device)

# Transform
test_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

labels = {0: 'Blight', 1: 'Common_Rust', 2: 'Gray_Leaf_Spot', 3: 'Healthy'}
solutions = {
    'Blight': """
    • Apply fungicides like Mancozeb or Chlorothalonil  
    • Remove and destroy infected leaves  
    • Improve air circulation by proper spacing  
    • Use blight-resistant maize varieties  
    """,

    'Common_Rust': """
    • Use fungicides such as Azoxystrobin or Propiconazole  
    • Avoid overhead irrigation  
    • Plant rust-resistant hybrids  
    • Rotate crops to break the fungus lifecycle  
    """,

    'Gray_Leaf_Spot': """
    • Apply fungicides like Triazoles or Strobilurins  
    • Use crop rotation and proper field drainage  
    • Remove infected crop residue  
    • Improve sunlight penetration by proper spacing  
    """,

    'Healthy': """
    • The leaf is healthy!  
    • Continue regular monitoring  
    • Maintain proper soil nutrition  
    • Use preventive fungicide sprays if needed  
    """
}


def predict_image(img_path):
    image = Image.open(img_path).convert('RGB')
    img_tensor = test_transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img_tensor)
        _, predicted = torch.max(output, 1)

    return labels[predicted.item()]

# ---------------- LOGIN -----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("index"))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# ---------------- HOME -----------------

@app.route("/home", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        if "image" not in request.files:
            return render_template("index.html", error="No file uploaded")

        file = request.files["image"]
        
        if file.filename == "":
            return render_template("index.html", error="No file selected")

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        label = predict_image(filepath)
        solution=solutions[label]

        return render_template("index.html", filename=file.filename, label=label, solution=solution)

    return render_template("index.html")

# ---------------- LOGOUT -----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- SIGNUP -----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return render_template("signup.html", error="User already exists!")

        users[username] = password
        return redirect(url_for("login"))

    return render_template("signup.html")

# ---------------- RUN -----------------
@app.route("/")
def home_redirect():
    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug=True)
=======
import os
from flask import Flask, render_template, request, redirect, url_for, session
from PIL import Image
import torch
from torchvision.models import resnet18, ResNet18_Weights
import torchvision.transforms as transforms
from torch import nn

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Upload folder
app.config["UPLOAD_FOLDER"] = "static/uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Temporary user storage (in-memory)
users = {}

# ---------------- MODEL LOADING -----------------

def load_model(model_path, device):
    model = resnet18(weights=ResNet18_Weights.DEFAULT)
    model.fc = nn.Linear(in_features=512, out_features=4)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model

device = "cuda" if torch.cuda.is_available() else "cpu"
model = load_model("./model.pth", device)

# Transform
test_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

labels = {0: 'Blight', 1: 'Common_Rust', 2: 'Gray_Leaf_Spot', 3: 'Healthy'}
solutions = {
    'Blight': """
    • Apply fungicides like Mancozeb or Chlorothalonil  
    • Remove and destroy infected leaves  
    • Improve air circulation by proper spacing  
    • Use blight-resistant maize varieties  
    """,

    'Common_Rust': """
    • Use fungicides such as Azoxystrobin or Propiconazole  
    • Avoid overhead irrigation  
    • Plant rust-resistant hybrids  
    • Rotate crops to break the fungus lifecycle  
    """,

    'Gray_Leaf_Spot': """
    • Apply fungicides like Triazoles or Strobilurins  
    • Use crop rotation and proper field drainage  
    • Remove infected crop residue  
    • Improve sunlight penetration by proper spacing  
    """,

    'Healthy': """
    • The leaf is healthy!  
    • Continue regular monitoring  
    • Maintain proper soil nutrition  
    • Use preventive fungicide sprays if needed  
    """
}


def predict_image(img_path):
    image = Image.open(img_path).convert('RGB')
    img_tensor = test_transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img_tensor)
        _, predicted = torch.max(output, 1)

    return labels[predicted.item()]

# ---------------- LOGIN -----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("index"))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# ---------------- HOME -----------------

@app.route("/home", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        if "image" not in request.files:
            return render_template("index.html", error="No file uploaded")

        file = request.files["image"]
        
        if file.filename == "":
            return render_template("index.html", error="No file selected")

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        label = predict_image(filepath)
        solution=solutions[label]

        return render_template("index.html", filename=file.filename, label=label, solution=solution)

    return render_template("index.html")

# ---------------- LOGOUT -----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- SIGNUP -----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return render_template("signup.html", error="User already exists!")

        users[username] = password
        return redirect(url_for("login"))

    return render_template("signup.html")

# ---------------- RUN -----------------
@app.route("/")
def home_redirect():
    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> b11d31254ad0695daf27846b0b5281c00650e204
