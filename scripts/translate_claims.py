#!/usr/bin/env python3
"""Add comprehensive, fluent Kenyan Kiswahili translations to data/claims.json and write data/claims.js."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAIMS_PATH = ROOT / "data" / "claims.json"
JS_PATH = ROOT / "data" / "claims.js"

CLAIMS_SW = {
  "unga-ksh100-june-2024": {
    "title_sw": "Alidai bei ya unga wa mahindi imeshuka hadi KSh100 kote nchini",
    "quote_sw": "Kilo mbili ya unga sasa inauzwa kwa shilingi mia moja.",
    "reality_sw": "Mnamo Juni 2024, pakiti ya kilo 2 ya unga wa mahindi iliuzwa kati ya KSh130 na KSh165 kulingana na takwimu rasmi za KNBS na uchunguzi wa madukani kote nchini."
  },
  "protest-death-toll-19": {
    "title_sw": "Alidai ni watu 19 pekee waliouawa wakati wa maandamano ya Juni 2024",
    "quote_sw": "Ninavyojua mimi, watu 19 wamepoteza maisha yao.",
    "reality_sw": "Tume ya Kitaifa ya Haki za Kibinadamu (KNCHR) ilithibitisha vifo 39 kufikia Julai 1, na idadi hiyo ilizidi 60 baadaye, huku zaidi ya watu 360 wakijeruhiwa kwa risasi hai."
  },
  "universities-budget-ksh40bn": {
    "title_sw": "Alidai bajeti ya vyuo vikuu iliongezwa kutoka KSh20bn hadi KSh40bn",
    "quote_sw": "Tumeongeza bajeti ya vyuo vikuu kutoka bilioni 20 hadi bilioni 40.",
    "reality_sw": "Ripoti ya Makadirio ya Bajeti ya Kitaifa ya 2024/25 ilionyesha bajeti halisi ya elimu ya juu ilitengewa KSh28.4bn, wala haikufikia KSh40bn kama ilivyodaiwa."
  },
  "inflation-drop-5pct": {
    "title_sw": "Alidai mfumuko wa bei umeshuka hadi chini ya asilimia 5 kutokana na sera zake",
    "quote_sw": "Mfumuko wa bei sasa umeshuka chini ya asilimia tano.",
    "reality_sw": "KNBS ilionyesha mfumuko wa bei ulikuwa 5.1% mnamo Mei 2024, ukichangiwa zaidi na mvua za kutosha zilizoshusha bei za vyakula na utulivu wa mafuta ulimwenguni, wala si sera za serikali."
  },
  "eurobond-cleared-april": {
    "title_sw": "Alidai deni la Eurobond la dola bilioni 2 lililipwa kikamilifu mnamo Aprili 2024",
    "quote_sw": "Tulilipa deni lote la Eurobond mwezi Aprili.",
    "reality_sw": "Kenya ililipa tu sehemu ya $1.5bn kwa kukopa Eurobond mpya yenye riba ya juu ya 10.37%, na salio la $500m likalipwa mnamo Juni 2024 kupitia mikopo zaidi ya kibiashara."
  },
  "sona-2023-unga-145-175": {
    "title_sw": "Alidai katika Hotuba ya Hali ya Taifa 2023 kwamba unga ulikuwa unauzwa KSh145-KSh175",
    "quote_sw": "Pakiti ya kilo 2 ya unga wa mahindi sasa inauzwa kati ya Sh145 na Sh175.",
    "reality_sw": "Wastani wa bei ya reja reja ya KNBS ya Novemba 2023 ilikuwa KSh180 hadi KSh210 kwa pakiti ya kilo 2 katika miji mingi ya Kenya."
  },
  "sona-2023-police-recruitment-drop": {
    "title_sw": "Alidai vigezo vya kuajiri polisi vililegeza ili vijana wengi wajiunge",
    "quote_sw": "Tumeshusha alama za kujiunga na polisi ili watoto wote wapate nafasi.",
    "reality_sw": "Tume ya Kitaifa ya Utumishi wa Polisi (NPSC) ilikanusha madai hayo na kusisitiza vigezo vya kisheria vya kidato cha nne daraja la D+ havijabadilishwa."
  },
  "sona-2023-20000-health-workers": {
    "title_sw": "Alidai wahudumu wa afya 20,000 wapya waliajiriwa",
    "quote_sw": "Tumeajiri wahudumu wa afya wapya elfu ishirini nchini.",
    "reality_sw": "Wizara ya Afya na Muungano wa Madaktari (KMPDU) walithibitisha hakuna uajiri kama huo uliotokea; madaktari walikuwa kwenye mgomo mkubwa wakidai kuajiriwa kwa madaktari wanafunzi."
  },
  "public-debt-ksh8-8-trillion": {
    "title_sw": "Alipunguza takwimu za deni la umma na kudai lilikuwa KSh8.8 trilioni pekee",
    "quote_sw": "Deni letu la taifa lilikuwa shilingi trilioni 8.8.",
    "reality_sw": "Nyaraka za Hazina ya Kitaifa na Benki Kuu ya Kenya (CBK) zilionyesha deni la umma lilikuwa tayari limepita KSh10.2 trilioni wakati alipochukua mamlaka mnamo Septemba 2022."
  },
  "exports-28pct-of-gdp": {
    "title_sw": "Alidai mauzo ya nje yaliporomoka kutoka 28% hadi 10% ya Pato la Taifa (GDP)",
    "quote_sw": "Mauzo yetu ya nje yalishuka kutoka asilimia 28 hadi asilimia 10 ya GDP.",
    "reality_sw": "Takwimu za Benki ya Dunia na KNBS zilionyesha mauzo ya nje ya Kenya hayajawahi kufikia 28% ya GDP katika historia ya hivi karibuni, kiwango cha juu zaidi kikiwa karibu 16% mnamo 2011."
  },
  "housing-250000-jobs": {
    "title_sw": "Alidai mradi wa nyumba za gharama nafuu ulitengeneza ajira 250,000",
    "quote_sw": "Mradi wa nyumba tayari umezalisha ajira laki mbili na nusu kwa vijana.",
    "reality_sw": "Ripoti ya KNBS ya 2024 ilionyesha sekta nzima ya ujenzi nchini iliajiri wafanyakazi chini ya 230,000 rasmi, na miradi ya serikali iliajiri sehemu ndogo sana ya idadi hiyo."
  },
  "fertiliser-food-production-50pct": {
    "title_sw": "Alidai ruzuku ya mbolea iliongeza uzalishaji wa chakula kwa asilimia 50",
    "quote_sw": "Mpango wetu wa ruzuku ya mbolea umeongeza uzalishaji wa chakula kwa 50%.",
    "reality_sw": "Ongezeko halisi la uzalishaji wa nafaka lilikuwa karibu 15-20% na lilichangiwa zaidi na mvua nzuri za El Niño baada ya miaka mitatu ya ukame, wala si ruzuku pekee."
  },
  "forex-reserves-2-5-months": {
    "title_sw": "Alidai akiba ya fedha za kigeni ilikuwa inatosha miezi 2.5 tu alipoingia madarakani",
    "quote_sw": "Tulikuta akiba ya fedha za kigeni inatosha miezi miwili na nusu tu ya uagizaji.",
    "reality_sw": "Takwimu rasmi za Benki Kuu ya Kenya za Septemba 2022 zilionyesha akiba ya fedha za kigeni ilikuwa $7.34bn, ikitosheleza miezi 4.13 ya uagizaji, juu ya kiwango cha kisheria cha miezi 4."
  },
  "ecitizen-14-million-users": {
    "title_sw": "Alidai zaidi ya Wakenya milioni 14 wanatumia huduma za eCitizen",
    "quote_sw": "Wakenya zaidi ya milioni kumi na nne sasa wanatumia mtandao wa eCitizen.",
    "reality_sw": "Idadi hiyo ilijumuisha akaunti za zamani zilizoundwa tangu 2014, zikiwemo akaunti zilizorudiwa, wageni, na akaunti zisizo hai, wala haikuwa watumiaji hai wa kila mwezi."
  },
  "sona-2025-asian-tigers": {
    "title_sw": "Alidai Kenya ililingana kiuchumi na nchi za 'Asian Tigers' wakati wa uhuru",
    "quote_sw": "Wakati wa uhuru, uchumi wa Kenya ulikuwa sawa na nchi kama Korea Kusini na Singapore.",
    "reality_sw": "Takwimu za Benki ya Dunia zinaonyesha hata mnamo 1963, Pato la Taifa la kila mtu la Korea Kusini na Singapore lilikuwa mara tatu zaidi ya Kenya, zikiwa na miundombinu na viwanda vilivyoimarika zaidi."
  },
  "sona-2025-sugar-imports-down-70pct": {
    "title_sw": "Alidai uagizaji wa sukari kutoka nje ya nchi umepunguzwa kwa asilimia 70",
    "quote_sw": "Tumepunguza uagizaji wa sukari kwa asilimia 70.",
    "reality_sw": "Mamlaka ya Kilimo na Chakula (AFA) ilionyesha uagizaji wa sukari uliendelea kuwa juu kutokana na kufungwa kwa viwanda vya kienyeji na gharama kubwa za uzalishaji."
  },
  "sona-2025-maize-67m-bags": {
    "title_sw": "Alidai mavuno ya mahindi nchini yaliongezeka hadi gunia milioni 67",
    "quote_sw": "Mavuno ya mahindi mwaka huu yamefikia magunia milioni sitini na saba.",
    "reality_sw": "Wizara ya Kilimo na KNBS walikadiria mavuno ya mahindi kuwa kati ya magunia milioni 44 na 47, tofauti ya zaidi ya magunia milioni 20 na madai ya Rais."
  },
  "sona-2025-sha-indigent-premiums": {
    "title_sw": "Alidai serikali inalipia michango ya bima ya SHA kwa Wakenya wote maskini",
    "quote_sw": "Serikali inalipa michango ya bima ya afya ya SHA kwa kila Mkenya asiyejiweza.",
    "reality_sw": "Hazina ya Bima ya Kijamii ilithibitisha mfumo wa kuwatambua wasiojiweza ulikwama, na maelfu ya wagonjwa maskini walifukuzwa hospitalini au kutozwa pesa taslimu."
  },
  "sona-2024-expenditure-cut": {
    "title_sw": "Alidai matumizi ya serikali yamepunguzwa tangu mwaka 2022",
    "quote_sw": "Tumepunguza kwa kiasi kikubwa matumizi yasiyo ya lazima serikalini.",
    "reality_sw": "Ripoti ya Mdhibiti wa Bajeti (COB) ilionyesha matumizi ya kawaida ya serikali yaliongezeka kwa zaidi ya KSh400bn, yakiongozwa na safari za nje na ukarabati wa Ikulu."
  },
  "sudan-tea-exports": {
    "title_sw": "Alidai Kenya bado inauza chai nchini Sudan licha ya vita na marufuku",
    "quote_sw": "Tunaendelea kuuza chai yetu Sudan bila usumbufu wowote.",
    "reality_sw": "Bodi ya Chai ya Kenya ilithibitisha mauzo ya chai kwenda Sudan yaliporomoka kwa zaidi ya 65% kutokana na vita vya wenyewe kwa wenyewe na uhaba mkubwa wa fedha za kigeni Khartoum."
  },
  "ford-foundation-protests": {
    "title_sw": "Alishutumu shirika la Ford Foundation kufadhili maandamano ya vijana ya Gen Z",
    "quote_sw": "Mashirika kama Ford Foundation yanafadhili ghasia na fujo nchini Kenya.",
    "reality_sw": "Ford Foundation ilikanusha madai hayo na kutoa rekodi wazi za ufadhili zinazozingatia sheria za kimataifa; serikali haikutoa ushahidi wowote mahakamani."
  },
  "protest-deaths-six": {
    "title_sw": "Alidai watu sita pekee walikufa wakati wa maandamano ya Bunge tarehe 25 Juni 2024",
    "quote_sw": "Watu sita pekee ndio walipoteza maisha yao kwenye maandamano ya Bunge.",
    "reality_sw": "Mashirika ya haki za kibinadamu, KMPDU, na KNCHR yalithibitisha zaidi ya waandamanaji 23 waliuawa kwa risasi za moto nje ya Bunge na katikati ya jiji la Nairobi siku hiyo."
  },
  "no-extrajudicial-killings": {
    "title_sw": "Alidai hakuna mauaji ya kiholela yaliyotekelezwa na polisi tangu alipoingia madarakani",
    "quote_sw": "Chini ya utawala wangu, hakuna mauaji ya kiholela yanayofanywa na maafisa wa usalama.",
    "reality_sw": "IPOA na mashirika ya kutetea haki za binadamu yameandika mamia ya kesi za mauaji ya kinyama ya waandamanaji wasio na silaha, ikiwemo Rex Masai na Denzel Omondi."
  },
  "no-known-abductions": {
    "title_sw": "Alidai hafahamu mtu yeyote aliyetekwa nyara na serikali baada ya maandamano",
    "quote_sw": "Sifahamu mtu yeyote aliyetekwa nyara na polisi; nileteeni majina kama mko nayo.",
    "reality_sw": "Zaidi ya wanaharakati 60 walitekwa nyara na makachero waliovalia kiraia, wakazuiliwa bila mawasiliano, na wengine kutupwa msituni wakiwa wameteswa vibaya."
  },
  "cabinet-50pct-women": {
    "title_sw": "Aliahidi asilimia 50 ya nafasi za Baraza la Mawaziri zingepewa wanawake",
    "quote_sw": "Nusu ya Baraza langu la Mawaziri litakuwa la wanawake wa Kenya.",
    "reality_sw": "Wakati wa kutangaza Baraza la Mawaziri, ni wanawake 7 pekee kati ya 22 (chini ya 32%) walioteuliwa, na baadaye idadi hiyo ikashuka zaidi wakati wa mageuzi ya Baraza."
  },
  "free-hospital-care-jan-2024": {
    "title_sw": "Aliahidi matibabu ya bure katika hospitali za umma kuanzia Januari 2024",
    "quote_sw": "Kuanzia Januari 2024, hakuna Mkenya atalipia matibabu kwenye hospitali za umma.",
    "reality_sw": "Mpango huo haukutekelezwa; badala yake, mpango mpya wa SHIF uliongeza makato ya lazima hadi 2.75% ya mshahara, huku wagonjwa wakikosa huduma hospitalini."
  },
  "dp-stadiums-six-months-2017": {
    "title_sw": "Aliahidi viwanja 9 vya kisasa vya michezo vingekamilika ndani ya miezi 6",
    "quote_sw": "Ndani ya miezi sita, viwanja tisa vya kisasa vitakuwa vimekamilika.",
    "reality_sw": "Miaka minane baadaye, hakuna hata uwanja mmoja kati ya tisa uliokamilika kwa kiwango cha kimataifa; miradi mingi ilitelekezwa licha ya mabilioni ya pesa kutumika."
  },
  "dp-laptops-class-one-2013": {
    "title_sw": "Aliahidi kompyuta za pakato (laptops) kwa kila mtoto wa Darasa la Kwanza ndani ya siku 100",
    "quote_sw": "Kila mtoto anayeingia Darasa la Kwanza atapata laptop ndani ya siku mia moja.",
    "reality_sw": "Mradi huo ulikumbwa na ufisadi mkubwa na kushindwa; mabilioni ya pesa za umma yalipotea huku shule nyingi za vijijini zikikosa umeme na vifaa hivyo."
  },
  "dp-arror-kimwarer-7bn-2019": {
    "title_sw": "Alidai ni KSh7bn pekee zilizohusika katika miradi ya mabwawa ya Arror na Kimwarer",
    "quote_sw": "Pesa zilizotolewa kwa Arror na Kimwarer ni bilioni saba pekee, si bilioni 21.",
    "reality_sw": "Uchunguzi wa DCI na mashtaka ya DPP ulithibitisha zaidi ya KSh19bn zililipwa kinyume cha sheria kwa kampuni ya Italia ya CMC di Ravenna kwa mabwawa ambayo hayakujengwa."
  },
  "dp-galana-kulalu-1m-acres": {
    "title_sw": "Aliahidi ekari milioni moja zingewekwa chini ya umwagiliaji katika mradi wa Galana Kulalu",
    "quote_sw": "Tutaweka ekari milioni moja chini ya umwagiliaji kule Galana Kulalu.",
    "reality_sw": "Mradi huo ulisambaratika baada ya kutumia zaidi ya KSh15bn, huku chini ya ekari 10,000 pekee zikilimwa kabla ya mradi kufungwa kutokana na ufisadi."
  },
  "dp-jubilee-1-3m-jobs-2017": {
    "title_sw": "Aliahidi kutengeneza ajira milioni 1.3 kila mwaka chini ya serikali ya Jubilee",
    "quote_sw": "Tutazalisha nafasi za kazi milioni 1.3 kila mwaka kwa vijana wetu.",
    "reality_sw": "Ripoti za KNBS zilionyesha ajira rasmi zilizoongezeka kwa mwaka zilikuwa chini ya 100,000, huku mamilioni ya vijana waliohitimu wakibaki bila ajira."
  },
  "dp-weston-hotel-land-2018": {
    "title_sw": "Alidai ardhi ya hoteli ya Weston ilipatikana kwa njia halali na ya uwazi",
    "quote_sw": "Nilinunua ardhi ya Weston Hotel kihalali baada ya kufanya uchunguzi kamili.",
    "reality_sw": "Mamlaka ya Kitaifa ya Ardhi (NLC) na Mahakama Kuu walithibitisha ardhi hiyo ilikuwa mali ya Mamlaka ya Usafiri wa Anga (KCAA) na ilinyakuliwa kinyume cha sheria."
  },
  "campaign-2022-hustler-fund-interest-free": {
    "title_sw": "Aliahidi Mfuko wa Hustler Fund wa KSh50bn ungekuwa bila riba yoyote",
    "quote_sw": "Hustler Fund haitakuwa na riba; itakuwa bure ili kusaidia mama mboga na bodaboda.",
    "reality_sw": "Mfuko huo ulizinduliwa ukiwa na riba ya asilimia 8 kwa mwaka (riba ya juu ya kila siku), ikiongezeka hadi 9.5% kwa wanaochelewa kulipa."
  },
  "campaign-dollar-fall-to-120": {
    "title_sw": "Aliwashauri Wakenya kuuza dola zao akidai thamani yake ingeshuka hadi KSh120",
    "quote_sw": "Wale wanaoshikilia dola watajuta; shilingi itaimarika hadi Sh120 hivi karibuni.",
    "reality_sw": "Miezi michache baadaye, shilingi ya Kenya iliporomoka hadi kiwango cha kihistoria cha KSh163 kwa kila dola moja ya Marekani, ikisababisha hasara kubwa kwa wafanyabiashara."
  },
  "campaign-fuel-price-reduction-2022": {
    "title_sw": "Aliahidi bei ya mafuta ingeshuka mara tu baada ya kuondoa ruzuku",
    "quote_sw": "Tukiondoa ruzuku ya ulaghai, bei ya mafuta itashuka mara moja.",
    "reality_sw": "Serikali iliondoa ruzuku na kupandisha VAT ya mafuta kutoka 8% hadi 16%, na kufanya bei ya petroli kupaa hadi zaidi ya KSh217 kwa lita, kiwango cha juu zaidi katika historia."
  },
  "dp-free-secondary-education-2014": {
    "title_sw": "Aliahidi elimu ya sekondari ingekuwa bure kabisa ifikapo mwaka 2017",
    "quote_sw": "Ifikapo mwaka 2017, elimu ya sekondari nchini Kenya itakuwa bure kabisa.",
    "reality_sw": "Wazazi wanaendelea kulipa ada kubwa za shule, michango ya ujenzi, sare, na chakula, huku serikali ikipunguza mgao wa fedha za elimu (capitation) kwa kila mwanafunzi."
  },
  "campaign-no-more-borrowing-2022": {
    "title_sw": "Aliahidi utawala wake hautakopa pesa zozote za ziada kutoka nje au ndani",
    "quote_sw": "Serikali yetu haitakopa hata shilingi moja; tutaishi kulingana na mapato yetu.",
    "reality_sw": "Ndani ya miaka miwili ya kwanza madarakani, serikali ilikopa zaidi ya KSh1.8 trilioni kupitia mikopo ya kibiashara, Eurobond, IMF, na Benki ya Dunia."
  },
  "dp-57-mega-dams-2016": {
    "title_sw": "Aliahidi ujenzi wa mabwawa makubwa 57 kote nchini ili kumaliza ukame",
    "quote_sw": "Tunajenga mabwawa makubwa 57 kote nchini ili kukomesha uhaba wa maji.",
    "reality_sw": "Miradi mingi ya mabwawa ilikwama au kugubikwa na kashfa kubwa za ufisadi (kama vile Arror, Kimwarer, na Itare), bila bwawa hata moja kati ya 57 kukamilika kwa wakati."
  },
  "minister-maize-subsidized-allocation-2009": {
    "title_sw": "Alikanusha kuhusika katika kashfa ya mahindi ya ruzuku ya NCPB ya mwaka 2009",
    "quote_sw": "Sikuhusika hata kidogo katika ugawaji usio halali wa mahindi ya NCPB.",
    "reality_sw": "Ripoti ya Ukaguzi wa Hesabu za Serikali na uchunguzi wa Kamati ya Bunge (PIC) ulibaini barua rasmi kutoka kwa Wizara yake ya Kilimo ziliidhinisha wafanyabiashara binafsi kununua mahindi ya ruzuku."
  },
  "ssu-disbandment-river-yala-promise": {
    "title_sw": "Aliahidi utekaji nyara, mauaji ya kiholela, na maiti za Mto Yala vilikuwa vimekoma kabisa",
    "quote_sw": "Tumevunja kitengo cha SSU; hakuna maiti zitakazopatikana tena Mto Yala au popote nchini.",
    "reality_sw": "Miaka miwili baadaye, maiti zilizokatwakatwa zilipatikana zikitupwa kwenye machimbo ya Kware huko Mukuru, Nairobi, huku wanaharakati wakiendelea kutekwa nyara na kuuawa."
  },
  "rex-masai-live-ammunition-denial": {
    "title_sw": "Utawala ulikanusha polisi kutumia risasi za moto dhidi ya waandamanaji wa amani",
    "quote_sw": "Polisi wetu walikuwa na nidhamu ya hali ya juu na hawakutumia risasi za moto.",
    "reality_sw": "Uchunguzi wa maiti ya Rex Masai ulithibitisha alipigwa risasi ya moto ya bastola iliyopasua mshipa mkuu wa paja, na video zilionyesha afisa wa polisi akifyatua risasi moja kwa moja."
  },
  "parliament-shootings-restraint-claim": {
    "title_sw": "Alidai polisi walijizuia na hawakutumia nguvu kupita kiasi wakati wa maandamano ya Bunge",
    "quote_sw": "Polisi wetu walionyesha weledi na kujizuia sana wakati Bunge lilipovamiwa.",
    "reality_sw": "Zaidi ya watu 23 waliuawa kwa risasi za moto nje ya majengo ya Bunge mnamo Juni 25, 2024, huku wengi wakipigwa risasi mgongoni na kichwani wakiwa wanakimbia."
  },
  "abductions-give-me-names-kisumu": {
    "title_sw": "Aliwataka wananchi kumpa majina ya mtu yeyote aliyetekwa nyara na polisi",
    "quote_sw": "Kama kuna mtu yeyote ametekwa nyara na polisi, nileteeni jina lake sasa hivi.",
    "reality_sw": "Mashirika ya Haki za Binadamu (Amnesty, LSK, KNCHR) yaliwasilisha orodha rasmi ya zaidi ya majina 60 ya watu waliotekwa nyara, lakini serikali ilikataa kuwajibika au kuwashtaki wahusika."
  },
  "maandamano-2023-police-professionalism": {
    "title_sw": "Alisifu weledi wa polisi wakati wa maandamano ya upinzani ya Julai 2023",
    "quote_sw": "Nawapongeza maafisa wetu wa polisi kwa kulinda amani kwa uadilifu mkubwa.",
    "reality_sw": "Tume ya Haki za Kibinadamu ilithibitisha zaidi ya waandamanaji 50 waliuawa kwa risasi za moto huko Mlolongo, Kisumu, Kisii na Nairobi, huku wengi wakipigwa ndani ya makazi yao."
  },
  "kware-quarry-transparent-investigation": {
    "title_sw": "Aliahidi uchunguzi huru na wazi kuhusu maiti zilizotupwa kwenye machimbo ya Kware",
    "quote_sw": "Tutafanya uchunguzi huru na wa uwazi; wote waliohusika na maafa ya Kware wataadhibiwa.",
    "reality_sw": "Mshukiwa mkuu Collins Jumaisi alitoroka kwa njia ya ajabu kutoka kituo cha polisi cha Gigiri chenye ulinzi mkali, na hakuna afisa mwandamizi aliyewajibishwa."
  },
  "dp-baby-pendo-police-denial-2017": {
    "title_sw": "Utawala ulikanusha polisi kuhusika na vifo vya baada ya uchaguzi wa 2017",
    "quote_sw": "Polisi hawakuhusika na mauaji yoyote baada ya uchaguzi; vifo vilikuwa vya wahalifu.",
    "reality_sw": "Mahakama iliamua katika kesi ya kifo cha mtoto Samantha Pendo (Baby Pendo) kwamba aliuawa na polisi waliovamia nyumba ya wazazi wake Kisumu, na makamanda wa polisi wakaamriwa kushtakiwa."
  },
  "mau-forest-settlers-title-deeds-2009": {
    "title_sw": "Alitetea walowezi wa Msitu wa Mau akidai walikuwa na hatimiliki halali na kupinga kuondolewa",
    "quote_sw": "Watu hawa wana hatimiliki halali za ardhi; hawapaswi kufukuzwa msituni.",
    "reality_sw": "Tume ya Uchunguzi ya Ndung'u na Mahakama Kuu zilithibitisha ardhi yote ya hifadhi ya Msitu wa Mau iligawiwa kinyume cha sheria kwa maslahi ya kisiasa, na hatimiliki hizo zilikuwa batili."
  },
  "mau-forest-no-evictions-promise-2018": {
    "title_sw": "Aliahidi walowezi wa Mau hawatafukuzwa bila kulipwa fidia na kupewa makazi mapya",
    "quote_sw": "Hakuna Mkenya atakayefukuzwa kutoka Mau bila fidia na mpango mzuri wa makazi.",
    "reality_sw": "Maelfu ya familia walifukuzwa na nyumba zao kuchomwa moto bila fidia yoyote wakati wa operesheni za kulinda msitu, jambo lililowaacha bila makazi."
  },
  "logging-ban-lifted-mature-trees-2023": {
    "title_sw": "Alidai kuondolewa kwa marufuku ya miaka 6 ya ukataji miti kulihitajika kwa sababu miti ilikuwa inaoza",
    "quote_sw": "Miti imekomaa na inaoza misituni huku wananchi wakikosa mbao na kazi.",
    "reality_sw": "Mashirika ya mazingira na wanasayansi walionyesha ukataji huo ulilenga misitu asili ya vyanzo vya maji, na Mahakama ya Mazingira na Ardhi ikatoa amri ya kusitisha ukataji huo."
  },
  "logging-trees-15-billion-promise": {
    "title_sw": "Alidai lengo la kupanda miti bilioni 15 halitaathiriwa na kuondolewa kwa marufuku ya ukataji miti",
    "quote_sw": "Mpango wetu wa kupanda miti bilioni 15 uko imara na hautavurugwa na uvunaji wa miti.",
    "reality_sw": "Kiwango cha ukataji miti kibiashara kiliongezeka mara tatu ya kasi ya upandaji miti, huku miche mingi ikikauka kutokana na ukosefu wa bajeti ya kuitunza."
  },
  "shareholding-government-equal-service-denial": {
    "title_sw": "Alikanusha serikali kuendeshwa kwa misingi ya 'hisa za kikabila' licha ya jamii 2 kutawala teuzi",
    "quote_sw": "Serikali yangu ni ya Wakenya wote bila ubaguzi wa kikabila au eneo.",
    "reality_sw": "Naibu Rais Rigathi Gachagua alitangaza hadharani kuwa serikali ni kampuni ya hisa (shareholding), na ripoti ya Tume ya Uwiano (NCIC) ilionyesha zaidi ya 70% ya nafasi kuu za serikali zilienda kwa jamii mbili pekee."
  },
  "vernacular-mobilization-one-kenya-contradiction": {
    "title_sw": "Alidai Kenya imeachana kabisa na siasa za kikabila na kuingia katika siasa za kiuchumi",
    "quote_sw": "Tumebadilisha siasa za Kenya milele; hakuna tena siasa za ukabila bali ni uchumi.",
    "reality_sw": "Utawala uliendelea kutumia mikutano ya kikabila Ikulu na vituo vya redio za kikabila kuhamasisha uungwaji mkono wa kisiasa pindi serikali ilipokosolewa."
  },
  "tsc-letters-mps-state-house-distribution": {
    "title_sw": "Alidai uajiri wa walimu ulikuwa kwa misingi ya sifa pekee huku barua za TSC zikigawiwa wabunge Ikulu",
    "quote_sw": "Uajiri wa walimu ni wa wazi asilimia mia moja kupitia mfumo wa kidijitali wa TSC.",
    "reality_sw": "Wabunge wa muungano tawala walithibitisha hadharani kupewa mafungu ya barua za ajira za walimu wa TSC Ikulu ili kuwazawadia wafuasi wao wa kisiasa maeneo bunge."
  },
  "jss-intern-teachers-permanent-promise": {
    "title_sw": "Aliahidi walimu wanafunzi wa JSS wataajiriwa kwa masharti ya kudumu baada ya mwaka mmoja",
    "quote_sw": "Walimu hawa wa mafunzo watathibitishwa kuwa wa kudumu mara tu mwaka mmoja utakapokamilika.",
    "reality_sw": "Mnamo 2024, serikali ilikataa kuwathibitisha na kutangaza wataendelea kuwa wanafunzi wa mafunzo kwa mkataba mpya, jambo lililosababisha mgomo wa nchi nzima na maamuzi ya mahakama."
  },
  "adani-jkia-deal-secrecy-denial": {
    "title_sw": "Alikanusha Uwanja wa Ndege wa Kimataifa wa JKIA kukodishwa kwa siri kwa Kampuni ya Adani",
    "quote_sw": "Hakuna anayeuza au kukodisha uwanja wa JKIA; hizi zote ni propaganda za wapinzani.",
    "reality_sw": "Nyaraka za siri zilizofichuliwa na Nelson Amenya zilionyesha mkataba wa miaka 30 wenye thamani ya $1.85bn ulikuwa tayari umesainiwa kwa siri kumpa Adani umiliki na ushuru wote wa JKIA."
  },
  "fake-fertiliser-scandal-denial": {
    "title_sw": "Alitupilia mbali ripoti za mbolea feki ya ruzuku akidai ni fitina za kisiasa",
    "quote_sw": "Hakuna mbolea feki; hizo ni hadithi za watu wanaotaka kurudisha siasa za nyuma.",
    "reality_sw": "Ukaguzi wa Shirika la Viwango nchini (KEBS) na Bunge ulithibitisha maelfu ya mifuko ya 'mbolea ya ruzuku' iliyouzwa kwa wakulima ilikuwa na mchanga, mawe, na samadi chafu."
  },
  "cas-50-appointments-unconstitutional": {
    "title_sw": "Aliunda na kuwaapisha Makatibu Wasaidizi 50 (CAS) baada ya kuahidi kupunguza matumizi ya serikali",
    "quote_sw": "Nitaongoza serikali ndogo yenye nidhamu ya kifedha bila vyeo visivyo vya lazima.",
    "reality_sw": "Mahakama Kuu ilitangaza nafasi zote 50 za CAS kuwa kinyume cha Katiba na batili, baada ya serikali kutenga mabilioni ya mishahara na magari ya kifahari kwa washirika wake wa kisiasa."
  },
  "luxury-jet-us-state-visit-cheaper-claim": {
    "title_sw": "Alidai ndege ya kifahari ya kukodi ya Boeing 737 ilikuwa nafuu kuliko Kenya Airways",
    "quote_sw": "Ndege ya kibinafsi tuliyotumia kwenda Marekani ilikuwa na gharama nafuu kuliko kutumia Kenya Airways.",
    "reality_sw": "Ndege hiyo ya Royal Jet iligharimu zaidi ya KSh200 milioni za walipakodi kwa safari moja tu ya Marekani, mara kumi zaidi ya tiketi za daraja la kwanza kwenye Shirika la Ndege la Kenya Airways."
  },
  "state-house-renovations-ksh1-5bn": {
    "title_sw": "Alihubiri kubana matumizi huku ukarabati wa Ikulu na anasa zikiongezeka kwa mabilioni",
    "quote_sw": "Lazima kila mtu ajifunge kibwebwe na serikali ianze kwa kupunguza matumizi yake.",
    "reality_sw": "Bajeti ya ziada ilitenga zaidi ya KSh1.5bn kwa ukarabati wa Ikulu ya Nairobi na Ikulu ndogo za mashambani, pamoja na mabilioni zaidi ya ununuzi wa magari mapya ya kifahari."
  },
  "judiciary-threats-defiance-court-orders": {
    "title_sw": "Alitoa vitisho kwa majaji na kuapa kukaidi amri za mahakama kuhusu Ushuru wa Nyumba na SHIF",
    "quote_sw": "Hatuwezi kuruhusu majaji fisadi kuzuia miradi yetu ya maendeleo; tutasonga mbele bila kujali maagizo yao.",
    "reality_sw": "Jaji Mkuu Martha Koome na Tume ya Utumishi wa Mahakama (JSC) walitoa onyo kali wakilaani mashambulizi ya Rais kama tishio kubwa kwa uhuru wa mahakama na utawala wa sheria."
  },
  "kdf-deployment-protesters-unconstitutional": {
    "title_sw": "Alituma Jeshi la KDF kukabili waandamanaji wasio na silaha bila idhini ya kikatiba ya Bunge",
    "quote_sw": "Majeshi yetu ya ulinzi yametumwa kisheria kusaidia polisi kulinda taifa dhidi ya wasaliti.",
    "reality_sw": "Mahakama Kuu iliamua kutumwa kwa wanajeshi wa KDF mitaani kulikiuka Ibara ya 241(3)(c) ya Katiba kwa kukosa idhini ya wazi ya Bunge na masharti ya ulinzi wa haki za kibinadamu."
  },
  "kntc-kemsa-cooking-oil-scandal": {
    "title_sw": "Alidai mpango wa kuingiza mafuta ya kula bila ushuru ulikuwa wazi na ulishusha bei za vyakula",
    "quote_sw": "Mpango wa KNTC wa mafuta ya kula umepunguza gharama ya maisha kwa wananchi.",
    "reality_sw": "Ripoti ya Mkaguzi Mkuu wa Hesabu za Serikali ilifichua kampuni zilizopewa zabuni ya KSh16.5bn ziliteuliwa kisiri bila ushindani, na mafuta hayo yalibainika hayakufaa kwa matumizi ya binadamu na KEBS."
  },
  "buying-opposition-mps-cooptation-denial": {
    "title_sw": "Alikanusha kugawa hongo au kutumia mashine ya serikali kusambaratisha upinzani bungeni",
    "quote_sw": "Sijawahi kumnunua mbunge yeyote; wabunge wanajiunga nasi kwa hiari kwa ajili ya maendeleo.",
    "reality_sw": "Wabunge kadhaa wa Azimio walikiri hadharani kuahidiwa miradi, fedha, na kufutiwa kesi za ufisadi ili kupiga kura kuunga mkono miswada ya kodi ya serikali bungeni."
  },
  "housing-levy-unconstitutional-ruling": {
    "title_sw": "Alisisitiza Ushuru wa lazima wa Nyumba wa 1.5% ulikuwa halali na unafuata Katiba",
    "quote_sw": "Ushuru wa nyumba uko ndani ya Katiba na unaleta usawa kwa kila Mkenya.",
    "reality_sw": "Majaji watatu wa Mahakama Kuu waliamua kwa pamoja kwamba ushuru huo ulikuwa wa kibaguzi, uliokiuka Ibara ya 10 na 201 ya Katiba, na ulikosa msingi thabiti wa kisheria."
  },
  "adani-ketraco-power-lines-deal": {
    "title_sw": "Alidai mkataba wa kampuni ya Adani wa kusambaza nyaya za umeme za KETRACO ulikuwa wa ushindani na wazi",
    "quote_sw": "Mkataba wa KETRACO na Adani ulifanywa kwa uwazi mkubwa na utaleta umeme nafuu.",
    "reality_sw": "Mkataba huo wa KSh95bn ulitolewa kisiri bila zabuni ya wazi ya ushindani kulingana na sheria ya PPP, na kusababisha kusitishwa kwake na Mahakama Kuu na kufutiliwa mbali baadaye."
  },
  "controller-of-budget-budgeted-corruption": {
    "title_sw": "Utawala ulikanusha madai ya Mdhibiti wa Bajeti kuhusu ufisadi uliopangwa kwenye bajeti ya serikali",
    "quote_sw": "Hakuna ufisadi kwenye bajeti; kila shilingi inatengwa kwa mujibu wa sheria za fedha.",
    "reality_sw": "Mdhibiti wa Bajeti Margaret Nyakang'o alifichua bungeni kuwa bajeti ya kawaida iliongezwa kwa siri mabilioni ya mishahara hewa, ikiwemo mishahara ya watendaji wakuu wa serikali iliyolipwa mara tatu."
  },
  "shif-sha-healthcare-unconstitutional": {
    "title_sw": "Alidai mpango mpya wa afya wa SHIF/SHA ulizinduliwa vizuri na unatoa matibabu bure kwa wote",
    "quote_sw": "Mpito wa kwenda SHA umekuwa wa mafanikio makubwa; hakuna Mkenya anayenyimwa huduma.",
    "reality_sw": "Mahakama Kuu ilitangaza Sheria ya Bima ya Afya ya Jamii (SHIA) kuwa kinyume cha Katiba, huku maelfu ya wagonjwa wa saratani na wanaohitaji kusafishwa figo (dialysis) wakikwama hospitalini."
  },
  "office-of-first-lady-budget-broken-promise": {
    "title_sw": "Aliahidi hakutakuwa na Ofisi ya Mke wa Rais wala bajeti ya umma kwa wake za viongozi",
    "quote_sw": "Hakutakuwa na Ofisi ya Mke wa Rais; fedha za umma hazitatumika kwa familia ya Rais.",
    "reality_sw": "Hazina ya Kitaifa ilitenga zaidi ya KSh1.2bn kwa Ofisi ya Mke wa Rais na Mke wa Naibu Rais, ikijumuisha wafanyakazi rasmi na walinzi wa serikali kabla ya maandamano ya Gen Z kulazimisha kufutwa kwake."
  },
  "dpp-withdrawal-graft-cases-allies": {
    "title_sw": "Aliahidi vita dhidi ya ufisadi vitakuwa huru na havitalinda washirika wa kisiasa",
    "quote_sw": "Taasisi za kukabili ufisadi zitakuwa huru kabisa; hakuna atakayekingwa hata akiwa rafiki yangu.",
    "reality_sw": "Mkurugenzi wa Mashtaka ya Umma (DPP) aliondoa ghafla kesi za ufisadi za mabilioni ya pesa zilizowakabili washirika wake wakuu wa kisiasa mara tu walipoteuliwa kuwa Mawaziri na vigogo wa serikali."
  },
  "foreign-trips-presidential-travel-austerity": {
    "title_sw": "Aliahidi kupunguza safari za nje za serikali kwa 50% ili kubana matumizi",
    "quote_sw": "Nimeagiza safari zote za nje za watumishi wa umma zipunguzwe kwa asilimia hamsini mara moja.",
    "reality_sw": "Ndani ya miezi 20 ya kwanza, Rais Ruto alisafiri nje ya nchi zaidi ya mara 50 akitembelea nchi zaidi ya 35, akivunja rekodi ya matumizi ya safari za nje ya marais wote waliomtangulia."
  },
  "finance-bill-2024-criminal-infiltrators-claim": {
    "title_sw": "Alidai waandamanaji wa Gen Z waliopinga kodi walikuwa wahalifu na vibaraka wa kigeni",
    "quote_sw": "Maandamano haya yameingiliwa na magenge ya wahalifu hatari wanaotaka kupindua serikali.",
    "reality_sw": "Maandamano hayo yaliongozwa kwa amani na vijana wa Kenya wa kizazi cha Gen Z bila itikadi za kikabila au kisiasa, wakitetea haki zao za kikatiba chini ya Ibara ya 37 ya Katiba."
  },
  "icc-cases-witness-tampering-vindication-claim": {
    "title_sw": "Alidai kuondolewa kwa kesi yake katika Mahakama ya ICC ilikuwa ushindi kamili wa kutokuwa na hatia",
    "quote_sw": "Mahakama ya ICC ilitupilia mbali kesi zote na kuthibitisha hatukuwa na hatia yoyote.",
    "reality_sw": "Majaji wa ICC walisitisha kesi hiyo bila kumuondolea hatia (no acquittal), wakibainisha kuwa mashahidi walitishwa, kuhongwa, na kuingiliwa kisiasa kwa kiwango kikubwa kilichovuruga kesi."
  },
  "icc-witness-meshack-yebei-murder-denial": {
    "title_sw": "Utawala ulidai shahidi wa ICC aliyeuawa Meshack Yebei alitekwa nyara na maadui wanaotaka kupaka matope utetezi",
    "quote_sw": "Meshack Yebei alikuwa shahidi wa upande wetu wa utetezi na aliuawa na maadui zetu.",
    "reality_sw": "Mwendesha Mashtaka wa ICC alithibitisha Yebei alikuwa shahidi muhimu wa upande wa mashtaka kabla ya kuuawa kinyama na mwili wake kutupwa katika Hifadhi ya Wanyama ya Tsavo."
  },
  "icc-paul-gicheru-witness-tampering-denial": {
    "title_sw": "Alikanusha kuhusika katika mtandao wa kutoa hongo kwa mashahidi wa ICC kabla ya mshukiwa mkuu kufa kizembe Karen",
    "quote_sw": "Sijawahi kuhusika na ulipaji hongo au ushawishi wa mashahidi wa ICC.",
    "reality_sw": "Wakili Paul Gicheru alijisalimisha ICC akikabiliwa na mashtaka ya kusimamia mtandao wa kuhonga mashahidi kwa mamilioni ya fedha kwa manufaa ya Ruto, kabla ya kufa ghafla nyumbani kwake Karen mnamo 2022."
  },
  "dp-muteshi-pev-land-ruling-2013": {
    "title_sw": "Alidai alinunua kwa njia halali shamba la ekari 100 la Turbo lililonyakuliwa kutoka kwa mwathiriwa wa PEV Adrian Muteshi",
    "quote_sw": "Shamba la Turbo nililinunua kisheria na nilikuwa mnunuzi asiye na hatia.",
    "reality_sw": "Jaji Rose Ougo wa Mahakama Kuu aliamua kwamba Ruto alijinyakulia shamba hilo kinyume cha sheria kutoka kwa Muteshi aliyekimbia ghasia za 2007/08, na akamuamuru arudishe shamba hilo na kulipa fidia ya KSh5 milioni."
  },
  "tourists-doubled-2022-2023": {
    "title_sw": "Alidai idadi ya watalii iliongezeka mara mbili kutoka milioni 1 hadi milioni 2",
    "quote_sw": "Idadi ya watalii mwaka 2022 ilikuwa milioni moja; mwaka 2023 imefika watalii milioni mbili.",
    "reality_sw": "Takwimu za KNBS zilionyesha watalii walikuwa milioni 1.54 mnamo 2022 na milioni 2.1 mnamo 2023. Kupunguza idadi ya 2022 kulifanya ongezeko halisi la 35% kuonekana kama lilikuwa mara mbili."
  },
  "youth-4-5-million-jobless": {
    "title_sw": "Alidai vijana milioni 4.5 waliohitimu vyuo hawana ajira",
    "quote_sw": "Tuna takriban vijana milioni nne na nusu waliomaliza vyuo wenye shahada na stashahada lakini hawana kazi.",
    "reality_sw": "Takwimu za KNBS zilionyesha takriban vijana milioni 3.5 hawako shuleni au kazini, na idadi ya wenye stashahada au shahada ilikuwa chini sana ya takwimu hiyo aliyojumuisha makundi tofauti."
  },
  "sona-2023-ttc-admissions-300pct": {
    "title_sw": "Alidai udahili katika vyuo vya walimu uliongezeka kwa 300% kufikia 20,456",
    "quote_sw": "Udahili katika vyuo vya mafunzo ya walimu umeongezeka kwa 300% na sasa umefikia 20,456.",
    "reality_sw": "Utafiti wa Kiuchumi wa KNBS ulionyesha wanafunzi wa ualimu walikuwa 17,984 mnamo 2022; hivyo 20,456 lilikuwa ongezeko la karibu 13.7% pekee, wala si 300% kama ilivyodaiwa."
  }
}

def enrich_claims():
    claims = json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))
    updated = 0
    for c in claims:
        cid = c["id"]
        if cid in CLAIMS_SW:
            sw = CLAIMS_SW[cid]
            c["title_sw"] = sw["title_sw"]
            c["reality_sw"] = sw["reality_sw"]
            c["quote_sw"] = sw["quote_sw"]
            updated += 1
        else:
            print(f"Warning: Missing Swahili translation for {cid}")
    
    CLAIMS_PATH.write_text(json.dumps(claims, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    JS_PATH.write_text("window.CLAIMS = " + json.dumps(claims, indent=2, ensure_ascii=False) + ";\n", encoding="utf-8")
    print(f"Successfully added Swahili translations to {updated}/{len(claims)} claims in data/claims.json and data/claims.js")

if __name__ == "__main__":
    enrich_claims()
