from django.urls import path, re_path 
from . import views 

# 配置一个 命名空间， 解决 不同应用下 路由名 命名冲突问题
#  如果 应用配置了 命名空间， 那么 每一个路由的名字 是  <namespace>:<name>
app_name = "todotasks"

# 配置 应用路由
urlpatterns = [

    path('todolist', views.todolist, name="todolist"),  # 路由名为  todotasks:todolist

    path('task-add', views.task_add, name="task-add") , 

    path('task-list', views.task_list, name="task-list"),

    path('task-delete/<int:taskId>', views.task_delete, name="task-delete"),

    path('task-state/<int:taskId>', views.task_state, name='task-state'),

    re_path(r'^task-modify/(?P<taskId>\d+)$', views.task_modify, name='task-modify'),
]