from django.shortcuts import render
from django_demo.db import DBUtils
from django.http import JsonResponse
from apps.todotasks.models import Task


def todolist(request):
    return render(request, "todolist.html")


def task_add(request): 
    """
    保存 任务 
    """
    # 获取 页面传入的 任务名 
    taskname = request.POST.get("name")

    # 编写一个 SQL 命令、负责 查询 今日 当前任务 是否已经存在 
    # sql = """
    #     select 1 from tb_task where name = %s and time = current_date()
    # """


    # # 执行 SQL 
    # if DBUtils.select_one(sql, args=(taskname, )) is not None:
    #     # 任务 添加失败 、返回一个 错误 结果 
    #     return JsonResponse(data={"message": "当前任务已存在"}, status=400)

    from datetime import date 

    if Task.objects.filter(name=taskname, time=date.today()).exists():
        return JsonResponse(data={"message": "当前任务已存在"}, status=400)


    from datetime import date 
    # 如果 任务名 在表中 不存在、 则 将数据插入到表中 
    # sql = """
    #     insert into tb_task(name, state, time) values
    #     ( %s,  0, %s)
    # """
    # time = date.today()
    # # 执行 SQL 
    # pk = DBUtils.insert(sql, args=(taskname, time))
    task = Task.objects.create(name=task_add)

    # 返回一个 成功的 结果 
    return JsonResponse(data={"id": task.pk, "name": taskname, "state": 0,  "time": task.time })


def task_list(request):
    """
        查询今日所有的任务
    
    视图函数的 三个重要职责 :

        1. 尝试 接收 请求传递的数据,  request.GET,  request.POST,  request.FIELS 

        2. 处理业务 (通常会通过 SQL 操作表中的数据、核心代码)

        3. 返回合适的数据 给 发起 请求者
                render() : 返回 模板 
                redirect() : 返回 路由对应的模板
                JsonResponse: 返回 JSON 数据


    """
    sql = "select * from tb_task where time = current_date()" 

    data = DBUtils.select_all(sql)
    # 如果 返回列表， 必须设置 safe = False
    return JsonResponse(data=data, safe=False)


def task_delete(request, taskId):
    """
    删除任务 
    """
    # 编写 SQL 执行 删除命令 
    sql = "delete from tb_task where id = %s" 

    # 执行 SQL 
    rows = DBUtils.delete(sql, args=(taskId, )) 

    return JsonResponse(data={"message": "操作成功"})


def task_state(request, taskId):

    # 编写 SQL 命令，将任务的状态设置为 已完成
    sql = "update tb_task set state = 1 where id = %s"

    DBUtils.update(sql, args=(taskId, ))

    return JsonResponse(data={"message": "操作成功"})


def task_modify(request, taskId):
    # 接收 请求传入的 任务名
    task_name = request.POST.get("name")

    # 检查 当前任务名 是否在 今日 已经存在
    sql = """
        select 1 from tb_task where name = %s and id != %s and time = current_date()
    """

    if DBUtils.select_one(sql, args=(task_name, taskId)) is not None:
        # 失败
        return JsonResponse(data={"message": "当前任务名已存在"}, status=400)

    # 如果 任务名可以使用、 则将当前数据 进行更改
    sql = "update tb_task set name = %s where id = %s"

    DBUtils.update(sql, args=(task_name, taskId))

    return JsonResponse(data={"message": "操作成功"})

