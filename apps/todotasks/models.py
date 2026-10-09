from django.db import models

"""
ORM (对象关系映射), 它主要解决三个问题 

1.  类 和 表的关系 

2.  属性 和 字段的关系 

3.  对象 和 表中记录的关系


如何 根据 模型 创建 表 


"""

class Task(models.Model):
    """
    类 和 数据库 表 进行 映射、默认 映射规则是 <应用名>_<模型名> 作为 映射的表名

    Task 类 默认 和  todotasks_task 表 进行映射 、可以 通过 db_table 进行修改 

    模型 在 定义属性 和 表字段的关系、 可以 不用设置 主键、默认为 id 且 类型为 bigint, 自动增长
    
    """
    # 定义 属性 、描述 属性 和 表中 字段的关系 
    # id = models.BigAutoField(primary_key=True)

    # 定义一个 name 属性 ，默认 会和 数据库表中的 name 字段对应、可以 通过 db_column 进行修改
    # 如果 字段名 和属性名 相同， 则可以省略 db_column 
    name = models.CharField(max_length=100, null=True, db_comment="任务名", db_column="name")

    # 定义一个 state 属性 、使用 default 设置 默认值 
    state = models.BooleanField(default=False, db_comment="任务状态")

    # 定义一个 time 属性 ,  auto_now_add (添加数据的时候，默认使用 当前系统时间)
    time = models.DateField(auto_now_add=True, db_comment="任务时间")

    class Meta:
        # 将 当前类 Task 和 数据库中的 tb_task 进行绑定
        db_table = "tb_task"
        # 是否 将当前模型 交给 Django 管理、默认为 True,  如果设置为 False, 则 该模型 不会生成对应的表
        managed = True

