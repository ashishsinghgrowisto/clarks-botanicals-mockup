JS = r"""
(function(){
var PW = "__PW__";

/* ---------------- password gate ---------------- */
function gateInit(){
  var g = document.getElementById('gate');
  if(!g) return;
  try{ if(localStorage.getItem('cb_gate_ok')==='1'){ g.remove(); document.body.classList.remove('locked'); return; } }catch(e){}
  document.body.classList.add('locked'); g.classList.add('on');
  var inp = g.querySelector('input'), err = g.querySelector('.gate-err');
  function submit(){
    if(inp.value.trim().toLowerCase() === PW){
      try{ localStorage.setItem('cb_gate_ok','1'); }catch(e){}
      g.remove(); document.body.classList.remove('locked');
    } else { err.textContent = 'Incorrect password'; inp.value=''; inp.focus(); }
  }
  g.querySelector('button').addEventListener('click', submit);
  inp.addEventListener('keydown', function(e){ if(e.key==='Enter') submit(); });
  setTimeout(function(){ inp.focus(); }, 60);
}

/* ---------------- layout metrics ---------------- */
function metrics(){
  var ann = document.querySelector('.ann'), hdr = document.querySelector('.hdr');
  var root = document.documentElement;
  if(ann) root.style.setProperty('--annh', ann.offsetHeight + 'px');
  if(hdr) root.style.setProperty('--hdrh', hdr.offsetHeight + 'px');
  var s = document.querySelector('.search');
  if(s && ann && hdr) s.style.top = (ann.offsetHeight + hdr.offsetHeight) + 'px';
}

/* ---------------- overlays ---------------- */
function overlay(){ return document.querySelector('.ov'); }
function openPanel(sel){
  var p = document.querySelector(sel); if(!p) return;
  p.classList.add('on');
  var o = overlay(); if(o) o.classList.add('on');
  document.body.style.overflow='hidden';
}
function closeAll(){
  document.querySelectorAll('.panel.on,.sheet.on,.search.on').forEach(function(x){ x.classList.remove('on'); });
  if(window.cbCloseSATC) window.cbCloseSATC();
  var o = overlay(); if(o) o.classList.remove('on');
  document.body.style.overflow='';
}

/* ---------------- cart ---------------- */
var CART = [];
try{ CART = JSON.parse(localStorage.getItem('cb_cart')||'[]'); }catch(e){ CART=[]; }
function saveCart(){ try{ localStorage.setItem('cb_cart', JSON.stringify(CART)); }catch(e){} }
function cartCount(){ return CART.reduce(function(a,b){ return a + b.q; },0); }
function cartTotal(){ return CART.reduce(function(a,b){ return a + b.q*b.price; },0); }
function money(n){ return '$' + n.toFixed(2); }
function syncDots(){
  var n = cartCount();
  document.querySelectorAll('.cartdot').forEach(function(d){
    if(n > 0){ d.classList.add('num'); d.textContent = n; }
    else { d.classList.remove('num'); d.textContent = ''; }
  });
}
function addToCart(item){
  var k = CART.find(function(c){ return c.handle===item.handle && c.opt===item.opt && c.sub===item.sub; });
  if(k) k.q += item.q||1;
  else CART.push({handle:item.handle,title:item.title,price:item.price,img:item.img,
                  opt:item.opt||'',sub:item.sub||'',q:item.q||1});
  saveCart(); syncDots(); renderCart(); openPanel('#cart');
}

function mostLoved(){
  var pool = (window.CB_PRODUCTS||[]).filter(function(p){
    return !CART.some(function(c){ return c.handle===p.handle; });
  });
  var p = pool[0]; if(!p) return '';
  return '<div class="cart__div ml"><h4>Most loved</h4><div class="ml__row">' +
    '<img src="' + p.img + '" alt="">' +
    '<div><p class="ci__t">' + p.title + '</p>' +
    '<p class="ci__p">' + money(p.price) + '</p>' +
    '<p style="margin-top:8px"><button class="tlink" type="button" data-quick="' + p.handle + '">Add to cart</button></p>' +
    '</div></div></div>';
}

function renderCart(){
  var bd = document.querySelector('#cart .panel__bd'), ft = document.querySelector('#cart .panel__ft');
  if(!bd) return;
  if(!CART.length){
    bd.innerHTML = '<p class="empty">Your cart is empty</p>' + mostLoved();
    ft.innerHTML = '<a class="cart__co" href="collection.html">Continue shopping</a>';
    return;
  }
  var rows = CART.map(function(c,i){
    return '<div class="ci">' +
      '<img src="' + c.img + '" alt="">' +
      '<div><div class="ci__t">' + c.title + '</div>' +
      '<div class="ci__p">' + money(c.price) + '</div>' +
      (c.opt ? '<div class="ci__o">' + c.opt + '</div>' : '') +
      (c.sub ? '<div class="ci__sub">' + c.sub + '</div>' : '') +
      '<div class="ci__row">' +
        '<span class="qty"><button data-q="-1" data-i="' + i + '" aria-label="Decrease">&minus;</button>' +
        '<span>' + c.q + '</span>' +
        '<button data-q="1" data-i="' + i + '" aria-label="Increase">+</button></span>' +
        '<button class="tlink" data-rm="' + i + '">Remove</button>' +
      '</div></div></div>';
  }).join('');
  bd.innerHTML = rows + mostLoved();
  ft.innerHTML =
    '<p class="cart__note">*Discounts, taxes &amp; shipping shown at checkout</p>' +
    '<button class="cart__co" type="button">Checkout <span>&middot;</span> ' + money(cartTotal()) + '</button>';
}

document.addEventListener('click', function(e){
  var t = e.target.closest('[data-q],[data-rm]');
  if(t && t.closest('#cart')){
    if(t.hasAttribute('data-q')){ var i=+t.dataset.i; CART[i].q = Math.max(1, CART[i].q + (+t.dataset.q)); }
    if(t.hasAttribute('data-rm')){ CART.splice(+t.dataset.rm,1); }
    saveCart(); syncDots(); renderCart();
  }
});

/* ---------------- shared variant panel ---------------- */
/* One panel serves every entry point: product cards, the cart's Most loved
   row, and the PDP sticky bar. Contents are built per product on open. */
var VP = { handle:null, sel:{}, qty:1, sub:true, mode:'cart' };

function vp(){ return document.getElementById('vpanel'); }
function vpProduct(){ return (window.CB_PRODUCTS||[]).find(function(x){ return x.handle===VP.handle; }); }
function vpFreeShip(){ var e=vp(); return e ? +(e.dataset.freeship||75) : 75; }
function vpSubOff(){ var e=vp(); return e ? +(e.dataset.suboff||0.15) : 0.15; }
function vpSubWord(){ var e=vp(); return e ? (e.dataset.subword||'15') : '15'; }

function vpUnit(){ var p=vpProduct(); if(!p) return 0;
  return VP.sub ? p.price * (1 - vpSubOff()) : p.price; }
function vpTotal(){ return vpUnit() * VP.qty; }
function vpOptText(){ return Object.keys(VP.sel).map(function(k){ return VP.sel[k]; }).join(' · '); }

function vpRender(){
  var el = vp(), p = vpProduct(); if(!el || !p) return;
  var groups = (p.opts||[]).map(function(o){
    return '<div class="satc__grp"><p class="satc__lbl"><b>' + o.name + '</b>' +
      '<span data-satc-selname="' + o.name + '"></span></p><div class="satc__opts">' +
      o.values.map(function(v){
        return '<button type="button" data-satc-opt="' + o.name + '" data-satc-val="' + v + '">' + v + '</button>';
      }).join('') + '</div></div>';
  }).join('');
  var freqs = ['1 week','2 weeks','1 month','2 months','3 months'];
  var opts = freqs.map(function(f){
    return '<option' + (f==='1 month' ? ' selected' : '') + '>Deliver every ' + f + '</option>'; }).join('');
  el.innerHTML =
    '<button class="satc__close" type="button" data-satc-close aria-label="Close">' +
      '<svg width="16" height="16" fill="none" viewBox="0 0 16 16">' +
      '<path d="m1 1 14 14M1 15 15 1" stroke="currentColor" stroke-width="1.6"/></svg></button>' +
    '<div class="satc__in">' +
      '<div class="satc__hd"><img src="' + p.img + '" alt="">' +
        '<div><h3 class="h">' + p.title + '</h3>' +
        (p.rating ? '<p class="satc__rate"><span class="stars">★★★★★</span>' + p.rating +
          ' (' + p.rev + ' review' + (p.rev===1?'':'s') + ')</p>' : '') +
        '<p class="satc__price" data-satc-price></p></div></div>' +
      groups +
      '<div class="satc__qty"><p class="satc__lbl" style="margin:0"><b>Quantity</b></p>' +
        '<span class="qty" data-satc-qty>' +
        '<button type="button" data-satc-step="-1" aria-label="Decrease quantity">&minus;</button>' +
        '<span>1</span>' +
        '<button type="button" data-satc-step="1" aria-label="Increase quantity">+</button></span></div>' +
      '<div class="satc__ship"><p data-satc-ship></p>' +
        '<span class="satc__bar"><i data-satc-bar></i></span></div>' +
    '</div>' +
    '<div class="satc__foot">' +
      '<div class="satc__sub">' +
        '<label><span class="satc__sw" data-satc-sub role="switch"></span>' +
        '<span><b>Subscribed.</b> Saving ' + vpSubWord() + '%</span></label>' +
        '<select data-satc-freq aria-label="Delivery frequency">' + opts + '</select>' +
      '</div>' +
      '<button class="satc__cta" type="button" data-satc-cta>Add to cart</button>' +
    '</div>';
  vpPaint();
}

function vpPaint(){
  var el = vp(), p = vpProduct(); if(!el || !p) return;
  var price = el.querySelector('[data-satc-price]'), cta = el.querySelector('[data-satc-cta]');
  if(!price || !cta) return;
  price.textContent = money(vpUnit());
  cta.textContent = (VP.mode === 'buy' ? 'Buy now  ' : 'Add to cart  ') + money(vpTotal());
  el.querySelector('[data-satc-qty] span').textContent = VP.qty;
  var left = vpFreeShip() - vpTotal();
  el.querySelector('[data-satc-ship]').innerHTML = left > 0
    ? 'You&rsquo;re <b>' + money(left) + '</b> away from free shipping'
    : '<b>You&rsquo;ve unlocked free shipping</b>';
  el.querySelector('[data-satc-bar]').style.width =
    Math.min(100, vpTotal() / vpFreeShip() * 100) + '%';
  var subWrap = el.querySelector('.satc__sub'), subSel = el.querySelector('[data-satc-freq]');
  subWrap.classList.toggle('on', VP.sub);
  if(subSel) subSel.disabled = !VP.sub;
  el.querySelectorAll('[data-satc-opt]').forEach(function(b){
    b.classList.toggle('on', VP.sel[b.dataset.satcOpt] === b.dataset.satcVal);
  });
  el.querySelectorAll('[data-satc-selname]').forEach(function(sp){
    sp.textContent = VP.sel[sp.dataset.satcSelname] + ' selected';
  });
  window.VPSTATE = { handle: VP.handle, price: money(vpUnit()), opt: vpOptText() };
  if(window.cbSyncBar) window.cbSyncBar();
}

function openVariant(handle, mode){
  var p = (window.CB_PRODUCTS||[]).find(function(x){ return x.handle===handle; });
  var el = vp(); if(!p || !el) return;
  VP = { handle:handle, sel:{}, qty:1, sub:true, mode:mode||'cart' };
  (p.opts||[]).forEach(function(o){ VP.sel[o.name] = o.values[0]; });
  vpRender();
  el.classList.add('on');
  var bar = document.querySelector('.satcbar'); if(bar) bar.classList.remove('on');
  var o = overlay(); if(o) o.classList.add('on');
  document.body.style.overflow = 'hidden';
}
window.openVariant = openVariant;

function closeVariant(){
  var el = vp(); if(el) el.classList.remove('on');
  var o = overlay(); if(o) o.classList.remove('on');
  document.body.style.overflow = '';
  if(window.cbSyncBar) window.cbSyncBar();
}
window.cbCloseSATC = closeVariant;

document.addEventListener('click', function(e){
  var q = e.target.closest('[data-quick]');
  if(q){ e.preventDefault(); openVariant(q.dataset.quick, 'cart'); return; }
  /* single-variant add-on: no options to pick, so skip the panel */
  var d = e.target.closest('[data-add]');
  if(d){
    e.preventDefault();
    var dp = (window.CB_PRODUCTS||[]).find(function(x){ return x.handle===d.dataset.add; });
    if(dp) addToCart({handle:dp.handle,title:dp.title,price:dp.price,img:dp.img,opt:'',sub:'',q:1});
    return;
  }
  var el = vp(); if(!el || !el.contains(e.target)) return;
  var o = e.target.closest('[data-satc-opt]');
  if(o){ VP.sel[o.dataset.satcOpt] = o.dataset.satcVal; vpPaint(); return; }
  var st = e.target.closest('[data-satc-step]');
  if(st){ VP.qty = Math.max(1, VP.qty + (+st.dataset.satcStep)); vpPaint(); return; }
  if(e.target.closest('[data-satc-sub]')){ VP.sub = !VP.sub; vpPaint(); return; }
  if(e.target.closest('[data-satc-close]')){ closeVariant(); return; }
  if(e.target.closest('[data-satc-cta]')){
    var p = vpProduct(); if(!p) return;
    var sel = el.querySelector('[data-satc-freq]');
    var freq = (VP.sub && sel) ? sel.value : '';
    var item = { handle:p.handle, title:p.title, price:vpUnit(), img:p.img,
                 opt:vpOptText(), sub:freq, q:VP.qty };
    closeVariant();
    addToCart(item);
  }
});

/* ---------------- mobile drawer ---------------- */
function initDrawer(){
  var dd = document.querySelector('#menu .dd'); if(!dd) return;
  dd.addEventListener('click', function(e){
    var it = e.target.closest('[data-sub]');
    if(it){ var v = dd.querySelector('[data-view="' + it.dataset.sub + '"]'); if(v) v.classList.add('on'); return; }
    if(e.target.closest('.dd__back')){ e.target.closest('.dd__view').classList.remove('on'); }
  });
}
function resetDrawer(){ document.querySelectorAll('#menu .dd__view.sub').forEach(function(v){ v.classList.remove('on'); }); }

/* ---------------- sliders ---------------- */
function initSliders(){
  document.querySelectorAll('.slider').forEach(function(s){
    var tr = s.querySelector('.slider__track'), dots = s.querySelector('.dots');
    if(!tr || !dots) return;
    var n = tr.children.length;
    dots.innerHTML = Array.from({length:n}).map(function(_,i){
      return '<button type="button" class="' + (i===0?'on':'') + '" aria-label="Go to item ' + (i+1) + '"></button>'; }).join('');
    dots.addEventListener('click', function(e){
      var b = e.target.closest('button'); if(!b) return;
      var i = Array.prototype.indexOf.call(dots.children, b);
      tr.scrollTo({left: i*tr.clientWidth, behavior:'smooth'});
    });
    tr.addEventListener('scroll', function(){
      var i = Math.round(tr.scrollLeft / tr.clientWidth);
      Array.prototype.forEach.call(dots.children, function(d,j){ d.classList.toggle('on', j===i); });
    });
  });
  document.querySelectorAll('[data-rail]').forEach(function(btn){
    btn.addEventListener('click', function(){
      var rail = document.querySelector(btn.dataset.rail);
      if(rail) rail.scrollBy({left: (+btn.dataset.dir) * rail.clientWidth * 0.8, behavior:'smooth'});
    });
  });
}

/* ---------------- before / after ---------------- */
function initBA(){
  document.querySelectorAll('.ba').forEach(function(ba){
    var af = ba.querySelector('.ba__after'), hd = ba.querySelector('.ba__handle');
    var afImg = af.querySelector('img');
    function sizeAfter(){ afImg.style.width = ba.clientWidth + 'px'; }
    sizeAfter();
    window.addEventListener('resize', sizeAfter);
    afImg.addEventListener('load', sizeAfter);
    ba.querySelectorAll('img').forEach(function(i){ i.addEventListener('load', sizeAfter); });
    var drag = false;
    function set(x){
      var r = ba.getBoundingClientRect();
      var p = Math.min(100, Math.max(0, (x - r.left)/r.width*100));
      af.style.width = p + '%'; hd.style.left = p + '%';
    }
    function down(e){ drag = true; set(e.touches?e.touches[0].clientX:e.clientX); }
    function move(e){ if(!drag) return; set(e.touches?e.touches[0].clientX:e.clientX); }
    function up(){ drag = false; }
    ba.addEventListener('mousedown', down); ba.addEventListener('touchstart', down, {passive:true});
    window.addEventListener('mousemove', move); window.addEventListener('touchmove', move, {passive:true});
    window.addEventListener('mouseup', up); window.addEventListener('touchend', up);
  });
}

/* ---------------- PDP ---------------- */
function initPDP(){
  var gal = document.querySelector('.gal');
  if(gal){
    var thumbs = gal.querySelector('.gal__thumbs'), rail = gal.querySelector('.gal__mrail');
    var main = rail.querySelector('img');
    function fit(){ if(thumbs && main && main.clientHeight) thumbs.style.maxHeight = main.clientHeight + 'px'; }
    window.addEventListener('resize', fit); setTimeout(fit, 300);
    if(main) main.addEventListener('load', fit);
    if(thumbs) thumbs.addEventListener('click', function(e){
      var b = e.target.closest('button'); if(!b) return;
      var i = +b.dataset.i;
      thumbs.querySelectorAll('button').forEach(function(x,j){ x.classList.toggle('on', j===i); });
      rail.querySelectorAll('img').forEach(function(x,j){ x.classList.toggle('on', j===i); });
      if(window.innerWidth < 1000) rail.scrollTo({left: i*rail.clientWidth, behavior:'smooth'});
    });
  }
  /* subscription selector */
  var subs = document.querySelector('.subs');
  if(subs){
    subs.addEventListener('change', function(){
      subs.querySelectorAll('label').forEach(function(l){
        l.classList.toggle('on', l.querySelector('input').checked);
      });
    });
  }
  /* qty stepper on PDP */
  document.querySelectorAll('[data-pdp-qty]').forEach(function(w){
    var out = w.querySelector('span');
    w.addEventListener('click', function(e){
      var b = e.target.closest('button'); if(!b) return;
      var v = Math.max(1, (+out.textContent) + (+b.dataset.step));
      out.textContent = v;
    });
  });
  var atc = document.querySelector('[data-pdp-add]');
  if(atc) atc.addEventListener('click', function(){
    var h = atc.dataset.pdpAdd;
    var p = (window.CB_PRODUCTS||[]).find(function(x){ return x.handle===h; });
    if(!p) return;
    var qEl = document.querySelector('[data-pdp-qty] span');
    var q = qEl ? +qEl.textContent : 1;
    var chosen = document.querySelector('.subs input:checked');
    var sub = chosen && chosen.dataset.sub ? chosen.dataset.sub : '';
    var price = chosen && chosen.dataset.price ? +chosen.dataset.price : p.price;
    var optEl = document.querySelector('[data-pdp-opt]');
    addToCart({handle:p.handle,title:p.title,price:price,img:p.img,
               opt:optEl?optEl.textContent.trim():'', sub:sub, q:q});
  });
}

/* ---------------- PDP sticky bar ---------------- */
function initSATC(){
  var bar = document.querySelector('.satcbar'); if(!bar) return;
  var anchor = document.querySelector('[data-pdp-add]');
  var handle = bar.dataset.handle;
  var p = (window.CB_PRODUCTS||[]).find(function(x){ return x.handle===handle; });
  if(!p) return;
  var barPrice = bar.querySelector('[data-satcbar-price]');
  var barOpt   = bar.querySelector('[data-satcbar-opt]');

  bar.addEventListener('click', function(e){
    var t = e.target.closest('[data-satcbar-open]');
    if(t) openVariant(handle, t.dataset.satcbarOpen);
  });

  function sync(){
    var panel = document.getElementById('vpanel');
    if(panel && panel.classList.contains('on')){ bar.classList.remove('on'); return; }
    /* mirror whatever the panel currently holds for this product */
    if(barPrice && window.VPSTATE && window.VPSTATE.handle === handle){
      barPrice.textContent = window.VPSTATE.price;
      if(barOpt) barOpt.textContent = window.VPSTATE.opt;
    }
    var r = anchor ? anchor.getBoundingClientRect() : null;
    var visible = r && r.bottom > 0 && r.top < (window.innerHeight || 0);
    bar.classList.toggle('on', !visible);
  }
  window.cbSyncBar = sync;

  if('IntersectionObserver' in window && anchor){
    new IntersectionObserver(function(){ sync(); }, {threshold:0}).observe(anchor);
  }
  window.addEventListener('scroll', sync, {passive:true});
  window.addEventListener('resize', sync);
  sync();
}

/* ---------------- PLP ---------------- */
function initPLP(){
  var list = document.getElementById('plist'); if(!list) return;
  var active = new Set(), sort = 'manual';
  var chips = document.getElementById('achips');
  function apply(){
    var cards = Array.prototype.slice.call(list.children);
    cards.forEach(function(c){
      c.style.display = (!active.size || active.has(c.dataset.type)) ? '' : 'none';
    });
    var vis = cards.filter(function(c){ return c.style.display !== 'none'; });
    if(sort !== 'manual'){
      vis.sort(function(a,b){
        if(sort==='price-asc') return (+a.dataset.price) - (+b.dataset.price);
        if(sort==='price-desc') return (+b.dataset.price) - (+a.dataset.price);
        if(sort==='az') return a.dataset.title.localeCompare(b.dataset.title);
        if(sort==='za') return b.dataset.title.localeCompare(a.dataset.title);
        return 0;
      });
      vis.forEach(function(c){ list.appendChild(c); });
    }
    chips.innerHTML = Array.from(active).map(function(t){
      return '<button type="button" data-chip="' + t + '">' + t + ' <span>&times;</span></button>';
    }).join('');
  }
  document.addEventListener('change', function(e){
    var f = e.target.closest('[data-filter]'); if(!f) return;
    if(f.checked) active.add(f.value); else active.delete(f.value);
    apply();
  });
  document.addEventListener('click', function(e){
    var c = e.target.closest('[data-chip]');
    if(c){ active.delete(c.dataset.chip);
      document.querySelectorAll('[data-filter]').forEach(function(i){ if(i.value===c.dataset.chip) i.checked=false; });
      apply(); return; }
    var s = e.target.closest('[data-sort]');
    if(s){ sort = s.dataset.sort;
      s.parentElement.querySelectorAll('[data-sort]').forEach(function(x){ x.classList.remove('on'); });
      s.classList.add('on'); apply(); closeAll(); }
  });
  apply();
}

/* ---------------- predictive search ---------------- */
function initSearch(){
  var s = document.querySelector('.search'); if(!s) return;
  var input = s.querySelector('input');
  var sug = s.querySelector('.search__sug');
  var tiles = s.querySelector('.search__tiles');
  var all = window.CB_PRODUCTS || [];
  function render(){
    var q = input.value.trim().toLowerCase();
    var hits = q ? all.filter(function(p){ return p.title.toLowerCase().indexOf(q) > -1; }) : all;
    hits = hits.slice(0,4);
    sug.innerHTML = q
      ? '<p style="margin:0"><b>' + q + '</b></p>'
      : ['retinol','eye cream','serum','moisturizer'].map(function(t){
          return '<p style="margin:0">' + t + '</p>'; }).join('');
    tiles.innerHTML = hits.map(function(p){
      return '<a href="product.html"><img src="' + p.img + '" alt="" loading="lazy">' +
        '<p class="pc__title" style="margin:14px 0 6px;text-align:center">' + p.title + '</p>' +
        '<p class="price' + (p.cmp?'':' plain') + '" style="margin:0">' + money(p.price) +
        (p.cmp ? '<s>' + money(p.cmp) + '</s>' : '') + '</p></a>';
    }).join('');
  }
  input.addEventListener('input', render);
  render();
  var btn = document.querySelector('[data-open-search]');
  if(btn) btn.addEventListener('click', function(){
    metrics();
    var open = s.classList.contains('on');
    closeAll();
    if(!open){ s.classList.add('on'); document.body.style.overflow='hidden';
      setTimeout(function(){ input.focus(); }, 120); }
  });
}

/* ---------------- boot ---------------- */
document.addEventListener('DOMContentLoaded', function(){
  gateInit(); metrics(); syncDots(); renderCart();
  initDrawer(); initSliders(); initBA(); initPDP(); initPLP(); initSearch(); initSATC();
  window.addEventListener('resize', metrics);
  window.addEventListener('load', metrics);

  document.querySelectorAll('[data-open]').forEach(function(b){
    b.addEventListener('click', function(e){
      e.preventDefault();
      var sel = b.dataset.open;
      if(sel === '#menu') resetDrawer();
      openPanel(sel);
    });
  });
  document.querySelectorAll('[data-close]').forEach(function(b){ b.addEventListener('click', closeAll); });
  var o = overlay(); if(o) o.addEventListener('click', closeAll);
  document.addEventListener('keydown', function(e){ if(e.key==='Escape'){ closeAll(); } });
});
})();


/* ---- 9. desktop sticky nav: pin .pnav once the logo row has scrolled off ---- */
(function(){
  var hdr = document.querySelector('.hdr');
  var pnav = document.querySelector('.pnav');
  if(!hdr || !pnav) return;
  var spacer = document.querySelector('.navspacer');
  if(!spacer){
    spacer = document.createElement('div');
    spacer.className = 'navspacer';
    hdr.parentNode.insertBefore(spacer, hdr.nextSibling);
  }
  var desktop = window.matchMedia('(min-width:1000px)');
  function trigger(){
    /* stick the moment the nav's own top edge would leave the viewport */
    return pnav.getBoundingClientRect().top + window.scrollY;
  }
  var point = 0, stuck = false, navH = 0;
  function measure(){
    if(document.body.classList.contains('nav-stuck')) return;
    point = trigger();
    navH = pnav.offsetHeight;
  }
  function onScroll(){
    if(!desktop.matches){
      document.body.classList.remove('nav-stuck');
      spacer.style.height = '0px';
      stuck = false;
      return;
    }
    var should = window.scrollY > point;
    if(should === stuck) return;
    stuck = should;
    document.body.classList.toggle('nav-stuck', stuck);
    spacer.style.height = stuck ? navH + 'px' : '0px';
  }
  measure();
  window.addEventListener('scroll', onScroll, {passive:true});
  window.addEventListener('resize', function(){
    document.body.classList.remove('nav-stuck');
    spacer.style.height = '0px';
    stuck = false;
    measure();
    onScroll();
  });
  window.addEventListener('load', function(){ measure(); onScroll(); });
  onScroll();
})();

/* ---- 6. mobile bottom nav: mirror the cart count, flag the current page ---- */
(function(){
  var bar = document.querySelector('.mobnav');
  if(!bar) return;
  var src = document.querySelector('.hdr__icons .cartdot');
  var dst = bar.querySelector('.mobnav__dot');
  function sync(){
    if(!dst) return;
    var n = src ? (src.textContent || '').trim() : '';
    var on = !!(src && src.offsetParent !== null) || !!n;
    dst.textContent = n;
    dst.style.display = on && n ? 'block' : 'none';
  }
  sync();
  if(src && window.MutationObserver){
    new MutationObserver(sync).observe(src, {childList:true, characterData:true, subtree:true, attributes:true});
  }
  document.addEventListener('click', function(){ setTimeout(sync, 60); });

  var here = (location.pathname.split('/').pop() || 'home.html');
  bar.querySelectorAll('a[href]').forEach(function(a){
    if(a.getAttribute('href') === here) a.setAttribute('aria-current','page');
  });
})();

/* ---- 5. marquee: only animate when the text would actually overflow ---- */
(function(){
  var track = document.querySelector('.ann__track');
  if(!track) return;
  function check(){
    var first = track.querySelector('span');
    if(!first) return;
    var fits = first.scrollWidth <= track.parentNode.clientWidth;
    track.style.animationPlayState =
      (window.matchMedia('(max-width:999px)').matches && !fits) ? 'running' : '';
  }
  window.addEventListener('resize', check);
  check();
})();

/* ---- signed-in demo toggle for the recommendations block ---- */
(function(){
  var btn = document.querySelector('.authtoggle');
  if(!btn) return;
  var KEY = 'cb_mock_signed_in';
  function paint(){
    var on = false;
    try{ on = localStorage.getItem(KEY) === '1'; }catch(e){}
    document.body.classList.toggle('is-signed-in', on);
    btn.textContent = on ? 'Signed in \u00b7 demo' : 'Signed out \u00b7 demo';
  }
  btn.addEventListener('click', function(){
    var on = document.body.classList.contains('is-signed-in');
    try{ localStorage.setItem(KEY, on ? '0' : '1'); }catch(e){}
    paint();
  });
  paint();
})();


/* keep the demo toggle clear of the sticky add-to-cart bar */
(function(){
  var bar = document.querySelector('.satcbar');
  if(!bar) return;
  function sync(){
    var on = bar.classList.contains('on');
    document.documentElement.style.setProperty('--satc-h', on ? (bar.offsetHeight + 10) + 'px' : '0px');
  }
  if(window.MutationObserver){
    new MutationObserver(sync).observe(bar, {attributes:true, attributeFilter:['class']});
  }
  window.addEventListener('resize', sync);
  sync();
})();
"""
