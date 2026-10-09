"""

path 函数 :  定义 路由 

path(route,  view,  kwargs=None, name=None)

    route :  用来 设置 路由地址、 值是一个 字符串 、不能以 /  开头、访问的时候 需要添加 /  

    view  :  用来 设置 视图函数 ( 处理业务、 并返回一个 页面给用户 ) 

    kwargs :  给 视图函数 传递 额外的 数据 、值是一个字典、例如 {'name': '张三'}

    name :  给路由设置一个名字  

参数路由: 
    在 route 中 定义路由的时候， 支持使用  `<>` 进行占位、例如 <id>  

    在 进行占位的时候， 也支持 设置 并限定的 参数的类型 例如 <int:id>

    常见的参数类型 有 5种 
        int : 限定 参数类型是个整数 

        str : 限定参数类型是一个 字符串、且字符串中 不包含 `/` 路径分隔符 、当 占位符 不限定类型的类型，默认值为 str

        slug : 限定参数类型 是一个 字符串 、 字符串中 字母、数字、下划线 字符组成

        uuid : 限定参数 类型 必须是 uuid 格式 (8-4-4-4-12) 的 字符串

        path : 限定参数类型 必须是 字符串、对字符串 没有限定 。


 正则路由:
    
    在 定义路由的时候，允许使用正则表达式 进行路由限定 。

    正则路由 必须使用 re_path 函数 定义 、该函数 用法参考 path

    正则路由 在定义的时候 一定要 注意 是否使用 限定符 ^,  $


"""
from django.contrib import admin
from django.urls import path, re_path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # 定义一个 正则路径、支持使用 限定符 
    re_path(r'^$', views.index, name="index"),

    # 定义一个普通路由 
    path('login',  views.login, name="login"), 

    # 定义一个参数路由 、也支持 给 参数 设置 并限定类型
    # path('detail/<int:id>', views.detail, name="detail"),

    # 正则参数 路由 可以 使用 命名捕获分组实现
    re_path(r'^detail/(?P<id>\d+)$', views.detail, name="detail"),

    # 管理 应用路由 （分布式路由）
    re_path(r'^tasks/', include('apps.todotasks.urls')) ,


    # 故事类型管理路由
    path('story-type', views.story_type_list, name='story-type'),
    path('story-type/query', views.story_type_query, name='story-type-query'),
    path('story-type/add', views.story_type_add, name='story-type-add'),
    path('story-type/update/<int:typeId>', views.story_type_update, name='story-type-update'),
    path('story-type/delete/<int:typeId>', views.story_type_delete, name='story-type-delete'),
    path('story-type/state/<int:typeId>', views.story_type_state, name='story-type-state'),

    # 故事管理路由 
    path('story-list', views.story_list, name="story-list"),

    path('story-add', views.story_add, name="story-add"),

    path('story-type/list', views.story_type_list, name="story-type-list"),

    path('story-generator', views.story_generator, name='story-generator') , 

    path('captcha', views.captcha_code, name='captcha'),

    path('sse', views.sse, name='sse') ,
]
