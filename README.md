# YOGA CENTER WEBSITE
Website quản lý trung tâm tập Yoga

## Chuẩn bị: Cài đặt Python3, Pip và Virtualenv

### Cài đặt Python3
Mở file [runtime.txt](runtime.txt) để kiểm tra python version được sử dụng

Phiên bản đang được sử dụng hiện tại trong project là 3.8.0

```
python-3.8.0
```

Truy cập [Python.org](https://www.python.org/downloads/) để tải và cài đặt Python

Kiểm tra việc cài đặt thành công Python bằng cách mở terminal và gõ lệnh sau

```
python --version
```
### Cài đặt pip
Với phiên bản python hiện tại, bạn có thể bỏ qua bước này vì
```
Từ phiên bản python 3.4 trở đi, PIP đã được cài sẵn trong python
```
Kiểm tra pip đã được cài đặt thành công bằng cách gõ lệnh
```
pip --version
```
### Cài đặt Virtualenv
```
pip install virtualenv
```
Kiểm tra Virtualenv đã cài đặt thành công bằng cách gõ lệnh
```
virtualenv --version
```

## Cài đặt Project

### Bước 1: Clone repository theo lệnh sau

```sh
$ git clone git@github.com:giatruongtran27/yoga-center-website.git
```
hoặc
```sh
$ git clone https://github.com/giatruongtran27/yoga-center-website.git
```
Sau đó truy cập vào thư mục của project
```sh
$ cd yoga-center-website
```
### Bước 2: Khởi tạo một virtual environment để cài đặt dependencies

```sh
$ virtualenv --no-site-packages env
```
Kích hoạt virtualenv bằng 1 trong 2 lệnh sau
```
$ source env/bin/activate
```
hoặc
```
$ source env/Scripts/activate
```

### Bước 3: Cài đặt dependencies bằng cách gõ lệnh sau

```sh
(env)$ pip install -r requirements.txt
```
Lưu ý: `(env)` trước dấu nhắc để chỉ ra rằng terminal session này hoạt động trong một môi trường ảo được thiết lập bởi `virtualenv`

### Bước 4: Sau khi cài đặt thành công, tạo file `.env` bằng cách gõ lệnh
```
$ touch .env
```
Thiết lập một số thông số trong file `.env` (Có thể tạm bỏ qua nếu bạn chưa chuẩn bị đầy đủ để cài đặt)

- YOGA_CENTER_YOUTUBE_URL = "https://www.youtube.com/channel/UCKEKFt8623RUF-7Phxtnn-A" hoặc "your youtube url"
- YOGA_CENTER_FACEBOOK_URL = "https://www.facebook.com/CLB-Yoga-Huong-Tre-479934325379747/" hoặc "your facebook page url"

MAIL Settings
- EMAIL = 'your email'
- PASSWORD = 'your password'

DATABASE Settings
- DATABASE_NAME = 'your database name'
- DATABASE_USER = 'your user'
- DATABASE_PASSWORD = 'your password'
- DATABASE_HOST = 'your host'
- DATABASE_PORT = 'your port'

[STRIPE](https://testdriven.io/blog/django-stripe-tutorial/) Settings
- STRIPE_PUBLISHABLE_KEY = 'pk_test_0NmjgWZnyRpJJQZmOy3sz0Ml00vWX2eZfR'
- STRIPE_SECRET_KEY = 'sk_test_rFnSzD5bgmB3huVG4rDlw1Q700SwnBSCZl'

[TWILIO](https://www.twilio.com/) Settings
- TWILIO_ACCOUNT_SID = 'your Twilio Account SID'
- TWILIO_AUTH_TOKEN = 'your Twilio Auth Token'
- TWILIO_PHONE_NUMBER = 'your Phone Number'
- DEFAULT_TO_NUMBER = 'your DefaultToNumber'

[TAWK.TO](https://www.tawk.to/) Settings
- TAWK_TO_API_URL = 'your Tawk.to API'

[FACEBOOK COMMENT PLUGIN](https://developers.facebook.com/docs/plugins/comments/)
- FACEBOOK_PRIVACY_POLICY_URL = yogahuongtre.herokuapp.com

### Bước 5: Migrate database bằng lệnh
```sh
(env)$ python manage.py migrate
```
### Bước 6: Chạy lệnh để tạo dữ liệu mẫu
```sh
(env)$ python manage.py load_sample_data
```
### Bước 7: Chạy dự án bằng cách thực hiện lệnh
```sh
(env)$ python manage.py runserver
```
Trang web được hiển thị tại `http://127.0.0.1:8000/`.
```
