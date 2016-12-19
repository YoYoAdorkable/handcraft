# coding:utf-8
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render_to_response

from handcraft.api import *
from hasset.views import httperror
from django.http import HttpResponseNotFound

CONF = ConfigParser()
CONF.read('%s/handcraft.conf' % BASE_DIR)


def my_render(template, data, request):
    return render_to_response(template, data, context_instance=RequestContext(request))


def get_user_info(request, offset):
    """ 获取用户信息及环境 """
    env_dic = {'online': 0, 'offline': 1}
    env = env_dic[offset]
    keyword = request.GET.get('keyword', '')
    user_info = get_session_user_info(request)
    user_id, username = user_info[0:2]
    dept_id, dept_name = user_info[3:5]
    ret = [request, keyword, env, username, dept_name]

    return ret


def get_user_log(ret_list):
    """ 获取不同类型用户日志记录 """
    request, keyword, env, username, dept_name = ret_list
    post_all = Log.objects.filter(is_finished=env).order_by('-start_time')
    post_keyword_all = Log.objects.filter(Q(user__contains=keyword) |
                                          Q(host__contains=keyword)) \
        .filter(is_finished=env).order_by('-start_time')

    if is_super_user(request):
        if keyword:
            posts = post_keyword_all
        else:
            posts = post_all

    elif is_group_admin(request):
        if keyword:
            posts = post_keyword_all.filter(dept_name=dept_name)
        else:
            posts = post_all.filter(dept_name=dept_name)

    elif is_common_user(request):
        if keyword:
            posts = post_keyword_all.filter(user=username)
        else:
            posts = post_all.filter(user=username)

    return posts


@require_login
def log_list(request, offset):
    """ 显示日志 """
    header_title, path1, path2 = u'查看日志', u'查看日志', u'错误日志'
    keyword = request.GET.get('keyword', '')
    web_socket_host = CONF.get('websocket', 'web_socket_host')
    posts = get_user_log(get_user_info(request, offset))
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)

    return render_to_response('hlog/log_%s.html' % offset, locals(), context_instance=RequestContext(request))


@require_admin
def log_kill(request):
    """ 杀掉connect进程 """
    pid = request.GET.get('id', '')
    log = Log.objects.filter(pid=pid)
    if log:
        log = log[0]
        dept_name = log.dept_name
        deptname = get_session_user_info(request)[4]
        if is_group_admin(request) and dept_name != deptname:
            return httperror(request, u'Kill失败, 您无权操作!')
        try:
            os.kill(int(pid), 9)
        except OSError:
            pass
        Log.objects.filter(pid=pid).update(is_finished=1, end_time=datetime.datetime.now())
        return render_to_response('hlog/log_offline.html', locals(), context_instance=RequestContext(request))
    else:
        return HttpResponseNotFound(u'没有此进程!')


@require_login
def log_history(request):
    """ 命令历史记录 """
    log_id = request.GET.get('id', 0)
    log = Log.objects.filter(id=int(log_id))
    if log:
        log = log[0]
        dept_name = log.dept_name
        deptname = get_session_user_info(request)[4]
        if is_group_admin(request) and dept_name != deptname:
            return httperror(request, '查看失败, 您无权查看!')

        elif is_common_user(request):
            return httperror(request, '查看失败, 您无权查看!')

        log_his = "%s.his" % log.log_path
        if os.path.isfile(log_his):
            f = open(log_his)
            content = f.read()
            return HttpResponse(content)
        else:
            return httperror(request, '无日志记录, 请查看日志处理脚本是否开启!')

@require_login
def log_search(request):
    """ 搜索监控 """
    keyword = request.GET.get('keyword')
    login_types = {'S': 'SSH', 'T': 'TELNET'}
    dept = get_session_user_info(request)[5]
    post_all = WEB_Logs.objects.filter(Q(name__contains=keyword) |
                                       Q(header__contains=keyword)).distinct().order_by('name')

    if is_super_user(request):
        posts = post_all

    elif is_group_admin(request):
        posts = post_all.filter(dept=dept)

    elif is_common_user(request):
        user_id, username = get_session_user_info(request)[0:2]
        post_perm = user_perm_asset_api(username)
        posts = list(set(post_all) & set(post_perm))

    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('hlog/log_search.html', locals(), request)



@require_login
def log_urllist(request):
    """ URL详情 """
    header_title, path1, path2 = u'URL详细信息', u'日志详情', u'URL详情'
    keyword = request.GET.get('keyword', '')
    host_id = request.GET.get('id', '')
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    user_id = get_session_user_info(request)[0]

    post_all = WEB_Logs.objects.filter(id=host_id)
    post_keyword_all = WEB_Logs.objects.filter(id=host_id)

    #post_all = WEB_Status.objects.filter(status=1)
    #post_keyword_all = WEB_Status.objects.filter(status=1)

    if did:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        if is_group_admin(request):
            user, dept = get_session_user_dept(request)
        else:
            dept = DEPT.objects.get(id=did)
        posts = dept.asset_set.all()
        return my_render('hlog/log_urllist_nop.html', locals(), request)

    elif gid:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        elif is_group_admin(request) and not validate(request, user_group=[gid]):
            return httperror(request, u'您无权查看!')

        posts = []
        user_group = UserGroup.objects.filter(id=gid)
        if user_group:
            perms = Perm.objects.filter(user_group=user_group)
            for perm in perms:
                for post in perm.asset_group.asset_set.all():
                    posts.append(post)
            posts = list(set(posts))
        else:
            return httperror(request, u'没有这个小组!')
        return my_render('hlog/log_urllist_nop.html', locals(), request)

    elif sid:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        elif is_group_admin(request) and not validate(request, user_group=[sid]):
            return httperror(request, u'您无权查看!')

        posts, asset_groups = [], []
        user_group = UserGroup.objects.filter(id=int(sid))
        if user_group:
            user_group = user_group[0]
            for perm in user_group.sudoperm_set.all():
                asset_groups.extend(perm.asset_group.all())

            for asset_group in asset_groups:
                posts.extend(asset_group.asset_set.all())
            posts = list(set(posts))
        else:
            return httperror(request, u'没有这个sudo授权!')
        return my_render('hlog/log_urllist_nop.html', locals(), request)

    else:
        if is_super_user(request):
            if keyword:
                posts = post_keyword_all
            else:
                posts = post_all
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hlog/log_urllist.html', locals(), request)

        elif is_group_admin(request):
            if keyword:
                posts = post_keyword_all.filter(dept=dept)
            else:
                posts = post_all.filter(dept=dept)

            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hlog/log_urllist.html', locals(), request)

        elif is_common_user(request):
            user_id, username = get_session_user_info(request)[0:2]
            posts = user_perm_asset_api(username)
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hlog/log_urllist_common.html', locals(), request)


@require_login
def log_weblog(request):
    """ 日志详情 """
    header_title, path1, path2 = u'日志详细信息', u'日志管理', u'日志详情'
    keyword = request.GET.get('keyword', '')
    host_id = request.GET.get('id', '')
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    user_id = get_session_user_info(request)[0]

    post_all = WEB_Logs.objects.all().order_by('-id')
    #post_keyword_all = WEB_Logs.objects.all().order_by('-id')
    post_keyword_all = WEB_Logs.objects.filter(Q(name__contains=keyword)).distinct().order_by('-id')

    if did:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        if is_group_admin(request):
            user, dept = get_session_user_dept(request)
        else:
            dept = DEPT.objects.get(id=did)
        posts = dept.asset_set.all()
        return my_render('hlog/log_urllist_nop.html', locals(), request)

    elif gid:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        elif is_group_admin(request) and not validate(request, user_group=[gid]):
            return httperror(request, u'您无权查看!')

        posts = []
        user_group = UserGroup.objects.filter(id=gid)
        if user_group:
            perms = Perm.objects.filter(user_group=user_group)
            for perm in perms:
                for post in perm.asset_group.asset_set.all():
                    posts.append(post)
            posts = list(set(posts))
        else:
            return httperror(request, u'没有这个小组!')
        return my_render('hlog/log_urllist_nop.html', locals(), request)

    elif sid:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        elif is_group_admin(request) and not validate(request, user_group=[sid]):
            return httperror(request, u'您无权查看!')

        posts, asset_groups = [], []
        user_group = UserGroup.objects.filter(id=int(sid))
        if user_group:
            user_group = user_group[0]
            for perm in user_group.sudoperm_set.all():
                asset_groups.extend(perm.asset_group.all())

            for asset_group in asset_groups:
                posts.extend(asset_group.asset_set.all())
            posts = list(set(posts))
        else:
            return httperror(request, u'没有这个sudo授权!')
        return my_render('hlog/log_urllist_nop.html', locals(), request)

    else:
        if is_super_user(request):
            if keyword:
                posts = post_keyword_all
            else:
                posts = post_all
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hlog/log_weblog.html', locals(), request)

        elif is_group_admin(request):
            if keyword:
                posts = post_keyword_all.filter(dept=dept)
            else:
                posts = post_all.filter(dept=dept)

            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hlog/log_weblog.html', locals(), request)

        elif is_common_user(request):
            user_id, username = get_session_user_info(request)[0:2]
            posts = user_perm_asset_api(username)
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hlog/log_urllist_common.html', locals(), request)


@require_login
def log_errorlist(request):
    """ URL详情 """
    header_title, path1, path2 = u'URL详细信息', u'日志详情', u'URL详情'
    keyword = request.GET.get('keyword', '')
    host_id = request.GET.get('id', '')
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    user_id = get_session_user_info(request)[0]

    post_all = WEB_Logs.objects.filter(id=host_id)
    post_keyword_all = WEB_Logs.objects.filter(id=host_id)

    #post_all = WEB_Status.objects.filter(status=1)
    #post_keyword_all = WEB_Status.objects.filter(status=1)

    if did:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        if is_group_admin(request):
            user, dept = get_session_user_dept(request)
        else:
            dept = DEPT.objects.get(id=did)
        posts = dept.asset_set.all()
        return my_render('hlog/log_urllist_nop.html', locals(), request)

    elif gid:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        elif is_group_admin(request) and not validate(request, user_group=[gid]):
            return httperror(request, u'您无权查看!')

        posts = []
        user_group = UserGroup.objects.filter(id=gid)
        if user_group:
            perms = Perm.objects.filter(user_group=user_group)
            for perm in perms:
                for post in perm.asset_group.asset_set.all():
                    posts.append(post)
            posts = list(set(posts))
        else:
            return httperror(request, u'没有这个小组!')
        return my_render('hlog/log_urllist_nop.html', locals(), request)

    elif sid:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        elif is_group_admin(request) and not validate(request, user_group=[sid]):
            return httperror(request, u'您无权查看!')

        posts, asset_groups = [], []
        user_group = UserGroup.objects.filter(id=int(sid))
        if user_group:
            user_group = user_group[0]
            for perm in user_group.sudoperm_set.all():
                asset_groups.extend(perm.asset_group.all())

            for asset_group in asset_groups:
                posts.extend(asset_group.asset_set.all())
            posts = list(set(posts))
        else:
            return httperror(request, u'没有这个sudo授权!')
        return my_render('hlog/log_urllist_nop.html', locals(), request)

    else:
        if is_super_user(request):
            if keyword:
                posts = post_keyword_all
            else:
                posts = post_all
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hlog/log_errorlist.html', locals(), request)

        elif is_group_admin(request):
            if keyword:
                posts = post_keyword_all.filter(dept=dept)
            else:
                posts = post_all.filter(dept=dept)

            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hlog/log_errorlist.html', locals(), request)

        elif is_common_user(request):
            user_id, username = get_session_user_info(request)[0:2]
            posts = user_perm_asset_api(username)
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hlog/log_urllist_common.html', locals(), request)




