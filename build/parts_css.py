CSS = r"""
*,*::before,*::after{box-sizing:border-box}
:root{
  --ink:#000; --bg:#fff; --line:#e3e3e3; --muted:#6f6f6f; --soft:#f5f5f5;
  --teal:#04a788; --sale:#01a889; --maroon:#7c0147;
  --yellow:#ffba64;
  --ann-bg:#00638d; --ann-fg:#fdc733;
  --font:"Poppins",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --maxw:1260px; --gut:20px; --wgut:20px;
  --h-ls:0.14em; --btn-ls:0.1em;
  --barh:0px;
}
@media(min-width:1000px){:root{--gut:40px;--wgut:clamp(24px,3.2vw,62px)}}
html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:var(--font);font-weight:400;font-size:15px;line-height:1.7;
  color:var(--ink);background:var(--bg);overflow-x:hidden}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}
ul{margin:0;padding:0;list-style:none}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.wrap{max-width:var(--maxw);margin:0 auto;padding-inline:var(--gut)}
.wrap--wide{max-width:none;padding-inline:var(--wgut)}
.wrap--narrow{max-width:940px}
.wrap--pdp{max-width:1400px;padding-inline:var(--gut)}
.h{font-weight:600;text-transform:uppercase;letter-spacing:var(--h-ls);line-height:1.4}
.h1{font-size:clamp(22px,2.5vw,32px)}
.h2{font-size:clamp(17px,1.6vw,21px)}
.h3{font-size:16px}
.h5{font-size:15px}
.h6{font-size:13px}
.xxs{font-size:12px}
.sub{color:var(--muted)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;
  background:var(--ink);color:#fff;border:1px solid var(--ink);border-radius:0;
  padding:16px 34px;font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:var(--btn-ls);
  transition:opacity .2s;min-height:52px}
.btn:hover{opacity:.82}
.btn--ghost{background:transparent;color:var(--ink)}
.btn--light{background:#fff;color:#1c1c1c;border-color:#fff}
.btn--yellow{background:var(--yellow);border-color:var(--yellow);color:#fff}
.btn--full{width:100%}
.ulink{display:inline-block;border-bottom:1px solid currentColor;padding-bottom:3px;
  font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:var(--btn-ls)}
.tlink{border-bottom:1px solid currentColor;padding-bottom:1px}

/* ---------- password gate ---------- */
#gate{position:fixed;inset:0;z-index:9999;background:#fff;display:none;
  align-items:center;justify-content:center;padding:24px}
#gate.on{display:flex}
.gate-card{max-width:380px;width:100%;text-align:center}
.gate-card img{width:230px;margin:0 auto 28px}
.gate-card input{width:100%;padding:14px;border:1px solid var(--line);border-radius:0;
  font:inherit;font-size:14px;text-align:center;letter-spacing:.08em;margin-bottom:12px}
.gate-card input:focus{outline:none;border-color:var(--ink)}
.gate-err{color:#cb2b2b;font-size:12px;min-height:16px;margin-top:10px;
  text-transform:uppercase;letter-spacing:.1em}
body.locked{overflow:hidden}
body.locked .site{visibility:hidden}

/* ---------- announcement ---------- */
.ann{background:var(--ann-bg);color:var(--ann-fg);text-align:center;padding:14px 16px;
  font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:var(--h-ls);
  position:sticky;top:var(--barh);z-index:60;line-height:1.2}
@media(min-width:1000px){.ann{font-size:13px}}

/* ---------- header ---------- */
.hdr{position:sticky;top:calc(var(--barh) + var(--annh,44px));z-index:55;background:#fff;
  padding-top:18px}
@media(min-width:1000px){.hdr{padding-top:30px}}
.hdr__in{max-width:none;margin:0 auto;padding-inline:var(--wgut);
  display:grid;grid-template-areas:"burger logo icons";
  grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);align-items:center;gap:10px;
  padding-bottom:18px}
.hdr__logo{grid-area:logo;justify-self:center;margin:0}
.hdr__logo img{width:150px}
.hdr__burger{grid-area:burger;justify-self:start;display:flex;padding:4px}
.hdr__icons{grid-area:icons;justify-self:end;display:flex;align-items:center;gap:20px}
.hdr__icons a,.hdr__icons button{display:flex;align-items:center;position:relative;padding:2px}
.hdr__icons .loc{display:none;font-size:13px;font-weight:600;text-transform:uppercase;
  letter-spacing:var(--h-ls);align-items:center;gap:6px;color:var(--muted)}
.hdr__icons .acct{display:none}
.pnav{display:none}
@media(min-width:1000px){
  .hdr__in{grid-template-areas:". logo icons" "pnav pnav pnav";row-gap:26px;padding-bottom:0}
  .hdr__logo img{width:250px}
  .hdr__burger{display:none}
  .hdr__icons .loc{display:flex}
  .hdr__icons .acct{display:flex}
  .pnav{grid-area:pnav;display:flex;justify-content:center}
}
.pnav>ul{display:flex;flex-wrap:wrap;justify-content:center;gap:0 50px}
.pnav>ul>li{position:static}
.navtop{display:flex;align-items:center;gap:6px;font-size:14px;font-weight:600;
  text-transform:uppercase;letter-spacing:var(--h-ls);white-space:nowrap;
  padding:6px 0 22px;border-bottom:2px solid transparent}
.pnav>ul>li:hover>.navtop,.pnav>ul>li:focus-within>.navtop{border-color:var(--ink)}
.cartdot{position:absolute;top:0;right:-2px;width:7px;height:7px;border-radius:9999px;
  background:var(--ink);display:block}
.cartdot.num{width:auto;min-width:16px;height:16px;top:-4px;right:-7px;color:#fff;font-size:9px;
  font-weight:600;display:flex;align-items:center;justify-content:center;padding:0 4px;letter-spacing:0}

/* mega menu - a single centred row of links */
.mega{position:absolute;left:0;right:0;top:100%;background:#fff;
  box-shadow:0 14px 24px -18px rgb(0 0 0 / .25);
  opacity:0;visibility:hidden;transition:.16s ease;z-index:54}
.pnav>ul>li:hover>.mega,.pnav>ul>li:focus-within>.mega{opacity:1;visibility:visible}
.mega__in{padding:26px var(--wgut) 30px;display:flex;flex-wrap:wrap;justify-content:center;gap:16px 42px}
.mega__in a{font-size:14px;font-weight:600;text-transform:uppercase;letter-spacing:var(--h-ls);
  white-space:nowrap}
.mega__in a:hover{opacity:.55}

/* ---------- overlays ---------- */
.ov{position:fixed;inset:0;background:rgb(0 0 0 / .35);opacity:0;visibility:hidden;
  transition:.25s;z-index:90}
.ov.on{opacity:1;visibility:visible}
.panel{position:fixed;top:0;bottom:0;width:min(460px,92vw);background:#fff;z-index:95;
  display:flex;flex-direction:column;transition:transform .3s ease}
.panel--l{left:0;transform:translateX(-100%)}
.panel--r{right:0;transform:translateX(100%)}
.panel.on{transform:none}
.panel__hd{display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding:26px 30px 22px;flex:0 0 auto}
.panel__hd .h{font-size:17px;letter-spacing:.16em}
.panel__bd{flex:1 1 auto;overflow-y:auto;padding:0 30px}
.panel__ft{flex:0 0 auto;padding:18px 30px 26px;background:#fff;border-top:1px solid var(--line)}

/* mobile drawer drill-down */
.dd{position:relative;overflow:hidden;height:100%}
.dd__view{position:absolute;inset:0;overflow-y:auto;background:#fff;padding:8px 30px 30px;
  transition:transform .28s ease}
.dd__view.sub{transform:translateX(100%)}
.dd__view.sub.on{transform:none}
.dd__item{display:flex;align-items:center;justify-content:space-between;width:100%;
  padding:16px 0;border-bottom:1px solid var(--line);
  font-size:14px;font-weight:600;text-transform:uppercase;letter-spacing:var(--h-ls);text-align:left}
.dd__back{display:flex;align-items:center;gap:8px;padding:8px 0 18px;font-size:12px;
  font-weight:600;text-transform:uppercase;letter-spacing:var(--h-ls);color:var(--muted)}

/* ---------- predictive search panel ---------- */
.search{position:fixed;left:0;right:0;background:#fff;z-index:96;
  border-top:1px solid var(--line);box-shadow:0 20px 30px -24px rgb(0 0 0 / .3);
  opacity:0;visibility:hidden;transform:translateY(-8px);transition:.22s ease;
  max-height:76vh;overflow-y:auto}
.search.on{opacity:1;visibility:visible;transform:none}
.search__in{padding:0 var(--wgut) 40px}
.search__row{display:flex;align-items:center;gap:14px;border-bottom:1px solid var(--line);
  padding:18px 0}
.search__row input{flex:1;border:0;font:inherit;font-size:17px;padding:6px 0;background:none}
.search__row input:focus{outline:none}
.search__res{display:grid;gap:26px;padding-top:22px}
@media(min-width:1000px){.search__res{grid-template-columns:220px minmax(0,1fr);gap:60px}}
.search__hd{font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:var(--h-ls);
  color:var(--muted);padding-bottom:12px;border-bottom:1px solid var(--line);margin:0 0 18px}
.search__tabwrap{border-bottom:1px solid var(--line);margin-bottom:22px}
.search__tab{display:inline-block;font-size:12px;font-weight:600;text-transform:uppercase;
  letter-spacing:var(--h-ls);border-bottom:2px solid var(--ink);padding-bottom:11px;margin-bottom:-1px}
.search__sug{display:grid;gap:14px;font-size:15px}
.search__sug b{font-weight:600}
.search__tiles{display:grid;grid-template-columns:repeat(2,1fr);gap:22px}
@media(min-width:800px){.search__tiles{grid-template-columns:repeat(4,1fr)}}

/* ---------- product card ---------- */
.grid{display:grid;gap:56px 26px;grid-template-columns:repeat(2,minmax(0,1fr))}
@media(min-width:1000px){.grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:80px 40px}}
.grid--4{grid-template-columns:repeat(2,minmax(0,1fr));gap:40px 20px}
@media(min-width:1000px){.grid--4{grid-template-columns:repeat(4,minmax(0,1fr));gap:54px 30px}}
.pc{position:relative}
.pc__fig{position:relative;background:var(--soft);overflow:hidden}
.pc__fig img{width:100%;aspect-ratio:1;object-fit:cover;transition:opacity .35s}
.pc__fig img.sec{position:absolute;inset:0;opacity:0}
.pc:hover .pc__fig img.sec{opacity:1}
.pc__rev{position:absolute;left:8px;bottom:8px;z-index:2;display:inline-flex;align-items:center;
  gap:4px;background:rgb(255 255 255 / .94);border:1px solid var(--line);
  backdrop-filter:blur(3px);color:var(--ink);
  font-size:11px;font-weight:600;line-height:1;letter-spacing:.02em;padding:5px 8px;
  white-space:nowrap;pointer-events:none}
.pc__rev i{font-style:normal;font-weight:400;color:var(--muted)}
@media(min-width:760px){.pc__rev{left:10px;bottom:10px;font-size:12px;padding:6px 10px}}
.badge{position:absolute;top:8px;left:8px;z-index:2;background:var(--sale);color:#fff;
  font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;padding:7px 13px}
.pc__info{margin-top:26px;display:grid;justify-items:center;gap:10px;text-align:center}
.pc__title{font-size:14px;font-weight:600;text-transform:uppercase;letter-spacing:.12em;line-height:1.5}
.price{display:flex;align-items:baseline;gap:10px;justify-content:center;flex-wrap:wrap;
  font-size:14px;font-weight:600;letter-spacing:.06em;color:var(--sale);text-transform:uppercase}
.price.plain{color:var(--muted)}
.price s{color:var(--muted);font-weight:600;white-space:nowrap}
.price b{font-weight:600;white-space:nowrap}
.pc__add{width:100%;margin-top:6px;padding:13px 14px;font-size:12px;min-height:46px}

/* ---------- sections ---------- */
.sec{padding-block:clamp(40px,5vw,74px)}
.sec--tight{padding-block:clamp(26px,3vw,44px)}
.bleed{position:relative}
.bleed img{width:100%;display:block}
.scrollcue{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);z-index:3;
  width:42px;height:42px;border-radius:9999px;background:rgb(255 255 255/.9);
  display:grid;place-items:center}
.intro{max-width:1000px;margin:0 auto;text-align:center;font-size:13px;font-weight:600;
  text-transform:uppercase;letter-spacing:var(--h-ls);line-height:1.9}
.sec__title{text-align:center;margin:0 0 40px}
.rail{display:flex;gap:30px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;
  padding-bottom:4px}
.rail::-webkit-scrollbar{display:none}
.rail>*{flex:0 0 calc(50% - 15px);scroll-snap-align:start}
@media(min-width:1000px){.rail>*{flex:0 0 calc(25% - 23px)}}
.arrows{display:flex;gap:10px;justify-content:center;margin-top:30px}
.arrows button{width:38px;height:38px;border:1px solid var(--line);display:grid;place-items:center}
.arrows button:hover{border-color:var(--ink)}

/* press band */
.band{padding-block:clamp(40px,4.5vw,62px)}
.band--maroon{background:var(--maroon);color:#fff}
.band--teal{background:var(--teal);color:#fff}
.press{display:grid;gap:36px;text-align:center;align-items:start}
@media(min-width:1000px){.press{grid-template-columns:repeat(3,1fr);gap:60px}}
.press blockquote{margin:0;font-size:clamp(14px,1.15vw,16px);line-height:1.75}
.press img{height:26px;width:auto;margin:26px auto 0;object-fit:contain}

/* overlay banner */
.ovb{position:relative;display:grid;min-height:clamp(340px,29vw,470px)}
.ovb>img{grid-area:1/1;width:100%;height:100%;object-fit:cover}
.ovb::after{content:"";grid-area:1/1;background:rgb(255 255 255 / .34);pointer-events:none}
.ovb--dark::after{background:rgb(0 0 0 / .3)}
.ovb__t{grid-area:1/1;position:relative;z-index:2;display:grid;align-content:center;
  justify-items:center;text-align:center;padding:32px;gap:16px;max-width:820px;margin:0 auto}
.ovb__t .h1,.ovb__t .h6,.ovb__t p{margin:0}
.ovb__t p.lede{max-width:560px;font-size:14px;line-height:1.8}

/* split image + text */
.split{display:grid;align-items:center}
@media(min-width:900px){.split{grid-template-columns:1fr 1fr}}
.split img{width:100%;height:100%;object-fit:cover;min-height:280px}
.split__t{padding:clamp(28px,4vw,70px)}
.split__t h2{margin:0 0 18px}
.split__t p{margin:0 0 14px;font-size:15px;line-height:1.8}

/* UGC rail */
.ugc{display:flex;gap:16px;overflow-x:auto;scrollbar-width:none}
.ugc::-webkit-scrollbar{display:none}
.ugc__card{flex:0 0 200px;position:relative}
.ugc__card>img{aspect-ratio:9/14;object-fit:cover;background:var(--soft)}
.ugc__tag{display:flex;align-items:center;gap:9px;margin-top:10px}
.ugc__tag img{width:34px;height:34px;object-fit:cover;background:var(--soft)}
.ugc__tag p{margin:0;font-size:11px;line-height:1.35}
.ugc__tag span{display:block;color:var(--muted)}
.ugc__play{position:absolute;top:10px;right:10px;width:26px;height:26px;border-radius:9999px;
  background:rgb(0 0 0/.45);color:#fff;display:grid;place-items:center}

/* before/after */
.ba{position:relative;overflow:hidden;user-select:none;touch-action:pan-y;margin:0 auto}
.ba img{width:100%;display:block}
.ba__after{position:absolute;inset:0;overflow:hidden;width:50%}
.ba__after img{position:absolute;top:0;left:0;height:auto;max-width:none}
.ba__handle{position:absolute;top:0;bottom:0;left:50%;width:2px;background:#fff;z-index:3;cursor:ew-resize}
.ba__handle::after{content:"";position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:38px;height:38px;border-radius:9999px;background:#fff;box-shadow:0 2px 10px rgb(0 0 0/.25)}
.ba__lbl{position:absolute;bottom:16px;z-index:4;color:#fff;font-size:11px;font-weight:600;
  text-transform:uppercase;letter-spacing:var(--h-ls);text-shadow:0 1px 6px rgb(0 0 0/.5)}

/* slideshow */
.slider{position:relative}
.slider__track{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}
.slider__track::-webkit-scrollbar{display:none}
.slider__track>*{flex:0 0 100%;scroll-snap-align:center}
.dots{display:flex;gap:9px;justify-content:center;padding:18px 0 0}
.dots button{width:8px;height:8px;border-radius:9999px;background:var(--line)}
.dots button.on{background:var(--ink)}

/* ---------- footer ---------- */
.ft{background:var(--teal);color:#fff;padding-block:clamp(44px,4.5vw,68px)}
.ft__grid{display:grid;gap:38px}
@media(min-width:900px){.ft__grid{grid-template-columns:1.55fr 1fr 1fr 1.25fr;gap:44px}}
.ft p.h6{margin:0 0 24px;font-size:13px;letter-spacing:.14em}
.ft li{margin-bottom:14px;font-size:15px}
.ft li a:hover{opacity:.75}
.ft__about{font-size:15px;line-height:1.8;margin:0}
.ft__form{display:grid;gap:22px;justify-items:start;margin-top:20px}
.ft__form input{width:100%;padding:15px 16px;border:1px solid rgb(255 255 255/.45);
  background:transparent;color:#fff;font:inherit;font-size:15px}
.ft__form input::placeholder{color:rgb(255 255 255/.85)}
.ft__form input:focus{outline:none;border-color:#fff}
.ft__soc{display:flex;gap:38px;margin-top:44px}
.ft__aside{margin-top:44px;display:grid;gap:20px;align-items:center;font-size:13px;
  font-weight:600;letter-spacing:var(--h-ls);text-transform:uppercase}
@media(min-width:900px){.ft__aside{grid-template-columns:1fr auto 1fr}}
.ft__loc{display:flex;align-items:center;gap:10px}
.ft__loc img{width:24px;height:17px;object-fit:cover}
.ft__cc{text-align:center}
.ft__pay{display:flex;flex-wrap:wrap;gap:7px;justify-content:flex-start}
@media(min-width:900px){.ft__pay{justify-content:flex-end;max-width:430px;margin-left:auto}}
.ft__pay span{width:40px;height:26px;background:#fff;border-radius:4px;display:grid;
  place-items:center;font-size:7px;font-weight:700;letter-spacing:0;
  text-transform:none;overflow:hidden;line-height:1;padding:0 2px;text-align:center}

/* ---------- cart drawer ---------- */
.ci{display:grid;grid-template-columns:88px 1fr;gap:18px;padding:22px 0}
.ci+.ci{border-top:1px solid var(--line)}
.ci img{width:88px;aspect-ratio:1;object-fit:cover;background:var(--soft)}
.ci__t{font-size:14px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;line-height:1.5}
.ci__p{font-size:15px;color:var(--muted);margin-top:6px}
.ci__o{font-size:13px;color:var(--muted);margin-top:6px;text-transform:uppercase;letter-spacing:.06em}
.ci__sub{font-size:15px;margin-top:6px}
.ci__row{display:flex;align-items:center;gap:20px;margin-top:14px;flex-wrap:wrap}
.qty{display:inline-flex;align-items:center;border:1px solid var(--line)}
.qty button{width:38px;height:42px;display:grid;place-items:center;font-size:15px}
.qty span{min-width:34px;text-align:center;font-size:15px}
.cart__div{border-top:1px solid var(--line)}
.ml{padding:26px 0 30px}
.ml h4{margin:0 0 20px;font-size:12px;font-weight:600;text-transform:uppercase;
  letter-spacing:var(--h-ls);color:var(--muted)}
.ml__row{display:grid;grid-template-columns:66px 1fr;gap:18px;align-items:center}
.ml__row img{width:66px;aspect-ratio:1;object-fit:cover;background:var(--soft)}
.ml__row p{margin:0}
.cart__note{margin:0 0 16px;font-size:14px;color:var(--teal)}
.cart__co{display:flex;align-items:center;justify-content:center;gap:14px;width:100%;
  background:var(--ink);color:#fff;padding:20px;font-size:14px;font-weight:600;
  text-transform:uppercase;letter-spacing:var(--btn-ls)}
.empty{text-align:center;padding:60px 0;color:var(--muted);font-size:13px;
  text-transform:uppercase;letter-spacing:var(--h-ls)}

/* ---------- variant modal ---------- */
.modal{position:fixed;inset:0;z-index:97;display:none;align-items:center;justify-content:center;padding:20px}
.modal.on{display:flex}
.modal__bg{position:absolute;inset:0;background:rgb(0 0 0/.45)}
.modal__card{position:relative;background:#fff;width:min(760px,100%);max-height:90vh;overflow-y:auto;
  display:grid;grid-template-columns:1fr;z-index:2}
@media(min-width:700px){.modal__card{grid-template-columns:300px 1fr}}
.modal__img{background:var(--soft)}
.modal__img img{width:100%;aspect-ratio:1;object-fit:cover}
.modal__body{padding:30px}
.modal__close{position:absolute;top:12px;right:14px;z-index:3;width:32px;height:32px;
  display:grid;place-items:center;background:#fff}
.opt{margin-top:22px}
.opt>p{margin:0 0 10px;font-size:12px;text-transform:uppercase;letter-spacing:var(--h-ls);color:var(--muted)}
.opt__row{display:flex;flex-wrap:wrap;gap:9px}
.opt__row button{border:1px solid var(--line);padding:11px 16px;font-size:12px;font-weight:600;
  text-transform:uppercase;letter-spacing:var(--btn-ls)}
.opt__row button.on{border-color:var(--ink);background:var(--ink);color:#fff}
.stars{display:inline-flex;gap:2px;color:#000;font-size:12px;letter-spacing:1px}

/* ---------- PLP ---------- */
.ctool{border-block:1px solid var(--line);position:sticky;
  top:calc(var(--barh) + var(--annh,44px) + var(--hdrh,120px));z-index:40;background:#fff}
.ctool__in{display:flex;justify-content:flex-end}
.ctool__in button{padding:20px 34px;font-size:14px;font-weight:600;text-transform:uppercase;
  letter-spacing:var(--h-ls);color:var(--muted);display:flex;align-items:center;gap:10px;
  border-left:1px solid var(--line);min-width:200px;justify-content:center}
.ctool__in button:hover{color:var(--ink)}
.sheet{position:fixed;right:0;top:0;bottom:0;width:min(420px,92vw);background:#fff;z-index:95;
  transform:translateX(100%);transition:transform .3s ease;display:flex;flex-direction:column}
.sheet.on{transform:none}
.fgroup{padding:6px 0 16px}
.fgroup>p{margin:0 0 14px;font-size:12px;font-weight:600;text-transform:uppercase;
  letter-spacing:var(--h-ls);color:var(--muted)}
.fopt{display:flex;align-items:center;gap:12px;padding:9px 0;font-size:15px;cursor:pointer}
.fopt input{width:16px;height:16px;accent-color:#000}
.achips{display:flex;flex-wrap:wrap;gap:9px;margin-bottom:30px}
.achips button{border:1px solid var(--ink);padding:8px 14px;font-size:11px;font-weight:600;
  text-transform:uppercase;letter-spacing:var(--h-ls);display:flex;gap:8px;align-items:center}
.sortopt{display:block;width:100%;text-align:left;padding:14px 0;font-size:15px;
  border-bottom:1px solid var(--line)}
.sortopt.on{font-weight:600}

/* ---------- PDP ---------- */
.pdp{display:grid;gap:34px}
@media(min-width:1000px){.pdp{grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:70px;align-items:start}}
.gal{display:grid;gap:16px}
@media(min-width:1000px){.gal{grid-template-columns:64px minmax(0,1fr)}}
.gal__thumbs{display:none;gap:12px;overflow-y:auto;scrollbar-width:none}
.gal__thumbs::-webkit-scrollbar{display:none}
@media(min-width:1000px){.gal__thumbs{display:grid;grid-auto-rows:64px}}
.gal__thumbs button{border:1px solid transparent;padding:0;overflow:hidden;height:64px}
.gal__thumbs button.on{border-color:var(--ink)}
.gal__thumbs img{width:100%;height:100%;object-fit:cover;background:var(--soft)}
.gal__main{position:relative}
.gal__mrail{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}
.gal__mrail::-webkit-scrollbar{display:none}
.gal__mrail img{flex:0 0 100%;scroll-snap-align:center;width:100%;aspect-ratio:1;object-fit:contain}
@media(min-width:1000px){.gal__mrail{display:block}.gal__mrail img{display:none}.gal__mrail img.on{display:block}}
.pinfo{display:grid;align-content:start}
.pinfo__top{display:flex;align-items:flex-start;justify-content:space-between;gap:24px}
.pinfo h1{margin:0;font-size:clamp(16px,1.4vw,19px)}
.pinfo__price{font-size:17px;font-weight:600;white-space:nowrap}
.pinfo .rr{display:flex;align-items:center;gap:10px;margin-top:14px}
.pinfo .afterpay{margin:18px 0 0;font-size:14px;color:#333;display:flex;align-items:center;
  gap:7px;flex-wrap:wrap}
.pinfo .afterpay b{font-weight:600}
.chipdark{background:#000;color:#fff;font-size:11px;padding:3px 8px;font-weight:600}
.pinfo .lede{font-size:15px;line-height:1.8;margin:22px 0 0}
.subs{display:grid;gap:10px;margin-top:24px}
.subs label{display:flex;align-items:center;gap:12px;border:1px solid var(--line);
  padding:15px 16px;font-size:14px;cursor:pointer}
.subs label.on{border-color:var(--ink);background:#fafafa}
.subs input{accent-color:#000;width:16px;height:16px}
.subs .sp{margin-left:auto;font-weight:600}
.subs .tiny{font-size:12px;color:var(--muted);padding-left:2px}
.qtyrow{margin-top:24px}
.acc{margin-top:8px}
.acc details{border-bottom:1px solid var(--line)}
.acc summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;
  gap:14px;padding:20px 0;font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:var(--h-ls)}
.acc summary::-webkit-details-marker{display:none}
.acc summary i{font-style:normal;font-size:17px;line-height:1;transition:transform .2s}
.acc details[open] summary i{transform:rotate(45deg)}
.acc__c{padding:0 0 22px;font-size:15px;line-height:1.8}
.acc__c p{margin:0 0 14px}
.acc__c ul{list-style:disc;padding-left:20px;margin:0 0 14px}
.acc__c li{margin-bottom:7px}
.wyl{display:grid;grid-template-columns:repeat(2,1fr);gap:22px;justify-items:center}
@media(min-width:800px){.wyl{grid-template-columns:repeat(5,1fr)}}
.wyl div{text-align:center}
.wyl span{width:88px;height:88px;background:var(--teal);color:#fff;display:grid;place-items:center;
  margin:0 auto 14px}
.wyl p{margin:0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:var(--h-ls)}
.vidcard{display:flex;align-items:center;gap:16px;margin-top:14px}
.vidcard>div{position:relative;width:118px}
.vidcard img{width:118px;aspect-ratio:3/4;object-fit:cover;background:var(--soft)}
.vidcard i{position:absolute;inset:0;display:grid;place-items:center}
.vidcard i b{width:34px;height:34px;border-radius:9999px;background:rgb(255 255 255/.9);
  display:grid;place-items:center}

/* ---------- shop by category ---------- */
.cats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px 14px}
@media(min-width:760px){.cats{grid-template-columns:repeat(6,minmax(0,1fr));gap:28px 22px}}
.cat{display:block;text-align:center}
.cat__fig{position:relative;display:block}
.cat img{width:100%;aspect-ratio:1;object-fit:cover;background:var(--soft);transition:opacity .25s}
.cat:hover img{opacity:.82}
.cat__from{position:absolute;left:8px;bottom:8px;background:rgb(255 255 255 / .94);
  color:var(--ink);font-size:10px;font-weight:600;text-transform:uppercase;
  letter-spacing:.08em;padding:5px 9px;line-height:1.2;white-space:nowrap}
@media(min-width:760px){.cat__from{left:10px;bottom:10px;font-size:11px;padding:6px 11px}}
.cat p{margin:14px 0 0;font-size:11px;font-weight:600;text-transform:uppercase;
  letter-spacing:var(--h-ls);line-height:1.5}
@media(min-width:760px){.cat p{font-size:12px;margin-top:16px}}

/* ---------- pairs well with (under the PDP buy button) ---------- */
.pw-wrap{margin:26px 0 4px;border-top:1px solid var(--line);padding-top:20px;min-width:0}
.pw-hd{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:14px}
.pw-hd h2{margin:0}
.pw-arr{display:flex;gap:8px;flex:0 0 auto}
.pw-arr button{width:30px;height:30px;border:1px solid var(--line);display:grid;place-items:center;
  background:#fff;transition:border-color .2s}
.pw-arr button:hover{border-color:var(--ink)}
.pw-arr svg{width:12px;height:12px}
.pw-rail{gap:14px;min-width:0}
.pw-rail>*{flex:0 0 148px;scroll-snap-align:start}
.pw{display:flex;flex-direction:column}
.pw__fig{display:block;background:var(--soft);aspect-ratio:1/1;overflow:hidden}
.pw__fig img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s}
.pw:hover .pw__fig img{transform:scale(1.04)}
.pw__title{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;
  margin:10px 0 0;font-size:12px;font-weight:600;line-height:1.45;
  text-decoration:none;color:var(--ink)}
.pw__title:hover{text-decoration:underline}
.pw__price{display:block;margin-top:4px;font-size:12px;font-weight:600}
.pw__opt{display:block;margin:2px 0 10px;min-height:15px;font-size:10px;color:var(--muted);
  text-transform:uppercase;letter-spacing:.06em;white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis}
.pw__add{margin-top:auto;width:100%;min-height:38px;padding:9px 10px;
  border:1px solid var(--ink);background:#fff;color:var(--ink);cursor:pointer;
  font-family:inherit;font-size:10px;font-weight:600;text-transform:uppercase;
  letter-spacing:var(--btn-ls);transition:background .2s,color .2s}
.pw__add:hover:not(:disabled){background:var(--ink);color:#fff}
.pw__add:disabled{border-color:var(--line);color:var(--muted);cursor:not-allowed}
@media(max-width:760px){
  .pw-rail>*{flex:0 0 136px}
  .pw-wrap{margin-top:22px}
}

/* ---------- sticky bar (PDP trigger) ---------- */
.satcbar{position:fixed;left:0;right:0;bottom:0;z-index:86;background:#fff;
  border-top:1px solid var(--line);box-shadow:0 -10px 28px -20px rgb(0 0 0 / .45);
  transform:translateY(100%);transition:transform .3s cubic-bezier(.22,.7,.3,1);
  visibility:hidden}
.satcbar.on{transform:none;visibility:visible}
.satcbar__in{display:flex;align-items:center;gap:16px;padding:10px var(--wgut)}
.satcbar__img{width:38px;height:38px;object-fit:cover;background:var(--soft);flex:0 0 auto}
.satcbar__t{flex:1 1 auto;min-width:0}
.satcbar__t p{margin:0;font-size:13px;font-weight:600;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis}
.satcbar__t span{display:block;font-size:12px;color:var(--muted);white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis}
.satcbar__price{flex:0 0 auto;font-size:15px;font-weight:600}
.satcbar__act{flex:0 0 auto;display:flex;gap:10px}
.satcbar__act .btn{min-height:44px;padding:12px 24px;font-size:12px}
@media(max-width:760px){
  .satcbar__in{flex-wrap:wrap;gap:10px 12px;padding:10px 16px calc(10px + env(safe-area-inset-bottom))}
  .satcbar__t p{font-size:12px}
  .satcbar__t span{font-size:11px}
  .satcbar__price{font-size:14px}
  .satcbar__act{width:100%;gap:8px}
  .satcbar__act .btn{flex:1;padding:12px 8px;min-height:46px}
}

/* ---------- sticky add-to-cart panel (PDP) ---------- */
.satc{position:fixed;z-index:93;background:#fff;border:1px solid var(--line);
  box-shadow:0 18px 44px -18px rgb(0 0 0 / .3);
  left:50%;bottom:24px;transform:translateX(-50%) translateY(calc(100% + 40px));
  width:min(560px,calc(100vw - 40px));
  display:flex;flex-direction:column;overflow:visible;
  transition:transform .34s cubic-bezier(.22,.7,.3,1),opacity .24s;opacity:0;
  pointer-events:none;visibility:hidden}
.satc.on{transform:translateX(-50%) translateY(0);opacity:1;pointer-events:auto;visibility:visible}
.satc__in{flex:1 1 auto;overflow:visible;padding:22px 24px 4px}
.satc__foot{flex:0 0 auto;padding:14px 24px 20px;background:#fff;border-top:1px solid var(--line)}
.satc__close{position:absolute;top:12px;right:12px;width:30px;height:30px;border-radius:9999px;
  border:1px solid var(--line);display:grid;place-items:center;background:#fff;z-index:2}
.satc__close:hover{border-color:var(--ink)}
.satc__hd{display:grid;grid-template-columns:78px 1fr;gap:16px;align-items:start;
  padding-right:34px;margin-bottom:18px}
.satc__hd img{width:78px;aspect-ratio:1;object-fit:cover;background:var(--soft)}
.satc__hd h3{margin:0 0 8px;font-size:16px}
.satc__rate{display:flex;align-items:center;gap:8px;margin:0 0 8px;font-size:12px;color:var(--muted)}
.satc__price{margin:0;font-size:19px;font-weight:600}
.satc__grp{margin-bottom:16px}
.satc__lbl{display:flex;align-items:baseline;gap:9px;margin:0 0 9px}
.satc__lbl b{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:var(--h-ls)}
.satc__lbl span{font-size:12px;color:var(--muted)}
.satc__opts{display:flex;flex-wrap:wrap;gap:9px}
.satc__opts button{border:1px solid var(--line);padding:11px 17px;font-size:12px;font-weight:600;
  min-width:64px;line-height:1.25}
.satc__opts button small{display:block;font-size:9px;font-weight:500;color:var(--muted);
  text-transform:uppercase;letter-spacing:.06em;margin-top:2px}
.satc__opts button:hover{border-color:var(--ink)}
.satc__opts button.on{background:var(--ink);border-color:var(--ink);color:#fff}
.satc__opts button.on small{color:rgb(255 255 255 / .7)}
.satc__qty{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:18px}
.satc__ship{border:1px solid var(--line);padding:12px 14px;margin-bottom:16px}
.satc__ship p{margin:0 0 9px;font-size:12px;color:var(--muted)}
.satc__ship p b{color:var(--ink);font-weight:600}
.satc__bar{display:block;height:5px;background:var(--soft);position:relative;overflow:hidden}
.satc__bar i{position:absolute;inset:0 auto 0 0;background:var(--teal);width:0;transition:width .3s}
.satc__sub{display:flex;align-items:center;gap:14px;flex-wrap:wrap;
  border:1px solid var(--line);padding:13px 14px;margin-bottom:12px}
.satc__sub.on{border-color:var(--teal);background:rgb(4 167 136 / .06)}
.satc__sub label{display:flex;align-items:center;gap:11px;font-size:13px;cursor:pointer;flex:1;min-width:170px}
.satc__sub label b{font-weight:600}
.satc__sw{width:42px;height:24px;border-radius:9999px;background:var(--line);position:relative;
  flex:0 0 auto;transition:background .2s}
.satc__sw::after{content:"";position:absolute;top:3px;left:3px;width:18px;height:18px;
  border-radius:9999px;background:#fff;transition:transform .2s;box-shadow:0 1px 3px rgb(0 0 0/.3)}
.satc__sub.on .satc__sw{background:var(--teal)}
.satc__sub.on .satc__sw::after{transform:translateX(18px)}
.satc__sub select{border:1px solid var(--line);padding:9px 11px;font:inherit;font-size:12px;
  background:#fff;border-radius:0}
.satc__sub select:disabled{opacity:.45}
.satc__cta{display:flex;align-items:center;justify-content:center;gap:14px;width:100%;
  background:var(--ink);color:#fff;padding:18px;font-size:13px;font-weight:600;
  text-transform:uppercase;letter-spacing:var(--btn-ls)}
.satc__cta:hover{opacity:.85}
@media(max-width:760px){
  .satc{left:0;right:0;bottom:0;width:100%;max-width:none;border-left:0;border-right:0;border-bottom:0;
    transform:translateY(100%)}
  .satc.on{transform:translateY(0)}
  .satc__in{padding:20px 18px 4px}
  .satc__foot{padding:12px 18px calc(16px + env(safe-area-inset-bottom))}
  .satc__hd{grid-template-columns:64px 1fr;gap:13px}
  .satc__hd img{width:64px}
}

/* short viewports: compact the panel rather than scroll it */
@media (max-height:700px){
  .satc{bottom:14px}
  .satc__in{padding:16px 20px 2px}
  .satc__foot{padding:11px 20px 15px}
  .satc__hd{grid-template-columns:60px 1fr;gap:13px;margin-bottom:13px}
  .satc__hd img{width:60px}
  .satc__hd h3{font-size:14px;margin-bottom:6px}
  .satc__rate{margin:7px 0 5px}
  .satc__price{font-size:17px}
  .satc__grp{margin-bottom:11px}
  .satc__lbl{margin-bottom:7px}
  .satc__opts button{padding:9px 14px}
  .satc__qty{margin-bottom:12px}
  .satc__ship{padding:9px 12px;margin-bottom:11px}
  .satc__sub{padding:10px 12px;margin-bottom:12px}
  .satc__cta{padding:15px}
}
@media (max-height:580px){
  .satc__hd{grid-template-columns:46px 1fr;gap:11px;margin-bottom:10px}
  .satc__hd img{width:46px}
  .satc__ship{display:none}
  .satc__in{padding:13px 18px 2px}
  .satc__grp,.satc__qty,.satc__sub{margin-bottom:9px}
}

/* index hub */
.hub{min-height:100vh;display:grid;place-items:center;padding:60px 20px;background:var(--soft)}
.hub__in{max-width:980px;width:100%;text-align:center}
.hub__in>img{width:250px;margin:0 auto 14px}
.hub__grid{display:grid;gap:18px;margin-top:40px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}
.hub__card{background:#fff;border:1px solid var(--line);padding:28px 24px;text-align:left;display:block}
.hub__card:hover{border-color:var(--ink)}
.hub__card p{margin:0 0 8px;font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:var(--h-ls)}
.hub__card span{font-size:14px;color:var(--muted);line-height:1.6}
.hub__note{margin-top:38px;font-size:13px;color:var(--muted)}
"""
