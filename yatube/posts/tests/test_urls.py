from http import HTTPStatus

from django.test import Client, TestCase

from posts.models import Group, Post, User
from posts.tests.fixtures.fixtures_urls import URLFixtures


class PostsURLTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create_user(
            username='Author',
        )
        cls.not_author = User.objects.create_user(
            username='NotAuthor',
        )
        cls.group = Group.objects.create(
            title='тестовый заголовок',
            slug='test-slug',
            description='тестовое описание группы',
        )
        cls.post = Post.objects.create(
            text='тестовые текст',
            author=cls.author,
            group=cls.group,
        )
        cls.guest_client = Client()
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)

    def test_unexisting_page(self):
        """Запрос к несуществующей странице возвращает статус код
         404 и отдает кастомный шаблон."""
        response = PostsURLTests.guest_client.get(
            URLFixtures.unexisting_page
        )
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND,
            'Код ответа не равен 404'
        )
        self.assertTemplateUsed(
            response,
            URLFixtures.custom_404
        )

    def test_urls_exists(self):
        """Доступность страниц любому пользователю."""
        for url in URLFixtures.templates_url_names:
            if url not in URLFixtures.urls_for_authorized:
                with self.subTest(url=url):
                    response = PostsURLTests.guest_client.get(url)
                    self.assertEqual(
                        response.status_code,
                        HTTPStatus.OK,
                        'Код ответа не равен 200, страница недоступна')

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for url, template in URLFixtures.templates_url_names.items():
            with self.subTest(url=url):
                response = PostsURLTests.author_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_create_post(self):
        """
        Возможность создания поста есть только у авторизованного пользователя.
        В ином случае происходит редирект на страницу авторизации.
        """
        response_guest = PostsURLTests.guest_client.get(
            URLFixtures.create_url, follow=True
        )
        response_authorized = PostsURLTests.author_client.get(
            URLFixtures.create_url)
        self.assertRedirects(response_guest, URLFixtures.create_redirect_url)
        self.assertEqual(
            response_authorized.status_code,
            HTTPStatus.OK,
            'Код ответа не равен 200, страница недоступна'
        )

    def test_edit_post(self):
        """
        Возможность редактирования поста есть только у его автора.
        В ином случае происходит редирект на страницу этого поста.
        """
        response_not_author = PostsURLTests.not_author_client.get(
            URLFixtures.edit_url, follow=True
        )
        response_author = PostsURLTests.author_client.get(
            URLFixtures.edit_url
        )
        self.assertRedirects(
            response_not_author, URLFixtures.edit_redirect_url
        )
        self.assertEqual(
            response_author.status_code,
            HTTPStatus.OK,
            'Код ответа не равен 200, страница недоступна'
        )

    def test_add_comment(self):
        """
        Возможность добавлять комментарии есть только у авторизованного
         пользователя.
         В ином случае происходит редирект на страницу авторизации.
        """
        response_author = PostsURLTests.author_client.get(
            URLFixtures.comment_url
        )
        response_guest = PostsURLTests.guest_client.get(
            URLFixtures.comment_url
        )
        self.assertRedirects(
            response_author, URLFixtures.comment_redirect_authorized_url
        )
        self.assertRedirects(
            response_guest, URLFixtures.comment_redirect_guest_url
        )
