from dataclasses import dataclass


@dataclass
class ModelsFixtures():
    expected_verboses = {
        'text': 'Текст поста',
        'pub_date': 'Дата публикации',
        'author': 'Автор',
        'group': 'Группа',
    }
    expected_help_text = {
        'text': 'Введите текст поста',
        'group': 'Группа, к которой будет относиться пост',
    }
    len_str_post_model = 15
