import os
from flask import Flask, render_template, request, redirect, url_for
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
        text = request.form["data"]
        file = request.files.get("img")   # <-- ĐÃ SỬA DÒNG NÀY
        filename = ""

        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_url = url_for('static', filename=f'uploads/{filename}', _external=True)
        else:
            img_url = ""
            filename = ""

        # Tạo link dẫn tới trang view
        view_link = url_for("view_content", text=text, img=filename, _external=True)

        # Tạo QR code chứa link đó
        qr = qrcode.make(view_link)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        qr_img_data = base64.b64encode(buf.getvalue()).decode("ascii")
        url = view_link

    return render_template("index.html", img_data=qr_img_data, url=url)

@app.route("/view")
def view_content():
    text = request.args.get("text", "")
    img = request.args.get("img", "")
    img_url = url_for('static', filename=f'uploads/{img}') if img else ""
    return render_template("view.html", text=text, img_url=img_url)

if __name__ == "__main__":
    app.run(debug=True)
