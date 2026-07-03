
import os
from flask import Flask, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Folder where uploaded images are saved (inside Flask's static folder
# so they can be served back to the browser).
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def learn():
    image_html = ""

    if request.method == "POST":
        # "image" must match the name="image" attribute on the <input>.
        file = request.files.get("image")
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            image_url = url_for("static", filename=f"uploads/{filename}")
            image_html = f'<img src="{image_url}" alt="uploaded image" width="300">'

    return f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Week 12 - Activity 4</title>
        </head>
        <body>
            <h1>Week 12 - Activity 4: Load and Show an Image</h1>
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="image" accept="image/*">
                <button type="submit">Upload</button>
            </form>
            {image_html}
        </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
