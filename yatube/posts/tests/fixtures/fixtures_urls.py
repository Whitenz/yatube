from dataclasses import dataclass


@dataclass
class URLFixtures():
    templates_url_names = {
        '/': 'posts/index.html',
        '/group/test-slug/': 'posts/group_list.html',
        '/profile/Author/': 'posts/profile.html',
        '/posts/1/': 'posts/post_detail.html',
        '/posts/1/edit/': 'posts/create_post.html',
        '/create/': 'posts/create_post.html',
    }
    unexisting_page = '/unexisting_page/'
    custom_404 = 'core/404.html'
    urls_for_authorized = ['/posts/1/edit/', '/create/']
    create_url = '/create/'
    create_redirect_url = '/auth/login/?next=/create/'
    edit_url = '/posts/1/edit/'
    edit_redirect_url = '/posts/1/'
    comment_url = '/posts/1/comment/'
    comment_redirect_authorized_url = '/posts/1/'
    comment_redirect_guest_url = '/auth/login/?next=/posts/1/comment/'
