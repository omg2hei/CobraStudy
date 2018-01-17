# -*- coding: utf-8 -*-

'''
写该文件中代码的4个目的：
    1、学习@staticmethod静态方法装饰器
    2、学习ConfigParser模块
        ConfigParser模块使用步骤：
        一、实例化ConfigParser对象 config = ConfigParser()
        二、读取配置文件 config.read(config_path) 传入参数类型：str 字符串类型
        三、读取配置文件中的配置信息 value = config.get(level1, level2) 两个传入类型的参数均为：str 字符串类型
    3、复习Python类基础
    4、分析Cobra源码，剥离出来更好理解

文件相对路径/study/ConfigParser_study.py
'''

import os #os模块中有执行命令、文件目录操作等相关方法
import traceback # 用于后面调用traceback.print_exc()输出详细的异常信息（栈回溯信息）

# 通过该方法可以兼容Python2、Python3
try:
    from configparser import ConfigParser  # Python3
except ImportError:
    from ConfigParser import ConfigParser  # Python2

project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) # 定义项目目录
config_path = os.path.join(project_directory, 'config') # 定义配置文件

class Config(object):
    def __init__(self, level1=None, level2=None):  # __init__构造方法，即创建对象时则会执行该方法
        self.level1 = level1  # 初始化 类属性，self就是当前对象，self.level1就是对象内的level1属性
        self.level2 = level2
        if level1 is None and level2 is None:
            return
        config = ConfigParser()  # 实例化ConfigParser对象

        config.read(config_path)  # 读取配置文件
        value = None
        try:
            value = config.get(level1, level2)
        except Exception as e:
            traceback.print_exc() # 想必print(e)可以输出详细的异常信息（栈回溯信息）
            # Cobra中采用logger.critical()方法进行错误信息的输出，这里为了方便，直接采用print()
            print("./configs file configure failed.")
        # 这里是__init__构造方法的精华所在，value值就是配置文件中，:右边的内容，类型为 字符串（str）
        self.value = value

        # 根据方法名字，2个参数的名字，方法实现可知：这个方法的功能是用来进行复制文件，从一个位置复制到另一个位置
        # 使用场景：配置文件未定义时会调用该方法，将config.template中的内容复制到config中
        # ps：全局搜索了下copy，并没有看到调用该方法的位置
    @staticmethod
    def copy(source, destination):
        if os.path.isfile(destination) is not True: #如果目标位置不是文件（即文件未创建），则执行该逻辑
            print("配置文件未设置，正在设置")
            with open(source) as f:
                content = f.readlines()
            with open(destination, 'w+') as f:
                f.writelines(content)
            print("配置文件设置成功.")
        else:
            return

    # 静态方法和类方法均可以在类不进行实例化的时候进行调用
    # 就这一点上与类方法@classmethod没啥区别
    # 其他不同用到的时候再补充
    @staticmethod
    def test(canshu):
        print('静态方法测试.{canshu}'.format(canshu=canshu))

# 这个类的功能是判断
class Vulnerabilities(object):
    def __init__(self, key):
        self.key = key

    '''
    修复状态描述，共有三种
    1、未修复
    2、未修复（Push third-party）
    3、已修复
    
    另外两个方法思路完全相同，在此不在赘述
    '''
    def status_description(self):
        status = {
            0: 'Not fixed',
            1: 'Not fixed(Push third-party)',
            2: 'Fixed'
        }
        if self.key in status:
            return status[self.key]
        else:
            return False


if __name__ == '__main__':
    config = Config(level1="cobra", level2="secret_key")
    key = config.value
    print(key)
    config.test(canshu=124)
    Config.test(canshu=125)
    print(Config.test)