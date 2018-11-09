# 系统资源数据采集器

## 功能说明
该程序运行在CentOS系统下，用于采集系统资源使用情况，目前支持监控如下资源：

* CPU负载
* 内存使用情况
* 磁盘使用情况
* 系统活跃线程数量

依赖如下条件：

* python2.7.x
* 配置MySQL服务器添加数据表，数据表属性见后文
* python控制MySQL的MySQLdb工具

* * *
该程序并非实时监控，采用采样记录，执行一次脚本可以采样一次数据，一般在cron里添加自动化任务即可：
打开cron编辑
```
crontab -e
```
设置任务：
```
01 * * * * nohup python /root/workroot/server/watcher/src/sys_source.py > log 2>&1 &
```
cron使用可以参考百度或者谷歌资料，上边代码配置量每小时的01分启动该任务脚本，将当前的环境数据写入到MySQL数据表中。

任务执行情况会写到log目录下的日志文件中，请在conf目录下配置好mysql的参数以及log参数等。

* * *
MySQL数据表属性：
![087621759e94ffb422590f214872af68.png](evernotecid://2802695D-8393-4550-B6FB-97FCF5E4E13D/appyinxiangcom/17861192/ENResource/p91)
按照该属性创建表，并配置好用户权限即可

* * *
效果：
![0ed82120a96cf4f703556b3750ca2882.png](evernotecid://2802695D-8393-4550-B6FB-97FCF5E4E13D/appyinxiangcom/17861192/ENResource/p92)

