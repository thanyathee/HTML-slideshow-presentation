# Vector A4 "รายการใช้จ่ายเงิน" form used by slides 16-18 (camera zoom sequence)
# A4 canvas = 794 x 1123 px; the camera moves the whole sheet inside a fixed viewport.

COLS = [70, 58, 58, 68, 230, 60, 58, 56, 56]   # sums to 714 (page inner width)
NROWS = 15

SIG1 = 'M4 30 C10 6 18 6 16 26 C15 34 24 10 32 16 C38 22 34 30 44 18 C52 10 60 14 72 12'
SIG2 = 'M6 28 C14 4 26 2 22 22 C20 34 10 34 18 24 C30 12 40 20 46 16 C56 10 62 22 74 10'


def hw(text, d=None, cls=''):
    """handwritten value; d = animation delay (s) or None = already written"""
    if d is None:
        return '<span class="hw pre %s">%s</span>' % (cls, text)
    return '<span class="hw %s" style="--d:%.2fs">%s</span>' % (cls, d, text)


def sig(path, d=None):
    st = '' if d is None else ' style="--d:%.2fs"' % d
    pre = ' pre' if d is None else ''
    return '<svg class="sig%s"%s viewBox="0 0 80 36"><path d="%s"/></svg>' % (pre, st, path)


def field(label, val='', w=None):
    st = ' style="flex:%s"' % w if w else ''
    return '<div class="ff"%s><b>%s</b><span class="dl">%s</span></div>' % (st, label, val)


def page(mode):
    """mode: 'blank' (slide 16), 'head' (slide 17: header + first row written live),
       'rows' (slide 18: header/row1 pre-written, rows 2-6 written live)"""
    live = mode == 'head'
    H = (lambda t, d: hw(t, d if live else None)) if mode != 'blank' else (lambda t, d: '')
    t0 = 1.5  # header writing starts after the zoom-in lands
    hdr = (
        '<div class="fhead">'
        '<div class="flogo"><i></i><div><small>มูลนิธิทิสโก้ เพื่อการกุศล</small><b>TISCO FOUNDATION</b><small>www.tiscofoundation.org</small></div><i></i></div>'
        '<div class="ftitle"><b>รายการใช้จ่ายเงิน</b><span>ทุนการศึกษามูลนิธิทิสโก้ เพื่อการกุศล&nbsp; ประจำปี <span class="dl short">%s</span></span></div>'
        '</div>' % H('2566', t0)
    )
    rows = [
        [field('ชื่อผู้รับทุน', H('น.ส.ชมพู เรียนดี', t0 + .35), 2.2), field('ระดับชั้น', H('ม.5', t0 + .75), 1)],
        [field('โรงเรียน', H('ทิสโก้', t0 + 1.0), 2.2), field('จังหวัด', H('กรุงเทพฯ', t0 + 1.3), 1)],
        [field('ชื่ออาจารย์ผู้ดูแลทุน', H('คุณครูเพ็ญศรี ใจดี', t0 + 1.6), 1.45), field('เบอร์ติดต่ออาจารย์ผู้ดูแลทุน', H('099-999-9999', t0 + 2.0), 1.55)],
        [field('ยอดเงินคงเหลือในบัญชี', H('300', t0 + 2.4), 1.1), field('จำนวนเงินทุนที่ได้รับปีนี้', H('3,500', t0 + 2.7), 1.3), field('รวม', H('3,800', t0 + 3.0), .8)],
    ]
    fields = '<div class="ffields">' + ''.join('<div class="frow">%s</div>' % ''.join(r) for r in rows) + '</div>'

    # table body
    r1 = ['1/7/66', '3,500', '-', '3,800', 'ฝากเงินทุนปี 2566', '', '', '', '']
    body = []
    tr = 6.3  # slide 17: first table row is written after the camera pans down
    for i in range(NROWS):
        cells = [''] * 9
        if mode in ('head', 'rows') and i == 0:
            for k, v in enumerate(r1):
                if v:
                    cells[k] = hw(v, (tr + k * .22) if live else None)
        body.append(cells)
    if mode == 'rows':
        R = 1.2  # slide 18 writing starts once the cross-fade settles
        data = [
            (['15/7/66', '-', '500', '3,300', 'ซื้อชุดนักเรียน', '500', 'ชมพู'], ''),
            (['1/9/66', '-', '500', '2,800', 'อาหารกลางวัน กันยายน วันละ 30 บาท', '', ''], 'wide'),
            (['', '', '', '', '<i class="ind"></i>วันที่ 4-8 ก.ย. (5 วัน)', '150', 'ชมพู'], ''),
            (['', '', '', '', '<i class="ind"></i>วันที่ 11-15 ก.ย. (5 วัน)', '150', 'ชมพู'], ''),
            (['', '', '', '', 'ค่ารถโดยสาร วันละ 20 x 10 วัน', '200', 'ชมพู'], 'wide'),
        ]
        d = R
        for j, (vals, flag) in enumerate(data):
            cells = body[j + 1]
            for k, v in enumerate(vals):
                if v:
                    cells[k] = hw(v, d, 'wide' if (flag and k == 4) else '')
                    d += .12
            if vals[6]:
                cells[7] = sig(SIG1, d); d += .22
                cells[8] = sig(SIG2, d); d += .22
            d += .15
    th = ('<div class="ftr fth">'
          '<div class="c" style="grid-row:1/3">ว.ด.ป.</div><div class="c" style="grid-column:2/4">จำนวนเงิน</div>'
          '<div class="c" style="grid-row:1/3;grid-column:4">คงเหลือ</div><div class="c" style="grid-row:1/3;grid-column:5">รายการที่จ่าย</div>'
          '<div class="c" style="grid-row:1/3;grid-column:6">ราคา</div><div class="c sm" style="grid-row:1/3;grid-column:7">ลายเซ็น<br>นักเรียนทุน</div>'
          '<div class="c sm" style="grid-row:1/3;grid-column:8">ผู้ปกครอง<br>รับทราบ</div><div class="c sm" style="grid-row:1/3;grid-column:9">อ.ผู้ดูแลทุน<br>รับทราบ</div>'
          '<div class="c" style="grid-row:2;grid-column:2">ฝาก</div><div class="c" style="grid-row:2;grid-column:3">ถอน</div></div>')
    tb = ''.join('<div class="ftr">%s</div>' % ''.join('<div class="c">%s</div>' % v for v in r) for r in body)
    table = '<div class="ftable">' + th + tb + '</div>'
    warn = ('<div class="fwarn"><b>คำเตือน</b>กรุณาอ่านระเบียบปฏิบัติการใช้จ่ายเงินทุนเพื่อการศึกษาด้านหลังอย่างละเอียด<br>'
            'และต้องใช้แบบฟอร์มรายการใช้จ่ายเงินของมูลนิธิฯ เท่านั้น</div>'
            '<div class="ffoot"><span>หน้า 1</span><span>แก้ไขล่าสุด 04/10/2566</span></div>')
    return '<div class="a4 nw">' + hdr + fields + table + warn + '</div>'
