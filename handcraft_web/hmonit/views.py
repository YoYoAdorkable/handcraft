# coding:utf-8

import sys
 
reload(sys)
sys.setdefaultencoding('utf-8')

import ast

from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import get_object_or_404

#from jperm.models import Perm
from handcraft.api import *

#cryptor = PyCrypt(KEY)


class RaiseError(Exception):
    pass


def my_render(template, data, request):
    return render_to_response(template, data, context_instance=RequestContext(request))

#def get_monit_groups(contacts):
#    """ 获取监控所属的组类 """
#    ret = []
#    for group_id in contacts:
#        group = BisGroup.objects.filter(id=group_id)
#        if group:
#            group = group[0]
#            ret.append(group)
#    #group_all = get_object_or_404(BisGroup, name='ALL')
#    #ret.append(group_all)
#    return ret

def db_monit_insert(monit_info):
    """ 添加监控时数据库操作函数 """
    name, header, url, ip, contact, rule, json, json_array, json_variable, parameter, level, route, comment = monit_info
    #ip, public_ip, manage_ip, port, idc, jtype, group, dept, Manufacturer, os, sn, active, comment = host_info
    #contact = UserGroup.objects.filter(name=contact)
    #if contact:
    #   contact = contact[0]
    a = Monit(name=name, header=header, url=url,
              ip=ip, rule=int(rule),
              json=int(json), json_array=json_array, json_variable=json_variable,
              parameter=parameter,
              level=int(level), route=int(route),
              comment=comment)
    a.save()

    #contacts = get_monit_groups(contact) 
    a.contact = contact
    
    a.save()


def db_monit_update(monit_info):
    """ 修改监控时数据库操作函数 """
    name, header, url, ip, contact, rule, json, json_array, json_variable, parameter, level, route, comment, monit = monit_info

    monit.name = name
    monit.header = header
    monit.url = url
    monit.ip = ip
    monit.contact = contact
    monit.rule = rule
    monit.json = json
    monit.json_array = json_array
    monit.json_variable = json_variable
    monit.parameter = parameter
    monit.level = level
    monit.route = route
    monit.comment = comment

    monit.save()


#def batch_monit_edit(host_info, j_user='', j_password=''):
#    """ 批量修改监控函数 """
#    j_id, j_ip, j_public_ip, j_manage_ip, j_port, j_idc, j_type, j_group, j_dept, j_Manufacturer, j_os, j_sn, j_active, j_comment = host_info
#    groups, depts = [], []
#    is_active = {u'是': '1', u'否': '2'}
#    login_types = {'SSH': 'S', 'TELNET': 'T'}
#    a = Monit.objects.get(id=j_id)
#    if '...' in j_group[0].split():
#        groups = a.bis_group.all()
#    else:
#        for group in j_group[0].split():
#            c = BisGroup.objects.get(name=group.strip())
#            groups.append(c)
#
#    if '...' in j_dept[0].split():
#        depts = a.dept.all()
#    else:
#        for d in j_dept[0].split():
#            p = DEPT.objects.get(name=d.strip())
#            depts.append(p)
#
#    j_type = login_types[j_type]
#    j_idc = IDC.objects.get(name=j_idc)
#    if j_type == 'T':
#        if a.password != j_password:
#            j_password = 'admin'
#            #j_password = cryptor.decrypt(j_password)
#        a.ip = j_ip
#        a.public_ip = j_public_ip
#        a.manage_ip = j_manage_ip
#        a.port = j_port
#        a.login_type = j_type
#        a.idc = j_idc
#        a.Manufacturer = j_Manufacturer
#        a.os = j_os
#        a.sn = j_sn
#        a.is_active = j_active
#        a.comment = j_comment
#        a.username = j_user
#        a.password = j_password
#    else:
#        a.ip = j_ip
#        a.public_ip = j_public_ip
#        a.manage_ip = j_manage_ip
#        a.port = j_port
#        a.idc = j_idc
#        a.Manufacturer = j_Manufacturer
#        a.os = j_os
#        a.sn = j_sn
#        a.login_type = j_type
#        a.is_active = is_active[j_active]
#        a.comment = j_comment
#    a.save()
#    a.bis_group = groups
#    a.dept = depts
#    a.save()


def db_monit_delete(request, host_id):
    """ 删除监控操作 """
    if is_group_admin(request) and not validate(request, asset=[host_id]):
        return httperror(request, '删除失败, 您无权删除!')

    asset = Monit.objects.filter(id=host_id)
    if asset:
        asset.delete()
    else:
        return httperror(request, '删除失败, 没有此监控!')


@require_admin
def monit_add(request):
    """ 添加监控 """
    header_title, path1, path2 = u'添加监控', u'监控管理', u'添加监控'
    mcontact = UserGroup.objects.exclude(name='ALL')

    if is_super_user(request):
        edept = DEPT.objects.all()
        egroup = BisGroup.objects.exclude(name='ALL')
    elif is_group_admin(request):
        dept = get_session_user_info(request)[5]
        egroup = dept.bisgroup_set.all()

    if request.method == 'POST':
        j_name = request.POST.get('j_name')
        j_header = request.POST.get('j_header')
        j_url = request.POST.get('j_url')
        j_ip = request.POST.get('j_ip')
        j_contact = request.POST.get('j_contact')
        j_rule = request.POST.get('j_rule')
        j_json = request.POST.get('j_json')
        j_json_array = request.POST.get('j_json_array')
        j_json_variable = request.POST.get('j_json_variable')
        j_parameter = request.POST.get('j_parameter')
        j_level = request.POST.get('j_level')
        j_route = request.POST.get('j_route')
        j_comment = request.POST.get('j_comment')

        if is_super_user(request):
            #j_dept = request.POST.getlist('j_dept')
            monit_info = [j_name, j_header, j_url, j_ip, j_contact, j_rule, j_json, j_json_array, j_json_variable, j_parameter, j_level, j_route, j_comment]
        elif is_group_admin(request):
            j_dept = request.POST.get('j_dept')
            monit_info = [j_name, j_header, j_url, j_ip, j_contact, j_rule, j_json, j_json_array, j_json_variable, j_parameter, j_level, j_route, j_comment]

        if is_group_admin(request) and not validate(request, asset_group=j_contact):
            return httperror(request, u'添加失败,您无权操作!')

        if Monit.objects.filter(name=str(j_name)):
            emg = u'该监控名 %s 已存在!' % j_name
            return my_render('hmonit/monit_add.html', locals(), request)
        db_monit_insert(monit_info)
        smg = u'监控 %s 添加成功' % j_name

    return my_render('hmonit/monit_add.html', locals(), request)


@require_admin
def monit_add_batch(request):
    """ 批量添加监控 """
    header_title, path1, path2 = u'批量添加监控', u'监控管理', u'批量添加监控'
    #login_types = {'SSH': 'S', 'TELNET': 'T'}
    rule_types = {'激活': 1, '禁用': 0}
    json_types = {'是': 1, '否': 0}
    level_types = {'高': 0, '中': 2, '低': 4, '最低': 9}
    route_types = {'UP': 1, 'DOWN': 0}
    #dept_id = get_user_dept(request)
    if request.method == 'POST':
        multi_hosts = request.POST.get('j_multi').splitlines()
        for host in multi_hosts:
            if host == '':
                break
            j_name, j_header, j_url, j_ip, j_contact, j_rule, j_json, j_json_array, j_json_variable, j_parameter, j_level, j_route, j_comment = host.split(',')
            
            j_rule = rule_types[str(j_rule)]
            j_json = json_types[str(j_json)]
            j_level = level_types[str(j_level)]
            j_route = route_types[str(j_route)]

            contact = UserGroup.objects.filter(name=j_contact)
            if contact:
                j_contact = contact[0].id
            else:
                return httperror(request, '添加失败, 没有%s这个报警组' % j_contact)

            if Monit.objects.filter(name=str(j_name)):
                return httperror(request, '该监控名 %s已存在' % j_name)
           
            monit_info = [j_name, j_header, j_url, j_ip, str(j_contact), j_rule, j_json, j_json_array, j_json_variable, j_parameter, j_level, j_route, j_comment]
            db_monit_insert(monit_info)

        smg = u'批量添加添加成功'
        return my_render('hmonit/monit_add_multi.html', locals(), request)

    return my_render('hmonit/monit_add_multi.html', locals(), request)


@require_login
def monit_list(request):
    """ 列出监控 """
    header_title, path1, path2 = u'查看监控', u'监控管理', u'查看监控'
    keyword = request.GET.get('keyword', '')
    #dept_id = get_session_user_info(request)[3]
    #dept = DEPT.objects.get(id=dept_id)
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    user_id = get_session_user_info(request)[0]

    post_all = Monit.objects.all().order_by('ip')
    post_keyword_all = Monit.objects.filter(Q(name__contains=keyword) |
                                            Q(comment__contains=keyword)).distinct().order_by('ip')
    if did:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        if is_group_admin(request):
            user, dept = get_session_user_dept(request)
        else:
            dept = DEPT.objects.get(id=did)
        posts = dept.asset_set.all()
        return my_render('hmonit/monit_list_nop.html', locals(), request)

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
        return my_render('hmonit/monit_list_nop.html', locals(), request)

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
        return my_render('hmonit/monit_list_nop.html', locals(), request)

    else:
        if is_super_user(request):
            if keyword:
                posts = post_keyword_all
            else:
                posts = post_all
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_list.html', locals(), request)

        elif is_group_admin(request):
            if keyword:
                posts = post_keyword_all.filter(dept=dept)
            else:
                posts = post_all.filter(dept=dept)

            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_list.html', locals(), request)

        elif is_common_user(request):
            user_id, username = get_session_user_info(request)[0:2]
            posts = user_perm_asset_api(username)
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_list_common.html', locals(), request)


@require_admin
def monit_del(request, offset):
    """ 删除监控 """
    if offset == 'multi':
        len_list = request.POST.get("len_list")
        for i in range(int(len_list)):
            key = "id_list[" + str(i) + "]"
            host_id = request.POST.get(key)
            db_monit_delete(request, host_id)
    else:
        db_monit_delete(request, offset)

    return HttpResponseRedirect('/hmonit/monit_list/')


@require_super_user
def monit_edit(request):
    """ 修改监控 """
    header_title, path1, path2 = u'修改监控', u'监控管理', u'修改监控'
    mcontact = UserGroup.objects.exclude(name='ALL')
    egroup = BisGroup.objects.exclude(name='ALL')
    host_id = request.GET.get('id', '')
    post = Monit.objects.filter(id=int(host_id))
    if post:
        post = post[0]
    else:
        return httperror(request, '没有此监控!')
    
    if request.method == 'POST':
        j_name = request.POST.get('j_name', '')
        j_header = request.POST.get('j_header', '')
        j_url = request.POST.get('j_url', '')
        j_ip = request.POST.get('j_ip', '')
        j_contact = request.POST.get('j_contact', '')
        j_rule = request.POST.get('j_rule', '')
        j_json = request.POST.get('j_json', '')
        j_json_array = request.POST.get('j_json_array', '')
        j_json_variable = request.POST.get('j_json_variable', '')
        j_parameter = request.POST.get('j_parameter', '')
        j_level = request.POST.get('j_level', '')
        j_route = request.POST.get('j_route', '')
        j_comment = request.POST.get('j_comment', '')

	#if is_super_user(request):
        monit_info = [j_name, j_header, j_url, j_ip, j_contact, j_rule, j_json, j_json_array, j_json_variable, j_parameter, j_level, j_route, j_comment, post]
    #    elif is_group_admin(request):
    #        j_dept = request.POST.get('j_dept')
    #        monit_info = [j_name, j_header, j_url, j_ip, j_contact, j_rule, j_json, j_json_array, j_json_variable, j_parameter, j_level, j_route, j_comment, post]

    #    if is_group_admin(request) and not validate(request, asset_group=j_contact):
    #        return httperror(request, u'添加失败,您无权操作!')
        
        db_monit_update(monit_info)

        smg = u'监控 %s 修改成功' % j_name
        return HttpResponseRedirect('/hmonit/monit_detail/?id=%s' % host_id)

    return my_render('hmonit/monit_edit.html', locals(), request)


@require_admin
def monit_edit_adm(request):
    """ 部门管理员修改监控 """
    header_title, path1, path2 = u'修改监控', u'监控管理', u'修改监控'
    actives = {1: u'激活', 0: u'禁用'}
    login_types = {'S': 'SSH', 'T': 'TELNET'}
    eidc = IDC.objects.all()
    dept = get_session_user_info(request)[5]
    egroup = BisGroup.objects.exclude(name='ALL').filter(dept=dept)
    host_id = request.GET.get('id', '')
    post = Monit.objects.filter(id=int(host_id))
    if post:
        post = post[0]
    else:
        return httperror(request, '没有此监控!')

    e_group = post.bis_group.all()

    if request.method == 'POST':
        j_ip = request.POST.get('j_ip')
        j_public_ip = request.POST.get('j_public_ip', '')
        j_manage_ip = request.POST.get('j_manage_ip', '')
        j_idc = request.POST.get('j_idc')
        j_Manufacturer = request.POST.get('j_Manufacturer', '')
        j_os = request.POST.get('j_os', '')
        j_sn = request.POST.get('j_sn', '')
        j_port = request.POST.get('j_port')
        j_type = request.POST.get('j_type')
        j_dept = request.POST.getlist('j_dept')
        j_group = request.POST.getlist('j_group')
        j_active = request.POST.get('j_active')
        j_comment = request.POST.get('j_comment')

        host_info = [j_ip, j_public_ip, j_manage_ip, j_port, j_idc, j_type, j_group, j_dept, j_Manufacturer, j_os, j_sn, j_active, j_comment]

        if not validate(request, asset_group=j_group, edept=j_dept):
            emg = u'修改失败,您无权操作!'
            return my_render('hmonit/monit_edit.html', locals(), request)

        if j_type == 'M':
            j_user = request.POST.get('j_user')
            j_password = request.POST.get('j_password')
            db_host_update(host_info, j_user, j_password, post)
        else:
            db_host_update(host_info, post)

        smg = u'监控 %s 修改成功' % j_ip
        return HttpResponseRedirect('/hmonit/monit_detail/?id=%s' % host_id)

    return my_render('hmonit/monit_edit.html', locals(), request)


@require_login
def monit_detail(request):
    """ 监控详情 """
    header_title, path1, path2 = u'监控详细信息', u'监控管理', u'监控详情'
    host_id = request.GET.get('id', '')
    post = Monit.objects.filter(id=host_id)
    if not post:
        return httperror(request, '没有此监控!')
    post = post[0]

    if is_group_admin(request) and not validate(request, asset=[host_id]):
        return httperror(request, '您无权查看!')

    elif is_common_user(request):
        username = get_session_user_info(request)[1]
        user_permed_hosts = user_perm_asset_api(username)
        if post not in user_permed_hosts:
            return httperror(request, '您无权查看!')
    else:
        log_all = Log.objects.filter(host=post.ip)
        log, log_more = log_all[:10], log_all[10:]
        user_permed_list = monit_perm_api(post)

    return my_render('hmonit/monit_detail.html', locals(), request)


@require_super_user
#def idc_add(request):
#    """ 添加IDC """
#    header_title, path1, path2 = u'添加IDC', u'监控管理', u'添加IDC'
#    if request.method == 'POST':
#        j_idc = request.POST.get('j_idc')
#        j_comment = request.POST.get('j_comment')
#        if IDC.objects.filter(name=j_idc):
#            emg = u'该IDC已存在!'
#            return my_render('hmonit/idc_add.html', locals(), request)
#        else:
#            smg = u'IDC:%s添加成功' % j_idc
#            IDC.objects.create(name=j_idc, comment=j_comment)
#
#    return my_render('hmonit/idc_add.html', locals(), request)
#
#
#@require_admin
#def idc_list(request):
#    """ 列出IDC """
#    header_title, path1, path2 = u'查看IDC', u'监控管理', u'查看IDC'
#    dept_id = get_user_dept(request)
#    dept = DEPT.objects.get(id=dept_id)
#    keyword = request.GET.get('keyword', '')
#    if keyword:
#        posts = IDC.objects.filter(Q(name__contains=keyword) | Q(comment__contains=keyword))
#    else:
#        posts = IDC.objects.exclude(name='ALL').order_by('id')
#    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
#    return my_render('hmonit/idc_list.html', locals(), request)
#
#
#@require_super_user
#def idc_edit(request):
#    """ 修改IDC """
#    header_title, path1, path2 = u'编辑IDC', u'监控管理', u'编辑IDC'
#    idc_id = request.GET.get('id', '')
#    idc = IDC.objects.filter(id=idc_id)
#    if int(idc_id) == 1:
#        return httperror(request, u'默认IDC不能编辑!')
#    if idc:
#        idc = idc[0]
#        default = IDC.objects.get(id=1).asset_set.all()
#        eposts = Monit.objects.filter(idc=idc).order_by('ip')
#        posts = [g for g in default if g not in eposts]
#    else:
#        return httperror(request, u'此IDC不存在')
#
#    if request.method == 'POST':
#        idc_id = request.POST.get('id')
#        j_idc = request.POST.get('j_idc')
#        j_hosts = request.POST.getlist('j_hosts')
#        j_comment = request.POST.get('j_comment')
#        idc_default = request.POST.getlist('idc_default')
#
#        idc = IDC.objects.filter(id=idc_id)
#        if idc:
#            idc.update(name=j_idc, comment=j_comment)
#            for host_id in j_hosts:
#                Monit.objects.filter(id=host_id).update(idc=idc[0])
#
#            i = IDC.objects.get(id=1)
#            for host in idc_default:
#                g = Monit.objects.filter(id=host).update(idc=i)
#        else:
#            return httperror(request, u'此IDC不存在')
#
#        return HttpResponseRedirect('/hmonit/idc_list/?id=%s' % idc_id)
#
#    return my_render('hmonit/idc_edit.html', locals(), request)
#
#
#@require_admin
#def idc_detail(request):
#    """ IDC详情 """
#    header_title, path1, path2 = u'IDC详情', u'监控管理', u'IDC详情'
#    login_types = {'S': 'SSH', 'T': 'TELNET'}
#    idc_id = request.GET.get('id', '')
#    idc_filter = IDC.objects.filter(id=idc_id)
#    if idc_filter:
#        idc = idc_filter[0]
#    else:
#        return httperror(request, '没有此IDC')
#    dept = get_session_user_info(request)[5]
#    if is_super_user(request):
#        posts = Monit.objects.filter(idc=idc).order_by('ip')
#    elif is_group_admin(request):
#        posts = Monit.objects.filter(idc=idc, dept=dept).order_by('ip')
#    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
#
#    return my_render('hmonit/idc_detail.html', locals(), request)
#
#
#@require_super_user
#def idc_del(request):
#    """ 删除IDC """
#    offset = request.GET.get('id', '')
#    if offset == 'multi':
#        len_list = request.POST.get("len_list")
#        for i in range(int(len_list)):
#            key = "id_list[" + str(i) + "]"
#            idc_id = request.POST.get(key)
#            db_idc_delete(request, int(idc_id))
#    else:
#        db_idc_delete(request, int(offset))
#    return HttpResponseRedirect('/hmonit/idc_list/')
#
#
#@require_admin
#def group_add(request):
#    """ 添加监控组 """
#    header_title, path1, path2 = u'添加监控组', u'监控管理', u'添加监控组'
#    if is_super_user(request):
#        posts = Monit.objects.all()
#        edept = DEPT.objects.all()
#    elif is_group_admin(request):
#        dept_id = get_user_dept(request)
#        dept = DEPT.objects.get(id=dept_id)
#        posts = Monit.objects.filter(dept=dept)
#        edept = get_session_user_info(request)[5]
#
#    if request.method == 'POST':
#        j_group = request.POST.get('j_group', '')
#        j_dept = request.POST.get('j_dept', '')
#        j_hosts = request.POST.getlist('j_hosts', '')
#        j_comment = request.POST.get('j_comment', '')
#
#        try:
#            if is_group_admin(request) and not validate(request, asset=j_hosts, edept=[j_dept]):
#                emg = u'添加失败, 您无权操作!'
#                raise RaiseError
#
#            elif BisGroup.objects.filter(name=j_group):
#                emg = u'添加失败, 该监控组已存在!'
#                raise RaiseError
#
#        except RaiseError:
#            pass
#
#        else:
#            j_dept = DEPT.objects.filter(id=j_dept)[0]
#            group = BisGroup.objects.create(name=j_group, dept=j_dept, comment=j_comment)
#            for host in j_hosts:
#                g = Monit.objects.get(id=host)
#                group.asset_set.add(g)
#            smg = u'监控组 %s 添加成功' % j_group
#
#    return my_render('hmonit/group_add.html', locals(), request)
#
#
#@require_admin
#def group_list(request):
#    """ 列出监控组 """
#    header_title, path1, path2 = u'查看监控组', u'监控管理', u'查看监控组'
#    dept_id = get_user_dept(request)
#    dept = DEPT.objects.get(id=dept_id)
#    keyword = request.GET.get('keyword', '')
#    gid = request.GET.get('gid')
#    sid = request.GET.get('sid')
#    if gid:
#        if is_common_user(request):
#            return httperror(request, u'您无权查看!')
#
#        elif is_group_admin(request) and not validate(request, user_group=[gid]):
#            return httperror(request, u'您无权查看!')
#
#        posts = []
#        user_group = UserGroup.objects.filter(id=gid)
#        if user_group:
#            user_group = user_group[0]
#            perms = Perm.objects.filter(user_group=user_group)
#            for perm in perms:
#                posts.append(perm.asset_group)
#
#    elif sid:
#        if is_common_user(request):
#            return httperror(request, u'您无权查看!')
#
#        elif is_group_admin(request) and not validate(request, user_group=[sid]):
#            return httperror(request, u'您无权查看!')
#
#        posts = []
#        user_group = UserGroup.objects.filter(id=sid)
#        if user_group:
#            user_group = user_group[0]
#            for perm in user_group.sudoperm_set.all():
#                posts.extend(perm.asset_group.all())
#            posts = list(set(posts))
#        else:
#            return httperror(request, u'没有此sudo授权!')
#
#    else:
#        if is_super_user(request):
#            if keyword:
#                posts = BisGroup.objects.exclude(name='ALL').filter(
#                    Q(name__contains=keyword) | Q(comment__contains=keyword))
#            else:
#                posts = BisGroup.objects.exclude(name='ALL').order_by('id')
#        elif is_group_admin(request):
#            if keyword:
#                posts = BisGroup.objects.filter(Q(name__contains=keyword) | Q(comment__contains=keyword)).filter(
#                    dept=dept)
#            else:
#                posts = BisGroup.objects.filter(dept=dept).order_by('id')
#    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
#    return my_render('hmonit/group_list.html', locals(), request)
#
#
#@require_admin
#def group_edit(request):
#    """ 修改监控组 """
#    header_title, path1, path2 = u'编辑监控组', u'监控管理', u'编辑监控组'
#    group_id = request.GET.get('id', '')
#    group = BisGroup.objects.filter(id=group_id)
#    if group:
#        group = group[0]
#    else:
#        httperror(request, u'没有这个监控组!')
#
#    host_all = Monit.objects.all()
#    dept_id = get_session_user_info(request)[3]
#    eposts = Monit.objects.filter(bis_group=group)
#
#    if is_group_admin(request) and not validate(request, asset_group=[group_id]):
#        return httperror(request, '编辑失败, 您无权操作!')
#    dept = DEPT.objects.filter(id=group.dept.id)
#    if dept:
#        dept = dept[0]
#    else:
#        return httperror(request, u'没有这个部门!')
#
#    all_dept = dept.asset_set.all()
#    posts = [g for g in all_dept if g not in eposts]
#
#    if request.method == 'POST':
#        j_group = request.POST.get('j_group', '')
#        j_hosts = request.POST.getlist('j_hosts', '')
#        j_dept = request.POST.get('j_dept', '')
#        j_comment = request.POST.get('j_comment', '')
#
#        j_dept = DEPT.objects.filter(id=int(j_dept))
#        j_dept = j_dept[0]
#
#        group.asset_set.clear()
#        for host in j_hosts:
#            g = Monit.objects.get(id=host)
#            group.asset_set.add(g)
#        BisGroup.objects.filter(id=group_id).update(name=j_group, dept=j_dept, comment=j_comment)
#        smg = u'监控组%s修改成功' % j_group
#        return HttpResponseRedirect('/hmonit/group_list')
#
#    return my_render('hmonit/group_edit.html', locals(), request)
#
#
#@require_admin
#def group_detail(request):
#    """ 监控组详情 """
#    header_title, path1, path2 = u'监控组详情', u'监控管理', u'监控组详情'
#    login_types = {'S': 'SSH', 'T': 'TELNET'}
#    dept = get_session_user_info(request)[5]
#    group_id = request.GET.get('id', '')
#    group = BisGroup.objects.get(id=group_id)
#    if is_super_user(request):
#        posts = Monit.objects.filter(bis_group=group).order_by('ip')
#
#    elif is_group_admin(request):
#        if not validate(request, asset_group=[group_id]):
#            return httperror(request, u'您无权查看!')
#        posts = Monit.objects.filter(bis_group=group).filter(dept=dept).order_by('ip')
#
#    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
#    return my_render('hmonit/group_detail.html', locals(), request)
#
#
#@require_admin
#def group_del_host(request):
#    """ 监控组中剔除监控, 并不删除真实监控 """
#    if request.method == 'POST':
#        group_id = request.POST.get('group_id')
#        offset = request.GET.get('id', '')
#        group = BisGroup.objects.get(id=group_id)
#        if offset == 'group':
#            len_list = request.POST.get("len_list")
#            for i in range(int(len_list)):
#                key = "id_list[" + str(i) + "]"
#                jid = request.POST.get(key)
#                g = Monit.objects.get(id=jid)
#                group.asset_set.remove(g)
#
#    else:
#        offset = request.GET.get('id', '')
#        group_id = request.GET.get('gid', '')
#        group = BisGroup.objects.get(id=group_id)
#        g = Monit.objects.get(id=offset)
#        group.asset_set.remove(g)
#
#    return HttpResponseRedirect('/hmonit/group_detail/?id=%s' % group.id)
#
#
#@require_admin
#def group_del(request):
#    """ 删除监控组 """
#    offset = request.GET.get('id', '')
#    if offset == 'multi':
#        len_list = request.POST.get("len_list")
#        for i in range(int(len_list)):
#            key = "id_list[" + str(i) + "]"
#            gid = request.POST.get(key)
#            if is_group_admin(request) and not validate(request, asset_group=[gid]):
#                return httperror(request, '删除失败, 您无权删除!')
#            BisGroup.objects.filter(id=gid).delete()
#    else:
#        gid = int(offset)
#        if is_group_admin(request) and not validate(request, asset_group=[gid]):
#            return httperror(request, '删除失败, 您无权删除!')
#        BisGroup.objects.filter(id=gid).delete()
#    return HttpResponseRedirect('/hmonit/group_list/')
#

@require_admin
def dept_host_ajax(request):
    """ 添加监控组时, 部门联动监控异步 """
    dept_id = request.GET.get('id', '')
    if dept_id not in ['1', '2']:
        dept = DEPT.objects.filter(id=dept_id)
        if dept:
            dept = dept[0]
            hosts = dept.asset_set.all()
    else:
        hosts = Monit.objects.all()

    return my_render('hmonit/dept_host_ajax.html', locals(), request)


def show_all_ajax(request):
    """ 批量修改监控时, 部门和组全部显示 """
    env = request.GET.get('env', '')
    get_id = request.GET.get('id', '')
    host = Monit.objects.filter(id=get_id)
    if host:
        host = host[0]
    return my_render('hmonit/show_all_ajax.html', locals(), request)


@require_login
def monit_search(request):
    """ 搜索监控 """
    keyword = request.GET.get('keyword')
    login_types = {'S': 'SSH', 'T': 'TELNET'}
    dept = get_session_user_info(request)[5]
    post_all = Monit.objects.filter(Q(name__contains=keyword) |
                                    Q(header__contains=keyword) |
                                    Q(contact__name__contains=keyword) |
                                    Q(comment__contains=keyword)).distinct().order_by('name')

    if is_super_user(request):
        posts = post_all

    elif is_group_admin(request):
        posts = post_all.filter(dept=dept)

    elif is_common_user(request):
        user_id, username = get_session_user_info(request)[0:2]
        post_perm = user_perm_asset_api(username)
        posts = list(set(post_all) & set(post_perm))

    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('hmonit/monit_search.html', locals(), request)



@require_login
def monit_iplist(request):
    """ 列出报警 """
    header_title, path1, path2 = u'查看报警', u'监控管理', u'查看报警'
    keyword = request.GET.get('keyword', '')
    #dept_id = get_session_user_info(request)[3]
    #dept = DEPT.objects.get(id=dept_id)
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    user_id = get_session_user_info(request)[0]

    post_all = IP_Status.objects.filter(status=0).distinct().order_by('ip')
    #post_all = IP_Alarm_Status.objects.filter(status=0)
    post_keyword_all = IP_Status.objects.filter(status=0).distinct().order_by('ip')
    #post_keyword_all = IP_Alarm_Status.objects.filter(status=0)
    if did:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        if is_group_admin(request):
            user, dept = get_session_user_dept(request)
        else:
            dept = DEPT.objects.get(id=did)
        posts = dept.asset_set.all()
        return my_render('hmonit/monit_iplist_nop.html', locals(), request)

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
        return my_render('hmonit/monit_iplist_nop.html', locals(), request)

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
        return my_render('hmonit/monit_iplist_nop.html', locals(), request)

    else:
        if is_super_user(request):
            if keyword:
                posts = post_keyword_all
            else:
                posts = post_all
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_iplist.html', locals(), request)

        elif is_group_admin(request):
            if keyword:
                posts = post_keyword_all.filter(dept=dept)
            else:
                posts = post_all.filter(dept=dept)

            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_iplist.html', locals(), request)

        elif is_common_user(request):
            user_id, username = get_session_user_info(request)[0:2]
            posts = user_perm_asset_api(username)
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_iplist_common.html', locals(), request)



@require_login
def monit_urllist(request):
    """ URL详情 """
    header_title, path1, path2 = u'URL详细信息', u'监控管理', u'URL详情'
    keyword = request.GET.get('keyword', '')
    host_id = request.GET.get('id', '')
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    user_id = get_session_user_info(request)[0]

    post_all = Monit.objects.filter(name=host_id)
    post_keyword_all = Monit.objects.filter(name=host_id)

    #post_all = Monit.objects.filter(name=host_id)
    #post_keyword_all = Monit.objects.filter(name=host_id)
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
        return my_render('hmonit/monit_urllist_nop.html', locals(), request)

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
        return my_render('hmonit/monit_urllist_nop.html', locals(), request)

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
        return my_render('hmonit/monit_urllist_nop.html', locals(), request)

    else:
        if is_super_user(request):
            if keyword:
                posts = post_keyword_all
            else:
                posts = post_all
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_urllist.html', locals(), request)

        elif is_group_admin(request):
            if keyword:
                posts = post_keyword_all.filter(dept=dept)
            else:
                posts = post_all.filter(dept=dept)

            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_urllist.html', locals(), request)

        elif is_common_user(request):
            user_id, username = get_session_user_info(request)[0:2]
            posts = user_perm_asset_api(username)
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_urllist_common.html', locals(), request)


@require_login
def monit_alarmlist(request):
    """ URL详情 """
    header_title, path1, path2 = u'URL详细信息', u'监控管理', u'URL详情'
    keyword = request.GET.get('keyword', '')
    host_id = request.GET.get('id', '')
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    user_id = get_session_user_info(request)[0]

    post_all = WEB_Alarm_Status.objects.filter(status=0)
    post_keyword_all = WEB_Alarm_Status.objects.filter(status=0)

    if did:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        if is_group_admin(request):
            user, dept = get_session_user_dept(request)
        else:
            dept = DEPT.objects.get(id=did)
        posts = dept.asset_set.all()
        return my_render('hmonit/monit_urllist_nop.html', locals(), request)

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
        return my_render('hmonit/monit_urllist_nop.html', locals(), request)

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
        return my_render('hmonit/monit_urllist_nop.html', locals(), request)

    else:
        if is_super_user(request):
            if keyword:
                posts = post_keyword_all
            else:
                posts = post_all
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_alarmlist.html', locals(), request)

        elif is_group_admin(request):
            if keyword:
                posts = post_keyword_all.filter(dept=dept)
            else:
                posts = post_all.filter(dept=dept)

            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_alarmlist.html', locals(), request)

        elif is_common_user(request):
            user_id, username = get_session_user_info(request)[0:2]
            posts = user_perm_asset_api(username)
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_urllist_common.html', locals(), request)

@require_login
def monit_urllist1(request):
    """ URL详情 """
    header_title, path1, path2 = u'URL详细信息', u'监控管理', u'URL详情'
    keyword = request.GET.get('keyword', '')
    host_id = request.GET.get('id', '')
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    user_id = get_session_user_info(request)[0]

    post_all = WEB_Alarm_Status.objects.filter(name=host_id)
    post_keyword_all = WEB_Alarm_Status.objects.filter(name=host_id)

    #post_all = Monit.objects.filter(name=host_id)
    #post_keyword_all = Monit.objects.filter(name=host_id)
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
        return my_render('hmonit/monit_urllist_nop.html', locals(), request)

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
        return my_render('hmonit/monit_urllist_nop.html', locals(), request)

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
        return my_render('hmonit/monit_urllist_nop.html', locals(), request)

    else:
        if is_super_user(request):
            if keyword:
                posts = post_keyword_all
            else:
                posts = post_all
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_urllist1.html', locals(), request)

        elif is_group_admin(request):
            if keyword:
                posts = post_keyword_all.filter(dept=dept)
            else:
                posts = post_all.filter(dept=dept)

            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_urllist1.html', locals(), request)

        elif is_common_user(request):
            user_id, username = get_session_user_info(request)[0:2]
            posts = user_perm_asset_api(username)
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_urllist_common.html', locals(), request)


@require_login
def monit_errorlog_search(request):
    """ 搜索日志 """
    keyword = request.GET.get('keyword')
    login_types = {'S': 'SSH', 'T': 'TELNET'}
    dept = get_session_user_info(request)[5]
    post_all = WEB_Logs.objects.filter(Q(name__contains=keyword) |
                                    Q(header__contains=keyword) |
                                    Q(contact__name__contains=keyword) |
                                    Q(comment__contains=keyword)).distinct().order_by('name')

    if is_super_user(request):
        posts = post_all

    elif is_group_admin(request):
        posts = post_all.filter(dept=dept)

    elif is_common_user(request):
        user_id, username = get_session_user_info(request)[0:2]
        post_perm = user_perm_asset_api(username)
        posts = list(set(post_all) & set(post_perm))

    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('hmonit/monit_errorlog_search.html', locals(), request)


@require_admin
def monit_alarmdel(request, offset):
    """ 删除监控 """
    if offset == 'multi':
        len_list = request.POST.get("len_list")
        for i in range(int(len_list)):
            key = "id_list[" + str(i) + "]"
            host_id = request.POST.get(key)
            db_alarm_delete(request, host_id)
    else:
        db_alarm_delete(request, offset)

    return HttpResponseRedirect('/hmonit/monit_alarmlist/')


@require_admin
def db_alarm_delete(request, host_id):
    """ 删除监控操作 """
    if is_group_admin(request) and not validate(request, asset=[host_id]):
        return httperror(request, '删除失败, 您无权删除!')

    asset = WEB_Alarm_Status.objects.filter(id=host_id)
    if asset:
        asset.delete()
    else:
        return httperror(request, '删除失败, 没有此监控!')

@require_login
def monit_dnslist(request):
    """ 列出监控 """
    header_title, path1, path2 = u'查看监控', u'监控管理', u'查看监控'
    keyword = request.GET.get('keyword', '')
    #dept_id = get_session_user_info(request)[3]
    #dept = DEPT.objects.get(id=dept_id)
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    user_id = get_session_user_info(request)[0]

    post_all = Dnspod.objects.all().order_by('name')
    post_keyword_all = Dnspod.objects.filter(Q(name__contains=keyword)).distinct().order_by('name')
    if did:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        if is_group_admin(request):
            user, dept = get_session_user_dept(request)
        else:
            dept = DEPT.objects.get(id=did)
        posts = dept.asset_set.all()
        return my_render('hmonit/monit_dnslist_nop.html', locals(), request)

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
        return my_render('hmonit/monit_dnslist_nop.html', locals(), request)

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
        return my_render('hmonit/monit_dnslist_nop.html', locals(), request)

    else:
        if is_super_user(request):
            if keyword:
                posts = post_keyword_all
            else:
                posts = post_all
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_dnslist.html', locals(), request)

        elif is_group_admin(request):
            if keyword:
                posts = post_keyword_all.filter(dept=dept)
            else:
                posts = post_all.filter(dept=dept)

            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_dnslist.html', locals(), request)

        elif is_common_user(request):
            user_id, username = get_session_user_info(request)[0:2]
            posts = user_perm_asset_api(username)
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_dnslist_common.html', locals(), request)

@require_login
def monit_dnstail(request):
    """ 监控详情 """
    header_title, path1, path2 = u'监控详细信息', u'监控管理', u'监控详情'
    host_id = request.GET.get('id', '')
    post = Dnspod.objects.filter(id=host_id)
    if not post:
        return httperror(request, '没有此监控!')
    post = post[0]

    if is_group_admin(request) and not validate(request, asset=[host_id]):
        return httperror(request, '您无权查看!')

    elif is_common_user(request):
        username = get_session_user_info(request)[1]
        #user_permed_hosts = user_perm_asset_api(username)
        if post not in user_permed_hosts:
            return httperror(request, '您无权查看!')
    else:
        log_all = Log.objects.filter(host=post.ip)
        log, log_more = log_all[:10], log_all[10:]
        #user_permed_list = monit_perm_api(post)

    return my_render('hmonit/monit_dnstail.html', locals(), request)

@require_super_user
def monit_dnsedit(request):
    """ 修改监控 """
    header_title, path1, path2 = u'修改监控', u'监控管理', u'修改监控'
    host_id = request.GET.get('id', '')
    post = Dnspod.objects.filter(id=int(host_id))
    if post:
        post = post[0]
    else:
        return httperror(request, '没有此监控!')

    if request.method == 'POST':
        j_name = request.POST.get('j_name', '')
        j_ip = request.POST.get('j_ip', '')
        j_type = request.POST.get('j_type', '')
        j_rule = request.POST.get('j_rule', '')

        monit_info = [j_name, j_ip, j_type, j_rule, post]
        db_dnspod_update(monit_info)

        smg = u'监控 %s 修改成功' % j_name
        return HttpResponseRedirect('/hmonit/monit_dnstail/?id=%s' % host_id)

    return my_render('hmonit/monit_dnsedit.html', locals(), request)


def db_dnspod_update(monit_info):
    """ 修改监控时数据库操作函数 """
    name, ip, type, rule, dnspod = monit_info

    dnspod.name = name
    dnspod.ip = ip
    dnspod.type = type 
    dnspod.rule = rule

    dnspod.save()


@require_admin
def monit_dnsdel(request, offset):
    """ 删除监控 """
    if offset == 'multi':
        len_list = request.POST.get("len_list")
        for i in range(int(len_list)):
            key = "id_list[" + str(i) + "]"
            host_id = request.POST.get(key)
            db_dnspod_delete(request, host_id)
    else:
        db_dnspod_delete(request, offset)

    return HttpResponseRedirect('/hmonit/monit_dnslist/')


def db_dnspod_delete(request, host_id):
    """ 删除监控操作 """
    if is_group_admin(request) and not validate(request, asset=[host_id]):
        return httperror(request, '删除失败, 您无权删除!')

    asset = Dnspod.objects.filter(id=host_id)
    if asset:
        asset.delete()
    else:
        return httperror(request, '删除失败, 没有此监控!')

@require_admin
def monit_dnsadd(request):
    """ 添加监控 """
    header_title, path1, path2 = u'添加监控', u'监控管理', u'添加监控'

    if is_super_user(request):
        edept = DEPT.objects.all()
        egroup = BisGroup.objects.exclude(name='ALL')
    elif is_group_admin(request):
        dept = get_session_user_info(request)[5]
        egroup = dept.bisgroup_set.all()

    if request.method == 'POST':
        j_name = request.POST.get('j_name')
        j_ip = request.POST.get('j_ip')
        j_type = request.POST.get('j_type')
        j_rule = request.POST.get('j_rule')

        if is_super_user(request):
            monit_info = [j_name, j_ip, j_type, j_rule]
        elif is_group_admin(request):
            j_dept = request.POST.get('j_dept')
            monit_info = [j_name, j_ip, j_type, j_rule]

        if is_group_admin(request) and not validate(request, asset_group=j_contact):
            return httperror(request, u'添加失败,您无权操作!')

        if Monit.objects.filter(name=str(j_name)):
            emg = u'该监控名 %s 已存在!' % j_name
            return my_render('hmonit/monit_dnsadd.html', locals(), request)
        db_dnspod_insert(monit_info)
        smg = u'监控 %s 添加成功' % j_name

    return my_render('hmonit/monit_dnsadd.html', locals(), request)

def db_dnspod_insert(monit_info):
    """ 添加监控时数据库操作函数 """
    name, ip, type, rule = monit_info
    a = Dnspod(name=name, ip=ip, type=int(type), rule=int(rule))
    a.save()

@require_login
def monit_dnsalarmlist(request):
    """ DNS详情 """
    header_title, path1, path2 = u'DNS详细信息', u'监控管理', u'DNS详情'
    keyword = request.GET.get('keyword', '')
    host_id = request.GET.get('id', '')
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    user_id = get_session_user_info(request)[0]

    post_all = Dnspod_Alarm.objects.filter(status=0)
    post_keyword_all = Dnspod_Alarm.objects.filter(status=0)

    if did:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        if is_group_admin(request):
            user, dept = get_session_user_dept(request)
        else:
            dept = DEPT.objects.get(id=did)
        posts = dept.asset_set.all()
        return my_render('hmonit/monit_dnslist_nop.html', locals(), request)

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
        return my_render('hmonit/monit_dnslist_nop.html', locals(), request)

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
        return my_render('hmonit/monit_dnslist_nop.html', locals(), request)

    else:
        if is_super_user(request):
            if keyword:
                posts = post_keyword_all
            else:
                posts = post_all
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_dnsalarmlist.html', locals(), request)

        elif is_group_admin(request):
            if keyword:
                posts = post_keyword_all.filter(dept=dept)
            else:
                posts = post_all.filter(dept=dept)

            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_dnsalarmlist.html', locals(), request)

        elif is_common_user(request):
            user_id, username = get_session_user_info(request)[0:2]
            posts = user_perm_asset_api(username)
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_dnslist_common.html', locals(), request)

@require_admin
def monit_dnsalarmdel(request, offset):
    """ 删除监控 """
    if offset == 'multi':
        len_list = request.POST.get("len_list")
        for i in range(int(len_list)):
            key = "id_list[" + str(i) + "]"
            host_id = request.POST.get(key)
            db_dnsalarm_delete(request, host_id)
    else:
        db_dnsalarm_delete(request, offset)

    return HttpResponseRedirect('/hmonit/monit_dnsalarmlist/')

@require_admin
def db_dnsalarm_delete(request, host_id):
    """ 删除监控操作 """
    if is_group_admin(request) and not validate(request, asset=[host_id]):
        return httperror(request, '删除失败, 您无权删除!')

    asset = Dnspod_Alarm.objects.filter(id=host_id)
    if asset:
        asset.delete()
    else:
        return httperror(request, '删除失败, 没有此监控!')


@require_login
def monit_portlist(request):
    """ 列出监控 """
    header_title, path1, path2 = u'查看监控', u'监控管理', u'查看监控'
    keyword = request.GET.get('keyword', '')
    #dept_id = get_session_user_info(request)[3]
    #dept = DEPT.objects.get(id=dept_id)
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    user_id = get_session_user_info(request)[0]

    post_all = Port.objects.all().order_by('ip')
    post_keyword_all = Port.objects.filter(Q(ip__contains=keyword)).distinct().order_by('ip')
    if did:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        if is_group_admin(request):
            user, dept = get_session_user_dept(request)
        else:
            dept = DEPT.objects.get(id=did)
        posts = dept.asset_set.all()
        return my_render('hmonit/monit_portlist_nop.html', locals(), request)

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
        return my_render('hmonit/monit_portlist_nop.html', locals(), request)

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
        return my_render('hmonit/monit_portlist_nop.html', locals(), request)

    else:
        if is_super_user(request):
            if keyword:
                posts = post_keyword_all
            else:
                posts = post_all
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_portlist.html', locals(), request)

        elif is_group_admin(request):
            if keyword:
                posts = post_keyword_all.filter(dept=dept)
            else:
                posts = post_all.filter(dept=dept)

            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_portlist.html', locals(), request)

        elif is_common_user(request):
            user_id, username = get_session_user_info(request)[0:2]
            posts = user_perm_asset_api(username)
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_portlist_common.html', locals(), request)

@require_admin
def monit_portadd(request):
    """ 添加监控 """
    header_title, path1, path2 = u'添加监控', u'监控管理', u'添加监控'
    mcontact = UserGroup.objects.exclude(name='ALL')

    if is_super_user(request):
        edept = DEPT.objects.all()
        egroup = BisGroup.objects.exclude(name='ALL')
    elif is_group_admin(request):
        dept = get_session_user_info(request)[5]
        egroup = dept.bisgroup_set.all()

    if request.method == 'POST':
        j_ip = request.POST.get('j_ip')
        j_port = request.POST.get('j_port')
        j_contact = request.POST.get('j_contact')
        j_rule = request.POST.get('j_rule')
        j_time = request.POST.get('j_time')
        j_date = request.POST.get('j_date')

        if is_super_user(request):
            monit_info = [j_ip, j_port, j_contact, j_rule, j_time, j_date]
        elif is_group_admin(request):
            j_dept = request.POST.get('j_dept')
            monit_info = [j_ip, j_port, j_contact, j_rule, j_time, j_date]

        if is_group_admin(request) and not validate(request, asset_group=j_contact):
            return httperror(request, u'添加失败,您无权操作!')

        if Port.objects.filter(ip=str(j_ip)):
	    emg = u'该监控IP %s 已存在!' % j_ip
            return my_render('hmonit/monit_portadd.html', locals(), request)
        db_port_insert(monit_info)
        smg = u'监控 %s 添加成功' % j_ip

    return my_render('hmonit/monit_portadd.html', locals(), request)

def db_port_insert(monit_info):
    """ 添加监控时数据库操作函数 """
    ip, port, contact, rule, time, date = monit_info
    a = Port(ip=ip, port=port, 
              rule=int(rule),
              time=time,
              date=date)
    a.save()

    a.contact = contact

    a.save()

@require_login
def monit_porttail(request):
    """ 监控详情 """
    header_title, path1, path2 = u'监控详细信息', u'监控管理', u'监控详情'
    host_id = request.GET.get('id', '')
    post = Port.objects.filter(id=host_id)
    if not post:
        return httperror(request, '没有此监控!')
    post = post[0]

    if is_group_admin(request) and not validate(request, asset=[host_id]):
        return httperror(request, '您无权查看!')

    elif is_common_user(request):
        username = get_session_user_info(request)[1]
        #user_permed_hosts = user_perm_asset_api(username)
        if post not in user_permed_hosts:
            return httperror(request, '您无权查看!')
    else:
        log_all = Log.objects.filter(host=post.ip)
        log, log_more = log_all[:10], log_all[10:]
        user_permed_list = monit_perm_api(post)

    return my_render('hmonit/monit_porttail.html', locals(), request)

@require_super_user
def monit_portedit(request):
    """ 修改监控 """
    header_title, path1, path2 = u'修改监控', u'监控管理', u'修改监控'
    host_id = request.GET.get('id', '')
    mcontact = UserGroup.objects.exclude(name='ALL')
    post = Port.objects.filter(id=int(host_id))
    if post:
        post = post[0]
    else:
        return httperror(request, '没有此监控!')

    if request.method == 'POST':
        j_ip = request.POST.get('j_ip', '')
        j_port = request.POST.get('j_port', '')
        j_contact = request.POST.get('j_contact')
        j_rule = request.POST.get('j_rule')
        j_time = request.POST.get('j_time')
        j_date = request.POST.get('j_date')
        monit_info = [j_ip, j_port, j_contact, j_rule, j_time, j_date, post]
        db_port_update(monit_info)

        smg = u'监控 %s 修改成功' % j_ip
        return HttpResponseRedirect('/hmonit/monit_porttail/?id=%s' % host_id)

    return my_render('hmonit/monit_portedit.html', locals(), request)

def db_port_update(monit_info):
    """ 修改监控时数据库操作函数 """
    ip, ports, contact, rule, time, date, port = monit_info
    port.ip = ip
    port.port = ports
    port.contact = contact
    port.rule = rule 
    port.time = time
    port.date = date
 
    port.save()

@require_admin
def monit_portdel(request, offset):
    """ 删除监控 """
    if offset == 'multi':
        len_list = request.POST.get("len_list")
        for i in range(int(len_list)):
            key = "id_list[" + str(i) + "]"
            host_id = request.POST.get(key)
            db_port_delete(request, host_id)
    else:
        db_port_delete(request, offset)

    return HttpResponseRedirect('/hmonit/monit_portlist/')

@require_admin
def db_port_delete(request, host_id):
    """ 删除监控操作 """
    if is_group_admin(request) and not validate(request, asset=[host_id]):
        return httperror(request, '删除失败, 您无权删除!')

    asset = Port.objects.filter(id=host_id)
    if asset:
        asset.delete()
    else:
        return httperror(request, '删除失败, 没有此监控!')


@require_admin
def monit_iplistdel(request, offset):
    """ 删除监控 """
    if offset == 'multi':
        len_list = request.POST.get("len_list")
        for i in range(int(len_list)):
            key = "id_list[" + str(i) + "]"
            host_id = request.POST.get(key)
            db_iplist_delete(request, host_id)
    else:
        db_iplist_delete(request, offset)

    return HttpResponseRedirect('/hmonit/monit_iplist/')

@require_admin
def db_iplist_delete(request, host_id):
    """ 删除监控操作 """
    if is_group_admin(request) and not validate(request, asset=[host_id]):
        return httperror(request, '删除失败, 您无权删除!')

    asset = IP_Status.objects.filter(id=host_id)
    #asset = IP_Alarm_Status.objects.filter(id=host_id)
    if asset:
        asset.delete()
    else:
        return httperror(request, '删除失败, 没有此监控!')


@require_login
def monit_port_iplist(request):
    """ 列出监控 """
    header_title, path1, path2 = u'查看监控', u'监控管理', u'查看监控'
    keyword = request.GET.get('keyword', '')
    #dept_id = get_session_user_info(request)[3]
    #dept = DEPT.objects.get(id=dept_id)
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    user_id = get_session_user_info(request)[0]

    post_all = Port_Ip_Alarm_Status.objects.all().order_by('ip')
    post_keyword_all = Port_Ip_Alarm_Status.objects.filter(Q(ip__contains=keyword)).distinct().order_by('ip')
    if did:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        if is_group_admin(request):
            user, dept = get_session_user_dept(request)
        else:
            dept = DEPT.objects.get(id=did)
        posts = dept.asset_set.all()
        return my_render('hmonit/monit_port_iplist.html', locals(), request)

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
        return my_render('hmonit/monit_port_iplist.html', locals(), request)

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
        return my_render('hmonit/monit_port_iplist.html', locals(), request)

    else:
        if is_super_user(request):
            if keyword:
                posts = post_keyword_all
            else:
                posts = post_all
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_port_iplist.html', locals(), request)

        elif is_group_admin(request):
            if keyword:
                posts = post_keyword_all.filter(dept=dept)
            else:
                posts = post_all.filter(dept=dept)

            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_port_iplist.html', locals(), request)

        elif is_common_user(request):
            user_id, username = get_session_user_info(request)[0:2]
            posts = user_perm_asset_api(username)
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_portlist_common.html', locals(), request)


@require_login
def monit_port_list(request):
    """ 列出监控 """
    header_title, path1, path2 = u'查看监控', u'监控管理', u'查看监控'
    keyword = request.GET.get('keyword', '')
    #dept_id = get_session_user_info(request)[3]
    #dept = DEPT.objects.get(id=dept_id)
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    user_id = get_session_user_info(request)[0]

    post_all = Port_Alarm_Status.objects.all().order_by('ip')
    post_keyword_all = Port_Alarm_Status.objects.filter(Q(ip__contains=keyword)).distinct().order_by('ip')
    if did:
        if is_common_user(request):
            return httperror(request, u'您无权查看!')

        if is_group_admin(request):
            user, dept = get_session_user_dept(request)
        else:
            dept = DEPT.objects.get(id=did)
        posts = dept.asset_set.all()
        return my_render('hmonit/monit_port_list.html', locals(), request)

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
        return my_render('hmonit/monit_port_list.html', locals(), request)

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
        return my_render('hmonit/monit_port_list.html', locals(), request)

    else:
        if is_super_user(request):
            if keyword:
                posts = post_keyword_all
            else:
                posts = post_all
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_port_list.html', locals(), request)

        elif is_group_admin(request):
            if keyword:
                posts = post_keyword_all.filter(dept=dept)
            else:
                posts = post_all.filter(dept=dept)

            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_port_list.html', locals(), request)

        elif is_common_user(request):
            user_id, username = get_session_user_info(request)[0:2]
            posts = user_perm_asset_api(username)
            contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
            return my_render('hmonit/monit_port_list.html', locals(), request)


@require_admin
def monit_port_ipdel(request, offset):
    """ 删除监控 """
    if offset == 'multi':
        len_list = request.POST.get("len_list")
        for i in range(int(len_list)):
            key = "id_list[" + str(i) + "]"
            host_id = request.POST.get(key)
            db_iplist_delete(request, host_id)
    else:
        db_port_ipdel(request, offset)

    return HttpResponseRedirect('/hmonit/monit_port_iplist/')

@require_admin
def db_port_ipdel(request, host_id):
    """ 删除监控操作 """
    if is_group_admin(request) and not validate(request, asset=[host_id]):
        return httperror(request, '删除失败, 您无权删除!')

    asset = Port_Ip_Alarm_Status.objects.filter(id=host_id)
    if asset:
        asset.delete()
    else:
        return httperror(request, '删除失败, 没有此监控!')


@require_admin
def monit_port_del(request, offset):
    """ 删除监控 """
    if offset == 'multi':
        len_list = request.POST.get("len_list")
        for i in range(int(len_list)):
            key = "id_list[" + str(i) + "]"
            host_id = request.POST.get(key)
            db_iplist_delete(request, host_id)
    else:
        db_port_del(request, offset)

    return HttpResponseRedirect('/hmonit/monit_port_list/')

@require_admin
def db_port_del(request, host_id):
    """ 删除监控操作 """
    if is_group_admin(request) and not validate(request, asset=[host_id]):
        return httperror(request, '删除失败, 您无权删除!')

    asset = Port_Alarm_Status.objects.filter(id=host_id)
    if asset:
        asset.delete()
    else:
        return httperror(request, '删除失败, 没有此监控!')
