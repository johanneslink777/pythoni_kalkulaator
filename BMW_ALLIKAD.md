# Prodigy BMW mootoriprofiilid

Kontrollitud 03.11.2026. Iga profiil esindab alltoodud varianti, mitte kogu mootoriperekonda. Nimivõimsus on taustainfo ega osale õhuvoolu arvutuses.

| Mootor ja variant | Kubatuur | Võimsus | Allikas |
|---|---:|---:|---|
| M47D20, E46 320d, 1998–2001 | 1951 cm³ | 100 kW | [BMW 320d](https://www.bmwgroup-classic.com/de/modelle/bmw-klassiker/product-description-page.ad-90-1.bmw-320d-e46.html) |
| M57D30, E46 330d, enne 03/2003 | 2926 cm³ | 135 kW | [BMW 330d](https://www.bmwgroup-classic.com/en/models/bmw-classics/product-description-page.ad-630-1.bmw-330d-e46.html) |
| M67D40, E38 740d, 175 kW variant | 3901 cm³ | 175 kW | [BMW 740d](https://www.bmwgroup-classic.com/en/models/bmw-classics/product-description-page.ad-851-1.bmw-740d-e38.html) |
| M62B44, E39 540i, enne TU uuendust | 4398 cm³ | 210 kW | [BMW 540i](https://www.bmwgroup-classic.com/de/modelle/bmw-klassiker/product-description-page.ad-640-1.bmw-540i-e39.html) |
| M50B20, varajane E36 320i | 1991 cm³ | 110 kW | [BMW 320i](https://www.bmwgroup-classic.com/en/models/bmw-classics/product-description-page.ad-464-5.bmw-320i-e36.html) |
| M42B18, E30 318is, 1989–1991 | 1796 cm³ | 100 kW | [BMW 318is](https://www.bmwgroup-classic.com/de/modelle/bmw-klassiker/product-description-page.ad-83-1.bmw-318is-e30.html) |

M67-l on ka 180 kW variant; siin on valitud BMW Classicu 175 kW kirjeldus. M42 E36 variandi võimsus erineb siin kasutatud E30 omast. M47 ja M57 hilisemad versioonid on teise kubatuuri ja võimsusega.

## Arvutuse eeldused, mitte BMW mõõteandmed

- Diislid: 2500 p/min, 45 °C, 1,5 bar ülerõhk (2,51325 bar absoluutne), õhu-kütuse massisuhe 25.
- Bensiinimootorid: 3000 p/min, 20 °C, 1,01325 bar absoluutne rõhk, massisuhe 14,7.
- Kõigi profiilide mahuline kasutegur on näitlikult 85%.
- Kütusekogused on valitud näidissisendid, mitte mõõdetud kulu ega nimivõimsusele vastav kütusekulu.
- Kasutaja saab muuta kubatuuri, pöördeid, temperatuuri ja kütusekogust. Ülejäänud eeldused jäävad profiili valiku järgi fikseerituks.

Need allikad ei anna töörežiimide kaupa õhuvoolu, kütusekulu ega ülelaaderõhu kaarte. Seetõttu ei ole kalkulaator konkreetse BMW mootori kalibreeritud simulatsioon. Turbo rõhku ei korrutata turbolaadurite arvuga.


## Võimsus ja väändemoment

Võimsus on valitud töörežiimi lihtsustatud energiabilanss, mitte tehase maksimum ega dünostendi tulemus.

- Arvestatav kütus [g/min] = min(sisestatud kütus, õhuvool / profiili õhu-kütuse suhe).
- Võimsus [kW] = arvestatav kütus × alumine kütteväärtus [MJ/kg] / 60 × efektiivne kasutegur.
- Väändemoment [Nm] = võimsus × 60000 / (2π × pöörded [p/min]).
- Mudeli konstandid: diisel 42,6 MJ/kg ja 32%; bensiin 43,5 MJ/kg ja 24%. Need on illustratiivsed eeldused, mitte BMW mootorite mõõdetud kasutegurid.
- Õhupiirang on valitud massisuhte järgi seatud mudelipiir, mitte tegeliku põlemise või mootori juhtaju simulatsioon.
- Kasutegur ei muutu pöörete ega koormusega; mudel ei arvesta mootori tegelikku pöördepiiri. Ebatavaliste sisendite tulemused ei pruugi olla füüsiliselt saavutatavad.

Taust: [Open University: Petrol and diesel engines](https://www.open.edu/openlearn/mod/oucontent/view.php?id=165180&section=6).
Võimsuse ja väändemomendi seos: [Thompson Couplings](https://thompsoncouplings.com/wp-content/uploads/2021/05/TECHNICAL-UPDATE-003-Torque-Power-and-Speed.pdf).
