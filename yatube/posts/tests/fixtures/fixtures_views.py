from dataclasses import dataclass

from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


@dataclass
class ViewsFixtures():
    author = 'Author'
    first_user = 'Subscriber'
    another_user = 'Another'
    slug = 'test-slug'
    title = 'тестовый заголовок'
    description = 'тестовое описание группы'
    text = 'тестовый текст поста номер'
    templates_names = {
        reverse('posts:index'): 'posts/index.html',
        reverse('posts:profile',
                kwargs={'username': 'Author'}
                ): 'posts/profile.html',
        reverse('posts:group_list',
                kwargs={'slug': 'test-slug'}
                ): 'posts/group_list.html',
        reverse('posts:post_create'): 'posts/create_post.html',
        reverse('posts:post_detail',
                kwargs={'post_id': 1}
                ): 'posts/post_detail.html',
        reverse('posts:post_edit',
                kwargs={'post_id': 1}
                ): 'posts/create_post.html',
    }
    form_fields = {
        'text': forms.fields.CharField,
        'group': forms.fields.ChoiceField,
        'image': forms.fields.ImageField,
    }
    posts_on_page = 10
    first_post_id = 1
    first_object_in_list = 0
    last_post_id = 13
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00'
        b'\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
        b'\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    uploaded = SimpleUploadedFile(
        name='small.gif',
        content=small_gif,
        content_type='image/gif'
    )
