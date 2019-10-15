# -*- coding: UTF-8 -*-
from gevent import monkey
monkey.patch_all()

import multiprocessing
# 开启子进程是不支持打包exe文件的，所以会不停向操作系统申请创建子进程，导致内存炸了，multiprocessing.freeze_support()就是解决这个问题的
multiprocessing.freeze_support()

import config
import spider
import availability
import persistence
import web





if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>启动代理IP爬虫程序>>>>>>>>>>>>>>>>>>")
    print('********************************************************')
    print('本程序运行条件：')
    print('1、请先确保本程序处于外网环境')
    print('2、须安装redis数据库')
    print('********************************************************')

    if config.is_internet():
        # 进程间队列
        # 爬取的代理
        queue_verification = multiprocessing.Queue(config.COROUTINE_NUM)
        # 待持久化的代理
        queue_persistence = multiprocessing.Queue()

        # 多进程列表
        workers = list()
        # 爬虫
        workers.append(multiprocessing.Process(target=spider.worker, args=(queue_verification,)))
        # 爬取下来的代理验证
        workers.append(multiprocessing.Process(target=availability.crawl_worker, args=(queue_verification, queue_persistence)))
        # 已持久化的代理验证
        workers.append(multiprocessing.Process(target=availability.store_worker))
        # 持久化
        workers.append(multiprocessing.Process(target=persistence.worker, args=(queue_persistence,)))
        # web api 服务
        workers.append(multiprocessing.Process(target=web.worker))

        for worker in workers:
                worker.start()

        for worker in workers:
            worker.join()
    else:
        print('====================本程序只能在外网环境下运行====================')
