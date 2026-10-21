(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var stage=document.getElementById('stage'),area=document.getElementById('area'),deck=document.getElementById('deck');
  var zoom=document.getElementById('zoom'),zimg=zoom.querySelector('img');
  var prog=document.querySelector('.progress i');
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var lite=/[?&]lite/.test(location.search)||(navigator.hardwareConcurrency||8)<=2||(navigator.deviceMemory||8)<=2;
  if(lite)document.documentElement.classList.add('lite');
  var cur=0,token=0,timers=[],N=slides.length;
  var CHART=slides.findIndex(function(s){return s.querySelector('[data-count]')}),CONFETTI=slides.findIndex(function(s){return s.querySelector('#conf')});
  var MOODS=slides.map(function(s){return s.dataset.mood||'blue'});
  var ICON={
    prev:'<svg viewBox="0 0 32 32"><path d="M27 16H6M14 7L5 16l9 9"/></svg>',
    next:'<svg viewBox="0 0 32 32"><path d="M5 16h21M18 7l9 9-9 9"/></svg>',
    fs:'<svg viewBox="0 0 32 32"><path d="M4 12V4h8M20 4h8v8M28 20v8h-8M12 28H4v-8"/></svg>'
  };
  var fsLabel=document.fullscreenEnabled?'เต็มจอ':'เปิดเต็มหน้าจอในแท็บใหม่';

  function fit(){var r=area.getBoundingClientRect();var s=Math.min(r.width/1280,r.height/720);stage.style.transform='translate(-50%,-50%) scale('+s+')'}
  if(window.ResizeObserver)new ResizeObserver(fit).observe(area);window.addEventListener('resize',fit);fit();


  /* Thai word-aware line breaking: put <wbr> between dictionary words so lines never split mid-word */
  (function(){
    if(!window.Intl||!Intl.Segmenter)return;
    var sg=new Intl.Segmenter('th',{granularity:'word'}),th=/[\u0E00-\u0E7F]/;
    var w=document.createTreeWalker(stage,NodeFilter.SHOW_TEXT,{acceptNode:function(n){
      var p=n.parentNode;if(!p||/^(SCRIPT|STYLE|CANVAS)$/.test(p.nodeName)||!th.test(n.nodeValue)||p.closest('.gantt,.mlab,.legend,.badge'))return NodeFilter.FILTER_REJECT;return NodeFilter.FILTER_ACCEPT}});
    var list=[],n;while(n=w.nextNode())list.push(n);
    list.forEach(function(t){
      var d=getComputedStyle(t.parentNode).display;
      if(/flex|grid/.test(d)){var sp=document.createElement('tw');t.parentNode.replaceChild(sp,t);sp.appendChild(t);}
      var f=document.createDocumentFragment(),first=true,prev='';
      for(var x of sg.segment(t.nodeValue)){
        if(!first&&x.isWordLike!==false&&!/^\s/.test(x.segment)&&!/[.\u0E2F]$/.test(prev))f.appendChild(document.createElement('wbr'));
        f.appendChild(document.createTextNode(x.segment));first=false;prev=x.segment;
      }
      t.parentNode.replaceChild(f,t);
    });
  })();


  /* Fill the slide: scale each slide's content up (never down) until it uses the available width and height */
  function fillSlides(){
    var PADX=72,PADY=38;
    slides.forEach(function(s){
      if(s.classList.contains('cover'))return;
      var w=s.querySelector(':scope>.fit');
      if(!w){
        w=document.createElement('div');w.className='fit';
        [].slice.call(s.childNodes).forEach(function(c){if(!(c.nodeType===1&&c.classList.contains('confetti')))w.appendChild(c)});
        s.appendChild(w);
      }
      var W=1280-PADX,H=720-PADY,lo=1,hi=1.32,k=1;
      function ok(x){w.style.width=(W/x)+'px';return w.offsetHeight*x<=H}
      if(ok(hi))k=hi;else{for(var i=0;i<9;i++){var m=(lo+hi)/2;if(ok(m)){k=m;lo=m}else hi=m}k=lo}
      w.style.width=(W/k)+'px';w.style.height='auto';w.style.minHeight=(H/k)+'px';w.style.transform='scale('+k+')';
    });
  }
  window.deckFill=fillSlides;

  var counts=[];
  function setCount(){counts.forEach(function(c){c.textContent=(cur+1)+' / '+N})}
  function clear(){token++;timers.forEach(clearTimeout);timers=[];stopConf()}
  function applyGroup(s,g,anim){
    var tr=s.querySelector('.track');if(!tr)return;
    tr.style.transition=anim?'':'none';tr.style.setProperty('--g',g);
    [].forEach.call(tr.children,function(c,i){c.style.transition=anim?'':'none';c.classList.toggle('dim',Math.floor(i/3)!==g)});
    [].forEach.call(s.querySelectorAll('.mg'),function(m){m.classList.toggle('cur',+m.dataset.g===g)});
  }
  slides.forEach(function(s){if(s.dataset.strip!==undefined)applyGroup(s,+s.dataset.strip,false)});
  function go(n){
    n=Math.max(0,Math.min(N-1,n));hideZoom();
    if(n!==cur||!slides[n].dataset.ready)clear();
    var sp=slides[cur],sn=slides[n];
    if(sp!==sn&&sp.dataset.strip!==undefined&&sn.dataset.strip!==undefined){
      sn.classList.add('keep');applyGroup(sn,+sp.dataset.strip,false);void sn.offsetWidth;
      requestAnimationFrame(function(){applyGroup(sn,+sn.dataset.strip,true)});
    }else{sn.classList.remove('keep');if(sn.dataset.strip!==undefined)applyGroup(sn,+sn.dataset.strip,false)}
    cur=n;
    slides.forEach(function(s,i){s.dataset.pos=i<n?'before':i>n?'after':'active';s.dataset.ready=1});
    setCount();
    if(prog)prog.style.width=((n+1)/N*100)+'%';
    if(window.DeckBG)DeckBG.setMood(MOODS[n]||'blue');
    if(n===CHART)counters();
    if(n===CONFETTI)startConf();
  }
  window.deckGo=go;
  function toggleFs(){
    try{
      if(document.fullscreenElement){document.exitFullscreen();return}
      if(!document.fullscreenEnabled||!document.documentElement.requestFullscreen){window.open(location.href,'_blank');return}
      var p=document.documentElement.requestFullscreen();if(p&&p.catch)p.catch(function(){window.open(location.href,'_blank')});
    }catch(e){window.open(location.href,'_blank')}
  }

  /* CSS fallback controls (used until/unless the glass dock is ready) */
  var fb=document.getElementById('fbDock'),fbFs=document.getElementById('fbFs');
  fb.querySelector('[data-a=prev]').onclick=function(){go(cur-1)};
  fb.querySelector('[data-a=next]').onclick=function(){go(cur+1)};
  fbFs.onclick=toggleFs;fbFs.title=fsLabel;fbFs.setAttribute('aria-label',fsLabel);
  counts.push(fb.querySelector('span'));

  /* liquid-glass dock (WebGL refraction); falls back silently */
  function glassDock(){
    try{
      if(lite||typeof Container==='undefined'||typeof html2canvas==='undefined')throw 0;
      var c=document.createElement('canvas');if(!(c.getContext('webgl')||c.getContext('experimental-webgl')))throw 0;
      var dock=new Container({type:'pill',borderRadius:40,tintOpacity:0.18});
      var mk=function(t,svg,label,fn,size){
        var b=new Button({text:t,size:size||20,type:'circle',tintOpacity:0.12,onClick:fn});
        var tx=b.element.querySelector('.glass-button-text');if(tx)tx.innerHTML=svg;
        b.element.setAttribute('role','button');b.element.setAttribute('tabindex','0');b.element.setAttribute('aria-label',label);
        b.element.addEventListener('keydown',function(e){if(e.key==='Enter'){e.stopPropagation();fn()}});
        return b;
      };
      var bp=mk('',ICON.prev,'หน้าก่อนหน้า',function(){go(cur-1)});
      var cnt=document.createElement('div');cnt.className='gcount';cnt.style.cssText='font:500 19px Prompt,sans-serif;color:#0B2A6F;min-width:84px;text-align:center;pointer-events:none';
      var bn=mk('',ICON.next,'หน้าถัดไป',function(){go(cur+1)});
      dock.addChild(bp);dock.element.appendChild(cnt);dock.addChild(bn);
      dock.element.style.cssText+=';display:flex;align-items:center;gap:6px;padding:6px 10px;position:relative;left:auto;top:auto;transform:none';
      document.getElementById('dock').appendChild(dock.element);
      var fsb=new Button({text:'',size:20,type:'circle',tintOpacity:0.12,onClick:toggleFs});
      var ft=fsb.element.querySelector('.glass-button-text');if(ft)ft.innerHTML=ICON.fs;
      fsb.element.setAttribute('role','button');fsb.element.setAttribute('tabindex','0');fsb.element.setAttribute('aria-label',fsLabel);fsb.element.title=fsLabel;
      fsb.element.style.cssText+=';position:relative;left:auto;top:auto;transform:none';
      document.getElementById('fsWrap').appendChild(fsb.element);
      counts=[cnt];setCount();
      fb.classList.remove('on');fbFs.classList.remove('on');
      document.documentElement.classList.add('glass-on');
    }catch(e){fb.classList.add('on');fbFs.classList.add('on')}
  }
  fb.classList.add('on');fbFs.classList.add('on');

  function boot(){
    var bgel=document.getElementById('bg');
    if(window.DeckBG&&!lite||window.DeckBG&&lite){
      try{DeckBG.mount(bgel,{lite:lite})}catch(e){}
      DeckBG.setMood(MOODS[cur],true);
    }
    /* take the glass snapshot after the background has painted a few frames */
    setTimeout(glassDock,lite?0:1800);
  }

  /* image zoom */
  function showZoom(src,alt){zimg.src=src;zimg.alt=alt||'';zoom.hidden=false}
  function hideZoom(){if(!zoom.hidden){zoom.hidden=true;zimg.removeAttribute('src')}}
  stage.addEventListener('click',function(e){var t=e.target;if(t.closest&&t.closest('.shot')&&t.tagName==='IMG')showZoom(t.src,t.alt)});
  zoom.addEventListener('click',hideZoom);
  [].forEach.call(document.querySelectorAll('[data-go]'),function(b){b.addEventListener('click',function(){go(+b.dataset.go)})});

  /* spotlight on cards */
  stage.addEventListener('pointermove',function(e){
    var c=e.target.closest&&e.target.closest('.card');if(!c)return;
    var r=c.getBoundingClientRect();c.style.setProperty('--mx',((e.clientX-r.left)/r.width*100)+'%');c.style.setProperty('--my',((e.clientY-r.top)/r.height*100)+'%');
  });

  document.addEventListener('keydown',function(e){
    var k=e.key,btn=e.target&&e.target.tagName==='BUTTON';
    if(k==='Escape'){hideZoom();return}
    if(k==='ArrowRight'||k==='PageDown'||(k===' '&&!btn)){e.preventDefault();go(cur+1)}
    else if(k==='ArrowLeft'||k==='PageUp'){e.preventDefault();go(cur-1)}
    else if(k==='Home')go(0);else if(k==='End')go(N-1);
    else if(k==='f'||k==='F')toggleFs();
  });
  var tx=null;
  area.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});
  area.addEventListener('touchend',function(e){if(tx===null)return;var dx=e.changedTouches[0].clientX-tx;tx=null;if(Math.abs(dx)>60)go(cur+(dx<0?1:-1))},{passive:true});

  function counters(){
    var my=token;
    [].forEach.call(slides[CHART].querySelectorAll('[data-count]'),function(el,i){
      var end=+el.dataset.count;
      if(reduce){el.textContent=end.toLocaleString('en-US');return}
      el.textContent='0';
      var t=setTimeout(function(){
        var t0=performance.now(),d=900;
        (function step(now){
          if(my!==token)return;
          var p=Math.min(1,(now-t0)/d),e=1-Math.pow(1-p,3);
          el.textContent=Math.round(end*e).toLocaleString('en-US');
          if(p<1)requestAnimationFrame(step);
        })(t0);
      },500+i*100);timers.push(t);
    });
  }

  var cv=document.getElementById('conf'),cx=cv.getContext('2d'),raf=0;
  function stopConf(){if(raf)cancelAnimationFrame(raf);raf=0;cx.clearRect(0,0,cv.width,cv.height)}
  function startConf(){
    if(reduce)return;
    var cols=['#5A97FF','#FF5A64','#FFD166','#2DD4A0','#FF9A3D','#FFFFFF'],W=cv.width,H=cv.height,t0=performance.now();
    var ps=[];for(var i=0;i<(lite?60:140);i++)ps.push({x:Math.random()*W,y:-Math.random()*500,vx:(Math.random()-.5)*3,vy:2+Math.random()*4,s:9+Math.random()*10,r:Math.random()*6,vr:(Math.random()-.5)*.3,c:cols[i%6]});
    (function loop(now){
      cx.clearRect(0,0,W,H);var alive=false;
      ps.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.r+=p.vr;if(p.y<H+30)alive=true;
        cx.save();cx.translate(p.x,p.y);cx.rotate(p.r);cx.fillStyle=p.c;cx.globalAlpha=.9;cx.beginPath();cx.roundRect?cx.roundRect(-p.s/2,-p.s/4,p.s,p.s/2,3):cx.rect(-p.s/2,-p.s/4,p.s,p.s/2);cx.fill();cx.restore()});
      if(alive&&now-t0<7000)raf=requestAnimationFrame(loop);else{raf=0;cx.clearRect(0,0,W,H)}
    })(t0);
  }

  (document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve()).then(fillSlides);setTimeout(fillSlides,2500);
  go(0);
  if(document.readyState==='complete')boot();else window.addEventListener('load',boot);
})();
