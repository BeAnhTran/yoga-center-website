try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction


class Command(BaseCommand):
    help = "Load some sample data into the db"

    @transaction.atomic
    def handle(self, **options):
        from apps.accounts.models import User, Trainer
        print("Create trainers")
        data1 = {
            'email': 'phuongnguyen@gmail.com',
            'first_name': 'Phượng',
            'last_name': 'Nguyễn',
            'image': '/seeds/images/trainers/chi_phuong.jpg'
        }
        user1 = User(**data1)
        user1.set_password('truong77')
        user1.is_trainer = True
        user1.save()
        trainer1 = Trainer.objects.create(user=user1)
        trainer1.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        trainer1.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        trainer1.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_phuong_anh_tan.jpg" /></p>'''
        trainer1.save()
        user1.certificates.create(
            name='Chứng nhận hoàn thành khóa đào tạo Hướng dẫn viên cơ bản Yoga', image='/seeds/images/trainers/chi-phuong/chung-nhan-da-hoan-thanh-khoa-dao-tao-huong-dan-vien-yoga.jpg')
        user1.certificates.create(
            name='Chứng nhận Giải Nhất Festival Yoga Hồ Chí Minh mở rộng lần 1 năm 2017', image='/seeds/images/trainers/chi-phuong/festival-yoga-thanh-pho-hcm.jpg')
        user1.certificates.create(
            name='Chứng nhận Giải Nhất Festival Yoga Hồ Chí Minh mở rộng lần 2 năm 2018', image='/seeds/images/trainers/chi-phuong/giai-nhat-yoga-mo-rong-lan2-nam-2018.jpg')
