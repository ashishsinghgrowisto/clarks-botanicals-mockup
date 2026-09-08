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
    '<p class="ci__p">' + money(p.price) + ' USD</p>' +
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
      '<div class="ci__p">' + money(c.price) + ' USD</div>' +
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

/* ---------------- variant modal ---------------- */
var MODAL_SEL = {};
function openQuick(handle){
  var p = (window.CB_PRODUCTS||[]).find(function(x){ return x.handle===handle; });
  if(!p) return;
  var m = document.getElementById('vmodal'); if(!m) return;
  MODAL_SEL = {}; (p.opts||[]).forEach(function(o){ MODAL_SEL[o.name] = o.values[0]; });
  m.querySelector('.modal__img img').src = p.img;
  m.querySelector('.modal__body').innerHTML =
    '<p class="h h5" style="margin:0">' + p.title + '</p>' +
    '<div style="display:flex;gap:12px;align-items:center;margin-top:12px">' +
      '<span class="stars">' + '★★★★★' + '</span>' +
      '<span class="xxs sub">(' + (p.rev||6) + ')</span>' +
      '<span class="price' + (p.cmp ? '' : ' plain') + '" style="justify-content:flex-start">' +
        money(p.price) + ' USD' + (p.cmp ? '<s>' + money(p.cmp) + ' USD</s>' : '') + '</span>' +
    '</div>' +
    (p.opts||[]).map(function(o){
      return '<div class="opt"><p>' + o.name + '</p><div class="opt__row">' + o.values.map(function(v,i){
        return '<button type="button" data-opt="' + o.name + '" data-val="' + v + '" class="' + (i===0?'on':'') + '">' + v + '</button>';
      }).join('') + '</div></div>';
    }).join('') +
    '<div style="margin-top:26px;display:grid;gap:14px;justify-items:start">' +
      '<button class="btn btn--full" type="button" data-madd="' + p.handle + '">Add to cart</button>' +
      '<a class="ulink" href="product.html">View full product details</a>' +
    '</div>';
  m.classList.add('on'); document.body.style.overflow='hidden';
}
function closeQuick(){
  var m=document.getElementById('vmodal'); if(m) m.classList.remove('on');
  if(!document.querySelector('.panel.on,.sheet.on')) document.body.style.overflow='';
}

document.addEventListener('click', function(e){
  var q = e.target.closest('[data-quick]');
  if(q){ e.preventDefault(); openQuick(q.dataset.quick); return; }
  var o = e.target.closest('[data-opt]');
  if(o){
    MODAL_SEL[o.dataset.opt] = o.dataset.val;
    o.parentElement.querySelectorAll('button').forEach(function(x){ x.classList.remove('on'); });
    o.classList.add('on'); return;
  }
  var a = e.target.closest('[data-madd]');
  if(a){
    var p = (window.CB_PRODUCTS||[]).find(function(x){ return x.handle===a.dataset.madd; });
    var opt = Object.keys(MODAL_SEL).map(function(k){ return MODAL_SEL[k]; }).join(' / ');
    closeQuick(); addToCart({handle:p.handle,title:p.title,price:p.price,img:p.img,opt:opt,q:1});
    return;
  }
  if(e.target.closest('.modal__bg') || e.target.closest('.modal__close')) closeQuick();
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

/* ---------------- sticky bar + add-to-cart panel (PDP) ---------------- */
function initSATC(){
  var el = document.querySelector('.satc'); if(!el) return;
  var bar = document.querySelector('.satcbar');
  var anchor = document.querySelector('[data-pdp-add]');
  var p = (window.CB_PRODUCTS||[]).find(function(x){ return x.handle===el.dataset.handle; });
  if(!p) return;

  var FREE_SHIP = +(el.dataset.freeship || 75);
  var SUB_OFF   = +(el.dataset.suboff || 0.15);
  var sel = {}, qty = 1, sub = true, mode = 'cart';
  (p.opts||[]).forEach(function(o){ sel[o.name] = o.values[0]; });

  var priceEl = el.querySelector('[data-satc-price]');
  var ctaEl   = el.querySelector('[data-satc-cta]');
  var qtyEl   = el.querySelector('[data-satc-qty] span');
  var shipTxt = el.querySelector('[data-satc-ship]');
  var shipBar = el.querySelector('[data-satc-bar]');
  var subWrap = el.querySelector('.satc__sub');
  var subSel  = el.querySelector('[data-satc-freq]');
  var barPrice = bar && bar.querySelector('[data-satcbar-price]');
  var barOpt   = bar && bar.querySelector('[data-satcbar-opt]');

  function unit(){ return sub ? p.price * (1 - SUB_OFF) : p.price; }
  function total(){ return unit() * qty; }
  function optText(){ return Object.keys(sel).map(function(k){ return sel[k]; }).join(' · '); }

  function paint(){
    priceEl.textContent = money(unit());
    ctaEl.textContent = (mode === 'buy' ? 'Buy now  ' : 'Add to cart  ') + money(total());
    qtyEl.textContent = qty;
    var left = FREE_SHIP - total();
    shipTxt.innerHTML = left > 0
      ? 'You&rsquo;re <b>' + money(left) + '</b> away from free shipping'
      : '<b>You&rsquo;ve unlocked free shipping</b>';
    shipBar.style.width = Math.min(100, total() / FREE_SHIP * 100) + '%';
    subWrap.classList.toggle('on', sub);
    if(subSel) subSel.disabled = !sub;
    el.querySelectorAll('[data-satc-opt]').forEach(function(b){
      b.classList.toggle('on', sel[b.dataset.satcOpt] === b.dataset.satcVal);
    });
    el.querySelectorAll('[data-satc-selname]').forEach(function(sp){
      sp.textContent = sel[sp.dataset.satcSelname] + ' selected';
    });
    if(barPrice) barPrice.textContent = money(unit());
    if(barOpt) barOpt.textContent = optText();
  }

  function openPanel_(m){
    mode = m || 'cart';
    paint();
    el.classList.add('on');
    if(bar) bar.classList.remove('on');
    var o = document.querySelector('.ov'); if(o) o.classList.add('on');
    document.body.style.overflow = 'hidden';
  }
  function closePanel(){
    el.classList.remove('on');
    var o = document.querySelector('.ov'); if(o) o.classList.remove('on');
    document.body.style.overflow = '';
    sync();
  }
  window.cbCloseSATC = closePanel;

  if(bar) bar.addEventListener('click', function(e){
    var t = e.target.closest('[data-satcbar-open]');
    if(t) openPanel_(t.dataset.satcbarOpen);
  });

  el.addEventListener('click', function(e){
    var o = e.target.closest('[data-satc-opt]');
    if(o){ sel[o.dataset.satcOpt] = o.dataset.satcVal; paint(); return; }
    var q = e.target.closest('[data-satc-step]');
    if(q){ qty = Math.max(1, qty + (+q.dataset.satcStep)); paint(); return; }
    if(e.target.closest('[data-satc-sub]')){ sub = !sub; paint(); return; }
    if(e.target.closest('[data-satc-close]')){ closePanel(); return; }
    if(e.target.closest('[data-satc-cta]')){
      var freq = (sub && subSel) ? subSel.value : '';
      closePanel();
      addToCart({handle:p.handle,title:p.title,price:unit(),img:p.img,
                 opt:optText(), sub:freq, q:qty});
    }
  });

  /* the bar rides on the main Add to cart button leaving the viewport */
  function sync(){
    if(!bar || el.classList.contains('on')) return;
    var r = anchor ? anchor.getBoundingClientRect() : null;
    var visible = r && r.bottom > 0 && r.top < (window.innerHeight || 0);
    bar.classList.toggle('on', !visible);
  }
  if('IntersectionObserver' in window && anchor && bar){
    new IntersectionObserver(function(en){
      if(el.classList.contains('on')) return;
      bar.classList.toggle('on', !en[0].isIntersecting);
    }, {threshold: 0}).observe(anchor);
  }
  window.addEventListener('scroll', sync, {passive:true});
  window.addEventListener('resize', sync);
  paint(); sync();
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
        '<p class="price' + (p.cmp?'':' plain') + '" style="margin:0">' + money(p.price) + ' USD' +
        (p.cmp ? '<s>' + money(p.cmp) + ' USD</s>' : '') + '</p></a>';
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
  document.addEventListener('keydown', function(e){ if(e.key==='Escape'){ closeAll(); closeQuick(); } });
});
})();
"""
