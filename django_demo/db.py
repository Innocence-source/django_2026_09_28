from django.db import connection

class DBUtils:

    @classmethod
    def get_connection(cls):
        """获取数据库连接"""
        return connection

    @classmethod
    def execute(cls, sql, args=None, *, functional):
        """执行SQL"""
        # 获取 数据库的连接 
        conn = cls.get_connection()
        # 获取 SQL 执行器 
        with conn.cursor() as cursor:
            # 执行 SQL 并获取 结果 
            rowcount = cursor.execute(sql, args)
            return functional(cursor, rowcount)

    @classmethod
    def insert(cls, sql, args=None):
        """新增数据、并返回主键"""
        return cls.execute(sql, args, functional=lambda cursor, rowcount: cursor.lastrowid)

    @classmethod
    def update(cls, sql, args=None):
        """修改数据、并返回影响的行数"""
        return cls.execute(sql, args, functional=lambda cursor, rowcount: rowcount)

    @classmethod
    def delete(cls, sql, args=None):
        """删除数据、并返回影响函数"""
        return cls.update(sql, args)

    @classmethod
    def select_one(cls, sql, args=None):
        """查询满足条件的 单条数据"""

        def fetch(cursor, rowcount):
            if rowcount > 1:
                raise ValueError(f"{cls.__name__}.select_one(sql, args=None) 期待查询 1 条数据、实际返回 {rowcount} 条")
            
            if rowcount == 0:
                return None
            # 如果查询到了数据、获取数据 
            data = cursor.fetchone()
            columns = [column[0] for column in cursor.description] 
            return dict(zip(columns, data))

        return cls.execute(sql, args, functional=fetch)

    @classmethod
    def select_all(cls, sql, args=None):
        """查询多条数据"""
        def fetch(cursor, rowcount):
            if rowcount == 0:
                return []
            # 如果查询到了数据、获取数据 
            data = cursor.fetchall()
            columns = [column[0] for column in cursor.description] 
            return [dict(zip(columns, d)) for d in data]

        return cls.execute(sql, args, functional=fetch)  

