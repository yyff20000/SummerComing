# -*- coding:utf-8 -*-
import redis,time,redis_handle

# def init(lalaland):#初始化常见故障，solved:id.scenario（场景）,detail（故障描述）,solution（解决方法）,quoted（被查询次数）
# 	lalaland.hmset('solved:'+'1',{'scenario':'VPN登录','detail':'网准登陆时，[正在从自助服务器上加载数据][自助服务暂时无法使用]','solution':'程序服务启动失败，重启本地终端。','quoted':10,})
# 	lalaland.hmset('solved:'+'2',{'scenario':'VPN登录','detail':'点击获取动态口令后提示已获取，但无法收到短信','solution':'1、请检查手机接收是否设置黑名单。2、请用账号关联号码联系福莱特运维人员核查手机号是否绑错。点击[系统及联系人]查询最新人员列表。','quoted':10,})
# 	lalaland.hmset('solved:'+'3',{'scenario':'VPN登录','detail':'点击获取动态口令后提示[连接动态口令服务失败，请稍后重试]','solution':'1、请检查当前网络到福莱特动态口令服务器地址是否丢包，如丢包，用手机热点等方式再尝试一次。点击[系统及联系人]查询最新服务器地址。','quoted':10,})
# 	lalaland.hmset('solved:'+'4',{'scenario':'VPN登录','detail':'点击获取动态口令后提示[用户标识无效，申请动态口令失败][禁止外网登录]','solution':'1、请检查是否为网管准入客户端。2、请检查是否输入了正确的手机号。3、请调出以前申请VPN时的工单截图及电子档后（注意有效期，超时请重新申请VPN权限），联系福莱特运维人员核查。点击[系统及联系人]查询最新人员列表。','quoted':10,})
# 	lalaland.hmset('solved:'+'5',{'scenario':'VPN登录','detail':'安装客户端时未出现[开始安装]的图标，或安装后无法启动程序','solution':'1、请检查是否启用了杀毒软件，关闭后重新安装。2、从控制面板的程序里将福莱特网络准入相关软件卸载，重启，再右键点击安装程序，以管理员身份运行。','quoted':10,})
# 	lalaland.hmset('solved:'+'6',{'scenario':'账号权限','detail':'申请管控账号','solution':'在eoms系统中提交工单申请，参见[常用资料]:安全管控平台申请工单操作手册\管控平台账号&VPN申请表','quoted':10,})
# 	lalaland.hmset('solved:'+'7',{'scenario':'账号权限','detail':'申请资源登录/管理权限','solution':'在eoms系统中提交工单申请，参见[常用资料]:安全管控平台申请工单操作手册\湖南移动安全管控平台应用资源授权调研表','quoted':10,})
# 	lalaland.hmset('solved:'+'8',{'scenario':'账号权限','detail':'申请VPN权限','solution':'在eoms系统中提交工单申请，参见[常用资料]:安全管控平台申请工单操作手册\管控平台账号&VPN申请表','quoted':10,})
# 	lalaland.hmset('solved:'+'9',{'scenario':'资源登录','detail':'点击资源时提示citrix错误，[无法连接至citrix xenapp服务器]or[与此计算机的连接数量是有限的]or[Citrix XenApp license acquistion error(500)]or[Citrix XenApp license acquistion error(6)]or[无法启动应用程序]or[citrix xenapp服务器不可用]','solution':'服务器宕机，需发送，点击[快速报障]（IP）','quoted':10,})
# 	lalaland.hmset('solved:'+'10',{'scenario':'资源登录','detail':'[与此计算机的连接数量是有限的，现在已经使用所有连接]，[Citrix XenApp license acquition error from XXXX server]','solution':'服务器连接数已满，请稍后再尝试。','quoted':10,})
# 	lalaland.hmset('solved:'+'11',{'scenario':'资源登录','detail':'[user Profile Service服务未能登录，无法加载用户配置文件]','solution':'域控服务器不能加载用户信息，点击[快速报障](需管控主账号和IP）','quoted':10,})
# 	lalaland.hmset('solved:'+'12',{'scenario':'资源登录','detail':'[资源XXXX过citrix客户端YYYY登录失败]','solution':'服务器宕机，需发送，点击[快速报障]（需要提供报错截图里的资源名称YYYY）','quoted':10,})
# 	lalaland.hmset('solved:'+'13',{'scenario':'资源登录','detail':'[Password authentication failed.]','solution':'从帐号与密码错误。点击登陆选项中的“密码自学习”，并安装最新版单点登录控件','quoted':10,})
# 	lalaland.hmset('solved:'+'14',{'scenario':'资源登录','detail':'登录成功后发现部分授权资源丢失','solution':'管控版本升级或系统管理员进行了账号梳理，请联系系统管理员重新进行授权，点击[系统及联系人]查询最新人员列表。','quoted':10,})
# 	lalaland.hmset('solved:'+'15',{'scenario':'账号权限','detail':'更换手机号','solution':'在eoms系统中提交工单申请，并于备注中说明。参见[常用资料]:安全管控平台申请工单操作手册','quoted':10,})
# def recentPro(lalaland):#为问题列表按照提交时间进行排序，返回近十个prob:id，显示为probtitle，链接为prob的反馈时间，所属组织，所属系统，问题描述，解决时间，解决方式
# 	pass
# def document(lalaland):#初始化常用资料，doc:id. assort（分类）,name（名称），detail（人员或者地址）
# 	lalaland.hmset('doc:1',{'assort':'管控平台常用','name':'福莱特动态口令服务器','detail':'211.142.211.98（禁ping，请用telnet 211.142.211.98 6005测试）',})
# 	lalaland.hmset('doc:2',{'assort':'管控平台常用','name':'福莱特运维人员','detail':'宋涛，15116173586，songtao@forenet.cn',})
# 	lalaland.hmset('doc:3',{'assort':'管控平台常用','name':'泰岳运维人员（日常运维及故障处理）','detail':'贺奇丰：13875827652，heqifeng@ultrapower.com.cn  ',})
# 	lalaland.hmset('doc:4',{'assort':'管控平台常用','name':'泰岳运维人员（技术支撑）','detail':'程清云：15388983153，chengqingyun@ultrapower.com.cn',})
# 	lalaland.hmset('doc:5',{'assort':'管控平台常用','name':'泰岳运维人员（合规审计）','detail':'黄思思：18773160128，huangsisi1@ultrapower.com.cn   ',})
# 	lalaland.hmset('doc:6',{'assort':'资料下载','name':'常见资料下载','detail':'链接: https://pan.baidu.com/s/1chP1ka 密码: ftn6',})
# 	lalaland.hmset('doc:7',{'assort':'地市管理员','name':'衡阳管控管理员','detail':'网络维护中心彭清华',})
# 	lalaland.hmset('doc:8',{'assort':'地市管理员','name':'常德管控管理员','detail':'客户响应中心彭峰',})
# 	lalaland.hmset('doc:9',{'assort':'地市管理员','name':'郴州管控管理员','detail':'网络维护中心罗志宁',})
# 	lalaland.hmset('doc:10',{'assort':'地市管理员','name':'怀化管控管理员','detail':'网络部杨青聪',})
# 	lalaland.hmset('doc:11',{'assort':'地市管理员','name':'娄底管控管理员','detail':'网维中心罗枝花',})
# 	lalaland.hmset('doc:12',{'assort':'地市管理员','name':'娄底管控管理员','detail':'网维中心康军',})
# 	lalaland.hmset('doc:13',{'assort':'地市管理员','name':'邵阳管控管理员','detail':'网络优化中心谢思艺',})
# 	lalaland.hmset('doc:14',{'assort':'地市管理员','name':'湘潭管控管理员','detail':'客户响应中心李定',})
# 	lalaland.hmset('doc:15',{'assort':'地市管理员','name':'益阳管控管理员','detail':'网络维护中心李盼',})
# 	lalaland.hmset('doc:16',{'assort':'地市管理员','name':'益阳管控管理员','detail':'网络维护中心刘楷文',})
# 	lalaland.hmset('doc:17',{'assort':'地市管理员','name':'永州管控管理员','detail':'网络部肖荣杰',})
# 	lalaland.hmset('doc:18',{'assort':'地市管理员','name':'岳阳管控管理员','detail':'客户响应中心王继东',})
# 	lalaland.hmset('doc:19',{'assort':'地市管理员','name':'张家界管控管理员','detail':'客户响应中心李英豪',})
# 	lalaland.hmset('doc:20',{'assort':'地市管理员','name':'长沙管控管理员','detail':'网络服务中心王梦杰',})
# 	lalaland.hmset('doc:21',{'assort':'地市管理员','name':'长沙管控管理员','detail':'客户响应中心苏叙涛',})
# 	lalaland.hmset('doc:22',{'assort':'地市管理员','name':'株洲管控管理员','detail':'网络维护中心李海鸥',})
# 	lalaland.hmset('doc:23',{'assort':'地市管理员','name':'自治州管控管理员','detail':'客户响应中心徐远松',})
# 	lalaland.hmset('doc:24',{'assort':'地市管理员','name':'自治州管控管理员','detail':'客户响应中心许连杰',})
# 	lalaland.hmset('doc:25',{'assort':'系统管理员','name':'CDN','detail':'互联网室刘华沙',})
# 	lalaland.hmset('doc:26',{'assort':'系统管理员','name':'DNS系统','detail':'互联网室于文晓',})
# 	lalaland.hmset('doc:27',{'assort':'系统管理员','name':'DPI','detail':'互联网室周雅红',})
# 	lalaland.hmset('doc:28',{'assort':'系统管理员','name':'IP承载网','detail':'互联网室戴佳伟',})
# 	lalaland.hmset('doc:29',{'assort':'系统管理员','name':'Radius系统','detail':'互联网室王喆',})
# 	lalaland.hmset('doc:30',{'assort':'系统管理员','name':'cmnet系统','detail':'互联网室刘起松',})
# 	lalaland.hmset('doc:31',{'assort':'系统管理员','name':'mdcn系统','detail':'互联网室赵尚桃',})
# 	lalaland.hmset('doc:32',{'assort':'系统管理员','name':'互联网内容资源管理平台','detail':'互联网室于文晓',})
# 	lalaland.hmset('doc:33',{'assort':'系统管理员','name':'互联网流量分析系统','detail':'互联网室刘华沙',})
# 	lalaland.hmset('doc:34',{'assort':'系统管理员','name':'互联网电视CDN','detail':'互联网室刘华沙',})
# 	lalaland.hmset('doc:35',{'assort':'系统管理员','name':'互联网网络质量监测','detail':'互联网室胡兴',})
# 	lalaland.hmset('doc:36',{'assort':'系统管理员','name':'华为CACHE','detail':'互联网室刘华沙',})
# 	lalaland.hmset('doc:37',{'assort':'系统管理员','name':'华为UCDN系统','detail':'互联网室李健',})
# 	lalaland.hmset('doc:38',{'assort':'系统管理员','name':'华为_M2M','detail':'互联网室许文卓',})
# 	lalaland.hmset('doc:39',{'assort':'系统管理员','name':'带外网管','detail':'互联网室赵尚桃',})
# 	lalaland.hmset('doc:40',{'assort':'系统管理员','name':'智能IP管理系统','detail':'互联网室刘阳',})
# 	lalaland.hmset('doc:41',{'assort':'系统管理员','name':'流量清洗系统','detail':'互联网室刘起松',})
# 	lalaland.hmset('doc:42',{'assort':'系统管理员','name':'自建CACHE系统','detail':'互联网室刘华沙',})
# 	lalaland.hmset('doc:43',{'assort':'系统管理员','name':'不良信息检测系统','detail':'互联网室/信安部',})
# 	lalaland.hmset('doc:44',{'assort':'系统管理员','name':'核心机房容量预警','detail':'传输室蒋斐',})
# 	lalaland.hmset('doc:45',{'assort':'系统管理员','name':'流量监控系统','detail':'传输室黎玮',})
# 	lalaland.hmset('doc:46',{'assort':'系统管理员','name':'网管电源后评估系统','detail':'传输室肖坤平',})
# 	lalaland.hmset('doc:47',{'assort':'系统管理员','name':'互联网欺诈网络治理系统','detail':'信安部朱子涵',})
# 	lalaland.hmset('doc:48',{'assort':'系统管理员','name':'DRA信令采集','detail':'核心网室曾国顺',})
# 	lalaland.hmset('doc:49',{'assort':'系统管理员','name':'HLR系统','detail':'核心网室彭昂',})
# 	lalaland.hmset('doc:50',{'assort':'系统管理员','name':'IMS系统','detail':'核心网室彭翔',})
# 	lalaland.hmset('doc:51',{'assort':'系统管理员','name':'IP可视化','detail':'核心网室邹晖',})
# 	lalaland.hmset('doc:52',{'assort':'系统管理员','name':'LDRA','detail':'核心网室曾国顺',})
# 	lalaland.hmset('doc:53',{'assort':'系统管理员','name':'LSTP','detail':'核心网室唐宇清',})
# 	lalaland.hmset('doc:54',{'assort':'系统管理员','name':'PS域核心网','detail':'核心网室戴晓群',})
# 	lalaland.hmset('doc:55',{'assort':'系统管理员','name':'VOLTE系统','detail':'核心网室彭翔',})
# 	lalaland.hmset('doc:56',{'assort':'系统管理员','name':'分组域核心网','detail':'核心网室王磊',})
# 	lalaland.hmset('doc:57',{'assort':'系统管理员','name':'语音交换','detail':'核心网室胡婧',})
# 	lalaland.hmset('doc:58',{'assort':'系统管理员','name':'诺西Traffica','detail':'核心网室马东洋',})
# 	lalaland.hmset('doc:59',{'assort':'系统管理员','name':'诺西专家运维平台','detail':'核心网室马东洋',})
# 	lalaland.hmset('doc:60',{'assort':'系统管理员','name':'金硕业务拨测系统','detail':'核心网室马东洋',})
# 	lalaland.hmset('doc:61',{'assort':'系统管理员','name':'长途软交换','detail':'核心网室李莎',})
# 	lalaland.hmset('doc:62',{'assort':'系统管理员','name':'防火墙日志采集-中兴','detail':'核心网室李宁',})
# 	lalaland.hmset('doc:63',{'assort':'系统管理员','name':'骚扰电话监控系统','detail':'核心网室王丹阳',})
# 	lalaland.hmset('doc:64',{'assort':'系统管理员','name':'测试数据管理分析系统','detail':'网优中心宋雷',})
# 	lalaland.hmset('doc:65',{'assort':'系统管理员','name':'网优平台','detail':'网优中心宋雷',})
# 	lalaland.hmset('doc:66',{'assort':'系统管理员','name':'4G_OMC','detail':'网管室吴应攀',})
# 	lalaland.hmset('doc:67',{'assort':'系统管理员','name':'4G小基站OMC','detail':'网管室吴应攀',})
# 	lalaland.hmset('doc:68',{'assort':'系统管理员','name':'Arcgis','detail':'网管室邓鹏',})
# 	lalaland.hmset('doc:69',{'assort':'系统管理员','name':'EMOS系统','detail':'网管室邓鹏',})
# 	lalaland.hmset('doc:70',{'assort':'系统管理员','name':'VOLTE信令监测系统','detail':'网管室李茂桂',})
# 	lalaland.hmset('doc:71',{'assort':'系统管理员','name':'上网日志留存系统','detail':'网管室王业亮',})
# 	lalaland.hmset('doc:72',{'assort':'系统管理员','name':'中兴LTE信令监测','detail':'网管室王业亮',})
# 	lalaland.hmset('doc:73',{'assort':'系统管理员','name':'交换网管','detail':'网管室吴应攀',})
# 	lalaland.hmset('doc:74',{'assort':'系统管理员','name':'传输外线资源采集平台','detail':'网管室戴佳伟',})
# 	lalaland.hmset('doc:75',{'assort':'系统管理员','name':'传输综合网管','detail':'网管室罗武平',})
# 	lalaland.hmset('doc:76',{'assort':'系统管理员','name':'信令监测-CS域','detail':'网管室王业亮',})
# 	lalaland.hmset('doc:77',{'assort':'系统管理员','name':'信令监测-PS域','detail':'网管室王业亮',})
# 	lalaland.hmset('doc:78',{'assort':'系统管理员','name':'动力环境监控CSC平台','detail':'网管室罗武平',})
# 	lalaland.hmset('doc:79',{'assort':'系统管理员','name':'华为虚拟化管理节点','detail':'网管室王业亮',})
# 	lalaland.hmset('doc:80',{'assort':'系统管理员','name':'家客日志留存系统','detail':'网管室齐志辉',})
# 	lalaland.hmset('doc:81',{'assort':'系统管理员','name':'家客软探针','detail':'网管室齐志辉',})
# 	lalaland.hmset('doc:82',{'assort':'系统管理员','name':'宽带接入平台','detail':'网管室齐志辉',})
# 	lalaland.hmset('doc:83',{'assort':'系统管理员','name':'性能管理','detail':'网管室徐仕成',})
# 	lalaland.hmset('doc:84',{'assort':'系统管理员','name':'数字家庭管理平台','detail':'网管室齐志辉',})
# 	lalaland.hmset('doc:85',{'assort':'系统管理员','name':'数据网管','detail':'网管室罗武平',})
# 	lalaland.hmset('doc:86',{'assort':'系统管理员','name':'无线OMC','detail':'网管室吴应攀',})
# 	lalaland.hmset('doc:87',{'assort':'系统管理员','name':'无线omc','detail':'网管室吴应攀',})
# 	lalaland.hmset('doc:88',{'assort':'系统管理员','name':'湖南移动家宽端到端质量分析系统','detail':'网管室齐志辉',})
# 	lalaland.hmset('doc:89',{'assort':'系统管理员','name':'湖南移动感知提升','detail':'网管室徐仕成',})
# 	lalaland.hmset('doc:90',{'assort':'系统管理员','name':'猫池养卡挖掘设备','detail':'网管室陶娟',})
# 	lalaland.hmset('doc:91',{'assort':'系统管理员','name':'省干EMS','detail':'网管室吴应攀',})
# 	lalaland.hmset('doc:92',{'assort':'系统管理员','name':'统一采集平台','detail':'网管室屈罡',})
# 	lalaland.hmset('doc:93',{'assort':'系统管理员','name':'综合分析系统_浪潮','detail':'网管室徐仕成',})
# 	lalaland.hmset('doc:94',{'assort':'系统管理员','name':'综合呈现系统','detail':'网管室秦华',})
# 	lalaland.hmset('doc:95',{'assort':'系统管理员','name':'综合监控','detail':'网管室秦华',})
# 	lalaland.hmset('doc:96',{'assort':'系统管理员','name':'综合资源管理系统','detail':'网管室江友军',})
# 	lalaland.hmset('doc:97',{'assort':'系统管理员','name':'网管网络维护','detail':'网管室王业亮',})
# 	lalaland.hmset('doc:98',{'assort':'系统管理员','name':'网络支撑客服系统','detail':'网管室李茂桂',})
# 	lalaland.hmset('doc:99',{'assort':'系统管理员','name':'自主研发资源池','detail':'网管室黄磊',})
# 	lalaland.hmset('doc:100',{'assort':'系统管理员','name':'话务网管','detail':'网管室秦华',})
# 	lalaland.hmset('doc:101',{'assort':'系统管理员','name':'集中故障管理大数据挖掘分析','detail':'网管室徐仕成',})
# 	lalaland.hmset('doc:102',{'assort':'系统管理员','name':'1259系统','detail':'网络安全室李聃',})
# 	lalaland.hmset('doc:103',{'assort':'系统管理员','name':'IDC信安系统','detail':'网络安全室吴丽巧',})
# 	lalaland.hmset('doc:104',{'assort':'系统管理员','name':'IDC系统','detail':'网络安全室吴丽巧',})
# 	lalaland.hmset('doc:105',{'assort':'系统管理员','name':'IDC防病毒','detail':'网络安全室张荣辉',})
# 	lalaland.hmset('doc:106',{'assort':'系统管理员','name':'LSP系统','detail':'网络安全室李聃',})
# 	lalaland.hmset('doc:107',{'assort':'系统管理员','name':'misc系统','detail':'网络安全室曾宇',})
# 	lalaland.hmset('doc:108',{'assort':'系统管理员','name':'wap系统','detail':'网络安全室郑秀娟',})
# 	lalaland.hmset('doc:109',{'assort':'系统管理员','name':'东信北邮智能网','detail':'网络安全室唐赛',})
# 	lalaland.hmset('doc:110',{'assort':'系统管理员','name':'中兴智能网','detail':'网络安全室谢秋杨',})
# 	lalaland.hmset('doc:111',{'assort':'系统管理员','name':'互通网关','detail':'网络安全室李聃',})
# 	lalaland.hmset('doc:112',{'assort':'系统管理员','name':'垃圾短信','detail':'网络安全室张纯',})
# 	lalaland.hmset('doc:113',{'assort':'系统管理员','name':'安全管控平台','detail':'网络安全室向玉卉',})
# 	lalaland.hmset('doc:114',{'assort':'系统管理员','name':'宽带测速系统','detail':'网络安全室吴丽巧',})
# 	lalaland.hmset('doc:115',{'assort':'系统管理员','name':'彩信系统','detail':'网络安全室郭谦伟',})
# 	lalaland.hmset('doc:116',{'assort':'系统管理员','name':'彩铃系统','detail':'网络安全室杨晓芳',})
# 	lalaland.hmset('doc:117',{'assort':'系统管理员','name':'支撑网关','detail':'网络安全室李聃',})
# 	lalaland.hmset('doc:118',{'assort':'系统管理员','name':'梦网网关','detail':'网络安全室李聃',})
# 	lalaland.hmset('doc:119',{'assort':'系统管理员','name':'短信专家','detail':'网络安全室王新宇',})
# 	lalaland.hmset('doc:120',{'assort':'系统管理员','name':'短信中心','detail':'网络安全室何宾',})
# 	lalaland.hmset('doc:121',{'assort':'系统管理员','name':'短号短信系统','detail':'网络安全室何宾',})
# 	lalaland.hmset('doc:122',{'assort':'系统管理员','name':'综合网关-华为','detail':'网络安全室谢智斌',})
# 	lalaland.hmset('doc:123',{'assort':'系统管理员','name':'综合网关-诺西','detail':'网络安全室谢智斌',})
# 	lalaland.hmset('doc:124',{'assort':'系统管理员','name':'行业网关','detail':'网络安全室王新宇',})
# 	lalaland.hmset('doc:125',{'assort':'系统管理员','name':'视频监控平台','detail':'网络安全室吴丽巧',})
# 	lalaland.hmset('doc:126',{'assort':'系统管理员','name':'防病毒系统','detail':'网络安全室张荣辉',})
#
#
weixinId = 'oDFHUv8_F7PVZc0oMrVjlBrlMKto'

def main():

	# r = redis.Redis(host='192.168.140.130',port=6379,password='nino38')

	conn = redis_handle.connect()  # 连接新浪云服务器

	redis_handle.post_article(conn, weixinId, "网准登陆时，正在从自助服务器上加载数据", "程序服务启动失败，重启本地终端。")

	redis_handle.post_article(conn, weixinId, "网准登陆时，自助服务暂时无法使用", "程序服务启动失败，重启本地终端。")

	redis_handle.post_article(conn, weixinId, "点击获取动态口令后提示已获取，但无法收到短信", "1、请检查手机接收是否设置黑名单"
		"。2、请用账号关联号码联系福莱特运维人员核查手机号是否绑错。请于链接: https://pan.baidu.com/s/1chP1ka 密码: ftn6处查看管理人员列表。")

	redis_handle.post_article(conn, weixinId, "点击获取动态口令后提示连接动态口令服务失败，请稍后重试", "1、请检查当前网络到"
		"福莱特动态口令服务器地址是否丢包，如丢包，用手机热点等方式再尝试一次。请于链接: https://pan.baidu.com/s/1chP1ka 密码: ftn6处下载最新服务器地址。")

	redis_handle.post_article(conn, weixinId, "点击获取动态口令后提示用户标识无效，申请动态口令失败", "1、请检查是否为网管准入客户端。"
		"2、请检查是否输入了正确的手机号。3、请调出以前申请VPN时的工单截图及电子档后（注意有效期，超时请重新申请VPN权限），联系福莱特运维人员核查。"
		"请于链接: https://pan.baidu.com/s/1chP1ka 密码: ftn6处下载管理人员列表。")

	redis_handle.post_article(conn, weixinId, "点击获取动态口令后提示禁止外网登录", "1、请检查是否为网管准入客户端。2、请检查是否输入了正确的手机号。"
		"3、请调出以前申请VPN时的工单截图及电子档后（注意有效期，超时请重新申请VPN权限），联系福莱特运维人员核查。"
		"请于链接: https://pan.baidu.com/s/1chP1ka 密码: ftn6处下载管理人员列表。")

	redis_handle.post_article(conn, weixinId, "安装客户端时未出现开始安装的图标", "1、请检查是否启用了杀毒软件，关闭后重新安装。2、从控制面板的程序里将福莱特网络准入相关软件卸载，重启，再右键点击安装程序，以管理员身份运行。")

	redis_handle.post_article(conn, weixinId, "安装客户端后无法启动程序", "1、请检查是否启用了杀毒软件，关闭后重新安装。2、从控制面板的程序里将福莱特网络准入相关软件卸载，重启，再右键点击安装程序，以管理员身份运行。")

	redis_handle.post_article(conn, weixinId, "申请管控账号", "在eoms系统中提交工单申请，请于链接: https://pan.baidu.com/s/1chP1ka 密码: ftn6处下载安全管控平台申请工单操作手册\管控平台账号&VPN申请表")

	redis_handle.post_article(conn, weixinId, "申请资源登录", "在eoms系统中提交工单申请，请于链接: https://pan.baidu.com/s/1chP1ka 密码: ftn6处下载安全管控平台申请工单操作手册\湖南移动安全管控平台应用资源授权调研表")

	redis_handle.post_article(conn, weixinId, "申请管理权限", "在eoms系统中提交工单申请，请于链接: https://pan.baidu.com/s/1chP1ka 密码: ftn6处下载安全管控平台申请工单操作手册\湖南移动安全管控平台应用资源授权调研表")

	redis_handle.post_article(conn, weixinId, "申请VPN权限", "在eoms系统中提交工单申请，请于链接: https://pan.baidu.com/s/1chP1ka 密码: ftn6处下载安全管控平台申请工单操作手册\管控平台账号&VPN申请表")

	redis_handle.post_article(conn, weixinId, "点击资源时提示citrix错误，无法连接至citrix xenapp服务器", "服务器宕机，需发送报障工单")

	redis_handle.post_article(conn, weixinId, "点击资源时提示citrix错误，与此计算机的连接数量是有限的", "服务器宕机，需发送报障工单")

	redis_handle.post_article(conn, weixinId, "点击资源时提示citrix错误，Citrix XenApp license acquistion error(500)", "服务器宕机，需发送报障工单")

	redis_handle.post_article(conn, weixinId, "点击资源时提示citrix错误，Citrix XenApp license acquistion error(6)", "服务器宕机，需发送报障工单")

	redis_handle.post_article(conn, weixinId, "点击资源时提示citrix错误，无法启动应用程序", "服务器宕机，需发送报障工单")

	redis_handle.post_article(conn, weixinId, "点击资源时提示citrix错误，Citrix xenapp服务器不可用", "服务器宕机，需发送报障工单")

	redis_handle.post_article(conn, weixinId, "与此计算机的连接数量是有限的，现在已经使用所有连接", "服务器连接数已满，请稍后再尝试。")

	redis_handle.post_article(conn, weixinId, "Citrix XenApp license acquition error from XXX server", "服务器连接数已满，请稍后再尝试。")

	redis_handle.post_article(conn, weixinId, "user Profile Service服务未能登录，无法加载用户配置文件", "域控服务器不能加载用户信息，需发送报障工单")

	redis_handle.post_article(conn, weixinId, "资源XXX过citrix客户端XXX登录失败", "服务器宕机，需发送报障工单")

	redis_handle.post_article(conn, weixinId, "Password authentication failed.", "从帐号与密码错误。点击登陆选项中的'密码自学习'，并安装最新版单点登录控件")

	redis_handle.post_article(conn, weixinId, "登录成功后发现部分授权资源丢失", "管控版本升级或系统管理员进行了账号梳理，请联系系统管理员重新进行授权，于链接: https://pan.baidu.com/s/1chP1ka 密码: ftn6处下载管理人员列表。")

	redis_handle.post_article(conn, weixinId, "更换手机号", "在eoms系统中提交工单申请，并于备注中说明。请于链接: https://pan.baidu.com/s/1chP1ka 密码: ftn6处下载安全管控平台申请工单操作手册")

if __name__=='__main__':
	main()
