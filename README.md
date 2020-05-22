# YOGA CENTER WEBSITE

## Cài đặt Python3
Mở file [runtime.txt](runtime.txt) để kiểm tra python version được sử dụng

Phiên bản đang được sử dụng hiện tại trong project là 3.8.0

```
python-3.8.0
```

Truy cập [Python.org](https://www.python.org/downloads/) để tải và cài đặt Python

Kiểm tra việc cài đặt thành công Python bằng cách mở terminal và gõ lệnh sau:

```
python --version
```
## Cài đặt Project

Điều đầu tiên cần làm là clone repository theo lệnh sau:

```sh
$ git clone git@github.com:giatruongtran27/yoga-center-website.git
$ cd yoga-center-website
```

Khởi tạo một virtual environment để cài đặt dependencies và kích hoạt:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Cài đặt dependencies bằng cách gõ lệnh sau:

```sh
(env)$ pip install -r requirements.txt
```
Lưu ý `(env)` trước dấu nhắc. Điều này chỉ ra rằng terminal session này hoạt động trong một môi trường ảo được thiết lập bởi `virtualenv2`

Sau khi cài đặt thành công, ta tiến hành chạy dự án bằng cách truy cập vào dự án và gõ lệnh:
```sh
(env)$ python manage.py runserver
```
Trang web được hiển thị tại `http://127.0.0.1:8000/`.
