# This is based off of https://github.com/s0md3v/Zen
	
import re
import sys
import json
import argparse
import threading
from requests import get
from requests.auth import HTTPBasicAuth

i = 'csrs' # your GitHub username here

def findContributorsFromRepo(username, repo):
	response = get('https://api.github.com/repos/%s/%s/contributors?per_page=100' % (username, repo), auth=HTTPBasicAuth(i, '')).text
	contributors = re.findall(r'https://github\.com/(.*?)"', response)
	return contributors

def findReposFromUsername(username):
	response = get('https://api.github.com/users/%s/repos?per_page=100&sort=pushed' % username, auth=HTTPBasicAuth(i, '')).text
	repos = re.findall(r'"full_name":"%s/(.*?)",.*?"fork":(.*?),' % username, response)
	nonForkedRepos = []
	for repo in repos:
		if repo[1] == 'false':
			nonForkedRepos.append(repo[0])
	return nonForkedRepos

def findEmailFromContributor(username, repo, contributor):
	response = get('https://github.com/%s/%s/commits?author=%s' % (username, repo, contributor), auth=HTTPBasicAuth(i, '')).text
	latestCommit = re.search(r'href="/%s/%s/commit/(.*?)"' % (username, repo), response)
	if latestCommit:
		latestCommit = latestCommit.group(1)
	else:
		latestCommit = 'dummy'
	commitDetails = get('https://github.com/%s/%s/commit/%s.patch' % (username, repo, latestCommit), auth=HTTPBasicAuth(i, '')).text
	email = re.search(r'<(.*)>', commitDetails)
	if email:
		email = email.group(1)
		# if breach:
		# 	jsonOutput[contributor] = {}
		# 	jsonOutput[contributor]['email'] = email
		# 	if get('https://haveibeenpwned.com/api/v2/breachedaccount/' + email).status_code == 200:
		# 		email = email + start + 'pwned' + stop
		# 		jsonOutput[contributor]['pwned'] = True
		# 	else:
		# 		jsonOutput[contributor]['pwned'] = False
		# else:
		# 	jsonOutput[contributor] = email
	return email

def findEmailFromUsername(username):
	repos = findReposFromUsername(username)
	for repo in repos:
		email = findEmailFromContributor(username, repo, username)
			# print (username + ' : ' + email)
		return email or ''

def findEmailsFromRepo(username, repo):
	contributors = findContributorsFromRepo(username, repo)
	# print ('%s Total contributors: %s%i%s' % (info, green, len(contributors), end))
	for contributor in contributors:
		email = (findEmailFromContributor(username, repo, contributor))
		if email:
			print (contributor + ' : ' + email)

def findUsersFromOrganization(username):
	response = get('https://api.github.com/orgs/%s/members?per_page=100' % username, auth=HTTPBasicAuth(i, '')).text
	members = re.findall(r'"login":"(.*?)"', response)
	return members


uname = ['torvalds', 'ruanyf', 'yyx990803', 'gaearon', 'JakeWharton', 'tj', 'sindresorhus', 'llSourcell', 'addyosmani', 'michaelliao', 'paulirish', 'bradtraversy', 'ken-reitz', 'getify', 'karpathy', 'buckyroberts', 'daimajia', 'ry', 'mojombo', 'StephenGrider', 'wesbos', 'defunkt', 'mbostock', 'JacksonTian', 'douglascrockford', 'mdo', 'taylorotwell', 'hadley', 'Trinea', 'phodal', 'vczh', 'mattt', 'cloudwu', 'jeresig', 'MorvanZhou', 'geohot', 'stormzhang', 'chrisbanes', 'jlord', 'dhh', 'kelseyhightower', 'clowwindy', 'lifesinger', 'mitsuhiko', 'shiffman', 'kentcdodds', 'antirez', 'mrdoob', 'sdras', 'substack', 'astaxie', 'RubyLouvre', 'johnpapa', 'diego3g', 'justjavac', 'filipedeschamps', 'onevcat', 'kamranahmedse', 'yinwang0', 'tpope', 'breakwa11', 'LeaVerou', 'rasbt', '88250', 'keijiro', 'JeffreyWay', 'programthink', 'jashkenas', 'schacon', 'hongyangAndroid', 'angusshire', 'laruence', 'BYVoid', 'goodfeli', 'bailicangdu', 'jakevdp', 'ibireme', 'fchollet', 'codingforentrepreneurs', 'gvanrossum', 'isaacs', 'iamshaunjp', 'CyC2018', 'Ovilia', 'fabpot', 'jessfraz', 'iconfont-cn', 'feross', 'josevalim', 'muan', 'unknwon', '3b1b', 'xiaolai', 'hakimel', 'gustavoguanabara', 'donnemartin', 'agentzh', 'fouber', 'romannurik', 'sofish', 'developit', 'unclebob', 'chenshuo', 'ChenYilong', 'romainguy', 'fat', 'amueller', 'tqchen', 'pjhyett', 'dyc87112', 'CoderMJLee', 'rauchg', 'miguelgrinberg', 'wintercn', 'spf13', 'rakyll', 'necolas', 'fengdu78', 'developit', 'unclebob', 'chenshuo', 'ChenYilong', 'romainguy', 'fat', 'amueller', 'liaohuqiu', 'tqchen', 'pjhyett', 'Code-Bullet', 'dyc87112', 'lepture', 'toddmotto', 'miloyip', 'dennybritz', 'taniarascia', 'nzakas', 'dmalan', 'offensive-security', 'acdlite', 'bradfitz', 'ustbhuangyi', 'matz', 'tenderlove', 'igrigorik', 'colah', 'chriscoyier', 'haoel', 'ahejlsberg', 'mitchellh', 'ityouknow', 'vbuterin', 'KaimingHe', 'PanJiaChen', 'koush', 'jcjohnson', 'egoist', 'wasabeef', '996icu', 'fengmk2', 'sophiebits', 'wizardforcel', 'DIYgod', 'cusspvz', 'DevonCrawford', 'zenorocha', 'mnielsen', 'ryanb', 'in28minutes', 'pjreddie', 'singwhatiwanna', 'shanselman', 'rengwuxian', 'drakeet', 'carpedm20', 'YunaiV', 'ageron', 'mgechev', 'jakearchibald', 'i5ting', 'rovo89', 'tangqiaoboy', 'joshlong', 'jamiebuilds', 'yihui', 'Sentdex', 'ryanflorence', 'draveness', 'tekkub', 'samyk', 'cyanharlow', 'xufei', 'audreyt', 'mattn', 'CoreyMSchafer', 'zcbenz', 'developedbyed', 'daneden', 'benawad', 'commonsguy', 'mqyqingfeng', 'maxogden', 'jtleek', 'iampawan', 'rdpeng', 'GoesToEleven', 'mercyblitz', 'dalinhuang99', 'Rich-Harris', 'chiphuyen', 'robpike', 'AllenDowney', 'sokra', 'dsacademybr', 'mosh-hamedani', 'remy', 'overtrue', 'Jinjiang', 'LukeSmithxyz', 'brianyu28', 'jvns', 'notwaldorf', 'mxcl', 'justmarkham', 'geerlingguy', 'crnacura', 'davidfowl', 'android10', 'mli', 'liuyubobobo', 'typicode', 'holman', 'MisterBooo', 'easychen', 'Yangqing', 'ericelliott', 'bvaughn', 'KalleHallden', 'rbgirshick', 'BilgisayarKavramlari', 'sebastianbergmann', 'lattner', 'mpj', 'Germey', 'alex', 'eugenp', 'amitshekhariitbhu', 'mstraughan86', 'desandro', 'nicklockwood', 'hackedteam', 'fatih', 'swankjesse', 'norvig', 'JohnSundell', 'DeborahK', 'petehunt', 'greenrobot', 'steveklabnik', 'chokcoco', 'cassidoo', 'CarGuo', 'btholt', 'nfultz', 'TheLarkInn', 'researchersource', 'MichalPaszkiewicz', 'staltz', 'sebmarkbage', 'jhaddix', 'mxstbr', 'rwieruch', 'qiwsir', 'rhiever', 'trekhleb', 'jskeet', 'oldratlee', 'BaseMax', 'mafintosh', 'GrahamCampbell', 'nswbmw', 'adamwathan', 'rsc', 'yangshun', 'hehonghui', 'julycoding', 'alsotang', 'afc163', 'cheshire137', 'mjackson', 'jonasschmedtmann', 'rstacruz', 'jamesmontemagno', 'jxnblk', 'ebidel', 'evilsocket', 'evancz', 'prakhar1989', 'alanhamlett', 'crossoverJie', 'junegunn', 'JeffreyZhao', 'munificent', 'antoniolg', 'Snailclimb', 'richhickey', 'brendangregg', 'creationix', 'SebLague', 'jgilfelt', 'junyanz', 'ai', 'aymericdamien', 'techwithtim', 'afollestad', 'geeeeeeeeek', 'jaredpalmer', 'jdalton', 'kevinsawicki', 'tylermcginnis', 'geektime-geekbang', 'chenglou', 'davecheney', 'csswizardry', 'lydiahallie', 'wepe', 'biezhi', 'historicalsource', 'NARKOZ', 'huacnlee', 'evilcos', 'kenwheeler', 'Pierian-Data', 'nikic', 'joyeecheung', 'yanhaijing', 'vim-scripts', 'bevacqua', 'soffes', 'hussien89aa', 'zhangxinxu', 'numbbbbb', 'krishnaik06', 'jgthms', 'sebastianruder', 'BurntSushi', 'domenic', 'kesenhoo', 'mikepenz', 'hzoo', 'huangz1990', 'planetoftheweb', 'mikeal', 'cyrilmottier', 'BrendanEich', 'aneagoie', 'guolindev', 'tiangolo', 'nat', 'ForrestKnight', 'springframeworkguru', 'satyanadella', 'RamotionDev', 'marijnh', 'mhevery', 'leebyron', 'jordwalke', 'TheCherno', 'barryvdh', 'steipete', 'xuxueli', 'sebmck', 'willianjusten', 'gopinav', 'asLody', 'FiloSottile', 'noopkat', 'mschwarzmueller', 'madeye', 'dead-horse', 'pengzhile', 'KrauseFx', 'waylau', 'fogleman', 'jaywcjlove', 'ashleygwilliams', 'moxie0', 'mattdesl', 'SimonVT', 'JeffLi1993', 'lexfridman', 'yuanming-hu', 'jennybc', 'mcxiaoke', 'aphyr', 'Colt', 'mcollina', 'Shougo', 'teddysun', 'WebDevSimplified', 'happypeter', 'lzyzsd', 'ahmetb', 'rsms', 'barretlee', 'orta', 'KevinHock', 'QuincyLarson', 'campoy', 'felipefialho', 'akitaonrails', 'Alvin9999', 'macrozheng', 'lihaoyi', 'sahat', 'wx-chevalier', 'bojone', 'listen1', 'philsturgeon', 'rfthusn', 'blueimp', 'danielmiessler', 'coryhouse', 'dodola', 'florent37', 'SaraSoueidan', 's0md3v', 'evanw', 'bbatsov', 'DanWahlin', '521xueweihan', 'Blankj', 'byt3bl33d3r', 'ming1016', 'vinta', 'ljharb', 'peng-zhihui', 'vakila', 'hmason', 'mitchtabian', 'yangyangwithgnu', 'mikeash', 'oschina', 'philipwalton', 'shengxinjing', 'Grafikart', 'tomnomnom', 'timbl', 'CamDavidsonPilon', 'hankcs', 'bingoogolapple', 'robbyrussell', 'loopj', 'atian25', 'TooTallNate', 'maccman', 'zhangkaitao', 'felixrieseberg', 'mourner', 'phith0n', 'CleverProgrammer', 'jawil', 'LeonidasEsteban', 'JessYanCoding', 'jfeinstein10', 'swannodette', 'mission-peace', 'kevinzhow', 'sstephenson', 'brentvatne', 'OneLoneCoder', 'karan', 'Huxpro', 'Seldaek', 'darkwing', 'casatwy', 'JedWatson', 'Ocramius', 'yeasy', 'andrewjmead', 'appleboy', 'code4craft', 'cssmagic', 'markzhai', 'adeshpande3', 'zedshaw', 'lexrus', 'migueldeicaza', 'ashfurrow', 'ken', 'cowboy', 'iamtrask', 'ekmett', 'chrisvfritz', 'jadijadi', 'bcaffo', 'pedrovgs', 'xoreaxeaxeax', 'hardmaru', 'ncase', 'halfrost', 'rlerdorf', 'gsdios', 'koushikkothagal', 'PresidentObamaBot', 'clementmihailescu', 'btford', 'angelabauer', 'bradfrost', 'windiest', 'matyhtf', 'lemire', 'garybernhardt', 'arun-gupta', 'kytrinyx', 'nathanmarz', 'gaoxiang12', 'wangshub', 'BenTristem', 'twostraws', 'roboticcam', 'hax', 'slidenerd', 'dominictarr', 'sunnyxx', 'pwn20wndstuff', 'hunkim', 'eriklindernoren', 'florinpop17', 'dongweiming', 'jeasonlzy', 'progrium', 'eliben', 'octocat', 'shu223', 'sharkdp', 'STRML', 'leixiaohua1020', 'erica', 'dabeaz', 'mholt', 'chloerei', 'yiminghe', 'krzysztofzablocki', 'simplesteph', 'rwaldron', 'cornflourblue', 'lucasmontano', 'pydanny', 'answershuto', 'yegor256', 'skywind3000', 'camsong', 'QianMo', 'Akkariiin', 'maykbrito', 'hzlzh', 'codefollower', 'botelho', 'minimaxir', 'inconvergent', 'hustcc', 'zpao', 'codediodeio', 'insidegui', 'ogrisel', 'alexcrichton', 'ariya', 'topjohnwu', 'keyboardsurfer', 'vhf', 'qiangxue', 'AdiChat', 'donnfelker', 'dgrtwo', 'jonhoo', 'wenshao', 'rogerwang', 'jph00', 'soulmachine', 'florina-muntenescu', 'una', 'susanli2016', 'ring04h', 'rs', 'gregkh', 'nickbutcher', 'RehabMan', 'mislav', 'kangax', 'kripken', 'jeffheaton', 'KieSun', 'GcsSloop', 'LingDong-', 'KyleAMathews', 'IgorMinar', 'kylemcdonald', 'cloudhead', 'tiann', 'zloirock', 'vjeux', 'haacked', 'f', 'akira-cn', 'tholman', 'unicodeveloper', 'jbogard', 'Jack-Cherish', 'pissang', 'nostra13', 'ageitgey', 'ccoenraets', 'lanxuezaipiao', 'mhartl', 'felixge', 'nelsonic', 'x0rz', 'Akryum', 'KittenYang', 'alexjlockwood', 'WillKoehrsen', 'hak5darren', 'ManuelPeinado', 'kymjs', 'pifafu', 'sentsin', 'muaz-khan', 'lazyprogrammer', 'litesuits', 'smallnest', 'bytemaster', 'opengineer', 'dsyer', 'yanzhenjie', 'luin', 'diracdeltas', 'yigit', 'jaredhanson', 'qyuhen', 'lenve', 'ghost', 'liuhuanyong', 'jmportilla', 'saulmm', 'emmabostian', 'jspahrsummers', 'fxsjy', 'deepfakes', 'emilsjolander', 'hmaverickadams', 'indutny', 'anvaka', 'zce', 'SaraVieira', 'LiveOverflow', 'summerblue', 'cyanzhong', 'leah', 'FaztTech', 'johnmyleswhite', 'jendewalt', 'freekmurze', 'xcatliu', 'avelino', 'aui', 'hansonwang99', 'iluwatar', 'wangzheng0822', 'dougwilson', 'lucasr', 'xhzengAIB', 'sandhikagalih', 'laanwj', 'XadillaX', 'joelgrus', 'amusi', 'binux', 'datasciencescoop', 'cpojer', 'freddier', 'dlew', 'bang590', 'themsaid', 'pkrumins', 'ankane', 'alexellis', 'anishathalye', 'spacehuhn', 'Avik-Jain', 'vczero', 'alvarotrigo', 'jlongster', 'yygmind', 'guo-yu', 'tmcw', 'deeplearningturkiye', 'madrobby', 'odrotbohm', 'jinzhu', 'jrosebr1', 'azer', 'tannerlinsley', 'sephiroth74', 'madskristensen', 'ppwwyyxx', 'SensorsIot', 'chai2010', 'airen', 'nvie', 'daylerees', 'gabrielemariotti', 'jpetazzo', 'wcandillon', 'xinyu198736', 'ahmadawais', 'mikepound', 'abhishekkrthakur', 'jacobian', 'rootsongjc', 'baoyongzhang', 'bdamcoin', 'gitster', 'JakeLin', 'tencent-wechat', 'ramalho', 'amatsuda', 'graydon', 'yunjey', 'odersky', 'mrmrs', 'benjchristensen', 'technoweenie', 'tonsky', 'nahamsec', 'brunosimon', 'brightmart', 'josephmisiti', 'azl397985856', 'iliakan', 'fzaninotto', 'cyanogen', 'rodrigobranas', 'jasondavies', 'latentflip', 'HugoGiraudel', 'jedisct1', 'HackerPoet', 'jserv', 'floodsung', 'naveenanimation20', 'EpicTeamAdmin', 'codeguy', 'flavienlaurent', 'Vermisse', 'shiftkey', 'DrBoolean', 'robbiehanson', '0xAX', 'vitorfs', 'johnlui', 'SamyPesse', 'liuchuo', 'photonstorm', 'IonicaBizau', 'rnystrom', '0xd4d', 'rfyiamcool', 'ornicar', 'brunocasanova', 'kitze', 'chyyuu', 'juliemr', 'paullewis', 'asweigart', 'mixu', 'harthur', 'CSSEGISandData', 'hanxiao', 'wyouflf', 'mustafamuratcoskun', 'siddontang', 'FrankFang', 'bagder', 'aspittel', 'suissa', 'dabit3', 'ddevault', 'xtaci', 'judasn', 'thedaviddias', 'shykes', 'jindongwang', 'purcell', 'jiyinyiyong', 'andrew', 'nikitavoloboev', 'ireade', 'juliangarnier', 'jonschlinkert', 'be5invis', 'soulwire', 'yexiaochai', 'mweststrate', 'openbilibili', 'gorhill', 'coolsnowwolf', 'kamilmysliwiec', 'sferik', 'championswimmer', 'DmitryBaranovskiy', 'EduardoPires', 'Justineo', 'AlexeyAB', 'travisneilson', 'acenelio', 'ines', 'mubix', 'android-cjj', 'ibdknox', 'dbader', 'surma', 'Klerith', 'geekcomputers', 'twiecki', 'ZhangMYihua', 'abel533', 'Skykai521', 'josh', 'PascalPrecht', 'kdn251', 'contra', 'ardalis', 'Terry-Mao', 'samdark', 'crazycodeboy', 'robdodson', 'dylanaraps', 'ice1000', 'mgp25', 'miyagawa', 'carlosazaustre', 'gabrielecirulli', 'fdaciuk', 'agragregra', 'orangetw', 'berwin', 'lh3', 'egonSchiele', 'SudalaiRajkumar', 'kujian', 'livid', 'weierophinney', 'arunoda', 'hasherezade', 'hollance', 'stoked-zz', 'AdamBien', 'phuslu', 'yulingtianxia', 'paulmillr', 'jessesquires', 'mperham', 'yoshuawuyts', 'scottjehl', 'ginatrapani', 'DanMcInerney', 'jeromeetienne', 'devunwired', 'zkat', 'ErickWendel', 'orderedlist', 'rtomayko', 'pluskid', 'rafaelfranca', 'yangfuhai', 'tomchristie', 'lijiejie', 'GaelVaroquaux', 'rxin', 'unconed', 'tmm1', 'zzz40500', 'fool2fish', 'zhengmin1989', 'joearms', 'yuanyan', 'caolan', 'markerikson', 'SpikeKing', 'stefanprodan', 'JsAaron', 'erikras', 'basarat', 'apaszke', 'hemanth', 'PhilJay', 'mackenziechild', 'peterbourgon', 'dgryski', 'Kyubyong', 'rhettinger', 'mariobehling', 'GeekTrainer', 'TKkk-iOSer', 'nolimits4web', 'Marak', 'rvagg', 'hasinhayder', 'soimort', 'BretFisher', 'wenzhixin', 'ircmaxell', 'coderwhy', 'rmurphey', 'Jason-Cooke', 'benjamn', 'ATBrackeys', 'CompuIves', 'posva', 'chiuki', 'yorkie', 'mmin18', 'surmon-china', 'kbastani', 'cer', 'samccone', 'mikolalysenko', 'colodenn', 'stubbornella', 'ianstormtaylor', 'caged', 'bisqwit', 'winterbe', 'devxoul', 'williamfiset', 'candycat1992', 'SelmanKahya', 'Errichto', 'w3cj', 'jeffrafter', 'xudafeng', 'keon', 'jas502n', 'davideast', 'walkor', 'digoal', 'felangel', 'j2kun', 'Jabrils', 'sdiehl', 'sipa', 'indexzero', 'rochacbruno', 'bnoordhuis', 'SlexAxton', 'acgotaku', 'kartik-v', 'dcramer', 'medcl', 'xpqiu', 'codebytere', 'codepo8', 'Vamei', 'yuuwill', 'jezdez', 'zilongshanren', 'azat-co', 'poteto', 'trueadm', 'ded', 'dntzhang', 'rednaxelafx', 'fly51fly', 'DamianEdwards', 'chrismccord', 'yujiangshui', 'charliegerard', 'chenjiandongx', 'sonyxperiadev', 'threepointone', 'spmallick', 'stolinski', 'g0tmi1k', 'algebric', 'chjj', 'davatron5000', 'sjl', 'FeeiCN', 'livoras', 'andrewrk', 'hiteshchoudhary', 'schneems', 'kishikawakatsumi', 'kelthuzadx', 'nayuki', 'gentilkiwi', 'HcySunYang', 'terrytangyuan', 'happyfish100', 'bamos']
emails_dict = dict.fromkeys(uname,'')
# print(emails_dict)
for name in uname:
	email = findEmailFromUsername(name)
	emails_dict[name] = email
	print(name, email)
print(emails_dict)
