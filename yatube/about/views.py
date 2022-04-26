from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """Возвращает статичную страницу с информацией об авторе сайте."""
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """Возвращает статичную страницу с информацией о стеке технолгий
    для разработки сайта."""
    template_name = 'about/tech.html'
