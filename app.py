import os
from flask import Flask, render_template, request, url_for
import qrcode
import io
import base64
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_img_data = None
    url = ""
    if request.method == "POST":
        title = request.form.get("title", "")
        text = request.form.get("data", "")
        files = request.files.getlist("img")
        filenames = []

        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filenames.append(filename)

        img_param = ",".join(filenames)
        view_link = url_for("view_content", title=title, text=text, img=img_param, _external=True)

        qr = qrcode.make(view_link)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        qr_img_data = base64.b64encode(buf.getvalue()).decode("ascii")
        url = view_link

    return render_template("index.html", img_data=qr_img_data, url=url)

@app.route("/view")
def view_content():
    title = request.args.get("title", "")
    text = request.args.get("text", "")
    img_param = request.args.get("img", "")
    img_urls = []
    if img_param:
        for fname in img_param.split(","):
            if fname.strip():
                img_urls.append(url_for('static', filename=f'uploads/{fname}'))
    return render_template("view.html", text=text, img_urls=img_urls, title=title)

if __name__ == "__main__":
    app.run(debug=True)
