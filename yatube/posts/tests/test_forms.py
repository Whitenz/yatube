import shutil
import tempfile

from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Post, User
from posts.tests.fixtures.fixtures_forms import FormsFixtures

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsFormsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username=FormsFixtures.username
        )
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.author)
        Post.objects.create(
            text=FormsFixtures.text_first_post,
            author=cls.author,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_form_for_create_post(self):
        """Форма позволяет создать новый пост с изображением."""
        initial_count = Post.objects.count()
        PostsFormsTests.authorized_client.post(
            reverse('posts:post_create'),
            FormsFixtures.form_data
        )
        self.assertEqual(
            Post.objects.count(),
            initial_count + FormsFixtures.posts_added,
            'Количество постов в базе не изменилось'
        )
        self.assertTrue(
            Post.objects.filter(
                text=FormsFixtures.form_data['text'],
                image=FormsFixtures.image_url,
            ).exists(),
            'Новый пост с картинкой не найден в базе.'
        )

    def test_form_for_edit_post(self):
        """Форма позволяет отредактировать пост."""
        PostsFormsTests.authorized_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': FormsFixtures.first_post_id}
            ),
            FormsFixtures.form_new_data,
        )
        post_text = Post.objects.get(id=FormsFixtures.first_post_id).text
        expected_text = FormsFixtures.form_new_data['text']
        self.assertEqual(
            post_text,
            expected_text,
            'Текст поста не изменился'
        )

    def test_form_add_comment(self):
        """Форма позволяет добавить комментарий к существующему посту."""
        PostsFormsTests.authorized_client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': FormsFixtures.first_post_id}
            ),
            FormsFixtures.form_comment,
        )
        response = PostsFormsTests.authorized_client.post(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': FormsFixtures.first_post_id}
            )
        )
        comment_from_respones = response.context['comments'][
            FormsFixtures.first_object_in_list].text
        expected_comment = FormsFixtures.form_comment['text']
        self.assertEqual(
            comment_from_respones,
            expected_comment,
            'Ожидаемый комментарий не найден'
        )
