# 配置邮件通知

## 功能说明
该程序用于从服务器上发送邮件到个人邮箱中，用于某些模块服务数据监控管理，当前使用该模块传输服务器监视资源使用情况，需要的依赖如下：

* python2.7.x

* * *
由于我需要使用[server_watcher](https://github.com/hexueyuan/pythontatter/tree/master/server_watcher)模块采集的数据，因此需要查询MySQL数据库；在conf下的html_page中定义了html模版，该模版可以根据自己的需求修改，然后在src/server_source_watcher.py中build_html方法中定义了填充该模版的方法，也是按需求自定义，最后配置好之后添加到cron中每天定时运行即可。

* * *
我当前使用该模块每天凌晨计算前一天的服务器资源使用情况并通过邮件发送到我的邮箱中，效果如下：
![效果展示](https://github.com/hexueyuan/pythontatter/blob/master/mailToMe/.image/420AB037-22EB-4E0F-9591-2784B2957DA5.png)
