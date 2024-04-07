![Release](https://img.shields.io/badge/Release-1.1.9-blue)
---
## 介绍
一款基于Python-Flask框架,开发的短网址程序.
## 需求
1. 平台: Windows/Linux/Docker/Vercel/Deta.
2. 语言: Python3.8+.
3. 数据库: MySQL.
## 配置
查看config.py文件.
## 部署
### 手动
1. Windows: 运行wsgi.py文件.
2. Linux: 执行`gunicorn main:app -c gunicorn.py`命令.
3. 支持Docker.
### 自动
Vecel|Render
---|---
[![Vercel](https://vercel.com/button)](https://vercel.com/import/project?template=https://github.com/H2Oye/H2O-Short-Url)|[![Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/H2Oye/H2O-Short-Url)
1. 参考各平台文档.
2. 添加环境变量,DATABASE_HOST(数据库地址),DATABASE_PORT(数据库端口),DATABASE_USERNAME(数据库用户名),DATABASE_PASSWORD(数据库密码),DATABASE_NAME(数据库名称),DATABASE_TABLE_PREFIX(数据库表前缀,推荐使用h2o_short_url_),DATABASE_SSL_CA_PATH(启用),DATABASE_SSL_CA_PATH(CA路径),DATABASE_SSL_KEY_PATH(Key路径),DATABASE_SSL_CERT_PATH(Cert路径),三种证书路径无则空.
## 数据库
1. core表修改网站标题,关键词,描述.
2. domain表修改域名,protocol仅能填http/https.
## 问题
1. 问: Vercel无法访问.  
   答: Vercel被墙.