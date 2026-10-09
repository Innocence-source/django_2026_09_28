"""
HttResponse(content=b"",  content_type=None,  status=None, charset=None, headers=None) :  

    content: 响应的内容  

    status:  响应的状态码, 默认成功 值 200

    headers: 响应的头信息

    content_type: 响应的 数据类型、默认值 text/html (超文本)
         text/html 
         application/json 
         text/plain （纯文本）

    charset:  响应的编码 


render(request, template_name,  context=None) :  可以 跳转到 指定的模板页面、并返回一个 HttpResponse 对象， 该对象会显示 该模板页面的内容

    context : 想 指定的模板页面 传递 数据 、 格式一个 字典

    render 跳转 是 一次请求 、 从 发起请求 到 获取 结果、 地址栏地址不会发生改变


redirect(to, *args, permanent=False, **kwargs) :  重定向 到 一个 指定的路由 中 

    redirect 重定向 是 二次请求 、 从发起请求到 获取结果、 地址栏地址 发生改变 

    to : 用来 设置 要重定向的 路由地址 、也支持 设置 路由名称 

        路由地址 必须 以  `/` 开头 

    kwargs : 如果 是 参数路由、 可以使用 kwargs 传递参数

重定向 支持 跳转到 外部请求、 例如 百度


重定向的原理 :  

    当 用户发送 一次请求的时候、 如果 服务器 响应一个 302 / 301 的状态码的时候 

    那么 浏览器 获取 获取 响应的 头信息 Location 、并 获取 Location 的值 作为 新请求 继续 发起 第二次请求

    最终 浏览器 呈现 的是 第二次请求响应的结果

    301 : 永久性重定向 
    302 : 临时性重定向


"""
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from .db import DBUtils
from openai import OpenAI
from .captchacode import CaptchaCode


def index(request: WSGIRequest):
    """
    request 代表 请求对象、 一个请求 对象主要包含 

        请求地址 
            网址:  协议 、 域名、 端口、 路由地址、 查询参数、锚点 

        请求方式
            GET, POST, PUT,  PATCH, DELETE , .... (django 只支持 GET, POST,  axios 异步请求全部支持) 

        请求参数
            查询参数 : 以 GET 请求 传递的参数
            表单参数 : 以 POST 请求传递的参数 
            JSON参数 (django 暂不支持)
        请求头信息

    """
    # 获取 请求对应的协议信息 
    print(request.scheme)
    # 获取 主机和端口 
    print(request.get_host())
    print(request.get_port())

    # 获取 路由地址 
    print(request.path) 
    # 获取 查询参数， 返回一个 QueryDict 对象 
    print(request.GET) 
    # 获取 指定查询参数的值 、 get 获取 单值 、如果传入多值、只获取最后一个值 
    print(request.GET.get("a"))
    # 获取 指定查询参数的值、 getlist 获取 多值 、返回一个列表、存储多值
    print(request.GET.getlist("a"))
    # 获取所有的查询参数、并转成字典对象、 多值 只保留最后一个
    print(request.GET.dict())

    # 如果要获取 表单参数、 使用 request.POST 获取，返回一个 QueryDict 对象、 用法和 GET 完全相同 
    print(request.POST)

    # 获取 请求方式 
    print(request.method) 

    # 获取请求头信息 组成的 字典对象 （头信息中的键 区分大小写）
    print(request.headers.get("user-agent")) 
    # 获取 请求元数据、包含所有的请求头信息、(头信息键全大写、且均已 HTTP_ 开头、 单词中的 中划线全部更改为 下划线)
    print(request.META)

    return render(request, "index.html")


def login(request):
    """
    request 是 路由访问视图函数 自动注入的一个参数 、它是 WSGIRequest 对象 
    """
    # print(request, "=====================================")
    # return HttpResponse(content="<h1>我是一个登录页面</h1>")
    # 登录 成功、跳转到详情页
    # return redirect(to="detail", id=1000)
    # return redirect(to="https://www.baidu.com")
    return render(request, "login.html")


class Dog:
    def __init__(self, name):
        self.name = name 

class MyDjangoJSONEncoder(DjangoJSONEncoder):

    def default(self, o):

        if isinstance(o, Dog):
            return o.name 

        return super().default(o)



def detail(request, id):
    """
    参数 路由 会 给 视图函数 传入 额外的参数、 参数的关键字 是 参数路由中对应的占位符名字
    """
    # return HttpResponse(content=f"<h1>我是一个详情页, ID是 {id}, 类型是 {type(id).__name__}</h1>")
    from datetime import date 
    # 定义一个 字典 
    users = [
        {
            "name": "张三", 
            "birth": date(2000, 10, 20),
            "gender": "男",
            "anl": Dog("小黑")
        }
    ]

    # import json 
    # content = json.dumps(user, ensure_ascii=False)
    # return HttpResponse(content=content, content_type="application/json")
    return JsonResponse(data=users, encoder=MyDjangoJSONEncoder,  safe=False, json_dumps_params={"ensure_ascii": False})



# ==================== 故事类型管理 ====================

def story_type_list(request):
    """
    故事类型列表页面
    """
    return render(request, "story_type_list.html")


def story_type_query(request):
    """
    查询所有故事类型
    """
    sql = "select * from tb_story_type where is_delete = 0 order by id desc"
    data = DBUtils.select_all(sql)
    return JsonResponse(data=data, safe=False)


def story_type_add(request):
    """
    添加故事类型
    """
    # 获取类型名
    type_name = request.POST.get("name")

    # 检查类型名是否已存在
    sql = "select 1 from tb_story_type where name = %s"
    if DBUtils.select_one(sql, args=(type_name,)) is not None:
        return JsonResponse(data={"message": "该类型名已存在"}, status=400)

    # 插入数据
    sql = "insert into tb_story_type(name, enabled, create_time) values(%s, 1, now())"
    pk = DBUtils.insert(sql, args=(type_name,))

    return JsonResponse(data={"id": pk, "name": type_name, "state": 1})


def story_type_update(request, typeId):
    """
    修改故事类型
    """
    # 接收参数
    type_name = request.POST.get("name")
    state = request.POST.get("state")

    # 检查类型名是否已存在（排除当前记录）
    sql = "select 1 from tb_story_type where name = %s and id != %s"
    if DBUtils.select_one(sql, args=(type_name, typeId)) is not None:
        return JsonResponse(data={"message": "该类型名已存在"}, status=400)

    # 更新数据
    sql = "update tb_story_type set name = %s, enabled = %s where id = %s"
    DBUtils.update(sql, args=(type_name, state, typeId))

    return JsonResponse(data={"message": "操作成功"})


def story_type_delete(request, typeId):
    """
    删除故事类型
    """
    sql = "update tb_story_type set is_delete = 1, delete_time = now() where id = %s"
    DBUtils.delete(sql, args=(typeId,))

    return JsonResponse(data={"message": "操作成功"})


def story_type_state(request, typeId):
    """
    切换故事类型启用状态
    """
    # 先查询当前状态
    sql = "select enabled from tb_story_type where id = %s"
    item = DBUtils.select_one(sql, args=(typeId,))

    if item is None:
        return JsonResponse(data={"message": "记录不存在"}, status=400)

    # 切换状态
    new_state = 0 if item["state"] == 1 else 1
    sql = "update tb_story_type set enabled = %s where id = %s"
    DBUtils.update(sql, args=(new_state, typeId))

    return JsonResponse(data={"message": "操作成功", "state": new_state})


def story_list(request):

    return render(request, "story_list.html")


def story_add(request):

    return render(request, "story_add.html")


def story_type_list(request):

    sql = "select id, name from tb_story_type where is_delete = 0 and enabled = 1" 
    data = DBUtils.select_all(sql)
    return JsonResponse(data=data, safe=False)


def story_generator(request):
    # title,type, font_count,keywords, bg_settings,  role_desc, story_detail
    # 获取 故事标题 
    title = request.POST.get("title")
    # 获取 故事分类 
    type_id = request.POST.get("type")
    # 获取 字数限制 
    font_count = request.POST.get("font_count")
    # 获取关键字
    keywords = request.POST.get("keywords")
    # 获取 故事背景设定 
    bg_settings = request.POST.get("bg_settings")
    # 获取 角色描述 
    role_desc = request.POST.get("role_desc")
    # 获取 故事梗概 / 情节要求
    story_detail = request.POST.get("story_detail")

    # 根据 故事类型 ID 查询 故事类型的名字 
    sql = "select name from tb_story_type where id = %s" 
    story_type = DBUtils.select_one(sql, args=(type_id, ))

    # 编写 生成故事的 AI提示词
    prompt_template = f"""
        你是一个拥有十年写作经验的故事作家、非常擅长编写不同风格的故事。

        故事标题: {title}
        故事分类: {story_type.get('name')}
        字数限制: {font_count}
        关键字: {keywords}
        故事背景设定:  {bg_settings}
        主要角色描述: {role_desc}
        故事梗概 / 情节要求: {story_detail}

        要求语言风趣幽默、只输出故事内容(纯文本)即可，不要输出故事标题及和故事内容不相关的信息, 。
    """
    # 构建一个 基于 OpenAI 的大模型对象 
    client = OpenAI(
        api_key="sk-cddgdmfn8xc5pgm2afo5cmfab1rmj50sunw7exxah51niwqs",
        base_url="https://api.xiaomimimo.com/v1",
    )

    # 以流的方式 返回数据 、返回的是一个 迭代器 
    stream = client.responses.create(
        model="mimo-v2.6-pro",
        input=prompt_template,
        temperature=0.7,
        stream=True
    )

    def generator():
        for event in stream: 
            if event.type == "response.output_text.delta":
                yield f"data: {event.delta}\n\n"

    # 以流的形式 返回结果 、必须设置 响应的数据格式为 text/event-stream 格式 （该格式会以 流的方式 实时响应）
    return StreamingHttpResponse(streaming_content=generator(), content_type="text/event-stream")


def sse(request):

    # 定义一个 生成器函数 负责生成 1 ~ 100 的所有数据 
    def generator_num():
        import time, random , json
        for x in range(1, 10): 

            yield f"data: {x}\n\n"
            time.sleep(random.uniform(0.2, 0.6))
    # 使用 SSE 协议 返回数据
    return StreamingHttpResponse(generator_num(), content_type="text/event-stream")


def captcha_code(request):
    # 接收 传入的 验证码的 宽 和 高 
    width = int(request.GET.get("w", "120"))
    height = int(request.GET.get("h", "40"))
    space = int(request.GET.get("s", "10"))
    # 生成验证码 
    bytesio, chars = CaptchaCode(width, height, space).get_captcha_code()

    # chars 后期 要存储到 服务器中 、例如 使用 redis 、session 或者 和一个 唯一键进行绑定 
    #  streaming_content 它的值 可以是一个迭代器、 也可以使用 包含 read() 方法的对象
    return StreamingHttpResponse(streaming_content=bytesio, content_type="image/png")

