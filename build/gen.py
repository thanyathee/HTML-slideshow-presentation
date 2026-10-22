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
          '<div class="hc red pop" style="--i:3"><div class="hhead"><div class="hico">'+ic2+'</div><div class="ht"><h3>เขียนแบบฟอร์มส่งทางไปรษณีย์</h3><span class="url">ดาวน์โหลด <a href="https://www.tiscofoundation.org" target="_blank" rel="noopener">www.tiscofoundation.org</a></span></div></div><div class="hlist">'+R+'</div></div>'
          '</div>'
          '<div class="ybar pop" style="--i:4">* เฉพาะผู้ขอรับทุนที่กำลังศึกษาอยู่ระดับปริญญาตรี สามารถรวบรวมเอกสารแล้วสมัครเองได้ 2 ช่องทาง *</div>')
        x=re.sub(r'<p class="note pop".*?</section>',lambda m:body+'\n  </section>',x,flags=re.S)
        x=re.sub(r'<span class="tpill"[^>]*>เลือกวิธีใดวิธีหนึ่ง</span>','<span class="pickpill">เลือกวิธีใดวิธีหนึ่ง</span>',x)
    if n==12:
        x=x.replace('น้องๆ ทั้งทุนใหม่และทุนต่อเนื่อง ที่กรอกข้อมูลตอนสมัครว่า จะย้าย/เปลี่ยนสถานศึกษาใหม่ในปีการศึกษาหน้า','<span class="wl nw">น้องๆ ทั้งทุนใหม่และทุนต่อเนื่อง ที่กรอกข้อมูล</span><span class="wl nw">ตอนสมัครว่า จะย้าย/เปลี่ยนสถานศึกษาใหม่</span><span class="wl nw">ในปีการศึกษาหน้า</span>')
        x=x.replace('<b>31 ม.ค.</b>ปิดรับสมัคร','<b>มีนาคม</b>แจ้งให้ส่งหลักฐาน<br>/ หน้าเพจ Facebook')
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
import hashlib
for f in ('assets/glass.css','assets/deck.css','assets/html2canvas.min.js','vendor/liquid-glass-js/container.js','vendor/liquid-glass-js/button.js','assets/bg.js','assets/deck.js'):
    v=hashlib.md5(open(f,'rb').read()).hexdigest()[:8]
    html=html.replace('"%s"'%f,'"%s?v=%s"'%(f,v))
open('index.html','w').write(html)
print(len(html), html.count('<section'))
