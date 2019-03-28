# 软件工程大作业 - 后端部分

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)  

[![License: LGPL v3+](https://img.shields.io/badge/License-LGPL%20v3+-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)


## 想法

使用flask开发后端

使用正则表达式替代原有的cssselect , 合理使用正则表达式应该也能解决获取登录ip的功能

(如果有其他想法可以在这里写下, push上来就行)

## TO-DO

1. 解决爬虫脚本`get_pay_info`中的相关问题

   1. 竹园, 海棠,丁香 的校园网用户在这个网页上的表格名不同, 翼讯和校园网的也不同, 现在是只能处理海棠的流量问题

   2. 解决自动识别验证码的问题, 目前的OCR方案识别率太低, 严重影响效率[已初步解决]

   3. 加入获取目前登录ip的功能
2. 对脚本进行整理, 统一返回格式, 取消原来的交互逻辑, 为接下来的开发做准备
3. 设计数据库, 存储用户相关信息(app是不是要加一个免责声明之类的, 使用本app即视为授权我们使用他的校园网等的用户名密码)
4. 一个类似队列的中间件, 这个我还没了解. 因为需要做消息提醒, 所以要对所有设置了消息提醒的用户, 按其设置的时间间隔去爬取数据, 然后返回给app或者调用邮件/短信插件去推送信息
5. 后端的架构设计

(同上)

