import os
import util

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from dotenv import dotenv_values

config = dotenv_values(".env")

UPLOAD_FOLDER = config["UPLOAD_FOLDER"]
ALLOWED_EXTENSIONS = {"wav", "mp3"}

app = Flask(__name__, template_folder="template")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def upload_files():
    return render_template("upload.html")


@app.route("/api", methods=["GET", "POST"])
@cross_origin()
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"status": False, "error": "No file part", "data": {}}), 400

        file = request.files["file"]

        if file.filename == "":
            return (
                jsonify({"status": False, "error": "No selected file", "data": {}}),
                400,
            )

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename, file_extension = os.path.splitext(filename)

            print(file_extension)
            if file_extension != ".wav":
                return (jsonify({"status": False, "error": "file extension error ", "data": {}}),400,)
            else:
                filename = util.generate_name(filename) + ".wav"

            fileLocation = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            if os.path.exists(fileLocation):
                # os.remove(fileLocation)
                print("The file delete success")
            else:
                print("The file does not exist")
            
        return jsonify({"status": True, "error": "success", "data": {}}), 200


if __name__ == "__main__":
    app.run(host=config["HOST"], port=int(config["PORT"]), debug=True)