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
        trainer1.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga Quốc tế')
        trainer1.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')
        trainer1.certificates.create(
            name='Chứng chỉ trị liệu Yoga cấp bởi Indian Board of Alternative Medicines')
        trainer1.certificates.create(
            name='Huy chương vàng cuộc thi Master Yoga Science & Holistic Health')
        trainer1.certificates.create(
            name='Bằng thạc sĩ khoa học Yoga của Đại Học Haridwar, Ấn Độ năm 2012')

        data2 = {
            'email': 'mantue@gmail.com',
            'first_name': 'Mẫn',
            'last_name': 'Tuệ',
            'image': '/seeds/images/trainers/chi_man.jpg'
        }
        user2 = User(**data2)
        user2.set_password('truong77')
        user2.is_trainer = True
        user2.save()
        trainer2 = Trainer.objects.create(user=user2)
        trainer2.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        trainer2.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        trainer2.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_man.jpg" /></p>'''
        trainer2.save()
        trainer2.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')
        trainer2.certificates.create(
            name='Chứng chỉ trị liệu Yoga cấp bởi Indian Board of Alternative Medicines')
        trainer2.certificates.create(
            name='Huy chương vàng cuộc thi Master Yoga Science & Holistic Health')
        trainer2.certificates.create(
            name='Bằng thạc sĩ khoa học Yoga của Đại Học Haridwar, Ấn Độ năm 2012')

        data3 = {
            'email': 'hoanganh@gmail.com',
            'first_name': 'Anh',
            'last_name': 'Hoàng',
            'image': '/seeds/images/trainers/thay_hoang_anh.jpg'
        }
        user3 = User(**data3)
        user3.set_password('truong77')
        user3.is_trainer = True
        user3.save()
        trainer3 = Trainer.objects.create(user=user3)
        trainer3.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        trainer3.experience = '''<ul><li>10 năm luyện tập Yoga.</li><li>8 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        trainer3.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/all.jpg" /></p>'''
        trainer3.save()
        trainer3.certificates.create(
            name='Chứng chỉ trị liệu Yoga cấp bởi Indian Board of Alternative Medicines')
        trainer3.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')
        trainer3.certificates.create(
            name='Bằng thạc sĩ khoa học Yoga của Đại Học Haridwar, Ấn Độ năm 2012')
        trainer3.certificates.create(
            name='Huy chương vàng cuộc thi Master Yoga Science & Holistic Health')

        data4 = {
            'email': 'duonghaitan@gmail.com',
            'first_name': 'Tân',
            'last_name': 'Dương',
            'image': '/seeds/images/trainers/anh_tan.jpg'
        }
        user4 = User(**data4)
        user4.set_password('truong77')
        user4.is_trainer = True
        user4.save()
        trainer4 = Trainer.objects.create(user=user4)
        trainer4.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        trainer4.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        trainer4.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_phuong_anh_tan.jpg" /></p>'''
        trainer4.save()
        trainer4.certificates.create(
            name='Bằng thạc sĩ khoa học Yoga của Đại Học Haridwar, Ấn Độ năm 2012')
        trainer4.certificates.create(
            name='Chứng chỉ trị liệu Yoga cấp bởi Indian Board of Alternative Medicines')
        trainer4.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')
        trainer4.certificates.create(
            name='Huy chương vàng cuộc thi Master Yoga Science & Holistic Health')

        data5 = {
            'email': 'thanhtien@gmail.com',
            'first_name': 'Tiến',
            'last_name': 'Thanh',
            'image': '/seeds/images/trainers/anh_tien.jpg'
        }
        user5 = User(**data5)
        user5.set_password('truong77')
        user5.is_trainer = True
        user5.save()
        trainer5 = Trainer.objects.create(user=user5)
        trainer5.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        trainer5.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        trainer5.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/all.jpg" /></p>'''
        trainer5.save()
        trainer5.certificates.create(
            name='Chứng chỉ trị liệu Yoga cấp bởi Indian Board of Alternative Medicines')
        trainer5.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')
        trainer5.certificates.create(
            name='Huy chương vàng cuộc thi Master Yoga Science & Holistic Health')
        trainer5.certificates.create(
            name='Bằng thạc sĩ khoa học Yoga của Đại Học Haridwar, Ấn Độ năm 2012')

        data6 = {
            'email': 'kieulinh@gmail.com',
            'first_name': 'Linh',
            'last_name': 'Kiều',
            'image': '/seeds/images/trainers/em_linh.jpg'
        }
        user6 = User(**data6)
        user6.set_password('truong77')
        user6.is_trainer = True
        user6.save()
        trainer6 = Trainer.objects.create(user=user6)
        trainer6.introduction = '''Phấn đấu là một huấn luyện viên được mọi người săn đón. Tôi không ngừng học hỏi, trau dồi kiến thức dinh dưỡng, tập luyện để áp dụng cho bản thân qua đó truyền cảm hứng, động lực cho học viên có một lối sống tích cực, khoa học, thói quen tập luyện đều đặn và đạt được kết quả sớm nhất trong việc tập luyện.'''
        trainer6.experience = '''<ul><li>8 năm luyện tập Yoga.</li><li>5 năm giảng dạy Yoga ở nhiều trung t&acirc;m kh&aacute;c nhau.</li></ul>'''
        trainer6.achievements = '''<p>Tham gia c&aacute;c cuộc thi Yoga ở th&agrave;nh phố Hồ Ch&iacute; Minh v&agrave; đạt được nhiều th&agrave;nh t&iacute;ch.</p><p>Đạt <strong>Giải nhất&nbsp;</strong>Yoga đơn/đ&ocirc;i năm 2015</p><p><img alt="" src="/media/seeds/achievements/chi_ly.jpg" /></p>'''
        trainer6.save()
        trainer6.certificates.create(
            name='Chứng chỉ Huấn luyện viên Yoga của trung tâm Yoga Hương Tre')
        trainer6.certificates.create(
            name='Bằng thạc sĩ khoa học Yoga của Đại Học Haridwar, Ấn Độ năm 2012')
        trainer6.certificates.create(
            name='Chứng chỉ trị liệu Yoga cấp bởi Indian Board of Alternative Medicines')
        trainer6.certificates.create(
            name='Huy chương vàng cuộc thi Master Yoga Science & Holistic Health')
