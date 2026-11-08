"""Mootorite nimimahud; töörežiimid on õppemudeli eeldused."""
# kood/nimi, liitrid, ehitus, diisel, ülelaadimine, allikagrupp
ENGINES = [
('M47D20',1.951,'R4',True,True,'DE'),
('M57D30',2.926,'R6',True,True,'DE'),
('M67D40',3.901,'V8',True,True,'DE'),
('M62B44',4.398,'V8',False,False,'DE'),
('M50B20',1.991,'R6',False,False,'DE'),
('M42B18',1.796,'R4',False,False,'DE'),
('1NZ-FE',1.496,'R4',False,False,'JP3'),
('2ZR-FE',1.797,'R4',False,False,'JP3'),
('1ZZ-FE',1.794,'R4',False,False,'JP1'),
('2ZZ-GE',1.795,'R4',False,False,'JP1'),
('2JZ-GE',2.997,'R6',False,False,'JP2'),
('2JZ-GTE',2.997,'R6',False,True,'JP2'),
('EcoBoost 1.0',0.999,'R3',False,True,'F'),
('Dragon 1.5 GTDI',1.497,'R3',False,True,'F'),
('EcoBoost 2.0',2.0,'R4',False,True,'F'),
('EcoBlue 2.0',1.996,'R4',True,True,'F'),
('Duratorq 2.2',2.198,'R4',True,True,'F'),
('EcoBoost 2.3',2.298,'R4',False,True,'F'),
('Duratec 2.5 PFI',2.5,'R4',False,False,'F'),
('EcoBoost 2.7',2.7,'V6',False,True,'F'),
('EcoBoost 3.0',3.0,'V6',False,True,'F'),
('Duratorq 3.2',3.198,'R5',True,True,'F'),
('Ti-VCT 3.3 PFDI',3.3,'V6',False,False,'F'),
('LS3',6.2,'V8',False,False,'GM'),
('LSA',6.2,'V8',False,True,'GM'),
('LS9',6.2,'V8',False,True,'GM'),
('LS7',7.0,'V8',False,False,'GM'),
('LSX454',7.4,'V8',False,False,'GM'),
('ZZ427/480',7.0,'V8',False,False,'GM'),
('454 HO',7.4,'V8',False,False,'GM'),
('ZZ454/440',7.4,'V8',False,False,'GM'),
('HT502',8.2,'V8',False,False,'GM'),
('502 HO',8.2,'V8',False,False,'GM'),
('ZZ502',8.2,'V8',False,False,'GM'),
('ZZ572/620',9.4,'V8',False,False,'GM'),
]


def profiles():
    """Üldised õppemudeli profiilid, mitte konkreetsete tootjate mootorid."""
    variants = set()
    for _, volume, layout, diesel, boosted, _ in ENGINES:
        variants.add((round(volume, 1), layout, diesel, boosted))
    # Täiendavad üldised konfiguratsioonid, et valik säiliks mitmekesine.
    variants.update([
        (1.0, 'R3', False, False), (1.2, 'R3', False, True),
        (1.2, 'R4', False, False), (1.4, 'R4', False, False),
        (1.4, 'R4', False, True), (1.6, 'R4', False, False),
        (1.6, 'R4', False, True), (1.6, 'R4', True, True),
        (1.8, 'R4', False, True), (2.0, 'R4', True, False),
        (2.4, 'R4', False, False), (3.5, 'R6', False, False),
        (4.0, 'V8', False, False), (5.0, 'V8', False, False),
    ])
    presets, info = {}, []
    for volume, layout, diesel, boosted in sorted(variants):
        fuel = 'diisel' if diesel else 'bensiin'
        name = f'{volume:.1f}L {layout} {fuel.capitalize()}'
        if boosted:
            name += ' · ülelaadimisega'
        rpm = 2500 if diesel else 3000
        temperature = 45 if boosted else 20
        pressure = 2.51325 if diesel and boosted else 1.81325 if boosted else 1.01325
        ratio = 25 if diesel else 14.7
        amount = round(volume * (275 if diesel else 180 if boosted else 105))
        presets[name] = (volume, rpm, 85, temperature, pressure, amount, ratio)
        induction = 'Ülelaadimisega' if boosted else 'Vabalthingav'
        info.append(f'{induction} · üldine näidisprofiil')
    return presets, info
