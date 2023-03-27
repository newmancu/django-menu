from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from menu.models import MenuModel
from menu.templatetags.draw_menu import draw_menu


class DrawMenuTestCase(TestCase):
    def setUp(self):
        self.t1 = MenuModel.objects.create(
            name='t1',
            title='t1',
            url=r'https://google.com/'
        )
        self.t1_1 = MenuModel.objects.create(
            name='t1_1',
            parent=self.t1,
            title='t1_1',
            url='admin:index'
        )
        self.t1_2 = MenuModel.objects.create(
            name='t1_2',
            parent=self.t1,
            title='t1_2',
            url='admin:index'
        )
        self.t1_2_1 = MenuModel.objects.create(
            name='t1_2_1',
            parent=self.t1_2,
            title='t1_2_1',
            url='testcase'
        )

    def test_draw_menu_children(self):
        c = draw_menu('t1')
        self.assertEqual(c['root'], self.t1)
        self.assertEqual(set(c['root'].children), set([self.t1_2,self.t1_1]))
        self.assertEqual(c['root'].children[1].children[0], self.t1_2_1)

    def test_draw_menu_subchildren(self):
        c = draw_menu('t1_2')
        self.assertEqual(c['root'], self.t1_2)
        self.assertEqual(set(c['root'].children), set([self.t1_2_1]))

        c = draw_menu('t1_2_1')
        self.assertEqual(c['root'], self.t1_2_1)
        self.assertEqual(set(c['root'].children), set([]))

    def test_draw_menu_urls(self):
        c = draw_menu('t1')
        self.assertEqual(c['root'].get_url, r'https://google.com/')
        self.assertEqual(c['root'].children[0].get_url, reverse('admin:index'))
        self.assertEqual(c['root'].children[1].children[0].get_url, settings.MENU_DEFAULT_REDIRECT)

