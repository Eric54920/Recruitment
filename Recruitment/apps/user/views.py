import os
import time
import random
import json
import re
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, RetrieveAPIView
from Recruitment.libs.geetest import GeetestLib
from rest_framework.response import Response
from rest_framework import mixins
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from . import serializers
from . import models
from django.db.models import Q
from . import filters
from . import paginations
from rest_framework import status
from django_redis import get_redis_connection
from django_filters.rest_framework import DjangoFilterBackend
from Recruitment.utils.tencent.sms import send_sms_single
from home.models import Position, Company
from qiniu import Auth
from Recruitment.utils.qiniu.uploader import put_file
import uuid
# Create your views here.

# 极验验证视图
class GeetestCapchaAPIView(APIView):
    def get(self, request):
        """生成验证码的流水号"""
        user_id = 'test'
        gt = GeetestLib(settings.GEETEST["pc_geetest_id"], settings.GEETEST["pc_geetest_key"])
        status = gt.pre_process(user_id)
        response_str = gt.get_response_str()
        import json
        response = json.loads(response_str)
        return Response(response)

    def post(self,request):
        """校验验证码的结果"""
        gt = GeetestLib(settings.GEETEST["pc_geetest_id"], settings.GEETEST["pc_geetest_key"])
        challenge = request.data.get(gt.FN_CHALLENGE, '')
        validate = request.data.get(gt.FN_VALIDATE, '')
        seccode = request.data.get(gt.FN_SECCODE, '')
        result = gt.failback_validate(challenge, validate, seccode)
        if result:
            result = {"status": "success"} 
        else:
            result = {"status": "fail"}
        return Response(result)

class AccountAPIView(CreateAPIView):
    """用户管理"""
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountModelSerializer

@csrf_exempt
def change_user_type(request):
    """切换用户类型为普通用户"""
    data = json.loads(request.body.decode())
    user_id = data.get('user_id')
    mobile = data.get('mobile')
    user_obj = models.Account.objects.filter(pk=user_id, mobile=mobile).first()
    if not user_obj:
        return JsonResponse({'status': 400})
    user_obj.user_type = "0" if user_obj.user_type == "1" else "1"
    user_obj.companyId = None
    user_obj.save()
    Position.objects.filter(publisher_id=user_id).update(is_delete=1, is_show=0)
    return JsonResponse({'status': 200})

class AccountViewset(GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    """用户"""
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class NewsViewset(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """动态"""
    queryset = models.News.objects.filter(is_delete=0).order_by('-pub_date')
    serializer_class = serializers.NewSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = filters.NewsFilter
    pagination_class = paginations.NewsPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ArticleViewset(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """文章"""
    queryset = models.Article.objects.filter(is_delete=0).order_by('-pub_date')
    serializer_class = serializers.ArticleSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = filters.ArticleFilter
    pagination_class = paginations.ArticlePagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class FocusArticleViewset(mixins.ListModelMixin, GenericViewSet):
    """获取我关注的人的文章"""
    serializer_class = serializers.ArticleSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = filters.ArticleFilter
    pagination_class = paginations.ArticlePagination
    
    def list(self, request, *args, **kwargs):
        queryset = models.Article.objects.filter(user__in=models.Focus.objects.filter(follower=kwargs.get('user')).values('followed'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ArticleRetrieve(GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    """获取单篇文章"""
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        obj = serializer.data
        obj.pop('pub_date')
        obj.pop('update_date')
        obj.pop('is_delete')
        return JsonResponse({'result': obj})

class ArticleCommentsViewset(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """文章评论"""
    queryset = models.ArticleComments.objects.all()
    serializer_class = serializers.ArticleCommentsSerializer
    def getUserInfo(self, comment):
        dic = {}
        dic['cid'] = comment.pk
        dic['content'] = comment.content
        dic['create_time'] = comment.create_time
        dic['reply'] = {}
        reply_obj = models.ArticleComments.objects.filter(pk=comment.reply).first()
        dic['reply']['uid'] = reply_obj.user.pk
        dic['reply']['nic_name'] = reply_obj.user.nic_name
        dic['user'] = {}
        dic['user']['uid'] = comment.user.pk
        dic['user']['avatar'] = comment.user.avatar
        dic['user']['nic_name'] = comment.user.nic_name

        return dic

    def list(self, request, *args, **kwargs):
        comment_dic = {}
        comment_list = self.queryset.filter(article_id=kwargs['aid'])
        for comment in comment_list:
            if comment.parent:
                comment_dic[comment.parent].setdefault('sub_comment', [])
                comment_dic[comment.parent]['sub_comment'].append(self.getUserInfo(comment))
            else:
                comment_dic[comment.pk] = {}
                comment_dic[comment.pk]['cid'] = comment.pk
                comment_dic[comment.pk]['content'] = comment.content
                comment_dic[comment.pk]['create_time'] = comment.create_time
                comment_dic[comment.pk]['aid'] = comment.article_id
                comment_dic[comment.pk]['user'] = {}
                comment_dic[comment.pk]['user']['uid'] = comment.user.id
                comment_dic[comment.pk]['user']['avatar'] = comment.user.avatar
                comment_dic[comment.pk]['user']['nic_name'] = comment.user.nic_name
        return JsonResponse(comment_dic)

class FollowedListView(mixins.ListModelMixin, GenericViewSet):
    """获取我关注的人"""
    serializer_class = serializers.FollowedListSerializer
    pagination_class = paginations.FollowedPagination

    def list(self, request, *args, **kwargs):
        queryset = models.Account.objects.filter(pk__in=models.Focus.objects.filter(follower=kwargs.get('follower')).values('followed'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ResumeViewset(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """简历"""
    queryset = models.Resume.objects.filter(is_delete=0).order_by('-pub_date')
    serializer_class = serializers.ResumeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = filters.ResumeFilter
    pagination_class = paginations.ResumePagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ResumeRetrieve(GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    """获取单篇简历"""
    queryset = models.Resume.objects.all()
    serializer_class = serializers.ResumeSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

@csrf_exempt
def user_auth(request):
    """用户角色切换"""
    comapanyName = request.GET.get('name')
    email = request.GET.get('email')
    user_id = request.GET.get('uid')
    mobile = request.GET.get('mobile')
    company_obj = Company.objects.filter(companyFullName=comapanyName, companyEmail__icontains=email).first()
    if not company_obj:
        return JsonResponse({'status': 400, 'msg': "该公司或邮箱不存在"})
    user_obj = models.Account.objects.filter(pk=user_id, mobile=mobile).first()
    if not user_obj:
        return JsonResponse({'status': 400, 'msg': "该用户不存在"})
    user_obj.user_type = "1"
    user_obj.companyId = company_obj.companyId
    user_obj.save()
    return JsonResponse({'status': 200, 'msg': "切换切页用户成功"})

class DeliveryViewset(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    GenericViewSet):
    """投递记录"""
    queryset = models.DeliveryRecord.objects.filter(isdelivery_delete=0).order_by('create_time')
    serializer_class = serializers.DeliverySerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

def delivery_record(request, user):
    """获取投递记录"""
    data = models.DeliveryRecord.objects.filter(isdelivery_delete=False, user_id=user).values('pk', 'create_time', 'position__id', 'position__positionName', 'status')
    return JsonResponse({'status': 200, 'data': list(data)})

def received_record(request, user):
    """获取接收投递记录"""
    data = models.DeliveryRecord.objects.filter(isreceiver_delete=False,position__publisher_id=user).values('pk', 'user__nic_name', 'user__resume__id', 'user_id', 'position_id', 'status', 'create_time')
    return JsonResponse({'status': 200, 'data': list(data)})

def received_change(request, pk):
    """改变投递记录状态"""
    obj = models.DeliveryRecord.objects.filter(pk=pk).first()
    obj.status = 1
    obj.save()
    return JsonResponse({'status': 200})

def delivery_delete(request, pk):
    """删除投递记录"""
    user_type = request.GET.get('type')
    obj = models.DeliveryRecord.objects.filter(pk=pk).first()
    if user_type == 'receiver':
        obj.isreceiver_delete = 1
    elif user_type == 'delivery':
        obj.isdelivery_delete = 1
    obj.save()
    return JsonResponse({'status': 200})

@csrf_exempt
def article_like(request):
    """文章点赞"""
    data = json.loads(request.body.decode('utf-8'))
    try:
        user = data.get('user')
        article_id = data.get('article_id')
    except:
        return JsonResponse({'status': 400})
    obj = models.ArticleLike.objects.filter(user_id=user, article_id_id=article_id).first()
    if obj:
        obj.delete()
    else:
        models.ArticleLike.objects.create(user_id=user, article_id_id=article_id)
    return JsonResponse({'status': 200})

@csrf_exempt
def news_like(request):
    """动态点赞"""
    data = json.loads(request.body.decode('utf-8'))
    try:
        user = data.get('user')
        news_id = data.get('news_id')
    except:
        return JsonResponse({'status': 400})
    obj = models.NewsLike.objects.filter(user_id=user, news_id_id=news_id).first()
    if obj:
        obj.delete()
    else:
        models.NewsLike.objects.create(user_id=user, news_id_id=news_id)
    return JsonResponse({'status': 200})

@csrf_exempt
def upload_file(request):
    """上传文件获取token"""
    q = Auth(settings.QINIU['ACCESS_KEY'], settings.QINIU['SECRET_KEY'])
    BUCKET_NAME = settings.QINIU['BUCKET_NAME']
    key = uuid.uuid4()
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(BUCKET_NAME, key, 3600)

    return JsonResponse({'status': 200, 'token': token, 'key': key})

@csrf_exempt
def focus(request):
    """关注"""
    if request.method == "GET":
        uid = request.GET.get('uid')
        try:
            user_id = request.GET.get('user_id')
            obj = models.Focus.objects.filter(follower_id=user_id, followed_id=uid).first()
            if obj:
                is_focus = True
            else:
                is_focus = False
        except:
            is_focus = False
        followed = models.Focus.objects.filter(followed_id=uid).count()
        follower = models.Focus.objects.filter(follower_id=uid).count()
        return JsonResponse({'status': 200, 'followed': followed, 'follower': follower, 'is_focus': is_focus})

    data = json.loads(request.body.decode('utf-8'))
    follower = data.get('follower')
    followed = data.get('followed')
    obj = models.Focus.objects.filter(follower_id=follower, followed_id=followed).first()
    if obj:
        obj.delete()
        return JsonResponse({'status': 200, 'action': 'cancel'})
    models.Focus.objects.create(follower_id=follower, followed_id=followed)
    return JsonResponse({'status': 200, 'action': 'focus'})

class ChatRecord(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = models.ChatRecord.objects.all()
    serializer_class = serializers.ChatRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = filters.ChatRecordFilter

    def filter_queryset(self, queryset, *args, **kwargs):
        queryset = queryset.filter(send_id__in=[kwargs.get('send'), kwargs.get('receive')], receive_id__in=[kwargs.get('send'), kwargs.get('receive')]).order_by('send_time')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(), *args, **kwargs)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

def get_chat_list(request, user):
    querysets = models.ChatRecord.objects.filter(Q(send_id=user) | Q(receive_id=user)).distinct().values('receive_id', 'receive__nic_name', 'receive__avatar','send_id', 'send__nic_name', 'send__avatar')
    dic = {}
    for item in list(querysets):
        dic.setdefault(item.get('receive_id'), {})
        dic[item.get('receive_id')]['avatar'] = item.get('receive__avatar')
        dic[item.get('receive_id')]['pk'] = item.get('receive_id')
        dic[item.get('receive_id')]['nic_name'] = item.get('receive__nic_name')

        dic.setdefault(item.get('send_id'), {})
        dic[item.get('send_id')]['avatar'] = item.get('send__avatar')
        dic[item.get('send_id')]['pk'] = item.get('send_id')
        dic[item.get('send_id')]['nic_name'] = item.get('send__nic_name')
    lst = []
    for k, v in dic.items():
        lst.append(v)
    return JsonResponse({'status': 200, 'data': lst})

def delete_chat(request, send, receive):
    querysets = models.ChatRecord.objects.filter(Q(Q(send_id=send) & Q(receive_id=receive)) | Q(Q(send_id=receive) & Q(receive_id=send))).delete()
    return JsonResponse({'status': 200})

# 发送短信视图
class SMSAPIView(APIView):
    def get(self, request):
        """
        短信发送接口
        """
        # 验证手机号是否正确
        mobile = request.GET.get('mobile')
        reg = "1[3|4|5|7|8][0-9]{9}"
        if not re.findall(reg, mobile):
            return Response({'status': False, 'msg': '手机号格式不正确'})

        # 验证模版id
        tpl = request.GET.get('tpl')
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            return Response({'status': False, 'msg': '模版id不存在'})

        # 验证手机号码是否已经注册了
        exists = models.Account.objects.filter(mobile=mobile).exists()
        if exists:
            return Response({'status': False, "message": "对不起，当前手机已经被注册！"})

        # 验证手机是否在一分钟内曾经发送过短信了
        redis_conn = get_redis_connection("sms_code")
        # 还剩多久过期
        ret = redis_conn.ttl(mobile) 
        if ret >= 0:
            return Response({"status": False, "message": f"对不起，请在{ret}秒后重试"})

        # 生成短信验证码
        sms_code = random.randrange(1000, 9999)

        # 发送短信
        sms = send_sms_single(mobile, template_id, [sms_code, ])
        if sms['result'] != 0:
            return Response({'status': False, 'msg': '短信发送失败'})

        # 保存短信验证码
        redis_conn.set(mobile, sms_code, ex=settings.SMS_EXPIRE)
        return Response({'status': 0, "message": "验证码正发往您的手机, 请留心"})