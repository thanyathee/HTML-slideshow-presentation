# A4 "รายการใช้จ่ายเงิน" form (real page 1 of the 2570 PDF as background) + handwriting overlay.
# A4 canvas = 794 x 1123 px. Coordinates measured from the PDF render (scale 794/1414).
K = 794 / 1414
COLX = [67, 162, 274, 382, 512, 885, 1014, 1123, 1232, 1342]
ROWY0, ROWH = 655, 68.5          # first body row top, row height (display px)
SIG1 = 'M4 30 C10 6 18 6 16 26 C15 34 24 10 32 16 C38 22 34 30 44 18 C52 10 60 14 72 12'
SIG2 = 'M6 28 C14 4 26 2 22 22 C20 34 10 34 18 24 C30 12 40 20 46 16 C56 10 62 22 74 10'


def hw(text, d, live, cls=''):
    if not live:
        return '<span class="hw pre %s">%s</span>' % (cls, text)
    return '<span class="hw %s" style="--d:%.2fs">%s</span>' % (cls, d, text)


def sig(path, d, live):
    if not live:
        return '<svg class="sig pre" viewBox="0 0 80 36"><path d="%s"/></svg>' % path
    return '<svg class="sig" style="--d:%.2fs" viewBox="0 0 80 36"><path d="%s"/></svg>' % (d, path)


def at(cx, base, inner):
    """value centred on x, sitting on the underline at y (display px)"""
    return '<div class="fv" style="left:%.1fpx;top:%.1fpx">%s</div>' % (cx * K, base * K, inner)


def cell(r, c, inner, left=False, cls=''):
    x0, x1 = COLX[c] * K, COLX[c + 1] * K
    y0 = (ROWY0 + r * ROWH) * K
    return '<div class="fc%s %s" style="left:%.1fpx;top:%.1fpx;width:%.1fpx;height:%.1fpx">%s</div>' % (
        ' l' if left else '', cls, x0, y0, x1 - x0, ROWH * K, inner)


def page(mode):
    """'blank' (slide 16) | 'head' (slide 17, header+row1 written live) | 'rows' (slide 18)"""
    out = []
    if mode != 'blank':
        live = mode == 'head'
        t = 1.5
        hdr = [((1120, 212), '2566'), ((470, 298), 'น.ส.ชมพู เรียนดี'), ((1095, 298), 'ม.5'),
               ((460, 364), 'ทิสโก้'), ((1085, 364), 'กรุงเทพฯ'),
               ((485, 431), 'คุณครูเพ็ญศรี ใจดี'), ((1165, 431), '099-999-9999'),
               ((484, 498), '300'), ((992, 498), '3,500'), ((1247, 498), '3,800')]
        for k, ((x, y), v) in enumerate(hdr):
            out.append(at(x, y, hw(v, t + k * .32, live)))
        r1 = ['1/7/66', '3,500', '-', '3,800', 'ฝากเงินทุนปี 2566']
        tr = 6.3
        for c, v in enumerate(r1):
            out.append(cell(0, c, hw(v, tr + c * .22, live), left=(c == 4), cls=('dt' if c == 0 else '')))
    if mode == 'rows':
        d = 1.2
        data = [
            ['15/7/66', '-', '500', '3,300', 'ซื้อชุดนักเรียน', '500', 'ชมพู'],
            ['1/9/66', '-', '500', '2,800', 'อาหารกลางวัน กันยายน วันละ 30 บาท', '', ''],
            ['', '', '', '', '<i class="ind"></i>วันที่ 4-8 ก.ย. (5 วัน)', '150', 'ชมพู'],
            ['', '', '', '', '<i class="ind"></i>วันที่ 11-15 ก.ย. (5 วัน)', '150', 'ชมพู'],
            ['', '', '', '', 'ค่ารถโดยสาร วันละ 20 x 10 วัน', '200', 'ชมพู'],
        ]
        for j, vals in enumerate(data):
            r = j + 1
            for c, v in enumerate(vals):
                if v:
                    out.append(cell(r, c, hw(v, d, True, 'wide' if (c == 4 and len(v) > 22) else ''), left=(c == 4), cls=('dt' if c == 0 else '')))
                    d += .12
            if vals[6]:
                out.append(cell(r, 7, sig(SIG1, d, True))); d += .22
                out.append(cell(r, 8, sig(SIG2, d, True))); d += .22
            d += .15
    return '<div class="a4 nw"><img class="a4img" src="images/form2570.jpg" alt="แบบฟอร์มรายการใช้จ่ายเงิน">' + ''.join(out) + '</div>'
