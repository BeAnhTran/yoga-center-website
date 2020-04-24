import os
from django.conf import settings

try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction


class Command(BaseCommand):
    help = "LOAD SOME SAMPLE INTO THE DATABASE"

    @transaction.atomic
    def handle(self, **options):
        from getenv import env
        from apps.blog.models import PostCategory, Post
        print("Create Blog")
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