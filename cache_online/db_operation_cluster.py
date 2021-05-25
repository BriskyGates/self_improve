import traceback

import pymysql
from pymysql.cursors import DictCursor

# from setting import PROJECT_BASE_DIR
# from utils.db_operation import DMU_DB_CONFIG
from loguru import logger

# 数据库相关配置
# from universal_constant import *
from utils.routine.loguru_utils import LoguruUtil
from utils.routine.wrapper_utils import check_empty

DB_CONFIG = {
    'host': '49.235.158.172',
    'port': 6600,
    'user': 'mwadmin',
    'password': 'Mwclg_2018!@#',
    'db': 'postprocess',
    'charset': 'utf8',

}

LoguruUtil(LOG_DIR, 'db_operation_cluster.log').loguru_main()


class DBOperationBase():

    def __init__(self, db_config, flag=True):
        """
        db_config 为数据库连接相关配置
        1.支持链式调用
        2. 目前调用都是针对依次执行, 可能在很多方面不太适合
        """
        self.conn = None
        self.cursor = None
        self.db_config = db_config
        self.table_name = table_name
        self.flag = flag  # 用来规定是否取一条数据,True: fetchmany()
        self.options = {
            'fields': '*',  # 字段列表,默认是全部字段
            'table': "",  # 表名
            'where': '',  # where条件
            'groupby': '',  # group by分组条件
            'having': '',  # having 分组过滤条件
            'orderby': '',  # order by排序条件
            'limit': ''  # limit 限制结果集
        }

    # 连接数据库
    def connect(self, cursor_option=None):
        """
        cursor对有元组形式和字典形式DictCursor
        """
        self.conn = pymysql.connections.Connection(**self.db_config)
        self.cursor = self.conn.cursor(cursor=cursor_option)

    # 关闭数据库连接对象
    def close(self):
        self.cursor.close()
        self.conn.close()

    def table(self, tablename):
        # print(tablename)
        self.options['table'] = tablename
        # 在此处调用了缓存字段函数,出错原因:当fields字段为*时,才给它能成 cachefield(全字段)
        # 其他情况,保持原本值
        return self

    def select(self):
        sql = "SELECT {fields} FROM {table} {where} {groupby} {having} {orderby} {limit}"
        sql = sql.format(**self.options)  # 为啥会在options中又定义一个table呢?此处见端倪
        logger.info(f"options参数为:{self.options}")
        logger.info(f'SQL 语句为{sql}')
        # self.sql = sql  # 保存sql语句
        return self.query(sql)

    def handle_condition(self, condition: dict, extra_ch="="):
        """
        键是字符串,值是列表
        将条件设置成 例如'name="张三"',汇总到 condition_list中
        可能出现bug ,传入的condition 可能需要模糊匹配和正常的查询, 就需要多次链式调用 NOT ACK
        """

        condition_list = []
        for key, value in condition.items():
            temp_value = f'{key} {extra_ch} "{value}"'  #
            condition_list.append(temp_value)
        # 开始组装wheresql条件语句
        for condition in condition_list:  # 两个相同的键无法做选择
            self.where(condition)
        return self

    @check_empty(return_value='*')
    def __add_comma(self, data: list):
        return ','.join(data)

    # 还原options条件
    def init_options(self):
        self.options = {
            'fields': "",  # 全部字段列表
            'table': self.table_name,  # 表名, 不同子表的切换可能会有问题
            'where': '',  # where条件
            'groupby': '',  # group by分组条件
            'having': '',  # having 分组过滤条件
            'orderby': '',  # order by排序条件
            'limit': ''  # limit 限制结果集
        }

    def field(self, fields_inner):
        """
        传入的field 为列表, 类似于['palindrome','retention']
        """
        new_fields = self.__add_comma(fields_inner)
        self.options['fields'] = new_fields
        logger.info(f'类属性options中的field字段值:{self.options["fields"]}')
        return self

    @staticmethod
    def handle_in_list(data: list):
        """
        传入data, 处理成每个都是字符串形式
        输入['123','345']
        输出 "'123',''345'"
        Args:
            data:

        Returns:

        """
        temp = map(lambda x: f'"{x}"', data)
        new_data = ','.join(temp)
        return new_data

    def where_in(self, condition):  # 目前只支持一个键
        """
        实现 WHERE column_name IN(value1, value2, ...);

        Args:
            condition:

        Returns:

        """
        condition_list = []
        for key, value in condition.items():
            if isinstance(value, list):
                new_value = self.handle_in_list(value)
                condition = f'{key} in ({new_value})'
            else:
                condition = f'{key}="{value}"'  #
            condition_list.append(condition)
        for con in condition_list:
            self.where(con)
        return self

    def where(self, conditions):  # 当where 调用两次是走else条件
        # 判断options中where是否为空
        if not self.options['where']:  # 为空
            self.options['where'] = " WHERE " + conditions
        else:
            self.options['where'] += ' AND ' + conditions  # 传入多个条件则变成或关系
        return self

    # 可以进行原生的sql查询
    def query(self, sql):
        try:
            self.cursor.execute(sql)
            if self.flag:
                res = self.cursor.fetchall()
            else:
                res = self.cursor.fetchone()
            logger.info(f'得到的结果为{res}')
            return res  # 返回查询结果
        except:
            logger.info(traceback.format_exc())
            return None


if __name__ == '__main__':
    table_name = 'docu_type_mapping'
    db_config = DB_CONFIG
    db_op = DBOperationBase(table_name, db_config)
    db_op.connect(DictCursor)
    db_op.select()
    # condition = {"template_id": "%1c%", 'file_type': "%T"}
    # fields = ['template_id']
    # db_op.handle_condition(condition, flag=False).field(fields).select()
    db_op.close()
"""
功能实现:
    查看影响行数
"""
