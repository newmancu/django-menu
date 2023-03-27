from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from menu.models import MenuModel

class Command(BaseCommand):
  help = "startup command"

  def handle(self, *args, **options):
    try:
      user = User.objects.get(username='admin')
    except:
      user = User.objects.create_superuser('admin', 'admin@admin.ad','admin')
      self.stdout.write(self.style.SUCCESS(f'adding default superuser'))
    self.createMenus()

  def createMenus(self):
    bulk = []
    if MenuModel.objects.all().count() == 0:
      bulk.append(MenuModel(name="test_empty", title="Empty Menu", url=r"https://dzen.ru/?yredirect=true"))
      t1 = MenuModel.objects.create(name="Test1", title="Menu1", url=r"admin:index")
      t2 = MenuModel.objects.create(name="Test2", title="Menu2", parent=t1, url=r"invalid_url")
      t3 = MenuModel.objects.create(name="Test3", title="Menu3", parent=t2, url=r"/?Test1=Test1/Test1_1&Test2=Test2/Test3")
      t4 = MenuModel.objects.create(name="Test4", title="Menu4", parent=t3, url=r"/?Test1=Test1/Test1_1/Test2_3")
      bulk.append(MenuModel(name="Test1_1", title="Sub Menu1", parent=t1, url=r"/?Test1=Test1/Test1_1"))
      bulk.append(MenuModel(name="Test1_2", title="Sub Menu2", parent=t1, url=r"#"))
      bulk.append(MenuModel(name="Test1_3", title="Sub Menu3", parent=t1, url=r"#"))
      bulk.append(MenuModel(name="Test2_1", title="Sub2 Menu1", parent=t2, url=r"#"))
      bulk.append(MenuModel(name="Test2_2", title="Sub2 Menu2", parent=t2, url=r"#"))
      t6 = MenuModel.objects.create(name="Test2_3", title="Sub2 Menu3", parent=t2, url=r"#")
      MenuModel.objects.create(name="Test2_3_1", title="Sub2 Menu3_1", parent=t6, url=r"/")


      MenuModel.objects.bulk_create(bulk)