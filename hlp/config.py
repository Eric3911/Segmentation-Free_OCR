#!/usr/bin/env python
__author__ = 'solivr'

import os
import json
import time
from glob import glob


class CONST:
    DIMENSION_REDUCTION_W_POOLING = 2 * 2 # 2x2 pooling in dimension W on layer 1 and 2


class Alphabet:
    LettersLowercase = 'abcdefghijklmnopqrstuvwxyz'  # 26
    LettersCapitals = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # 26
    Digits = '0123456789'  # 10
    Symbols = '~!@#$%^&*()+-=,.。<>/?\`;:\'"[]{}《》'  # 33
    # Symbols = "'.,:;-=()[]{}/°" #17

    # Symbols = " '.,:-="  # 7
    # 3755 ChineseChar
    # with open('hlp/dict.txt', encoding='utf8') as to_read:
    # ChineseChar = ''.join(map(str.strip, to_read.readlines()))
    ChineseChar = '啊阿埃挨哎唉哀皑癌蔼矮艾碍爱隘鞍氨安俺按暗岸胺案肮昂盎凹敖熬翱袄傲奥懊澳芭捌扒叭吧笆八疤巴拔跋靶把耙坝霸罢爸白柏百摆佰败拜稗斑班搬扳般颁板版扮拌伴瓣半办绊邦帮梆榜膀绑棒磅蚌镑傍谤苞胞包褒剥薄雹保堡饱宝抱报暴豹鲍爆杯碑悲卑北辈背贝钡倍狈备惫焙被奔苯本笨崩绷甭泵蹦迸逼鼻比鄙笔彼碧蓖蔽毕毙毖币庇痹闭敝弊必辟壁臂避陛鞭边编贬扁便变卞辨辩辫遍标彪膘表鳖憋别瘪彬斌濒滨宾摈兵冰柄丙秉饼炳病并玻菠播拨钵波博勃搏铂箔伯帛舶脖膊渤泊驳捕卜哺补埠不布步簿部怖擦猜裁材才财睬踩采彩菜蔡餐参蚕残惭惨灿苍舱仓沧藏操糙槽曹草厕策侧册测层蹭插叉茬茶查碴搽察岔差诧拆柴豺搀掺蝉馋谗缠铲产阐颤昌猖场尝常长偿肠厂敞畅唱倡超抄钞朝嘲潮巢吵炒车扯撤掣彻澈郴臣辰尘晨忱沉陈趁衬撑称城橙成呈乘程惩澄诚承逞骋秤吃痴持匙池迟弛驰耻齿侈尺赤翅斥炽充冲虫崇宠抽酬畴踌稠愁筹仇绸瞅丑臭初出橱厨躇锄雏滁除楚础储矗搐触处揣川穿椽传船喘串疮窗幢床闯创吹炊捶锤垂春椿醇唇淳纯蠢戳绰疵茨磁雌辞慈瓷词此刺赐次聪葱囱匆从丛凑粗醋簇促蹿篡窜摧崔催脆瘁粹淬翠村存寸磋撮搓措挫错搭达答瘩打大呆歹傣戴带殆代贷袋待逮怠耽担丹单郸掸胆旦氮但惮淡诞弹蛋当挡党荡档刀捣蹈倒岛祷导到稻悼道盗德得的蹬灯登等瞪凳邓堤低滴迪敌笛狄涤翟嫡抵底地蒂第帝弟递缔颠掂滇碘点典靛垫电佃甸店惦奠淀殿碉叼雕凋刁掉吊钓调跌爹碟蝶迭谍叠丁盯叮钉顶鼎锭定订丢东冬董懂动栋侗恫冻洞兜抖斗陡豆逗痘都督毒犊独读堵睹赌杜镀肚度渡妒端短锻段断缎堆兑队对墩吨蹲敦顿囤钝盾遁掇哆多夺垛躲朵跺舵剁惰堕蛾峨鹅俄额讹娥恶厄扼遏鄂饿恩而儿耳尔饵洱二贰发罚筏伐乏阀法珐藩帆番翻樊矾钒繁凡烦反返范贩犯饭泛坊芳方肪房防妨仿访纺放菲非啡飞肥匪诽吠肺废沸费芬酚吩氛分纷坟焚汾粉奋份忿愤粪丰封枫蜂峰锋风疯烽逢冯缝讽奉凤佛否夫敷肤孵扶拂辐幅氟符伏俘服浮涪福袱弗甫抚辅俯釜斧脯腑府腐赴副覆赋复傅付阜父腹负富讣附妇缚咐噶嘎该改概钙盖溉干甘杆柑竿肝赶感秆敢赣冈刚钢缸肛纲岗港杠篙皋高膏羔糕搞镐稿告哥歌搁戈鸽胳疙割革葛格蛤阁隔铬个各给根跟耕更庚羹埂耿梗工攻功恭龚供躬公宫弓巩汞拱贡共钩勾沟苟狗垢构购够辜菇咕箍估沽孤姑鼓古蛊骨谷股故顾固雇刮瓜剐寡挂褂乖拐怪棺关官冠观管馆罐惯灌贯光广逛瑰规圭硅归龟闺轨鬼诡癸桂柜跪贵刽辊滚棍锅郭国果裹过哈骸孩海氦亥害骇酣憨邯韩含涵寒函喊罕翰撼捍旱憾悍焊汗汉夯杭航壕嚎豪毫郝好耗号浩呵喝荷菏核禾和何合盒貉阂河涸赫褐鹤贺嘿黑痕很狠恨哼亨横衡恒轰哄烘虹鸿洪宏弘红喉侯猴吼厚候后呼乎忽瑚壶葫胡蝴狐糊湖弧虎唬护互沪户花哗华猾滑画划化话槐徊怀淮坏欢环桓还缓换患唤痪豢焕涣宦幻荒慌黄磺蝗簧皇凰惶煌晃幌恍谎灰挥辉徽恢蛔回毁悔慧卉惠晦贿秽会烩汇讳诲绘荤昏婚魂浑混豁活伙火获或惑霍货祸击圾基机畸稽积箕肌饥迹激讥鸡姬绩缉吉极棘辑籍集及急疾汲即嫉级挤几脊己蓟技冀季伎祭剂悸济寄寂计记既忌际妓继纪嘉枷夹佳家加荚颊贾甲钾假稼价架驾嫁歼监坚尖笺间煎兼肩艰奸缄茧检柬碱硷拣捡简俭剪减荐槛鉴践贱见键箭件健舰剑饯渐溅涧建僵姜将浆江疆蒋桨奖讲匠酱降蕉椒礁焦胶交郊浇骄娇嚼搅铰矫侥脚狡角饺缴绞剿教酵轿较叫窖揭接皆秸街阶截劫节桔杰捷睫竭洁结解姐戒藉芥界借介疥诫届巾筋斤金今津襟紧锦仅谨进靳晋禁近烬浸尽劲荆兢茎睛晶鲸京惊精粳经井警景颈静境敬镜径痉靖竟竞净炯窘揪究纠玖韭久灸九酒厩救旧臼舅咎就疚鞠拘狙疽居驹菊局咀矩举沮聚拒据巨具距踞锯俱句惧炬剧捐鹃娟倦眷卷绢撅攫抉掘倔爵觉决诀绝均菌钧军君峻俊竣浚郡骏喀咖卡咯开揩楷凯慨刊堪勘坎砍看康慷糠扛抗亢炕考拷烤靠坷苛柯棵磕颗科壳咳可渴克刻客课肯啃垦恳坑吭空恐孔控抠口扣寇枯哭窟苦酷库裤夸垮挎跨胯块筷侩快宽款匡筐狂框矿眶旷况亏盔岿窥葵奎魁傀馈愧溃坤昆捆困括扩廓阔垃拉喇蜡腊辣啦莱来赖蓝婪栏拦篮阑兰澜谰揽览懒缆烂滥琅榔狼廊郎朗浪捞劳牢老佬姥酪烙涝勒乐雷镭蕾磊累儡垒擂肋类泪棱楞冷厘梨犁黎篱狸离漓理李里鲤礼莉荔吏栗丽厉励砾历利傈例俐痢立粒沥隶力璃哩俩联莲连镰廉怜涟帘敛脸链恋炼练粮凉梁粱良两辆量晾亮谅撩聊僚疗燎寥辽潦了撂镣廖料列裂烈劣猎琳林磷霖临邻鳞淋凛赁吝拎玲菱零龄铃伶羚凌灵陵岭领另令溜琉榴硫馏留刘瘤流柳六龙聋咙笼窿隆垄拢陇楼娄搂篓漏陋芦卢颅庐炉掳卤虏鲁麓碌露路赂鹿潞禄录陆戮驴吕铝侣旅履屡缕虑氯律率滤绿峦挛孪滦卵乱掠略抡轮伦仑沦纶论萝螺罗逻锣箩骡裸落洛骆络妈麻玛码蚂马骂嘛吗埋买麦卖迈脉瞒馒蛮满蔓曼慢漫谩芒茫盲氓忙莽猫茅锚毛矛铆卯茂冒帽貌贸么玫枚梅酶霉煤没眉媒镁每美昧寐妹媚门闷们萌蒙檬盟锰猛梦孟眯醚靡糜迷谜弥米秘觅泌蜜密幂棉眠绵冕免勉娩缅面苗描瞄藐秒渺庙妙蔑灭民抿皿敏悯闽明螟鸣铭名命谬摸摹蘑模膜磨摩魔抹末莫墨默沫漠寞陌谋牟某拇牡亩姆母墓暮幕募慕木目睦牧穆拿哪呐钠那娜纳氖乃奶耐奈南男难囊挠脑恼闹淖呢馁内嫩能妮霓倪泥尼拟你匿腻逆溺蔫拈年碾撵捻念娘酿鸟尿捏聂孽啮镊镍涅您柠狞凝宁拧泞牛扭钮纽脓浓农弄奴努怒女暖虐疟挪懦糯诺哦欧鸥殴藕呕偶沤啪趴爬帕怕琶拍排牌徘湃派攀潘盘磐盼畔判叛乓庞旁耪胖抛咆刨炮袍跑泡呸胚培裴赔陪配佩沛喷盆砰抨烹澎彭蓬棚硼篷膨朋鹏捧碰坯砒霹批披劈琵毗啤脾疲皮匹痞僻屁譬篇偏片骗飘漂瓢票撇瞥拼频贫品聘乒坪苹萍平凭瓶评屏坡泼颇婆破魄迫粕剖扑铺仆莆葡菩蒲埔朴圃普浦谱曝瀑期欺栖戚妻七凄漆柒沏其棋奇歧畦崎脐齐旗祈祁骑起岂乞企启契砌器气迄弃汽泣讫掐恰洽牵扦钎铅千迁签仟谦乾黔钱钳前潜遣浅谴堑嵌欠歉枪呛腔羌墙蔷强抢橇锹敲悄桥瞧乔侨巧鞘撬翘峭俏窍切茄且怯窃钦侵亲秦琴勤芹擒禽寝沁青轻氢倾卿清擎晴氰情顷请庆琼穷秋丘邱球求囚酋泅趋区蛆曲躯屈驱渠取娶龋趣去圈颧权醛泉全痊拳犬券劝缺炔瘸却鹊榷确雀裙群然燃冉染瓤壤攘嚷让饶扰绕惹热壬仁人忍韧任认刃妊纫扔仍日戎茸蓉荣融熔溶容绒冗揉柔肉茹蠕儒孺如辱乳汝入褥软阮蕊瑞锐闰润若弱撒洒萨腮鳃塞赛三叁伞散桑嗓丧搔骚扫嫂瑟色涩森僧莎砂杀刹沙纱傻啥煞筛晒珊苫杉山删煽衫闪陕擅赡膳善汕扇缮墒伤商赏晌上尚裳梢捎稍烧芍勺韶少哨邵绍奢赊蛇舌舍赦摄射慑涉社设砷申呻伸身深娠绅神沈审婶甚肾慎渗声生甥牲升绳省盛剩胜圣师失狮施湿诗尸虱十石拾时什食蚀实识史矢使屎驶始式示士世柿事拭誓逝势是嗜噬适仕侍释饰氏市恃室视试收手首守寿授售受瘦兽蔬枢梳殊抒输叔舒淑疏书赎孰熟薯暑曙署蜀黍鼠属术述树束戍竖墅庶数漱恕刷耍摔衰甩帅栓拴霜双爽谁水睡税吮瞬顺舜说硕朔烁斯撕嘶思私司丝死肆寺嗣四伺似饲巳松耸怂颂送宋讼诵搜艘擞嗽苏酥俗素速粟僳塑溯宿诉肃酸蒜算虽隋随绥髓碎岁穗遂隧祟孙损笋蓑梭唆缩琐索锁所塌他它她塔獭挞蹋踏胎苔抬台泰酞太态汰坍摊贪瘫滩坛檀痰潭谭谈坦毯袒碳探叹炭汤塘搪堂棠膛唐糖倘躺淌趟烫掏涛滔绦萄桃逃淘陶讨套特藤腾疼誊梯剔踢锑提题蹄啼体替嚏惕涕剃屉天添填田甜恬舔腆挑条迢眺跳贴铁帖厅听烃汀廷停亭庭挺艇通桐酮瞳同铜彤童桶捅筒统痛偷投头透凸秃突图徒途涂屠土吐兔湍团推颓腿蜕褪退吞屯臀拖托脱鸵陀驮驼椭妥拓唾挖哇蛙洼娃瓦袜歪外豌弯湾玩顽丸烷完碗挽晚皖惋宛婉万腕汪王亡枉网往旺望忘妄威巍微危韦违桅围唯惟为潍维苇萎委伟伪尾纬未蔚味畏胃喂魏位渭谓尉慰卫瘟温蚊文闻纹吻稳紊问嗡翁瓮挝蜗涡窝我斡卧握沃巫呜钨乌污诬屋无芜梧吾吴毋武五捂午舞伍侮坞戊雾晤物勿务悟误昔熙析西硒矽晰嘻吸锡牺稀息希悉膝夕惜熄烯溪汐犀檄袭席习媳喜铣洗系隙戏细瞎虾匣霞辖暇峡侠狭下厦夏吓掀锨先仙鲜纤咸贤衔舷闲涎弦嫌显险现献县腺馅羡宪陷限线相厢镶香箱襄湘乡翔祥详想响享项巷橡像向象萧硝霄削哮嚣销消宵淆晓小孝校肖啸笑效楔些歇蝎鞋协挟携邪斜胁谐写械卸蟹懈泄泻谢屑薪芯锌欣辛新忻心信衅星腥猩惺兴刑型形邢行醒幸杏性姓兄凶胸匈汹雄熊休修羞朽嗅锈秀袖绣墟戌需虚嘘须徐许蓄酗叙旭序畜恤絮婿绪续轩喧宣悬旋玄选癣眩绚靴薛学穴雪血勋熏循旬询寻驯巡殉汛训讯逊迅压押鸦鸭呀丫芽牙蚜崖衙涯雅哑亚讶焉咽阉烟淹盐严研蜒岩延言颜阎炎沿奄掩眼衍演艳堰燕厌砚雁唁彦焰宴谚验殃央鸯秧杨扬佯疡羊洋阳氧仰痒养样漾邀腰妖瑶摇尧遥窑谣姚咬舀药要耀椰噎耶爷野冶也页掖业叶曳腋夜液一壹医揖铱依伊衣颐夷遗移仪胰疑沂宜姨彝椅蚁倚已乙矣以艺抑易邑屹亿役臆逸肄疫亦裔意毅忆义益溢诣议谊译异翼翌绎茵荫因殷音阴姻吟银淫寅饮尹引隐印英樱婴鹰应缨莹萤营荧蝇迎赢盈影颖硬映哟拥佣臃痈庸雍踊蛹咏泳涌永恿勇用幽优悠忧尤由邮铀犹油游酉有友右佑釉诱又幼迂淤于盂榆虞愚舆余俞逾鱼愉渝渔隅予娱雨与屿禹宇语羽玉域芋郁吁遇喻峪御愈欲狱育誉浴寓裕预豫驭鸳渊冤元垣袁原援辕园员圆猿源缘远苑愿怨院曰约越跃钥岳粤月悦阅耘云郧匀陨允运蕴酝晕韵孕匝砸杂栽哉灾宰载再在咱攒暂赞赃脏葬遭糟凿藻枣早澡蚤躁噪造皂灶燥责择则泽贼怎增憎曾赠扎喳渣札轧铡闸眨栅榨咋乍炸诈摘斋宅窄债寨瞻毡詹粘沾盏斩辗崭展蘸栈占战站湛绽樟章彰漳张掌涨杖丈帐账仗胀瘴障招昭找沼赵照罩兆肇召遮折哲蛰辙者锗蔗这浙珍斟真甄砧臻贞针侦枕疹诊震振镇阵蒸挣睁征狰争怔整拯正政帧症郑证芝枝支吱蜘知肢脂汁之织职直植殖执值侄址指止趾只旨纸志挚掷至致置帜峙制智秩稚质炙痔滞治窒中盅忠钟衷终种肿重仲众舟周州洲诌粥轴肘帚咒皱宙昼骤珠株蛛朱猪诸诛逐竹烛煮拄瞩嘱主著柱助蛀贮铸筑住注祝驻抓爪拽专砖转撰赚篆桩庄装妆撞壮状椎锥追赘坠缀谆准捉拙卓桌琢茁酌啄着灼浊兹咨资姿滋淄孜紫仔籽滓子自渍字鬃棕踪宗综总纵邹走奏揍租足卒族祖诅阻组钻纂嘴醉最罪尊遵昨左佐柞做作坐座'
    DecodingList = ['same', 'lowercase']

    BLANK_SYMBOL = '$'
    DIGITS_ONLY = Digits + BLANK_SYMBOL
    SYMBOLS_ONLY = Symbols + BLANK_SYMBOL
    CHINESECHAR_ONLY = ChineseChar + BLANK_SYMBOL
    LETTERS_DIGITS = Digits + LettersCapitals + LettersLowercase + BLANK_SYMBOL
    LETTERS_DIGITS_LOWERCASE = Digits + LettersLowercase + BLANK_SYMBOL
    LETTERS_ONLY = LettersCapitals + LettersLowercase + BLANK_SYMBOL
    LETTERS_ONLY_LOWERCASE = LettersLowercase + BLANK_SYMBOL
    LETTERS_EXTENDED = LettersCapitals + LettersLowercase + Symbols + BLANK_SYMBOL
    LETTERS_EXTENDED_LOWERCASE = LettersLowercase + Symbols + BLANK_SYMBOL
    LETTERS_DIGITS_EXTENDED = Digits + LettersCapitals + LettersLowercase + Symbols + BLANK_SYMBOL
    LETTERS_DIGITS_EXTENDED_LOWERCASE = Digits + LettersLowercase + Symbols + BLANK_SYMBOL
    CHINESECHAR_LETTERS_DIGITS_EXTENDED = Digits + LettersCapitals + LettersLowercase + Symbols + ChineseChar + BLANK_SYMBOL
    # TODO : Maybe add a unique code (unicode?) to each character and add mask

    LabelMapping = {
        'digits_only': DIGITS_ONLY,
        'symbols_only': SYMBOLS_ONLY,
        'chinesechar_only': CHINESECHAR_ONLY,
        'letters_only': LETTERS_ONLY,
        'letters_digits': LETTERS_DIGITS,
        'letters_extended': LETTERS_EXTENDED,
        'letters_digits_extended': LETTERS_DIGITS_EXTENDED,
        'chinese_char_digits_letters_extend': CHINESECHAR_LETTERS_DIGITS_EXTENDED

    }
    # 所有的字母表
    AlphabetsList = [DIGITS_ONLY, SYMBOLS_ONLY, CHINESECHAR_ONLY, LETTERS_DIGITS, LETTERS_DIGITS_LOWERCASE,
                     LETTERS_ONLY, LETTERS_ONLY_LOWERCASE,
                     LETTERS_EXTENDED, LETTERS_EXTENDED_LOWERCASE, LETTERS_DIGITS_EXTENDED,
                     LETTERS_DIGITS_EXTENDED_LOWERCASE, CHINESECHAR_LETTERS_DIGITS_EXTENDED]
    # 只包含小写字母的的字母表
    LowercaseAlphabetsList = [LETTERS_DIGITS_LOWERCASE, LETTERS_ONLY_LOWERCASE,
                              LETTERS_EXTENDED_LOWERCASE, LETTERS_DIGITS_EXTENDED_LOWERCASE]
    # 包含小写和大写的字母表
    FullAlphabetList = [DIGITS_ONLY, LETTERS_DIGITS, LETTERS_ONLY,
                        LETTERS_EXTENDED, LETTERS_DIGITS_EXTENDED,
                        CHINESECHAR_LETTERS_DIGITS_EXTENDED]

    # This are codes for the case DecodingList = 'lowercase' 字母表中只包含小写字母时，小写字母和大写字母的label一样
    CODES_DIGITS_ONLY = list(range(len(Digits) + 1))
    CODES_LETTERS_DIGITS = list(range(len(Digits))) + \
                           list(range(len(Digits), len(Digits) + len(LettersCapitals))) + \
                           list(range(len(Digits), len(Digits) + len(LettersLowercase) + 1))
    CODES_LETTERS_DIGITS_LOWERCASE = list(range(len(Digits))) + \
                                     list(range(len(Digits), len(Digits) + len(LettersLowercase) + 1))
    CODES_LETTERS_ONLY = list(range(len(LettersCapitals))) + \
                         list(range(len(LettersLowercase) + 1))
    CODES_LETTERS_ONLY_LOWERCASE = list(range(len(LettersLowercase) + 1))
    CODES_LETTERS_EXTENDED = list(range(len(LettersCapitals))) + \
                             list(range(len(LettersLowercase))) + \
                             list(range(len(LettersCapitals), len(LettersCapitals) + len(Symbols) + 1))
    CODES_LETTERS_EXTENDED_LOWERCASE = list(range(len(LettersLowercase))) + \
                                       list(range(len(LettersLowercase), len(LettersLowercase) + len(Symbols) + 1))
    CODES_LETTERS_DIGITS_EXTENDED = list(range(len(Digits))) + \
                                    list(range(len(Digits), len(Digits) + len(LettersCapitals))) + \
                                    list(range(len(Digits), len(Digits) + len(LettersLowercase))) + \
                                    list(range(len(Digits) + len(LettersCapitals),
                                               len(Digits) + len(LettersCapitals) +
                                               len(Symbols) + 1))
    CODES_LETTERS_DIGITS_EXTENDED_LOWERCASE = list(range(len(Digits))) + \
                                              list(range(len(Digits), len(Digits) + len(LettersLowercase))) + \
                                              list(range(len(Digits) + len(LettersLowercase),
                                                         len(Digits) + len(LettersLowercase) +
                                                         len(Symbols) + 1))


class Params:
    def __init__(self, **kwargs):
        self.train_batch_size = kwargs.get('train_batch_size', 100)
        self.eval_batch_size = kwargs.get('eval_batch_size', 200)
        # Initial value of learining rate (exponential learning rate is used)
        self.learning_rate = kwargs.get('learning_rate', 1e-4)
        # Learning rate decay for exponential learning rate
        self.learning_decay_rate = kwargs.get('learning_decay_rate', 0.96)
        # Decay steps for exponential learning rate
        self.learning_decay_steps = kwargs.get('learning_decay_steps', 1000)
        self.optimizer = kwargs.get('optimizer', 'adam')
        self.n_epochs = kwargs.get('n_epochs', 50)
        self.evaluate_every_epoch = kwargs.get('evaluate_every_epoch', 5)
        self.save_interval = kwargs.get('save_interval', 1e3)
        # Shape of the image to be processed. The original with either be resized or pad depending on its original size
        self.input_shape = kwargs.get('input_shape', (32, 100))
        # Either decode with the same alphabet or map capitals and lowercase letters to the same symbol (lowercase)
        self.alphabet_decoding = kwargs.get('alphabet_decoding', 'same')
        self.csv_delimiter = kwargs.get('csv_delimiter', ';')
        self.gpu = kwargs.get('gpu', '')
        # Alphabet to use (from class Alphabet)
        self.alphabet = kwargs.get('alphabet')
        self.csv_files_train = kwargs.get('csv_files_train')
        self.csv_files_eval = kwargs.get('csv_files_eval')
        self.output_model_dir = kwargs.get('output_model_dir')
        self.image_channels = kwargs.get('image_channels')
        self._keep_prob_dropout = kwargs.get('keep_prob')

        assert self.optimizer in ['adam', 'rms', 'ada'], 'Unknown optimizer {}'.format(self.optimizer)

        self._assign_alphabet(alphabet_decoding_list=Alphabet.DecodingList)

    def export_experiment_params(self):
        if not os.path.isdir(self.output_model_dir):
            os.mkdir(self.output_model_dir)
        filename = os.path.join(self.output_model_dir, 'model_params_{}.json'.format(round(time.time())))
        with open(filename, 'w') as f:
            json.dump(vars(self), f)

    def show_experiment_params(self):
        return vars(self)

    def _assign_alphabet(self, alphabet_decoding_list):
        assert (self.alphabet in Alphabet.LabelMapping.keys() or self.alphabet in Alphabet.LabelMapping.values()), \
            'Unknown alphabet {}'.format(self.alphabet)
        assert (self.alphabet_decoding in alphabet_decoding_list) or (self.alphabet in Alphabet.AlphabetsList), \
            'Unknown alphabet decoding {}'.format(self.alphabet_decoding)

        if self.alphabet in Alphabet.LabelMapping.keys():
            self.alphabet = Alphabet.LabelMapping[self.alphabet]

        if self.alphabet_decoding == 'lowercase' or self.alphabet_decoding in Alphabet.LowercaseAlphabetsList:
            if self.alphabet == Alphabet.LETTERS_DIGITS:
                self.alphabet_decoding = Alphabet.LETTERS_DIGITS_LOWERCASE
                self._alphabet_codes = Alphabet.CODES_LETTERS_DIGITS
                self._alphabet_decoding_codes = Alphabet.CODES_LETTERS_DIGITS_LOWERCASE
                self.blank_label_code = self._alphabet_codes[-1]

            elif self.alphabet == Alphabet.LETTERS_ONLY:
                self.alphabet_decoding = Alphabet.LETTERS_ONLY_LOWERCASE
                self._alphabet_codes = Alphabet.CODES_LETTERS_ONLY
                self._alphabet_decoding_codes = Alphabet.CODES_LETTERS_ONLY_LOWERCASE
                self.blank_label_code = self._alphabet_codes[-1]

            elif self.alphabet == Alphabet.LETTERS_EXTENDED:
                self.alphabet_decoding = Alphabet.LETTERS_EXTENDED_LOWERCASE
                self._alphabet_codes = Alphabet.CODES_LETTERS_EXTENDED
                self._alphabet_decoding_codes = Alphabet.CODES_LETTERS_EXTENDED_LOWERCASE
                self.blank_label_code = self._alphabet_codes[-1]

            elif self.alphabet == Alphabet.LETTERS_DIGITS_EXTENDED:
                self.alphabet_decoding = Alphabet.LETTERS_DIGITS_EXTENDED_LOWERCASE
                self._alphabet_codes = Alphabet.CODES_LETTERS_DIGITS_EXTENDED
                self._alphabet_decoding_codes = Alphabet.CODES_LETTERS_DIGITS_EXTENDED_LOWERCASE

        elif self.alphabet_decoding == 'same' or self.alphabet_decoding in Alphabet.FullAlphabetList:
            self.alphabet_decoding = self.alphabet
            self._alphabet_codes = list(range(len(self.alphabet)))
            self.blank_label_code = self._alphabet_codes[-1]
            self._alphabet_decoding_codes = self._alphabet_codes

        self._nclasses = self._alphabet_codes[-1] + 1
        self._blank_label_symbol = Alphabet.BLANK_SYMBOL

    @property
    def keep_prob_dropout(self):
        return self._keep_prob_dropout

    @keep_prob_dropout.setter
    def keep_prob_dropout(self, value):
        assert (0.0 < value <= 1.0), 'Must be 0.0 < value <= 1.0'
        self._keep_prob_dropout = value

    @property
    def n_classes(self):
        return self._nclasses

    @property
    def blank_label_symbol(self):
        return self._blank_label_symbol

    @property
    def alphabet_codes(self):
        return self._alphabet_codes

    @property
    def alphabet_decoding_codes(self):
        return self._alphabet_decoding_codes


def import_params_from_json(model_directory: str = None, json_filename: str = None) -> dict:
    assert not all(p is None for p in [model_directory, json_filename]), 'One argument at least should not be None'

    if model_directory:
        # Import parameters from the json file
        try:
            json_filename = glob(os.path.join(model_directory, 'model_params*.json'))[-1]
        except IndexError:
            print('No json found in dir {}'.format(model_directory))
            raise FileNotFoundError
    else:
        if not os.path.isfile(json_filename):
            print('No json found with filename {}'.format(json_filename))
            raise FileNotFoundError

    with open(json_filename, 'r') as data_json:
        params_json = json.load(data_json)

    # Remove 'private' keys
    keys = list(params_json.keys())
    for key in keys:
        if key[0] == '_':
            params_json.pop(key)

    return params_json
