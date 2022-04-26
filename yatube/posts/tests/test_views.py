import shutil
import tempfile
import time

from django.conf import settings
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Group, Post, User
from posts.tests.fixtures.fixtures_views import ViewsFixtures

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create_user(
            username=ViewsFixtures.author,
        )
        cls.first_user = User.objects.create_user(
            username=ViewsFixtures.first_user,
        )
        cls.another_user = User.objects.create_user(
            username=ViewsFixtures.another_user,
        )
        cls.group = Group.objects.create(
            title=ViewsFixtures.title,
            slug=ViewsFixtures.slug,
            description=ViewsFixtures.description,
        )
        for i in range(1, ViewsFixtures.last_post_id + 1):
            Post.objects.create(
                text=f'{i} {ViewsFixtures.text}',
                author=cls.author,
                group=cls.group,
                image=ViewsFixtures.uploaded,
            )
            time.sleep(0.01)
        cls.guest_client = Client()
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.first_user_client = Client()
        cls.first_user_client.force_login(cls.first_user)
        cls.another_user_client = Client()
        cls.another_user_client.force_login(cls.another_user)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def response_from_index_page(self):
        return PostsViewsTests.guest_client.get(
            reverse('posts:index')
        )

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for reverse_name, template in ViewsFixtures.templates_names.items():
            with self.subTest(template=template):
                response = PostsViewsTests.author_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_show_correct_context_and_ten_posts(self):
        """
        Шаблон index сформирован с правильным контекстом и содержит на первой
         странице 10 постов.
        """
        query_model = Post.objects.all()[:ViewsFixtures.posts_on_page]
        posts_from_model = list(query_model)
        response = PostsViewsTests.guest_client.get(reverse('posts:index'))
        posts_from_response = list(response.context['page_obj'].object_list)
        response_post_counter = response.context['page_obj'].end_index()
        self.assertEqual(posts_from_response, posts_from_model)
        self.assertEqual(response_post_counter, ViewsFixtures.posts_on_page)
        self.assertTrue(
            posts_from_response[ViewsFixtures.first_object_in_list].image
        )

    def test_group_list_page_show_correct_context_and_ten_posts(self):
        """
        Шаблон group_list сформирован с правильным контекстом и содержит на
         первой странице 10 постов отфильтрованных по групе.
        """
        query_model = Post.objects.filter(
            group__slug=ViewsFixtures.slug)[:ViewsFixtures.posts_on_page]
        posts_from_model = list(query_model)
        response = PostsViewsTests.guest_client.get(
            reverse('posts:group_list', kwargs={'slug': ViewsFixtures.slug})
        )
        posts_from_response = response.context['page_obj'].object_list
        response_post_counter = response.context['page_obj'].end_index()
        self.assertEqual(posts_from_response, posts_from_model)
        self.assertEqual(response_post_counter, ViewsFixtures.posts_on_page)
        self.assertTrue(
            posts_from_response[ViewsFixtures.first_object_in_list].image
        )

    def test_profile_page_show_correct_context_and_ten_posts(self):
        """
        Шаблон profile сформирован с правильным контекстом и содержит на
         первой странице 10 постов отфильтрованных по пользователю.
        """
        query_model = Post.objects.filter(
            author__username=ViewsFixtures.author
        )[:ViewsFixtures.posts_on_page]
        posts_from_model = list(query_model)
        response = PostsViewsTests.guest_client.get(
            reverse('posts:profile', kwargs={'username': ViewsFixtures.author})
        )
        posts_from_response = response.context['page_obj'].object_list
        response_post_counter = response.context['page_obj'].end_index()
        self.assertEqual(posts_from_response, posts_from_model)
        self.assertEqual(response_post_counter, ViewsFixtures.posts_on_page)
        self.assertTrue(
            posts_from_response[ViewsFixtures.first_object_in_list].image
        )

    def test_post_detail_page_show_correct_context(self):
        """
        Шаблон post_detail сформирован с правильным контекстом и содержит
         один пост отфильтрованный по id.
        """
        post_from_model = Post.objects.get(id=ViewsFixtures.first_post_id)
        response = PostsViewsTests.guest_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': ViewsFixtures.first_post_id}
            )
        )
        post_from_response = response.context['post']
        self.assertEqual(post_from_response, post_from_model)
        self.assertTrue(
            post_from_response.image
        )

    def test_create_post_page_show_correct_context(self):
        """
        Шаблон create_post для создания поста сформирован с правильным
         контекстом. При создании нового поста содержит пустую форму.
        """
        response = PostsViewsTests.author_client.get(
            reverse('posts:post_create')
        )
        for value, expected in ViewsFixtures.form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get(
                    'form'
                ).fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_edit_post_page_show_correct_context(self):
        """
        Шаблон create_post для редактирования поста сформирован с правильным
         контекстом. При редактировании поста содержит данные запрошенного
         поста.
        """
        response = PostsViewsTests.author_client.get(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': ViewsFixtures.first_post_id}
            )
        )
        for value, expected in ViewsFixtures.form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get(
                    'form'
                ).fields.get(value)
                self.assertIsInstance(form_field, expected)
        post_from_model = Post.objects.get(id=ViewsFixtures.first_post_id)
        text_from_model = post_from_model.text
        group_from_model = post_from_model.group
        text_from_response = response.context['post'].text
        group_from_response = response.context['post'].group
        self.assertEqual(text_from_model, text_from_response)
        self.assertEqual(group_from_model, group_from_response)

    def test_create_post_for_special_group(self):
        """
        При создании поста с указанием группы этот пост отображается на
         странице этой группы и не попадает на страницы других.
        """
        post_from_model = Post.objects.select_related(
            'author', 'group'
        ).get(id=ViewsFixtures.last_post_id)
        slug = post_from_model.group.slug
        username = post_from_model.author.username
        response_index = PostsViewsTests.guest_client.get(
            reverse('posts:index')
        )
        response_group_list = PostsViewsTests.guest_client.get(
            reverse('posts:group_list', kwargs={'slug': slug})
        )
        respose_profile = PostsViewsTests.guest_client.get(
            reverse('posts:profile', kwargs={'username': username})
        )
        posts_from_response = response_index.context['page_obj'].object_list
        posts_from_group = response_group_list.context['page_obj'].object_list
        posts_from_profile = respose_profile.context['page_obj'].object_list
        self.assertIn(post_from_model, posts_from_response)
        self.assertIn(post_from_model, posts_from_group)
        self.assertIn(post_from_model, posts_from_profile)
        self.assertEqual(slug, ViewsFixtures.slug)

    def test_cache_index_page(self):
        """
        На главной странице кэшируется список постов.
        """
        response_with_post = self.response_from_index_page()
        Post.objects.get(id=ViewsFixtures.last_post_id).delete()
        response_without_post = self.response_from_index_page()
        key = make_template_fragment_key('index_page')
        cache.delete(key)
        response_cleaned_cache = self.response_from_index_page()
        self.assertEqual(
            response_with_post.content,
            response_without_post.content,
            'Удаленный объект не сохранился в кэше')
        self.assertNotEqual(
            response_with_post.content,
            response_cleaned_cache.content,
            'Кэш не был очищен'
        )

    def test_profile_follow(self):
        """
        Авторизованный пользователь может подписываться
         на других пользователей.
        """
        PostsViewsTests.first_user_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': PostsViewsTests.author.username}
            )
        )
        check_follow = (
            PostsViewsTests.first_user.follower.filter(
                author=PostsViewsTests.author
            ).exists()
        )
        self.assertTrue(
            check_follow,
            'Подписка на автора не оформлена'
        )

    def test_profile_unfollow(self):
        """
        Авторизованный пользователь может отменять оформленные подписки.
        """
        PostsViewsTests.first_user_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': PostsViewsTests.author.username}
            )
        )
        PostsViewsTests.first_user_client.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': PostsViewsTests.author.username}
            )
        )
        check_unfollow = (
            PostsViewsTests.first_user.follower.filter(
                author=PostsViewsTests.author
            ).exists()
        )
        self.assertFalse(
            check_unfollow,
            'Подписка на автора не отменена'
        )

    def test_follow_page(self):
        """
        Записи пользователя появляются в ленте тех, кто на него подписан
         и не появляется в ленте тех, кто не подписан.
        """
        PostsViewsTests.first_user_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': PostsViewsTests.author.username}
            )
        )
        response_first_user = PostsViewsTests.first_user_client.get(
            reverse('posts:follow_index')
        )
        count_from_first_user = (
            response_first_user.context['page_obj'].paginator.count
        )
        response_another_user = PostsViewsTests.another_user_client.get(
            reverse('posts:follow_index')
        )
        count_from_another_user = (
            response_another_user.context['page_obj'].paginator.count
        )
        self.assertTrue(
            count_from_first_user,
            'У подписанного пользователя нет постов автора в избранном'
        )
        self.assertFalse(
            count_from_another_user,
            'У неподписанного пользователя обнаружены посты в избранном'
        )
