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
                                    FOR_SOME_LESSONS, FOR_TRIAL, FOR_TRAINING_COURSE, FOR_PERIOD_TIME_LESSONS)
from apps.cards.models import Card
from apps.roll_calls.models import RollCall
from services.card_invoice_service import CardInvoiceService
from services.roll_call_service import RollCallService
from apps.blog.models import PostCategory, Post
from apps.events.models import Event
from apps.faq.models import FAQ
from services.roll_call_service import RollCallService
from services.card_invoice_service import CardInvoiceService
from apps.shop.models import ProductCategory, Product
from random import randint
import uuid
from apps.card_invoices.models import PREPAID, POSTPAID


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

        default_range_time_for_practice_lesson = 60
        default_range_time_for_training_lesson = 120

        print("Create ADMIN")
        self.__create_admin()

        print("Create STAFF")
        self.__create_staffs()

        print("Create BLOG")
        self.__create_blog()

        print("Create EVENTS")
        self.__create_events()

        print("Create FAQ")
        self.__create_faq()

        print("Create SHOP")
        self.__create_shop()

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
            'name': 'Đăng ký học theo tháng',
            'description': 'Áp dụng cho học viên muốn học tất cả các buổi trong tháng',
            'form_of_using': FOR_FULL_MONTH
        }
        full_month_card_type = CardType(**data_for_full_month)
        full_month_card_type.save()

        print("Create <FOR PERIOD TIME LESSONS> CARD TYPE")
        data_for_period_lessons = {
            'name': 'Đăng ký học trong khoảng thời gian',
            'description': 'Áp dụng cho học viên muốn đăng kí học trong một khoảng thời gian xác định.',
            'form_of_using': FOR_PERIOD_TIME_LESSONS
        }
        period_lessons_card_type = CardType(
            **data_for_period_lessons)
        period_lessons_card_type.save()

        print("Create <FOR SOME LESSONS> CARD TYPE")
        data_for_some_lessons = {
            'name': 'Đăng ký học một số buổi',
            'description': 'Áp dụng cho học viên muốn đăng kí học một số buổi',
            'form_of_using': FOR_SOME_LESSONS,
            'multiplier': 1.5
        }
        some_lessons_card_type = CardType(
            **data_for_some_lessons)
        some_lessons_card_type.save()

        print("Create <FOR TRIAL> CARD TYPE")
        data_for_trial = {
            'name': 'Đăng ký học thử',
            'description': 'Áp dụng cho học viên muốn học thử 1 buổi miễn phí',
            'form_of_using': FOR_TRIAL
        }
        trial_card_type = CardType(
            **data_for_trial)
        trial_card_type.save()

        print("Create <FOR TRAINING COURSE> CARD TYPE")
        data_for_training_course = {
            'name': 'Đăng ký học khóa đào tạo',
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
            period_lessons_card_type,
            some_lessons_card_type,
            trial_card_type
        )
        # Add Lectures
        self.__add_basic_lectures(basic_yoga_course)

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
            period_lessons_card_type,
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
            period_lessons_card_type,
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
            'price_for_training_class': 15000000,
        }
        training_yoga_trainer_course = Course(
            **training_yoga_trainer_course_data)
        training_yoga_trainer_course.save()

        training_yoga_trainer_course.card_types.add(
            training_course_card_type
        )
        self.__add_training_lectures(training_yoga_trainer_course)

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
            "max_people": 10
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
        basic_yoga_course_lectures = basic_yoga_course.lectures.all()
        basic_yoga_course_lectures_count = basic_yoga_course_lectures.count()

        number_of_weeks = 12
        basic_yoga_class_co_man_5h30_t246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Mận 5h30 sáng 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
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
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_man_5h30_246.append(l1)
            l2 = basic_yoga_class_co_man_5h30_t246.lessons.create(**{
                "room_id": room1.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_5h_30,
                "end_time": t_6h_30
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_man_5h30_246.append(l2)
            l3 = basic_yoga_class_co_man_5h30_t246.lessons.create(**{
                "room_id": room1.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_5h_30,
                "end_time": t_6h_30
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_man_5h30_246.append(l3)
        # add-trainees
        self.__enroll('Dung', 'Lê Thị Hoàng', 'lethihoangdung1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:10])
        self.__enroll('Thùy', 'Ngô Bích', 'ngobichthuy1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:12])
        self.__enroll('Oanh', 'Đinh Thị Hoàng', 'dinhthihoangoanh1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:18])
        self.__enroll('Giang', 'Mai Thị Cẩm', 'maithicamgiang1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:24])
        self.__enroll('Trinh', 'Nguyễn Thị Diễm', 'nguyenthidiemtrinh1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:36])
        self.__enroll('Vi', 'Đinh Thị Tường', 'dinhthituongvi1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:18])
        self.__enroll('Hàng', 'Phạm Thị', 'phamthihang1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:18])
        self.__enroll('Hoàng', 'Nguyễn Thị Mỹ', 'nguyenthimyhoang1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:24])
        self.__enroll('Vi', 'Lê Tường', 'letuongvi1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:18])
        self.__enroll('Phượng', 'Nguyễn Thị Kim', 'nguyenthikimphuong1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:24])
        self.__enroll('Lý', 'Nguyễn Thị', 'nguyenthily1@gmail.com', basic_yoga_class_co_man_5h30_t246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_5h30_246[0:36])
        # end add-trainees
        basic_yoga_class_co_hang_nga_5h30_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Hằng Nga 5h30 sáng 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
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
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_hang_nga_5h30_246.append(l1)
            l2 = basic_yoga_class_co_hang_nga_5h30_246.lessons.create(**{
                "room_id": room2.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_5h_30,
                "end_time": t_6h_30
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_hang_nga_5h30_246.append(l2)
            l3 = basic_yoga_class_co_hang_nga_5h30_246.lessons.create(**{
                "room_id": room2.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_5h_30,
                "end_time": t_6h_30
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_hang_nga_5h30_246.append(l3)
        # add-trainees
        self.__enroll('Phương', 'Nguyễn Thị', 'nguyenthiphuong1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:10])
        self.__enroll('Dương', 'Lê Thị', 'lethiduong1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:12])
        self.__enroll('Hương', 'Nguyễn Thị Ngọc', 'nguyenthingochuong1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246)
        self.__enroll('Thảo', 'Trần Thị Thu', 'tranthithuthao1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:18])
        self.__enroll('Trang', 'Lê Thị Phương', 'lethiphuongtrang1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:18])
        self.__enroll('Thủy', 'Trương Thanh', 'truongthanhthuy1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:18])
        self.__enroll('Ngân', 'Đoàn Thị', 'doanthingan1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:18])
        self.__enroll('Thanh', 'Kiều Thị', 'kieuthithanh1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:18])
        self.__enroll('Anh', 'Phạm Thị Khuê', 'phamthikhueanh1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:24])
        self.__enroll('Chuyên', 'Phạm Thị Hồng', 'phamthihongchuyen1@gmail.com', basic_yoga_class_co_hang_nga_5h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_hang_nga_5h30_246[0:24])
        # end add-trainees

        intermediate_yoga_class_co_man_7h_246 = intermediate_yoga_course.classes.create(
            name='Lớp trung cấp cô Mận 7h sáng 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_man,
        )
        t_7h = '07:00'
        t_8h = (datetime.strptime(t_7h, '%H:%M') + timedelta(
            minutes=default_range_time_for_practice_lesson)).strftime("%H:%M")
        arr_lessons_intermediate_yoga_class_co_man_7h_246 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = intermediate_yoga_class_co_man_7h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_7h,
                "end_time": t_8h
            })
            arr_lessons_intermediate_yoga_class_co_man_7h_246.append(l1)
            l2 = intermediate_yoga_class_co_man_7h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_7h,
                "end_time": t_8h
            })
            arr_lessons_intermediate_yoga_class_co_man_7h_246.append(l2)
            l3 = intermediate_yoga_class_co_man_7h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_7h,
                "end_time": t_8h
            })
            arr_lessons_intermediate_yoga_class_co_man_7h_246.append(l3)
        # add-trainees
        self.__enroll('Nhi', 'Võ Thị', 'vothinhi1@gmail.com', intermediate_yoga_class_co_man_7h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_man_7h_246[0:10])
        self.__enroll('Hương', 'Lê Thị Thu', 'lethithuhuong1@gmail.com', intermediate_yoga_class_co_man_7h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_man_7h_246[0:12])
        self.__enroll('Các', 'Đặng Thị Thúy', 'dangthithuycac1@gmail.com', intermediate_yoga_class_co_man_7h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_man_7h_246)
        self.__enroll('Lan', 'Nguyễn Huỳnh', 'nguyenhuynhlan1@gmail.com', intermediate_yoga_class_co_man_7h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_man_7h_246[0:18])
        self.__enroll('Thanh', 'Hoàng Thị Lý', 'hoangthilythanh1@gmail.com', intermediate_yoga_class_co_man_7h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_man_7h_246[0:18])
        self.__enroll('My', 'Đặng Thị Diễm', 'dangthidiemmy1@gmail.com', intermediate_yoga_class_co_man_7h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_man_7h_246[0:18])
        self.__enroll('Đức', 'Võ Minh', 'vominhduc1@gmail.com', intermediate_yoga_class_co_man_7h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_man_7h_246[0:18])
        self.__enroll('Vui', 'Nhan Thị Kim', 'nhanthikimvui1@gmail.com', intermediate_yoga_class_co_man_7h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_man_7h_246[0:18])
        self.__enroll('Hồng', 'Bùi Thị', 'buithihong1@gmail.com', intermediate_yoga_class_co_man_7h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_man_7h_246[0:24])
        self.__enroll('Hằng', 'Bành Thị Diễm', 'banhthidiemhang1@gmail.com', intermediate_yoga_class_co_man_7h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_man_7h_246[0:24])
        # end add-trainees
        t_15h = '15:00'
        t_16h = (datetime.strptime(t_15h, '%H:%M') + timedelta(
            minutes=default_range_time_for_practice_lesson)).strftime("%H:%M")

        basic_yoga_class_co_nhu_15h_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Như 15h chiều 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_nhu,
        )
        arr_lessons_basic_yoga_class_co_nhu_15h_246 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_nhu_15h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_nhu_15h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_nhu_15h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_nhu_15h_246.append(l1)
            arr_lessons_basic_yoga_class_co_nhu_15h_246.append(l2)
            arr_lessons_basic_yoga_class_co_nhu_15h_246.append(l3)
        # add-trainees
        self.__enroll('Nga', 'Từ Thị Nguyệt', 'tuthinguyetnga1@gmail.com', basic_yoga_class_co_nhu_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_15h_246[0:10])
        self.__enroll('Én', 'Võ Thị', 'vothien1@gmail.com', basic_yoga_class_co_nhu_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_15h_246[0:12])
        self.__enroll('Hằng', 'Nguyễn Thị', 'nguyenthihang1@gmail.com', basic_yoga_class_co_nhu_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_15h_246)
        self.__enroll('Hiền', 'Nguyễn Thị Diệu', 'nguyenthidieuhien1@gmail.com', basic_yoga_class_co_nhu_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_15h_246[0:18])
        self.__enroll('Oanh', 'Hà Kiều', 'hakieuoanh1@gmail.com', basic_yoga_class_co_nhu_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_15h_246[0:18])
        self.__enroll('Thúy', 'Võ Thị Thanh', 'vothithanhthuy1@gmail.com', basic_yoga_class_co_nhu_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_15h_246[0:18])
        self.__enroll('Oanh', 'Đặng Thu', 'dangthuoanh1@gmail.com', basic_yoga_class_co_nhu_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_15h_246[0:18])
        self.__enroll('Khuê', 'Bùi Thị Kim', 'buithikimkhue1@gmail.com', basic_yoga_class_co_nhu_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_15h_246[0:18])
        self.__enroll('Yến', 'Trần Thị Hải', 'tranthihaiyen1@gmail.com', basic_yoga_class_co_nhu_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_15h_246[0:24])
        self.__enroll('Huyền', 'Hoàng Thị Diệu', 'hoangthidieuhuyen1@gmail.com', basic_yoga_class_co_nhu_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_15h_246[0:24])
        # end add-trainees
        basic_yoga_class_co_man_15h_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Mận 15h chiều 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_man,
        )
        arr_lessons_basic_yoga_class_co_man_15h_246 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_man_15h_246.lessons.create(**{
                "room_id": room2.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_man_15h_246.lessons.create(**{
                "room_id": room2.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_man_15h_246.lessons.create(**{
                "room_id": room2.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_man_15h_246.append(l1)
            arr_lessons_basic_yoga_class_co_man_15h_246.append(l2)
            arr_lessons_basic_yoga_class_co_man_15h_246.append(l3)
        # add-trainees
        self.__enroll('Hồng', 'Phạm Thị Anh', 'phamthianhhong1@gmail.com', basic_yoga_class_co_man_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_15h_246[0:10])
        self.__enroll('Huyền', 'Huỳnh Thanh', 'huynhthanhhuyen1@gmail.com', basic_yoga_class_co_man_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_15h_246[0:12])
        self.__enroll('Quyên', 'Nguyễn Thị Xuân', 'nguyenthixuanquyen@gmail.com', basic_yoga_class_co_man_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_15h_246)
        self.__enroll('Như', 'Cao Võ Quỳnh', 'caovoquynhnhu1@gmail.com', basic_yoga_class_co_man_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_15h_246[0:18])
        self.__enroll('Thụy', 'Đỗ Cao Đan', 'docaodanthuy1@gmail.com', basic_yoga_class_co_man_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_15h_246[0:18])
        self.__enroll('Hà', 'Đoàn Thị Thu', 'doanthithuha1@gmail.com', basic_yoga_class_co_man_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_15h_246[0:18])
        self.__enroll('Thiệm', 'Trương Văn Công', 'truongvancongthiem1@gmail.com', basic_yoga_class_co_man_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_15h_246[0:18])
        self.__enroll('Trang', 'Lý Kiều', 'lykieutrang1@gmail.com', basic_yoga_class_co_man_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_15h_246[0:18])
        self.__enroll('Hạnh', 'Hồ Thị Mỹ', 'hothimyhanh1@gmail.com', basic_yoga_class_co_man_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_15h_246[0:24])
        self.__enroll('Thy', 'Trần Minh', 'tranminhthy1@gmail.com', basic_yoga_class_co_man_15h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_15h_246[0:24])
        # end add-trainees

        intermediate_yoga_class_co_ngung_15h_246 = intermediate_yoga_course.classes.create(
            name='Lớp trung cấp cô Ngừng 15h chiều 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_ngung,
        )
        arr_lessons_intermediate_yoga_class_co_ngung_15h_246 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = intermediate_yoga_class_co_ngung_15h_246.lessons.create(**{
                "room_id": room3.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            l2 = intermediate_yoga_class_co_ngung_15h_246.lessons.create(**{
                "room_id": room3.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            l3 = intermediate_yoga_class_co_ngung_15h_246.lessons.create(**{
                "room_id": room3.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            arr_lessons_intermediate_yoga_class_co_ngung_15h_246.append(l1)
            arr_lessons_intermediate_yoga_class_co_ngung_15h_246.append(l2)
            arr_lessons_intermediate_yoga_class_co_ngung_15h_246.append(l3)
        # add-trainees
        self.__enroll('Hà', 'Nguyễn Thị Thanh', 'nguyenthithanhha1@gmail.com', intermediate_yoga_class_co_ngung_15h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_ngung_15h_246[0:10])
        self.__enroll('Thảo', 'Trần Thị Mai', 'tranthimaithao1@gmail.com', intermediate_yoga_class_co_ngung_15h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_ngung_15h_246[0:12])
        self.__enroll('Ánh', 'Phan Thị Ngọc', 'phanthingocanh1@gmail.com', intermediate_yoga_class_co_ngung_15h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_ngung_15h_246)
        self.__enroll('Phượng', 'Đoàn Thị Kim', 'doanthikimphuong1@gmail.com', intermediate_yoga_class_co_ngung_15h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_ngung_15h_246[0:18])
        self.__enroll('Hân', 'Ngô Gia', 'ngogiahan1@gmail.com', intermediate_yoga_class_co_ngung_15h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_ngung_15h_246[0:18])
        self.__enroll('Đạm', 'Phạm Thị', 'phamthidam1@gmail.com', intermediate_yoga_class_co_ngung_15h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_ngung_15h_246[0:18])
        self.__enroll('Thư', 'Nguyễn Thị Diễm', 'nguyenthidiemthu1@gmail.com', intermediate_yoga_class_co_ngung_15h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_ngung_15h_246[0:18])
        self.__enroll('Hạnh', 'Mạc Tuyết', 'mactuyethanh1@gmail.com', intermediate_yoga_class_co_ngung_15h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_ngung_15h_246[0:18])
        self.__enroll('Thanh', 'Hoàng Thị', 'hoangthithanh1@gmail.com', intermediate_yoga_class_co_ngung_15h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_ngung_15h_246[0:24])
        self.__enroll('Tâm', 'Đào Thị Minh', 'daothiminhtam1@gmail.com', intermediate_yoga_class_co_ngung_15h_246,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_co_ngung_15h_246[0:24])
        # end add-trainees

        t_17h = '17:00'
        t_18h = '18:00'
        basic_yoga_class_co_nhu_17h_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Như 17h chiều 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_nhu,
        )
        arr_lessons_basic_yoga_class_co_nhu_17h_246 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_nhu_17h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_nhu_17h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_nhu_17h_246.lessons.create(**{
                "room_id": room1.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_nhu_17h_246.append(l1)
            arr_lessons_basic_yoga_class_co_nhu_17h_246.append(l2)
            arr_lessons_basic_yoga_class_co_nhu_17h_246.append(l3)
        # add-trainees
        self.__enroll('Trâm', 'Đèo Nguyễn Mai', 'deonguyenmaitram1@gmail.com', basic_yoga_class_co_nhu_17h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_17h_246[0:10])
        self.__enroll('Hạnh', 'Cao Thị Ngọc', 'caothingochanh1@gmail.com', basic_yoga_class_co_nhu_17h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_17h_246[0:12])
        self.__enroll('Vy', 'Lê Thị Tường', 'lethituongvy1@gmail.com', basic_yoga_class_co_nhu_17h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_17h_246)
        self.__enroll('Phượng', 'Thanh', 'thanhphuong1@gmail.com', basic_yoga_class_co_nhu_17h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_17h_246[0:18])
        self.__enroll('Thảo', 'Lê Thị', 'lethithao1@gmail.com', basic_yoga_class_co_nhu_17h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_17h_246[0:18])
        self.__enroll('Xuân', 'Lê Hoàng', 'lehoangxuan1@gmail.com', basic_yoga_class_co_nhu_17h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_17h_246[0:18])
        self.__enroll('Thư', 'Hoàng Anh', 'hoanganhthu1@gmail.com', basic_yoga_class_co_nhu_17h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_17h_246[0:18])
        self.__enroll('Xuân', 'Dương Thị Tuyết', 'duongthituyetxuan1@gmail.com', basic_yoga_class_co_nhu_17h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_17h_246[0:18])
        self.__enroll('Thanh', 'Nguyễn Phạm Hằng', 'nguyenphamhangthanh1@gmail.com', basic_yoga_class_co_nhu_17h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_17h_246[0:24])
        # end add-trainees

        t_17h30 = '17:30'
        t_18h30 = '18:30'
        basic_yoga_class_co_kieu_17h30_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Kiều 17h30 chiều 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_kieu,
        )
        arr_lessons_basic_yoga_class_co_kieu_17h30_246 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_kieu_17h30_246.lessons.create(**{
                "room_id": room2.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_17h30,
                "end_time": t_18h30
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_kieu_17h30_246.lessons.create(**{
                "room_id": room2.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_17h30,
                "end_time": t_18h30
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_kieu_17h30_246.lessons.create(**{
                "room_id": room2.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_17h30,
                "end_time": t_18h30
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_kieu_17h30_246.append(l1)
            arr_lessons_basic_yoga_class_co_kieu_17h30_246.append(l2)
            arr_lessons_basic_yoga_class_co_kieu_17h30_246.append(l3)
        # add-trainees
        self.__enroll('Cương', 'Trần Thị Kim', 'tranthikimcuong1@gmail.com', basic_yoga_class_co_kieu_17h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h30_246[0:10])
        self.__enroll('Hương', 'Nguyễn Thị Thúy', 'nguyenthithuyhuong1@gmail.com', basic_yoga_class_co_kieu_17h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h30_246[0:12])
        self.__enroll('Oanh', 'Nguyễn Thị Kim', 'nguyenthikimoanh1@gmail.com', basic_yoga_class_co_kieu_17h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h30_246)
        self.__enroll('Anh', 'Phạm Hoàng', 'phamhoanganh1@gmail.com', basic_yoga_class_co_kieu_17h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h30_246[0:18])
        self.__enroll('Lành', 'Nguyễn Thị Bích', 'nguyenthibichlanh1@gmail.com', basic_yoga_class_co_kieu_17h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h30_246[0:18])
        self.__enroll('Phương', 'Bùi Thị Thanh', 'buithithanhphuong1@gmail.com', basic_yoga_class_co_kieu_17h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h30_246[0:18])
        self.__enroll('Vân', 'Nguyễn Ngọc Thùy', 'nguyenngocthuyvan1@gmail.com', basic_yoga_class_co_kieu_17h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h30_246[0:18])
        self.__enroll('Vi', 'Dương Thị Hoài', 'duongthihoaivy1@gmail.com', basic_yoga_class_co_kieu_17h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h30_246[0:18])
        self.__enroll('Ngọc', 'Đào Thị Bích', 'daothibichngoc1@gmail.com', basic_yoga_class_co_kieu_17h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h30_246[0:24])
        # end add-trainees

        t_18h15 = '18:15'
        t_19h15 = '19:15'
        basic_yoga_class_co_nhu_18h15_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Như 18h15 tối 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_nhu,
        )
        arr_lessons_basic_yoga_class_co_nhu_18h15_246 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_nhu_18h15_246.lessons.create(**{
                "room_id": room1.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_nhu_18h15_246.lessons.create(**{
                "room_id": room1.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_nhu_18h15_246.lessons.create(**{
                "room_id": room1.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_nhu_18h15_246.append(l1)
            arr_lessons_basic_yoga_class_co_nhu_18h15_246.append(l2)
            arr_lessons_basic_yoga_class_co_nhu_18h15_246.append(l3)
        # add-trainees
        self.__enroll('Tâm', 'Hồ Thị Minh', 'hothiminhtam1@gmail.com', basic_yoga_class_co_nhu_18h15_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_18h15_246[0:10])
        self.__enroll('Tú', 'Hồ Thị Minh', 'hothiminhtu1@gmail.com', basic_yoga_class_co_nhu_18h15_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_18h15_246[0:12])
        self.__enroll('Vân', 'Ngô Thị Thùy', 'ngothithuyvan1@gmail.com', basic_yoga_class_co_nhu_18h15_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_18h15_246)
        self.__enroll('Dương', 'Trần Thị Thùy', 'tranthithuyduong1@gmail.com', basic_yoga_class_co_nhu_18h15_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_18h15_246[0:18])
        self.__enroll('Trúc', 'Ngô Thị Túy', 'ngothituytruc1@gmail.com', basic_yoga_class_co_nhu_18h15_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_18h15_246[0:18])
        self.__enroll('Hà', 'Phan Thị Thu', 'phanthithuha1@gmail.com', basic_yoga_class_co_nhu_18h15_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_18h15_246[0:18])
        self.__enroll('Thư', 'Lê Thị Minh', 'lethiminhthu1@gmail.com', basic_yoga_class_co_nhu_18h15_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_18h15_246[0:18])
        self.__enroll('Hồng', 'Hoàng Thị', 'hoangthihong1@gmail.com', basic_yoga_class_co_nhu_18h15_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_18h15_246[0:18])
        self.__enroll('Hợi', 'Trần Thị', 'tranthihoi1@gmail.com', basic_yoga_class_co_nhu_18h15_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_18h15_246[0:24])
        self.__enroll('Vân', 'Phan Thị Tường', 'phanthituongvan1@gmail.com', basic_yoga_class_co_nhu_18h15_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_18h15_246[0:24])
        self.__enroll('Nguyên', 'Ngô Ngọc Khôi', 'ngongockhoinguyen1@gmail.com', basic_yoga_class_co_nhu_18h15_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_18h15_246[0:24])
        # end add-trainees

        t_18h35 = '18:35'
        t_19h35 = '19:35'
        basic_yoga_class_co_xuan_18h35_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Xuân 18h35 tối 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_xuan,
        )
        arr_lessons_basic_yoga_class_co_xuan_18h35_246 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_xuan_18h35_246.lessons.create(**{
                "room_id": room3.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_18h35,
                "end_time": t_19h35
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_xuan_18h35_246.lessons.create(**{
                "room_id": room3.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_18h35,
                "end_time": t_19h35
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_xuan_18h35_246.lessons.create(**{
                "room_id": room3.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_18h35,
                "end_time": t_19h35
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_xuan_18h35_246.append(l1)
            arr_lessons_basic_yoga_class_co_xuan_18h35_246.append(l2)
            arr_lessons_basic_yoga_class_co_xuan_18h35_246.append(l3)
        # add-trainees
        self.__enroll('Anh', 'Ngô Vân', 'ngovananh1@gmail.com', basic_yoga_class_co_xuan_18h35_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_xuan_18h35_246[0:10])
        self.__enroll('Yến', 'Đoàn Thị Hồng', 'doanthihongyen1@gmail.com', basic_yoga_class_co_xuan_18h35_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_xuan_18h35_246[0:12])
        self.__enroll('Nhung', 'Nguyễn Thị Tuyết', 'nguyenthituyetnhung1@gmail.com', basic_yoga_class_co_xuan_18h35_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_xuan_18h35_246)
        self.__enroll('Trâm', 'Lý Thị Anh', 'lythianhtram1@gmail.com', basic_yoga_class_co_xuan_18h35_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_xuan_18h35_246[0:18])
        self.__enroll('Dung', 'Phan Thị Kim', 'phanthikimdung1@gmail.com', basic_yoga_class_co_xuan_18h35_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_xuan_18h35_246[0:18])
        self.__enroll('Trang', 'Đỗ Minh', 'dominhtrang1@gmail.com', basic_yoga_class_co_xuan_18h35_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_xuan_18h35_246[0:18])
        self.__enroll('Hà', 'Nguyễn Thu', 'nguyenthuha1@gmail.com', basic_yoga_class_co_xuan_18h35_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_xuan_18h35_246[0:18])
        self.__enroll('Toàn', 'Nguyễn Thị Phương', 'nguyenthiphuongtoan1@gmail.com', basic_yoga_class_co_xuan_18h35_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_xuan_18h35_246[0:18])
        self.__enroll('Như', 'Quỳnh', 'nhuquynh1@gmail.com', basic_yoga_class_co_xuan_18h35_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_xuan_18h35_246[0:24])
        self.__enroll('Phấn', 'Phan Mỹ', 'phanmyphan1@gmail.com', basic_yoga_class_co_xuan_18h35_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_xuan_18h35_246[0:24])
        self.__enroll('Trang', 'Trần Thị Ngọc', 'tranthingoctrang1@gmail.com', basic_yoga_class_co_xuan_18h35_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_xuan_18h35_246[0:24])
        self.__enroll('Trang', 'Nguyễn Lê Thu', 'nguyenlethutrang1@gmail.com', basic_yoga_class_co_xuan_18h35_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_xuan_18h35_246[0:24])
        self.__enroll('Oanh', 'Đoàn Thị Kim', 'doanthikimoanh1@gmail.com', basic_yoga_class_co_xuan_18h35_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_xuan_18h35_246[0:24])
        self.__enroll('Hằng', 'Nguyễn Thị Thanh', 'nguyenthithanhhang1@gmail.com', basic_yoga_class_co_xuan_18h35_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_xuan_18h35_246[0:24])
        # end add-trainees

        t_19h = '19:00'
        t_20h = '20:00'
        basic_yoga_class_co_thuy_19h_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Thùy 19h tối 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_thuy,
        )
        arr_lessons_basic_yoga_class_co_thuy_19h_246 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_thuy_19h_246.lessons.create(**{
                "room_id": room2.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_19h,
                "end_time": t_20h
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_thuy_19h_246.lessons.create(**{
                "room_id": room2.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_19h,
                "end_time": t_20h
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_thuy_19h_246.lessons.create(**{
                "room_id": room2.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_19h,
                "end_time": t_20h
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_thuy_19h_246.append(l1)
            arr_lessons_basic_yoga_class_co_thuy_19h_246.append(l2)
            arr_lessons_basic_yoga_class_co_thuy_19h_246.append(l3)
        # add-trainees
        self.__enroll('Phương', 'Trần Thị Thanh', 'tranthithanhphuong1@gmail.com', basic_yoga_class_co_thuy_19h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_19h_246[0:10])
        self.__enroll('Liên', 'Hoàng Thị Quỳnh', 'hoangthiquynhlien1@gmail.com', basic_yoga_class_co_thuy_19h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_19h_246[0:12])
        self.__enroll('Anh', 'Nguyễn Thị Lan', 'nguyenthilananh1@gmail.com', basic_yoga_class_co_thuy_19h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_19h_246)
        self.__enroll('Linh', 'Đoàn Thị Thùy', 'doanthithuylinh1@gmail.com', basic_yoga_class_co_thuy_19h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_19h_246[0:18])
        self.__enroll('Mai', 'Nguyễn Kim', 'nguyenkimmai1@gmail.com', basic_yoga_class_co_thuy_19h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_19h_246[0:18])
        self.__enroll('Trang', 'Nguyễn Vân', 'nguyenvantrang1@gmail.com', basic_yoga_class_co_thuy_19h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_19h_246[0:18])
        self.__enroll('Châu', 'Trần Thị Diễm', 'tranthidiemchau1@gmail.com', basic_yoga_class_co_thuy_19h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_19h_246[0:18])
        self.__enroll('Thúy', 'Lương Thị', 'luongthithuy1@gmail.com', basic_yoga_class_co_thuy_19h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_19h_246[0:18])
        self.__enroll('Thủy', 'Phạm Thanh', 'phamthanhthuy1@gmail.com', basic_yoga_class_co_thuy_19h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_19h_246[0:24])
        self.__enroll('Anh', 'Hoàng Thị Ngọc', 'hoangthingocanh1@gmail.com', basic_yoga_class_co_thuy_19h_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_19h_246[0:24])
        # end add-trainees

        t_19h30 = '19:30'
        t_20h30 = '20:30'
        basic_yoga_class_co_nhan_19h30_246 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Nhàn 19h30 tối 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_nhan,
        )
        arr_lessons_basic_yoga_class_co_nhan_19h30_246 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_nhan_19h30_246.lessons.create(**{
                "room_id": room1.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_nhan_19h30_246.lessons.create(**{
                "room_id": room1.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_nhan_19h30_246.lessons.create(**{
                "room_id": room1.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_nhan_19h30_246.append(l1)
            arr_lessons_basic_yoga_class_co_nhan_19h30_246.append(l2)
            arr_lessons_basic_yoga_class_co_nhan_19h30_246.append(l3)
        # add-trainees
        self.__enroll('Thảo', 'Đặng Hoàng', 'danghoangthao1@gmail.com', basic_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhan_19h30_246[0:10])
        self.__enroll('Phương', 'Trần Thị Bích', 'tranthibichphuong1@gmail.com', basic_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhan_19h30_246[0:12])
        self.__enroll('Sang', 'Phan Thị Châu', 'phanthichausang1@gmail.com', basic_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhan_19h30_246)
        self.__enroll('Liêm', 'Trần Thanh', 'tranthanhliem1@gmail.com', basic_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhan_19h30_246[0:18])
        self.__enroll('Ly', 'Nguyễn Thị Ái', 'nguyenthiaily1@gmail.com', basic_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhan_19h30_246[0:18])
        self.__enroll('Hiền', 'Minh', 'minhhien1@gmail.com', basic_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhan_19h30_246[0:18])
        self.__enroll('Thảo', 'Bùi Phương', 'buiphuongthao1@gmail.com', basic_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhan_19h30_246[0:18])
        self.__enroll('Loan', 'Phạm Thị Thùy', 'phamthithuyloan1@gmail.com', basic_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhan_19h30_246[0:18])
        self.__enroll('Thảo', 'Nguyễn Thị Phương', 'nguyenthiphuongthao1@gmail.com', basic_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhan_19h30_246[0:24])
        self.__enroll('Ngọc', 'Huỳnh Thị Hoàng', 'huynhthihoangngoc1@gmail.com', basic_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhan_19h30_246[0:24])
        self.__enroll('Duy', 'Ánh', 'anhduy1@gmail.com', basic_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhan_19h30_246[0:24])
        # end add-trainees

        advanced_yoga_class_co_nhan_19h30_246 = advanced_yoga_course.classes.create(
            name='Lớp nâng cao cô Trà My 19h30 tối 2-4-6',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_tra_my,
        )
        arr_lessons_advanced_yoga_class_co_nhan_19h30_246 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = advanced_yoga_class_co_nhan_19h30_246.lessons.create(**{
                "room_id": room4.pk,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })
            l2 = advanced_yoga_class_co_nhan_19h30_246.lessons.create(**{
                "room_id": room4.pk,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })
            l3 = advanced_yoga_class_co_nhan_19h30_246.lessons.create(**{
                "room_id": room4.pk,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })
            arr_lessons_advanced_yoga_class_co_nhan_19h30_246.append(l1)
            arr_lessons_advanced_yoga_class_co_nhan_19h30_246.append(l2)
            arr_lessons_advanced_yoga_class_co_nhan_19h30_246.append(l3)
        # add-trainees
        self.__enroll('Thư', 'Huỳnh', 'thuhuynh1@gmail.com', advanced_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_co_nhan_19h30_246[0:10])
        self.__enroll('Huyền', 'Tô Nam', 'tonamhuyen1@gmail.com', advanced_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_co_nhan_19h30_246[0:12])
        self.__enroll('Vỹ', 'Nguyễn Đình', 'nguyendinhvy1@gmail.com', advanced_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_co_nhan_19h30_246)
        self.__enroll('Anh', 'Nguyễn Thành Thoại', 'nguyenthanhthoaianh1@gmail.com', advanced_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_co_nhan_19h30_246[0:18])
        self.__enroll('Thi', 'Nguyễn Thị Anh', 'nguyenthianhthi1@gmail.com', advanced_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_co_nhan_19h30_246[0:18])
        self.__enroll('Thủy', 'Lê Thị', 'lethithuy1@gmail.com', advanced_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_co_nhan_19h30_246[0:18])
        self.__enroll('Hoa', 'Nguyễn Thị', 'nguyenthihoa1@gmail.com', advanced_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_co_nhan_19h30_246[0:18])
        self.__enroll('Tố', 'Lê Thị Linh', 'lethilinhto1@gmail.com', advanced_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_co_nhan_19h30_246[0:18])
        self.__enroll('Huệ', 'Đài Thị Tuyết', 'daithituyethue1@gmail.com', advanced_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_co_nhan_19h30_246[0:24])
        self.__enroll('Hương', 'Nguyễn Thu', 'nguyenthuhuong1@gmail.com', advanced_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_co_nhan_19h30_246[0:24])
        self.__enroll('Thảo', 'Lê Trương Phương', 'letruongphuongthao1@gmail.com', advanced_yoga_class_co_nhan_19h30_246,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_co_nhan_19h30_246[0:24])
        # end add-trainees

        t_6h = '06:00'
        t_7h = '07:00'
        basic_yoga_class_co_nhu_6h_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Như 6h sáng 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_nhu,
        )
        arr_lessons_basic_yoga_class_co_nhu_6h_357 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_nhu_6h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_6h,
                "end_time": t_7h
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_nhu_6h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_6h,
                "end_time": t_7h
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_nhu_6h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_6h,
                "end_time": t_7h
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_nhu_6h_357.append(l1)
            arr_lessons_basic_yoga_class_co_nhu_6h_357.append(l2)
            arr_lessons_basic_yoga_class_co_nhu_6h_357.append(l3)
        # add-trainees
        self.__enroll('My', 'Phạm Đỗ Trà', 'phamdotramy1@gmail.com', basic_yoga_class_co_nhu_6h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_6h_357[0:10])
        self.__enroll('Phương', 'Nguyễn Ngọc', 'nguyenngocphuong1@gmail.com', basic_yoga_class_co_nhu_6h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_6h_357[0:12])
        self.__enroll('Cảnh', 'Lê Thị', 'lethicanh1@gmail.com', basic_yoga_class_co_nhu_6h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_6h_357)
        self.__enroll('Nhiệm', 'Nguyễn Thị Bích', 'nguyenthibichnhiem1@gmail.com', basic_yoga_class_co_nhu_6h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_6h_357[0:18])
        self.__enroll('Hòe', 'Mai Thị', 'maithihoe1@gmail.com', basic_yoga_class_co_nhu_6h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_6h_357[0:18])
        self.__enroll('Hà', 'Lê Thị Cẩm', 'lethicamha1@gmail.com', basic_yoga_class_co_nhu_6h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_6h_357[0:18])
        self.__enroll('Mai', 'Dương Thị Tuyết', 'duongthituyetmai1@gmail.com', basic_yoga_class_co_nhu_6h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_6h_357[0:18])
        self.__enroll('Len', 'Nguyễn Thị', 'nguyenthilen1@gmail.com', basic_yoga_class_co_nhu_6h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_6h_357[0:18])
        self.__enroll('Xuân', 'Phan Thị Thanh', 'phanthithanhxuan1@gmail.com', basic_yoga_class_co_nhu_6h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_6h_357[0:24])
        self.__enroll('Hương', 'Nguyễn Thị', 'nguyenthihuong1@gmail.com', basic_yoga_class_co_nhu_6h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_6h_357[0:24])
        self.__enroll('Huyền', 'Hoàng Thị Hải', 'hoangthihaihuyen1@gmail.com', basic_yoga_class_co_nhu_6h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_nhu_6h_357[0:24])
        # end add-trainees

        advanced_yoga_class_thay_tien_6h_357 = advanced_yoga_course.classes.create(
            name='Lớp nâng cao thầy Tiến 6h sáng 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=thay_tien,
        )
        arr_lessons_advanced_yoga_class_thay_tien_6h_357 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = advanced_yoga_class_thay_tien_6h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_6h,
                "end_time": t_7h
            })
            l2 = advanced_yoga_class_thay_tien_6h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_6h,
                "end_time": t_7h
            })
            l3 = advanced_yoga_class_thay_tien_6h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_6h,
                "end_time": t_7h
            })
            arr_lessons_advanced_yoga_class_thay_tien_6h_357.append(l1)
            arr_lessons_advanced_yoga_class_thay_tien_6h_357.append(l2)
            arr_lessons_advanced_yoga_class_thay_tien_6h_357.append(l3)
        # add-trainees
        self.__enroll('Diệu', 'Đinh Thị', 'dinhthidieu1@gmail.com', advanced_yoga_class_thay_tien_6h_357,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_thay_tien_6h_357[0:10])
        self.__enroll('Chuyển', 'Ngô Thị', 'ngothichuyen1@gmail.com', advanced_yoga_class_thay_tien_6h_357,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_thay_tien_6h_357[0:12])
        self.__enroll('Ny', 'Tô Rô Ly', 'torolyny1@gmail.com', advanced_yoga_class_thay_tien_6h_357,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_thay_tien_6h_357)
        self.__enroll('Hoài', 'Đoàn Thị', 'doanthihoai1@gmail.com', advanced_yoga_class_thay_tien_6h_357,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_thay_tien_6h_357[0:18])
        self.__enroll('Chi', 'Nguyễn Thị Kim', 'nguyenthikimchi1@gmail.com', advanced_yoga_class_thay_tien_6h_357,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_thay_tien_6h_357[0:18])
        self.__enroll('Loan', 'Huỳnh Kim', 'huynhkimloan1@gmail.com', advanced_yoga_class_thay_tien_6h_357,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_thay_tien_6h_357[0:18])
        self.__enroll('Nguyên', 'Phạm Thị Thảo', 'phamthithaonguyen1@gmail.com', advanced_yoga_class_thay_tien_6h_357,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_thay_tien_6h_357[0:18])
        self.__enroll('Sương', 'Bùi Thị', 'buithisuong1@gmail.com', advanced_yoga_class_thay_tien_6h_357,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_thay_tien_6h_357[0:18])
        self.__enroll('Huyền', 'Nguyễn Thị Mộng', 'nguyenthimonghuyen1@gmail.com', advanced_yoga_class_thay_tien_6h_357,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_thay_tien_6h_357[0:24])
        self.__enroll('Trinh', 'Nguyễn Phạm Văn', 'nguyenphamvantrinh1@gmail.com', advanced_yoga_class_thay_tien_6h_357,
                      period_lessons_card_type, arr_lessons_advanced_yoga_class_thay_tien_6h_357[0:24])
        # end add-trainees

        t_9h = '09:00'
        t_10h = '10:00'
        basic_yoga_class_co_phuong_9h_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Phượng 9h sáng 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_phuong,
        )
        arr_lessons_basic_yoga_class_co_phuong_9h_357 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_phuong_9h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_9h,
                "end_time": t_10h
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_phuong_9h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_9h,
                "end_time": t_10h
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_phuong_9h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_9h,
                "end_time": t_10h
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_phuong_9h_357.append(l1)
            arr_lessons_basic_yoga_class_co_phuong_9h_357.append(l2)
            arr_lessons_basic_yoga_class_co_phuong_9h_357.append(l3)
        # add-trainees
        self.__enroll('Minh', 'Hoàng Cẩm', 'hoangcamminh1@gmail.com', basic_yoga_class_co_phuong_9h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_9h_357[0:10])
        self.__enroll('Cơ', 'Nguyễn Thiện', 'nguyenthienco1@gmail.com', basic_yoga_class_co_phuong_9h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_9h_357[0:12])
        self.__enroll('Hiền', 'Đoàn Minh', 'doanminhhien1@gmail.com', basic_yoga_class_co_phuong_9h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_9h_357)
        self.__enroll('Vi', 'Lê Thị Xuân', 'lethixuanvi1@gmail.com', basic_yoga_class_co_phuong_9h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_9h_357[0:18])
        self.__enroll('Diễm', 'Quách Thúy', 'quachthuydiem1@gmail.com', basic_yoga_class_co_phuong_9h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_9h_357[0:18])
        self.__enroll('Tiên', 'Phan Thị Mỹ', 'phanthimytien1@gmail.com', basic_yoga_class_co_phuong_9h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_9h_357[0:18])
        self.__enroll('Giang', 'Lê Hoàng', 'lehoanggiang1@gmail.com', basic_yoga_class_co_phuong_9h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_9h_357[0:18])
        self.__enroll('Út', 'Phạm Thị Thúy', 'phamthiutsuong1@gmail.com', basic_yoga_class_co_phuong_9h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_9h_357[0:18])
        # end add-trainees

        t_15h = '15:00'
        t_16h = '16:00'
        basic_yoga_class_co_thuy_15h_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Thúy 15h chiều 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_thuy,
        )
        arr_lessons_basic_yoga_class_co_thuy_15h_357 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_thuy_15h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_thuy_15h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_thuy_15h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_thuy_15h_357.append(l1)
            arr_lessons_basic_yoga_class_co_thuy_15h_357.append(l2)
            arr_lessons_basic_yoga_class_co_thuy_15h_357.append(l3)
        # add-trainees
        self.__enroll('Chánh', 'Nguyễn Thị', 'nguyenthichanh1@gmail.com', basic_yoga_class_co_thuy_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_15h_357[0:10])
        self.__enroll('Hạnh', 'Phạm Thị Ngọc', 'phamthingochanh1@gmail.com', basic_yoga_class_co_thuy_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_15h_357[0:12])
        self.__enroll('Hằng', 'Nguyễn Thị Minh', 'nguyenthiminhhang1@gmail.com', basic_yoga_class_co_thuy_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_15h_357)
        self.__enroll('Nương', 'Hồ Thị Xuân', 'hothixuannuong1@gmail.com', basic_yoga_class_co_thuy_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_15h_357[0:18])
        self.__enroll('Trang', 'Nguyễn Thị Quỳnh', 'nguyenthiquynhtrang1@gmail.com', basic_yoga_class_co_thuy_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_15h_357[0:18])
        self.__enroll('Diễm', 'Nguyễn Thị Bích', 'nguyenthibichdiem1@gmail.com', basic_yoga_class_co_thuy_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_15h_357[0:18])
        self.__enroll('Ca', 'Ngô Sơn', 'ngosonca1@gmail.com', basic_yoga_class_co_thuy_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_15h_357[0:18])
        self.__enroll('Tuyến', 'Lê Thị Kim', 'lethikimtuyen1@gmail.com', basic_yoga_class_co_thuy_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_15h_357[0:18])
        self.__enroll('Tư', 'Đoàn Thị', 'doanthitu1@gmail.com', basic_yoga_class_co_thuy_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_15h_357[0:18])
        self.__enroll('Thảo', 'Nguyễn Thị Thu', 'nguyenthithuthao1@gmail.com', basic_yoga_class_co_thuy_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_thuy_15h_357[0:18])
        # end add-trainees

        basic_yoga_class_co_quyen_15h_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Quyên 15h chiều 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_quyen,
        )
        arr_lessons_basic_yoga_class_co_quyen_15h_357 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_quyen_15h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_quyen_15h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_quyen_15h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_quyen_15h_357.append(l1)
            arr_lessons_basic_yoga_class_co_quyen_15h_357.append(l2)
            arr_lessons_basic_yoga_class_co_quyen_15h_357.append(l3)

        # add-trainees
        self.__enroll('Loan', 'Trần Thị Kim', 'tranthikimloan1@gmail.com', basic_yoga_class_co_quyen_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_quyen_15h_357[0:10])
        self.__enroll('Thảo', 'Lê Thị Phương', 'lethiphuongthao1@gmail.com', basic_yoga_class_co_quyen_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_quyen_15h_357[0:12])
        self.__enroll('Như', 'Nguyễn Thị Bảo', 'nguyenthibaonhu1@gmail.com', basic_yoga_class_co_quyen_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_quyen_15h_357)
        self.__enroll('Đức', 'Phan Bá', 'phabaduc1@gmail.com', basic_yoga_class_co_quyen_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_quyen_15h_357[0:18])
        self.__enroll('Hằng', 'Bùi Thị Thu', 'buithithuhang1@gmail.com', basic_yoga_class_co_quyen_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_quyen_15h_357[0:18])
        self.__enroll('Uyên', 'Nguyễn Như Thúy', 'nguyennhuthuyuyen1@gmail.com', basic_yoga_class_co_quyen_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_quyen_15h_357[0:18])
        self.__enroll('Dung', 'Trương Thị', 'truongthidung1@gmail.com', basic_yoga_class_co_quyen_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_quyen_15h_357[0:18])
        self.__enroll('Hạnh', 'Dương Thị Bích', 'duongthibichhanh1@gmail.com', basic_yoga_class_co_quyen_15h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_quyen_15h_357[0:18])
        # end add-trainees

        intermediate_yoga_class_thay_tan_15h_357 = intermediate_yoga_course.classes.create(
            name='Lớp trung cấp thầy Tân 15h chiều 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=thay_tan,
        )
        arr_lessons_intermediate_yoga_class_thay_tan_15h_357 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = intermediate_yoga_class_thay_tan_15h_357.lessons.create(**{
                "room_id": room3.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            l2 = intermediate_yoga_class_thay_tan_15h_357.lessons.create(**{
                "room_id": room3.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            l3 = intermediate_yoga_class_thay_tan_15h_357.lessons.create(**{
                "room_id": room3.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_15h,
                "end_time": t_16h
            })
            arr_lessons_intermediate_yoga_class_thay_tan_15h_357.append(l1)
            arr_lessons_intermediate_yoga_class_thay_tan_15h_357.append(l2)
            arr_lessons_intermediate_yoga_class_thay_tan_15h_357.append(l3)
        # add-trainees
        self.__enroll('Hồng', 'Nguyễn Thị Tuyết', 'nguyenthituyethong1@gmail.com', intermediate_yoga_class_thay_tan_15h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_tan_15h_357[0:10])
        self.__enroll('Bích', 'Nguyễn Thị', 'nguyenthibich1@gmail.com', intermediate_yoga_class_thay_tan_15h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_tan_15h_357[0:12])
        self.__enroll('Uyên', 'Nguyễn Tú', 'nguyentuuyen1@gmail.com', intermediate_yoga_class_thay_tan_15h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_tan_15h_357)
        self.__enroll('Cúc', 'Nguyễn Thị Kim', 'nguyenthikimcuc1@gmail.com', intermediate_yoga_class_thay_tan_15h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_tan_15h_357[0:18])
        self.__enroll('Hiếu', 'Trần Thị Thu', 'tranthithuhieu1@gmail.com', intermediate_yoga_class_thay_tan_15h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_tan_15h_357[0:18])
        self.__enroll('Phúc', 'Võ Thị Hồng', 'vothihongphuc1@gmail.com', intermediate_yoga_class_thay_tan_15h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_tan_15h_357[0:18])
        self.__enroll('Ngân', 'Lý Thị Kim', 'lythikimngan1@gmail.com', intermediate_yoga_class_thay_tan_15h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_tan_15h_357[0:18])
        self.__enroll('Huệ', 'Phạm Thị Minh', 'phamthiminhhue1@gmail.com', intermediate_yoga_class_thay_tan_15h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_tan_15h_357[0:18])
        self.__enroll('Trúc', 'Bùi Nguyễn Bảo', 'buinguyenbaotruc1@gmail.com', intermediate_yoga_class_thay_tan_15h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_tan_15h_357[0:18])
        self.__enroll('Nga', 'Trần Thị', 'tranthinga1@gmail.com', intermediate_yoga_class_thay_tan_15h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_tan_15h_357[0:18])
        self.__enroll('Dung', 'Trương Thị Thùy', 'truongthithuydung1@gmail.com', intermediate_yoga_class_thay_tan_15h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_tan_15h_357[0:18])
        # end add-trainees

        t_17h = '17:00'
        t_18h = '18:00'
        intermediate_yoga_class_thay_thien_17h_357 = intermediate_yoga_course.classes.create(
            name='Lớp trung cấp thầy Thiên 17h chiều 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=thay_thien,
        )
        arr_lessons_intermediate_yoga_class_thay_thien_17h_357 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = intermediate_yoga_class_thay_thien_17h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })
            l2 = intermediate_yoga_class_thay_thien_17h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })
            l3 = intermediate_yoga_class_thay_thien_17h_357.lessons.create(**{
                "room_id": room1.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })
            arr_lessons_intermediate_yoga_class_thay_thien_17h_357.append(l1)
            arr_lessons_intermediate_yoga_class_thay_thien_17h_357.append(l2)
            arr_lessons_intermediate_yoga_class_thay_thien_17h_357.append(l3)
        # add-trainees
        self.__enroll('Dung', 'Hồ Thị Phương', 'hothiphuongdung1@gmail.com', intermediate_yoga_class_thay_thien_17h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_thien_17h_357[0:10])
        self.__enroll('Anh', 'Nguyễn Thị Vân', 'nguyenthivananh1@gmail.com', intermediate_yoga_class_thay_thien_17h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_thien_17h_357[0:12])
        self.__enroll('Ngân', 'Văn Thu', 'vanthungan1@gmail.com', intermediate_yoga_class_thay_thien_17h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_thien_17h_357)
        self.__enroll('Phương', 'Phạm Thị Thùy', 'phamthithuyphuong1@gmail.com', intermediate_yoga_class_thay_thien_17h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_thien_17h_357[0:18])
        self.__enroll('Thảo', 'Nguyễn Mai Hiếu', 'nguyenmaihieuthao1@gmail.com', intermediate_yoga_class_thay_thien_17h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_thien_17h_357[0:18])
        self.__enroll('Chi', 'Nguyễn Thị Diệu', 'nguyenthidieuchi1@gmail.com', intermediate_yoga_class_thay_thien_17h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_thien_17h_357[0:18])
        self.__enroll('Mai', 'Nguyễn Thị Tuyết', 'nguyenthituyetmai1@gmail.com', intermediate_yoga_class_thay_thien_17h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_thien_17h_357[0:18])
        self.__enroll('Mai', 'Vũ Hồng Sao', 'vuhongsaomai1@gmail.com', intermediate_yoga_class_thay_thien_17h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_thien_17h_357[0:18])
        self.__enroll('Thảo', 'Đặng Phương', 'dangphuongthao1@gmail.com', intermediate_yoga_class_thay_thien_17h_357,
                      period_lessons_card_type, arr_lessons_intermediate_yoga_class_thay_thien_17h_357[0:18])
        # end add-trainees

        basic_yoga_class_co_kieu_17h_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Kiều 17h chiều 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_kieu,
        )
        arr_lessons_basic_yoga_class_co_kieu_17h_357 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_kieu_17h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_kieu_17h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_kieu_17h_357.lessons.create(**{
                "room_id": room2.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_17h,
                "end_time": t_18h
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_kieu_17h_357.append(l1)
            arr_lessons_basic_yoga_class_co_kieu_17h_357.append(l2)
            arr_lessons_basic_yoga_class_co_kieu_17h_357.append(l3)
        # add-trainees
        self.__enroll('Nga', 'Nguyễn Hồng Bích', 'nguyenhongbichnga1@gmail.com', basic_yoga_class_co_kieu_17h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h_357[0:10])
        self.__enroll('Phương', 'Trần Thị Hoài', 'tranthihoaiphuong1@gmail.com', basic_yoga_class_co_kieu_17h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h_357[0:12])
        self.__enroll('Trân', 'Nguyễn Bảo', 'nguyenbaotran1@gmail.com', basic_yoga_class_co_kieu_17h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h_357)
        self.__enroll('Anh', 'Nguyễn Phan', 'nguyenphananh1@gmail.com', basic_yoga_class_co_kieu_17h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h_357[0:18])
        self.__enroll('Hương', 'Nguyễn Thị Thu', 'nguyenthithuhuong1@gmail.com', basic_yoga_class_co_kieu_17h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h_357[0:18])
        self.__enroll('Vân', 'Chu Thị', 'chuthivan1@gmail.com', basic_yoga_class_co_kieu_17h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h_357[0:18])
        self.__enroll('Khai', 'Đàm Thị', 'damthikhai1@gmail.com', basic_yoga_class_co_kieu_17h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h_357[0:18])
        self.__enroll('Hân', 'Lê Ngọc', 'lengochan1@gmail.com', basic_yoga_class_co_kieu_17h_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_kieu_17h_357[0:18])
        # end add-trainees

        t_16h30 = '16:30'
        t_17h30 = '17:30'
        basic_yoga_class_co_tra_my_16h30_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Trà My 16h30 chiều 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_tra_my,
        )
        arr_lessons_basic_yoga_class_co_tra_my_16h30_357 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_tra_my_16h30_357.lessons.create(**{
                "room_id": room3.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_16h30,
                "end_time": t_17h30
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_tra_my_16h30_357.lessons.create(**{
                "room_id": room3.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_16h30,
                "end_time": t_17h30
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_tra_my_16h30_357.lessons.create(**{
                "room_id": room3.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_16h30,
                "end_time": t_17h30
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_tra_my_16h30_357.append(l1)
            arr_lessons_basic_yoga_class_co_tra_my_16h30_357.append(l2)
            arr_lessons_basic_yoga_class_co_tra_my_16h30_357.append(l3)
        # add-trainees
        self.__enroll('An', 'Lê Thị Vân', 'lethivanan1@gmail.com', basic_yoga_class_co_tra_my_16h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_tra_my_16h30_357[0:10])
        self.__enroll('Tiên', 'Vũ Thủy', 'vuthuytien1@gmail.com', basic_yoga_class_co_tra_my_16h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_tra_my_16h30_357[0:12])
        self.__enroll('Lụa', 'Trần Thị', 'tranthilua1@gmail.com', basic_yoga_class_co_tra_my_16h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_tra_my_16h30_357)
        self.__enroll('Hà', 'Phạm Thị Bích', 'phamthibichha1@gmail.com', basic_yoga_class_co_tra_my_16h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_tra_my_16h30_357[0:18])
        self.__enroll('Phước', 'Võ Thị Hồng', 'vothihongphuoc1@gmail.com', basic_yoga_class_co_tra_my_16h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_tra_my_16h30_357[0:18])
        self.__enroll('Châu', 'Vũ Thị Minh', 'vuthiminhchau1@gmail.com', basic_yoga_class_co_tra_my_16h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_tra_my_16h30_357[0:18])
        self.__enroll('Tuyết', 'Nguyễn Thu Hồng', 'nguyenthuhongtuyet1@gmail.com', basic_yoga_class_co_tra_my_16h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_tra_my_16h30_357[0:18])
        self.__enroll('Ngọc', 'Lê Thị Hoàng', 'lethihoangngoc1@gmail.com', basic_yoga_class_co_tra_my_16h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_tra_my_16h30_357[0:18])
        # end add-trainees

        basic_yoga_class_co_phuong_17h30_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Phượng 17h30 chiều 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_phuong,
        )
        arr_lessons_basic_yoga_class_co_phuong_17h30_357 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_phuong_17h30_357.lessons.create(**{
                "room_id": room4.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_17h30,
                "end_time": t_18h30
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_phuong_17h30_357.lessons.create(**{
                "room_id": room4.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_17h30,
                "end_time": t_18h30
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_phuong_17h30_357.lessons.create(**{
                "room_id": room4.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_17h30,
                "end_time": t_18h30
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_phuong_17h30_357.append(l1)
            arr_lessons_basic_yoga_class_co_phuong_17h30_357.append(l2)
            arr_lessons_basic_yoga_class_co_phuong_17h30_357.append(l3)
        # add-trainees
        self.__enroll('Quyên', 'Nguyễn Vũ Ngọc', 'nguyenvungocquyen1@gmail.com', basic_yoga_class_co_phuong_17h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_17h30_357[0:10])
        self.__enroll('Huyền', 'Trương Thị Ngọc', 'truongthingochuyen1@gmail.com', basic_yoga_class_co_phuong_17h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_17h30_357[0:12])
        self.__enroll('Hân', 'Trần Thị Ngọc', 'tranthingochan1@gmail.com', basic_yoga_class_co_phuong_17h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_17h30_357)
        self.__enroll('Hùng', 'Nguyễn Xuân', 'nguyenxuanhung1@gmail.com', basic_yoga_class_co_phuong_17h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_17h30_357[0:18])
        self.__enroll('Anh', 'Lê Tuyết', 'letuyetanh1@gmail.com', basic_yoga_class_co_phuong_17h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_17h30_357[0:18])
        self.__enroll('Huy', 'Nguyễn Đoàn', 'nguyendoanhuy1@gmail.com', basic_yoga_class_co_phuong_17h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_17h30_357[0:18])
        self.__enroll('Hiền', 'Nguyễn Thị', 'nguyenthihien1@gmail.com', basic_yoga_class_co_phuong_17h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_17h30_357[0:18])
        self.__enroll('Liễu', 'Lê Thị Bích', 'lethibichlieu1@gmail.com', basic_yoga_class_co_phuong_17h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_17h30_357[0:18])
        self.__enroll('Trúc', 'Nguyễn Thanh', 'nguyenthanhtruc1@gmail.com', basic_yoga_class_co_phuong_17h30_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_phuong_17h30_357[0:18])
        # end add-trainees

        basic_yoga_class_co_vo_hanh_18h15_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Võ Hạnh 18h15 tối 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_vo_hanh,
        )
        arr_lessons_basic_yoga_class_co_vo_hanh_18h15_357 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_vo_hanh_18h15_357.lessons.create(**{
                "room_id": room1.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_vo_hanh_18h15_357.lessons.create(**{
                "room_id": room1.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_vo_hanh_18h15_357.lessons.create(**{
                "room_id": room1.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_vo_hanh_18h15_357.append(l1)
            arr_lessons_basic_yoga_class_co_vo_hanh_18h15_357.append(l2)
            arr_lessons_basic_yoga_class_co_vo_hanh_18h15_357.append(l3)
        # add-trainees
        self.__enroll('Tâm', 'Nguyễn Ngọc', 'nguyenngoctam1@gmail.com', basic_yoga_class_co_vo_hanh_18h15_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_18h15_357[0:10])
        self.__enroll('Yến', 'Võ Thị Thu', 'vothithuyen1@gmail.com', basic_yoga_class_co_vo_hanh_18h15_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_18h15_357[0:12])
        self.__enroll('Hoa', 'Hoàng Thị Thanh', 'hoangthithanhhoa1@gmail.com', basic_yoga_class_co_vo_hanh_18h15_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_18h15_357)
        self.__enroll('Huệ', 'Lê Thị', 'lethihue1@gmail.com', basic_yoga_class_co_vo_hanh_18h15_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_18h15_357[0:18])
        self.__enroll('Đạt', 'Đinh Phước', 'dinhphuocdat1@gmail.com', basic_yoga_class_co_vo_hanh_18h15_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_18h15_357[0:18])
        self.__enroll('Phượng', 'Đào Thị Thúy', 'daothithuyphuong1@gmail.com', basic_yoga_class_co_vo_hanh_18h15_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_18h15_357[0:18])
        self.__enroll('Tùng', 'Phạm Thị Kim', 'phamthikimtung1@gmail.com', basic_yoga_class_co_vo_hanh_18h15_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_18h15_357[0:18])
        self.__enroll('Trang', 'Nguyễn Thị Diễm', 'nguyenthidiemtrang1@gmail.com', basic_yoga_class_co_vo_hanh_18h15_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_18h15_357[0:18])
        # end add-trainees

        basic_yoga_class_co_man_18h15_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Mận 18h15 tối 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_man,
        )
        arr_lessons_basic_yoga_class_co_man_18h15_357 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_man_18h15_357.lessons.create(**{
                "room_id": room2.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_man_18h15_357.lessons.create(**{
                "room_id": room2.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_man_18h15_357.lessons.create(**{
                "room_id": room2.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_18h15,
                "end_time": t_19h15
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_man_18h15_357.append(l1)
            arr_lessons_basic_yoga_class_co_man_18h15_357.append(l2)
            arr_lessons_basic_yoga_class_co_man_18h15_357.append(l3)
        # add-trainees
        self.__enroll('Sang', 'Lữ Đình', 'ludinhsang1@gmail.com', basic_yoga_class_co_man_18h15_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_18h15_357[0:10])
        self.__enroll('Trâm', 'Lê Thị Ngọc', 'lethingoctram1@gmail.com', basic_yoga_class_co_man_18h15_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_18h15_357[0:12])
        self.__enroll('Ngọc', 'Trần Bích', 'tranbichngoc1@gmail.com', basic_yoga_class_co_man_18h15_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_18h15_357)
        self.__enroll('Ngân', 'Trần Thị Tuyết', 'tranthituyetngan1@gmail.com', basic_yoga_class_co_man_18h15_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_18h15_357[0:18])
        self.__enroll('Hiền', 'Vũ Thị', 'vuthihien1@gmail.com', basic_yoga_class_co_man_18h15_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_18h15_357[0:18])
        self.__enroll('Hằng', 'Vũ Thị', 'vuthihang1@gmail.com', basic_yoga_class_co_man_18h15_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_18h15_357[0:18])
        self.__enroll('Hường', 'Vũ Thị', 'vuthihuong1@gmail.com', basic_yoga_class_co_man_18h15_357,
                      period_lessons_card_type, arr_lessons_basic_yoga_class_co_man_18h15_357[0:18])
        # end add-trainees

        basic_yoga_class_co_vo_hanh_19h30_357 = basic_yoga_course.classes.create(
            name='Lớp cơ bản cô Võ Hạnh 19h30 tối 3-5-7',
            price_per_lesson=50000,
            price_per_month=600000,
            trainer=co_vo_hanh,
        )
        arr_lessons_basic_yoga_class_co_vo_hanh_19h30_357 = []
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            l1 = basic_yoga_class_co_vo_hanh_19h30_357.lessons.create(**{
                "room_id": room4.pk,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l1.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2 = basic_yoga_class_co_vo_hanh_19h30_357.lessons.create(**{
                "room_id": room4.pk,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l2.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3 = basic_yoga_class_co_vo_hanh_19h30_357.lessons.create(**{
                "room_id": room4.pk,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t_19h30,
                "end_time": t_20h30
            })
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            l3.lectures.add(basic_yoga_course_lectures[randint(
                0, basic_yoga_course_lectures_count - 1)])
            arr_lessons_basic_yoga_class_co_vo_hanh_19h30_357.append(l1)
            arr_lessons_basic_yoga_class_co_vo_hanh_19h30_357.append(l2)
            arr_lessons_basic_yoga_class_co_vo_hanh_19h30_357.append(l3)
        # add-trainees
        self.__enroll('Hằng', 'Trần Thị Thu', 'tranthithuhang1@gmail.com', basic_yoga_class_co_vo_hanh_19h30_357,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_19h30_357[0:10])
        self.__enroll('Yên', 'Hồng Ngọc', 'hongngocyen1@gmail.com', basic_yoga_class_co_vo_hanh_19h30_357,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_19h30_357[0:12])
        self.__enroll('Ánh', 'Võ Thị Ngọc', 'vothingocanh1@gmail.com', basic_yoga_class_co_vo_hanh_19h30_357,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_19h30_357)
        self.__enroll('Nguyên', 'Nguyễn Thị', 'nguyenthinguyen1@gmail.com', basic_yoga_class_co_vo_hanh_19h30_357,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_19h30_357[0:18])
        self.__enroll('Thủy', 'Bùi Thị Thu', 'buithithuthuy1@gmail.com', basic_yoga_class_co_vo_hanh_19h30_357,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_19h30_357[0:18])
        self.__enroll('Hoa', 'Trần Thị Kim', 'tranthikimhoa1@gmail.com', basic_yoga_class_co_vo_hanh_19h30_357,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_19h30_357[0:18])
        self.__enroll('Sang', 'Vương Bội', 'vuongboisang1@gmail.com', basic_yoga_class_co_vo_hanh_19h30_357,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_19h30_357[0:18])
        self.__enroll('Thúy', 'Nguyễn Ngọc', 'nguyenngocthuy1@gmail.com', basic_yoga_class_co_vo_hanh_19h30_357,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_19h30_357[0:18])
        self.__enroll('Tuyền', 'Nguyễn Ngọc Phương', 'nguyenngocphuongtuyen1@gmail.com', basic_yoga_class_co_vo_hanh_19h30_357,
                      some_lessons_card_type, arr_lessons_basic_yoga_class_co_vo_hanh_19h30_357[0:18])
        # end add-trainees

        # TRAINING CLASS
        t_21h = '21:00'
        training_class_thay_hoang_anh = training_yoga_trainer_course.classes.create(
            name='Lớp đào tạo thầy Hoàng Anh 18h tối thứ 7',
            price_for_training_class=15000000,
            start_at=saturday + timedelta(days=14),
            trainer=thay_hoang_anh,
        )
        for i in range(0, 12):
            count_date = 7 * i + 14
            training_class_thay_hoang_anh.lessons.create(**{
                "room_id": room3.pk,
                "date": saturday + timedelta(days=count_date),
                "start_time": t_18h,
                "end_time": t_21h
            })
        training_class_thay_hoang_anh.payment_periods.create(**{
            'name': 'Đợt thanh toán 1',
            'amount': 7500000,
            'end_at': saturday + timedelta(days=14)
        })
        training_class_thay_hoang_anh.payment_periods.create(**{
            'name': 'Đợt thanh toán 2',
            'amount': 7500000,
            'end_at': saturday + timedelta(days=(14 + 7*7))
        })

    def __add_basic_lectures(self, course):
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

    def __add_training_lectures(self, course):
        data = [
            {
                'name': 'Lý thuyết & thực hành: Chuyên đề 1: Kiến thức tổng quát về yoga.',
            },
            {
                'name': 'Lý thuyết & thực hành: Chuyên đề 2: Giải phẫu học cơ thể người.',
            },
            {
                'name': 'Lý thuyết & thực hành: Chuyên đề 3: Luân xa – Các trung tâm năng lượng.',
            },
            {
                'name': 'Lý thuyết & thực hành: Chuyên đề 4: Thiền định – Tư duy tích cực.',
            },
            {
                'name': 'Lý thuyết & thực hành: Chuyên đề 5: Hệ thống và chi tiết các phép thở.',
            },
            {
                'name': 'Lý thuyết & thực hành: Chuyên đề 6: Hệ thống và cách vận hành các asana cơ bản (theo bộ, theo nhóm).',
            },
            {
                'name': 'Lý thuyết & thực hành: Chuyên đề 7: Phương pháp thực hành Asana Yoga nâng cao (Theo nhóm tư thế và theo nhu cầu).',
            },
            {
                'name': 'Lý thuyết & thực hành: Chuyên đề 8: Kỹ năng soạn giáo trình căn bản, trung cấp, nâng cao.',
            },
            {
                'name': 'Lý thuyết & thực hành: Chuyên đề 9: Kỹ năng chỉnh sửa, chấn thương, phòng ngừa và cách xử lý.',
            },
            {
                'name': 'Lý thuyết & thực hành: Chuyên đề 10: Kĩ năng đứng lớp.',
            },
            {
                'name': 'Thực hành: Chuyên đề: Gân khớp.',
            },
            {
                'name': 'Thực hành: Chuyên đề: Thể lực.',
            },
            {
                'name': 'Thực hành: Chuyên đề: Thăng bằng.',
            },
            {
                'name': 'Thực hành: Chuyên đề: Độ dẻo.',
            },
            {
                'name': 'Tham gia trợ giảng.',
            },
            {
                'name': 'Tập đứng lớp giảng dạy.',
            },
            {
                'name': 'Thi cuối khóa: Gồm thi lý thuyết và thực hành.',
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
        if card_type.form_of_using == FOR_SOME_LESSONS:
            amount = lesson_arr.__len__() * yoga_class.price_per_lesson * card_type.multiplier
        elif card_type.form_of_using == FOR_PERIOD_TIME_LESSONS:
            amount = lesson_arr.__len__() * yoga_class.price_per_lesson
        CardInvoiceService(card, PREPAID, 'Thanh toán thẻ tập',
                           amount, str(uuid.uuid4())).call()
        RollCallService(card, lesson_arr).call()

    def __create_admin(self):
        data = {
            'email': 'admin@admin.com',
            'first_name': 'Grey',
            'last_name': 'Tran'
        }
        admin = User(**data)
        admin.set_password('truong77')
        admin.is_superuser = True
        admin.save()

    def __create_staffs(self):
        fake = Faker()
        number_of_staff = 5
        for i in range(1, int(number_of_staff)):
            data = {
                'email': 'staff' + str(i) + '@gmail.com',
                'first_name': fake.first_name(),
                'last_name': fake.last_name()
            }
            staff = User(**data)
            staff.set_password('truong77')
            staff.is_staff = True
            staff.save()
            Staff.objects.create(user=staff)

    def __create_blog(self):
        print("Create post categories")
        category1 = PostCategory.objects.create(name='Yoga và đời sống')
        category2 = PostCategory.objects.create(name='Yêu thương và chia sẻ')
        print("Create posts")
        data = {
            'category': category1,
            'image': 'seeds/blog/yoga-mang-lai-su-tinh-tam.jpg',
            'title': 'Yoga mang lại sự tịnh tâm, cân bằng',
            'description': 'Tập Yoga giúp tăng cường máu lên não, điều hóa, mang lại sự cân bằng, thoải mái tinh thần',
            'content': '''<ul><li>Giải toả căng thẳng v&agrave; mệt mỏi cải thiện giấc ngủ</li><li>Tăng cường sự hoạt b&aacute;t của cơ thể</li><li>Ph&aacute;t triển tr&iacute; tuệ;</li><li>Tăng cường &yacute; ch&iacute; sự tự tin</li><li>Đạt được sự tĩnh t&acirc;m</li><li>Ph&aacute;t triển một lối sống lạc quan h&agrave;i h&ograve;a với m&ocirc;i trường xung quanh</li></ul><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/yoga-va-doi-song-7.jpg" style="height:452px; width:603px" /></p><p>Yoga c&oacute; nhiều b&agrave;i tập thiền, tập thở, tập thể dục th&ocirc;ng qua việc điều chỉnh Kh&iacute; của cơ thể đ&ograve;i hỏi người tập phải thực sự tĩnh t&acirc;m, nhập t&acirc;m v&agrave;o những &acirc;m thanh thư gi&atilde;n, lắng nghe cơ thể từ đ&oacute; qu&ecirc;n hết muộn phiền lo &acirc;u. Những giờ ph&uacute;t tập thiền, hoặc ch&uacute; t&acirc;m v&agrave;o việc điều khiển hơi thở sẽ khiến cơ thể được thăng hoa, n&acirc;ng cao năng lực của tr&iacute; tuệ, nắm bắt được quy lu&acirc;t của sự sống, t&igrave;m được cội nguồn gi&aacute; trị của cuộc đời từ đ&oacute; sống l&agrave;nh mạnh, an h&ograve;a v&agrave; thư th&aacute;i hơn.</p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/yoga-va-doi-song-e1500981544866.jpg" style="height:338px; width:600px" /></p><p>Rất nhiều lợi &iacute;ch của Yoga đ&atilde; được chứng minh bởi h&agrave;ng triệu người luyện tập tr&ecirc;n to&agrave;n thế giới. Người th&agrave;nh đạt, gi&agrave;u c&oacute; ở đỉnh cao của x&atilde; hội t&igrave;m đến Yoga để c&acirc;n bằng v&agrave; g&igrave;n giữ lối sống l&agrave;nh mạnh. Người gặp nhiều stress v&agrave; c&aacute;c vấn đề về sức khỏe t&igrave;m đến Yoga để được thanh lọc cả cơ thể v&agrave; t&acirc;m hồn. Người b&eacute;o, người gầy, người ốm yếu, đ&agrave;n &ocirc;ng, đ&agrave;n b&agrave;, người gi&agrave;, người trẻ t&igrave;m đến Yoga để luyện tập cho m&igrave;nh một h&igrave;nh thể khỏe mạnh, dẻo dai v&agrave; t&acirc;m hồn thư th&aacute;i, tr&iacute; tuệ anh minh.</p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/yoga-la-phuong-thuoc-cho-su-lo-lang-va-tram-cam-1.jpg" style="height:337px; width:598px" /></p><p><strong>Đ&oacute; l&agrave; sự kỳ diệu của Yoga! H&atilde;y tập Yoga để ho&agrave;n thiện vẻ đẹp h&igrave;nh thể, chăm s&oacute;c t&acirc;m hồn v&agrave; tận hưởng cuộc sống trọn vẹn hơn!</strong></p>''',
        }
        Post.objects.create(**data)

        data2 = {
            'category': category2,
            'image': 'seeds/blog/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong.jpg',
            'title': 'Ngày chủ nhật yêu thương',
            'description': 'CLB đã thực hiện giúp đỡ, trao yêu thương cho những hoàn cảnh khó khăn',
            'content': '''<p>Đo&agrave;n Yoga Hương Tre đ&atilde; trao tận tay 150 phần qu&agrave; đến b&agrave; con ngh&egrave;o nhiểm chất độc m&agrave;u da cam v&agrave; khiếm thị tại Định Qu&aacute;n &ndash; Đồng Nai.</p><ul>	<li>🙏Cảm ơn qu&yacute; mạnh thường qu&acirc;n trong v&agrave; ngo&agrave;i CLB đ&atilde; y&ecirc;u thương v&agrave; t&iacute;n nhiệm.</li>	<li>🙏&nbsp;Cảm ơn qu&yacute; học vi&ecirc;n, gi&aacute;o vi&ecirc;n, bạn b&egrave; ,&hellip; c&ugrave;ng tham gia gi&uacute;p c&ocirc;ng t&aacute;c ph&aacute;t qu&agrave; cho b&agrave; con khuyết tật v&agrave; khiếm thị diễn ra dễ d&agrave;ng hơn, phụ gi&uacute;p ph&acirc;n qu&agrave;, phụ gi&uacute;p bưng b&ecirc; qu&agrave;. CLB rất tr&acirc;n qu&yacute; t&igrave;nh cảm đ&oacute; của cả nh&agrave;.</li>	<li>🙏CLB cảm ơn Thầy Nguy&ecirc;n Tấn &ndash; ch&ugrave;a Từ T&acirc;n, đ&atilde; c&ugrave;ng Đo&agrave;n gieo duy&ecirc;n trong chuyến từ thiện n&agrave;y, đ&oacute; l&agrave; điều may mắn cho CLB v&agrave; cho cả Đo&agrave;n.</li>	<li>🙏&nbsp;CLB cảm ơn c&ocirc; quỹ H&agrave; Ngọc ( c&ocirc; Hồng ) g&oacute;p phần quan trọng gi&uacute;p chuyến đi thiện nguyện được ho&agrave;n th&agrave;nh tốt đẹp, từ kh&acirc;u k&ecirc;u gọi mạnh thường qu&acirc;n, lo xe cộ, qu&agrave; cho b&agrave; con, lo ăn uống cho cả đo&agrave;n.CLB biết ơn tấm l&ograve;ng của c&ocirc; rất nhiều.</li><li>🙏&nbsp;Cảm ơn những lời động vi&ecirc;n, khuyến kh&iacute;ch từ học vi&ecirc;n , gi&aacute;o vi&ecirc;n,bạn b&egrave; gần xa, &hellip;gi&uacute;p cho CLB c&oacute; động lực tổ chức những chiến thiện nguyện &yacute; nghĩa tiếp theo.</li>	<li>🙏Cảm ơn Mẹ thi&ecirc;n nhi&ecirc;n đ&atilde; ban cho Suối Mơ vẻ đẹp thơ mộng đ&uacute;ng như t&ecirc;n gọi, Đo&agrave;n c&oacute; dịp tắm suối m&aacute;t v&agrave; lưu lại những h&igrave;nh ảnh kỷ niệm đẹp.</li>	<li>🙏&nbsp;Ch&uacute;c cả nh&agrave; lu&ocirc;n b&igrave;nh an, khỏe mạnh v&agrave; hạnh ph&uacute;c.</li></ul><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong.jpg" style="height:497px; width:750px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-1.jpg" style="height:563px; width:751px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-2.png" style="height:417px; width:751px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-3.png" style="height:629px; width:750px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-4.jpg" style="height:629px; width:750px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-5.jpg" style="height:629px; width:750px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-6.jpg" style="height:960px; width:412px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-7.jpg" style="height:960px; width:720px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-8.jpg" style="height:563px; width:751px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-9.jpg" style="height:562px; width:749px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-10.jpg" style="height:960px; width:720px" /></p>''',
        }
        Post.objects.create(**data2)

        data3 = {
            'category': category1,
            'image': 'seeds/blog/thuat_ngu_trong_yoga.jpg',
            'title': 'Thuật ngữ trong Yoga',
            'description': 'Nếu bạn là một tín đồ của môn Yoga, ắt hẳn bạn sẽ nghe các thuật ngữ như "Yoga", "Namaste", "Om".. thường xuyên. Nhưng liệu bạn có biết rõ ý nghĩa các thuật ngữ quen thuộc của môn yoga ấy là gì và xuất xứ của chúng từ đâu?',
            'content': '''<h3>🌟&nbsp;YOGA</h3><p>Ch&uacute;ng ta đều biết rằng yoga l&agrave; sự kết hợp của cơ thể, t&acirc;m tr&iacute; v&agrave; tinh thần. Đ&oacute; l&agrave; sự thực h&agrave;nh kết nối v&agrave; c&oacute; nghĩa l&agrave; nhiều hơn thế nữa. L&agrave; kết nối với ch&iacute;nh m&igrave;nh, kết nối với nhau, với m&ocirc;i trường sống chung quanh ta v&agrave; cuối c&ugrave;ng &ndash; kết nối với sự thật.<br />Mỗi ch&uacute;ng ta đều được ban phước với vẻ đẹp, h&ograve;a b&igrave;nh, t&igrave;nh y&ecirc;u v&agrave; &aacute;nh s&aacute;ng.</p><p>Đ&acirc;y l&agrave; thuật ngữ quen thuộc nhất đấy nh&eacute;. &ldquo;Yoga&rdquo; trong tiếng Phạn c&oacute; nghĩa l&agrave; Yuj với &yacute; nghĩa l&agrave; sự r&agrave;ng buộc hoặc gắn kết, v&agrave; thường được hiểu l&agrave; &ldquo;sự li&ecirc;n kết&rdquo; hoặc một phương ph&aacute;p c&oacute; t&iacute;nh kỷ luật. Một người tập yoga l&agrave; nam sẽ được gọi l&agrave; &ldquo;Yogi&rdquo; c&ograve;n nữ tập Yoga sẽ được gọi l&agrave; Yogini. Thực tế, yoga bao gồm 8 nh&aacute;nh: Yama (5 đạo l&yacute; khi đối xử với người kh&aacute;c), Niyama (5 đạo l&yacute; của ch&iacute;nh bản th&acirc;n m&igrave;nh), Asana (Thực h&agrave;nh c&aacute;c tư thế Yoga), Pranayama (Luyện thở &ndash; kiểm so&aacute;t nguồn sinh lực), Pratyahara (Từ bỏ cảm x&uacute;c, c&oacute; nghĩa l&agrave; thế giới b&ecirc;n ngo&agrave;i kh&ocirc;ng ảnh hưởng đến thế giới b&ecirc;n trong người tập Yoga), Dharana (Sự tập trung, c&oacute; nghĩa l&agrave; khả năng tập trung v&agrave;o một việc g&igrave; đ&oacute; kh&ocirc;ng bị đứt qu&atilde;ng bởi sự sao nh&atilde;ng ở trong hay ngo&agrave;i), Dhyana (Thiền định. Dựa tr&ecirc;n Dharana, sự tập trung kh&ocirc;ng c&ograve;n bị giới hạn ở một sự việc n&agrave;o đ&oacute; nữa m&agrave; l&agrave; bao tr&ugrave;m tất cả), Samadhi (Trạng th&aacute;i ph&uacute;c lạc. Dựa tr&ecirc;n Dhyana, sự si&ecirc;u nghiệm của bản th&acirc;n qua thiền định. Sự hợp nhất bản th&acirc;n với vũ trụ). Ng&agrave;y nay hầu hết những người thực h&agrave;nh yoga đều tham gia v&agrave;o nh&aacute;nh thứ ba, asana, l&agrave; c&aacute;c b&agrave;i tập c&oacute; t&aacute;c dụng thanh lọc cơ thể v&agrave; cung cấp sức mạnh thể chất, sự dẻo dai.</p><h3>🌟&nbsp;NAMASTE</h3><p>Bắt nguồn từ tiếng Phạn, &lsquo;Namaste&rsquo; l&agrave; một điệu bộ chấp hai l&ograve;ng b&agrave;n tay trước ngực v&agrave; cuối đầu ch&agrave;o trước khi bắt đầu v&agrave; khi kết th&uacute;c lớp yoga. Sự chấp hai l&ograve;ng b&agrave;n tay thể hiện rằng trong mỗi ch&uacute;ng ta điều c&oacute; một niềm tin thi&ecirc;ng li&ecirc;ng từ trong t&acirc;m v&agrave; điều n&agrave;y được t&igrave;m ẩn ở lu&acirc;n xa thứ 4 ( con tim). Điệu bộ l&agrave; một cảm nhận của một linh hồn đối với một linh hồn kh&aacute;c.</p><p><img alt="nhung-thuat-ngu-trong-yoga-1" src="http://yogahuongtre.com/wp-content/uploads/nhung-thuat-ngu-trong-yoga-1.jpg"/></p><p>Dịch một c&aacute;ch đơn giản hơn: T&ocirc;i l&agrave; tuyệt vời. Bạn cũng tuyệt vời. Tất cả những người kh&aacute;c l&agrave; tuyệt vời. Cảm ơn v&igrave; sự hiện diện của bạn.</p><h3>🌟&nbsp;OM</h3><p>Đ&acirc;y l&agrave; &acirc;m thanh của vũ trụ. Om đ&atilde; trở th&agrave;nh một biểu tượng phổ qu&aacute;t của yoga v&agrave; được hiện diện ở khắp mọi nơi n&agrave;o tr&ecirc;n thế giới c&oacute; c&aacute;c yogi.</p><p><img alt="nhung-thuat-ngu-trong-yoga" src="http://yogahuongtre.com/wp-content/uploads/nhung-thuat-ngu-trong-yoga.jpg"/></p><p><br />Về cơ bản, n&oacute; c&oacute; nghĩa l&agrave; ta đều l&agrave; một phần của vũ trụ n&agrave;y &ndash; vũ trụ lu&ocirc;n lu&ocirc;n chuyển động, lu&ocirc;n lu&ocirc;n thay đổi, lu&ocirc;n lu&ocirc;n thở. Khi bạn tụng Om, bạn đang chạm v&agrave;o sự rung động tuyệt vời đ&oacute;.</p><h3>🌟&nbsp;SHANTI</h3><p>Khi bạn h&aacute;t: &ldquo;Om shanti shanti shanti,&rdquo; đ&oacute; l&agrave; một lời gọi h&ograve;a b&igrave;nh. Trong Phật gi&aacute;o v&agrave; truyền thống Hindu bạn tụng shanti ba lần đại diện cho sự h&ograve;a b&igrave;nh trong cơ thể, lời n&oacute;i, v&agrave; t&acirc;m tr&iacute;.</p><h3>🌟&nbsp;Asana Yoga</h3><p><img alt="nhung-thuat-ngu-trong-yoga-2" src="http://yogahuongtre.com/wp-content/uploads/nhung-thuat-ngu-trong-yoga-2.png"/></p><p>Tư thế Yoga, trong tiếng Phạn được gọi l&agrave; Asana. Asana c&oacute; nghĩa l&agrave; tư thế tạo cho người tập một cảm gi&aacute;c thoải m&aacute;i về thể x&aacute;c v&agrave; một t&acirc;m tr&iacute; điềm tĩnh. C&aacute;c Asana trong Yoga t&aacute;c động đến tuyến gi&aacute;p, thần kinh, cơ, điều h&ograve;a h&oacute;c-m&ocirc;n chứa trong tuyến nội tiết, l&agrave;m c&acirc;n bằng cảm x&uacute;c&hellip; Như vậy c&aacute;c Asana trong Yoga l&agrave; c&aacute;c b&agrave;i tập thể chất, nhưng n&oacute; mang đến cho người tập cả những lợi &iacute;ch về thể x&aacute;c lẫn tinh thần.</p>''',
        }
        Post.objects.create(**data3)

    def __create_events(self):
        today = datetime.now()
        data = {
            'image': 'seeds/images/events/yoga_va_doi_song.jpg',
            'name': 'Cuộc thi ảnh đẹp Yoga và đời sống',
            'content': '''<h3>💁&zwj;♀️CUỘC THI ẢNH YOGA - LẦN 4&nbsp;🎉🎉<br />💕YOGA V&Agrave; ĐỜI SỐNG<br />✍️C&ograve;n &iacute;t thời gian nữa th&ocirc;i l&agrave; ch&uacute;ng ta đ&oacute;n ch&agrave;o một năm mới, một h&agrave;nh tr&igrave;nh mới. L&agrave; thời điểm để nh&igrave;n nhận lại thời gian qua ch&uacute;ng ta đ&atilde; l&agrave;m được g&igrave;, bỏ lỡ những g&igrave;. Trong đ&oacute; việc chăm s&oacute;c sức khỏe bản th&acirc;n với yoga đ&atilde; được c&aacute;c Yogi ứng dụng v&agrave;o đời sống như thế n&agrave;o? Để tạo n&ecirc;n một cuộc sống c&acirc;n bằng v&agrave; thịnh vượng.<br />✍️Mỗi sự thay đổi t&iacute;ch cực b&ecirc;n trong, mang n&eacute;t đẹp của Yoga v&agrave;o gia đ&igrave;nh, v&agrave;o nơi l&agrave;m việc, v&agrave;o sứ mạng ri&ecirc;ng của mỗi người ch&iacute;nh l&agrave; sự biết ơn s&acirc;u sắc nhất đối với m&oacute;n qu&agrave; m&agrave; Vũ trụ mang lại; với người thầy; người c&ocirc; đ&atilde; t&acirc;m huyết truyền thụ như một m&oacute;n qu&aacute; để tri &acirc;n v&agrave; ch&agrave;o mừng ng&agrave;y nh&agrave; gi&aacute;o Việt Nam 20/11/2019.<br />✍️V&agrave; cũng l&agrave; dịp để ch&uacute;ng ta ngồi b&ecirc;n nhau với c&acirc;u chuyện cuối năm v&agrave; đầu năm.<br />CLB TỔ CHỨC CUỘC THI ẢNH ĐẸP YOGA - Lần 4<br />Với chủ đề: Yoga v&agrave;o đời sống<br />&ldquo;Kh&ocirc;ng chỉ vui khỏe tr&ecirc;n thảm tập m&agrave; c&ograve;n ngo&agrave;i đời thực&rdquo;<br />Mỗi cảm nhận của ch&uacute;ng ta tr&ecirc;n h&agrave;nh tr&igrave;nh đến với yoga, ứng dụng yoga v&agrave;o đời sống ch&iacute;nh l&agrave; nguồn năng lượng động vi&ecirc;n to lớn đến mỗi th&agrave;nh vi&ecirc;n trong gia đ&igrave;nh, cộng đồng nơi ta chung sống để c&ugrave;ng nhau g&oacute;p phần tạo n&ecirc;n một x&atilde; hội vui khỏe.<br />Với phương ch&acirc;m:<br />Một người khỏe<br />Một gia đ&igrave;nh khỏe<br />Một đất nước khỏe<br />Một thế giới khỏe<br />&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;-<br />1. CHỦ ĐỀ: YOGA V&Agrave; ĐỜI SỐNG<br />Yoga kh&ocirc;ng c&ograve;n xa lạ m&agrave; trở th&agrave;nh phong c&aacute;ch sống của người hiện đại kh&ocirc;ng chỉ tr&ecirc;n thảm tập m&agrave; trong cả đời sống hằng ng&agrave;y. Ch&uacute;ng ta y&ecirc;u Yoga v&agrave; đ&oacute; như l&agrave; một nguồn năng lượng cảm hứng trong tất cả sinh hoạt hằng ng&agrave;y: Bạn c&oacute; thể tranh thủ l&uacute;c vừa l&agrave;m c&ocirc;ng việc nh&agrave;, l&uacute;c chăm con, chăm s&oacute;c c&acirc;y cối, đọc s&aacute;ch, l&uacute;c l&agrave;m việc tại cơ quan,... kết hợp với một động t&aacute;c Yoga y&ecirc;u th&iacute;ch để c&aacute;c c&ocirc;ng việc nh&agrave;m ch&aacute;n h&agrave;ng ng&agrave;y trở n&ecirc;n th&uacute; vị hơn.<br />2. THỜI GIAN<br />- Bắt đầu nhận b&agrave;i thi: 6:00 ng&agrave;y 24/10/2019<br />- Kết th&uacute;c nhận b&agrave;i thi: 18:00 ng&agrave;y 20/11/2019<br />- C&ocirc;ng bố kết quả: 30/11/2019.<br />- Trao thưởng: 22/12/2019.<br />3. ĐỐI TƯỢNG THAM GIA:<br />Tất cả Học vi&ecirc;n v&agrave; Gi&aacute;o vi&ecirc;n của Yoga Hương Tre<br />4. GIẢI THƯỞNG<br />- 1 Giải nhất: 2 triệu đồng tiền mặt. Phiếu tập full 3 th&aacute;ng ở CLB Yoga Hương Tre. Khung ảnh đoạt giải.<br />- 2 Giải nh&igrave;: 1 triệu đồng tiền mặt. Phiếu tập full 3 th&aacute;ng ở CLB Yoga Hương Tre. Khung ảnh đoạt giải.<br />- 3 Giải 3: 500 ngh&igrave;n đồng tiền mặt. Phiếu tập full 3 th&aacute;ng ở CLB Yoga Hương Tre. Khung ảnh đoạt giải.<br />- 4 Giải khuyến kh&iacute;ch: Phiếu tập full 1 th&aacute;ng ở CLB Yoga Hương Tre. Khung ảnh đoạt giải<br />5. THỂ LỆ CUỘC THI:<br />- C&aacute;c bạn c&oacute; thể tham gia ảnh đ&ocirc;i, ảnh đơn, ảnh nh&oacute;m ( từ 3 &ndash; 5 người)<br />- B&agrave;i dự thi b&agrave;o gồm một ảnh v&agrave; một b&agrave;i viết cảm nhận về bức ảnh của m&igrave;nh. H&igrave;nh ảnh kh&ocirc;ng qu&aacute; mờ v&agrave; nh&igrave;n thấy được mặt của th&iacute; sinh dự thi. B&agrave;i cảm nhận kh&ocirc;ng qu&aacute; 500 chữ.<br />- B&agrave;i dự thi chia sẻ l&ecirc;n trang c&aacute; nh&acirc;n Facebook c&ograve;n hoạt động &iacute;t nhất 3 th&aacute;ng<br />- Cuộc thi tr&ecirc;n tinh thần tự nguyện, vui tươi, đo&agrave;n kết, c&ocirc;ng bằng. N&ecirc;n tr&aacute;nh c&aacute;c trường hợp mua like, hack like. Nếu CLB ph&aacute;t hiện sẽ loại c&aacute; nh&acirc;n/ nh&oacute;m ra khỏi cuộc thi.<br />- Ảnh gửi về phải ch&iacute;nh chủ. Kh&ocirc;ng sao ch&eacute;p, lấy tr&ecirc;n mạng. Ch&uacute;ng t&ocirc;i sẽ kh&ocirc;ng chịu tr&aacute;ch nhiệm về việc vi phạm bản quyền.<br />-B&agrave;i dự thi phải ph&ugrave; hợp với văn h&oacute;a, thuần phong mỹ tục v&agrave; ph&aacute;p luật của Việt Nam, kh&ocirc;ng c&oacute; yếu tố li&ecirc;n quan đến ch&iacute;nh trị.<br />Tất cả những c&aacute; nh&acirc;n hoặc nh&oacute;m tham gia cuộc thi vi phạm những nội dung tr&ecirc;n hoặc xảy ra tranh chấp th&igrave; BTC sẽ loại ra khỏi cuộc thi.<br />6. C&Aacute;CH THỨC ĐĂNG B&Agrave;I DỰ THI<br />- Bước 1: Bạn v&agrave;o Fanpage CLB Yoga Huong Tre v&agrave; đăng b&agrave;i dự thi với đầy đủ nội dung:<br />👉&nbsp;Họ v&agrave; T&ecirc;n<br />👉&nbsp;M&atilde; số thẻ , t&ecirc;n cơ sở , khung giờ, gi&aacute;o vi&ecirc;n hướng dẫn.<br />- Bước 2: Đ&iacute;nh k&egrave;m 2 hastag cuối b&agrave;i thi&nbsp;<a href="https://www.facebook.com/hashtag/yogavadoisonghuongtre?epa=HASHTAG">#yogavadoisonghuongtre</a><br /><a href="https://www.facebook.com/hashtag/anhdepyogalan4?epa=HASHTAG">#anhdepyogalan4</a><br />( c&aacute;c bạn ch&uacute; &yacute; kiểm tra đ&uacute;ng hastag nh&eacute; v&igrave; sẽ hỗ trợ ban tổ chức dễ d&agrave;ng thống k&ecirc; b&agrave;i dự thi cũng như c&aacute;c bạn c&oacute; thể dễ d&agrave;ng t&igrave;m kiếm b&agrave;i của m&igrave;nh n&egrave;)<br />- Bước 3: Like v&agrave; share b&agrave;i viết n&agrave;y. K&ecirc;u gọi mọi người like v&agrave; share nữa nh&eacute;!!<br />7. C&Aacute;CH T&Iacute;NH ĐIỂM:<br />- 1 lượt like tương đương với một điểm, 1 lượt share tương đương với 3 điểm. (Tổng điểm chiếm 70%),<br />- 30% c&ograve;n lại đến từ hội đồng chuy&ecirc;n m&ocirc;n dựa tr&ecirc;n ti&ecirc;u ch&iacute;:<br />- Ảnh c&oacute; thẩm mỹ, s&aacute;ng tạo về kh&ocirc;ng gian chụp, bố cục<br />- Ảnh t&ocirc;n l&ecirc;n thần th&aacute;i của người tập.<br />- Nếu l&agrave; Yoga đ&ocirc;i hoặc nh&oacute;m: Ảnh thể hiện sự kết nối, hổ trợ của c&aacute;c th&agrave;nh vi&ecirc;n với nhau v&agrave; tạo h&igrave;nh c&oacute; &yacute; nghĩa.<br />✌V&iacute; dụ c&aacute;ch t&iacute;nh điểm:<br />Chị A: 50 like, 4 share, Điểm của hội đồng chuy&ecirc;n m&ocirc;n 80/100 điểm.<br />Điểm quy đổi = (50x1 + 4x3) x70% +80x30% = 67.4 Đ</h3>''',
            'location': 'CLB Yoga HT',
            'start_at': today
        }
        Event.objects.create(**data)

        data = {
            'image': 'seeds/images/events/chuyen_gia_dinh_duong.jpg',
            'name': 'Gặp gỡ chuyên gia dinh dưỡng',
            'content': '''<h3>[ UNG THƯ - DINH DƯỠNG V&Agrave; YOGA ĐẨY L&Ugrave;I CĂN BỆNH TỬ THẦN ]💥💥<br />❓Bạn c&oacute; biết m&ocirc;i trường n&agrave;o l&agrave; nơi ưa sống của tế b&agrave;o ung thư?<br />❓Liệu rằng lối sinh hoạt hằng ng&agrave;y của bạn đ&atilde; v&ocirc; t&igrave;nh tạo n&ecirc;n m&ocirc;i trường thuận lợi để sản sinh ra tế b&agrave;o ung thư?<br />❓Loại thức ăn n&agrave;o gi&uacute;p ngăn chặn ung thư? C&aacute;c b&agrave;i thuốc qu&yacute; n&agrave;o d&agrave;nh cho cơ thể khoẻ mạnh?<br />❓Luyện tập h&iacute;t thở, tinh thần, th&acirc;n t&acirc;m trong Yoga như thế n&agrave;o để ngăn&nbsp;ngừa v&agrave; hỗ trợ điều trị ung thư?<br />👉Tất cả sẽ được giai đ&aacute;p trong buổi chia sẻ. H&atilde;y nhanh tay đăng k&yacute; để tham gia chương tr&igrave;nh v&agrave; x&acirc;y dựng một cộng đồng khoẻ mạnh nh&eacute;.<br />⭐️Thời Gian, Địa điểm:<br />📍Chủ nhật, Ng&agrave;y 4/8/2019<br />8:00 - 9:00 - Yoga đối với ung thư<br />9:30 - 11:30 - Dinh dưỡng ph&ograve;ng bệnh Ung thư<br />📍Clb Yoga Hương Tre</h3>''',
            'location': 'CLB Yoga HT',
            'start_at': today
        }
        Event.objects.create(**data)

        data = {
            'image': 'seeds/images/events/tu_thien_dong_nai.jpg',
            'name': 'Chuyến từ thiện giúp đỡ người nghèo ở Đồng Nai',
            'content': '''<p>Đo&agrave;n Yoga Hương Tre đ&atilde; trao tận tay 150 phần qu&agrave; đến b&agrave; con ngh&egrave;o nhiểm chất độc m&agrave;u da cam v&agrave; khiếm thị tại Định Qu&aacute;n &ndash; Đồng Nai.</p><ul>	<li>🙏Cảm ơn qu&yacute; mạnh thường qu&acirc;n trong v&agrave; ngo&agrave;i CLB đ&atilde; y&ecirc;u thương v&agrave; t&iacute;n nhiệm.</li>	<li>🙏&nbsp;Cảm ơn qu&yacute; học vi&ecirc;n, gi&aacute;o vi&ecirc;n, bạn b&egrave; ,&hellip; c&ugrave;ng tham gia gi&uacute;p c&ocirc;ng t&aacute;c ph&aacute;t qu&agrave; cho b&agrave; con khuyết tật v&agrave; khiếm thị diễn ra dễ d&agrave;ng hơn, phụ gi&uacute;p ph&acirc;n qu&agrave;, phụ gi&uacute;p bưng b&ecirc; qu&agrave;. CLB rất tr&acirc;n qu&yacute; t&igrave;nh cảm đ&oacute; của cả nh&agrave;.</li>	<li>🙏CLB cảm ơn Thầy Nguy&ecirc;n Tấn &ndash; ch&ugrave;a Từ T&acirc;n, đ&atilde; c&ugrave;ng Đo&agrave;n gieo duy&ecirc;n trong chuyến từ thiện n&agrave;y, đ&oacute; l&agrave; điều may mắn cho CLB v&agrave; cho cả Đo&agrave;n.</li>	<li>🙏&nbsp;CLB cảm ơn c&ocirc; quỹ H&agrave; Ngọc ( c&ocirc; Hồng ) g&oacute;p phần quan trọng gi&uacute;p chuyến đi thiện nguyện được ho&agrave;n th&agrave;nh tốt đẹp, từ kh&acirc;u k&ecirc;u gọi mạnh thường qu&acirc;n, lo xe cộ, qu&agrave; cho b&agrave; con, lo ăn uống cho cả đo&agrave;n.CLB biết ơn tấm l&ograve;ng của c&ocirc; rất nhiều.</li><li>🙏&nbsp;Cảm ơn những lời động vi&ecirc;n, khuyến kh&iacute;ch từ học vi&ecirc;n , gi&aacute;o vi&ecirc;n,bạn b&egrave; gần xa, &hellip;gi&uacute;p cho CLB c&oacute; động lực tổ chức những chiến thiện nguyện &yacute; nghĩa tiếp theo.</li>	<li>🙏Cảm ơn Mẹ thi&ecirc;n nhi&ecirc;n đ&atilde; ban cho Suối Mơ vẻ đẹp thơ mộng đ&uacute;ng như t&ecirc;n gọi, Đo&agrave;n c&oacute; dịp tắm suối m&aacute;t v&agrave; lưu lại những h&igrave;nh ảnh kỷ niệm đẹp.</li>	<li>🙏&nbsp;Ch&uacute;c cả nh&agrave; lu&ocirc;n b&igrave;nh an, khỏe mạnh v&agrave; hạnh ph&uacute;c.</li></ul><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong.jpg" style="height:497px; width:750px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-1.jpg" style="height:563px; width:751px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-2.png" style="height:417px; width:751px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-3.png" style="height:629px; width:750px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-4.jpg" style="height:629px; width:750px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-5.jpg" style="height:629px; width:750px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-6.jpg" style="height:960px; width:412px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-7.jpg" style="height:960px; width:720px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-8.jpg" style="height:563px; width:751px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-9.jpg" style="height:562px; width:749px" /></p><p><img alt="" src="http://yogahuongtre.com/wp-content/uploads/ngay-chu-nhat-tuyet-voi-tran-ngap-yeu-thuong-10.jpg" style="height:960px; width:720px" /></p>''',
            'location': 'Đồng Nai',
            'start_at': today
        }
        Event.objects.create(**data)

    def __create_faq(self):
        data = [
            {
                'question': 'Tôi cần chuẩn bị gì để bắt đầu tập Yoga?',
                'answer': '''<p>Ph&ograve;ng tập: Bạn n&ecirc;n t&igrave;m một trung t&acirc;m Yoga c&oacute; mở nhiều lớp Yoga kh&aacute;c nhau. Điều n&agrave;y sẽ cho bạn c&oacute; nhiều lựa chọn hơn v&agrave; bạn cũng c&oacute; thể thay đổi lớp học để t&igrave;m xem loại h&igrave;nh n&agrave;o l&agrave; tốt nhất v&agrave; ph&ugrave; hợp nhất với m&igrave;nh.</p><p>Quần &aacute;o ph&ugrave; hợp&nbsp;thoải m&aacute;i, tho&aacute;ng kh&iacute;: H&atilde;y nhớ rằng, c&oacute; rất nhiều c&aacute;c động t&aacute;c duỗi, căng khi tập Yoga. V&igrave; vậy, n&ecirc;n chọn quần &aacute;o vừa với cơ thể v&igrave; chắc chắn bạn sẽ kh&ocirc;ng muốn bị ph&acirc;n t&acirc;m khi luyện tập chỉ v&igrave; ống tay &aacute;o hoặc thắt lưng của bạn qu&aacute; chật.</p><p>B&ecirc;n cạnh đ&oacute;, sở hữu một thảm tập ri&ecirc;ng v&agrave; một chiếc khăn mặt cũng l&agrave; điều rất tuyệt vời.</p>''',
            },
            {
                'question': 'Loại hình Yoga nào phù hợp với tôi?',
                'answer': '''<p>Nếu xem Yoga như một b&agrave;i tập thể dục v&agrave; muốn c&oacute; được v&oacute;c d&aacute;ng như &yacute;, bạn n&ecirc;n chọn c&aacute;c loại Yoga mạnh mẽ như Power Yoga, Ashtanga Yoga, hoặc Hot Yoga.</p><p>Nếu muốn kh&aacute;m ph&aacute; sự kết nối đặc biệt giữa cơ thể v&agrave; t&acirc;m tr&iacute;, bạn c&oacute; thể chọn lựa c&aacute;c loại Yoga nhẹ nh&agrave;ng, y&ecirc;n tĩnh, những loại c&oacute; kết hợp ngồi thiền, tụng kinh v&agrave; t&igrave;m hiểu về c&aacute;c kh&iacute;a cạnh triết học của Yoga.</p><p>Nếu bị chấn thương, hay c&oacute; một t&igrave;nh trạng bệnh l&yacute; hoặc những hạn chế kh&aacute;c, bạn n&ecirc;n chọn lựa c&aacute;c lớp học Yoga chậm v&agrave; tập trung nhiều v&agrave;o việc điều chỉnh động t&aacute;c như Gentle Yoga.</p><p><img src="http://www.yogaplus.vn/storage/app/media/cach%20dua%20yoga%20vao%20cuoc%20song/cropped-images/30078936_240251686715287_8120693922964963328_n-0-0-0-0-1524475656.jpg" /></p>''',
            },
            {
                'question': 'Tập Yoga có rủi ro gì không?',
                'answer': '''<p>Giống như c&aacute;c b&agrave;i tập thể dục kh&aacute;c, tập Yoga cũng c&oacute; thể c&oacute; rủi ro. V&igrave; vậy, trước khi tập Yoga, bạn n&ecirc;n tham khảo &yacute; kiến b&aacute;c sĩ v&agrave; chia sẻ với huấn luyện vi&ecirc;n về t&igrave;nh trạng sức khỏe của m&igrave;nh đồng thời cho họ những việc hay động t&aacute;c bạn kh&ocirc;ng thể thực hiện được.</p>'''
            },
            {
                'question': 'Làm thế nào để giữ an toàn khi tập Yoga?',
                'answer': '''<p>Yoga ho&agrave;n to&agrave;n an to&agrave;n nếu bạn được dạy đ&uacute;ng c&aacute;ch bởi một huấn luyện vi&ecirc;n Yoga được đ&agrave;o tạo b&agrave;i bản v&agrave; một lớp học ph&ugrave; hợp với thể trạng. V&igrave; thế, nếu bạn đang tiếp nhận liệu tr&igrave;nh điều trị bệnh l&yacute; n&agrave;o đ&oacute;, h&atilde;y n&oacute;i với c&aacute;c chuy&ecirc;n gia Yoga v&agrave; b&aacute;c sĩ về &yacute; muốn sử dụng một liệu ph&aacute;p thay thế. Họ c&oacute; thể gi&uacute;p bạn x&aacute;c định c&aacute;c rủi ro li&ecirc;n quan v&agrave; tư vấn để bạn c&oacute; thể chọn lựa một lớp Yoga ph&ugrave; hợp.</p><p><img src="http://www.yogaplus.vn/storage/app/media/cach%20dua%20yoga%20vao%20cuoc%20song/cropped-images/27879494_789368487917955_3778794836421771264_n-0-0-0-0-1524475698.jpg" /></p>'''
            },
            {
                'question': 'Tôi có thể nâng cao kiến thức về Yoga như thế nào?',
                'answer': '''<p>Bạn biết kh&ocirc;ng? Yoga c&ograve;n chứa đựng những triết l&yacute;, những kiến thức uy&ecirc;n s&acirc;u tr&iacute; tuệ rất nhiều m&agrave; ch&uacute;ng ta kh&ocirc;ng thể bỏ qua. V&igrave; thế, ngo&agrave;i việc b&agrave;n luận trao đổi thật nhiều với c&aacute;c gi&aacute;o vi&ecirc;n giỏi v&agrave; người thực h&agrave;nh Yoga l&acirc;u năm, bạn cũng c&oacute; thể n&acirc;ng cao vốn hiểu biết v&agrave; nhận thức về Yoga th&ocirc;ng qua s&aacute;ch, b&aacute;o, internet v&agrave; c&aacute;c videp clip về Yoga. Chắc chắn, ch&uacute;ng sẽ gi&uacute;p đời sống Yoga của bạn trở n&ecirc;n phong ph&uacute; hơn về kiến thức, kinh nghiệm cũng như kĩ thuật luyện tập.</p>'''
            },
            {
                'question': 'Làm thế nào để lắng nghe cơ thể mình khi tập Yoga?',
                'answer': '''<p>Bạn phải tập v&agrave;i động t&aacute;c thở v&agrave; tập trung trước khi bắt đầu tập. Khi tập Yoga, n&ecirc;n lu&ocirc;n lắng nghe cơ thể m&igrave;nh. Đừng bao giờ tự &eacute;p m&igrave;nh v&agrave;o một tư thế l&agrave;m cho m&igrave;nh thấy đau hay kh&oacute; chịu. Thay v&agrave;o đ&oacute; th&igrave; bạn cử động chầm chậm khi v&agrave;o hay ra khỏi tư thế để l&uacute;c n&agrave;o cũng phải cảm thấy thoải m&aacute;i.</p><p><img src="http://www.yogaplus.vn/storage/app/media/cach%20dua%20yoga%20vao%20cuoc%20song/cropped-images/30079136_190870251705977_7070737048029626368_n-0-0-0-0-1524475725.jpg" /></p>'''
            },
            {
                'question': 'Yoga có thể hỗ trợ điều trị bệnh không?',
                'answer': '''<p>Yoga rất phổ biến với những người bị đau nhức, chẳng hạn như những người bị vi&ecirc;m khớp hoặc tho&aacute;i h&oacute;a khớp, v&igrave; những tư thế asana nhẹ nh&agrave;ng c&oacute; thể th&uacute;c đẩy sự linh hoạt v&agrave; cải thiện thể lực. Nhiều người cảm nhận rằng Yoga c&ograve;n c&oacute; t&aacute;c dụng ổn định huyết &aacute;p, điều tiết lưu th&ocirc;ng m&aacute;u, giảm vi&ecirc;m, giảm bớt c&aacute;c triệu chứng của bệnh trầm cảm v&agrave; căng thẳng, giảm mệt mỏi, v&agrave; c&oacute; thể gi&uacute;p đỡ bệnh nh&acirc;n hen suyễn h&iacute;t thở dễ d&agrave;ng hơn.</p>'''
            },
            {
                'question': 'Tôi có thể tập luyện Yoga nâng cao không?',
                'answer': '''<p>Luyện tập&nbsp;<strong>Yoga n&acirc;ng cao</strong>&nbsp;l&agrave; giai đoạn đ&ograve;i hỏi ở người tập thực hiện những tư thế kh&oacute; v&agrave; phức tạp, ch&iacute;nh v&igrave; vậy c&aacute;c b&agrave;i tập ở mức độ cao n&agrave;y đ&ograve;i hỏi người tập phải ki&ecirc;n tr&igrave; v&agrave; thực sự c&oacute; quyết t&acirc;m.</p><p>Đồng thời bạn phải l&agrave; người đ&atilde; trải qua, hiểu hết được những vấn đề về Yoga v&agrave; thực sự hiểu bản th&acirc;n để hạn chế những chấn thương kh&ocirc;ng mong muốn.</p><p><em><img src="http://www.yogaplus.vn/storage/app/media/cach%20dua%20yoga%20vao%20cuoc%20song/cropped-images/51e9dafe3162a6d2e916fe315ad3a6d0-0-0-0-0-1524475754.jpg" /></em></p>'''
            },
            {
                'question': 'Những lưu ý nào tôi cần biết khi tập Yoga nâng cao?',
                'answer': '''<p><strong>Yoga n&acirc;ng cao</strong> l&agrave; loại h&igrave;nh Yoga kh&ocirc;ng phải ai cũng tập được, n&ecirc;n trước khi bắt đầu với b&agrave;i tập n&agrave;y cần lưu &yacute; những điều sau:</p><ul><li>Đối với Yoga ở tr&igrave;nh độ Yoga cao, việc khởi động trước khi tập l&agrave; rất quan trọng. Nếu kh&ocirc;ng khởi động, cơ g&acirc;n chưa gi&atilde;n, c&ograve;n cứng, cơ thể chưa được l&agrave;m n&oacute;ng l&ecirc;n th&igrave; khi tập chấn thương cơ, g&acirc;n, xương l&agrave; điều rất dễ xảy đến.</li><li>Kh&ocirc;ng được tự &yacute; tập luyện tại nh&agrave; m&agrave; cần c&oacute; sự hướng dẫn của huấn luyện vi&ecirc;n để tr&aacute;nh chấn thương cột sống.</li><li>Khi thực hiện c&aacute;c b&agrave;i tập Yoga n&acirc;ng cao nếu gặp phải những t&igrave;nh trạng như đau lưng, huyết &aacute;p thấp, đau đầu th&igrave; bạn n&ecirc;n dừng lại v&agrave; nhờ sự hướng dẫn của huấn luyện vi&ecirc;n.</li><li>Đặc biệt với chị em phụ nữ, v&agrave;o những ng&agrave;y đ&egrave;n đỏ hoặc mới sinh tuyệt đối kh&ocirc;ng được thực hiện c&aacute;c động t&aacute;c n&acirc;ng cao.</li></ul>'''
            },
            {
                'question': 'Nếu muốn trở thành Yogi chuyên nghiệp, tôi nên tập ở đâu?',
                'answer': '''<p>C&aacute;c động t&aacute;c n&acirc;ng cao trong Yoga sẽ hỗ trợ người tập đạt đến t&aacute;c dụng kh&ocirc;ng ngờ về cuộc sống, niềm vui, sức khỏe. Ở lớp Yoga n&acirc;ng cao tại trung t&acirc;m Yoga HT, bạn sẽ được c&aacute;c huấn luyện vi&ecirc;n&nbsp;hướng dẫn tận t&igrave;nh từng động t&aacute;c Yoga từ cơ bản tới n&acirc;ng cao, th&iacute;ch hợp với sức khỏe v&agrave; mang đến hiệu quả cao nhất cho c&aacute;c bạn trong việc tập luyện.</p><p>Đ&acirc;y ch&iacute;nh l&agrave; giải ph&aacute;p to&agrave;n diện để bạn t&igrave;m hiểu chuy&ecirc;n s&acirc;u hơn về Yoga v&agrave; tiếp bước tr&ecirc;n con đường trở th&agrave;nh một Yogi chuy&ecirc;n nghiệp.</p><p><img src="http://yogahuongtre.com/wp-content/uploads/khai-giang-khoa-huan-luyen-vien-yoga-3-2.jpg" /></p>'''
            },
        ]
        for d in data:
            FAQ.objects.create(**d)

    def __create_shop(self):
        print("Create Product Categories")
        category = ProductCategory.objects.create(name='Thảm')
        print("Create Products")
        data = {
            'category': category,
            'name': 'Thảm yoga màu xanh rêu',
            'description': 'thảm yoga màu xanh rêu',
            'quantity': 10,
            'price': 200000,
            'image': 'seeds/shop/tham-yoga-xanh-reu-1.jpg'
        }
        Product.objects.create(**data)

        data = {
            'category': category,
            'name': 'Thảm yoga màu xanh lá cây',
            'description': 'thảm yoga màu xanh lá cây',
            'quantity': 10,
            'price': 200000,
            'image': 'seeds/shop/tham-yoga-xanh-la-cay.jpg'
        }
        Product.objects.create(**data)

        data = {
            'category': category,
            'name': 'Thảm yoga màu hồng',
            'description': 'thảm yoga màu hồng',
            'quantity': 10,
            'price': 200000,
            'image': 'seeds/shop/tham-yoga-hong.jpg'
        }
        Product.objects.create(**data)
