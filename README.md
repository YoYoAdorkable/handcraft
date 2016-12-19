# Handcraft
通过request请求url是否正常，修改header，透传后端ip访问。
通过django＋bootstrap前端展示

###Version
2016-12-19 发布handcraft version 1.0 （v1.0）

###Description
* python django
* 判断ip是否能过访问通，通过进行url检测，支持json接口、html页面检测

###Note
* 前端html页面有些乱，需要按自己需求再去修改
* 报警程序没有进行合并报警处理，需要的自己修改下，基于ops的报警需要手动修改下组id，代码中直接指定组id了，报警中直接指定了有些ip发给ops，其余按报警组发送，代码简单自己修改下。(m_alarm:135、136行)
* handcraft_web	前端页面
* handcraft	监控程序

###Install
* 创建数据库后，执行handcraft.sql

###Login
初始账户：admin		admin@123

