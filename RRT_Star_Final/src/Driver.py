from Map import Map
from Obstacle import Obstacle
from Node import Node
from RRTStar import RRTStar
from matplotlib.path import Path
import matplotlib.pyplot as plt
import random
import json

#map boundaries
XMIN, XMAX, YMIN, YMAX = -20, 20, -20, 20


# returns a map of id #
# available map ids:
# 0: zig-zag obstacles
# 1: maze obstacles
# 2: many circles
def make_map(id):
    obstacles = []

    if id == 1:
        # make zig zag obstacle course
        for i in range(-20,20,4):
            left,right = i,i+2
            if i % 8 == 0:
                top,bottom = YMAX, (1/5)* YMIN
            else:
                top,bottom = (1/5)* YMAX, YMIN
            obstacle_coords = [(left,top),(right,top),(right,bottom),(left,bottom),(left,top)]
            obstacles.append(Obstacle(obstacle_coords))
        
        course_map = Map([],obstacles,[XMIN,XMAX,YMIN,YMAX])
        course_map.set_start(Node(-18, 10))
        course_map.set_goal(Node(18, -10))
        return course_map

    elif id == 2:
        # make maze obstacle course
        obstacle_lists = []
        obstacle_lists.append([(0,0),(11,0),(11,3),(10,3),(10,1),(5,1),(5,3),(4,3),(4,1),(1,1),(1,4),(2,4),(2,2),(3,2),(3,4),(6,4),(6,2),(7,2),(7,4),
               (8,4),(8,2),(9,2),(9,5),(0,5),(0,0)])
        obstacle_lists.append([(12,0),(12,1),(20,1),(20,4),(19,4),(19,2),(18,2),(18,4),(17,4),(17,2),(14,2),(14,4),(13,4),(13,2),(12,2),(12,4),(10,4),(10,7),
         (11,7),(11,5),(12,5),(12,7),(13,7),(13,5),(14,5),(14,8),(12,8),(12,11),(13,11),(13,9),(14,9),(14,11),(15,11),(15,3),(16,3),
         (16,7),(17,7),(17,5),(18,5),(18,7),(19,7),(19,5),(21,5),(21,0),(12,0)])
        obstacle_lists.append([(8,5),(8,8),(7,8),(7,6),(6,6),(6,9),(10,9),(10,14),(8,14),(8,15),(13,15),(13,14),(11,14),(11,8),(9,8),(9,5),(8,5)])
        obstacle_lists.append([(20,5),(20,8),(18,8),(18,9),(20,9),(20,12),(19,12),(19,10),(18,10),(18,13),(20,13),(20,14),(18,14),(18,15),(20,15),(20,20),
         (19,20),(19,16),(18,16),(18,20),(17,20),(17,18),(15,18),(15,15),(16,15),(16,17),(17,17),(17,8),(16,8),(16,14),(15,14),(15,12),
         (12,12),(12,13),(14,13),(14,18),(13,18),(13,16),(12,16),(12,19),(16,19),(16,20),(11,20),(11,16),(10,16),(10,18),(9,18),(9,16),
         (8,16),(8,19),(10,19),(10,20),(7,20),(7,21),(21,21),(21,5),(20,5)])
        obstacle_lists.append([(0,12),(0,21),(7,21),(7,18),(6,18),(6,20),(1,20),(1,15),(2,15),(2,19),(3,19),(3,17),(4,17),(4,19),(5,19),(5,17),(7,17),(7,16),
         (5,16),(5,15),(7,15),(7,14),(5,14),(5,13),(9,13),(9,10),(8,10),(8,12),(5,12),(5,11),(7,11),(7,10),(4,10),(4,16),(3,16),
         (3,14),(1,14),(1,13),(3,13),(3,9),(5,9),(5,8),(2,8),(2,12),(0,12)])
        obstacle_lists.append([(4,5),(4,6),(2,6),(2,7),(5,7),(5,5),(4,5)])
        obstacle_lists.append([(0,5),(0,11),(1,11),(1,5),(0,5)])

        for coord_list in obstacle_lists:
            result_list = map(lambda point: (point[0]*2,point[1]*2), coord_list)
            obstacles.append(Obstacle(list(result_list)))
        
        course_map = Map([],obstacles,[0,42,0,42])
        course_map.set_start(Node(23, 1))
        course_map.set_goal(Node(1, 23))

        return course_map

    elif id == 3:
        # make forest map
        # obstacle_coords = []

        # while len(obstacle_coords) < 200:
        #     x,y,r = random.uniform(-20,20), random.uniform(-20,20), random.uniform(0.1,0.5)
        #     obs = Path.circle((x,y),r)
        #     flag = True
        #     for obstacle in obstacles:
        #         if obs.intersects_path(obstacle,filled=True):
        #             flag = False
        #     if flag:
        #         obstacles.append(obs)
        #         obstacle_coords.append([x,y,r])

        # obstacles = [Obstacle((x,y),r) for x,y,r in obstacle_coords]

        # for str in obstacle_coords:
        #     print("obstacles.append(Obstacle((%s,%s),%s))"%(str[0],str[1],str[2]))

        obstacles.append(Obstacle((-19.409234024200963,9.75586166237182),0.221816673267587))
        obstacles.append(Obstacle((13.082028949928088,17.518451272835144),0.25989024437415975))
        obstacles.append(Obstacle((1.4782990878278142,3.7835885886383736),0.19173622143794056))
        obstacles.append(Obstacle((-1.9499314646883583,17.652126076162617),0.4027628649976467))
        obstacles.append(Obstacle((19.906349376041163,-2.422186473593655),0.17063256557008138))
        obstacles.append(Obstacle((4.555710905917259,0.22275892265005837),0.1187822827566817))
        obstacles.append(Obstacle((0.8131772369015025,16.162124652487854),0.21836200339451675))
        obstacles.append(Obstacle((-18.694384710213875,-13.991962830544512),0.3209047891243948))
        obstacles.append(Obstacle((1.4104435033987386,-2.21402476403469),0.3659664792531352))
        obstacles.append(Obstacle((-19.744524817589337,12.60846005602626),0.30960766856076727))
        obstacles.append(Obstacle((-16.549883583810416,-0.14481092149350872),0.36930661365391393))
        obstacles.append(Obstacle((-8.493862691693192,5.240753664164288),0.4385422247150891))
        obstacles.append(Obstacle((2.744074982428085,4.440616235435378),0.2879092598824807))
        obstacles.append(Obstacle((16.93698983946466,-9.251877256947335),0.22310735980868204))
        obstacles.append(Obstacle((-11.708081931416107,2.8280788636107914),0.4158549496403613))
        obstacles.append(Obstacle((-16.187130306876316,-11.614870463045595),0.3055426875152938))
        obstacles.append(Obstacle((12.078983837622069,-19.456786176173427),0.47419863547265473))
        obstacles.append(Obstacle((-1.312703749597965,-4.529569989347767),0.24969794797013722))
        obstacles.append(Obstacle((-4.504529442405145,-16.85451671437694),0.2942485668387318))
        obstacles.append(Obstacle((14.877139161161466,-11.663160926117712),0.4660379330815553))
        obstacles.append(Obstacle((-17.72383064670997,15.196920108015526),0.21272116214238426))
        obstacles.append(Obstacle((1.3973991730911592,-11.985534727047252),0.23311170565617534))
        obstacles.append(Obstacle((-12.918842977634313,-4.656081165062144),0.26580509258037177))
        obstacles.append(Obstacle((7.77899932788937,-9.35877295969978),0.44528854631280446))
        obstacles.append(Obstacle((19.346121173731788,-18.469037755621684),0.13975573009621534))
        obstacles.append(Obstacle((-5.965152743522285,1.6299001755392126),0.33746126674063054))
        obstacles.append(Obstacle((-19.90514243217698,-9.183640317983714),0.11847088772599053))
        obstacles.append(Obstacle((11.259486438642202,8.867645334605179),0.187620443684382))
        obstacles.append(Obstacle((10.838706391464136,-18.535594543984036),0.12252848979676748))
        obstacles.append(Obstacle((-7.064624388194991,-13.963420715167647),0.43863055817634855))
        obstacles.append(Obstacle((10.99722729414719,-5.120494227760396),0.3332239594391666))
        obstacles.append(Obstacle((18.709355692724877,0.5690615138924642),0.187204017044044))
        obstacles.append(Obstacle((8.710375001564692,15.50050265058993),0.12140431717121208))
        obstacles.append(Obstacle((-15.298551678043717,-14.399600811171528),0.38603103393405735))
        obstacles.append(Obstacle((12.127161642559741,14.78973498997074),0.279129927411191))
        obstacles.append(Obstacle((-10.066392603689781,-4.339261929921218),0.30049945237426107))
        obstacles.append(Obstacle((11.541157268267416,-3.874530871355148),0.12114426394274568))
        obstacles.append(Obstacle((12.355424440705796,-3.4976256153619225),0.4345153984304674))
        obstacles.append(Obstacle((2.877516223137423,10.98933946952815),0.15112668378422833))
        obstacles.append(Obstacle((19.697396383817804,-3.4267515036851215),0.28101161492389326))
        obstacles.append(Obstacle((1.5191824444341826,-0.030563855013369334),0.48522960821694694))
        obstacles.append(Obstacle((-19.941867738355334,-2.901973369128598),0.34550488455619366))
        obstacles.append(Obstacle((-12.907888941578069,6.751542660333186),0.3865439896421089))
        obstacles.append(Obstacle((-9.311768283159637,17.378999749397302),0.4023049375898401))
        obstacles.append(Obstacle((7.332389609295113,-14.506807915890665),0.29477750609320924))
        obstacles.append(Obstacle((-15.756475396920466,-12.870274399620598),0.2427636816917311))
        obstacles.append(Obstacle((-5.023465194734818,9.017814346066594),0.4341750634339333))
        obstacles.append(Obstacle((15.30490210934542,5.259234011340666),0.11608220478479213))
        obstacles.append(Obstacle((-11.698869906694881,-19.264538399501255),0.4978449823225374))
        obstacles.append(Obstacle((-17.638015630594843,6.271782085721448),0.18311853775696862))
        obstacles.append(Obstacle((18.066859058935343,-14.773528245082748),0.46469476012463395))
        obstacles.append(Obstacle((10.793667877497231,3.063753835346663),0.41466170351495113))
        obstacles.append(Obstacle((-15.209834682357052,-0.9802384364228303),0.18921701375999278))
        obstacles.append(Obstacle((10.98057401093584,9.81381492397649),0.17579908503996725))
        obstacles.append(Obstacle((18.99154671019864,-19.422143584022123),0.48146834189167564))
        obstacles.append(Obstacle((7.65353404178715,8.59620424981507),0.2340139252762753))
        obstacles.append(Obstacle((10.642829987382491,-7.223908353262418),0.10793325993381951))
        obstacles.append(Obstacle((-14.68180373634732,-14.065347447642345),0.169643711925547))
        obstacles.append(Obstacle((6.809580803011794,2.9038806158538364),0.46458080529236223))
        obstacles.append(Obstacle((-5.038950971987205,7.21714759563833),0.1701640352716422))
        obstacles.append(Obstacle((13.955497519522716,-12.360129146713161),0.25545396178218915))
        obstacles.append(Obstacle((4.766511001995063,14.683782115998483),0.3056369590425257))
        obstacles.append(Obstacle((-1.5098061238285787,-14.742115420431897),0.10108351103515872))
        obstacles.append(Obstacle((2.2887909014611054,18.64623289070684),0.4416070266639638))
        obstacles.append(Obstacle((-14.810465440225142,14.382718177398303),0.34471004585969683))
        obstacles.append(Obstacle((8.341217593977532,17.150845507054868),0.15940630340821604))
        obstacles.append(Obstacle((4.898736873393563,15.535494735395133),0.26732805313993824))
        obstacles.append(Obstacle((-12.33937790590755,-13.55834187278619),0.2599017804345931))
        obstacles.append(Obstacle((4.856346069666767,4.458832854157361),0.44514011518085106))
        obstacles.append(Obstacle((-2.0032739594404347,19.70359928812254),0.3087329703854351))
        obstacles.append(Obstacle((-5.097382403457278,1.0180570990674909),0.20806340462242454))
        obstacles.append(Obstacle((11.512465180295681,0.5504810494141452),0.2813497860097116))
        obstacles.append(Obstacle((15.338710397709406,-17.71706125033665),0.49721516361984175))
        obstacles.append(Obstacle((4.374084238393429,-3.154100122030549),0.21518922927766795))
        obstacles.append(Obstacle((8.958456457079365,9.630779632412718),0.3840832058501047))
        obstacles.append(Obstacle((-1.49008957657637,8.770962088177441),0.26957700925138683))
        obstacles.append(Obstacle((-12.009563133258233,-17.243201367752732),0.35413003878868865))
        obstacles.append(Obstacle((0.37963791007732084,-8.38462395644408),0.36251612552473655))
        obstacles.append(Obstacle((17.18970673316658,-5.988682990625849),0.2726565719750327))
        obstacles.append(Obstacle((-2.004672640253105,-1.4302393727370273),0.28178726041724655))
        obstacles.append(Obstacle((-6.036145810561919,-17.585095174121086),0.13343200475557296))
        obstacles.append(Obstacle((-3.960859773643545,18.324664714427605),0.18818877921245303))
        obstacles.append(Obstacle((5.748291858636875,11.497710247676384),0.14859201144303966))
        obstacles.append(Obstacle((-11.868138666880954,-11.880565977980622),0.47407440676192814))
        obstacles.append(Obstacle((12.870690274626519,-7.198240485568235),0.3065198788388229))
        obstacles.append(Obstacle((-7.951857846679506,-11.591565445334687),0.10151625750061229))
        obstacles.append(Obstacle((-15.104523683924867,-9.935018703916253),0.16966394914951277))
        obstacles.append(Obstacle((6.947124626397798,10.320565489749775),0.31331827207297014))
        obstacles.append(Obstacle((-19.63314968085664,0.45645740786924094),0.4844602167852885))
        obstacles.append(Obstacle((-6.415705349209201,-9.404301952811892),0.1666980198808357))
        obstacles.append(Obstacle((19.477197241210177,-13.550903379701689),0.2199613860692006))
        obstacles.append(Obstacle((17.692366554728117,11.599897405983835),0.22807602311050892))
        obstacles.append(Obstacle((5.540876940919084,5.573635201433621),0.36373577433718074))
        obstacles.append(Obstacle((7.393332817575175,16.062030665284105),0.39617963066074935))
        obstacles.append(Obstacle((6.566723305284107,5.697385532177236),0.47461306682489346))
        obstacles.append(Obstacle((15.5510171739327,-9.911504799363753),0.28290855493249734))
        obstacles.append(Obstacle((11.859110744260377,8.546216922313391),0.37354925560328445))
        obstacles.append(Obstacle((-17.18001596999158,-4.516085107974996),0.1083765762179707))
        obstacles.append(Obstacle((19.401420075390725,-18.21847634401529),0.11694268371558816))
        obstacles.append(Obstacle((12.556368083378786,-5.43974535549439),0.4247361214132658))
        obstacles.append(Obstacle((12.541243586733486,6.157068569843773),0.10476312219958582))
        obstacles.append(Obstacle((-2.0168618344820324,5.976372434115053),0.11221144402096567))
        obstacles.append(Obstacle((18.034450578375335,3.8859191153284875),0.3760049868396035))
        obstacles.append(Obstacle((5.797413950482575,-0.21655081307526558),0.43183039345335317))
        obstacles.append(Obstacle((-12.156222715788253,11.743780430134308),0.12280039851098451))
        obstacles.append(Obstacle((-5.977346643981818,11.709940776016392),0.25519724567786617))
        obstacles.append(Obstacle((2.782389333224536,-11.79112778790406),0.4714083207487816))
        obstacles.append(Obstacle((-17.074646744336327,15.180714281821693),0.14626467380972127))
        obstacles.append(Obstacle((-4.135545100952566,-6.271460593696588),0.4387382727230129))
        obstacles.append(Obstacle((14.72020572771536,-14.402478769763887),0.1744744224949465))
        obstacles.append(Obstacle((2.3224588639116135,1.2688658239713675),0.3869267091149181))
        obstacles.append(Obstacle((11.778288636126327,-10.905731143452947),0.35288048896545343))
        obstacles.append(Obstacle((-10.922716426681474,-4.871393309844025),0.3298808904945374))
        obstacles.append(Obstacle((10.609881815531459,10.076675736640738),0.28166227832688895))
        obstacles.append(Obstacle((8.004843614614153,-13.634338586009491),0.23014193529207347))
        obstacles.append(Obstacle((15.869479949038286,5.953857180540659),0.41249322231884844))
        obstacles.append(Obstacle((10.45024086466746,5.496496362888877),0.30823876685160895))
        obstacles.append(Obstacle((-10.641639587755694,1.6645928132685341),0.4451468009977564))
        obstacles.append(Obstacle((-0.4970850443652779,-5.477853722231405),0.47965054271774066))
        obstacles.append(Obstacle((-2.2271240230180993,-4.7352355194720595),0.36888662256901694))
        obstacles.append(Obstacle((-14.60808012176011,7.873441230186138),0.18490417857834895))
        obstacles.append(Obstacle((-13.629050790422292,-8.705408698988384),0.1304077067131722))
        obstacles.append(Obstacle((5.880500365320408,19.85423744748016),0.10921804894324905))
        obstacles.append(Obstacle((-17.936532867588202,3.2329019184354664),0.32696948125538916))
        obstacles.append(Obstacle((3.723714350648102,0.25311334133220953),0.3637692931797657))
        obstacles.append(Obstacle((13.858999324774729,6.286392328093552),0.42012182134788145))
        obstacles.append(Obstacle((-10.808105877155501,-1.8647508610854686),0.38087768292362756))
        obstacles.append(Obstacle((-7.936684304766196,-19.379683897668084),0.47703754229174444))
        obstacles.append(Obstacle((-2.0795719041498906,-6.832128682906351),0.41785377592239414))
        obstacles.append(Obstacle((-14.628665689532339,17.875934578782562),0.21238539715368027))
        obstacles.append(Obstacle((-11.379822505856998,5.243008222924843),0.39444492875931036))
        obstacles.append(Obstacle((3.589309553367258,-8.673131628228896),0.34061627715782106))
        obstacles.append(Obstacle((14.162706646605095,-8.731990541553735),0.31944212494449636))
        obstacles.append(Obstacle((19.438236825072806,-6.6429347871026),0.276591376378871))
        obstacles.append(Obstacle((18.31872255347337,-19.97591224240349),0.15489804665160678))
        obstacles.append(Obstacle((-6.139203635704607,6.425132335552902),0.19519031302599907))
        obstacles.append(Obstacle((2.9101091672061052,0.9358706793495841),0.19197576380287718))
        obstacles.append(Obstacle((-4.256520359105815,-10.582904342505728),0.1000396169033751))
        obstacles.append(Obstacle((0.08493436342840965,3.518281872227938),0.2377695968394797))
        obstacles.append(Obstacle((-1.7193115998626354,-8.996772010295565),0.14788813501659406))
        obstacles.append(Obstacle((-13.514350549239857,12.226795454534148),0.17221430123189713))
        obstacles.append(Obstacle((12.051048622000074,10.487526451468916),0.19877609437917326))
        obstacles.append(Obstacle((-7.339983507334464,-17.971532053285515),0.4767932531822696))
        obstacles.append(Obstacle((-16.674340839278265,-11.384481310587184),0.15683655700441373))
        obstacles.append(Obstacle((-19.155747861898558,-1.5327125023457278),0.2833352486273426))
        obstacles.append(Obstacle((11.932059895650124,-11.609886947791072),0.30057249826914545))
        obstacles.append(Obstacle((11.622043277557399,12.799359822596934),0.35414274393915224))
        obstacles.append(Obstacle((4.453705084616843,5.97313342034154),0.38096691515811254))
        obstacles.append(Obstacle((7.475232188329031,-4.2445236546227285),0.24498458909453366))
        obstacles.append(Obstacle((-3.495972429398144,-16.704350421467993),0.48435994958027584))
        obstacles.append(Obstacle((-2.1953618595250575,3.1121723135386006),0.29558023367854946))
        obstacles.append(Obstacle((8.831202478366649,13.660186046188585),0.25439800805144464))
        obstacles.append(Obstacle((9.892824164819697,-1.3635996434065802),0.12532980358799192))
        obstacles.append(Obstacle((6.564060042795745,19.16551730194923),0.44306777677205234))
        obstacles.append(Obstacle((17.006905266916412,-5.281657845214141),0.3484301366405915))
        obstacles.append(Obstacle((-10.794010350335723,3.2289163916097685),0.2177774658242497))
        obstacles.append(Obstacle((-16.844300258502397,15.950419310119507),0.10556392338498433))
        obstacles.append(Obstacle((18.184552842751657,1.1150665624283604),0.460000485752467))
        obstacles.append(Obstacle((-18.129689678800776,-8.109418094327792),0.3210409647797947))
        obstacles.append(Obstacle((-14.045151720853584,16.492964728777253),0.12966930107284133))
        obstacles.append(Obstacle((-16.047766235442687,-3.1823555792409444),0.1152288257540771))
        obstacles.append(Obstacle((-17.384451816646546,8.69802012774209),0.4978414262623344))
        obstacles.append(Obstacle((-17.865746939067403,-9.552810417049189),0.2707009196768372))
        obstacles.append(Obstacle((-12.79807409263892,-17.384972387778035),0.22343740147027513))
        obstacles.append(Obstacle((-8.930518270695984,8.950208121954276),0.28683052678805937))
        obstacles.append(Obstacle((-16.40049314637301,7.219901664748569),0.10609480190061858))
        obstacles.append(Obstacle((-0.24734187485766412,15.106190769112558),0.488998132949917))
        obstacles.append(Obstacle((-5.727380968809616,14.473658924736995),0.4925751564614055))
        obstacles.append(Obstacle((14.325675371346122,8.125618822614122),0.3160081736867686))
        obstacles.append(Obstacle((-14.373506548896886,10.120484694667695),0.338941073164744))
        obstacles.append(Obstacle((-9.370142154892624,10.021140046818498),0.2661326051157875))
        obstacles.append(Obstacle((16.97424977007769,9.332487537140395),0.3667021632335181))
        obstacles.append(Obstacle((15.663848147562568,14.85040975870821),0.2620969849262159))
        obstacles.append(Obstacle((17.053214763198866,4.007738819870696),0.11301768816848093))
        obstacles.append(Obstacle((-16.541293594472073,14.078831113503078),0.28694034437031735))
        obstacles.append(Obstacle((-3.536136421750289,-9.863659740413006),0.23281529785937535))
        obstacles.append(Obstacle((1.945765051364468,-11.471391487040815),0.169060988285794))
        obstacles.append(Obstacle((-5.92304085082862,9.960511561391346),0.38768761716510525))
        obstacles.append(Obstacle((5.023650502618217,9.584422845658636),0.4860945712353778))
        obstacles.append(Obstacle((-4.6405972157910504,0.651511918432945),0.10852722205451029))
        obstacles.append(Obstacle((-11.157909637153525,13.971047650954134),0.30427443958626876))
        obstacles.append(Obstacle((15.569680056512006,-5.664922654430363),0.41919131294797596))
        obstacles.append(Obstacle((-7.324440017484349,-10.139560836431642),0.22500074235707623))
        obstacles.append(Obstacle((-16.813902884181058,-17.888284018395364),0.28749367746064847))
        obstacles.append(Obstacle((15.346051756114178,-6.561243504693799),0.15236748152854332))
        obstacles.append(Obstacle((-11.968063874801533,-6.892861563997975),0.2557897495099809))
        obstacles.append(Obstacle((-12.18897260071332,-5.827740047724168),0.14703623815993014))
        obstacles.append(Obstacle((-18.80551229317272,12.756243661150563),0.260671549505995))
        obstacles.append(Obstacle((-6.787724043873503,19.806750178180074),0.21969416922870272))
        obstacles.append(Obstacle((13.556619205252687,2.610428975086929),0.29791538574851995))
        obstacles.append(Obstacle((-1.0336102505006224,11.488135313071087),0.45131389287687484))
        obstacles.append(Obstacle((-10.836614447431092,-15.22069754577728),0.21172857261466002))
        obstacles.append(Obstacle((15.925772189917879,-8.41822876543214),0.4390787375451909))
        obstacles.append(Obstacle((13.110744674580772,-0.5127160137450879),0.3878514544686775))
        obstacles.append(Obstacle((-8.41724000480339,-3.1562642930572906),0.3971961983445941))
        obstacles.append(Obstacle((12.918636042159669,2.5976809347857),0.22042251496554136))
        obstacles.append(Obstacle((8.848025149644517,-6.165458481903713),0.43971713481466923))
        obstacles.append(Obstacle((11.392533376880912,-7.169911771877725),0.1629445008688834))
        obstacles.append(Obstacle((15.800847913229958,-0.6746923027643774),0.48557537803227824))
        obstacles.append(Obstacle((-15.422794336898033,14.50199845458804),0.19073129929979069))
                

        course_map = Map([],obstacles,[XMIN,XMAX,XMIN,XMAX])
        course_map.set_start(Node(0, -19))
        course_map.set_goal(Node(4, 19))
        

        return course_map


def generate_hulls(hull_size):
    # make hull for map id 1 (zig-zag)
    map1 = make_map(1)
    rrt1 = RRTStar(map1, 5)
    if rrt1.run():
        with open('hulls/map1_hull.json', 'w') as f:
            json.dump(rrt1.export_hull(hull_size), f, indent=2)
        print("Zig-Zag Success")
    else:
        print("Zig-Zag Failure")
    
    # make hull for map id 2 (maze)
    map2 = make_map(2)
    rrt2 = RRTStar(map2, 5)
    if rrt2.run():
        with open('hulls/map2_hull.json', 'w') as f:
            json.dump(rrt2.export_hull(hull_size), f, indent=2)
        print("Maze Success")
    else:
        print("Maze Failure")

    # make hull for map id 1 (maze)
    map3 = make_map(3)
    rrt3 = RRTStar(map3, 5)
    if rrt3.run():
        with open('hulls/map3_hull.json', 'w') as f:
            json.dump(rrt3.export_hull(hull_size), f, indent=2)
        print("Forest Success")
    else:
        print("Forest Failure")

def get_hull(map_id):
    if map_id == 1:
        with open("hulls/map1_hull.json", 'r') as f:
            return json.load(f)
    elif map_id == 2:
        with open("hulls/map2_hull.json", 'r') as f:
            return json.load(f)
    elif map_id == 3:
        with open("hulls/map3_hull.json", 'r') as f:
            return json.load(f)
    return []

def store_data(rrt, map_id, yes_hull, hull_size, trial_num):
    file_name = ""
    if yes_hull:
        file_name = "Results/Map" + str(map_id) + "/Hull/" + str(hull_size) + "/map" + str(map_id) + "_hullSize" + str(hull_size) + "_trial" + str(trial_num) + ".json"
    else:
        file_name = "Results/Map" + str(map_id) + "/NoHull/map" + str(map_id) + "_trial" + str(trial_num) + ".json"
    with open(file_name, 'w') as f:
        json.dump(rrt.data, f, indent=2)


if __name__ == "__main__":
    hull_size = 7
    num_trials = 5

    for i in range(5,num_trials + 1):
        generate_hulls(hull_size)
        plt.close()
        plt.close()
        plt.close()

        # Map 1 - No Hull
        map1_no_hull = make_map(1)
        rrt = RRTStar(map1_no_hull,5)
        rrt.run()
        rrt.plot_map()
        rrt.plot_time_to_length()
        # store_data(rrt,1,False,hull_size,i)

        # Map 1 - Hull
        map1_with_hull = make_map(1)
        rrt = RRTStar(map1_with_hull,5,get_hull(1))
        rrt.run()
        rrt.plot_map()
        rrt.plot_time_to_length()
        # store_data(rrt,1,True,hull_size,i)

        # Map 2 - No Hull
        map2_no_hull = make_map(2)
        rrt = RRTStar(map2_no_hull,5)
        rrt.run()
        rrt.plot_map()
        rrt.plot_time_to_length()
        # store_data(rrt,2,False,hull_size,i)

        #Map 2 - Hull
        map2_with_hull = make_map(2)
        rrt = RRTStar(map2_with_hull,5,get_hull(2))
        rrt.run()
        rrt.plot_map()
        rrt.plot_time_to_length()
        # store_data(rrt,2,True,hull_size,i)

        # Map 3 - No Hull
        map3_no_hull = make_map(3)
        rrt = RRTStar(map3_no_hull, 5)
        rrt.run()
        rrt.plot_map()
        rrt.plot_time_to_length()
        # store_data(rrt,3,False,hull_size,i)

        # Map 3 - Hull
        map3_with_hull = make_map(3)
        rrt = RRTStar(map3_with_hull,5,get_hull(3))
        rrt.run()
        rrt.plot_map()
        rrt.plot_time_to_length()
        # store_data(rrt,3,True,hull_size,i)

        
