from django.test import TestCase

from posts.models import Group, Post, User
from posts.tests.fixtures.fixtures_models import ModelsFixtures


class GroupModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.group = Group.objects.create(
            title='тестовый заголовок',
            slug='test-slug',
            description='тестовое описание группы',
        )

    def test_model_have_correct_str(self):
        """
        Проверяем, что у моделей корректно работает __str__ и возвращает
         название группы.
        """
        self.assertEqual(
            str(GroupModelTests.group),
            GroupModelTests.group.title,
            'Метод __str__ вернул неверное значение'
        )


class PostModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username='Author',
        )
        cls.group = Group.objects.create(
            title='тестовый заголовок',
            slug='test-slug',
            description='тестовое описание группы',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='тестовый текст тестовой группы',
            group=cls.group,
        )

    def test_model_have_correct_str(self):
        """Проверяем, что у моделей корректно работает __str__."""
        self.assertEqual(
            str(PostModelTests.post),
            PostModelTests.post.text[:ModelsFixtures.len_str_post_model],
            'Метод __str__ вернул неверное значение'
        )

    def test_verbose_name(self):
        """Сверяем verbose_name у полей объекта с ожидаемым."""
        for field, expected_value in ModelsFixtures.expected_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PostModelTests.post._meta.get_field(field).verbose_name,
                    expected_value,
                    'verbose_name поля задан неверно'
                )

    def test_help_text(self):
        """Сверяем help_text у полей объекта с ожидаемым."""
        for field, expected_value in ModelsFixtures.expected_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PostModelTests.post._meta.get_field(field).help_text,
                    expected_value,
                    'help_text поля задан неверно'
                )
