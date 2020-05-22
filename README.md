# YOGA CENTER WEBSITE

## Chuẩn bị: Cài đặt Python3, Pip và Virtualenv

### Cài đặt Python3
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

Điều đầu tiên cần làm là clone repository theo lệnh sau:

```sh
$ git clone git@github.com:giatruongtran27/yoga-center-website.git
$ cd yoga-center-website
```

Khởi tạo một virtual environment để cài đặt dependencies và kích hoạt:

```sh
$ virtualenv --no-site-packages env
$ source env/bin/activate
```

Cài đặt dependencies bằng cách gõ lệnh sau:

```sh
(env)$ pip install -r requirements.txt
```
Lưu ý `(env)` trước dấu nhắc để chỉ ra rằng terminal session này hoạt động trong một môi trường ảo được thiết lập bởi `virtualenv`

Sau khi cài đặt thành công, ta tiến hành chạy dự án bằng cách truy cập vào dự án và gõ lệnh:
```sh
(env)$ python manage.py runserver
```
Trang web được hiển thị tại `http://127.0.0.1:8000/`.
