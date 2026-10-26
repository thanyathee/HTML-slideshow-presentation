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
