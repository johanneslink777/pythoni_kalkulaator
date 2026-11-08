"""Prodigy lihtsustatud füüsikamudel; kasutajaliidesest sõltumatu."""
import math


def arvuta(kubatuur, poorded, taitumine, temperatuur, rohk, kytus, suhe):
    """Sisendid: L, p/min, %, °C, bar absoluutne, g/min, massisuhe."""
    values = (kubatuur, poorded, taitumine, temperatuur, rohk, kytus, suhe)
    if not all(math.isfinite(v) for v in values):
        raise ValueError('Sisesta lõplikud arvud.')
    if min(kubatuur, poorded, taitumine, rohk, suhe) <= 0 or kytus < 0:
        raise ValueError('Väärtused peavad olema positiivsed; kütusekogus võib olla null.')
    if temperatuur <= -273.15:
        raise ValueError('Temperatuur peab olema üle absoluutse nulli.')
    tihedus = rohk * 100000 / (287.05 * (temperatuur + 273.15))
    maht = kubatuur * poorded / 2 * taitumine / 100
    mass = maht / 1000 * tihedus * 1000
    return maht, mass, kytus * suhe, mass / suhe


def hinnang(kytus, ohule_vastav_kytus, poorded, diisel):
    """Energiapõhine hinnang; piirab kütust mudeli õhu-kütuse suhte järgi."""
    if not all(math.isfinite(x) for x in (kytus, ohule_vastav_kytus, poorded)):
        raise ValueError('Vigane sisend')
    if min(kytus, ohule_vastav_kytus) < 0 or poorded <= 0:
        raise ValueError('Vigane sisend')
    # Mudeli eeldused, mitte konkreetse mootori mõõdetud kasutegurid.
    energia, kasutegur = (42.6, 0.32) if diisel else (43.5, 0.24)
    kasutatud = min(kytus, ohule_vastav_kytus)
    kw = kasutatud * energia / 60 * kasutegur
    nm = kw * 60000 / (2 * math.pi * poorded)
    if not all(math.isfinite(x) for x in (kw, nm)):
        raise ValueError('Liiga suur sisend')
    return kw, nm


def tooreziim(base, rpm, diesel):
    """Illustratiivne püsikoormuse kõver, mitte mõõdetud mootorikaart."""
    limit = 5000 if diesel else 7500
    if not math.isfinite(rpm) or not 600 <= rpm <= limit:
        raise ValueError(f'Mudeli pöördevahemik on 600–{limit} p/min.')
    points = [(600, .62, 0), (1000, .72, .12), (1800, .86, .8),
              (2500, .9, 1), (3500, .86, 1), (4500, .7, .8), (5000, .55, .6)] if diesel else [
              (600, .55, 0), (1000, .65, .05), (2000, .78, .4),
              (3000, .85, .85), (4500, .92, 1), (6000, .85, .95), (7500, .65, .75)]
    for left, right in zip(points, points[1:]):
        if left[0] <= rpm <= right[0]:
            t = (rpm-left[0])/(right[0]-left[0])
            fill = left[1] + t*(right[1]-left[1])
            boost = left[2] + t*(right[2]-left[2])
            return fill*100, 1.01325 + (base[4]-1.01325)*boost

