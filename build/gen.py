import re,json
src=open('/tmp/claude-0/build/index.v24.html').read()
secs=re.findall(r'<section class="slide".*?</section>',src,re.S)
qr=json.load(open('/tmp/claude-0/build/qr.json'))
SEC={2:'กำหนดการ',3:'ทุนการศึกษา',4:'ทุนการศึกษา',5:'ทุนการศึกษา',6:'เอกสาร',7:'เอกสาร',8:'เอกสาร',9:'การสมัคร',10:'การสมัคร',11:'การสมัคร',12:'ย้ายสถานศึกษา',13:'ประกาศผล',14:'ประกาศผล',15:'ข้อปฏิบัติ',16:'การใช้จ่าย',17:'การใช้จ่าย',18:'การใช้จ่าย',19:'การใช้จ่าย',20:'ใบเสร็จ',21:'ใบเสร็จ',22:'ใบเสร็จ',23:'ใบเสร็จ',24:'ใบเสร็จ'}
OLDMOOD={2:'blue',3:'blue',4:'navy',5:'navy',6:'blue',7:'blue',8:'navy',9:'navy',10:'blue',11:'warm',12:'green',13:'warm',14:'blue',15:'red',16:'navy',17:'red',18:'navy',19:'navy',20:'green',21:'green',22:'red',23:'red',24:'red'}
KEYS={3:'grant',6:'docs',12:'move',13:'ann',15:'rules'}
out=[]   # (key, mood, html)
def eb(sec): return '<div class="eyebrow pop" style="--i:0"><i></i><b>%s</b><span>@@N@@ / @@T@@</span></div>'%sec
MONTHS=['พ.ย.','ธ.ค.','ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.','ม.ค.']
EV=[ # (date, text, short, start, end, color, white-text)
 ('1 พ.ย. – 31 ม.ค.','สมัครขอรับทุนการศึกษา ทั้งทุนใหม่และทุนต่อเนื่อง','สมัครขอรับทุน',0,2,'blue',1),
 ('ก.พ. – เม.ย.','มูลนิธิดำเนินการพิจารณาใบสมัครทุนการศึกษา','มูลนิธิพิจารณาใบสมัคร',3,5,'red',1),
 ('มี.ค. – 31 ก.ค.','ผู้ที่กรอกว่าปีการศึกษาหน้าจะย้ายสถานศึกษา ส่งหลักฐานยืนยันให้มูลนิธิ','ส่งหลักฐานย้ายสถานศึกษา',4,8,'green',0),
 ('มิถุนายน','ประกาศรายชื่อผู้ได้รับทุนรอบแรก ป.6 ม.3 ที่ส่งหลักฐานภายใน 15 พ.ค. มูลนิธิส่งตั๋วแลกเงินไปที่สถานศึกษา','ประกาศรายชื่อรอบแรก',7,7,'blue',1),
 ('31 กรกฎาคม','ปิดรับหลักฐานแจ้งย้ายสถานศึกษาทุกระดับชั้น ป.6 ม.3 ม.6 ปวช.3 ปวส.2','ปิดรับหลักฐานย้าย',8,8,'red',1),
 ('ส.ค. – ต.ค.','มูลนิธิพิจารณาทุนรอบรอฟังผล กลุ่มที่ส่งหลักฐานยืนยันการย้ายสถานศึกษา','พิจารณารอบรอฟังผล',9,11,'orange',0),
 ('พฤศจิกายน','ประกาศรายชื่อผู้ได้รับทุนรอบรอฟังผล ที่ส่งหลักฐานภายใน 31 ก.ค.','ประกาศรายชื่อรอบรอฟังผล',12,12,'blue',1),
 ('ธันวาคม','มูลนิธิส่งตั๋วแลกเงินรอบรอฟังผลไปที่สถานศึกษา','ส่งตั๋วแลกเงินรอบรอฟังผล',13,13,'red',1),
 ('1 พ.ย. – 31 ม.ค.','เปิดรับสมัครทุนการศึกษาปีถัดไป','เปิดรับสมัครปีถัดไป',12,14,'blue',1)]
def mbar(a,b,c):
    return '<div class="mbar">'+''.join('<i%s></i>'%(' class="on"' if a<=k<=b else '') for k in range(15))+'</div>'
def sched(part,idxs,title):
    cards=''
    for j,k in enumerate(idxs):
        d,t,sh,a,b,c,w=EV[k]
        cards+='<div class="card ev3 pop" style="--i:%d;--c:var(--%s)"><span class="stepn">%d</span><span class="badge%s big">%s</span><p>%s</p>%s</div>'%(j+1,c,k+1,' w' if w else '',d,t,mbar(a,b,c))
    return '<section class="slide" data-t="slide" data-pos="after">\n    %s\n    <div class="trow pop" style="--i:0"><h2 class="title">กำหนดการ <small>ช่วงที่ %d / 3</small> %s</h2></div>\n    <div class="ev3row">%s</div>\n  </section>'%(eb('กำหนดการ'),part,title,cards)
def gantt():
    head='<div class="gt-head"><span class="gt-yr y1" style="left:0;width:%.4f%%">ปีนี้</span><span class="gt-yr y2" style="left:%.4f%%;right:0">ปีถัดไป</span></div><div class="gt-head gt-months">'%(12/15*100,12/15*100)
    head+=''.join('<span class="%s">%s</span>'%('nx' if k>=12 else '',m) for k,m in enumerate(MONTHS))+'</div>'
    rows=''
    for k,(d,t,sh,a,b,c,w) in enumerate(EV):
        left=a/15*100; width=(b-a+1)/15*100
        lab='<span class="gt-t %s" style="%s"><b>%s</b><small>%s</small></span>'
        if b<=9: pos='left:calc(%.4f%% + 12px)'%((b+1)/15*100); cls='r'
        else: pos='right:calc(%.4f%% + 12px)'%((14-b+0)/15*100+ (14-a+1-(b-a+1))/15*100*0 + 100/15*0 + 0) ; cls='l'
        if b>9: pos='right:calc(%.4f%% + 12px)'%((15-a)/15*100); 
        rows+='<div class="gt-row"><span class="stepn s" style="--c:var(--%s)">%d</span><div class="gt-area"><div class="gt-bar%s" style="left:%.4f%%;width:%.4f%%;--c:var(--%s)"></div>%s</div></div>'%(c,k+1,' dot' if a==b else '',left,width,c,lab%(cls,pos,sh,d))
    return '<section class="slide" data-t="zoom" data-pos="after">\n    %s\n    <div class="trow pop" style="--i:0"><h2 class="title">ภาพรวมกำหนดการทั้งปี</h2><span class="loop">วนรอบใหม่ทุกปี</span></div>\n    <div class="gantt card pop" style="--i:1"><div class="gt-top">%s</div>%s</div>\n  </section>'%(eb('กำหนดการ'),'',head+rows)
for i in range(1,24):
    x=secs[i]; n=i+1
    if n==2:
        out.append(('sched','blue',sched(1,[0,1,2],'สมัครและพิจารณา')))
        out.append(('','navy',sched(2,[3,4,5],'ประกาศรอบแรก')))
        out.append(('','warm',sched(3,[6,7,8],'รอบรอฟังผล')))
        out.append(('','blue',gantt()))
        continue
    x=re.sub(r'<svg class="star".*?</svg>\s*','',x,flags=re.S)
    x=re.sub(r'(<section[^>]*>)',lambda m:m.group(1)+'\n    '+eb(SEC[n]),x,count=1)
    if n==17:
        x=re.sub(r'<svg class="bob".*?</svg>','<div class="alert" aria-hidden="true">!</div>',x,flags=re.S)
    out.append((KEYS.get(n,''),OLDMOOD[n],x))
def ico(p): return '<svg viewBox="0 0 24 24">%s</svg>'%p
contact='''<section class="slide" data-t="zoom" data-pos="after">
    <div class="eyebrow pop" style="--i:0"><i></i><b>ติดต่อ</b><span>@@N@@ / @@T@@</span></div>
    <div class="trow pop" style="--i:0"><h2 class="title">ติดต่อมูลนิธิทิสโก้ เพื่อการกุศล</h2></div>
    <div class="contact">
      <div class="cinfo">
        <div class="card crow pop" style="--i:1"><span class="ico" style="--c:var(--yellow)">%(pin)s</span><div><small>ที่อยู่</small>48/4 อาคารทิสโก้ทาวเวอร์ ชั้น 1 ถนนสาทรเหนือ แขวงสีลม เขตบางรัก กรุงเทพฯ 10500</div></div>
        <div class="card crow pop" style="--i:2"><span class="ico" style="--c:var(--green)">%(tel)s</span><div><small>โทรศัพท์</small><b>02 633 7501-7</b>02 638 0554</div></div>
        <div class="card crow pop" style="--i:3"><span class="ico" style="--c:var(--orange)">%(mail)s</span><div><small>อีเมล</small><b>tiscofoundation@tiscofoundation.org</b></div></div>
        <div class="card crow pop" style="--i:4"><span class="ico" style="--c:var(--acc)">%(fb)s</span><div><small>Facebook</small><b>TISCO Foundation</b>facebook.com/tiscofoundation</div></div>
      </div>
      <div class="qrs">
        <div class="card qr pop" style="--i:2"><div class="code">%(q1)s</div><div><b>สมัครทุนออนไลน์</b><span>scholarship.tiscofoundation.org</span></div></div>
        <div class="card qr pop" style="--i:3"><div class="code">%(q2)s</div><div><b>เว็บไซต์มูลนิธิ</b><span>www.tiscofoundation.org</span></div></div>
        <div class="card qr pop" style="--i:4"><div class="code">%(q3)s</div><div><b>Facebook</b><span>facebook.com/tiscofoundation</span></div></div>
      </div>
    </div>
  </section>'''%dict(
 pin=ico('<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>'),
 tel=ico('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>'),
 mail=ico('<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M3.5 7l8.5 6 8.5-6"/>'),
 fb=ico('<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8.5c0-.3.2-.5.5-.5z"/>'),
 q1=qr['scholarship'],q2=qr['website'],q3=qr['facebook'])
out.append(('contact','cover',contact))
def idx(key): return [o[0] for o in out].index(key)+2   # 1-based slide number incl. cover
AG=[('sched','blue','กำหนดการ'),('grant','red','ทุนการศึกษา'),('docs','yellow','เอกสารและการสมัคร'),('move','orange','ย้ายสถานศึกษา'),('ann','green','ประกาศผล'),('rules','red','ข้อปฏิบัติและการใช้จ่าย'),('contact','blue','ติดต่อมูลนิธิ')]
agenda=''.join('<button data-go="%d" style="--c:var(--%s)"><i></i>%s<span>%d</span></button>'%(idx(k)-1,c,t,idx(k)) for k,c,t in AG)
cover='''<section class="slide cover" data-t="zoom" data-pos="active" data-mood="cover">
    <div class="cover-grid">
      <div>
        <div class="kicker pop" style="--i:0"><i></i>มูลนิธิทิสโก้ เพื่อการกุศล</div>
        <h1 class="pop" style="--i:1">คู่มือสำหรับ<br>สถานศึกษา</h1>
        <p class="sub pop" style="--i:2">เพื่อใช้ชี้แจงให้นักเรียนทุน</p>
        <span class="org pop" style="--i:3">TISCO Foundation</span>
      </div>
      <nav class="card agenda pop" style="--i:3"><h3>สารบัญ</h3>'''+agenda+'''</nav>
    </div>
  </section>'''
final=[cover]
for k,m,h in out:
    final.append(h.replace('<section class="slide"','<section class="slide" data-mood="%s"'%m,1))
T=len(final)
final=[h.replace('@@N@@',str(i+1)).replace('@@T@@',str(T)) for i,h in enumerate(final)]
html='''<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>สไลด์คู่มือทุนการศึกษา</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;500;600;700&family=Prompt:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/glass.css">
<link rel="stylesheet" href="assets/deck.css">
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<symbol id="check" viewBox="0 0 60 60"><circle cx="30" cy="30" r="26" fill="#2DD4A0"/><path d="M17 31l9 9 18-20" fill="none" stroke="#06133F" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="cross" viewBox="0 0 60 60"><circle cx="30" cy="30" r="26" fill="#FF5A64"/><path d="M20 20l20 20M40 20L20 40" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round"/></symbol>
</defs></svg>
<div id="bg"></div><div class="veil"></div><div class="progress"><i></i></div>
<div class="deck" id="deck">
<div class="area" id="area">
<div class="stage" id="stage">
<div class="brand">TISCO FOUNDATION</div>
<div id="zoom" hidden><img alt=""></div>
%s
</div>
</div>
</div>
<div id="dock"></div><div id="fsWrap"></div>
<div class="fallback-dock" id="fbDock"><button data-a="prev" type="button" aria-label="หน้าก่อนหน้า"><svg viewBox="0 0 32 32"><path d="M27 16H6M14 7L5 16l9 9"/></svg></button><span>1 / %d</span><button data-a="next" type="button" aria-label="หน้าถัดไป"><svg viewBox="0 0 32 32"><path d="M5 16h21M18 7l9 9-9 9"/></svg></button></div>
<button class="fallback-dock fallback-fs" id="fbFs" type="button" style="width:48px;height:48px;padding:0;border-radius:50%%;place-items:center;background:rgba(255,255,255,.16)"><svg viewBox="0 0 32 32" style="width:22px;height:22px;fill:none;stroke:#fff;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round"><path d="M4 12V4h8M20 4h8v8M28 20v8h-8M12 28H4v-8"/></svg></button>
<script src="assets/html2canvas.min.js"></script>
<script src="vendor/liquid-glass-js/container.js"></script>
<script src="vendor/liquid-glass-js/button.js"></script>
<script src="assets/bg.js"></script>
<script src="assets/deck.js"></script>
</body>
</html>
'''%('\n  '.join(final),T)
# confetti canvas: add to the announce slide
html=html.replace('<canvas class="confetti" id="conf" width="1270" height="710"></canvas>','<canvas class="confetti" id="conf" width="1280" height="720"></canvas>')
open('index.html','w').write(html)
print(len(html), html.count('<section'))
