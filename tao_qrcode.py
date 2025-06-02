import qrcode

# Nội dung muốn mã hóa vào mã QR (có thể là text, URL, số điện thoại, v.v.)
data = "https://openai.com/"

# Tạo mã QR
img = qrcode.make(data)

# Lưu mã QR thành file ảnh
img.save("/Ảnh chụp màn hình 2025-05-24 171719.png")
