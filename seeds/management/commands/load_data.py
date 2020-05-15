try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction
from faker import Faker
from getenv import env
from datetime import datetime, date, timedelta
from django.utils import timezone
import pytz
import random
import os
from django.conf import settings
from apps.rooms.models import Room
from apps.classes.models import (YogaClass)
from apps.courses.models import (Course, TRAINING_COURSE,
                                 PRACTICE_COURSE, BASIC_LEVEL, INTERMEDIATE_LEVEL, ADVANCED_LEVEL)
from apps.lessons.models import Lesson
from apps.accounts.models import User, Trainer, Trainee, Staff
from apps.card_types.models import (CardType, FOR_FULL_MONTH,
                                    FOR_SOME_LESSONS, FOR_TRIAL, FOR_TRAINING_COURSE)
from apps.cards.models import Card
from apps.roll_calls.models import RollCall
from services.card_invoice_service import CardInvoiceService
from services.roll_call_service import RollCallService
from apps.blog.models import PostCategory, Post
from apps.events.models import Event
from apps.faq.models import FAQ
from apps.gallery.models import Gallery, GalleryImage
from services.roll_call_service import RollCallService
from services.card_invoice_service import CardInvoiceService


class Command(BaseCommand):
    help = "LOAD SAMPLE DATA INTO THE DB"
    @transaction.atomic
    def handle(self, **options):
        today = timezone.now()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday

        ############# DAY IN CURRENT WEEK ###########
        monday = start_of_week.date()
        tuesday = (start_of_week + timedelta(days=1)).date()
        wednesday = (start_of_week + timedelta(days=2)).date()
        thursday = (start_of_week + timedelta(days=3)).date()
        friday = (start_of_week + timedelta(days=4)).date()
        saturday = (start_of_week + timedelta(days=5)).date()
        sunday = end_of_week.date()
        ############# =================== ###########

        default_range_time_for_practice_lesson = int(env(
            'DEFAULT_RANGE_TIME_MINUTES_OF_LESSON'))
        default_range_time_for_training_lesson = int(env(
            'DEFAULT_RANGE_TIME_MINUTES_OF_TRAINING_LESSON'))

        data_co_phuong = {
            'email': 'phuongnguyen1@gmail.com',
            'first_name': 'Phượng',
            'last_name': 'Nguyễn',
            'image': '/seeds/images/trainers/chi_phuong.jpg'
        }
        user_cp = User(**data_co_phuong)
        user_cp.set_password('truong77')
        user_cp.is_trainer = True
        user_cp.save()
        co_phuong = Trainer.objects.create(user=user_cp)
        co_phuong.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        co_phuong.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        co_phuong.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_phuong_anh_tan.jpg" /></p>'''
        co_phuong.save()
        co_phuong.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga Quốc tế')
        co_phuong.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')
        co_phuong.certificates.create(
            name='Chứng chỉ trị liệu Yoga cấp bởi Indian Board of Alternative Medicines')
        co_phuong.certificates.create(
            name='Huy chương vàng cuộc thi Master Yoga Science & Holistic Health')
        co_phuong.certificates.create(
            name='Bằng thạc sĩ khoa học Yoga của Đại Học Haridwar, Ấn Độ năm 2012')

        data_co_man = {
            'email': 'mantue1@gmail.com',
            'first_name': 'Mẫn',
            'last_name': 'Tuệ',
            'image': '/seeds/images/trainers/chi_man.jpg'
        }
        user_co_man = User(**data_co_man)
        user_co_man.set_password('truong77')
        user_co_man.is_trainer = True
        user_co_man.save()
        co_man = Trainer.objects.create(user=user_co_man)
        co_man.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        co_man.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        co_man.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_man.jpg" /></p>'''
        co_man.save()
        co_man.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')
        co_man.certificates.create(
            name='Chứng chỉ trị liệu Yoga cấp bởi Indian Board of Alternative Medicines')
        co_man.certificates.create(
            name='Huy chương vàng cuộc thi Master Yoga Science & Holistic Health')
        co_man.certificates.create(
            name='Bằng thạc sĩ khoa học Yoga của Đại Học Haridwar, Ấn Độ năm 2012')

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
        thay_hoang_anh.certificates.create(
            name='Chứng chỉ trị liệu Yoga cấp bởi Indian Board of Alternative Medicines')
        thay_hoang_anh.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')
        thay_hoang_anh.certificates.create(
            name='Bằng thạc sĩ khoa học Yoga của Đại Học Haridwar, Ấn Độ năm 2012')
        thay_hoang_anh.certificates.create(
            name='Huy chương vàng cuộc thi Master Yoga Science & Holistic Health')

        data_hai_tan = {
            'email': 'duonghaitan1@gmail.com',
            'first_name': 'Tân',
            'last_name': 'Dương',
            'image': '/seeds/images/trainers/anh_tan.jpg'
        }
        user_tan = User(**data_hai_tan)
        user_tan.set_password('truong77')
        user_tan.is_trainer = True
        user_tan.save()
        thay_tan = Trainer.objects.create(user=user_tan)
        thay_tan.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        thay_tan.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        thay_tan.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_phuong_anh_tan.jpg" /></p>'''
        thay_tan.save()
        thay_tan.certificates.create(
            name='Bằng thạc sĩ khoa học Yoga của Đại Học Haridwar, Ấn Độ năm 2012')
        thay_tan.certificates.create(
            name='Chứng chỉ trị liệu Yoga cấp bởi Indian Board of Alternative Medicines')
        thay_tan.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')
        thay_tan.certificates.create(
            name='Huy chương vàng cuộc thi Master Yoga Science & Holistic Health')

        data_thay_tien = {
            'email': 'thanhtien1@gmail.com',
            'first_name': 'Tiến',
            'last_name': 'Thanh',
            'image': '/seeds/images/trainers/anh_tien.jpg'
        }
        user_thay_tien = User(**data_thay_tien)
        user_thay_tien.set_password('truong77')
        user_thay_tien.is_trainer = True
        user_thay_tien.save()
        thay_tien = Trainer.objects.create(user=user_thay_tien)
        thay_tien.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        thay_tien.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        thay_tien.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/all.jpg" /></p>'''
        thay_tien.save()
        thay_tien.certificates.create(
            name='Chứng chỉ trị liệu Yoga cấp bởi Indian Board of Alternative Medicines')
        thay_tien.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')
        thay_tien.certificates.create(
            name='Huy chương vàng cuộc thi Master Yoga Science & Holistic Health')
        thay_tien.certificates.create(
            name='Bằng thạc sĩ khoa học Yoga của Đại Học Haridwar, Ấn Độ năm 2012')

        data_kieu_linh = {
            'email': 'kieulinh1@gmail.com',
            'first_name': 'Linh',
            'last_name': 'Kiều',
            'image': '/seeds/images/trainers/em_linh.jpg'
        }
        user_kieu_linh = User(**data_kieu_linh)
        user_kieu_linh.set_password('truong77')
        user_kieu_linh.is_trainer = True
        user_kieu_linh.save()
        co_linh = Trainer.objects.create(user=user_kieu_linh)
        co_linh.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        co_linh.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        co_linh.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_ly.jpg" /></p>'''
        co_linh.save()
        co_linh.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')
        co_linh.certificates.create(
            name='Bằng thạc sĩ khoa học Yoga của Đại Học Haridwar, Ấn Độ năm 2012')
        co_linh.certificates.create(
            name='Chứng chỉ trị liệu Yoga cấp bởi Indian Board of Alternative Medicines')
        co_linh.certificates.create(
            name='Huy chương vàng cuộc thi Master Yoga Science & Holistic Health')

        data_co_hang_nga = {
            'email': 'hangnga1@gmail.com',
            'first_name': 'Nga',
            'last_name': 'Hằng',
            'image': '/seeds/images/trainers/co_hang_nga.jpg'
        }
        user_hang_nga = User(**data_co_hang_nga)
        user_hang_nga.set_password('truong77')
        user_hang_nga.is_trainer = True
        user_hang_nga.save()
        co_hang_nga = Trainer.objects.create(user=user_hang_nga)
        co_hang_nga.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        co_hang_nga.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        co_hang_nga.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_ly.jpg" /></p>'''
        co_hang_nga.save()
        co_hang_nga.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')

        data_co_ngung = {
            'email': 'ngungnguyen1@gmail.com',
            'first_name': 'Ngừng',
            'last_name': 'Nguyễn',
            'image': '/seeds/images/trainers/co_ngung.jpg'
        }
        user_co_ngung = User(**data_co_ngung)
        user_co_ngung.set_password('truong77')
        user_co_ngung.is_trainer = True
        user_co_ngung.save()
        co_ngung = Trainer.objects.create(user=user_co_ngung)
        co_ngung.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        co_ngung.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        co_ngung.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_ly.jpg" /></p>'''
        co_ngung.save()
        co_ngung.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')

        data_co_nhu = {
            'email': 'nhunguyen1@gmail.com',
            'first_name': 'Như',
            'last_name': 'Huỳnh',
            'image': '/seeds/images/trainers/co_nhu.jpg'
        }
        user_co_nhu = User(**data_co_nhu)
        user_co_nhu.set_password('truong77')
        user_co_nhu.is_trainer = True
        user_co_nhu.save()
        co_nhu = Trainer.objects.create(user=user_co_nhu)
        co_nhu.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        co_nhu.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        co_nhu.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_ly.jpg" /></p>'''
        co_nhu.save()
        co_nhu.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')

        data_co_kieu = {
            'email': 'kieutran1@gmail.com',
            'first_name': 'Kiều',
            'last_name': 'Trần',
            'image': '/seeds/images/trainers/co_kieu.jpg'
        }
        user_co_kieu = User(**data_co_kieu)
        user_co_kieu.set_password('truong77')
        user_co_kieu.is_trainer = True
        user_co_kieu.save()
        co_kieu = Trainer.objects.create(user=user_co_kieu)
        co_kieu.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        co_kieu.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        co_kieu.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_ly.jpg" /></p>'''
        co_kieu.save()
        co_kieu.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')

        data_co_xuan = {
            'email': 'xuannguyen1@gmail.com',
            'first_name': 'Xuân',
            'last_name': 'Nguyễn',
            'image': '/seeds/images/trainers/co_xuan.jpg'
        }
        user_co_xuan = User(**data_co_xuan)
        user_co_xuan.set_password('truong77')
        user_co_xuan.is_trainer = True
        user_co_xuan.save()
        co_xuan = Trainer.objects.create(user=user_co_xuan)
        co_xuan.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        co_xuan.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        co_xuan.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_ly.jpg" /></p>'''
        co_xuan.save()
        co_xuan.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')

        data_co_thuy = {
            'email': 'thuynguyen1@gmail.com',
            'first_name': 'Thùy',
            'last_name': 'Nguyễn',
            'image': '/seeds/images/trainers/co_thuy.jpg'
        }
        user_co_thuy = User(**data_co_thuy)
        user_co_thuy.set_password('truong77')
        user_co_thuy.is_trainer = True
        user_co_thuy.save()
        co_thuy = Trainer.objects.create(user=user_co_thuy)
        co_thuy.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        co_thuy.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        co_thuy.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_ly.jpg" /></p>'''
        co_thuy.save()
        co_thuy.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')

        data_co_tra_my = {
            'email': 'tramy1@gmail.com',
            'first_name': 'My',
            'last_name': 'Trà',
            'image': '/seeds/images/trainers/co_tra_my.jpg'
        }
        user_co_tra_my = User(**data_co_tra_my)
        user_co_tra_my.set_password('truong77')
        user_co_tra_my.is_trainer = True
        user_co_tra_my.save()
        co_tra_my = Trainer.objects.create(user=user_co_tra_my)
        co_tra_my.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        co_tra_my.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        co_tra_my.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_ly.jpg" /></p>'''
        co_tra_my.save()
        co_tra_my.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')

        data_co_nhan = {
            'email': 'nhannguyen1@gmail.com',
            'first_name': 'Nhàn',
            'last_name': 'Nguyễn',
            'image': '/seeds/images/trainers/co_nhan.jpg'
        }
        user_co_nhan = User(**data_co_nhan)
        user_co_nhan.set_password('truong77')
        user_co_nhan.is_trainer = True
        user_co_nhan.save()
        co_nhan = Trainer.objects.create(user=user_co_nhan)
        co_nhan.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        co_nhan.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        co_nhan.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_ly.jpg" /></p>'''
        co_nhan.save()
        co_nhan.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')

        data_co_quyen = {
            'email': 'quyennguyen1@gmail.com',
            'first_name': 'Quyên',
            'last_name': 'Nguyễn',
            'image': '/seeds/images/trainers/co_quyen.jpg'
        }
        user_co_quyen = User(**data_co_quyen)
        user_co_quyen.set_password('truong77')
        user_co_quyen.is_trainer = True
        user_co_quyen.save()
        co_quyen = Trainer.objects.create(user=user_co_quyen)
        co_quyen.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        co_quyen.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        co_quyen.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_ly.jpg" /></p>'''
        co_quyen.save()
        co_quyen.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')

        data_thay_thien = {
            'email': 'thiennguyen1@gmail.com',
            'first_name': 'Thiên',
            'last_name': 'Nguyễn',
            'image': '/seeds/images/trainers/thay_thien.jpg'
        }
        user_thay_thien = User(**data_thay_thien)
        user_thay_thien.set_password('truong77')
        user_thay_thien.is_trainer = True
        user_thay_thien.save()
        thay_thien = Trainer.objects.create(user=user_thay_thien)
        thay_thien.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        thay_thien.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        thay_thien.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_ly.jpg" /></p>'''
        thay_thien.save()
        thay_thien.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')

        data_co_vo_hanh = {
            'email': 'hanhvo1@gmail.com',
            'first_name': 'Hạnh',
            'last_name': 'Võ',
            'image': '/seeds/images/trainers/co_vo_hanh.jpg'
        }
        user_co_vo_hanh = User(**data_co_vo_hanh)
        user_co_vo_hanh.set_password('truong77')
        user_co_vo_hanh.is_trainer = True
        user_co_vo_hanh.save()
        co_vo_hanh = Trainer.objects.create(user=user_co_vo_hanh)
        co_vo_hanh.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        co_vo_hanh.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        co_vo_hanh.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_ly.jpg" /></p>'''
        co_vo_hanh.save()
        co_vo_hanh.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')

        data_co_hong = {
            'email': 'hongnguyen1@gmail.com',
            'first_name': 'Hồng',
            'last_name': 'Nguyễn',
            'image': '/seeds/images/trainers/co_hong.jpg'
        }
        user_co_hong = User(**data_co_hong)
        user_co_hong.set_password('truong77')
        user_co_hong.is_trainer = True
        user_co_hong.save()
        co_hong = Trainer.objects.create(user=user_co_hong)
        co_hong.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        co_hong.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        co_hong.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_ly.jpg" /></p>'''
        co_hong.save()
        co_hong.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')

        print("Create CARD TYPES")
        print("Create <FOR FULL MONTH> CARD TYPE")
        data_for_full_month = {
            'name': 'học theo tháng',
            'description': 'Áp dụng cho học viên muốn học tất cả các buổi trong tháng',
            'form_of_using': FOR_FULL_MONTH
        }
        full_month_card_type = CardType(**data_for_full_month)
        full_month_card_type.save()

        print("Create <FOR SOME LESSONS> CARD TYPE")
        data_for_some_lessons = {
            'name': 'học theo buổi',
            'description': 'Áp dụng cho học viên muốn học theo buổi với số buổi đăng kí trong một khoảng thời gian xác định.',
            'form_of_using': FOR_SOME_LESSONS
        }
        some_lessons_card_type = CardType(
            **data_for_some_lessons)
        some_lessons_card_type.save()
        print("Create <FOR TRIAL> CARD TYPE")
        data_for_trial = {
            'name': 'học thử',
            'description': 'Áp dụng cho học viên muốn học thử',
            'form_of_using': FOR_TRIAL,
            'multiplier': env('DEFAULT_MULTIPLIER_FOR_TRIAL')
        }

        trial_card_type = CardType(
            **data_for_trial)
        trial_card_type.save()
        print("Create <FOR TRAINING COURSE> CARD TYPE")
        data_for_training_course = {
            'name': 'học theo khóa đào tạo',
            'description': 'Áp dụng cho học viên học khóa học đào tạo',
            'form_of_using': FOR_TRAINING_COURSE
        }

        training_course_card_type = CardType(
            **data_for_training_course)
        training_course_card_type.save()

        print("==============CREATE COURSES==============")
        print("Create <YOGA BASIC LEVEL> COURSE")
        basic_yoga_course_data = {
            'name': 'Yoga cơ bản',
            'description': '''Hiểu cách hoạt động của Hơi thở, cách thức vận hành các tư thế an toàn và bảo toàn năng lượng. Lần đầu tiên bạn nhập môn Yoga thì đây là lớp tối ưu để bạn lựa chọn.''',
            'level': BASIC_LEVEL,
            'content': '''<h3>Nhập m&ocirc;n Yoga:</h3><p>Khi bạn tham gia v&agrave;o&nbsp;<strong>lớp Yoga căn bản</strong>, bạn sẽ được t&igrave;m hiểu những kh&aacute;i niệm cơ bản v&agrave; c&ocirc; đọng nhất về: Lịch sử Yoga, trường ph&aacute;i của Yoga, triết l&yacute; trong Yoga. Hiểu c&aacute;ch hoạt động của Hơi thở, c&aacute;ch thức vận h&agrave;nh c&aacute;c tư thế an to&agrave;n v&agrave; bảo to&agrave;n năng lượng. Lần đầu ti&ecirc;n bạn nhập m&ocirc;n Yoga th&igrave; đ&acirc;y l&agrave; lớp tối ưu để bạn lựa chọn, nếu bạn l&agrave; người đ&atilde; học Yoga rồi th&igrave; cũng l&agrave; dịp để bạn tiếp cận một trường ph&aacute;i Yoga mới, một chế độ tập luyện mới rồi sau đ&oacute; bạn sẽ chọn lớp ph&ugrave; hợp với thực trạng sức khỏe v&agrave; mong muốn của bạn.</p><h3>Nội dung tiếp cận:</h3><ol><li>Gi&uacute;p bạn x&aacute;c định r&otilde; mục ti&ecirc;u đến lớp, x&aacute;c định lớp học ph&ugrave; hợp với t&igrave;nh trạng sức khỏe, mục đ&iacute;ch &nbsp;nhu cầu của bạn.</li><li>Ph&acirc;n biệt lớp Yoga căn bản, Yoga trung cấp, Yoga n&acirc;ng cao.</li><li>L&agrave;m r&otilde;: Hatha Yoga, Astanga Yoga, Vinyasa Yoga.</li><li>Nguy&ecirc;n tắc tập luyện Yoga cần phải tu&acirc;n thủ.</li><li>Những ch&uacute; &yacute; trong tập luyện để đạt hiệu quả cao v&agrave; hạn chế chứng thương.</li><li>C&aacute;ch h&iacute;t thở đ&uacute;ng v&agrave; nguy&ecirc;n l&yacute; vận h&agrave;nh hơi thở đ&uacute;ng.</li><li>C&aacute;ch vận h&agrave;nh c&aacute;c Asana (tư thế Yoga)</li><li>Học c&aacute;ch thư gi&atilde;n v&agrave; nghĩ ngơi trong tập luyện, ứng dụng v&agrave;o c&ocirc;ng việc v&agrave; đời sống.</li><li>Được tư vấn chế độ dinh dưỡng hợp l&yacute;.</li><li>Tiếp cận những triết l&yacute; Yoga để &aacute;p dụng v&agrave;o cuộc sống tốt đẹp hơn.</li><li>Tiếp cận v&agrave; thực h&agrave;nh c&aacute;c tư thế Yoga căn bản, nhẹ nh&agrave;ng theo mức độ tăng dần để cơ thể th&iacute;ch nghi.</li></ol><h3>Lợi &iacute;ch cơ bản của tập Yoga:</h3><ol><li>Học c&aacute;ch nghỉ ngơi để xoa dịu thần kinh v&agrave; c&acirc;n n&atilde;o.</li><li>Tĩnh tọa để tập trung &yacute; ch&iacute;.</li><li>Điều tức để tẩy uế th&acirc;n thể, khu trục c&aacute;c chất cặn b&atilde;.</li><li>Điều kh&iacute; để kiểm so&aacute;t hơi thở.</li><li>Điều th&acirc;n: kiểm so&aacute;t th&acirc;n thể.</li></ol><p>Ngo&agrave;i ra, khi vận h&agrave;nh đ&uacute;ng, Yoga t&aacute;c đ&ocirc;ng l&ecirc;n c&aacute;c b&iacute; huyệt l&agrave;m mạnh c&aacute;c mạch m&aacute;u. Yoga c&ograve;n t&aacute;c động đến c&aacute;c hệ v&agrave; mở lối v&agrave;o t&acirc;m linh.</p><h3>Những ch&uacute; &yacute; trong tập luyện:</h3><ol><li>Tập tr&ecirc;n nền phẳng để giữ cho cột sống thẳng.</li><li>Ph&ograve;ng tập y&ecirc;n tĩnh, tho&aacute;ng m&aacute;t (thi&ecirc;n nhi&ecirc;n c&agrave;ng tốt), hạn chế gi&oacute; l&ugrave;a.</li><li>N&ecirc;n c&oacute; một tấm thảm ri&ecirc;ng v&agrave; khăn để tăng khả năng tập trung.</li><li>Kh&ocirc;ng ăn no trước giờ tập (ăn no &iacute;t nhất l&agrave; 3 tiếng), v&agrave; kh&ocirc;ng ăn liền sau sau khi tập (ăn uống b&igrave;nh thường sau 15 ph&uacute;t)</li><li>N&ecirc;n uống nước trước khi tập Yoga để cơ thể dẽo dai, hạn chế uống nhiều nước trong l&uacute;c tập.</li><li>Tắm sau khi tập &iacute;t nhất l&agrave; 30 ph&uacute;t.</li><li>Quần &aacute;o phải c&oacute; độ co gi&atilde;n v&agrave; thấm h&uacute;t mồ h&ocirc;i, gọn g&agrave;ng để kh&ocirc;ng l&agrave;m vướng l&uacute;c tập.</li><li>Phụ n&ecirc;n tập nhẹ hoặc nghĩ &iacute;t ng&agrave;y trong chu k&igrave; kinh nguyệt.</li><li>Một số trường hợp như: Huyết &aacute;p, tim mạch, cột sống,&hellip;.cần th&ocirc;ng b&aacute;o kĩ c&agrave;ng với nh&acirc;n vi&ecirc;n tư vấn hoặc người hướng dẫn để c&oacute; những lưu &yacute; ph&ugrave; hợp.</li><li>Phải đặt mục ti&ecirc;u tập luyện ph&ugrave; hợp với t&igrave;nh trạng sức khỏe, nhu cầu để duy tr&igrave; v&agrave; đặt kỉ luật tập luyện cho bản th&acirc;n.</li><li>Phải tập luyện với sự cảm nhận v&agrave; duy tr&igrave; &iacute;t nhất 3 th&aacute;ng mới c&oacute; kết quả.</li><li>Trong qu&aacute; tr&igrave;nh tập phải tập trung tư tưởng, &nbsp;giờ n&agrave;o việc đ&oacute;, hướng v&agrave;o cơ thể m&igrave;nh để quan s&aacute;t v&agrave; cảm nhận.</li><li>H&iacute;t v&agrave;o v&agrave; thở ra bằng mũi (những trường hợp cụ thể th&igrave; gi&aacute;o vi&ecirc;n sẽ nhắc nhở)</li><li>Khi giữ thế trong Yoga phải h&iacute;t thở thật chậm để d&ugrave;ng &yacute; vận kh&iacute;.</li><li>Hảy để tinh thần yoga sống kh&ocirc;ng chỉ tr&ecirc;n chiếu tập m&agrave; trong cả cuộc sống h&agrave;ng ng&agrave;y.</li></ol><p><a href="http://yogahuongtre.com/demo/wp-content/uploads/2015/02/770.jpg" title=""><img alt="Hình ảnh yoga căn bản tại cơ sở 1: 142 đường A4, Phường 12, Q.Tân Bình, HCM" src="http://yogahuongtre.com/wp-content/uploads/2015/02/770.jpg" style="height:463px; width:824px" /></a></p>''',
            'image': 'seeds/images/courses/yoga_co_ban.jpg',
            'price_per_lesson': 50000,
            'price_per_month': 600000,
        }
        basic_yoga_course = Course.objects.create(**basic_yoga_course_data)

        basic_yoga_course.card_types.add(
            full_month_card_type,
            some_lessons_card_type,
            trial_card_type
        )
        # Add Lectures
        self.__add_lectures(basic_yoga_course)

        print("Create <INTERMEDIATE YOGA > COURSE")
        intermediate_yoga_course_data = {
            'name': 'Yoga trung cấp',
            'description': '''Học viên đã trãi qua lớp yoga căn bản. Với sự kiểm soát cao về cơ thể, cơ thể trở nên cân đối, mềm dẽo, các khớp gần như đã mở hoàn toàn, phản xạ trở nên nhanh nhẹn, linh hoạt.''',
            'level': INTERMEDIATE_LEVEL,
            'image': 'seeds/images/courses/yoga-trung-cap.jpg',
            'price_per_lesson': 50000,
            'price_per_month': 600000,
        }
        intermediate_yoga_course = Course.objects.create(
            **intermediate_yoga_course_data)

        intermediate_yoga_course.card_types.add(
            full_month_card_type,
            some_lessons_card_type,
            trial_card_type
        )

        print("Create <ADVANCED YOGA > COURSE")
        advanced_yoga_course_data = {
            'name': 'Yoga nâng cao',
            'description': '''Học viên đã trãi qua lớp yoga căn bản, trung cấp. Với sự kiểm soát cao về cơ thể, cơ thể trở nên cân đối, mềm dẽo, các khớp gần như đã mở hoàn toàn, phản xạ trở nên nhanh nhẹn, linh hoạt.''',
            'level': ADVANCED_LEVEL,
            'image': 'seeds/images/courses/yoga_nang_cao.jpg',
            'price_per_lesson': 50000,
            'price_per_month': 600000,
        }
        advanced_yoga_course = Course.objects.create(
            **advanced_yoga_course_data)

        advanced_yoga_course.card_types.add(
            full_month_card_type,
            some_lessons_card_type,
            trial_card_type
        )

        print("Create <YOGA DANCE> COURSES")
        yoga_dance_course_data = {
            'name': 'Yoga Dance',
            'description': '''Yoga Dance là một khái niệm mới, một sự kết hợp tinh tế giữa sự nhẹ nhàng, thanh thoát trong các động tác Yoga truyền thống với các điệu nhảy uyển chuyển, quyến rũ cùng với âm nhạc cuốn hút.''',
            'image': 'seeds/images/courses/yoga_dance.png',
            'price_per_lesson': 50000,
            'price_per_month': 600000,
        }
        yoga_dance_course = Course(**yoga_dance_course_data)
        yoga_dance_course.save()

        print("Create <PRENATAL YOGA> COURSES")
        prenatal_yoga_course_data = {
            'name': 'Yoga cho bà bầu',
            'description': '''Là loại hình đặc biệt dành riêng cho các bà bầu hoặc phụ nữ chuẩn bị mang thai,... Với các động tác và kỹ năng thở tập trung vào phần xương chậu, chân và lưng dưới giúp hỗ trợ nâng đỡ phần bụng ngày một to ra''',
            'image': 'seeds/images/courses/yoga_bau.jpg',
            'price_per_lesson': 50000,
            'price_per_month': 600000,
        }
        prenatal_yoga_course = Course(**prenatal_yoga_course_data)
        prenatal_yoga_course.save()

        print("Create <TRAINING YOGA TRAINER> COURSES")
        training_yoga_trainer_course_data = {
            'name': 'Đào tạo huấn luyện viên',
            'description': '''Khóa học giúp đào tạo học viên trở thành một Huấn luyện viên Yoga.''',
            'course_type': TRAINING_COURSE,
            'image': 'seeds/images/courses/huan_luyen_vien_yoga.jpg',
            'price_for_training_class': 10000000,
        }
        training_yoga_trainer_course = Course(
            **training_yoga_trainer_course_data)
        training_yoga_trainer_course.save()

        training_yoga_trainer_course.card_types.add(
            training_course_card_type
        )

        print("Create <YOGA KID> COURSES")
        yoga_kid_course_data = {
            'name': 'Yoga Kid',
            'description': '''Yoga dành riêng cho trẻ nhỏ. Giúp trẻ tiếp cận Yoga một cách phù hợp thông qua hít thở và tập luyện, nâng cao sự dẻo dai và tập trung ở trẻ,...''',
            'course_type': PRACTICE_COURSE,
            'image': 'seeds/images/courses/yogakid.jpg',
            'price_per_lesson': 50000,
            'price_per_month': 600000,
        }
        yoga_kid_course = Course(
            **yoga_kid_course_data)
        yoga_kid_course.save()
        print("==============CREATE ROOMS==============")
        room1_data = {
            "name": "Phòng 1",
            "location": "Lầu 1",
            "max_people": 15
        }
        room1 = Room.objects.create(**room1_data)
        room2_data = {
            "name": "Phòng 2",
            "location": "Lầu 2",
            "max_people": 15
        }
        room2 = Room.objects.create(**room2_data)
        room3_data = {
            "name": "Phòng 3",
            "location": "Lầu 3",
            "max_people": 15
        }
        room3 = Room.objects.create(**room3_data)
        room4_data = {
            "name": "Phòng 4",
            "location": "Lầu 3",
            "max_people": 15
        }
        room4 = Room.objects.create(**room4_data)

        print("==============CREATE CLASSES==============")
        number_of_weeks = int(env('NUMBER_OF_WEEKS_TO_CREATE_LESSON'))
        basic_yoga_class_co_man_5h30_t246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Mận 5h30 sáng 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_man,
        )
        t_5h_30 = '05:30'
        t_6h_30 = (datetime.strptime(t_5h_30, '%H:%M') + timedelta(
            minutes=default_range_time_for_practice_lesson)).strftime("%H:%M")
        arr_lessons_basic_yoga_class_co_man_5h30_246 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_man_5h30_t246.lessons.create(**{
                "room_id": room1.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_5h_30,
                "end_time": t_6h_30
            })
            arr_lessons_basic_yoga_class_co_man_5h30_246.append(l1)
            l2 = basic_yoga_class_co_man_5h30_t246.lessons.create(**{
                "room_id": room1.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_5h_30,
                "end_time": t_6h_30
            })
            arr_lessons_basic_yoga_class_co_man_5h30_246.append(l2)
            l3 = basic_yoga_class_co_man_5h30_t246.lessons.create(**{
                "room_id": room1.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_5h_30,
                "end_time": t_6h_30
            })
            arr_lessons_basic_yoga_class_co_man_5h30_246.append(l3)
        # add-trainees
        self.__enroll('Dung', 'Lê Thị Hoàng', 'lethihoangdung1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:10])
        self.__enroll('Thùy', 'Ngô Bích', 'ngobichthuy1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:12])
        self.__enroll('Oanh', 'Đinh Thị Hoàng', 'dinhthihoangoanh1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:18])
        self.__enroll('Giang', 'Mai Thị Cẩm', 'maithicamgiang1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:24])
        self.__enroll('Trinh', 'Nguyễn Thị Diễm', 'nguyenthidiemtrinh1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:36])
        self.__enroll('Vi', 'Đinh Thị Tường', 'dinhthituongvi1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:18])
        self.__enroll('Hàng', 'Phạm Thị', 'phamthihang1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:18])
        self.__enroll('Hoàng', 'Nguyễn Thị Mỹ', 'nguyenthimyhoang1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:24])
        self.__enroll('Vi', 'Lê Tường', 'letuongvi1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:18])
        self.__enroll('Phượng', 'Nguyễn Thị Kim', 'nguyenthikimphuong1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:24])
        self.__enroll('Lý', 'Nguyễn Thị', 'nguyenthily1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:36])
        # end add-trainees
        basic_yoga_class_co_hang_nga_5h30_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Hằng Nga 5h30 sáng 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_hang_nga,
        )
        arr_lessons_basic_yoga_class_co_hang_nga_5h30_246 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_hang_nga_5h30_246.lessons.create(**{
                "room_id": room2.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_5h_30,
                "end_time": t_6h_30
            })
            arr_lessons_basic_yoga_class_co_hang_nga_5h30_246.append(l1)
            l2 = basic_yoga_class_co_hang_nga_5h30_246.lessons.create(**{
                "room_id": room2.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_5h_30,
                "end_time": t_6h_30
            })
            arr_lessons_basic_yoga_class_co_hang_nga_5h30_246.append(l2)
            l3 = basic_yoga_class_co_hang_nga_5h30_246.lessons.create(**{
                "room_id": room2.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_5h_30,
                "end_time": t_6h_30
            })
            arr_lessons_basic_yoga_class_co_hang_nga_5h30_246.append(l3)
        # add-trainees
        self.__enroll('Phương', 'Nguyễn Thị', 'nguyenthiphuong1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:10])
        self.__enroll('Dương', 'Lê Thị', 'lethiduong1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:12])
        self.__enroll('Hương', 'Nguyễn Thị Ngọc', 'nguyenthingochuong1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246)
        self.__enroll('Thảo', 'Trần Thị Thu', 'tranthithuthao1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:18])
        self.__enroll('Trang', 'Lê Thị Phương', 'lethiphuongtrang1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:18])
        self.__enroll('Thủy', 'Trương Thanh', 'truongthanhthuy1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:18])
        self.__enroll('Ngân', 'Đoàn Thị', 'doanthingan1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:18])
        self.__enroll('Thanh', 'Kiều Thị', 'kieuthithanh1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:18])
        self.__enroll('Anh', 'Phạm Thị Khuê', 'phamthikhueanh1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:24])
        self.__enroll('Chuyên', 'Phạm Thị Hồng', 'phamthihongchuyen1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:24])
        # end add-trainees

        intermediate_yoga_class_co_man_7h_246 = intermediate_yoga_course.classes.create(
            name='Lớp trung cấp cô Mận 7h sáng 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_man,
        )
        t_7h = '07:00'
        t_8h = (datetime.strptime(t_7h, '%H:%M') + timedelta(
            minutes=default_range_time_for_practice_lesson)).strftime("%H:%M")

        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            intermediate_yoga_class_co_man_7h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_7h,
                "end_time": t_8h
            })
            intermediate_yoga_class_co_man_7h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_7h,
                "end_time": t_8h
            })
            intermediate_yoga_class_co_man_7h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_7h,
                "end_time": t_8h
            })

        t_15h = '15:00'
        t_16h = (datetime.strptime(t_15h, '%H:%M') + timedelta(
            minutes=default_range_time_for_practice_lesson)).strftime("%H:%M")

        basic_yoga_class_co_nhu_15h_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Như 15h chiều 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_nhu,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_nhu_15h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            basic_yoga_class_co_nhu_15h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            basic_yoga_class_co_nhu_15h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })

        basic_yoga_class_co_man_15h_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Mận 15h chiều 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_man,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_man_15h_246.lessons.create(**{
                "room_id": room2.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            basic_yoga_class_co_man_15h_246.lessons.create(**{
                "room_id": room2.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            basic_yoga_class_co_man_15h_246.lessons.create(**{
                "room_id": room2.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })

        intermediate_yoga_class_co_ngung_15h_246 = intermediate_yoga_course.classes.create(
            name='Lớp trung cấp cô Ngừng 15h chiều 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_ngung,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            intermediate_yoga_class_co_ngung_15h_246.lessons.create(**{
                "room_id": room3.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            intermediate_yoga_class_co_ngung_15h_246.lessons.create(**{
                "room_id": room3.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            intermediate_yoga_class_co_ngung_15h_246.lessons.create(**{
                "room_id": room3.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })

        t_17h = '17:00'
        t_18h = '18:00'
        basic_yoga_class_co_nhu_17h_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Như 17h chiều 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_nhu,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_nhu_17h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })
            basic_yoga_class_co_nhu_17h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })
            basic_yoga_class_co_nhu_17h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })

        t_17h30 = '17:30'
        t_18h30 = '18:30'
        basic_yoga_class_co_kieu_17h30_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Kiều 17h30 chiều 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_kieu,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_kieu_17h30_246.lessons.create(**{
                "room_id": room2.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_17h30,
                "end_time": t_18h30
            })
            basic_yoga_class_co_kieu_17h30_246.lessons.create(**{
                "room_id": room2.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_17h30,
                "end_time": t_18h30
            })
            basic_yoga_class_co_kieu_17h30_246.lessons.create(**{
                "room_id": room2.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_17h30,
                "end_time": t_18h30
            })

        t_18h15 = '18:15'
        t_19h15 = '19:15'
        basic_yoga_class_co_nhu_18h15_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Như 18h15 tối 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_nhu,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_nhu_18h15_246.lessons.create(**{
                "room_id": room1.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })
            basic_yoga_class_co_nhu_18h15_246.lessons.create(**{
                "room_id": room1.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })
            basic_yoga_class_co_nhu_18h15_246.lessons.create(**{
                "room_id": room1.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })

        t_18h35 = '18:35'
        t_19h35 = '19:35'
        basic_yoga_class_co_xuan_18h35_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Xuân 18h35 tối 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_xuan,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_xuan_18h35_246.lessons.create(**{
                "room_id": room3.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_18h35,
                "end_time": t_19h35
            })
            basic_yoga_class_co_xuan_18h35_246.lessons.create(**{
                "room_id": room3.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_18h35,
                "end_time": t_19h35
            })
            basic_yoga_class_co_xuan_18h35_246.lessons.create(**{
                "room_id": room3.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_18h35,
                "end_time": t_19h35
            })

        t_19h = '19:00'
        t_20h = '20:00'
        basic_yoga_class_co_thuy_19h_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Thùy 19h tối 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_thuy,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_thuy_19h_246.lessons.create(**{
                "room_id": room2.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_19h,
                "end_time": t_20h
            })
            basic_yoga_class_co_thuy_19h_246.lessons.create(**{
                "room_id": room2.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_19h,
                "end_time": t_20h
            })
            basic_yoga_class_co_thuy_19h_246.lessons.create(**{
                "room_id": room2.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_19h,
                "end_time": t_20h
            })

        t_19h30 = '19:30'
        t_20h30 = '20:30'
        basic_yoga_class_co_nhan_19h30_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Nhàn 19h30 tối 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_nhan,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_nhan_19h30_246.lessons.create(**{
                "room_id": room1.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })
            basic_yoga_class_co_nhan_19h30_246.lessons.create(**{
                "room_id": room1.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })
            basic_yoga_class_co_nhan_19h30_246.lessons.create(**{
                "room_id": room1.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })

        advanced_yoga_class_co_nhan_19h30_246 = advanced_yoga_course.classes.create(
            name='Lớp nâng cao cô Trà My 19h30 tối 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_tra_my,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            advanced_yoga_class_co_nhan_19h30_246.lessons.create(**{
                "room_id": room4.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })
            advanced_yoga_class_co_nhan_19h30_246.lessons.create(**{
                "room_id": room4.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })
            advanced_yoga_class_co_nhan_19h30_246.lessons.create(**{
                "room_id": room4.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })

        t_6h = '06:00'
        t_7h = '07:00'
        basic_yoga_class_co_nhu_6h_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Như 6h sáng 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_nhu,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_nhu_6h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_6h,
                "end_time": t_7h
            })
            basic_yoga_class_co_nhu_6h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_6h,
                "end_time": t_7h
            })
            basic_yoga_class_co_nhu_6h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_6h,
                "end_time": t_7h
            })

        advanced_yoga_class_thay_tien_6h_357 = advanced_yoga_course.classes.create(
            name='Lớp nâng cao thầy Tiến 6h sáng 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=thay_tien,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            advanced_yoga_class_thay_tien_6h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_6h,
                "end_time": t_7h
            })
            advanced_yoga_class_thay_tien_6h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_6h,
                "end_time": t_7h
            })
            advanced_yoga_class_thay_tien_6h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_6h,
                "end_time": t_7h
            })

        t_9h = '09:00'
        t_10h = '10:00'
        basic_yoga_class_co_phuong_9h_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Phượng 9h sáng 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_phuong,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_phuong_9h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_9h,
                "end_time": t_10h
            })
            basic_yoga_class_co_phuong_9h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_9h,
                "end_time": t_10h
            })
            basic_yoga_class_co_phuong_9h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_9h,
                "end_time": t_10h
            })

        t_15h = '15:00'
        t_16h = '16:00'
        basic_yoga_class_co_thuy_15h_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Thúy 15h chiều 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_thuy,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_thuy_15h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            basic_yoga_class_co_thuy_15h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            basic_yoga_class_co_thuy_15h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })

        basic_yoga_class_co_quyen_15h_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Quyên 15h chiều 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_quyen,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_quyen_15h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            basic_yoga_class_co_quyen_15h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            basic_yoga_class_co_quyen_15h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })

        intermediate_yoga_class_thay_tan_15h_357 = intermediate_yoga_course.classes.create(
            name='Lớp trung cấp thầy Tân 15h chiều 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=thay_tan,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            intermediate_yoga_class_thay_tan_15h_357.lessons.create(**{
                "room_id": room3.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            intermediate_yoga_class_thay_tan_15h_357.lessons.create(**{
                "room_id": room3.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            intermediate_yoga_class_thay_tan_15h_357.lessons.create(**{
                "room_id": room3.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })

        t_17h = '17:00'
        t_18h = '18:00'
        intermediate_yoga_class_thay_thien_17h_357 = intermediate_yoga_course.classes.create(
            name='Lớp trung cấp thầy Thiên 17h chiều 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=thay_thien,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            intermediate_yoga_class_thay_thien_17h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })
            intermediate_yoga_class_thay_thien_17h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })
            intermediate_yoga_class_thay_thien_17h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })

        basic_yoga_class_co_kieu_17h_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Kiều 17h chiều 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_kieu,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_kieu_17h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })
            basic_yoga_class_co_kieu_17h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })
            basic_yoga_class_co_kieu_17h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })

        t_17h30 = '17:30'
        t_18h30 = '18:30'
        basic_yoga_class_co_tra_my_17h30_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Trà My 17h30 chiều 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_tra_my,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_tra_my_17h30_357.lessons.create(**{
                "room_id": room3.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_17h30,
                "end_time": t_18h30
            })
            basic_yoga_class_co_tra_my_17h30_357.lessons.create(**{
                "room_id": room3.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_17h30,
                "end_time": t_18h30
            })
            basic_yoga_class_co_tra_my_17h30_357.lessons.create(**{
                "room_id": room3.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_17h30,
                "end_time": t_18h30
            })

        basic_yoga_class_co_phuong_17h30_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Phượng 17h30 chiều 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_phuong,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_phuong_17h30_357.lessons.create(**{
                "room_id": room4.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_17h30,
                "end_time": t_18h30
            })
            basic_yoga_class_co_phuong_17h30_357.lessons.create(**{
                "room_id": room4.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_17h30,
                "end_time": t_18h30
            })
            basic_yoga_class_co_phuong_17h30_357.lessons.create(**{
                "room_id": room4.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_17h30,
                "end_time": t_18h30
            })

        basic_yoga_class_co_vo_hanh_18h15_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Võ Hạnh 18h15 tối 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_vo_hanh,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_vo_hanh_18h15_357.lessons.create(**{
                "room_id": room1.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })
            basic_yoga_class_co_vo_hanh_18h15_357.lessons.create(**{
                "room_id": room1.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })
            basic_yoga_class_co_vo_hanh_18h15_357.lessons.create(**{
                "room_id": room1.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })

        basic_yoga_class_co_man_18h15_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Mận 18h15 tối 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_man,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_man_18h15_357.lessons.create(**{
                "room_id": room2.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })
            basic_yoga_class_co_man_18h15_357.lessons.create(**{
                "room_id": room2.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })
            basic_yoga_class_co_man_18h15_357.lessons.create(**{
                "room_id": room2.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })

        basic_yoga_class_co_vo_hanh_19h30_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Võ Hạnh 19h30 tối 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=co_vo_hanh,
        )
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            basic_yoga_class_co_vo_hanh_19h30_357.lessons.create(**{
                "room_id": room4.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })
            basic_yoga_class_co_vo_hanh_19h30_357.lessons.create(**{
                "room_id": room4.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })
            basic_yoga_class_co_vo_hanh_19h30_357.lessons.create(**{
                "room_id": room4.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })

    def __add_lectures(self, course):
        data = [
            {
                'name': 'Tư thế chiến binh',
                'description': '''<p>T&ecirc;n tư thế được đặt theo người chiến binh thần thoại Virabhadra mang &yacute; nghĩa sức mạnh v&agrave; sự uy dũng, tư thế chiến binh gi&uacute;p người tập l&agrave;m mạnh hai ch&acirc;n, mở ngực, tăng độ dẻo dai v&agrave; cải thiện thăng bằng. Hơn nữa, b&agrave;i tập Yoga n&agrave;y c&ograve;n gi&uacute;p giảm đau lưng, tăng khả năng hoạt động của phổi, gi&uacute;p c&aacute;nh tay được săn chắc hơn.</p><p><img alt="Bai-tap-yoga-co-ban-cho-nguoi-moi-bat-dau" aria-describedby="caption-attachment-15691" data-no-retina="true" src="/media/seeds/lectures/tu-the-chien-binh.jpg" /></p><p><strong>C&aacute;c bước thực hiện:</strong></p><ul><li>Bước ch&acirc;n phải về ph&iacute;a trước, c&aacute;ch ch&acirc;n tr&aacute;i 1,5m.</li><li>Xoay b&agrave;n ch&acirc;n tr&aacute;i ra ngo&agrave;i 90 độ.</li><li>Duỗi thẳng hai tay bằng vai, hai tay song song với hai ch&acirc;n, l&ograve;ng b&agrave;n tay hướng xuống s&agrave;n.</li><li>Đầu gối khuỵu xuống 90 độ, mắt nh&igrave;n theo hướng mũi tay phải.</li><li>Đổi b&ecirc;n v&agrave; lặp lại động t&aacute;c từ 5-6 hiệp, mỗi hiệp từ 15-20 lần.</li></ul>'''
            },
            {
                'name': 'Tư thế đứa trẻ',
                'description': '''<p>Tư thế yoga n&agrave;y gi&uacute;p bạn giải toả căng thẳng, thư gi&atilde;n ngực, lưng v&agrave; vai. &nbsp;Đặc biệt l&agrave; khi bạn bị đau đầu ch&oacute;ng mặt, tư thế Yoga n&agrave;y c&oacute; thể gi&uacute;p bạn thư gi&atilde;n l&agrave;m giảm đau hiệu quả.</p><p><img alt="Bai-tap-Yoga-co-ban-cho-nguoi-moi-bat-dau" aria-describedby="caption-attachment-15692" data-no-retina="true" src="/media/seeds/lectures/tu-the-dua-tre.jpg" style="height:434px; width:600px" /></p><p><strong>C&aacute;c bước thực hiện:&nbsp;</strong></p><ul><li>Khởi động bằng tư thế quỳ gối với hai tay chống ngang vai, hai đầu gối c&oacute; mở rộng ngang vai hoặc rộng hơn nếu điều đ&oacute; l&agrave;m bạn cảm thấy thoải m&aacute;i.</li><li>Khi bạn thở ra hạ thấp m&ocirc;ng về ph&iacute;a g&oacute;t ch&acirc;n, đồng thời th&acirc;n m&igrave;nh nằm tr&ecirc;n đ&ugrave;i hoặc giữa hai đ&ugrave;i v&agrave; đầu bạn nằm tr&ecirc;n s&agrave;n hoặc tấm đệm tập.</li><li>Đặt c&aacute;nh tay của bạn dọc theo đ&ugrave;i, l&ograve;ng b&agrave;n tay hướng l&ecirc;n.</li><li>Thả lỏng c&aacute;c cơ xung quanh cột sống v&agrave; h&ocirc;ng, h&iacute;t thở chậm r&atilde;i.</li><li>Giữ tư thế v&agrave; thở đều trong 10 ph&uacute;t.</li></ul>'''
            },
            {
                'name': 'Tư thế tam giác',
                'description': '''<p>Tư thế tam gi&aacute;c trong yoga được xem l&agrave; một động t&aacute;c tăng cường sự dẻo dai của cột sống. B&agrave;i tập n&agrave;y c&oacute; t&aacute;c dụng đ&agrave;o thải mỡ t&iacute;ch trữ ở v&ugrave;ng bụng, gi&uacute;p bạn linh hoạt nhẹ nh&agrave;ng hơn.</p><p><img alt="Bai-tap-Yoga-co-ban-cho-nguoi-moi-bat-dau" aria-describedby="caption-attachment-15693" data-no-retina="true" src="/media/seeds/lectures/Tu-the-tam-giac.jpg" style="height:450px; width:800px" /></p><p><strong>C&aacute;c bước thực hiện:</strong></p><ul>	<li>Đứng thẳng, hai ch&acirc;n dạng ra thoải m&aacute;i tạo th&agrave;nh g&oacute;c 45 độ. T&ugrave;y thuộc v&agrave;o k&iacute;ch thước cơ thể bạn, người cao hơn c&oacute; thể đứng khoảng c&aacute;ch rộng hơn.</li><li>Quay b&agrave;n ch&acirc;n tr&aacute;i của bạn một ch&uacute;t sang phải rồi quay b&agrave;n ch&acirc;n phải 90 độ sao cho g&oacute;t ch&acirc;n phải thẳng h&agrave;ng với phần giữa của b&agrave;n ch&acirc;n tr&aacute;i. Giữ chắc đ&ugrave;i của bạn v&agrave; đảm bảo rằng trọng t&acirc;m của gối hướng thẳng với trọng t&acirc;m của cổ ch&acirc;n phải.</li><li>H&iacute;t v&agrave;o v&agrave; đồng thời n&acirc;ng hai tay cao ngang vai, l&ograve;ng b&agrave;n tay &uacute;p xuống.</li><li>Thở ra v&agrave; vươn c&aacute;nh tay phải sang phải, k&eacute;o d&agrave;i th&acirc;n m&igrave;nh qua ch&acirc;n phải khi bạn chuyển h&ocirc;ng sang b&ecirc;n tr&aacute;i.</li><li>Đặt tay phải l&ecirc;n ch&acirc;n, mắt c&aacute; ch&acirc;n hoặc s&agrave;n tập nằm ph&iacute;a b&ecirc;n ngo&agrave;i b&agrave;n ch&acirc;n phải của bạn. Giữ cho hai b&ecirc;n th&acirc;n c&acirc;n bằng.</li><li>Duỗi c&aacute;nh tay tr&aacute;i l&ecirc;n ph&iacute;a trần nh&agrave;, thẳng h&agrave;ng với đỉnh vai. Xoay th&acirc;n m&igrave;nh hướng l&ecirc;n trần nh&agrave;. Giữ cho đầu của bạn ở vị tr&iacute; trung lập hoặc xoay n&oacute; sang tr&aacute;i, mắt nh&igrave;n theo ng&oacute;n c&aacute;i tay tr&aacute;i.</li><li>Giữ tư thế v&agrave; thở trong một ph&uacute;t, sau đ&oacute; thử với b&ecirc;n ngược lại.</li></ul>'''
            },
            {
                'name': 'Tư thế cây cầu',
                'description': '''<p>Đ&acirc;y l&agrave; b&agrave;i tập yoga hữu &iacute;ch, điều trị c&aacute;c bệnh li&ecirc;n quan đến tuyến gi&aacute;p. B&agrave;i tập gi&uacute;p cải thiện t&igrave;nh trạng đau lưng, đau cổ v&agrave; c&aacute;c vấn đề về thần kinh. Nếu luyện tập thường xuy&ecirc;n tư thế c&acirc;y cầu c&oacute; thể gi&uacute;p người tập giảm mỡ bụng v&agrave; l&agrave;m đ&ugrave;i săn chắc.</p><p><img alt="Bai-tap-Yoga-co-ban-cho-nguoi-moi-bat-dau" aria-describedby="caption-attachment-15694" data-no-retina="true" src="/media/seeds/lectures/tu-the-cay-cau.jpg" style="height:600px; width:900px" /></p><p><strong>C&aacute;c bước thực hiện:</strong></p><ul><li>Nằm ngửa tr&ecirc;n tấm thảm của bạn. Cong đầu gối v&agrave; đặt b&agrave;n ch&acirc;n xuống s&agrave;n, g&oacute;t ch&acirc;n s&aacute;t th&acirc;n m&igrave;nh. Hai tay để dọc theo h&ocirc;ng, l&ograve;ng b&agrave;n tay &uacute;p xuống. H&iacute;t v&agrave;o.</li><li>Thở ra, ấn b&agrave;n ch&acirc;n ph&iacute;a trong v&agrave; l&ograve;ng b&agrave;n tay xuống s&agrave;n, nhấc h&ocirc;ng l&ecirc;n. Giữ cho đ&ugrave;i v&agrave; cạnh trong b&agrave;n ch&acirc;n song song với nhau.</li><li>Bắt hai b&agrave;n tay v&agrave;o nhau b&ecirc;n dưới nếu bạn c&oacute; thể v&agrave; dạng hai b&ecirc;n tay để gi&uacute;p giữ th&acirc;n người tr&ecirc;n đỉnh vai.</li><li>N&acirc;ng m&ocirc;ng của bạn cho đến khi đ&ugrave;i song song với s&agrave;n. Sử dụng ch&acirc;n để gi&uacute;p n&acirc;ng xương chậu. Hướng xương cụt về ph&iacute;a mặt sau đầu gối. N&acirc;ng xương mu về ph&iacute;a rốn.</li><li>Hơi n&acirc;ng cằm của bạn ra xa xương ức một ch&uacute;t, giữ chắc xương bả vai chống đỡ cho lưng, hướng đầu tr&ecirc;n xương ức về ph&iacute;a cằm.</li><li>Giữ nguy&ecirc;n tư thế trong một v&agrave;i nhịp thơ. Khi thở ra, thả lỏng v&agrave; hơi hoay cột sống xuống s&agrave;n tập.</li></ul>'''
            },
            {
                'name': 'Tư thế ngọn núi',
                'description': '''<p>B&agrave;i tập yoga n&agrave;y gi&uacute;p tạo kh&ocirc;ng gian mở b&ecirc;n trong cơ thể. Gi&uacute;p cơ quan nội tạng b&ecirc;n trong cơ thể hoạt động tốt hơn. Ngo&agrave;i ra c&ograve;n&nbsp;cải thiện tư thế đứng&nbsp;của bạn được thẳng hơn,tăng th&ecirc;m sức mạnh v&ugrave;ng ch&acirc;n v&agrave; vai.</p><p><img alt="Bai-tap-Yoga-co-ban-cho-nguoi-moi-bat-dau" aria-describedby="caption-attachment-15695" data-no-retina="true" src="/media/seeds/lectures/tu-the-ngon-nui.jpg" style="height:600px; width:600px" /></p><p><strong>C&aacute;c bước thực hiện:</strong></p><ul><li>Đứng thẳng, hai ch&acirc;n kh&eacute;p lại, hai vai thả lỏng.</li><li>Trọng lượng cơ thể ph&acirc;n t&aacute;n qua hai l&ograve;ng b&agrave;n ch&acirc;n, hai tay đặt hai b&ecirc;n.</li><li>H&iacute;t s&acirc;u v&agrave; n&acirc;ng hai tay song song qua đầu, l&ograve;ng b&agrave;n tay hướng v&agrave;o nhau.</li><li>Tạo cơ thể th&agrave;nh một đường thẳng từ ng&oacute;n tay tới g&oacute;t ch&acirc;n.</li></ul>'''
            },
            {
                'name': 'Tư thế chó cúi mặt',
                'description': '''<p>Tư thế ch&oacute; c&uacute;i mặt gi&uacute;p tăng sức mạnh cơ bụng, t&aacute;c động l&ecirc;n tay v&agrave; ch&acirc;n. Khi thực hiện tư thế n&agrave;y, to&agrave;n bộ trọng lượng cơ thể sẽ dồn l&ecirc;n tay v&agrave; ch&acirc;n n&ecirc;n sẽ gi&uacute;p bạn giữ thăng bằng tốt hơn. Hơn nữa, b&agrave;i tập n&agrave;y gi&uacute;p cải thiện hệ tuần ho&agrave;n, lưu th&ocirc;ng m&aacute;u tốt hơn, hệ ti&ecirc;u h&oacute;a hoạt động dễ hơn.</p><p><img alt="Bai-tap-Yoga-co-ban-cho-nguoi-moi-bat-dau" aria-describedby="caption-attachment-15697" data-no-retina="true" src="/media/seeds/lectures/tu-the-cho-cui-mat.jpg" style="height:462px; width:800px" /></p><p><strong>C&aacute;c bước thực hiện:</strong></p><ul><li>Quỳ tr&ecirc;n cả hai ch&acirc;n v&agrave; hai tay, đầu gối mở rộng bằng h&ocirc;ng. Hai tay mở rộng bằng vai, c&aacute;c ng&oacute;n tay x&ograve;e rộng.</li><li>H&iacute;t v&agrave;o, dồn lực đều v&agrave;o b&agrave;n tay &eacute;p xuống s&agrave;n v&agrave; n&acirc;ng đầu gối l&ecirc;n khỏi s&agrave;n.</li><li>N&acirc;ng h&ocirc;ng của bạn l&ecirc;n v&agrave; hạ xuống, l&agrave;m li&ecirc;n tục để căng gi&atilde;n cột sống.</li><li>Thở ra khi bạn bắt đầu duỗi thẳng ch&acirc;n hết mức c&oacute; thể, g&oacute;t ch&acirc;n hướng xuống s&agrave;n. Nếu ch&acirc;n bạn thẳng c&oacute; thể n&acirc;ng cơ đ&ugrave;i mạnh hơn khi ấn ch&acirc;n xuống s&agrave;n.</li><li>Nhấc người sao cho vai vượt ra khỏi ta, tạo phẳng cho xương bả vai tr&ecirc;n lưng.Xoay c&aacute;nh tay hướng xuống ph&iacute;a dưới s&agrave;n nh&agrave;, giữ vững phần h&ocirc;ng của bạn hướng về ph&iacute;a trung t&acirc;m.</li><li>Tiếp tục h&iacute;t v&agrave;o v&agrave; thở ra đều khi bạn giữ nguy&ecirc;n tư thế.</li></ul>'''
            },
            {
                'name': 'Tư thế cái cây',
                'description': '''<p>Tư thế c&aacute;i c&acirc;y gi&uacute;p tăng cường khả năng sự thăng bằng của bạn. Khi thực hiện b&agrave;i tập n&agrave;y, bạn sẽ r&egrave;n luyện t&iacute;nh ki&ecirc;n nhẫn, sự bền bỉ v&agrave; duy tr&igrave; trạng th&aacute;i t&acirc;m l&yacute; thư th&aacute;i, tĩnh t&acirc;m.</p><p><img alt="Bai-tap-Yoga-co-ban-cho-nguoi-moi-bat-dau" aria-describedby="caption-attachment-15700" data-no-retina="true" src="/media/seeds/lectures/tu-the-cai-cay-1.jpg" style="height:525px; width:600px" /></p><p><strong>C&aacute;c bước thực hiện:</strong></p><ul><li>Đứng tr&ecirc;n tấm thảm, hai ch&acirc;n bạn đặt s&aacute;t nhau hoặc hơi c&aacute;ch nhau nếu điều đ&oacute; l&agrave;m bạn thoải m&aacute;i. H&iacute;t một hơi.</li><li>Từ từ chuyển trọng lượng của bạn sang ch&acirc;n phải.</li><li>N&acirc;ng ch&acirc;n tr&aacute;i l&ecirc;n v&agrave; kẹp mắt c&aacute; ch&acirc;n của bạn để hướng l&ograve;ng b&agrave;n ch&acirc;n tr&aacute;i đến đ&ugrave;i trong của ch&acirc;n phải. Cố gắng giữ h&ocirc;ng ngang bằng.</li><li>Tựa b&agrave;n ch&acirc;n v&agrave;o đ&ugrave;i v&agrave; đ&ugrave;i đỡ lấy b&agrave;n ch&acirc;n.N&acirc;ng người l&ecirc;n qua ch&acirc;n đứng, th&acirc;n v&agrave; ngực của bạn.</li><li>H&iacute;t thở thường xuy&ecirc;n khi bạn giữ tư thế trong một v&agrave;i nhịp thở. Bạn c&oacute; thể chắp hai l&ograve;ng b&agrave;n tay v&agrave;o nhau l&ecirc;n ngực hoặc giơ hai tay l&ecirc;n tr&ecirc;n đầu nếu bạn cảm thấy đủ vững.</li><li>Hạ ch&acirc;n tr&aacute;i xuống v&agrave; thử tư thế n&agrave;y cho b&ecirc;n ngược lại.</li></ul>'''
            },
            {
                'name': 'Tư thế ngồi xoay người',
                'description': '''<p>Tư thế ngồi xoay người l&agrave; b&agrave;i tập tăng khả năng vận động linh hoạt của lưng v&agrave; h&ocirc;ng, gi&uacute;p bạn giảm &aacute;p lực, tạo sự thoải m&aacute;i. B&agrave;i tập n&agrave;y rất th&iacute;ch hợp cho d&acirc;n văn ph&ograve;ng sau những giờ l&agrave;m việc ngồi l&igrave; một chỗ, &iacute;t vận động cơ lưng, h&ocirc;ng.</p><p><img alt="Bai-tap-Yoga-co-ban-cho-nguoi-moi-bat-dau" aria-describedby="caption-attachment-15702" data-no-retina="true" src="/media/seeds/lectures/tu-the-xoay-nguoi.jpg" style="height:333px; width:500px" /></p><p><strong>C&aacute;c bước thực hiện:</strong></p><ul><li>Duỗi hai vai, h&ocirc;ng v&agrave; lưng.</li><li>Ngồi tr&ecirc;n s&agrave;n, hai ch&acirc;n duỗi thẳng.</li><li>Ch&eacute;o ch&acirc;n phải qua đ&ugrave;i tr&aacute;i, cong gối tr&aacute;i. Giữ gối phải hướng l&ecirc;n trần nh&agrave;.</li><li>Đặt c&ugrave;i chỏ tr&aacute;i tr&ecirc;n gối phải v&agrave; tay phải đặt tr&ecirc;n s&agrave;n ph&iacute;a sau lưng.</li><li>Vặn người qua b&ecirc;n phải c&agrave;ng nhiều c&agrave;ng tốt, di chuyển cơ bụng; giữ m&ocirc;ng cố định tr&ecirc;n s&agrave;n. Giữ nguy&ecirc;n tư thế n&agrave;y trong 1 ph&uacute;t.</li><li>Đổi b&ecirc;n v&agrave; lặp lại tư thế.</li></ul>'''
            },
            {
                'name': 'Tư thế rắn hổ mang',
                'description': '''<p>Tư thế rắn hổ mang hay c&ograve;n gọi l&agrave; b&agrave;i tập Bhujangasana mang lại nhiều lợi &iacute;ch cho sức khỏe của bạn. B&agrave;i tập củng cố sự khỏe mạnh, dẻo dai của cột sống, gi&uacute;p qu&aacute; tr&igrave;nh cải thiện lưu th&ocirc;ng m&aacute;u tốt. Hơn nữa, b&agrave;i tập c&oacute; t&aacute;c dụng k&iacute;ch th&iacute;ch qu&aacute; tr&igrave;nh ti&ecirc;u h&oacute;a, giảm căng thẳng, lo &acirc;u.</p><p><img alt="Bai-tap-Yoga-co-ban-cho-nguoi-moi-tap" aria-describedby="caption-attachment-15703" data-no-retina="true" src="/media/seeds/lectures/tu-the-ran-ho-mang.jpg" style="height:284px; width:500px" /></p><p><strong>C&aacute;c bước thực hiện:</strong></p><ul><li>Nằm sấp xuống s&agrave;n, nhấn mũi ch&acirc;n xuống s&agrave;n tập.</li><li>Đặt hai dưới vai, giữ khuỷa tay s&aacute;t th&acirc;n. Nhấc rốn l&ecirc;n khỏi s&agrave;n tập.</li><li>H&iacute;t v&agrave;o, nhấn mũi ch&acirc;n v&agrave; nhấn ph&iacute;a ch&acirc;n &uacute;t xuống s&agrave;n, thả xương đu&ocirc;i của bạn xuống về ph&iacute;a xương mu khi bạn thực hiện duỗi thẳng c&aacute;nh tay để n&acirc;ng đầu v&agrave; ngực về ph&iacute;a trước v&agrave; l&ecirc;n khỏi s&agrave;n.</li><li>H&iacute;t v&agrave;o khi bạn mở rộng ngực v&agrave; giữ hơi thở của bạn một, hai nhịp.</li><li>Khi thở ra, nhớ hạ đầu, cổ v&agrave; ngực xuống s&agrave;n tập.</li></ul>'''
            },
            {
                'name': 'Tư thế chim bồ câu',
                'description': '''<p>Tư thế chim bồ c&acirc;u l&agrave; b&agrave;i tập với mục ti&ecirc;u l&agrave;m săn chắc cơ m&ocirc;ng. B&agrave;i tập n&acirc;ng cao sự vận động linh hoạt của c&aacute;c cơ xương chậu c&ugrave;ng sự dẻo dai cho cột sống.</p><p><img alt="Bai-tap-Yoga-co-ban-cho-nguoi-moi-bat-dau" aria-describedby="caption-attachment-15704" data-no-retina="true" src="/media/seeds/lectures/tu-the-chim-bo-cau.jpg" style="height:338px; width:600px" /></p><p><strong>C&aacute;c bước thực hiện:</strong></p><ul><li>Bắt đầu ở tư thế h&iacute;t đất, l&ograve;ng b&agrave;n tay &uacute;p.</li><li>Hạ xuống cẳng tay v&agrave; k&eacute;o ch&acirc;n phải xuống, mu b&agrave;n ch&acirc;n đặt tr&ecirc;n s&agrave;n.</li><li>N&acirc;ng cao ngực l&ecirc;n, mắt nh&igrave;n xuống.</li><li>K&eacute;o ngực xuống dưới s&agrave;n v&agrave; duỗi hai c&aacute;nh tay ra ph&iacute;a trước. Hơi thu rốn về hướng xương cột sống v&agrave; căng cơ xương chậu.</li><li>Cong gối xuống s&agrave;n v&agrave; thả lỏng, lặp lại 5 lần</li><li>Đổi b&ecirc;n v&agrave; lặp lại tư thế.</li></ul>'''
            },
        ]
        for d in data:
            course.lectures.create(**d)

    def __enroll(self, first_name, last_name, email, yoga_class, card_type, lesson_arr):
        data = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        }
        u = User(**data)
        u.set_password('truong77')
        u.is_trainee = True
        u.save()
        trainee = Trainee.objects.create(user=u)
        card = trainee.cards.create(
            yogaclass=yoga_class, card_type=card_type)
        CardInvoiceService(card, 'Thanh toán thẻ tập', lesson_arr.__len__(
        ) * yoga_class.price_per_lesson).call()
        RollCallService(card, lesson_arr).call()
