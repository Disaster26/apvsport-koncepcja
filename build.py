# Buduje index.html z src.html: logo SVG, znak Wylinki (oficjalny fragment), karty produktow.
# Nazwy i ceny z aquaholm.pl (WooCommerce Store API) - wg klienta obowiazujace, sprawdzone 20.11.2026.
# Elite Series (21.11 klient: pokazac, brak w aquaholm.pl przez pomylke) - ceny z apvsport.pl Store API 21.11.2026 (takie same jak W8).
import html as H, re
s = open('src.html', encoding='utf-8').read()
svg = open('img/logo.svg', encoding='utf-8').read()
vb = re.search(r'viewBox="([^"]+)"', svg).group(1); d = re.search(r' d="([^"]+)"', svg).group(1)
LOGO = f'<svg viewBox="{vb}" role="img" aria-label="APVsport"><path fill="currentColor" fill-rule="evenodd" d="{d}"/></svg>'
s = s.replace('{{LOGO}}', LOGO)
s = s.replace('{{BADGE_STYLE}}', open('badge_style.part', encoding='utf-8').read().replace('<style>', '').replace('</style>', ''))
s = s.replace('{{BADGE_LINK}}', open('badge_link.part', encoding='utf-8').read().strip())
SW = '<svg class="sw" viewBox="0 0 26 12" aria-hidden="true"><path d="M0 12C8 5 17 1.4 26 0 18.4 3 11.6 7 6 12Z"/></svg>'

def zdj(img, alt, pc=''):
    p = f'<span class="pc">{pc}</span>' if pc else ''
    return (f'<button class="zd" type="button" data-lb="img/{img}-640.webp" aria-label="Powiększ zdjęcie: {H.escape(alt)}">{p}'
            f'<img src="img/{img}-360.webp" srcset="img/{img}-360.webp 360w, img/{img}-640.webp 640w" sizes="(min-width:1281px) 22vw, (min-width:601px) 40vw, 80vw" width="640" height="480" loading="lazy" decoding="async" alt="{H.escape(alt)}"></button>')

def wersje(ws):
    return '<ul class="wer">' + ''.join(f'<li><span>{H.escape(n)}</span><b>{c} zł{f"<s>{o} zł</s>" if o else ""}</b></li>' for n, c, o in ws) + '</ul>'

SERIE = [
    ('elitek', 'APV8000 Elite Series', 'Ekran dotykowy Android 10,1", pas 145 x 58 cm.', 'Bieżnia APVsport APV8000 Elite Series'),
    ('futura', 'APV8000 Futura Prestige', 'Największy ekran: dotykowy Android 15,6", pas 145 x 58 cm.', 'Bieżnia APVsport APV8000 Futura Prestige z ekranem 15,6 cala'),
    ('premium', 'APV8000 Premium Line', 'Ekran dotykowy Android 10,1", pas 145 x 58 cm.', 'Bieżnia APVsport APV8000 Premium Line'),
    ('top', 'APV8000 Top Quality', 'Ekran dotykowy Android 10,1", pas 145 x 58 cm.', 'Bieżnia APVsport APV8000 Top Quality'),
]
W8 = [('5 KM', '4 790', '6 790'), ('6 KM', '4 990', '7 290'), ('Wersja komercyjna', '5 590', '8 990')]
def karta8(img, nazwa, opis, alt):
    return (f'<article class="prod">{zdj(img, alt)}<div class="pin"><h3>{H.escape(nazwa)}</h3><p class="po">{H.escape(opis)}</p>'
            f'{wersje(W8)}<button type="button" class="btn dok" data-kosz>Dodaj do koszyka</button></div></article>')

MODELE = [
    ('apv6000', 'APV6000', 'Ekran dotykowy Android 10,1", silnik 6 KM, pas 135 x 48 cm, do 180 kg.', [('z zestawem dodatków', '6 490', None), ('APV6000 S', '5 690', None)], 'Bieżnia APVsport APV6000'),
    ('apv5000', 'APV5000', 'Ekran dotykowy Android 7", silnik 4,5 KM, pas 130 x 40 cm, do 160 kg.', [('z zestawem dodatków', '6 290', None), ('APV5000 S', '5 790', None)], 'Bieżnia APVsport APV5000'),
    ('apv900', 'APV900', 'Ekran LCD, silnik 4 KM, pas 130 x 38 cm, do 150 kg.', [('z zestawem dodatków', '4 385', None), ('APV900 S', '3 985', None)], 'Bieżnia APVsport APV900'),
    ('apv600', 'APV600', 'Ekran LCD, silnik 3,5 KM, pas 125 x 38 cm, do 140 kg.', [('z zestawem dodatków', '4 289', None), ('APV600 S', '3 885', None)], 'Bieżnia APVsport APV600'),
]
def kartam(img, nazwa, opis, ws, alt):
    return (f'<article class="prod">{zdj(img, alt)}<div class="pin"><h3>{H.escape(nazwa)}</h3><p class="po">{H.escape(opis)}</p>'
            f'{wersje(ws)}<p class="uw">Zestaw: masażer, hantle, przyrząd do brzuszków, mata.</p><p class="uw brak">Obecnie brak w magazynie</p><a class="btn dok" href="#kontakt">Zapytaj o termin</a></div></article>')

AKC = [
    ('zestaw', 'Zestaw dodatków do APV8000', 'Masażer, twister, 2 hantle, rama do brzuszków, wygłuszająca mata pod bieżnię i olej silikonowy.', '499', '800', 'Zestaw dodatków do bieżni APV8000: masażer, hantle, mata', False),
    ('pas', 'Pas piersiowy do pomiaru tętna', 'Telemetryczny pas na klatkę piersiową do bieżni APV8000 serii Premium Line, Top Quality i Futura Prestige.', '125', '139', 'Pas piersiowy telemetryczny do pomiaru tętna'),
]
def kartaa(img, nazwa, opis, c, o, alt, jest=True):
    kup = '<button type="button" class="btn dok" data-kosz>Dodaj do koszyka</button>' if jest else '<p class="uw brak">Obecnie brak w magazynie</p><a class="btn dok" href="#kontakt">Zapytaj o termin</a>'
    return (f'<article class="prod">{zdj(img, alt)}<div class="pin"><h3>{H.escape(nazwa)}</h3><p class="po">{H.escape(opis)}</p>'
            f'<p class="cena"><b>{c} zł</b><s>{o} zł</s></p>{kup}</div></article>')

s = s.replace('{{SERIE}}', '\n'.join(karta8(*x) for x in SERIE))
s = s.replace('{{MODELE}}', '\n'.join(kartam(*x) for x in MODELE))
s = s.replace('{{AKCESORIA}}', '\n'.join(kartaa(*x) for x in AKC))
assert '{{' not in s
open('index.html', 'w', encoding='utf-8').write(s)
print('ok', len(s))
