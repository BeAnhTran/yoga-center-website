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

from rooms.models import Room
from classes.models import (YogaClass, BASIC_LEVEL, INTERMEDIATE_LEVEL)
from courses.models import (Course, TRAINING_COURSE, PRACTICE_COURSE)
from lessons.models import Lesson
from core.models import User, Trainer, Trainee, Staff
from card_types.models import (CardType, FOR_FULL_MONTH,
                          FOR_SOME_LESSONS, FOR_TRIAL, FOR_TRAINING_COURSE)


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
            'username': 'admin',
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
        for i in range(0, int(number_of_staff)):
            data = {
                'username': 'staff' + str(i),
                'email': 'staff' + str(i) + '@staff.com',
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
        for i in range(0, int(number_of_trainer)):
            data = {
                'username': 'trainer' + str(i),
                'email': 'trainer' + str(i) + '@trainer.com',
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
        for i in range(0, int(number_of_trainee)):
            data = {
                'username': 'trainee' + str(i),
                'email': 'trainee' + str(i) + '@trainee.com',
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'address': fake.address(),
                'birth_day': fake.date_of_birth(tzinfo=None, minimum_age=15, maximum_age=70),
                'phone_number': fake.phone_number(),
                'gender': random.randint(0, 2),
                'image': fake.image_url(),
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
        print("CREATE <HATHA YOGA> COURSES")

        hatha_yoga_course_data = {
            'name': 'Hatha Yoga',
            'description': '''Hatha Yoga là tiền đề, nền tảng của tất cả các thể loại Yoga khác.
            Hatha Yoga loại Yoga nhẹ nhàng, phù hợp cho người mới bắt đầu hoặc những người đã thành thạo Yoga và muốn thư giãn. 
            Tập Hatha Yoga bạn sẽ được tập những bài tập thể chất (được gọi chung là tư thế hay asana) nhằm lấy lại sự cân bằng cho cơ thể thông qua các động tác căng, giãn, luyện thở, kỹ thuật thư giãn và thiền'''
        }
        hatha_yoga_course = Course(**hatha_yoga_course_data)
        hatha_yoga_course.save()

        print("==================")
        print("CREATE <YOGA DANCE> COURSES")

        yoga_dance_course_data = {
            'name': 'Yoga Dance',
            'description': '''Yoga Dance là một khái niệm mới, một sự kết hợp tinh tế giữa sự nhẹ nhàng, thanh thoát trong các động tác Yoga truyền thống với các điệu nhảy uyển chuyển, quyến rũ cùng với âm nhạc cuốn hút.
            Với Yoga mục tiêu rõ nét là làm dịu đi những bất ổn của xúc cảm và sự căng thẳng trong tinh thần.
            Và khi cơ thể đã thẩm thấu toàn bộ các động tác yoga căn bản, khi đó tự bản thân sẽ đòi hỏi một mức thư giãn cao hơn mà lúc này chỉ có âm nhạc mới giúp được mà thôi'''
        }
        yoga_dance_course = Course(**yoga_dance_course_data)
        yoga_dance_course.save()

        print("==================")
        print("CREATE <PRENATAL YOGA> COURSES")

        prenatal_yoga_course_data = {
            'name': 'Yoga cho bà bầu',
            'description': '''Là loại hình Yoga đặc biệt dành riêng cho các bà bầu hoặc phụ nữ chuẩn bị mang thai hay sanh đẻ,... 
            Với các động tác an toàn và kỹ năng thở hoàn toàn tập trung vào phần xương chậu, chân và lưng dưới, những bà mẹ tương lai chắc chắn sẽ yêu thích Prenatal Yoga vì nó giúp nâng cao sự dẻo dai của các cơ hỗ trợ nâng đỡ phần bụng ngày một to ra'''
        }
        prenatal_yoga_course = Course(**prenatal_yoga_course_data)
        prenatal_yoga_course.save()

        print("==================")
        print("CREATE <YOGA TRỊ LIỆU> COURSES")

        yoga_tri_lieu_course_data = {
            'name': 'Yoga trị liệu',
            'description': '''Yoga trị liệu là lớp Yoga đặc biệt đối với những học viên đang mang bệnh trong người hoặc muốn tập để duy trì sức khỏe.
            Các bênh về cột sống, tim mạch, huyết áp, tiền đình, tiểu đường.
            Với sự am hiểu về cơ thể người, có chuyên môn trong Yoga. 
            Học viên được trãi nghiệm với các bài tập để xoa dịu, tái tạo, cân bằng, duy trì bôi trơn cơ khớp. 
            Bài tập được thiết kế nhẹ nhàng, linh hoạt, khoa học, dễ tập,... đảm bảo đúng với nhu cầu, mục đích và tình trạng sức khỏe của Học viên.'''
        }
        yoga_tri_lieu_course = Course(**yoga_tri_lieu_course_data)
        yoga_tri_lieu_course.save()

        print("==================")
        print("CREATE <TRAINING YOGA TRAINER> COURSES")

        training_yoga_trainer_course_data = {
            'name': 'Đào tạo huấn luyện viên Yoga',
            'description': '''Khóa học giúp đào tạo học viên trở thành một Huấn luyện viên Yoga.''',
            'course_type': TRAINING_COURSE
        }
        training_yoga_trainer_course = Course(
            **training_yoga_trainer_course_data)
        training_yoga_trainer_course.save()

        # ====================================
        # CREATE ROOM
        # ====================================
        print("==================")
        print("CREATE ROOMS")

        for i in range(0, int(env('NUMBER_OF_ROOMS'))):
            idx = str(i+1)
            data = {
                "name": "Phòng " + idx,
                "location": "Lầu " + idx,
                "description": "Mô tả cho phòng " + idx,
                "max_people": 10 + i,
                "state": 0,
                "created_at": today,
                "updated_at": today
            }
            room = Room(**data)
            room.save()

        # ====================================
        # CREATE CLASS
        # ====================================
        print("==================")
        print("CREATE CLASSES")

        print("CREATE HATHA YOGA 1 - BASIC")
        trainer1 = Trainer.objects.first()
        hatha_yoga_class1 = hatha_yoga_course.classes.create(
            name='Hatha Yoga Cơ bản 1',
            description='mô tả cho hatha yoga cơ bản 1',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            form_trainer=trainer1,
            level=BASIC_LEVEL
        )
        hatha_yoga_class1.card_types.add(
            full_month_card_type,
            some_lessons_card_type,
            trial_card_type
        )

        print("CREATE HATHA YOGA 2 - BASIC")
        id_trainer2 = trainer1.pk + 1
        trainer2 = Trainer.objects.get(pk=id_trainer2)
        hatha_yoga_class2 = hatha_yoga_course.classes.create(
            name='Hatha Yoga Cơ bản 2',
            description='mô tả cho hatha yoga cơ bản 2',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            form_trainer=trainer2,
            level=BASIC_LEVEL
        )

        hatha_yoga_class2.card_types.add(
            full_month_card_type,
            some_lessons_card_type,
            trial_card_type
        )

        print("CREATE HATHA YOGA 3 - BASIC")
        id_trainer3 = trainer1.pk + 2
        trainer3 = Trainer.objects.get(pk=id_trainer3)
        hatha_yoga_class3 = hatha_yoga_course.classes.create(
            name='Hatha Yoga Cơ bản 3',
            description='mô tả cho hatha yoga cơ bản 3',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            form_trainer=trainer2,
            level=BASIC_LEVEL
        )
        hatha_yoga_class3.card_types.add(
            full_month_card_type,
            some_lessons_card_type,
            trial_card_type
        )

        print("CREATE HATHA YOGA - INTERMEDIATE")
        id_trainer4 = trainer1.pk + 3
        trainer4 = Trainer.objects.get(pk=id_trainer4)
        hatha_yoga_imtermediate_class = hatha_yoga_course.classes.create(
            name='Hatha Yoga Trung cấp',
            description='mô tả cho hatha yoga trung cấp',
            price_per_lesson=50000,
            price_per_month=600000,
            start_at=today,
            form_trainer=trainer2,
            level=INTERMEDIATE_LEVEL
        )
        hatha_yoga_imtermediate_class.card_types.add(
            full_month_card_type,
            some_lessons_card_type,
            trial_card_type
        )

        print("CREATE TRAINING YOGA TRAINER CLASS")
        id_trainer5 = trainer1.pk + 4
        trainer5 = Trainer.objects.get(pk=id_trainer5)
        training_class = training_yoga_trainer_course.classes.create(
            name='Đào tạo Huấn Luyện Viên 1',
            description='mô tả cho lớp đào tạo huấn luyện viên',
            price_per_lesson=100000,
            price_course=10000000,
            start_at=today,
            form_trainer=trainer5
        )
        training_class.card_types.add(
            training_course_card_type
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

        hatha_yoga_class1.lessons.create(**{
            "room_id": room_1.id,
            "day": monday,
            "start_time": t1_hatha_1_basic,
            "end_time": t2_hatha_1_basic
        })
        hatha_yoga_class1.lessons.create(**{
            "room_id": room_1.id,
            "day": wednesday,
            "start_time": t1_hatha_1_basic,
            "end_time": t2_hatha_1_basic
        })
        hatha_yoga_class1.lessons.create(**{
            "room_id": room_1.id,
            "day": friday,
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
        hatha_yoga_class2.lessons.create(**{
            "room_id": room_2.id,
            "day": tuesday,
            "start_time": t1_hatha_2_basic,
            "end_time": t2_hatha_2_basic
        })
        hatha_yoga_class2.lessons.create(**{
            "room_id": room_2.id,
            "day": thursday,
            "start_time": t1_hatha_2_basic,
            "end_time": t2_hatha_2_basic
        })
        hatha_yoga_class2.lessons.create(**{
            "room_id": room_2.id,
            "day": saturday,
            "start_time": t1_hatha_2_basic,
            "end_time": t2_hatha_2_basic
        })

        print("==================")
        print("CREATE <HATHA YOGA 3 - BASIC> Mon - Wed - Fri - (17:00 - 18:15) LESSONS")
        ######## Mon - Wed - Fri - (17:00 - 18:15) #######
        t1_hatha_3_basic = '17:00'
        t2_hatha_3_basic = (datetime.strptime(
            t1_hatha_3_basic, '%H:%M') + timedelta(minutes=default_range_time_for_practice_lesson)).strftime("%H:%M")
        hatha_yoga_class3.lessons.create(**{
            "room_id": room_1.id,
            "day": monday,
            "start_time": t1_hatha_3_basic,
            "end_time": t2_hatha_3_basic
        })
        hatha_yoga_class3.lessons.create(**{
            "room_id": room_1.id,
            "day": wednesday,
            "start_time": t1_hatha_3_basic,
            "end_time": t2_hatha_3_basic
        })
        hatha_yoga_class3.lessons.create(**{
            "room_id": room_1.id,
            "day": friday,
            "start_time": t1_hatha_3_basic,
            "end_time": t2_hatha_3_basic
        })

        print("==================")
        print("CREATE <HATHA YOGA IMTERMEDIATE> Tue - Thur - Sat - (18:00 - 19:15) LESSONS")
        ######## Tue - Thur - Sat - (18:00 - 19:15) #######
        t1_hatha_intermediate = '18:00'
        t2_hatha_intermediate = (datetime.strptime(
            t1_hatha_intermediate, '%H:%M') + timedelta(minutes=default_range_time_for_practice_lesson)).strftime("%H:%M")
        hatha_yoga_imtermediate_class.lessons.create(**{
            "room_id": room_2.id,
            "day": tuesday,
            "start_time": t1_hatha_intermediate,
            "end_time": t2_hatha_intermediate
        })
        hatha_yoga_imtermediate_class.lessons.create(**{
            "room_id": room_2.id,
            "day": thursday,
            "start_time": t1_hatha_intermediate,
            "end_time": t2_hatha_intermediate
        })
        hatha_yoga_imtermediate_class.lessons.create(**{
            "room_id": room_2.id,
            "day": saturday,
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
        training_class.lessons.create(**{
            "room_id": room_3.id,
            "day": friday,
            "start_time": t1_training_class,
            "end_time": t2_training_class
        })
        training_class.lessons.create(**{
            "room_id": room_3.id,
            "day": saturday,
            "start_time": t1_training_class,
            "end_time": t2_training_class
        })
        training_class.lessons.create(**{
            "room_id": room_3.id,
            "day": sunday,
            "start_time": t1_training_class,
            "end_time": t2_training_class
        })
