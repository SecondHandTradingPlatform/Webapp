from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Q
from webapp.models import Bulletin
from webapp.models import User
from webapp.models import Goods
from webapp.models import Record
from webapp.models import Message
from webapp.models import Friend
from webapp.models import Type
from django import forms
from django.core import serializers
import json
from PIL import Image


# Create your views here.

def admin_index(req):
    if req.method == 'GET':
        req.session.setdefault('admin_login', 0)
        if req.session['admin_login'] == 0:
            return HttpResponseRedirect('http://127.0.0.1:8000/admin_sign_in/')
        user_number = User.objects.count() - 1
        goods_number = Goods.objects.count()
        bulletin_number = Bulletin.objects.count()
        record_number = Record.objects.count()

        g = Goods.objects.all()
        goods0 = {}
        goods = []
        for each in g:
            goods0['id'] = each.id
            goods0['goods_name'] = each.goods_name
            goods0['goods_price'] = each.goods_price
            goods0['goods_seller'] = each.goods_seller.user_name
            goods0['goods_img'] = each.goods_img
            if each.goods_flag:
                goods0['goods_flag'] = '已售'
            else:
                goods0['goods_flag'] = '在售'
            goods0['goods_type'] = each.goods_type.type_name
            goods0['goods_detail'] = each.goods_detail
            goods.append(goods0.copy())

        b = Bulletin.objects.all().order_by('bulletin_time')
        bulletin = {}
        bulletins = []
        for each in b:
            bulletin['id'] = each.id
            bulletin['bulletin_title'] = each.bulletin_title
            bulletin['bulletin_detail'] = each.bulletin_detail
            bulletin['bulletin_time'] = each.bulletin_time.strftime('%Y-%m-%d %H:%I:%S')
            bulletin['bulletin_price'] = each.bulletin_price
            bulletin['bulletin_publisher'] = each.bulletin_publisher.user_name
            bulletins.append(bulletin.copy())

        u = User.objects.all().order_by('user_flag')
        user = {}
        users = []
        for each in u:
            if each.user_account != 'admin':
                user['user_account'] = each.user_account
                user['user_name'] = each.user_name
                user['user_contact'] = each.user_contact
                user['user_local'] = each.user_local
                if each.user_flag:
                    user['user_flag'] = '正式会员'
                else:
                    user['user_flag'] = '注册会员'
                users.append(user.copy())

        r = Record.objects.all()
        record = {}
        records = []
        for each in r:
            record['id'] = each.id
            record['record_buyer'] = each.record_buyer.user_name
            record['record_seller'] = each.record_seller.user_name
            record['record_goods'] = each.record_goods.goods_name
            record['record_time'] = each.record_time.strftime('%Y-%m-%d %H:%I:%S')
            records.append(record.copy())

        return render(req, 'admin/index.html',
                      {'goods': goods, 'bulletins': bulletins, 'users': users, 'records': records,
                       'user_number': user_number, 'goods_number': goods_number,
                       'bulletin_number': bulletin_number, 'record_number': record_number})
    else:
        return render(req, 'admin/index.html')


def admin_users(req):
    if req.method == 'GET':
        req.session.setdefault('admin_login', 0)
        if req.session['admin_login'] == 0:
            return HttpResponseRedirect('http://127.0.0.1:8000/admin_sign_in/')
        u = User.objects.all().order_by('user_flag')
        user = {}
        users = []
        for each in u:
            if each.user_account != 'admin':
                user['user_account'] = each.user_account
                user['user_name'] = each.user_name
                user['user_contact'] = each.user_contact
                user['user_local'] = each.user_local
                if each.user_flag:
                    user['user_flag'] = '正式会员'
                else:
                    user['user_flag'] = '注册会员'
                users.append(user.copy())
        return render(req, 'admin/users.html', {'users': users})
    else:
        account = req.POST['changeAccount']
        # print(req.POST['flag'])
        if req.POST['flag'] == '1':
            u = User.objects.filter(user_account=account)[0]
            u.user_flag = True
            u.save()
        else:
            u = User.objects.filter(user_account=account)[0]
            u.delete()
        return HttpResponse('success')


def admin_goods(req):
    if req.method == 'GET':
        req.session.setdefault('admin_login', 0)
        if req.session['admin_login'] == 0:
            return HttpResponseRedirect('http://127.0.0.1:8000/admin_sign_in/')
        g = Goods.objects.all()
        goods0 = {}
        goods = []
        for each in g:
            goods0['id'] = each.id
            goods0['goods_name'] = each.goods_name
            goods0['goods_price'] = each.goods_price
            goods0['goods_seller'] = each.goods_seller.user_name
            goods0['goods_img'] = each.goods_img
            if each.goods_flag:
                goods0['goods_flag'] = '已售'
            else:
                goods0['goods_flag'] = '在售'
            goods0['goods_type'] = each.goods_type.type_name
            goods0['goods_detail'] = each.goods_detail
            goods.append(goods0.copy())
        return render(req, 'admin/goods.html', {'goods': goods})
    else:
        gid = req.POST['gid']
        if req.POST['flag'] == '1':
            g = Goods.objects.filter(id=gid)[0]
            g.goods_flag = True
            g.save()
            account = req.POST['account']
            Record.objects.create(
                record_buyer=User.objects.filter(user_account=account)[0],
                record_seller=g.goods_seller,
                record_goods=g
            )
        else:
            g = Goods.objects.filter(id=gid)[0]
            g.delete()
        return HttpResponse('success')


def admin_newgoods(req):
    if req.method == 'GET':
        req.session.setdefault('admin_login', 0)
        if req.session['admin_login'] == 0:
            return HttpResponseRedirect('http://127.0.0.1:8000/admin_sign_in/')
        t = Type.objects.all()
        type0 = {}
        types = []
        for each in t:
            type0['id'] = each.id
            type0['name'] = each.type_name
            types.append(type0.copy())
        return render(req, 'admin/newgoods.html', {'types': types})
    else:
        if req.method == 'POST':
            img = req.FILES.get('img')
            account = req.POST.get('account')
            name = req.POST.get('name')
            price = req.POST.get('price')
            detail = req.POST.get('detail')
            type0 = req.POST.get('type')
            flag = False
            Goods.objects.create(
                goods_name=name,
                goods_price=price,
                goods_flag=flag,
                goods_img=img,
                goods_seller=User.objects.filter(user_account=account)[0],
                goods_type=Type.objects.filter(type_name=type0)[0],
                goods_detail=detail
            )
            return HttpResponseRedirect('http://127.0.0.1:8000/admin_goods/')


def admin_record(req):
    if req.method == 'GET':
        req.session.setdefault('admin_login', 0)
        if req.session['admin_login'] == 0:
            return HttpResponseRedirect('http://127.0.0.1:8000/admin_sign_in/')
        r = Record.objects.all()
        record = {}
        records = []
        for each in r:
            record['id'] = each.id
            record['record_buyer'] = each.record_buyer.user_name
            record['record_seller'] = each.record_seller.user_name
            record['record_goods'] = each.record_goods.goods_name
            record['record_time'] = each.record_time.strftime('%Y-%m-%d %H:%I:%S')

            g = each.record_goods
            record['gid'] = g.id
            record['goods_name'] = g.goods_name
            record['goods_price'] = g.goods_price
            record['goods_seller'] = g.goods_seller.user_name
            record['goods_img'] = g.goods_img
            if g.goods_flag:
                record['goods_flag'] = '已售'
            else:
                record['goods_flag'] = '在售'
            record['goods_type'] = g.goods_type.type_name
            record['goods_detail'] = g.goods_detail
            records.append(record.copy())

        return render(req, 'admin/record.html', {'records': records})  # 显示公告 get:全部 post:单条
    else:
        rid = req.POST['rid']
        r = Record.objects.filter(id=rid)[0]
        g = r.record_goods
        g.goods_flag = False
        g.save()
        r.delete()
        return HttpResponse('success')


def admin_bulletin(req):
    if req.method == 'GET':
        req.session.setdefault('admin_login', 0)
        if req.session['admin_login'] == 0:
            return HttpResponseRedirect('http://127.0.0.1:8000/admin_sign_in/')
        b = Bulletin.objects.all().order_by('bulletin_time')
        bulletin = {}
        bulletins = []
        for each in b:
            bulletin['id'] = each.id
            bulletin['bulletin_title'] = each.bulletin_title
            bulletin['bulletin_detail'] = each.bulletin_detail
            bulletin['bulletin_time'] = each.bulletin_time.strftime('%Y-%m-%d %H:%I:%S')
            bulletin['bulletin_price'] = each.bulletin_price
            bulletin['bulletin_publisher'] = each.bulletin_publisher.user_name
            bulletins.append(bulletin.copy())
        return render(req, 'admin/bulletin.html', {'bulletins': bulletins})
    else:
        bid = req.POST['bid']
        b = Bulletin.objects.filter(id=bid)[0]
        b.delete()
        return HttpResponse('success')


def admin_newbulletin(req):
    if req.method == 'POST':
        account = req.POST.get('account')
        title = req.POST.get('title')
        detail = req.POST.get('detail')
        price = req.POST.get('price')
        Bulletin.objects.create(
            bulletin_title=title,
            bulletin_price=price,
            bulletin_detail=detail,
            bulletin_publisher=User.objects.filter(user_account=account)[0]
        )
        return HttpResponseRedirect('http://127.0.0.1:8000/admin_bulletin/')

    else:

        req.session.setdefault('admin_login', 0)
        if req.session['admin_login'] == 0:
            return HttpResponseRedirect('http://127.0.0.1:8000/admin_sign_in/')
        return render(req, 'admin/newbulletin.html')


def admin_rstpassword(req):
    if req.method == 'POST':
        newpswd = req.POST.get('newpswd')
        u = User.objects.filter(user_account='admin')[0]
        u.user_password = newpswd
        u.save()
        return HttpResponseRedirect('http://127.0.0.1:8000/admin_sign_in/')
    else:
        req.session.setdefault('admin_login', 0)
        if req.session['admin_login'] == 0:
            return HttpResponseRedirect('http://127.0.0.1:8000/admin_sign_in/')
        return render(req, 'admin/reset-password.html')


def admin_login(req):
    if req.method == 'POST':
        account = req.POST.get('account')
        password = req.POST.get('password')
        if account == 'admin':
            u = User.objects.filter(user_account=account)[0]
            if u.user_password == password:
                req.session['admin_login'] = 1
                return HttpResponseRedirect('http://127.0.0.1:8000/admin_index/')
        return HttpResponseRedirect('http://127.0.0.1:8000/admin_sign_in/')
    else:
        req.session['admin_login'] = 0
        return render(req, 'admin/sign_in.html')


def admin_message(req):
    if req.method == 'GET':
        req.session.setdefault('admin_login', 0)
        if req.session['admin_login'] == 0:
            return HttpResponseRedirect('http://127.0.0.1:8000/admin_sign_in/')
        m = Message.objects.filter(message_to=User.objects.filter(user_account='admin')[0])
        message = {}
        messages = []
        for each in m:
            message['id'] = each.id
            message['message_from'] = each.message_from
            message['message_time'] = each.message_time.strftime('%Y-%m-%d %H:%I:%S')
            message['message_detail'] = each.message_detail
            messages.append(message.copy())
        # Message.objects.create(message_detail="改进意见", message_from=User.objects.filter(user_account='0212132121')[0],
        #                        message_to=User.objects.filter(user_account='admin')[0])
        return render(req, 'admin/message.html', {'messages': messages})
    else:
        mid = req.POST['mid']
        m = Message.objects.filter(id=mid)[0]
        m.delete()
        return HttpResponse("success")


def admin_remessage(req):
    if req.method == 'GET':
        req.session.setdefault('admin_login', 0)
        if req.session['admin_login'] == 0:
            return HttpResponseRedirect('http://127.0.0.1:8000/admin_sign_in/')
        return render(req, 'admin/remessage.html')
    else:
        account = req.POST.get('account')
        detail = req.POST.get('detail')
        Message.objects.create(message_from=User.objects.filter(user_account='admin')[0],
                               message_to=User.objects.filter(user_account=account)[0],
                               message_detail=detail)
        return HttpResponseRedirect("http://127.0.0.1:8000/admin_message/")



def user_myinfo(req):
    if req.method == 'GET':
        req.session.setdefault('user_login', 0)
        if req.session['user_login'] == 0:
            return HttpResponseRedirect('http://127.0.0.1:8000/------------/')
        u = User.objects.filter(user_account=req.session['user_account'])[0]
        user = {}
        user['user_account'] = u.user_account
        user['user_name'] = u.user_name
        user['user_contact'] = u.user_contact
        user['user_local'] = u.user_local
        if u.user_flag:
            user['user_flag'] = '正式会员'
        else:
            u['user_flag'] = '注册会员'
        return render(req, '----------', {'userinfo': user})
    else:
        changeAccount = req.POST['changeAccount']
        newName = req.POST['newName']
        newContact = req.POST['newContact']
        newLocal = req.POST['newLocal']

        # print(req.POST['flag'])
        u = User.objects.filter(user_account=changeAccount)[0]
        if User.objects.filter(user_name=newName)[0]:
            return HttpResponse('error')
        u.user_name = newName
        u.user_contact = newContact
        u.user_local = newLocal
        u.save()
        return HttpResponse('success')


def user_mylocal(req):



def show_bulletin(req):
    if req.method == 'GET':
        b = Bulletin.objects.all().order_by('bulletin_time')
        bulletin = {}
        bulletins = []
        for each in b:
            bulletin['id'] = each.id
            bulletin['bulletin_detail'] = each.bulletin_detail
            bulletin['bulletin_time'] = each.bulletin_time
            bulletins.append(bulletin.copy())

        bulletins = serializers.serialize("json", Bulletin.objects.all())
        return JsonResponse(list(bulletins), safe=False)
    else:
        bulletin_id = req.POST.get('id')
        bulletin = serializers.serialize("json", Bulletin.objects.get(id=bulletin_id))
        return JsonResponse(list(bulletin), safe=False)


# 发布公告
def publish_bulletin(req):
    if req.method == 'POST':
        publisher = User.objects.filter(user_name=req.session['user_name'])[0]
        detail = req.POST.get('bulletin_detail')
        price = req.POST.get('bulletin_price')

        publish = Bulletin.objects.create(bulletin_publisher=publisher, bulletin_detail=detail, bulletin_price=price)
        if publish:
            return JsonResponse({"flag": "success"})
        else:
            return JsonResponse({"flag": "fail"})
    else:
        return render_to_response(req)


# 删除公告
def delete_bulletin(req):
    if req.method == 'POST':
        now_user = User.objects.filter(user_name=req.session['user_name'])[0]
        bulletin_id = req.POST.get('id')
        bulletin = Bulletin.objects.filter(id=bulletin_id)[0]
        if now_user == bulletin.bulletin_publisher:
            bulletin.delete()
            return JsonResponse({"flag": "success"})
        else:
            return JsonResponse({"flag": "You Have No Permission"})
    else:
        return render_to_response(req)


# 修改公告
def change_bulletin(req):
    if req.method == 'POST':
        now_user = User.objects.filter(user_name=req.session['user_name'])[0]
        bulletin_id = req.POST.get('id')
        bulletin = Bulletin.objects.filter(id=bulletin_id)[0]
        new_detail = req.POST.get('new_detail')
        new_price = req.POST.get('new_price')
        if now_user == bulletin.bulletin_publisher:
            bulletin.bulletin_detail = new_detail
            bulletin.bulletin_price = new_price
            bulletin.save()
            return JsonResponse({"flag": "success"})
        else:
            return JsonResponse({"flag": "You Have No Permission"})
    else:
        return render_to_response(req)


# 用户修改密码
def change_password(req):
    if req.method == 'POST':
        now_user = User.objects.filter(user_name=req.session['user_name'])[0]
        old_password = req.POST.get('old_password')
        new_password = req.POST.get('new_password')

        if old_password == now_user.user_password:
            now_user.user_password = new_password
            now_user.save()
        return JsonResponse({"flag": "success"})
    else:
        return render_to_response(req)


# 用户修改联系方式
def change_contact(req):
    if req.method == 'POST':
        now_user = User.objects.filter(user_name=req.session['user_name'])[0]
        new_contact = req.POST.get('new_contact')
        now_user.user_ConInf = new_contact
        now_user.save()
        return JsonResponse({"flag": "success"})
    else:
        return render_to_response(req)


# 用户修改用户名
def change_name(req):
    if req.method == 'POST':
        now_user = User.objects.filter(user_name=req.session['user_name'])[0]
        new_name = req.POST.get('new_name')
        now_user.user_name = new_name
        now_user.save()
        req.session['user_name'] = new_name
        return JsonResponse({"flag": "success"})
    else:
        return render_to_response(req)


# 发布物品信息
def publish_goods(req):
    if req.method == 'POST':
        name = req.POST.get('goods_name')
        price = req.POST.get('goods_price')
        seller = User.objects.filter(user_name=req.session['user_name'])[0]
        type0 = req.POST.get('goods_type')
        # img = req.POST.get('goods_img')
        img0 = req.FILES.get('goods_img')
        img = Image.open(img0)

        detail = req.POST.get('goods_detail')

        publish = Goods.objects.create(goods_name=name, goods_price=price, goods_flag=False, goods_seller=seller,
                                       goods_type=type0, goods_img=img, goods_detail=detail)
        if publish:
            return JsonResponse({"flag": "success"})
        else:
            return JsonResponse({"flag": "fail"})
    else:
        return render_to_response(req)


# 显示物品信息
def show_goods(req):
    if req.method == 'GET':
        g = Goods.objects.all()
        goods = {}
        goods0 = []
        for each in g:
            goods['id'] = each.id
            goods['goods_name'] = each.goods_name
            goods['goods_price'] = each.goods_price
            goods['goods_seller'] = each.goods_seller.user_name
            goods['goods_img'] = each.goods_img
            goods['goods_flag'] = each.goods_flag
            goods['goods_type'] = each.goods_type
            goods['goods_detail'] = each.goods_detail
            goods0.append(goods.copy())

        goods = serializers.serialize("json", Goods.objects.all())
        return JsonResponse(list(goods), safe=False)
    else:
        goods_id = req.POST.get('id')
        goods = serializers.serialize("json", Goods.objects.filter(id=goods_id)[0])
        return JsonResponse(list(goods), safe=False)


# 更改物品信息
def change_goods(req):
    if req.method == 'POST':
        goods_id = req.POST.get('id')

        new_name = req.POST.get('new_name')
        new_price = req.POST.get('new_price')
        new_seller = req.POST.get('new_seller')
        new_img = req.POST.get('new_img')
        new_type = req.POST.get('new_type')
        new_detail = req.POST.get('new_detail')
        now_user = User.objects.filter(user_name=req.session['user_name'])[0]
        seller = Goods.objects.filter(id=goods_id)[0].goods_seller
        if now_user == seller:
            goods = Goods.objects.filter(id=goods_id)[0]
            goods.goods_name = new_name
            goods.goods_price = new_price
            goods.goods_seller = new_seller
            goods.goods_img = new_img
            goods.goods_type = new_type
            goods.goods_detail = new_detail
            goods.save()
            return JsonResponse({"flag": "success"})
        else:
            return JsonResponse({"flag": "You Have No Permission"})
    else:
        return render_to_response(req)


# 删除物品
def delete_goods(req):
    if req.method == 'POST':
        now_user = User.objects.filter(user_name=req.session['user_name'])[0]
        goods = Goods.objects.filter(req.POST.get('id'))[0]
        seller = goods.goods_seller
        if now_user == seller:
            goods.delete()
            return JsonResponse({"flag": "success"})
        else:
            return JsonResponse({"flag": "fail"})
    else:
        return render_to_response(req)


# 购买物品（创建购买记录）
def buy_goods(req):
    if req.method == 'POST':
        goods_id = req.POST.get('id')
        goods = Goods.objects.filter(id=goods_id)[0]
        seller = goods.goods_seller
        buyer = User.objects.filter(user_name=req.session['user_name'])[0]
        f = Record.objects.create(record_seller=seller, record_buyer=buyer, record_goods=goods)
        if f:
            goods.goods_flag = True
            goods.save()
            return JsonResponse({"flag": "success"})
        else:
            return JsonResponse({"flag": "fail"})
    else:
        return render_to_response(req)


# 留言
def publish_message(req):
    if req.method == 'POST':
        now_user = User.objects.filter(user_name=req.session['user_name'])[0]
        message_to0 = req.POST.get('message_to')
        detail = req.POST.get('message_detail')

        f = Message.objects.create(message_from=now_user, message_to=message_to0, message_detail=detail)
        if f:
            return JsonResponse({"flag": "success"})
        else:
            return JsonResponse({"flag": "fail"})
    else:
        return render_to_response(req)


# 添加好友
def add_friend(req):
    if req.method == 'POST':
        friend_name = req.POST.get('friend_name')
        now_user = User.objects.filter(user_name=req.session['user_name'])[0]
        f = Friend.objects.create(friend_userA=now_user, friend_userB=friend_name)
        if f:
            return JsonResponse({"flag": "success"})
        else:
            return JsonResponse({"flag": "fail"})
    else:
        return render_to_response(req)


# 删除好友
def delete_friend(req):
    if req.method == 'GET':
        now_user = User.objects.filter(user_name=req.session['user_name'])[0]
        friends = Friend.objects.filter(Q(friend_userA=now_user) | Q(friend_userB=now_user))
        friends0 = []
        for each in friends:
            if each.friend_userA == now_user:
                friends0.append(each.friend_userB)
            if each.friend_userB == now_user:
                friends0.append(each.friend_userA)
        friends1 = {"friend": friends0}
        return JsonResponse(list(friends1), safe=False)
    else:
        now_user = User.objects.filter(user_name=req.session['user_name'])[0]
        friendTodel = User.objects.filter(user_name=req.POST.get('friendTodel_name'))[0]
        friend = Friend.objects.filter(Q(friend_userA=now_user) | Q(friend_userB=friendTodel))[0]
        f = friend.delete()
        if f:
            return JsonResponse({"flag": "success"})
        else:
            return JsonResponse({"flag": "fail"})

# def create(req):
#     if req.method == 'POST':
#         img = req.FILES.get('img')
#         account = req.POST.get('account')
#         name = req.POST.get('name')
#         price = req.POST.get('price')
#         detail = req.POST.get('detail')
#         flag = req.POST.get('flag')
#         Goods.objects.create(
#             goods_name=name,
#             goods_price=price,
#             goods_flag=flag,
#             goods_img=img,
#             goods_seller=User.objects.filter(user_account=account)[0],
#             goods_type=Type.objects.filter(id=1)[0],
#             goods_detail=detail
#         )
#         if flag == 1:
#             Record.objects.create(
#                 record_buyer=User.objects.filter(user_account='0212132121')[0],
#                 record_seller=User.objects.filter(user_account='0152152152')[0],
#                 record_good=Goods.objects.filter(goods_name=name)[0]
#             )
#         return render(req, "create.html")
#     else:
#          Type.objects.create(type_name='书籍')
#
#          User.objects.create(user_account='0123121521', user_name='Mark', user_password='123456',
#                              user_contact='15612345678',
#                              user_local='东校区2号楼', user_flag=False)
#          User.objects.create(user_account='0152152152', user_name='Jam', user_password='123456',
#                              user_contact='15945678754',
#                              user_local='东校区3号楼', user_flag=True)
#          User.objects.create(user_account='0212132121', user_name='Amy', user_password='123456',
#                              user_contact='15215212120',
#                              user_local='东校区4号楼', user_flag=True)
#
#          Bulletin.objects.create(bulletin_detail='求购《Python：从入门到入土》', bulletin_price='10',
#                                  bulletin_publisher=User.objects.filter(user_account='0212132121')[0])
#         return render(req, "create.html")
