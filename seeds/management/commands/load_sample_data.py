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


class Command(BaseCommand):
    help = "LOAD SAMPLE DATA INTO THE DB"
    @transaction.atomic
    def handle(self, **options):

        fake = Faker()

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

        # ====================================
        # CREATE ADMIN
        # ====================================
        print("==================")
        print("CREATE ADMIN")

        data_admin = {
            'email': 'admin@admin.com',
            'first_name': fake.first_name(),
            'last_name': fake.last_name()
        }
        admin = User(**data_admin)
        admin.set_password('truong77')
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        # ====================================
        # CREATE STAFF
        # ====================================
        print("==================")
        print("CREATE STAFF")

        number_of_staff = env('NUMBER_OF_STAFF')
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

        # ====================================
        # CREATE TRAINER
        # ====================================
        print("==================")
        print("CREATE TRAINERS")

        number_of_trainer = env('NUMBER_OF_TRAINERS')
        for i in range(1, int(number_of_trainer)):
            data = {
                'email': 'trainer' + str(i) + '@gmail.com',
                'first_name': fake.first_name(),
                'last_name': fake.last_name()
            }
            trainer = User(**data)
            trainer.set_password('truong77')
            trainer.is_trainer = True
            trainer.save()
            Trainer.objects.create(user=trainer)

        # ====================================
        # CREATE TRAINEE
        # ====================================
        print("==================")
        print("CREATE TRAINEES")

        number_of_trainee = env('NUMBER_OF_TRAINEES')
        for i in range(1, int(number_of_trainee)):
            data = {
                'email': 'trainee' + str(i) + '@trainee.com',
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'address': fake.address(),
                'birth_day': fake.date_of_birth(tzinfo=None, minimum_age=15, maximum_age=70),
                'phone_number': fake.phone_number(),
                'gender': random.randint(0, 1)
            }
            trainee = User(**data)
            trainee.set_password('truong77')
            trainee.is_trainee = True
            trainee.save()
            Trainee.objects.create(user=trainee)

        # ====================================
        # CREATE CARD TYPE
        # ====================================
        print("==================")
        print("CREATE CARD TYPES")
        print("CREATE <FOR FULL MONTH> CARD TYPE")
        data_for_full_month = {
            'name': 'học theo tháng',
            'description': 'Áp dụng cho học viên muốn học tất cả các buổi trong tháng',
            'form_of_using': FOR_FULL_MONTH
        }
        full_month_card_type = CardType(**data_for_full_month)
        full_month_card_type.save()

        print("CREATE <FOR SOME LESSONS> CARD TYPE")
        data_for_some_lessons = {
            'name': 'học theo buổi',
            'description': 'Áp dụng cho học viên muốn học theo buổi với số buổi đăng kí trong một khoảng thời gian xác định.',
            'form_of_using': FOR_SOME_LESSONS
        }
        some_lessons_card_type = CardType(
            **data_for_some_lessons)
        some_lessons_card_type.save()
        print("CREATE <FOR TRIAL> CARD TYPE")
        data_for_trial = {
            'name': 'học thử',
            'description': 'Áp dụng cho học viên muốn học thử',
            'form_of_using': FOR_TRIAL,
            'multiplier': env('DEFAULT_MULTIPLIER_FOR_TRIAL')
        }

        trial_card_type = CardType(
            **data_for_trial)
        trial_card_type.save()
        print("CREATE <FOR TRAINING COURSE> CARD TYPE")
        data_for_training_course = {
            'name': 'học theo khóa đào tạo',
            'description': 'Áp dụng cho học viên học khóa học đào tạo',
            'form_of_using': FOR_TRAINING_COURSE
        }

        training_course_card_type = CardType(
            **data_for_training_course)
        training_course_card_type.save()

        # ====================================
        # CREATE COURSE
        # ====================================
        print("==================")
        print("CREATE <HATHA YOGA BASIC LEVEL> COURSES")

        hatha_yoga_course_data = {
            'name': 'Hatha Yoga cơ bản',
            'description': '''Hatha Yoga là tiền đề, nền tảng của tất cả các thể loại Yoga khác.
            Hatha Yoga loại Yoga nhẹ nhàng, phù hợp cho người mới bắt đầu hoặc những người đã thành thạo Yoga và muốn thư giãn. 
            Tập Hatha Yoga bạn sẽ được tập những bài tập thể chất (được gọi chung là tư thế hay asana) nhằm lấy lại sự cân bằng cho cơ thể thông qua các động tác căng, giãn, luyện thở, kỹ thuật thư giãn và thiền''',
            'level': BASIC_LEVEL,
            'content': '''<h3>Nhập m&ocirc;n Yoga:</h3><p>Khi bạn tham gia v&agrave;o&nbsp;<strong>lớp Yoga căn bản</strong>, bạn sẽ được t&igrave;m hiểu những kh&aacute;i niệm cơ bản v&agrave; c&ocirc; đọng nhất về: Lịch sử Yoga, trường ph&aacute;i của Yoga, triết l&yacute; trong Yoga. Hiểu c&aacute;ch hoạt động của Hơi thở, c&aacute;ch thức vận h&agrave;nh c&aacute;c tư thế an to&agrave;n v&agrave; bảo to&agrave;n năng lượng. Lần đầu ti&ecirc;n bạn nhập m&ocirc;n Yoga th&igrave; đ&acirc;y l&agrave; lớp tối ưu để bạn lựa chọn, nếu bạn l&agrave; người đ&atilde; học Yoga rồi th&igrave; cũng l&agrave; dịp để bạn tiếp cận một trường ph&aacute;i Yoga mới, một chế độ tập luyện mới rồi sau đ&oacute; bạn sẽ chọn lớp ph&ugrave; hợp với thực trạng sức khỏe v&agrave; mong muốn của bạn.</p><h3>Nội dung tiếp cận:</h3><ol><li>Gi&uacute;p bạn x&aacute;c định r&otilde; mục ti&ecirc;u đến lớp, x&aacute;c định lớp học ph&ugrave; hợp với t&igrave;nh trạng sức khỏe, mục đ&iacute;ch &nbsp;nhu cầu của bạn.</li><li>Ph&acirc;n biệt lớp Yoga căn bản, Yoga trung cấp, Yoga n&acirc;ng cao.</li><li>L&agrave;m r&otilde;: Hatha Yoga, Astanga Yoga, Vinyasa Yoga.</li><li>Nguy&ecirc;n tắc tập luyện Yoga cần phải tu&acirc;n thủ.</li><li>Những ch&uacute; &yacute; trong tập luyện để đạt hiệu quả cao v&agrave; hạn chế chứng thương.</li><li>C&aacute;ch h&iacute;t thở đ&uacute;ng v&agrave; nguy&ecirc;n l&yacute; vận h&agrave;nh hơi thở đ&uacute;ng.</li><li>C&aacute;ch vận h&agrave;nh c&aacute;c Asana (tư thế Yoga)</li><li>Học c&aacute;ch thư gi&atilde;n v&agrave; nghĩ ngơi trong tập luyện, ứng dụng v&agrave;o c&ocirc;ng việc v&agrave; đời sống.</li><li>Được tư vấn chế độ dinh dưỡng hợp l&yacute;.</li><li>Tiếp cận những triết l&yacute; Yoga để &aacute;p dụng v&agrave;o cuộc sống tốt đẹp hơn.</li><li>Tiếp cận v&agrave; thực h&agrave;nh c&aacute;c tư thế Yoga căn bản, nhẹ nh&agrave;ng theo mức độ tăng dần để cơ thể th&iacute;ch nghi.</li></ol><h3>Lợi &iacute;ch cơ bản của tập Yoga:</h3><ol><li>Học c&aacute;ch nghỉ ngơi để xoa dịu thần kinh v&agrave; c&acirc;n n&atilde;o.</li><li>Tĩnh tọa để tập trung &yacute; ch&iacute;.</li><li>Điều tức để tẩy uế th&acirc;n thể, khu trục c&aacute;c chất cặn b&atilde;.</li><li>Điều kh&iacute; để kiểm so&aacute;t hơi thở.</li><li>Điều th&acirc;n: kiểm so&aacute;t th&acirc;n thể.</li></ol><p>Ngo&agrave;i ra, khi vận h&agrave;nh đ&uacute;ng, Yoga t&aacute;c đ&ocirc;ng l&ecirc;n c&aacute;c b&iacute; huyệt l&agrave;m mạnh c&aacute;c mạch m&aacute;u. Yoga c&ograve;n t&aacute;c động đến c&aacute;c hệ v&agrave; mở lối v&agrave;o t&acirc;m linh.</p><h3>Những ch&uacute; &yacute; trong tập luyện:</h3><ol><li>Tập tr&ecirc;n nền phẳng để giữ cho cột sống thẳng.</li><li>Ph&ograve;ng tập y&ecirc;n tĩnh, tho&aacute;ng m&aacute;t (thi&ecirc;n nhi&ecirc;n c&agrave;ng tốt), hạn chế gi&oacute; l&ugrave;a.</li><li>N&ecirc;n c&oacute; một tấm thảm ri&ecirc;ng v&agrave; khăn để tăng khả năng tập trung.</li><li>Kh&ocirc;ng ăn no trước giờ tập (ăn no &iacute;t nhất l&agrave; 3 tiếng), v&agrave; kh&ocirc;ng ăn liền sau sau khi tập (ăn uống b&igrave;nh thường sau 15 ph&uacute;t)</li><li>N&ecirc;n uống nước trước khi tập Yoga để cơ thể dẽo dai, hạn chế uống nhiều nước trong l&uacute;c tập.</li><li>Tắm sau khi tập &iacute;t nhất l&agrave; 30 ph&uacute;t.</li><li>Quần &aacute;o phải c&oacute; độ co gi&atilde;n v&agrave; thấm h&uacute;t mồ h&ocirc;i, gọn g&agrave;ng để kh&ocirc;ng l&agrave;m vướng l&uacute;c tập.</li><li>Phụ n&ecirc;n tập nhẹ hoặc nghĩ &iacute;t ng&agrave;y trong chu k&igrave; kinh nguyệt.</li><li>Một số trường hợp như: Huyết &aacute;p, tim mạch, cột sống,&hellip;.cần th&ocirc;ng b&aacute;o kĩ c&agrave;ng với nh&acirc;n vi&ecirc;n tư vấn hoặc người hướng dẫn để c&oacute; những lưu &yacute; ph&ugrave; hợp.</li><li>Phải đặt mục ti&ecirc;u tập luyện ph&ugrave; hợp với t&igrave;nh trạng sức khỏe, nhu cầu để duy tr&igrave; v&agrave; đặt kỉ luật tập luyện cho bản th&acirc;n.</li><li>Phải tập luyện với sự cảm nhận v&agrave; duy tr&igrave; &iacute;t nhất 3 th&aacute;ng mới c&oacute; kết quả.</li><li>Trong qu&aacute; tr&igrave;nh tập phải tập trung tư tưởng, &nbsp;giờ n&agrave;o việc đ&oacute;, hướng v&agrave;o cơ thể m&igrave;nh để quan s&aacute;t v&agrave; cảm nhận.</li><li>H&iacute;t v&agrave;o v&agrave; thở ra bằng mũi (những trường hợp cụ thể th&igrave; gi&aacute;o vi&ecirc;n sẽ nhắc nhở)</li><li>Khi giữ thế trong Yoga phải h&iacute;t thở thật chậm để d&ugrave;ng &yacute; vận kh&iacute;.</li><li>Hảy để tinh thần yoga sống kh&ocirc;ng chỉ tr&ecirc;n chiếu tập m&agrave; trong cả cuộc sống h&agrave;ng ng&agrave;y.</li></ol><p><a href="http://yogahuongtre.com/demo/wp-content/uploads/2015/02/770.jpg" title=""><img alt="Hình ảnh yoga căn bản tại cơ sở 1: 142 đường A4, Phường 12, Q.Tân Bình, HCM" src="http://yogahuongtre.com/wp-content/uploads/2015/02/770.jpg" style="height:463px; width:824px" /></a></p>''',
            'image': 'seeds/images/courses/yoga_co_ban.jpg',
            'price_per_lesson': 50000,
            'price_per_month': 600000,
        }
        hatha_yoga_course = Course(**hatha_yoga_course_data)
        hatha_yoga_course.save()

        hatha_yoga_course.card_types.add(
            full_month_card_type,
            some_lessons_card_type,
            trial_card_type
        )

        print("==================")
        print("CREATE <HATHA YOGA ADVANCED LEVEL> COURSES")

        hatha_yoga_advanced_course_data = {
            'name': 'Hatha Yoga nâng cao',
            'description': '''Hatha Yoga là tiền đề, nền tảng của tất cả các thể loại Yoga khác.
            Hatha Yoga loại Yoga nhẹ nhàng, phù hợp cho người mới bắt đầu hoặc những người đã thành thạo Yoga và muốn thư giãn. 
            Tập Hatha Yoga bạn sẽ được tập những bài tập thể chất (được gọi chung là tư thế hay asana) nhằm lấy lại sự cân bằng cho cơ thể thông qua các động tác căng, giãn, luyện thở, kỹ thuật thư giãn và thiền''',
            'level': ADVANCED_LEVEL,
            'image': 'seeds/images/courses/yoga_nang_cao.jpg',
            'price_per_lesson': 50000,
            'price_per_month': 600000,
        }
        hatha_yoga_advanced_course = Course(
            **hatha_yoga_advanced_course_data)
        hatha_yoga_advanced_course.save()

        hatha_yoga_advanced_course.card_types.add(
            full_month_card_type,
            some_lessons_card_type,
            trial_card_type
        )

        print("==================")
        print("CREATE <YOGA DANCE> COURSES")

        yoga_dance_course_data = {
            'name': 'Yoga Dance',
            'description': '''Yoga Dance là một khái niệm mới, một sự kết hợp tinh tế giữa sự nhẹ nhàng, thanh thoát trong các động tác Yoga truyền thống với các điệu nhảy uyển chuyển, quyến rũ cùng với âm nhạc cuốn hút.
            Với Yoga mục tiêu rõ nét là làm dịu đi những bất ổn của xúc cảm và sự căng thẳng trong tinh thần.
            Và khi cơ thể đã thẩm thấu toàn bộ các động tác yoga căn bản, khi đó tự bản thân sẽ đòi hỏi một mức thư giãn cao hơn mà lúc này chỉ có âm nhạc mới giúp được mà thôi''',
            'image': 'seeds/images/courses/yoga_dance.png',
            'price_per_lesson': 50000,
            'price_per_month': 600000,
        }
        yoga_dance_course = Course(**yoga_dance_course_data)
        yoga_dance_course.save()

        print("==================")
        print("CREATE <PRENATAL YOGA> COURSES")

        prenatal_yoga_course_data = {
            'name': 'Yoga cho bà bầu',
            'description': '''Là loại hình Yoga đặc biệt dành riêng cho các bà bầu hoặc phụ nữ chuẩn bị mang thai hay sanh đẻ,... 
            Với các động tác an toàn và kỹ năng thở hoàn toàn tập trung vào phần xương chậu, chân và lưng dưới, những bà mẹ tương lai chắc chắn sẽ yêu thích Prenatal Yoga vì nó giúp nâng cao sự dẻo dai của các cơ hỗ trợ nâng đỡ phần bụng ngày một to ra''',
            'image': 'seeds/images/courses/yoga_bau.jpg',
            'price_per_lesson': 50000,
            'price_per_month': 600000,
        }
        prenatal_yoga_course = Course(**prenatal_yoga_course_data)
        prenatal_yoga_course.save()

        print("==================")
        print("CREATE <TRAINING YOGA TRAINER> COURSES")

        training_yoga_trainer_course_data = {
            'name': 'Đào tạo huấn luyện viên',
            'description': '''Khóa học giúp đào tạo học viên trở thành một Huấn luyện viên Yoga.''',
            'course_type': TRAINING_COURSE,
            'image': 'seeds/images/courses/huan_luyen_vien_yoga.jpg',
            'price_for_training_class':10000000,
        }
        training_yoga_trainer_course = Course(
            **training_yoga_trainer_course_data)
        training_yoga_trainer_course.save()

        training_yoga_trainer_course.card_types.add(
            training_course_card_type
        )

        print("==================")
        print("CREATE <YOGA KID> COURSES")

        yoga_kid_course_data = {
            'name': 'Yoga Kid',
            'description': '''Khóa học dành cho trẻ''',
            'course_type': PRACTICE_COURSE,
            'image': 'seeds/images/courses/yogakid.jpg',
            'price_per_lesson': 50000,
            'price_per_month': 600000,
        }
        yoga_kid_course = Course(
            **yoga_kid_course_data)
        yoga_kid_course.save()

        # ====================================
        # CREATE ROOM
        # ====================================
        print("==================")
        print("CREATE ROOMS")

        for i in range(1, int(env('NUMBER_OF_ROOMS'))):
            data = {
                "name": "Phòng " + str(i),
                "location": "Lầu " + str(i),
                "description": "Mô tả cho phòng " + str(i),
                "max_people": 10 + i,
                "state": 0,
                "created_at": today,
                "updated_at": today
            }
            room = Room(**data)
            room.save()

        r = Room.objects.first()
        r.max_people = 3
        r.save()

        # ====================================
        # CREATE CLASS
        # ====================================
        print("==================")
        print("CREATE CLASSES")

        print("CREATE HATHA YOGA 1 - BASIC")
        trainer1 = Trainer.objects.first()
        hatha_yoga_class1 = hatha_yoga_course.classes.create(
            name='Lớp 2 - 4 - 6',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=trainer1,
        )

        print("CREATE HATHA YOGA 2 - BASIC")
        id_trainer2 = trainer1.pk + 1
        trainer2 = Trainer.objects.get(pk=id_trainer2)
        hatha_yoga_class2 = hatha_yoga_course.classes.create(
            name='Lớp 3 - 5 - 7',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=trainer2,
        )

        print("CREATE HATHA YOGA 3 - BASIC")
        id_trainer3 = trainer1.pk + 2
        trainer3 = Trainer.objects.get(pk=id_trainer3)
        hatha_yoga_class3 = hatha_yoga_course.classes.create(
            name='Lớp chiều 2 - 4 - 6',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=trainer3,
        )

        print("CREATE HATHA YOGA - INTERMEDIATE")
        id_trainer4 = trainer1.pk + 3
        trainer4 = Trainer.objects.get(pk=id_trainer4)
        hatha_yoga_advanced_class = hatha_yoga_advanced_course.classes.create(
            name='Lớp trung cấp 3 - 5 - 7',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            trainer=trainer4,
        )

        print("CREATE TRAINING YOGA TRAINER CLASS")
        id_trainer5 = trainer1.pk + 4
        trainer5 = Trainer.objects.get(pk=id_trainer5)
        training_class = training_yoga_trainer_course.classes.create(
            name='Lớp đào tạo thứ 6 - 7 - CN',
            price_per_lesson=100000,
            price_for_training_class=10000000,
            start_at=today,
            trainer=trainer5
        )

        # ====================================
        # CREATE LESSON
        # ====================================
        print("==================")
        print("CREATE LESSONS")

        print("==================")
        print("CREATE <HATHA YOGA 1 - BASIC> Mon - Wed - Fri - (05:00 - 06:15) LESSONS")
        ######## Mon - Wed - Fri - (05:00 - 06:15) #######
        room_1 = Room.objects.first()
        t1_hatha_1_basic = '05:00'
        t2_hatha_1_basic = (datetime.strptime(t1_hatha_1_basic, '%H:%M') + timedelta(
            minutes=default_range_time_for_practice_lesson)).strftime("%H:%M")

        number_of_weeks = int(env('NUMBER_OF_WEEKS_TO_CREATE_LESSON'))

        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            hatha_yoga_class1.lessons.create(**{
                "room_id": room_1.id,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t1_hatha_1_basic,
                "end_time": t2_hatha_1_basic
            })
            hatha_yoga_class1.lessons.create(**{
                "room_id": room_1.id,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t1_hatha_1_basic,
                "end_time": t2_hatha_1_basic
            })
            hatha_yoga_class1.lessons.create(**{
                "room_id": room_1.id,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t1_hatha_1_basic,
                "end_time": t2_hatha_1_basic
            })

        print("==================")
        print("CREATE <HATHA YOGA 2 - BASIC> Tue - Thurs - Sat - (05:00 - 06:15) LESSONS")
        ######## Tue - Thurs - Sat - (05:00 - 06:15) #######
        id_room_2 = room_1.pk + 1
        room_2 = Room.objects.get(pk=id_room_2)
        t1_hatha_2_basic = '05:00'
        t2_hatha_2_basic = (datetime.strptime(
            t1_hatha_2_basic, '%H:%M') + timedelta(minutes=default_range_time_for_practice_lesson)).strftime("%H:%M")
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            hatha_yoga_class2.lessons.create(**{
                "room_id": room_2.id,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t1_hatha_2_basic,
                "end_time": t2_hatha_2_basic
            })
            hatha_yoga_class2.lessons.create(**{
                "room_id": room_2.id,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t1_hatha_2_basic,
                "end_time": t2_hatha_2_basic
            })
            hatha_yoga_class2.lessons.create(**{
                "room_id": room_2.id,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t1_hatha_2_basic,
                "end_time": t2_hatha_2_basic
            })

        print("==================")
        print("CREATE <HATHA YOGA 3 - BASIC> Mon - Wed - Fri - (17:00 - 18:15) LESSONS")
        ######## Mon - Wed - Fri - (17:00 - 18:15) #######
        t1_hatha_3_basic = '17:00'
        t2_hatha_3_basic = (datetime.strptime(
            t1_hatha_3_basic, '%H:%M') + timedelta(minutes=default_range_time_for_practice_lesson)).strftime("%H:%M")
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            hatha_yoga_class3.lessons.create(**{
                "room_id": room_1.id,
                "date": monday + timedelta(days=count_weeks),
                "start_time": t1_hatha_3_basic,
                "end_time": t2_hatha_3_basic
            })
            hatha_yoga_class3.lessons.create(**{
                "room_id": room_1.id,
                "date": wednesday + timedelta(days=count_weeks),
                "start_time": t1_hatha_3_basic,
                "end_time": t2_hatha_3_basic
            })
            hatha_yoga_class3.lessons.create(**{
                "room_id": room_1.id,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t1_hatha_3_basic,
                "end_time": t2_hatha_3_basic
            })

        print("==================")
        print("CREATE <HATHA YOGA ADVANCED> Tue - Thur - Sat - (18:00 - 19:15) LESSONS")
        ######## Tue - Thur - Sat - (18:00 - 19:15) #######
        t1_hatha_intermediate = '18:00'
        t2_hatha_intermediate = (datetime.strptime(
            t1_hatha_intermediate, '%H:%M') + timedelta(minutes=default_range_time_for_practice_lesson)).strftime("%H:%M")
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            hatha_yoga_advanced_class.lessons.create(**{
                "room_id": room_2.id,
                "date": tuesday + timedelta(days=count_weeks),
                "start_time": t1_hatha_intermediate,
                "end_time": t2_hatha_intermediate
            })
            hatha_yoga_advanced_class.lessons.create(**{
                "room_id": room_2.id,
                "date": thursday + timedelta(days=count_weeks),
                "start_time": t1_hatha_intermediate,
                "end_time": t2_hatha_intermediate
            })
            hatha_yoga_advanced_class.lessons.create(**{
                "room_id": room_2.id,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t1_hatha_intermediate,
                "end_time": t2_hatha_intermediate
            })

        print("==================")
        print(
            "CREATE <TRAINING YOGA TRAINER CLASS> Fri - Sat - Sun - (18:00 - 21:00) LESSONS")
        ######## Fri - Sat - Sun - (18:00 - 21:00) #######
        id_room_3 = room_2.id + 1
        room_3 = Room.objects.get(pk=id_room_3)
        t1_training_class = '18:00'
        t2_training_class = (datetime.strptime(
            t1_hatha_intermediate, '%H:%M') + timedelta(minutes=default_range_time_for_training_lesson)).strftime("%H:%M")
        for i in range(0, number_of_weeks):
            count_weeks = 7 * i
            training_class.lessons.create(**{
                "room_id": room_3.id,
                "date": friday + timedelta(days=count_weeks),
                "start_time": t1_training_class,
                "end_time": t2_training_class
            })
            training_class.lessons.create(**{
                "room_id": room_3.id,
                "date": saturday + timedelta(days=count_weeks),
                "start_time": t1_training_class,
                "end_time": t2_training_class
            })
            training_class.lessons.create(**{
                "room_id": room_3.id,
                "date": sunday + timedelta(days=count_weeks),
                "start_time": t1_training_class,
                "end_time": t2_training_class
            })

        # ######## Create trial card and roll call to test #######
        # print("==================")
        # print("CREATE CARD & ROLL CALL")
        # trainee1 = Trainee.objects.last()
        # trainee2_id = trainee1.pk - 1
        # trainee2 = Trainee.objects.get(pk=trainee2_id)
        # trainee3_id = trainee2.pk - 1
        # trainee3 = Trainee.objects.get(pk=trainee3_id)

        # card1 = Card.objects.create(**{
        #     'trainee': trainee1,
        #     'yogaclass': hatha_yoga_class1,
        #     'card_type': trial_card_type
        # })
        # # card1.lessons.add(lesson_hatha_yoga)
        # RollCall.objects.create(card=card1, lesson=lesson_hatha_yoga)
        # CardInvoiceService(card1, 'trial card', 0).call()

        # card2 = Card.objects.create(**{
        #     'trainee': trainee2,
        #     'yogaclass': hatha_yoga_class1,
        #     'card_type': trial_card_type
        # })
        # # card2.lessons.add(lesson_hatha_yoga)
        # RollCall.objects.create(card=card2, lesson=lesson_hatha_yoga)
        # CardInvoiceService(card2, 'trial card', 0).call()

        # card3 = Card.objects.create(**{
        #     'trainee': trainee3,
        #     'yogaclass': hatha_yoga_class1,
        #     'card_type': trial_card_type
        # })
        # RollCall.objects.create(card=card3, lesson=lesson_hatha_yoga)
        # # card3.lessons.add(lesson_hatha_yoga)
        # CardInvoiceService(card3, 'trial card', 0).call()
