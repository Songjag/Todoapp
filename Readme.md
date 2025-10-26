# Todo - Elysia's Realm

Ứng dụng web Todo nhỏ viết bằng Flask, gồm giao diện đăng nhập/đăng ký và quản lý công việc.

## Tính năng
- Đăng ký / Đăng nhập (templates: `register.html`, `login.html`)(code=gpt đừng có chê)
- Tạo / liệt kê công việc theo người dùng và ngày
- Giao diện responsive, theme tối

## Yêu cầu
- Python 3.10+ (dự án dùng virtualenv `.venv` có thể không)
- Flask (và các thư viện khác nếu có; thêm vào `requirements.txt` nếu cần)

## Cài đặt nhanh (Linux)
1. Tạo và kích hoạt virtualenv:
   - python -m venv .venv
   - source .venv/bin/activate
2. Cài dependencies:
   - pip install -r requirements.txt
   (Nếu không có `requirements.txt` chỉ cần `pip install flask`)

## Chạy ứng dụng
- Trong virtualenv:
  - python3 server.py/python server.py
  hoặc:
  - export FLASK_APP=server.py
  - flask run

Ứng dụng mặc định chạy trên http://127.0.0.1:5000

## Cấu trúc dự án (chỉ mục chính)
- server.py — entrypoint Flask
- templates/ — chứa `login.html`, `register.html`, `index.html`, ...
- static/ — ảnh
- data.py — lớp xử lý người dùng / todo (API lưu ý)
- .venv/ — virtualenv (không commit)

## Ghi chú quan trọng
- Nếu gặp lỗi: `AssertionError: View function mapping is overwriting an existing endpoint function: login`  
  => Đảm bảo mỗi route có tên hàm (function name) khác nhau hoặc chỉ đăng ký route một lần. Ví dụ đổi tên hàm cho route `/` thành `home`.
- Nếu muốn lưu cả giờ phút giây khi tạo/lọc task:
  - Sử dụng: `datetime.now().strftime("%Y-%m-%d %H:%M:%S")`
- Form đăng nhập/đăng ký trong `templates/*` sử dụng `action="{{ url_for('login') }}"` / `url_for('register')` và hiển thị `get_flashed_messages()` để hiện thông báo.

## Tùy biến / Mở rộng
- Thêm `requirements.txt` với `flask` và các thư viện khác.
- Thêm xử lý session / bảo mật mật khẩu (bcrypt).
- Kết nối DB (SQLite / SQLAlchemy) để lưu người dùng và tasks.
## Cách đẩy lên VPS (Nginx + systemd + Gunicorn)

Ngắn gọn các bước triển khai an toàn cho ứng dụng Flask trên VPS (Ubuntu).

1) Chuẩn bị VPS
- Cập nhật và cài công cụ:
  sudo apt update && sudo apt upgrade -y  
  sudo apt install python3-venv python3-pip nginx git -y

2) Triển khai mã nguồn
- Trên VPS:
  - cd /home/ubuntu
  - git clone <repo> todoapp
  - cd todoapp
  - python3 -m venv .venv
  - source .venv/bin/activate
  - pip install -r requirements.txt

3) Chạy bằng Gunicorn (systemd)
- Tạo file systemd để chạy Gunicorn (ví dụ /etc/systemd/system/todoapp.service):

```ini
# /etc/systemd/system/todoapp.service
[Unit]
Description=TodoApp Gunicorn Service
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/todoapp
Environment="PATH=/home/ubuntu/todoapp/.venv/bin"
# If you use env vars, reference an EnvironmentFile
# EnvironmentFile=/home/ubuntu/todoapp/.env
ExecStart=/home/ubuntu/todoapp/.venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

- Lưu file, reload systemd và khởi động:
  sudo systemctl daemon-reload  
  sudo systemctl enable --now todoapp.service  
  sudo systemctl status todoapp.service

4) Cấu hình Nginx
- Tạo file /etc/nginx/sites-available/todoapp:

```nginx
# /etc/nginx/sites-available/todoapp
server {
    listen 80;
    server_name yourdomain.tld www.yourdomain.tld;

    location /static/ {
        alias /home/ubuntu/todoapp/static/;
    }

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8000;
    }

    access_log /var/log/nginx/todoapp.access.log;
    error_log  /var/log/nginx/todoapp.error.log;
}
```

- Kích hoạt site và kiểm tra Nginx:
  sudo ln -s /etc/nginx/sites-available/todoapp /etc/nginx/sites-enabled/  
  sudo nginx -t  
  sudo systemctl restart nginx

5) TLS (Let's Encrypt)
- Cài certbot cho Nginx:
  sudo apt install certbot python3-certbot-nginx -y  
  sudo certbot --nginx -d yourdomain.tld -d www.yourdomain.tld

6) DNS
- Tạo bản ghi A cho domain:
  - Type: A
  - Host / Name: @
  - Value: <IP_VPS>
  - TTL: default
- (Tùy chọn) Tạo CNAME cho www trỏ tới @

7) Firewall (ufw)
- Nếu dùng ufw:
  sudo ufw allow OpenSSH  
  sudo ufw allow 'Nginx Full'  
  sudo ufw enable

8) Biến môi trường và bảo mật
- Đặt SECRET_KEY, DB config, etc. trong file .env (không commit) và load trong systemd bằng EnvironmentFile=/home/ubuntu/todoapp/.env hoặc export trực tiếp trong service file.
- Đặt quyền đúng cho thư mục và logs (user trong systemd).

9) Kiểm tra và debug
- Xem logs:
  sudo journalctl -u todoapp.service -f  
  sudo tail -f /var/log/nginx/todoapp.error.log

Ghi chú
- Thay `app:app` trong ExecStart bằng module:app phù hợp (ví dụ nếu entrypoint là server.py với Flask app biến tên `app`, dùng `server:app`).
- Nếu muốn socket-based setup (nginx <-> systemd socket) có thể dùng Gunicorn socket config — đây là cấu hình đơn giản, dễ gỡ lỗi.
- Sau mỗi thay đổi file systemd/nginx: reload systemd/nginx và restart dịch vụ tương ứng.