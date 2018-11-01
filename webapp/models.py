from django.db import models
import django.utils.timezone as timezone
# Create your models here.


class User(models.Model):
    user_account = models.CharField(max_length=50, primary_key=True)  #账号
    user_name = models.CharField(max_length=50, unique=True)  #用户名
    user_password = models.CharField(max_length=50)  #密码
    user_contact = models.CharField(max_length=50, unique=True)  #联系方式
    user_local = models.CharField(max_length=50)  #地址
    user_flag = models.BooleanField()


class Type(models.Model):
    #id = models.AutoField()  #标签id
    type_name = models.CharField(max_length=100)  #标签名


class Goods(models.Model):
    #id = models.AutoField() #物品id
    goods_name = models.CharField(max_length=50, unique=True)  #物品名
    goods_price = models.CharField(max_length=50)  #物品价格
    goods_seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goods_seller')  #物品出售人
    goods_flag = models.BooleanField()  #物品出售状态
    goods_type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='goods_type')  #物品类型
    goods_img = models.ImageField(upload_to='img')  #物品图片
    goods_detail = models.TextField()  #物品简介


class Record(models.Model):
    #id = models.AutoField()#记录编号
    record_buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='record_buyer')   #买家
    record_seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='record_seller') #卖家
    record_goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='record_good')    #所购商品
    record_time = models.DateTimeField(default=timezone.now)    #购买时间


class Message(models.Model):
    #id = models.AutoField()#留言编号
    message_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_from')   #留言人
    message_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_to')   #留言对象
    message_detail = models.TextField(max_length=1000)  #留言内容
    message_time = models.DateTimeField(default=timezone.now)   #留言时间


class Collect(models.Model):
    #id = models.AutoField()#收藏编号
    collect_collector = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collect_collector') #收藏人
    collect_goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='collect_goods')    #收藏物品
    collect_time = models.DateTimeField(default=timezone.now)


class Bulletin(models.Model):
    #id =models.AutoField()#公告编号
    bulletin_publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bulletion_publisher')  #公告发布人
    bulletin_title = models.CharField(max_length=100)
    bulletin_detail = models.TextField(max_length=1000) #公告内容
    bulletin_time = models.DateTimeField(default=timezone.now)  #发布时间
    bulletin_price = models.CharField(max_length=50)    #预期价位


class Friend(models.Model):
    #id = models.AutoField()#好友编号
    friend_userA = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_userA')   #用户A
    friend_userB = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_userB')   #用户B