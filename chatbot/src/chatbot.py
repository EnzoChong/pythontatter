# -*- coding:utf8 -*-
#!/user/bin/env python

import itchat
import webcrawl
import download
import json

atmyname = u"@那个什么什么源"

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    text = msg['Text'].encode("utf-8")
    user = msg['User']['UserName']
    if text == "表情包":
        image_url = webcrawl.get_image_url()
        image_path = download.download_image(image_url)
        itchat.send_image(image_path, toUserName=user)
    if text.startswith("表情包:") or text.startswith("表情包："):
        content = text.replace("表情包：", "").replace("表情包:", "").strip()
        image_url = webcrawl.get_image_url_with_content(content)
        image_path = download.download_image(image_url)
        itchat.send_image(image_path, toUserName=user)

@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.isAt:
        text = msg.text.replace(atmyname, u"").split(u"\u2005", 2)[-1].encode("utf-8")
        if text == "表情包":
            image_url = webcrawl.get_image_url()
            image_path = download.download_image(image_url)
            msg.user.send_image(image_path)
        if text.startswith("表情包:") or text.startswith("表情包："):
            content = text.replace("表情包：", "").replace("表情包:", "").strip()
            image_url = webcrawl.get_image_url_with_content(content)
            image_path = download.download_image(image_url)
            msg.user.send_image(image_path)

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()
