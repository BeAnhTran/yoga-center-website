import os
from django.conf import settings

try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction
from datetime import datetime, date, timedelta


class Command(BaseCommand):
    help = "LOAD SOME SAMPLE INTO THE DATABASE"

    @transaction.atomic
    def handle(self, **options):
        from getenv import env
        from apps.faq.models import FAQ
        print("Create FAQ")
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
