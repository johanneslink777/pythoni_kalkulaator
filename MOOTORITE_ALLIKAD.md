# Praegune valik: üldised mootoriprofiilid

Kasutajaliides kasutab 39 ümardatud kubatuuriga üldist konfiguratsiooni. Samaväärsed varasemad mootorid on ühendatud ning lisatud on üldised näidiskonfiguratsioonid. Mootori ehitus säilib: R6 tähendab reas kuut silindrit, V6 V-kujuliselt paigutatud kuut silindrit. Neid ei ühendata üheks profiiliks. Allolev tootjate loend kirjeldab varasemat lähtevalikut, mitte praeguste profiilide tehaseandmeid. Arvutuse eeldused kehtivad endiselt.

# Mootorite andmed ja eeldused

Varasem lähtevalik sisaldas 35 mootorit. Mahud on osaliselt ümardatud tootja nimimahud. Sama mahu, kütuseliigi ja ülelaadimisega mootorid võivad lihtsustatud mudelis anda sama tulemuse: silindrite paigutus ei lisa õhuvoolu valemisse eraldi kordajat.

| Kood | Liitrid | Allikas |
|---|---:|---|
| M47D20 | 1.951 | DE |
| M57D30 | 2.926 | DE |
| M67D40 | 3.901 | DE |
| M62B44 | 4.398 | DE |
| M50B20 | 1.991 | DE |
| M42B18 | 1.796 | DE |
| 1NZ-FE | 1.496 | JP3 |
| 2ZR-FE | 1.797 | JP3 |
| 1ZZ-FE | 1.794 | JP1 |
| 2ZZ-GE | 1.795 | JP1 |
| 2JZ-GE | 2.997 | JP2 |
| 2JZ-GTE | 2.997 | JP2 |
| EcoBoost 1.0 | 0.999 | F |
| Dragon 1.5 GTDI | 1.497 | F |
| EcoBoost 2.0 | 2 | F |
| EcoBlue 2.0 | 1.996 | F |
| Duratorq 2.2 | 2.198 | F |
| EcoBoost 2.3 | 2.298 | F |
| Duratec 2.5 PFI | 2.5 | F |
| EcoBoost 2.7 | 2.7 | F |
| EcoBoost 3.0 | 3 | F |
| Duratorq 3.2 | 3.198 | F |
| Ti-VCT 3.3 PFDI | 3.3 | F |
| LS3 | 6.2 | GM |
| LSA | 6.2 | GM |
| LS9 | 6.2 | GM |
| LS7 | 7 | GM |
| LSX454 | 7.4 | GM |
| ZZ427/480 | 7 | GM |
| 454 HO | 7.4 | GM |
| ZZ454/440 | 7.4 | GM |
| HT502 | 8.2 | GM |
| 502 HO | 8.2 | GM |
| ZZ502 | 8.2 | GM |
| ZZ572/620 | 9.4 | GM |

## Allikad
DE: varasema kuue mootori allikad ja arvutusvalemid failis BMW_ALLIKAD.md.
JP1: https://www.toyota-global.com/company/history_of_toyota/75years/vehicle_lineage/car/id60000312/index.html
JP2: https://www.toyota-global.com/company/history_of_toyota/75years/vehicle_lineage/car/id60000091/index.html
JP3: https://www.toyota-global.com/company/history_of_toyota/75years/vehicle_lineage/car/id60004229/
F: https://www.ford.co.uk/experience-ford/news/component-sales
GM: https://media.gm.com/content/dam/Media/images/US/Events/AutoShows/2013/SEMA/PerfParts/PerfPartsCatalog/ChevroletPerfPartsCatalog.pdf

## Näidiseeldused
Diisel: 2500 p/min, bensiin: 3000 p/min. Ülelaadimisega: 45 °C, vabalthingav: 20 °C. Ülerõhk diislil 1,5 bar, bensiinil 0,8 bar; need pole kinnitatud tehaseväärtused. Täitumine 85%, massisuhe diislil 25 ja bensiinil 14,7.
Kütus g/min = maht L × 275 diislil, × 180 ülelaadimisega bensiinil või × 105 vabalthingaval bensiinil. Ümardatud näidissisendid, mitte tehasekulu.
Võimsuse ja väändemomendi energiabilansi valemid ning piirangud on failis BMW_ALLIKAD.md. Kasutajaliideses automarke ega automudeleid ei kuvata.

## Pööretest sõltuv töörežiim
Kütus arvutatakse alati automaatselt. Kütusekogus [g/min] = praegune arvutatud õhumass [g/min] / profiili õhu-kütuse massisuhe. Varasemat näidiskütusekogust enam arvutuseks ei kasutata. Vajalik õhk vastab seega arvutatud õhuvoolule. See on mudeli tasakaal, mitte tegeliku mootori õhuvoolu mõõtmine. Temperatuuri ja kubatuuri muudatused mõjutavad samuti automaatset kütust.
Täitumine ja ülelaadimine muutuvad pideva tükiti lineaarse näidiskõvera järgi (tooreziim funktsioon). Need pole tootjate mõõtekaardid. Madalatel pööretel on ülelaadimine väiksem, keskel suureneb ning kõrgetel pööretel täitumine langeb.
Mudeli lubatud vahemik on diislil 600–5000 ja bensiinil 600–7500 p/min, mitte iga mootori tegelik pöördepiir. Temperatuur jääb käsitsi määratavaks. Kütuse käsitsi muutmine ei ole kasutajaliideses võimalik.
