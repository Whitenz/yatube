from dataclasses import dataclass

from django.core.files.uploadedfile import SimpleUploadedFile


@dataclass
class FormsFixtures():
    username = 'Author'
    text_first_post = 'первый тестовый текст поста'
    posts_added = 1
    first_post_id = 1
    first_object_in_list = 0
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
    form_data = {
        'text': 'второй тестовый текст поста',
        'image': uploaded,
    }
    form_new_data = {
        'text': 'новый тестовый текст поста',
    }
    form_comment = {
        'text': 'новый комментарий',
    }
    image_url = 'posts/small.gif'
