import os
from django.conf import settings

try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction
from datetime import datetime, date, timedelta, time
from django.utils import timezone
import pytz


class Command(BaseCommand):
    help = "LOAD SOME SAMPLE INTO THE DATABASE"

    @transaction.atomic
    def handle(self, **options):
        from getenv import env
        from apps.blog.models import PostCategory, Post
        from apps.classes.models import YogaClass, PaymentPeriod
        from apps.courses.models import Course, TRAINING_COURSE
        from apps.accounts.models import User, Trainer
        from apps.rooms.models import Room
        # new class in the future
        data_hoang_anh = {
            'email': 'hoanganh1@gmail.com',
            'first_name': 'Anh',
            'last_name': 'Hoàng',
            'image': '/seeds/images/trainers/thay_hoang_anh.jpg'
        }
        user_hoang_anh = User(**data_hoang_anh)
        user_hoang_anh.set_password('truong77')
        user_hoang_anh.is_trainer = True
        user_hoang_anh.save()
        thay_hoang_anh = Trainer.objects.create(user=user_hoang_anh)
        thay_hoang_anh.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        thay_hoang_anh.experience = '''<ul><li>10 năm luyện tập Yoga.</li><li>8 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        thay_hoang_anh.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/all.jpg" /></p>'''
        thay_hoang_anh.save()
        thay_hoang_anh.user.certificates.create(
            name='Chứng chỉ trị liệu Yoga cấp bởi Indian Board of Alternative Medicines')
        thay_hoang_anh.user.certificates.create(
            name='Chứng nhận đã hoàn thành khóa đào tạo Huấn luyện viên Yoga của CLB Yoga Hương Tre')
        thay_hoang_anh.user.certificates.create(
            name='Bằng thạc sĩ khoa học Yoga của Đại Học Haridwar, Ấn Độ năm 2012')
        thay_hoang_anh.user.certificates.create(
            name='Huy chương vàng cuộc thi Master Yoga Science & Holistic Health')
        print("Create <TRAINING YOGA TRAINER> COURSES")
        training_yoga_trainer_course_data = {
            'name': 'Đào tạo huấn luyện viên',
            'description': '''Yoga Hương Tre mang đến những kiến thức từ cơ bản đến nâng cao, từ đạo đức, triết lý nghề nghiệp. Đạo tạo ra một người giáo viên Yoga chân chính, tâm huyết với nghề. Chứ không phải chỉ là một người huấn luyện viên chỉ biết đưa các bài học động tác cho học''',
            'content': '''<p>⭐️&nbsp;Đội ngũ&nbsp;Gi&aacute;o vi&ecirc;n đ&agrave;o tạo nhiều năm kinh nghiệm.</p>
                        <p>⭐️&nbsp;Gi&aacute;o tr&igrave;nh b&agrave;i bản khoa học, đảm bảo kỹ năng đứng lớp, chất lượng giảng dạy ưu ti&ecirc;n h&agrave;ng đầu.</p>

                        <p>⭐️&nbsp;Được nhận <strong>GIẤY CHỨNG NHẬN</strong> sau khi ho&agrave;n th&agrave;nh kh&oacute;a học từ Trung T&acirc;m Yoga Hương Tre.</p>

                        <p>⭐️&nbsp;Học vi&ecirc;n sau khi tốt nghiệp được giới thiệu việc l&agrave;m&nbsp;hoặc được&nbsp;giảng dạy tại Trung T&acirc;m Yoga Hương Tre.</p>

                        <p>⭐️ Hỗ trợ về kỹ thuật, định hướng, thương hiệu, x&acirc;y dựng ph&ograve;ng tập yoga nếu mở trung t&acirc;m ri&ecirc;ng.</p>

                        <p>⭐️ Hỗ trợ học vi&ecirc;n đủ điều kiện tham gia học, nhận chứng chỉ Li&ecirc;n Đo&agrave;n Yoga Việt Nam.</p>

                        <p><img alt="💥" src="https://static.xx.fbcdn.net/images/emoji.php/v9/t99/1.5/16/1f4a5.png" style="height:16px; width:16px" />&nbsp;Lựa chọn Nghề HLV YOGA bạn kh&ocirc;ng chỉ bảo vệ cho ch&iacute;nh sức khỏe của bản th&acirc;n bạn m&agrave; c&ograve;n cho ch&iacute;nh những người th&acirc;n v&agrave; cộng đồng xung quanh bạn.</p>

                        <p><img alt="💯" src="https://static.xx.fbcdn.net/images/emoji.php/v9/t4a/1.5/16/1f4af.png" style="height:16px; width:16px" />&nbsp;KH&Ocirc;NG NHỮNG MANG LẠI GI&Aacute; TRỊ VỀ SỨC KHỎE, NGHỀ HLV YOGA C&Ograve;N GI&Uacute;P BẠN C&Oacute; THU NHẬP CAO.</p>

                        <p><img alt="‼" src="https://static.xx.fbcdn.net/images/emoji.php/v9/tfe/1.5/16/203c.png" style="height:16px; width:16px" />&nbsp;Đ&acirc;y l&agrave; việc hiếm hoi m&agrave; bạn vừa c&oacute; thể kiếm tiền vừa c&oacute; thể gi&uacute;p người kh&aacute;c khỏe mạnh, sống t&iacute;ch cực hơn.</p>

                        <p><img alt="‼" src="https://static.xx.fbcdn.net/images/emoji.php/v9/tfe/1.5/16/203c.png" style="height:16px; width:16px" />&nbsp;Việc trở th&agrave;nh một gi&aacute;o vi&ecirc;n Yoga sẽ khiến bạn c&oacute; thể l&agrave;m việc ở khắp mọi nơi. V&igrave; sau khi học xong bạn sẽ được Bằng Yoga c&oacute; gi&aacute; trị to&agrave;n quốc</p>

                        <p>===================</p>

                        <p>Giấy chứng nhận ho&agrave;n th&agrave;nh kh&oacute;a học</p>

                        <p><img alt="" src="/media/seeds/2020/07/03/hlv/giay-chung-nhan-hlv-2.jpg" style="height:526px; width:870px" /></p>

                        <p>===================</p>

                        <p><img alt="⚡" src="https://static.xx.fbcdn.net/images/emoji.php/v9/te4/1.5/16/26a1.png" style="height:16px; width:16px" /><img alt="⚡" src="https://static.xx.fbcdn.net/images/emoji.php/v9/te4/1.5/16/26a1.png" style="height:16px; width:16px" /><img alt="⚡" src="https://static.xx.fbcdn.net/images/emoji.php/v9/te4/1.5/16/26a1.png" style="height:16px; width:16px" />&nbsp;NHANH TAY&nbsp;ĐĂNG K&Yacute; NGAY KH&Oacute;A HỌC HUẤN LUYỆN VI&Ecirc;N YOGA ĐỂ TRỞ TH&Agrave;NH HUẤN LUYỆN VI&Ecirc;N YOGA TRONG TƯƠNG LAI</p>

                        <p>===================</p>

                        <p>Kh&oacute;a Đ&agrave;o tạo&nbsp;Huấn luyện vi&ecirc;n&nbsp;Yoga l&agrave; kh&oacute;a học d&agrave;nh cho những ai muốn theo đuổi sự nghiệp giảng dạy&nbsp;Yoga chuy&ecirc;n nghiệp.&nbsp;</p>

                        <p>Kh&oacute;a học l&agrave; một khởi đầu vững chắc cho bạn tr&ecirc;n con đường tiếp theo trong sự nghiệp giảng dạy Yoga sau n&agrave;y.</p>

                        <p>Nghề gi&aacute;o vi&ecirc;n Yoga cho bạn một sức khỏe, một tinh thần thoải m&aacute;i. Biết lắng nghe, hiểu cơ thể m&igrave;nh đang muốn g&igrave;. Bạn sẽ lu&ocirc;n thấy một sức khỏe dồi d&agrave;o, một cơ thể dẻo dai ở mỗi người huấn luyện vi&ecirc;n Yoga. Người tập sẽ được hướng dẫn chi tiết, cẩn thận để từng động t&aacute;c lu&ocirc;n ch&iacute;nh x&aacute;c. Cơ thể từ người tập đến người hướng dẫn đều được cải thiện.</p>

                        <p>CLB Yoga Hương Tre mang đến những kiến thức từ cơ bản đến n&acirc;ng cao, từ đạo đức, triết l&yacute; nghề nghiệp. Đạo tạo ra một người gi&aacute;o vi&ecirc;n Yoga ch&acirc;n ch&iacute;nh, t&acirc;m huyết với nghề. Chứ kh&ocirc;ng phải chỉ l&agrave; một người huấn luyện vi&ecirc;n chỉ biết đưa c&aacute;c b&agrave;i học động t&aacute;c cho học vi&ecirc;n. Đ&atilde; c&oacute; rất nhiều học vi&ecirc;n t&igrave;m đến nơi đ&acirc;y tr&ecirc;n cả nước với mong muốn thay đổi bản th&acirc;n, muốn c&oacute; một nghề nghiệp mới v&agrave; đ&atilde; th&agrave;nh c&ocirc;ng.</p>

                        <p>Vậy th&igrave; c&ograve;n bạn, bạn đ&atilde; thực sự sẵn s&agrave;ng để trở th&agrave;nh một gi&aacute;o vi&ecirc;n Yoga hay chưa?</p>

                        <p><img alt="" src="/media/seeds/2020/07/03/hlv/trung-tam-dao-tao-huan-luyen-vien-yoga-uy-tin-2.jpg" style="height:716px; width:960px" /></p>

                        <h3>Một số h&igrave;nh ảnh về lớp huấn luyện vi&ecirc;n Yoga</h3>

                        <p><img alt="" src="/media/seeds/2020/07/03/hlv/phong-dao-tao-hlv.jpg" style="height:656px; width:875px" /></p>

                        <p><img alt="" src="/media/seeds/2020/07/03/hlv/1.jpg" style="height:656px; width:875px" /></p>

                        <h3>Trao chứng nhận ho&agrave;n th&agrave;nh kh&oacute;a học</h3>

                        <p><img alt="" src="/media/seeds/2020/07/03/hlv/le-trao-chung-nhan-2.jpg" style="height:720px; width:960px" /></p>

                        <p><img alt="" src="/media/seeds/2020/07/03/hlv/le-trao-chung-nhan-4.jpg" style="height:720px; width:960px" /></p>

                        <p><img alt="" src="/media/seeds/2020/07/03/hlv/trao-chung-nhan-1.jpg" style="height:686px; width:960px" /></p>
                        ''',
            'course_type': TRAINING_COURSE,
            'image': 'seeds/images/courses/huan_luyen_vien_yoga.jpg',
            'price_for_training_class': 20000000,
            'wages_per_lesson': 500000
        }
        training_yoga_trainer_course = Course(
            **training_yoga_trainer_course_data)
        training_yoga_trainer_course.save()

        room3_data = {
            "name": "Phòng 3",
            "location": "Lầu 3",
            "max_people": 15
        }
        room3 = Room.objects.create(**room3_data)

        # TRAINING CLASS
        _today = timezone.now()
        _start_of_week = _today - timedelta(days=_today.weekday())  # Monday
        t_21h = '21:00'
        _saturday = (_start_of_week + timedelta(days=5)).date()
        training_class_thay_hoang_anh = training_yoga_trainer_course.classes.create(
            name='Lớp đào tạo thầy Hoàng Anh 18h tối thứ 7 - KDT2',
            price_for_training_class=20000000,
            start_at=_saturday + timedelta(days=14),
            end_at=_saturday + timedelta(days=14 + 28*3),
            trainer=thay_hoang_anh,
        )
        t_18h = '18:00'
        for i in range(0, 12):
            count_date = 7 * i + 14
            training_class_thay_hoang_anh.lessons.create(**{
                "room_id": room3.pk,
                "date": _saturday + timedelta(days=count_date),
                "start_time": t_18h,
                "end_time": t_21h
            })

        period1 = training_class_thay_hoang_anh.payment_periods.create(**{
            'name': 'Đợt thanh toán 1',
            'amount': 12000000,
            'end_at': datetime.combine(_saturday + timedelta(days=14), time.max, _today.tzinfo)
        })
        period2 = training_class_thay_hoang_anh.payment_periods.create(**{
            'name': 'Đợt thanh toán 2',
            'amount': 10000000,
            'end_at': datetime.combine(_saturday + timedelta(days=(14 + 7*7)), time.max, _today.tzinfo)
        })
