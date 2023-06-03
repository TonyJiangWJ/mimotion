# mimotion

![ 刷步数](https://github.com/tonyjiangwj/mimotion/actions/workflows/run.yml/badge.svg)
[![GitHub forks](https://img.shields.io/github/forks/tonyjiangwj/mimotion?style=flat-square)](https://github.com/tonyjiangwj/mimotion/network)
[![GitHub stars](https://img.shields.io/github/stars/tonyjiangwj/mimotion?style=flat-square)](https://github.com/tonyjiangwj/mimotion/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/tonyjiangwj/mimotion?style=flat-square)](https://github.com/tonyjiangwj/mimotion/issues)

## 小米运动自动刷步数（支持邮箱登录）

- 小米运动自动刷步数，小米运动APP现已改名 `Zepp Life`，为方便说明，后面还是称其为小米运动。但下载注册时请搜索 `Zepp Life`。
- 注册账号后建议先去以下网站测试自己的账号刷步数是否正常：[出去走走：https://motion.faithxy.com/](https://motion.faithxy.com/)
- 如无法刷步数同步到支付宝等，建议重新注册一个新的。

## Github Actions 部署指南

### 一、Fork 此仓库，然后创建token

#### 创建小权限的限时token，推荐

- 前往[https://github.com/settings/tokens?type=beta](https://github.com/settings/tokens?type=beta)创建个人token，建议使用Fine-grained tokens，避免token泄露导致不必要的麻烦。
- 填写token的名称，用于自己区别干嘛用的。
- 选择token有效期，最大时长为1年。一年后需要重新续期或重建，唯一缺点
- `Repository access` 选择 `Only select repositories` 勾选自己fork后的仓库，下拉可搜索：输入 mimotion 进行检索
- 点击 `Repository permissions` 展开菜单，并勾选以下四个权限即可，其他的可以不勾选
  - `Actions` Access: `Read and write` 用于获取Actions的权限
  - `Contents` Access: `Read and write` 用于更新定时任务和日志文件的权限
  - `Metadata` Access: `Read-only` 这个自带的必选
  - `Workflows` Access: `Read and write` 获取用于更新 `.github/workflow` 下文件的权限
- 完毕后点击最底下的 `Generate token` 即可生成token，复制token并保存到自己电脑以备后续使用，关闭当前页面后将无法再看到它

#### 你也可以创建更大权限的不限时token

- 建议使用上面的小权限token，这个token无法指定某一个仓库的权限，也就是token一旦泄露将有可能导致其他人直接自由访问和修改你的所有仓库代码
- 前往[https://github.com/settings/tokens/new](https://github.com/settings/tokens/new)创建
- 填写token名称，选择有效期
- `Select scopes` 勾选 `repo` 和 `workflow` 即可
- 完毕后点击最底下的 `Generate token` 即可生成token，复制token并保存到自己电脑以备后续使用，关闭当前页面后将无法再看到它

### 二、设置账号密码

#### 前往仓库设置创建变量

- Settings-->Secrets and variables-->Actions-->New repository secret
- 快捷跳转地址 [https://github.com/${你的github用户名}/mimotion/settings/secrets/actions](../../settings/secrets/actions)
- 点击右侧的 `New repository secret` 即可添加Secret

#### 添加名为 **PAT** 的变量，值为第一步申请的token

#### 添加名为 **CONFIG** 的变量

- CONFIG的内容：

  ```json
  {
    "USER": "abcxxx@xx.com",
    "PWD": "password"
  }
  ```

| 字段名  | 格式                                  |
|------|-------------------------------------|
| USER | 小米运动登录账号，仅支持小米运动账号对应的手机号或邮箱，不支持小米账号 |
| PWD  | 小米运动登录密码，仅支持小米运动账号对应的密码             |

### 三、多账户设置(用不上请忽略)

- 多账户请用 **#** 分割 然后保存到变量 **USER** 和 **PWD**

#### 例如

```json
{
  "USER": "13800138000#13800138001",
  "PWD": "abc123qwe#abcqwe2"
}
```

### 四、自定义启动时间

#### 两种方式自定义启动时间

- 1、编辑 **.github/workflows/run.yml** 中的cron表达式
  - cron表达式格式如下: `分 小时 日期 月份 年份`
  - github actions中执行时间为UTC时间，即**北京时间-8**，如果需要每天`8，10，12，14，16，22`点执行，则设置cron为`0 0,2,4,6,8,14 * * *`

  ```yaml
  on:
    schedule:
      - cron: '0 0,2,4,6,8,14 * * *'
  ```

- 2、添加名为 `CRON_HOURS` 的Variables变量 `Settings-->Secrets and variables-->Actions-->New repository variables` 注意不是Secret
- 快捷跳转地址 [https://github.com/${你的github用户名}/mimotion/settings/variables/actions](../../settings/variables/actions)
  - 填写自动执行的时间，单位为小时，此处需要设置UTC时间，例如设置 `0,2,4,6,8,14` 则会在北京时间 `8,10,12,14,16,22` 点触发执行
- 添加完成后可以在Actions中手动触发：`Random cron` 来触发替换。
- github actions 0点为执行高峰，排队可能会延后一两小时才执行，建议直接从2开始

### 五、手动触发测试工作流

- 前往Actions,左侧选择 `刷步数`，快捷链接：[https://github.com/${你的github用户名}/mimotion/actions/workflows/run.yml](../../actions/workflows/run.yml)
- 新fork的仓库默认未启用工作流，进入Actions后点击 `I understand my workflows, go ahead and enable them` 启用，然后左侧选择 `刷步数` 之后，再点击 `enable workflow` 启用工作流。请确保开启工作流，否则不会定时执行。
- 点击右侧的`Run workflow`触发执行，触发后刷新即可查看执行记录。验证是否正确配置并执行刷步数。

### 六、感谢列表

本项目基于 `https://github.com/xunichanghuan/mimotion(已被ban)` 和 [https://github.com/huangshihai/mimotion](https://github.com/huangshihai/mimotion) 项目修改，特此感谢

## 注意事项

1. 默认每天运行6+次，由run.yml中的cron控制，分钟为随机值，执行后自动更新分钟值，随机后可能当前整点二次执行，例如：8:05分执行后，分钟值随机为50，则会在8:50再次执行。

2. 多账户的数量和密码请一定要对上 不然无法使用!!!

3. 启动时间得是UTC时间!

4. 如果支付宝没有更新步数,到小米运动->设置->账号->注销账号->清空数据,然后重新登录,重新绑定第三方

5. 小米运动不会更新步数，只有关联的会同步！！！！！

6. 请各位在使用时Fork[当前分支](https://github.com/tonyjiangwj/mimotion/)，防止出现不必要的bug.

7. 请注意，账号不是 [小米账号]，而是 [小米运动/ZeppLife] 的账号。

8. 最大步数和最小步数随着时间增长，最后一次运行时到达最大步数，即默认最后一次运行在22点时，最大步数：Math.ceil(22/3)*3500=28000，最小为 Math.ceil(22/3-1)*3500=24500。

9. cron的执行根据github actions的资源进行排队，并不是百分百按指定的时间进行运行，请知悉。
