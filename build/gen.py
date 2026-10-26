import re,json,sys
sys.path.insert(0,__import__('os').path.dirname(__file__))
from form import page as a4page
src=open('/tmp/claude-0/build/index.v24.html').read()
secs=re.findall(r'<section class="slide".*?</section>',src,re.S)
qr=json.load(open('/tmp/claude-0/build/qr.json'))
SEC={2:'กำหนดการ',3:'ทุนการศึกษา',4:'ทุนการศึกษา',5:'ทุนการศึกษา',6:'เอกสาร',7:'เอกสาร',8:'เอกสาร',9:'การสมัคร',10:'การสมัคร',11:'การสมัคร',12:'ย้ายสถานศึกษา',13:'ประกาศผล',14:'ประกาศผล',15:'ข้อปฏิบัติ',16:'การใช้จ่าย',17:'การใช้จ่าย',18:'การใช้จ่าย',19:'การใช้จ่าย',20:'ใบเสร็จ',21:'ใบเสร็จ',22:'ใบเสร็จ',23:'ใบเสร็จ',24:'ใบเสร็จ'}
OLDMOOD={2:'blue',3:'blue',4:'navy',5:'navy',6:'blue',7:'blue',8:'navy',9:'navy',10:'blue',11:'warm',12:'green',13:'warm',14:'blue',15:'red',16:'navy',17:'blue',18:'blue',19:'blue',20:'green',21:'green',22:'red',23:'red',24:'red'}
KEYS={3:'grant',6:'docs',12:'move',13:'ann',15:'rules'}
out=[]   # (key, mood, html)
def eb(sec): return '<div class="eyebrow pop" style="--i:0"><i></i><b>%s</b><span>@@N@@ / @@T@@</span></div>'%sec
MONTHS=['พ.ย.','ธ.ค.','ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.','ม.ค.']
# (date, text, short label, start month idx, end idx, colour, white-text)
TRACKS=[
 dict(key='A',title='นักเรียนเรียนต่อสถานศึกษาเดิม',tag='รอบแรก',steps=[
  ('1 พฤศจิกายน – 31 มกราคม','สมัครขอรับทุน (ทุนใหม่ + ทุนต่อเนื่อง)','สมัครขอรับทุน',0,2,'blue',1),
  ('กุมภาพันธ์ – เมษายน','มูลนิธิพิจารณาใบสมัคร','พิจารณาใบสมัคร',3,5,'red',1),
  ('มิถุนายน','ประกาศรายชื่อผู้ได้รับทุนรอบแรก','ประกาศรายชื่อรอบแรก',7,7,'green',0),
  ('กรกฎาคม','มูลนิธิส่งตั๋วแลกเงินไปที่สถานศึกษา','ส่งตั๋วแลกเงินไปสถานศึกษา',8,8,'orange',0)]),
 dict(key='B',title='นักเรียนที่จะย้ายสถานศึกษา',tag='รอบรอฟังผล',steps=[
  ('1 พฤศจิกายน – 31 มกราคม','สมัครขอรับทุน (ทุนใหม่ + ทุนต่อเนื่อง)<br>กรอกในใบสมัครว่า <b class="em">ปีการศึกษาหน้าจะย้ายสถานศึกษา</b>','สมัครและแจ้งย้าย',0,2,'blue',1),
  ('มีนาคม – 31 กรกฎาคม','ส่งหลักฐานยืนยันการย้ายให้มูลนิธิ','ส่งหลักฐานยืนยันการย้าย',4,8,'red',1),
  ('สิงหาคม – ตุลาคม','มูลนิธิพิจารณาทุนรอบรอฟังผล<br>(เฉพาะผู้ที่ส่งหลักฐานยืนยันการย้ายสถานศึกษาแล้วเท่านั้น)','พิจารณารอบรอฟังผล',9,11,'orange',0),
  ('พฤศจิกายน','ประกาศรายชื่อผู้ได้รับทุนรอบรอฟังผล','ประกาศรายชื่อ',12,12,'green',0),
  ('ธันวาคม','มูลนิธิส่งตั๋วแลกเงินไปที่สถานศึกษา','ส่งตั๋วแลกเงินไปสถานศึกษา',13,13,'blue',1)])]
def mbar(a,b,c):
    return '<div class="mbar">'+''.join('<i%s></i>'%(' class="on"' if a<=k<=b else '') for k in range(15))+'</div>'
def sched(ti):
    T=TRACKS[ti];rows=''
    for k,(d,t,sh,a,b,c,w) in enumerate(T['steps']):
        hl=' hl' if 'ประกาศรายชื่อ' in t else ''
        tag='<span class="annchip">★</span>' if hl else ''
        rows+='<div class="srow pop%s" style="--i:%d"><span class="sn">%d</span><div class="sc"><span class="sd">%s</span><p%s>%s%s</p></div></div>'%(hl,k+1,k+1,d,(' class="nw"' if hl else (' class="ml"' if '<br>' in t else '')),tag,t)
    return '<section class="slide" data-t="slide" data-pos="after">\n    %s\n    <div class="rbanner r%s pop" style="--i:0"><div class="rw">%s</div><div class="rt">%s</div></div>\n    <div class="steps2">%s</div>\n  </section>'%(eb('กำหนดการ'),T['key'],T['title'],T['tag'],rows)
def gantt():
    rows=''
    for j,T in enumerate(TRACKS):
        ch=''
        for p,(d,t,sh,a,b,c,w) in enumerate(T['steps']):
            ch+='<div class="chev%s%s" style="--c:var(--%s)"><span class="stepn s">%d</span><b>%s</b><small>%s</small></div>'%(' first' if p==0 else '',' dk' if not w else '',c,p+1,sh,d)
        rows+='<div class="ov-row pop" style="--i:%d"><div class="ov-l"><span class="ab">%s</span><b>%s</b><em>%s</em></div><div class="ov-c">%s</div></div>'%(j+1,T['key'],T['title'],T['tag'],ch)
    return '<section class="slide" data-t="zoom" data-pos="after">\n    %s\n    <div class="trow pop" style="--i:0"><h2 class="title">ภาพรวมกำหนดการทั้งปี</h2><span class="loop">วนรอบใหม่ทุกปี</span></div>\n    <div class="ov">%s</div>\n  </section>'%(eb('กำหนดการ'),rows)
for i in range(1,24):
    x=secs[i]; n=i+1
    if n in (9,10): continue  # removed: write-form / online application detail slides
    if n==2:
        out.append(('sched','blue',sched(0)))
        out.append(('','navy',sched(1)))
        continue
    x=re.sub(r'<svg class="star".*?</svg>\s*','',x,flags=re.S)
    x=re.sub(r'(<section[^>]*>)',lambda m:m.group(1)+'\n    '+eb(SEC[n]),x,count=1)
    if n==3:
        x=x.replace('ประถมศึกษาปีที่ 5 จนถึงระดับปริญญาตรี','ประถมศึกษาปีที่ 5<br>จนถึงระดับปริญญาตรี')
        x=x.replace('มหาวิทยาลัยเอกชน และไม่เรียนภาคพิเศษ ภาคสมทบ','มหาวิทยาลัยเอกชน<br>และไม่เรียนภาคพิเศษ ภาคสมทบ')
        x=re.sub(r'<li>(.*?)</li>',lambda m:'<li><span>'+m.group(1)+'</span></li>',x)
        rowsA=[('ประถมศึกษาปีที่ 6',1000),('มัธยมศึกษาตอนต้น',3000),('มัธยมศึกษาตอนปลาย',3500),('ปวช.',7000),('ปวส. สาขาอื่นๆ',9000),('ปวส. สาขาอุตสาหกรรม',14000),('ปริญญาตรี',15000)]
        tbl='<div class="card amt pop" style="--i:2"><h3>ทุนการศึกษาต่อปี แต่ละระดับดังนี้</h3>'+''.join('<div class="arow"><span>%s</span><b class="hv" data-count="%d">{:,}</b></div>'.replace('{:,}','%s')%(l,v,format(v,',')) for l,v in rowsA)+'</div>'
        x=re.sub(r'<div class="card amt pop".*?</div>\s*</div>\s*</div>\s*</section>',lambda m:tbl+'\n    </div>\n  </section>',x,flags=re.S)
    if n==4:
        x=x.replace('<div class="two">','<div class="two l1">',1)
        x=x.replace('<p>สำหรับผู้ที่<b>ไม่เคยยื่นสมัคร</b>ขอรับทุนของมูลนิธิฯ มาก่อน หรือเป็นผู้ที่<b>เคยได้รับทุน</b>จากมูลนิธิฯ แล้วในปีก่อน แต่<b>ไม่ได้รับทุนในปีการศึกษาล่าสุดนี้</b></p>','<p>สำหรับผู้ที่<b>ไม่เคยยื่นสมัคร</b>ขอรับทุนของมูลนิธิฯ มาก่อน<br>หรือเป็นผู้ที่<b>เคยได้รับทุน</b>จากมูลนิธิฯ แล้วในปีก่อน<br>แต่<b>ไม่ได้รับทุนในปีการศึกษาล่าสุดนี้</b></p>')
        x=x.replace('<p>สำหรับผู้ขอทุนที่<b>ได้รับทุน</b>ของมูลนิธิฯ ในปีการศึกษาล่าสุดนี้ และประสงค์จะ<b>ขอรับทุนต่อเนื่องในปีการศึกษาต่อไป</b> ต้องยื่นแบบฟอร์มการขอรับทุนต่อเนื่องมายังมูลนิธิฯ ทุกปี</p>','<p>สำหรับผู้ขอทุนที่<b>ได้รับทุน</b>ของมูลนิธิฯ ในปีการศึกษาล่าสุดนี้<br>และประสงค์จะ<b>ขอรับทุนต่อเนื่องในปีการศึกษาต่อไป</b><br>ต้องยื่นแบบฟอร์มการขอรับทุนต่อเนื่องมายังมูลนิธิฯ ทุกปี</p>')
        x=x.replace('มอบทุนการศึกษาต่อเนื่อง ปีละ 1 ครั้ง โดยผู้ขอรับทุนจะต้องส่งแบบฟอร์มการขอรับทุนต่อเนื่องให้มูลนิธิทุกปี และต้องปฏิบัติตามระเบียบการใช้จ่ายเงินทุนการศึกษา จึงจะได้รับทุนการศึกษาต่อเนื่อง','มอบทุนการศึกษาต่อเนื่อง ปีละ 1 ครั้ง<br>โดยผู้ขอรับทุนจะต้องส่งแบบฟอร์มการขอรับทุนต่อเนื่องให้มูลนิธิทุกปี<br>และต้องปฏิบัติตามระเบียบการใช้จ่ายเงินทุนการศึกษา จึงจะได้รับทุนการศึกษาต่อเนื่อง')
        x=x.replace('<div><p>สำหรับ','<div><p class="nw">สำหรับ')
    if n==5:
        x=x.replace('<div class="two">','<div class="two l2">',1)
        x=re.sub(r'<ul class="bl"><li>พิจารณา.*?</li></ul>','<div class="cont">'+''.join('<span class="ln nw">%s</span>'%t for t in ['พิจารณาความครบถ้วนสมบูรณ์ของเอกสาร','การบันทึกรายการใช้จ่ายเงินทุนการศึกษา','รายการเดินบัญชีธนาคาร และใบเสร็จที่น่าเชื่อถือ','โดยเอกสารต้องมีความสอดคล้องกัน'])+'</div>',x,flags=re.S)
    if n==6:
        DOCS=[('แบบฟอร์มการขอรับทุนการศึกษา-ทุนใหม่','','1E0QsEzwqoGII7ZdYn0fVI0tbFmZlbKMP'),
        ('สำเนาบัตรประจำตัวประชาชนของผู้ขอรับทุน','',''),
        ('หนังสือรับรองสถานภาพการเป็นนักเรียน/นักศึกษา','',''),
        ('สำเนาผลการศึกษาเทอมล่าสุด','',''),
        ('รูปถ่ายสภาพบ้านที่อยู่อาศัย','',''),
        ('แบบฟอร์ม<br>“เขียนเล่าประวัติและสภาพความเป็นอยู่”','ยกเว้นระดับประถมศึกษาปีที่ 5','1iRyTIoz-zYIA11FyjEmqI3XHBs9SfTnG'),
        ('แบบฟอร์มรับรองสถานะการกู้ยืม กยศ./กรอ.<br>และการได้รับทุนการศึกษาอื่น','สำหรับระดับมัธยมศึกษาตอนปลาย<br>อาชีวศึกษา และปริญญาตรีเท่านั้น','1pGk5Rxvp8VcDgNputG_PXCLe-sk-kqGS'),
        ('จดหมายรับรองจากอาจารย์ที่ปรึกษา','เฉพาะระดับปริญญาตรีเท่านั้น','1LZu62vBiLPk5sxJEwYTYuoIFCKoaVfLh')]
        cards=''
        for k,(t,sub,fid) in enumerate(DOCS):
            inner='<svg class="chk" viewBox="0 0 60 60"><use href="#check"/></svg><span class="dt nw">%s%s</span>'%(t,('<small>%s</small>'%sub) if sub else '')
            if fid:
                cards+='<a class="card doc lnk pop" style="--i:%d" href="https://drive.google.com/file/d/%s/view" target="_blank" rel="noopener">%s<em class="ext" aria-hidden="true">↗</em></a>\n      '%(k+1,fid,inner)
            else:
                cards+='<div class="card doc pop" style="--i:%d">%s</div>\n      '%(k+1,inner)
        x=re.sub(r'<div class="docs">.*?</section>',lambda m:'<div class="docs d9">\n      '+cards+'</div>\n  </section>',x,flags=re.S)
        x=re.sub(r'<span class="tpill"[^>]*>ทุนใหม่</span>','<span class="newbig">ทุนใหม่</span>',x)
    if n==7:
        DOCS=[('แบบฟอร์มการขอรับทุนการศึกษา-ทุนต่อเนื่อง','','1E6UvDAav_k4fr3vUjWo1xMQg7iljlaCh'),
        ('สำเนาบัตรประจำตัวประชาชนของผู้ขอรับทุน','',''),
        ('หนังสือรับรองสถานภาพการเป็นนักเรียน/นักศึกษา','',''),
        ('สำเนาผลการศึกษาเทอมล่าสุด','',''),
        ('แบบฟอร์มรับรองสถานะการกู้ยืม กยศ./กรอ.<br>และการได้รับทุนการศึกษาอื่น','สำหรับระดับมัธยมศึกษาตอนปลาย<br>อาชีวศึกษา และปริญญาตรีเท่านั้น','1pGk5Rxvp8VcDgNputG_PXCLe-sk-kqGS'),
        ('สำเนาสมุดบัญชีเงินฝาก','หน้าที่แสดงชื่อเจ้าของบัญชี',''),
        ('สำเนาสมุดบัญชีเงินฝาก','หน้าที่แสดงรายการเดินบัญชีจำนวนเงินทุนในปีล่าสุด<br>ที่เข้าบัญชีจนถึงรายการปัจจุบัน',''),
        ('แบบฟอร์มรายการใช้จ่ายเงินทุนการศึกษา','','1E-gknKGFJaSOgHhfO4pATvLUPX0JOIoN'),
        ('ใบเสร็จรับเงิน ของการใช้จ่ายจากเงินทุนการศึกษาเท่านั้น','โดยเป็นรายการที่มีมูลค่าต่อรายการหรือต่อใบเสร็จตั้งแต่ 500 บาทขึ้นไป','')]
        cards=''
        for k,(t,sub,fid) in enumerate(DOCS):
            inner='<svg class="chk" viewBox="0 0 60 60"><use href="#check"/></svg><span class="dt nw">%s%s</span>'%(t,('<small>%s</small>'%sub) if sub else '')
            if fid:
                cards+='<a class="card doc lnk pop" style="--i:%d" href="https://drive.google.com/file/d/%s/view" target="_blank" rel="noopener">%s<em class="ext" aria-hidden="true">↗</em></a>\n      '%(k+1,fid,inner)
            else:
                cards+='<div class="card doc pop" style="--i:%d">%s</div>\n      '%(k+1,inner)
        x=re.sub(r'<div class="docs">.*?</section>',lambda m:'<div class="docs d9 d9b">\n      '+cards+'</div>\n  </section>',x,flags=re.S)
        x=re.sub(r'<span class="tpill"[^>]*>ทุนต่อเนื่อง</span>','<span class="newbig red">ทุนต่อเนื่อง</span>',x)
    if n==8:
        x=x.replace('การสมัครขอทุนการศึกษา','ข้อควรรู้ก่อนสมัครทุน')
        def r(cls,ic,t,i):
            return '<div class="card top %s pop" style="--i:%d"><svg class="chk" viewBox="0 0 60 60"><use href="#%s"/></svg><span class="nw">%s</span></div>'%(cls,i,ic,t)
        def c(cls,ic,t,i):
            return '<div class="card case %s pop" style="--i:%d"><svg class="chk" viewBox="0 0 60 60"><use href="#%s"/></svg><span class="nw">%s</span></div>'%(cls,i,ic,t)
        new9=('<div class="s9">'
          +r('no','cross','สมัครครั้งเดียว ได้รับทุนทุกปี',1)
          +r('ok','check','เป็น<em>ทุนต่อเนื่อง แต่ไม่ต่อให้อัตโนมัติ</em> ต้องยื่นสมัครทุนเข้ามาทุกปี',2)
          +'<div class="lblrow pop" style="--i:3"><div class="lblpill">การกู้ยืม กยศ. กรอ.</div><span>กองทุนเงินให้กู้ยืมเพื่อการศึกษา (กยศ.) และกองทุนเงินให้กู้ยืมที่ผูกกับรายได้ในอนาคต (กรอ.)</span></div>'
          +'<div class="cases">'
          +c('no','cross','นักเรียนที่<em>กำลังกู้ยืม</em><br>กยศ. กรอ. อยู่<br><em>ในปัจจุบัน</em>',4)
          +c('no','cross','นักเรียนที่<em>กำลังกู้ยืม</em><br>กยศ. กรอ. อยู่<br><em>แต่ปีการศึกษาหน้าไม่กู้ต่อ</em>',5)
          +c('ok','check','นักเรียนที่<em>จะยื่นกู้</em><br>กยศ. กรอ.<br><em>ในปีการศึกษาหน้า</em>',6)
          +'</div></div>')
        x=re.sub(r'<div class="rowsx">.*?</section>',lambda m:new9+'\n  </section>',x,flags=re.S)
    if n==11:
        def stp(i,who,t): return '<div class="hs"><i>%d</i><div><b class="chip %s">%s</b><span class="nw">%s</span></div></div>'%(i,'t' if who=='ครู' else 's',{'ครู':'ครูผู้ดูแลทุน','นร':'นักเรียน'}[who],t)
        L=''.join(stp(i+1,w,t) for i,(w,t) in enumerate([('ครู','ลงทะเบียนขอรหัสผ่านและเพิ่มชื่อสถานศึกษาในระบบ'),('นร','กรอกข้อมูล'),('ครู','อัพโหลดเอกสาร แล้วกดส่งข้อมูลให้มูลนิธิ')]))
        R=''.join(stp(i+1,w,t) for i,(w,t) in enumerate([('นร','กรอกข้อมูลในแบบฟอร์ม'),('ครู','รวบรวมเอกสารการขอรับทุน'),('ครู','ส่งให้มูลนิธิฯ ทางไปรษณีย์')]))
        ic1='<svg viewBox="0 0 48 48"><rect x="6" y="9" width="36" height="25" rx="4" fill="none" stroke="#fff" stroke-width="3.5"/><path d="M16 41h16M24 34v7" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/></svg>'
        ic2='<svg viewBox="0 0 48 48"><rect x="6" y="11" width="36" height="26" rx="4" fill="none" stroke="#fff" stroke-width="3.5"/><path d="M8 15l16 12 16-12" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        body=('<div class="lead pop" style="--i:1"><p class="nw l1b">เปิดรับสมัคร ตั้งแต่ <b>1 พฤศจิกายน – 31 มกราคม</b> ของทุกปี พร้อมกันทั้งทุนใหม่และทุนต่อเนื่อง</p>'
          '<p class="nw key">สมัครผ่านทางสถานศึกษาที่กำลังศึกษาอยู่ปัจจุบัน<u>เท่านั้น</u></p></div>'
          '<div class="how">'
          '<div class="hc blue pop" style="--i:2"><div class="hhead"><div class="hico">'+ic1+'</div><div class="ht"><h3>ระบบออนไลน์</h3><a class="url" href="https://scholarship.tiscofoundation.org" target="_blank" rel="noopener">scholarship.tiscofoundation.org</a></div></div><div class="hlist">'+L+'</div></div>'
          '<div class="hc red pop" style="--i:3"><div class="hhead"><div class="hico">'+ic2+'</div><div class="ht"><h3>เขียนแบบฟอร์มส่งทางไปรษณีย์</h3><span class="url">ดาวน์โหลด <a href="https://www.tiscofoundation.org" target="_blank" rel="noopener">tiscofoundation.org</a></span></div></div><div class="hlist">'+R+'</div></div>'
          '</div>'
          '<div class="ybar pop" style="--i:4">* เฉพาะผู้ขอรับทุนที่กำลังศึกษาอยู่ระดับปริญญาตรี สามารถรวบรวมเอกสารแล้วสมัครเองได้ 2 ช่องทาง *</div>')
        x=re.sub(r'<p class="note pop".*?</section>',lambda m:body+'\n  </section>',x,flags=re.S)
        x=re.sub(r'<span class="tpill"[^>]*>เลือกวิธีใดวิธีหนึ่ง</span>','<span class="pickpill">เลือกวิธีใดวิธีหนึ่ง</span>',x)
    if n==12:
        x=x.replace('น้องๆ ทั้งทุนใหม่และทุนต่อเนื่อง ที่กรอกข้อมูลตอนสมัครว่า จะย้าย/เปลี่ยนสถานศึกษาใหม่ในปีการศึกษาหน้า','<span class="wl nw">น้องๆ ทั้งทุนใหม่และทุนต่อเนื่อง ที่กรอกข้อมูล</span><span class="wl nw">ตอนสมัครว่า จะย้าย/เปลี่ยนสถานศึกษาใหม่</span><span class="wl nw">ในปีการศึกษาหน้า</span>')
        x=x.replace('<b>15 พ.ค.</b>','<b>15 พฤษภาคม</b>').replace('<b>31 ก.ค.</b>','<b>31 กรกฎาคม</b>')
        x=x.replace('<b>31 ม.ค.</b>ปิดรับสมัคร','<b>มีนาคม</b>แจ้งหน้าเพจ Facebook<br>ให้ส่งหลักฐาน')
    if n==13:
        ck='<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        def it(t,cls=''): return '<div class="ai %s"><i>%s</i><span class="nw">%s</span></div>'%(cls,ck,t)
        r1=it('นักเรียนที่กรอกข้อมูลว่า<br><b>เรียนต่อสถานศึกษาเดิม</b>')+it('นักเรียน <b class="lv"><lvl>ป.6</lvl><lvl>ม.3</lvl></b><br>ที่ส่งหลักฐานยืนยันการย้ายสถานศึกษาใหม่<br>ภายในวันที่ <b>15 พฤษภาคม</b>')
        r2=it('นักเรียน <b class="lv"><lvl>ป.6</lvl><lvl>ม.3</lvl><lvl>ม.6</lvl><lvl>ปวช.3</lvl><lvl>ปวส.2</lvl></b><br>ที่ส่งหลักฐานยืนยันการย้ายสถานศึกษาใหม่<br>ภายในวันที่ <b>31 กรกฎาคม</b>')
        body=('<div class="ann">'
          '<div class="ac a1 pop" style="--i:1"><div class="ah"><div class="hrow"><em>1</em><h3 class="nw">รอบแรก</h3></div><span class="mo">มิถุนายน</span></div><div class="al">'+r1+'</div></div>'
          '<div class="ac a2 pop" style="--i:2"><div class="ah"><div class="hrow"><em>2</em><h3 class="nw">รอบรอฟังผล</h3></div><span class="mo">พฤศจิกายน</span></div><div class="al">'+r2+'</div></div>'
          '</div>'
          '<div class="afoot pop" style="--i:3"><span class="nw">ติดตามประกาศรายชื่อได้ที่</span><b class="nw">tiscofoundation.org</b><span class="nw">และ</span><b class="nw">เพจ Facebook : TISCO Foundation</b></div>')
        x=re.sub(r'<div class="two rounds">.*?</section>',lambda m:body+'\n  </section>',x,flags=re.S)
    if n==14:
        I=lambda d:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">%s</svg>'%d
        ic=[I('<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/>'),
            I('<path d="M4 10v4h3l7 5V5L7 10H4z"/><path d="M17.5 9a4 4 0 010 6"/>'),
            I('<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>'),
            I('<rect x="2.5" y="6" width="19" height="12" rx="2.5"/><circle cx="12" cy="12" r="2.6"/><path d="M6 9.5v5M18 9.5v5"/>'),
            I('<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>'),
            I('<path d="M5 4h11a3 3 0 013 3v13H8a3 3 0 01-3-3z"/><path d="M5 17a3 3 0 013-3h11"/>')]
        st=[('#1D55C4','เช็กรายชื่อให้ชัวร์','','ชื่อ-สกุล สะกดถูกไหม<br>เปลี่ยนชื่อ-สกุลหรือเปล่า<br>สถานศึกษาตรงกับที่เรียนอยู่ปัจจุบันไหม<br><u>ข้อมูลผิด แจ้งมูลนิธิทันที!</u>'),
            ('#E8303A','รอฟังวันส่งเงินทุน','','มูลนิธิจะแจ้งวันส่ง<br>ตั๋วแลกเงิน / แคชเชียร์เช็ค<br>ที่เพจ Facebook <b>TISCO Foundation</b>'),
            ('#F07A12','ยังไม่ได้รับ?','2 สัปดาห์ – 1 เดือน','ถ้ายังไม่ได้รับ<br>ตั๋วแลกเงิน / แคชเชียร์เช็ค<br>เช็กที่ธุรการโรงเรียนก่อน<br>ถ้าไม่พบ <u>ติดต่อมูลนิธิทันที</u>'),
            ('#E8303A','ได้รับแล้ว รีบขึ้นเงิน!','อายุ 3 เดือน','ตั๋วแลกเงิน / แคชเชียร์เช็ค<br>มีอายุ 3 เดือน นับจากวันที่ที่ระบุไว้<br>ที่หน้าตั๋วแลกเงิน / แคชเชียร์เช็ค'),
            ('#12A87A','ใช้เงินแล้ว จดไว้ด้วย','','ลงบันทึกรายการค่าใช้จ่าย<br>เก็บใบเสร็จไว้แนบขอทุนต่อเนื่อง<br>ในปีถัดไป'),
            ('#1D55C4','สมุดบัญชีธนาคาร','','เก็บไว้ที่คุณครูผู้ดูแลทุน')]
        cards=''
        for k,(c,t,tag,b) in enumerate(st):
            tg='<span class="tk-tag nw">%s</span>'%tag if tag else ''
            cards+=('<div class="tk pop" style="--i:%d;--c:%s"><div class="tk-top"><em>%d</em><span class="tk-ic">%s</span>%s</div>'
                    '<h3 class="nw">%s</h3><p class="nw">%s</p></div>')%(k+1,c,k+1,ic[k],tg,t,b)
        body=('<div class="trow pop" style="--i:0"><h2 class="title">หลังจากประกาศรายชื่อ</h2><span class="tk-sub nw">ได้ทุนแล้ว ทำอะไรต่อ?</span></div>'
              '<div class="tkline"><div class="tkrail"></div><div class="tkrail r2"></div>'+cards+'</div>')
        x=re.sub(r'<div class="trow pop".*?</section>',lambda m:body+'\n  </section>',x,flags=re.S)
    if n==15:
        S=lambda d:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">%s</svg>'%d
        mk={'do':S('<path d="M5 12.5l4.5 4.5L19 7.5"/>'),'no':S('<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>'),'ca':S('<path d="M12 5v9"/><circle cx="12" cy="19" r=".6" fill="currentColor"/>')}
        G=lambda d:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">%s</svg>'%d
        HOUSE=G('<path d="M3.5 11L12 4l8.5 7"/><path d="M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/>')
        SCHOOL=G('<path d="M3 20h18"/><path d="M5 20V10l7-4 7 4v10"/><path d="M12 6V2.5l4 1.5-4 1.5"/><path d="M10 20v-4h4v4"/><circle cx="12" cy="11" r="1.6"/>')
        HOME2=G('<path d="M2.5 19l6-9 4 5.5 3-4 6 7.5z"/><circle cx="17.5" cy="6" r="2"/>')
        def place(ic,lab,cls=''): return '<span class="pl %s"><i>%s</i><small class="nw">%s</small></span>'%(cls,ic,lab)
        TRV=('<span class="ddtr">'
             '<span class="rt ok">'+place(HOUSE,'บ้าน')+'<span class="rd"><em class="nw">ไป-กลับ</em><u>'+mk['do']+'</u></span>'+place(SCHOOL,'')+'<b class="st nw">โรงเรียน</b></span>'
             '<span class="rt ng">'+place(HOUSE,'บ้าน')+'<span class="rd"><em class="nw">ไป-กลับ</em><u>'+mk['no']+'</u></span>'+place(HOME2,'')+'<b class="st nw">ภูมิลำเนา</b></span>'
             '</span>')
        cols=[('do','ต้องทำ','DO',[
                'ใช้เงินทุน<b>เฉพาะเรื่องการศึกษา</b><br>ของนักเรียน/นักศึกษาเท่านั้น<br>และใช้เฉพาะที่จำเป็น',
                'ใช้จ่ายเมื่อไร <b>บันทึกทันที</b><br>ใน “แบบฟอร์มรายการใช้จ่าย”<br>ผู้รับทุน ผู้ปกครอง และครูผู้ดูแลทุน<br>ต้องเซ็นรับทราบทุกรายการ',
                'ใช้จ่าย<b>ตั้งแต่ 500 บาทขึ้นไป</b><br>ต่อรายการหรือต่อใบเสร็จ<br>ต้องแนบใบเสร็จที่น่าเชื่อถือ']),
              ('no','ห้ามทำ',"DON'T",[
                '<b>สมัครใช้บัตร ATM</b>',
                '<b>เบิกเงินเป็นก้อนล่วงหน้านาน ๆ</b><br>แล้วนำไปใช้จ่ายภายหลัง<br>ควรเบิกเมื่อจำเป็นต้องใช้เท่านั้น',
                '<b>นำสมุดเงินฝากไปเก็บไว้เอง</b><br>หรือเก็บไว้ที่ผู้ปกครอง',
                '<b>นำเงินส่วนตัวหรือเงินครอบครัว</b><br>มาฝากหรือถอนร่วมกับ<br>บัญชีเงินทุนการศึกษา']),
              ('ca','ระวัง','CAREFUL',[
                'ได้รับตั๋วแลกเงิน / แคชเชียร์เช็ค<br><b>รีบนำไปฝากเข้าบัญชีทันที</b><br>มีอายุเพียง 3 เดือน นับจากวันที่<br>ที่ระบุบนตั๋วแลกเงิน / แคชเชียร์เช็ค<span class="ddw">หากเกินกำหนด<br>ถือว่าสละสิทธิ์รับทุนในปีนั้น</span>',
                '<b>ค่าเดินทาง</b>'+TRV])]
        h=''
        for j,(k,lab,en,items) in enumerate(cols):
            li=''.join('<div class="ddi"><i>%s</i><span class="nw">%s</span></div>'%(mk[k],t) for t in items)
            h+=('<div class="ddc dd-%s pop" style="--i:%d"><div class="ddh"><span class="ddic">%s</span><b class="nw">%s</b><small>%s</small></div><div class="ddl">%s</div></div>')%(k,j+1,mk[k],lab,en,li)
        body=('<div class="trow pop" style="--i:0"><h2 class="title">ข้อปฏิบัติและข้อห้ามของทุนต่อเนื่อง</h2><span class="tk-sub nw">อ่านให้ครบ ห้ามพลาด!</span></div>'
              '<div class="dd">'+h+'</div>')
        x=re.sub(r'<div class="trow pop".*?</section>',lambda m:body+'\n  </section>',x,flags=re.S)
    if n==16:
        G=lambda d,w='2.2':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round">%s</svg>'%(w,d)
        BOOK=G('<path d="M4 5.5A2.5 2.5 0 016.5 3H20v15H6.5A2.5 2.5 0 004 20.5z"/><path d="M4 20.5A2.5 2.5 0 016.5 23H20"/><path d="M9 8h7"/>')
        SHIRT=G('<path d="M8 3l4 2.5L16 3l5 3.5-2.5 4L17 9.5V21H7V9.5l-1.5 1L3 6.5z"/>')
        BUS=G('<rect x="4" y="3" width="16" height="15" rx="3"/><path d="M4 11h16M8 21v-3M16 21v-3"/><circle cx="8" cy="14.5" r=".8" fill="currentColor"/><circle cx="16" cy="14.5" r=".8" fill="currentColor"/>')
        LAP=G('<rect x="4" y="4.5" width="16" height="11" rx="2"/><path d="M2 19.5h20"/>')
        PIG=G('<path d="M4.5 12.5c0-3.6 3.4-6 7.5-6 1.6 0 3.1.3 4.3 1l2.2-1.5v3.2c.9.8 1.5 1.8 1.7 2.8H22v3h-1.9c-.5 1.2-1.4 2.2-2.6 2.9V21h-2.6v-1.9c-.9.2-1.9.3-2.9.3s-1.9-.1-2.7-.3V21H6.7v-2.8c-1.4-1.3-2.2-3-2.2-5.7z"/><path d="M10 8.5h3.5"/><circle cx="16.3" cy="11.3" r=".7" fill="currentColor"/><path d="M4.5 12.5c-1.2 0-2-.7-2-1.7"/>','2')
        CK=G('<path d="M5 12.5l4.5 4.5L19 7.5"/>','3.2'); NO=G('<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>','3.2')
        cats=[('เรื่องเรียน',BOOK,'#1D55C4',['*ค่าเทอม','ค่าเรียนพิเศษ / ค่าสมัครสอบ','ค่ากิจกรรม / ทัศนศึกษา / เข้าค่าย','หนังสือเรียน อุปกรณ์การเรียน','อุปกรณ์การเรียนช่าง / ทำโครงงาน','ถ่ายเอกสาร / พิมพ์งาน / เข้าเล่ม']),
              ('แต่งกาย & สุขภาพ',SHIRT,'#E8303A',['*ชุดนักเรียนนักศึกษา / ชุดพละ','ชุดลูกเสือเนตรนารี / รด. / ชุดพื้นเมือง','ตัดแว่นสายตา','ค่าตรวจสุขภาพ เพื่อมอบตัวเข้าศึกษาต่อ']),
              ('เดินทาง กิน อยู่',BUS,'#F07A12',['รถโดยสารจากบ้านไป-กลับโรงเรียน','ซื้อ/ซ่อม รถจักรยาน','อาหารกลางวัน','ค่าหอพักนักเรียน']),
              ('อุปกรณ์ไอที',LAP,'#7B4DE0',['เครื่องปริ้นเตอร์','คอมพิวเตอร์ / แล็ปท็อป / ไอแพด<em class="note"><i>หมายเหตุ</i>เฉพาะ ปวช. ปวส. ปริญญาตรี เท่านั้น</em>','อินเทอร์เน็ต<em class="note"><i>หมายเหตุ</i>ต้องแนบหลักฐานเท่านั้น</em>'])]
        cc=['','']
        for j,(lab,ic,c,its) in enumerate(cats):
            cc[(0,1,0,1)[j]]+='<div class="uc" style="--c:%s"><div class="uch"><i>%s</i><b class="nw">%s</b></div><div class="ucl">%s</div></div>'%(c,ic,lab,''.join(('<span class="nw hot">%s<sup>แนะนำ</sup></span>'%t[1:]) if t[0]=='*' else '<span class="nw">%s</span>'%t for t in its))
        bad=['ค่าเดินทางกลับภูมิลำเนา','เติมน้ำมันรถ','ซ่อมรถจักรยานยนต์','ซื้อโทรศัพท์ / จ่ายค่าโทรศัพท์','ข้าวสาร อาหารแห้ง ให้ครอบครัว','ค่าเช่าบ้าน ค่าน้ำ-ค่าไฟ ของที่บ้าน','ค่ายารักษาโรค / ค่ารักษาพยาบาล']
        bl=''.join('<div class="ubi"><i>%s</i><span class="nw">%s</span></div>'%(NO,t) for t in bad)
        body=('<div class="trow pop" style="--i:0"><h2 class="title">การใช้จ่ายเงินทุนการศึกษา</h2><div class="usave top"><span class="pig">%s</span><span class="svt"><b class="nw">ยังไม่ใช้ ไม่ต้องเบิก</b><span class="nw">ออมไว้ในบัญชีได้ <u>ไม่ถูกตัดทุน</u></span></span><em class="coin"></em></div></div>'
                            '<div class="ug">'
              '<div class="up ok pop" style="--i:2"><div class="uph"><span class="upi">%s</span><b class="nw">ใช้ได้</b><span class="upsub2 nw">ค่าใช้จ่ายเพื่อการเรียนเท่านั้น</span><!--%d--></div><div class="ucg">%s</div></div>'
              '<div class="up ng pop" style="--i:3"><div class="uph"><span class="upi">%s</span><b class="nw">ใช้ไม่ได้</b><small class="nw">ผิดวัตถุประสงค์</small></div><div class="ubl">%s</div></div>'
              '</div>'
              '<div class="uwarn bot pop" style="--i:4"><b class="nw">ระวัง!</b><span class="nw">ใช้จ่ายผิดวัตถุประสงค์ หรือแนบใบเสร็จที่ไม่น่าเชื่อถือ <u>จะถูกพิจารณาไม่ให้ทุนต่อเนื่อง</u></span></div>'
              '')%(PIG,CK,sum(len(c[3]) for c in cats),'<div class="ucc">'+cc[0]+'</div><div class="ucc">'+cc[1]+'</div>',NO,bl)
        x=re.sub(r'<div class="trow pop".*?</section>',lambda m:body+'\n  </section>',x,flags=re.S)
    if n in (17,18,19):
        x=re.sub(r'<section class="slide"[^>]*>',{17:'<section class="slide nofit fslide f16" data-t="cam" data-pos="after">',18:'<section class="slide nofit fslide f17" data-t="cam" data-pos="after">',19:'<section class="slide nofit fslide f18" data-t="cam" data-pos="after">'}[n],x,count=1)
        CHK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
        if n==17:
            mk='<span class="fmk m1">1</span><span class="fmk m2">2</span><span class="fmk m3">3</span>'
            side=('<div class="fside pop" style="--i:3">'
                  '<div class="fs-h"><b class="nw">ใช้แบบฟอร์มของมูลนิธิฯ เท่านั้น</b></div>'
                  '<div class="fs-i"><em>1</em><div><b class="nw">ส่วนหัว</b><span class="nw">ข้อมูลนักเรียน ครูผู้ดูแลทุน และยอดเงิน</span></div></div>'
                  '<div class="fs-i"><em>2</em><div><b class="nw">ตารางรายการใช้จ่าย</b><span class="nw">บันทึกทุกครั้งที่ฝาก-ถอน / ใช้จ่าย<br>นักเรียน ผู้ปกครอง ครูผู้ดูแลทุน เซ็นทุกรายการ</span></div></div>'
                  '<div class="fs-i fw3"><em>3</em><div><b class="nw">คำเตือน</b><span class="nw">อ่านระเบียบปฏิบัติการใช้จ่ายเงินทุน<br>ด้านหลังแบบฟอร์มอย่างละเอียด</span></div></div>'
                  '</div>')
            body=('<div class="trow pop" style="--i:0"><h2 class="title">แบบฟอร์มรายการใช้จ่ายเงิน</h2></div>'
                  '<div class="cam"><div class="a4w">'+a4page('blank').replace('<div class="a4 nw">','<div class="a4 nw">'+mk,1).replace('form2570.jpg','form2570s.jpg')+'</div>'+side+'</div>')
        elif n==18:
            body=('<div class="trow pop" style="--i:0"><h2 class="title">ตัวอย่างการกรอกแบบฟอร์ม</h2></div>'
                  '<div class="cam"><div class="a4w">'+a4page('head')+'</div>'
                  '<div class="fstep s1 nw"><em>1</em>กรอกข้อมูลส่วนหัวให้ครบ</div>'
                  '<div class="fstep s2 nw"><em>2</em>บรรทัดแรก บันทึกยอดฝากเงินทุน</div></div>')
        else:
            body=('<div class="trow pop" style="--i:0"><h2 class="title">ตัวอย่างการบันทึกรายการ</h2></div>'
                  '<div class="cam"><div class="a4w">'+a4page('rows')+'<div class="fhl"></div></div>'
                  '<div class="fco c1"><i>'+CHK+'</i><div><b class="nw">มีใบเสร็จ</b><span class="nw">ใช้จ่าย 500 บาทขึ้นไป<br>ต้องแนบใบเสร็จ</span></div></div>'
                  '<div class="fco c2"><i>!</i><div><b class="nw">ไม่มีใบเสร็จ</b><span class="nw">เขียนรายละเอียดให้ชัด<br>วันที่ จำนวนวัน ราคาต่อวัน</span></div></div>'
                  '<div class="fband nw">ตัวอย่างการบันทึกค่าอาหารกลางวันและค่ารถโดยสาร<br>จากบ้านไป-กลับโรงเรียน ที่ไม่มีใบเสร็จ</div></div>')
        x=re.sub(r'<div class="trow pop".*?</section>',lambda m:body+'\n  </section>',x,flags=re.S)
    x=x.replace('class="track pop"','class="ptrack pop"')
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
        <div class="card qr pop" style="--i:3"><div class="code">%(q2)s</div><div><b>เว็บไซต์มูลนิธิ</b><span>tiscofoundation.org</span></div></div>
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;500;600;700&family=Prompt:wght@400;500;600;700&family=Charm:wght@700&display=swap">
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
import hashlib
for f in ('assets/glass.css','assets/deck.css','assets/html2canvas.min.js','vendor/liquid-glass-js/container.js','vendor/liquid-glass-js/button.js','assets/bg.js','assets/deck.js'):
    v=hashlib.md5(open(f,'rb').read()).hexdigest()[:8]
    html=html.replace('"%s"'%f,'"%s?v=%s"'%(f,v))
open('index.html','w').write(html)
print(len(html), html.count('<section'))
