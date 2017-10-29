---
title: Flask + Gunicorn + Nginx 部署小坑记
date: 2017-10-26 22:59:37
categories:
  - Python
  - Web
---


碰到的坑主要通过[Flask + Gunicorn + Nginx 部署](http://www.cnblogs.com/Ray-liang/p/4837850.html)和[Nginx代理应用端口丢失问题](http://www.aichengxu.com/nginx/6455993.htm)解决的<br>
其他的坑主要就是将Gunicorn作为服务运行这一步，可能是因为系统的关系没有成功，只能用nohup command &暂时顶替。