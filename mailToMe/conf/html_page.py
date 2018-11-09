# -*- coding:utf-8 -*-
page = '''
<html>
    <head>
    </head>
    <body>
        <p>资源配置</p>
        <table class="tftable" border="1">
            <tr><th>资源</th><th>预配置</th></tr>
            <tr><td>CPU</td><td>{}</td></tr>
            <tr><td>内存</td><td>{}</td></tr>
            <tr><td>磁盘</td><td>{}</td></tr>
        </table>
        <br>
        <br>
        <p>服务器状态</p>
        <table class="tftable" border="1" border-collapse="collapse">
            <tr><td></td><td>平均</td><td>最大负载</td><td>最大负载时间</td><td>最小负载</td><td>最小负载时间</td></tr>
            <tr><td>CPU负载</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>
            <tr><td></td><td>平均</td><td>最大线程量</td><td>最大线程量时间</td><td>最小线程量</td><td>最小线程量时间</td></tr>
            <tr><td>活跃线程量</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>
            <tr><td></td><td>平均</td><td>最大使用量</td><td>最大使用量时间</td><td>最小使用量</td><td>最小使用量时间</td></tr>
            <tr><td>内存使用</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>
            <tr><td></td><td>平均</td><td>最大使用量</td><td>最大使用量时间</td><td>最小使用量</td><td>最小使用量时间</td></tr>
            <tr><td>磁盘使用</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>
        </table>
    </body>
    <style type="text/css">
        .tftable {{font-size:12px;color:#333333;width:100%;border-width: 1px;border-color: #729ea5;border-collapse: collapse;}}
        .tftable th {{font-size:12px;background-color:#acc8cc;border-width: 1px;padding: 8px;border-style: solid;border-color: #729ea5;text-align:left;}}
        .tftable tr {{background-color:#ffffff;}}
        .tftable td {{font-size:12px;border-width: 1px;padding: 8px;border-style: solid;border-color: #729ea5;}}
        .tftable tr:hover {{background-color:#ffff99;}}
    </style>
</html>
'''
