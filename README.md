# mimotion
![ 刷步数](https://github.com/huangshihai/mimotion/actions/workflows/run.yml/badge.svg)
[![GitHub forks](https://img.shields.io/github/forks/huangshihai/mimotion?style=flat-square)](https://github.com/huangsh/mimotion/network)
[![GitHub stars](https://img.shields.io/github/stars/huangshihai/mimotion?style=flat-square)](https://github.com/huangshihai/mimotion/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/huangshihai/mimotion?style=flat-square)](https://github.com/huangshihai/mimotion/issues)

# 小米运动自动刷步数

> 小米运动自动刷步数

## Github Actions 部署指南

### 一、Fork 此仓库

### 二、设置账号密码
> 添加名为  **USER**、**PWD**、**OPEN_GET_WEATHER**、**AREA**的变量: Settings-->Secrets-->New secret  

| Secrets |  格式  |
| -------- | ----- |
| USER |   小米运动登录账号,仅支持小米运动账号对应的手机号,不支持小米账号|
| PWD |   小米运动登录密码,仅支持小米运动账号对应的密码|
| OPEN_GET_WEATHER |   开启根据地区天气情况降低步数**False**关闭,**True**开启|
| AREA |   设置获取天气的地区（上面开启后必填）如：**北京**，当**OPEN_GET_WEATHER**为**False**时填写**NO**|
| PAT |   此处**PAT**需要申请，值为github token，教程详见：https://www.jianshu.com/p/bb82b3ad1d11 ,需要repo和workflow权限,此项必填，避免git push的权限错误。 |

### 三、自定义启动时间多账户(用不上请忽略)

多账户请用 **#** 分割 然后保存到变量 **USER** 和 **PWD**

#### 例如

**13800138000#13800138001** 变量 **USER**

**abc123qwe#abcqwe2** 变量 **PWD**

### 四、自定义启动时间

编辑 **.github/workflows/run.yml**
修改其中**cron**语句的判断时间为UTC时间，即**北京时间-8**，如北京时间8点为UTC时间0点，需要运行的时间-8就是UTC时间

### 五、感谢列表
本项目基于https://github.com/xunichanghuan/mimotion 项目修改，特此感谢

## 注意事项

1. 每天运行六次，整由run.yml中的cron控制，分钟为随机值

2. 多账户的数量和密码请一定要对上 不然无法使用!!!

3. 启动时间得是UTC时间!

4. 如果支付宝没有更新步数,到小米运动->设置->账号->注销账号->清空数据,然后重新登录,重新绑定第三方

5. 小米运动不会更新步数，只有关联的会同步！！！！！

6. 请各位在使用时Fork[主分支](https://github.com/huangshihai/mimotion/)，防止出现不必要的bug.

7. 请注意，账号不是 [小米账号]，而是 [小米运动] 的账号。
