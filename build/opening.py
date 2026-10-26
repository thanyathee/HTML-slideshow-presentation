# Two opening slides shown before the cover: formal title + playful animated school scene.

OPEN1 = '''<section class="slide opening op1 nofit" data-t="zoom" data-pos="active" data-mood="navy">
    <div class="opbg">
      <i class="ray r1"></i><i class="ray r2"></i><i class="ray r3"></i>
      <svg class="opwave" viewBox="0 0 1280 220" preserveAspectRatio="none"><path d="M0 120 C220 60 420 190 660 130 S1080 40 1280 110 V220 H0Z" fill="rgba(255,255,255,.06)"/><path d="M0 160 C260 110 470 220 720 170 S1100 110 1280 150 V220 H0Z" fill="rgba(255,255,255,.08)"/></svg>
    </div>
    <div class="opc">
      <span class="opline"></span>
      <h1 class="nw">มูลนิธิทิสโก้ เพื่อการกุศล</h1>
      <p class="nw">TISCO FOUNDATION</p>
      <span class="opline b"></span>
    </div>
  </section>'''

def _kid(x, shirt, skin, hair, bag, d, flip=False):
    sc = ' scale(-1,1)' if flip else ''
    return ('<g class="kid" style="--d:%ss" transform="translate(%d 0)%s"><g class="kb">'
            '<rect x="-30" y="440" width="60" height="70" rx="22" fill="%s" stroke="#0B2A6F" stroke-width="5"/>'
            '<rect x="-48" y="448" width="22" height="46" rx="10" fill="%s" stroke="#0B2A6F" stroke-width="5"/>'
            '<path d="M-14 508 v34 M14 508 v34" stroke="#0B2A6F" stroke-width="10" stroke-linecap="round"/>'
            '<circle cx="0" cy="398" r="44" fill="%s" stroke="#0B2A6F" stroke-width="5"/>'
            '<path d="M-44 392 C-44 350 44 340 44 392 C30 372 -10 362 -44 392Z" fill="%s" stroke="#0B2A6F" stroke-width="5" stroke-linejoin="round"/>'
            '<circle cx="-15" cy="402" r="5.5" fill="#0B2A6F"/><circle cx="15" cy="402" r="5.5" fill="#0B2A6F"/>'
            '<circle cx="-26" cy="416" r="7" fill="#FF8FB1" opacity=".7"/><circle cx="26" cy="416" r="7" fill="#FF8FB1" opacity=".7"/>'
            '<path d="M-9 420 Q0 430 9 420" fill="none" stroke="#0B2A6F" stroke-width="4" stroke-linecap="round"/>'
            '<path class="arm" d="M28 460 Q52 440 58 412" fill="none" stroke="#0B2A6F" stroke-width="9" stroke-linecap="round"/>'
            '</g></g>') % (d, x, sc, shirt, bag, skin, hair)

STICKERS = [
    # (left%, top%, rotate, delay, svg-inner, size)
    (6, 14, -12, 0, '<rect x="6" y="10" width="48" height="40" rx="6" fill="#2F6FED" stroke="#0B2A6F" stroke-width="4"/><path d="M30 10v40" stroke="#0B2A6F" stroke-width="4"/><path d="M12 20h12M12 28h12M36 20h12M36 28h12" stroke="#fff" stroke-width="3" stroke-linecap="round"/>', 86),
    (86, 12, 14, .6, '<path d="M30 4l7.6 15.4 17 2.5-12.3 12 2.9 16.9L30 42.8 14.8 50.8l2.9-16.9L5.4 21.9l17-2.5z" fill="#FFD23F" stroke="#0B2A6F" stroke-width="4" stroke-linejoin="round"/>', 82),
    (90, 52, -10, 1.2, '<path d="M30 52S6 37 6 21a12 12 0 0 1 24-4 12 12 0 0 1 24 4c0 16-24 31-24 31z" fill="#FF5A7A" stroke="#0B2A6F" stroke-width="4" stroke-linejoin="round"/>', 70),
    (4, 56, 10, .9, '<rect x="8" y="22" width="44" height="14" rx="3" transform="rotate(-35 30 29)" fill="#FF9A3D" stroke="#0B2A6F" stroke-width="4"/><path d="M14 46l-6 8 9-3" fill="#FFE2B8" stroke="#0B2A6F" stroke-width="3.5" stroke-linejoin="round"/>', 78),
    (76, 30, 8, .3, '<rect x="4" y="12" width="52" height="36" rx="10" fill="#fff" stroke="#0B2A6F" stroke-width="4"/><text x="30" y="39" text-anchor="middle" font-family="Prompt" font-weight="700" font-size="22" fill="#E8303A">A+</text>', 84),
    (18, 34, -8, 1.5, '<path d="M30 6v48M6 30h48M13 13l34 34M47 13L13 47" stroke="#2DD4A0" stroke-width="6" stroke-linecap="round"/>', 46),
]


def _stickers():
    out = ''
    for (l, t, r, d, inner, s) in STICKERS:
        out += ('<div class="stk" style="left:%s%%;top:%s%%;--r:%sdeg;--d:%ss;width:%dpx;height:%dpx">'
                '<svg viewBox="0 0 60 60">%s</svg></div>') % (l, t, r, d, s, s, inner)
    return out


SCHOOL = ('<g class="school">'
          '<rect x="470" y="300" width="340" height="250" rx="14" fill="#fff" stroke="#0B2A6F" stroke-width="6"/>'
          '<path d="M450 310 L640 200 L830 310Z" fill="#E8303A" stroke="#0B2A6F" stroke-width="6" stroke-linejoin="round"/>'
          '<circle cx="640" cy="262" r="26" fill="#FFD23F" stroke="#0B2A6F" stroke-width="5"/><path d="M640 248v14l9 6" stroke="#0B2A6F" stroke-width="4" stroke-linecap="round" fill="none"/>'
          '<path d="M640 200 V150" stroke="#0B2A6F" stroke-width="5"/><path class="flag" d="M640 150 h46 l-10 13 10 13 h-46z" fill="#2F6FED" stroke="#0B2A6F" stroke-width="4" stroke-linejoin="round"/>'
          '<rect x="500" y="340" width="70" height="56" rx="8" fill="#BFE8FC" stroke="#0B2A6F" stroke-width="5"/>'
          '<rect x="710" y="340" width="70" height="56" rx="8" fill="#BFE8FC" stroke="#0B2A6F" stroke-width="5"/>'
          '<rect x="500" y="420" width="70" height="56" rx="8" fill="#BFE8FC" stroke="#0B2A6F" stroke-width="5"/>'
          '<rect x="710" y="420" width="70" height="56" rx="8" fill="#BFE8FC" stroke="#0B2A6F" stroke-width="5"/>'
          '<rect x="600" y="430" width="80" height="120" rx="10" fill="#FF9A3D" stroke="#0B2A6F" stroke-width="5"/><circle cx="664" cy="492" r="5" fill="#0B2A6F"/>'
          '</g>')

OPEN2 = '''<section class="slide opening op2 nofit" data-t="zoom" data-pos="after" data-mood="blue">
    <div class="ksky"></div><div class="kbox">
      <div class="ksun"><i></i></div>
      <div class="kcloud c1"></div><div class="kcloud c2"></div><div class="kcloud c3"></div>
      ''' + _stickers() + '''
      <svg class="kscene" viewBox="0 0 1280 720" preserveAspectRatio="xMidYMax slice">
        <path d="M-400 548 C-120 530 120 520 260 540 C420 562 520 580 640 556 S1040 520 1280 552 C1420 566 1560 556 1680 548 V1000 H-400Z" fill="#7BD88F" stroke="#0B2A6F" stroke-width="6"/>
        <path d="M-400 606 C-100 596 160 592 300 600 C520 640 600 630 760 612 S1120 590 1280 606 C1440 618 1560 610 1680 604 V1000 H-400Z" fill="#54C474"/>
        ''' + SCHOOL + '''
        ''' + _kid(250, '#2F6FED', '#FFD9B8', '#3A2618', '#FFD23F', 0) + '''
        ''' + _kid(370, '#FF5A7A', '#F2C49B', '#14141F', '#2DD4A0', .35) + '''
        ''' + _kid(915, '#FFD23F', '#FFD9B8', '#6B3A1E', '#2F6FED', .7, True) + '''
        ''' + _kid(1035, '#2DD4A0', '#E8B48A', '#14141F', '#FF9A3D', .2, True) + '''
      </svg>
      <div class="ktitle">
        <h1 class="nw">มูลนิธิทิสโก้ เพื่อการกุศล</h1>
        <p class="nw">TISCO FOUNDATION</p>
      </div>
    </div>
  </section>'''


# ---------- v2: modern flat school scene (overrides OPEN2) ----------
def _kid2(x, y, s, skin, hair, girl, bag, d, wave=False, flip=False):
    sk = 'scale(%s,%s)' % (-s if flip else s, s)
    hairp = ('<path d="M-23 -128 C-24 -158 24 -158 23 -128 C23 -118 26 -100 20 -96 L16 -122 C8 -132 -8 -132 -16 -122 L-20 -96 C-26 -100 -23 -118 -23 -128Z" fill="%s"/>' % hair) if girl else \
            ('<path d="M-23 -126 C-24 -156 24 -156 23 -126 C14 -138 -6 -140 -23 -126Z" fill="%s"/>' % hair)
    bottom = ('<path d="M-22 -64 L22 -64 L28 -36 L-28 -36Z" fill="#1E3A8A"/>' if girl else
              '<rect x="-21" y="-64" width="42" height="26" rx="5" fill="#1E3A8A"/><rect x="-1.5" y="-50" width="3" height="12" fill="#152C6B"/>')
    arm_r = ('<g class="kwv" style="--d:%ss"><path d="M19 -96 Q34 -112 36 -134" stroke="%s" stroke-width="9" stroke-linecap="round" fill="none"/><circle cx="36" cy="-136" r="6" fill="%s"/></g>' % (d, skin, skin)) if wave else \
            ('<path d="M19 -96 Q28 -80 26 -66" stroke="%s" stroke-width="9" stroke-linecap="round" fill="none"/>' % skin)
    return ('<g transform="translate(%d %d)"><g transform="%s"><g class="kwk" style="--d:%ss">'
            '<ellipse cx="0" cy="2" rx="24" ry="5" fill="rgba(20,60,40,.18)"/>'
            '<rect x="-31" y="-104" width="20" height="40" rx="7" fill="%s"/>'
            '<path d="M-11 -38 v34 M11 -38 v34" stroke="%s" stroke-width="10" stroke-linecap="round"/>'
            '<path d="M-17 -2 h12 M5 -2 h12" stroke="#1F2937" stroke-width="7" stroke-linecap="round"/>'
            '%s'
            '<path d="M-21 -106 Q0 -112 21 -106 L22 -62 L-22 -62Z" fill="#FFFFFF"/>'
            '<path d="M-8 -108 L0 -98 L8 -108" fill="none" stroke="#CBD5E1" stroke-width="3"/>'
            '<rect x="6" y="-92" width="10" height="4" rx="2" fill="#2F6FED"/>'
            '<path d="M-19 -96 Q-28 -80 -26 -66" stroke="%s" stroke-width="9" stroke-linecap="round" fill="none"/>'
            '%s'
            '<circle cx="0" cy="-128" r="23" fill="%s"/>'
            '%s'
            '<circle cx="-8" cy="-127" r="3" fill="#1F2937"/><circle cx="8" cy="-127" r="3" fill="#1F2937"/>'
            '<circle cx="-14" cy="-119" r="4" fill="#FF8FA3" opacity=".6"/><circle cx="14" cy="-119" r="4" fill="#FF8FA3" opacity=".6"/>'
            '<path d="M-6 -117 Q0 -111 6 -117" fill="none" stroke="#1F2937" stroke-width="2.5" stroke-linecap="round"/>'
            '</g></g></g>') % (x, y, sk, d, bag, skin, bottom, skin, arm_r, skin, hairp)


def _tree(x, y, s, c1, c2, d):
    return ('<g transform="translate(%d %d) scale(%s)"><g class="ktr" style="--d:%ss">'
            '<rect x="-7" y="-70" width="14" height="72" rx="5" fill="#8B5A3C"/>'
            '<circle cx="0" cy="-110" r="52" fill="%s"/><circle cx="-34" cy="-82" r="34" fill="%s"/><circle cx="36" cy="-86" r="36" fill="%s"/>'
            '<circle cx="-12" cy="-128" r="26" fill="%s" opacity=".55"/>'
            '</g></g>') % (x, y, s, d, c1, c1, c2, c2)


def _cloud(x, y, s, cls):
    return ('<g class="kcl %s" transform="translate(%d %d) scale(%s)"><g class="kcli">'
            '<path d="M0 30 C-6 6 22 -4 34 10 C40 -16 84 -18 92 8 C112 2 124 22 116 30Z" fill="#fff" opacity=".95"/></g></g>') % (cls, x, y, s)


def _windows(x0, y0, cols, rows, dx, dy, w=34, h=30):
    o = ''
    for r in range(rows):
        for c in range(cols):
            o += '<rect x="%d" y="%d" width="%d" height="%d" rx="5" fill="#9ED8F7"/><rect x="%d" y="%d" width="%d" height="5" rx="2" fill="#fff" opacity=".7"/>' % (
                x0 + c * dx, y0 + r * dy, w, h, x0 + c * dx + 4, y0 + r * dy + 4, w - 18)
    return o


SCHOOL2 = ('<g class="k2school">'
           '<ellipse cx="640" cy="520" rx="330" ry="14" fill="rgba(20,60,40,.15)"/>'
           # wings
           '<rect x="330" y="350" width="200" height="170" rx="8" fill="#FFF3DC"/><rect x="750" y="350" width="200" height="170" rx="8" fill="#FFF3DC"/>'
           '<path d="M318 356 L540 356 L530 330 L328 330Z" fill="#E8503A"/><path d="M740 356 L962 356 L952 330 L750 330Z" fill="#E8503A"/>'
           + _windows(352, 372, 4, 2, 44, 58) + _windows(772, 372, 4, 2, 44, 58) +
           '<rect x="330" y="500" width="200" height="20" fill="#F2DDB6"/><rect x="750" y="500" width="200" height="20" fill="#F2DDB6"/>'
           # main block
           '<rect x="520" y="290" width="240" height="230" rx="10" fill="#FFF8EA"/>'
           '<path d="M500 300 L640 214 L780 300Z" fill="#E8503A"/><path d="M500 300 L780 300 L772 312 L508 312Z" fill="#C93A27"/>'
           '<circle cx="640" cy="262" r="24" fill="#fff"/><circle cx="640" cy="262" r="19" fill="#FFD23F"/>'
           '<path class="k2hand" d="M640 262 V249" stroke="#1F2937" stroke-width="3" stroke-linecap="round"/><path d="M640 262 L649 267" stroke="#1F2937" stroke-width="3" stroke-linecap="round"/>'
           + _windows(542, 330, 4, 2, 52, 56, 40, 32) +
           '<rect x="596" y="438" width="88" height="82" rx="8" fill="#2F6FED"/><rect x="600" y="442" width="38" height="78" rx="4" fill="#4C86F5"/><rect x="642" y="442" width="38" height="78" rx="4" fill="#4C86F5"/>'
           '<rect x="574" y="410" width="132" height="22" rx="6" fill="#1E3A8A"/><text x="640" y="426" text-anchor="middle" font-family="Sarabun" font-weight="700" font-size="15" fill="#fff">โรงเรียน</text>'
           '<path d="M580 520 h120 v8 h-120Z" fill="#E5D3B0"/>'
           # flag
           '<path d="M876 330 V214" stroke="#94A3B8" stroke-width="5" stroke-linecap="round"/><circle cx="876" cy="212" r="5" fill="#FFD23F"/>'
           '<g class="k2flag"><rect x="878" y="218" width="64" height="7" fill="#E8303A"/><rect x="878" y="225" width="64" height="7" fill="#fff"/><rect x="878" y="232" width="64" height="14" fill="#1E3A8A"/><rect x="878" y="246" width="64" height="7" fill="#fff"/><rect x="878" y="253" width="64" height="7" fill="#E8303A"/></g>'
           '</g>')

BUS = ('<g class="k2bus"><g transform="translate(70 560)">'
       '<ellipse cx="110" cy="66" rx="118" ry="8" fill="rgba(20,40,30,.2)"/>'
       '<rect x="0" y="0" width="220" height="60" rx="14" fill="#FFC531"/><rect x="0" y="40" width="220" height="10" fill="#F5A800"/>'
       '<rect x="190" y="8" width="26" height="26" rx="6" fill="#9ED8F7"/>'
       + ''.join('<rect x="%d" y="8" width="34" height="24" rx="5" fill="#9ED8F7"/>' % (12 + i * 44) for i in range(4)) +
       '<circle cx="48" cy="60" r="14" fill="#1F2937"/><circle cx="48" cy="60" r="6" fill="#CBD5E1"/>'
       '<circle cx="176" cy="60" r="14" fill="#1F2937"/><circle cx="176" cy="60" r="6" fill="#CBD5E1"/>'
       '<rect x="214" y="44" width="10" height="8" rx="3" fill="#FFF3B0"/>'
       '</g></g>')

BIRDS = ''.join('<path class="k2bird" style="--d:%ss;--y:%dpx" d="M0 0 q8 -8 16 0 q8 -8 16 0" fill="none" stroke="#1E3A8A" stroke-width="3" stroke-linecap="round" transform="translate(%d %d)"/>' % (d, y, x, y)
                for x, y, d in ((160, 150, 0), (196, 170, .4), (1040, 120, 1.1), (1080, 142, 1.5)))

SPARK = ''.join('<path class="k2sp" style="--d:%ss" d="M%d %d l4 10 10 4 -10 4 -4 10 -4 -10 -10 -4 10 -4z" fill="%s"/>' % (d, x, y, c)
                for x, y, c, d in ((250, 260, '#FFD23F', 0), (1010, 250, '#FF8FB1', .8), (1120, 380, '#FFD23F', 1.6), (160, 400, '#7DD3FC', 1.1)))

SCENE2 = ('<svg class="kscene2" viewBox="0 0 1280 720" preserveAspectRatio="xMidYMax meet">'
          '<defs><radialGradient id="k2sun"><stop offset="0" stop-color="#FFF6C9"/><stop offset=".35" stop-color="#FFE27A" stop-opacity=".9"/><stop offset="1" stop-color="#FFE27A" stop-opacity="0"/></radialGradient></defs>'
          '<circle class="k2sunglow" cx="1110" cy="120" r="150" fill="url(#k2sun)"/><circle cx="1110" cy="120" r="46" fill="#FFD84D"/>'
          + _cloud(120, 70, 1.1, 'a') + _cloud(820, 50, .9, 'b') + _cloud(420, 130, .7, 'c') + BIRDS + SPARK +
          '<path d="M-400 470 C-100 420 160 400 360 440 C560 480 700 410 900 420 C1100 430 1260 470 1680 440 V760 H-400Z" fill="#A7E3B9"/>'
          '<path d="M-400 500 C-60 470 220 470 420 492 C640 514 860 468 1080 480 C1260 490 1440 500 1680 488 V760 H-400Z" fill="#8BD6A2"/>'
          + _tree(250, 520, .9, '#46B26A', '#3A9C5B', 0) + _tree(1050, 520, 1, '#46B26A', '#3A9C5B', .7) + _tree(160, 530, .7, '#5CC57D', '#46B26A', 1.2) + _tree(1150, 530, .75, '#5CC57D', '#46B26A', .4) +
          SCHOOL2 +
          '<path d="M-400 520 C-100 510 200 512 640 520 C1000 528 1300 512 1680 518 V760 H-400Z" fill="#6CCB86"/>'
          '<path d="M520 528 C500 600 420 660 330 760 H950 C860 660 780 600 760 528Z" fill="#F4E4C1"/>'
          '<path d="M-400 600 C-100 590 240 610 420 606 L330 760 H-400Z M860 606 C1040 612 1300 596 1680 602 V760 H950Z" fill="#5BBE77"/>'
          + ''.join('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (x, y, r, c) for x, y, r, c in ((470, 528, 22, '#3FA45E'), (500, 532, 16, '#4CB86A'), (790, 528, 22, '#3FA45E'), (764, 532, 16, '#4CB86A'), (320, 524, 18, '#4CB86A'), (960, 524, 18, '#4CB86A'))) +
          ''.join('<circle cx="%d" cy="%d" r="4" fill="%s"/>' % (x, y, c) for x, y, c in ((470, 516, '#FF8FB1'), (488, 526, '#FFD23F'), (790, 516, '#FF8FB1'), (776, 526, '#fff'), (320, 514, '#FFD23F'), (960, 514, '#FF8FB1'))) +
          BUS +
          _kid2(450, 660, 1.0, '#F5C9A0', '#2B1B12', False, '#2F6FED', 0, wave=True) +
          _kid2(540, 690, 1.08, '#E8B48A', '#1A1A1A', True, '#FF5A7A', .3) +
          _kid2(740, 690, 1.08, '#F5C9A0', '#3A2618', True, '#2DD4A0', .6, flip=True) +
          _kid2(835, 662, 1.0, '#D9A27A', '#1A1A1A', False, '#FF9A3D', .15, wave=True, flip=True) +
          _kid2(1010, 640, .9, '#F5C9A0', '#2B1B12', False, '#FFD23F', .45, wave=True, flip=True) +
          '</svg>')

OPEN2 = '''<section class="slide opening op2 v2 nofit" data-t="zoom" data-pos="after" data-mood="blue">
    <div class="ksky"></div><div class="kbox">
      ''' + SCENE2 + '''
      <div class="ktitle">
        <h1 class="nw">มูลนิธิทิสโก้ เพื่อการกุศล</h1>
        <p class="nw">TISCO FOUNDATION</p>
      </div>
    </div>
  </section>'''
