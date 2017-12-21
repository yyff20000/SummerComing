# -*- coding:utf-8 -*-
import redis,time,redis_handle
#
weixinId = 'oDFHUv8_F7PVZc0oMrVjlBrlMKto'
conn = redis_handle.connect()

def addArticles():

	# r = redis.Redis(host='192.168.140.130',port=6379,password='nino38')

	  # 连接新浪云服务器
	redis_handle.adminPost(conn, weixinId, "新的故障场景", "请输入[报障 1 故障信息(包括ip、资源名称、故障详细情况描述等)]",1)

	redis_handle.adminPost(conn, weixinId, "网准登陆时，正在从自助服务器上加载数据", "程序服务启动失败，重启本地终端。")

	redis_handle.adminPost(conn, weixinId, "网准登陆时，自助服务暂时无法使用", "程序服务启动失败，重启本地终端。")

	redis_handle.adminPost(conn, weixinId, "点击获取动态口令后提示已获取，但无法收到短信", "1、请检查手机接收是否设置黑名单"
		"。2、请用账号关联号码联系福莱特运维人员核查手机号是否绑错。请<a href='http://111.23.233.129/contact'>查看管理人员列表</a>。")

	redis_handle.adminPost(conn, weixinId, "点击获取动态口令后提示连接动态口令服务失败，请稍后重试", "1、请检查当前网络到"
		"福莱特动态口令服务器地址是否丢包，如丢包，用手机热点等方式再尝试一次。请<a href='http://111.23.233.129/'>下载最新服务器地址</a>。")

	redis_handle.adminPost(conn, weixinId, "点击获取动态口令后提示用户标识无效，申请动态口令失败", "1、请检查是否为网管准入客户端。"
		"2、请检查是否输入了正确的手机号。3、请调出以前申请VPN时的工单截图及电子档后（注意有效期，超时请重新申请VPN权限），联系福莱特运维人员核查。"
		"请<a href='http://111.23.233.129/contact'>查看管理人员列表</a>。")

	redis_handle.adminPost(conn, weixinId, "点击获取动态口令后提示禁止外网登录", "1、请检查是否为网管准入客户端。2、请检查是否输入了正确的手机号。"
		"3、请调出以前申请VPN时的工单截图及电子档后（注意有效期，超时请重新申请VPN权限），联系福莱特运维人员核查。"
		"请<a href='http://111.23.233.129/contact'>查看管理人员列表</a>。")

	redis_handle.adminPost(conn, weixinId, "安装客户端时未出现开始安装的图标", "1、请检查是否启用了杀毒软件，关闭后重新安装。2、从控制面板的程序里将福莱特网络准入相关软件卸载，重启，再右键点击安装程序，以管理员身份运行。")

	redis_handle.adminPost(conn, weixinId, "安装客户端后无法启动程序", "1、请检查是否启用了杀毒软件，关闭后重新安装。2、从控制面板的程序里将福莱特网络准入相关软件卸载，重启，再右键点击安装程序，以管理员身份运行。")

	redis_handle.adminPost(conn, weixinId, "申请管控账号", "在eoms系统中提交工单申请，请<a href='http://111.23.233.129/'>下载安全管控平台申请工单操作手册\管控平台账号&VPN申请表</a>")

	redis_handle.adminPost(conn, weixinId, "申请资源登录", "在eoms系统中提交工单申请，请<a href='http://111.23.233.129/'>下载安全管控平台申请工单操作手册\湖南移动安全管控平台应用资源授权调研表</a>")

	redis_handle.adminPost(conn, weixinId, "申请管理权限", "在eoms系统中提交工单申请，请<a href='http://111.23.233.129/'>下载安全管控平台申请工单操作手册\湖南移动安全管控平台应用资源授权调研表</a>")

	redis_handle.adminPost(conn, weixinId, "申请VPN权限", "在eoms系统中提交工单申请，请<a href='http://111.23.233.129/'>下载安全管控平台申请工单操作手册\管控平台账号&VPN申请表</a>")

	redis_handle.adminPost(conn, weixinId, "点击资源时提示citrix错误，无法连接至citrix xenapp服务器", "服务器宕机，需发送报障工单,请输入[报障 故障类别id IP 资源名称]", 1)

	redis_handle.adminPost(conn, weixinId, "点击资源时提示citrix错误，与此计算机的连接数量是有限的", "服务器宕机，需发送报障工单,请输入[报障 故障类别id IP 资源名称]", 1)

	redis_handle.adminPost(conn, weixinId, "点击资源时提示citrix错误，Citrix XenApp license acquistion error(500)", "服务器宕机，需发送报障工单,请输入[报障 故障类别id IP 资源名称]", 1)

	redis_handle.adminPost(conn, weixinId, "点击资源时提示citrix错误，Citrix XenApp license acquistion error(6)", "服务器宕机，需发送报障工单,请输入[报障 故障类别id IP 资源名称]", 1)

	redis_handle.adminPost(conn, weixinId, "点击资源时提示citrix错误，无法启动应用程序", "服务器宕机，需发送报障工单,请输入[报障 故障类别id IP 资源名称]", 1)

	redis_handle.adminPost(conn, weixinId, "点击资源时提示citrix错误，Citrix xenapp服务器不可用", "服务器宕机，需发送报障工单,请输入[报障 故障类别id IP 资源名称]", 1)

	redis_handle.adminPost(conn, weixinId, "与此计算机的连接数量是有限的，现在已经使用所有连接", "服务器连接数已满，请稍后再尝试。")

	redis_handle.adminPost(conn, weixinId, "Citrix XenApp license acquition error from XXX server", "服务器连接数已满，请稍后再尝试。")

	redis_handle.adminPost(conn, weixinId, "user Profile Service服务未能登录，无法加载用户配置文件", "域控服务器不能加载用户信息，需发送报障工单,请输入[报障 故障类别id IP 资源名称]", 1)

	redis_handle.adminPost(conn, weixinId, "资源XXX过citrix客户端XXX登录失败", "服务器宕机，需发送报障工单,请输入[报障 故障类别id IP 资源名称]", 1)

	redis_handle.adminPost(conn, weixinId, "Password authentication failed.", "从帐号与密码错误。点击登陆选项中的'密码自学习'，并安装最新版单点登录控件")

	redis_handle.adminPost(conn, weixinId, "登录成功后发现部分授权资源丢失", "管控版本升级或系统管理员进行了账号梳理，请联系系统管理员重新进行授权，<a href='http://111.23.233.129/contact'>查看管理人员列表</a>。")

	redis_handle.adminPost(conn, weixinId, "更换手机号", "在eoms系统中提交工单申请，并于备注中说明。请<a href='http://111.23.233.129/'>下载安全管控平台申请工单操作手册</a>。")


def addUsers():
	redis_handle.addUser(conn, '13365188628', '袁枫', '分公司', '部门')
	redis_handle.addUser(conn, '13365188627', '啊', '分公司', '部门')
#
addUsers()
addArticles()