/* Charith Sulakshana — portfolio behaviour
   Smooth scroll (Lenis) + GSAP ScrollTrigger. Each side of the site gets its own
   animation context, which is thrown away when you switch sides. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var root = document.documentElement;
  var body = document.body;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasG = typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';
  if (hasG) gsap.registerPlugin(ScrollTrigger);

  var mains = { design: $('#design'), analyst: $('#analyst') };
  var mode = root.dataset.boot === 'analyst' ? 'analyst' : 'design';
  var ctx = null, mm = null, cleanups = [], busy = false;

  /* ---------- Smooth scroll ---------- */
  var lenis = null;
  if (!reduce && typeof window.Lenis !== 'undefined') {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true, wheelMultiplier: 0.95 });
    if (hasG) {
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
      gsap.ticker.lagSmoothing(0);
    } else {
      var raf = function (t) { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
  }
  function navH() { return ($('.nav') || {}).offsetHeight || 64; }
  function scrollToY(target, immediate) {
    if (lenis) lenis.scrollTo(target, { offset: typeof target === 'number' ? 0 : -(navH() + 8), immediate: !!immediate, duration: 1.3 });
    else {
      var y = typeof target === 'number' ? target : target.getBoundingClientRect().top + window.scrollY - navH() - 8;
      window.scrollTo({ top: y, behavior: immediate || reduce ? 'auto' : 'smooth' });
    }
  }

  /* ---------- Nav state + progress ---------- */
  var nav = $('.nav'), bar = $('.progress i');
  function onScroll() {
    var y = window.scrollY, max = document.documentElement.scrollHeight - window.innerHeight;
    nav.classList.toggle('on', y > 30);
    if (bar) bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, y / max) : 0) + ')';
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- Switch ---------- */
  var switchEl = $('.switch'), switchBtns = $$('.switch button'), switchBar = $('.switch__bar');
  function placeBar() {
    var b = switchBtns.filter(function (x) { return x.dataset.mode === mode; })[0];
    if (!b || !switchBar) return;
    switchBar.style.setProperty('--bx', b.offsetLeft + 'px');
    switchBar.style.setProperty('--bw', b.offsetWidth + 'px');
  }
  switchBtns.forEach(function (b) {
    b.addEventListener('click', function () { switchMode(b.dataset.mode); });
  });
  window.addEventListener('resize', placeBar);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { placeBar(); if (hasG) ScrollTrigger.refresh(); });

  function applyMode(m) {
    mode = m;
    body.dataset.mode = m;
    delete root.dataset.boot;
    mains.design.hidden = m !== 'design';
    mains.analyst.hidden = m !== 'analyst';
    switchBtns.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.mode === m)); });
    var hello = $('[data-contact]');
    if (hello) hello.setAttribute('href', m === 'design' ? '#d-contact' : '#a-contact');
    var tc = $('meta[name="theme-color"]');
    if (tc) tc.setAttribute('content', m === 'design' ? '#0C0F11' : '#F3F4F5');
    $('.skip').setAttribute('href', '#' + m);
    try { history.replaceState(null, '', m === 'analyst' ? '#analyst' : location.pathname + location.search); } catch (e) {}
    placeBar();
    scrollToY(0, true);
    window.scrollTo(0, 0);
    build(m);
    onScroll();
  }

  function switchMode(m) {
    if (m === mode || busy) return;
    if (reduce || !hasG) { applyMode(m); return; }
    busy = true;
    var w = $('.wipe'), lab = $('[data-wipe-label]');
    lab.textContent = m === 'design' ? 'Creative Designer' : 'Business Analyst';
    if (lenis) lenis.stop();
    gsap.timeline({ onComplete: function () { busy = false; if (lenis) lenis.start(); } })
      .set(w, { transformOrigin: '50% 100%', scaleY: 0 })
      .to(w, { scaleY: 1, duration: 0.55, ease: 'power3.inOut' })
      .to(lab, { autoAlpha: 1, duration: 0.2 }, '-=0.12')
      .add(function () { applyMode(m); })
      .to(lab, { autoAlpha: 0, duration: 0.2 }, '+=0.3')
      .set(w, { transformOrigin: '50% 0%' })
      .to(w, { scaleY: 0, duration: 0.6, ease: 'power3.inOut' });
  }

  /* ---------- Helpers ---------- */
  function splitTitle(h) {
    if (!h || h.dataset.split) return;
    h.dataset.split = '1';
    var label = h.textContent.replace(/\s+/g, ' ').trim();
    h.setAttribute('aria-label', label);
    $$('.split', h).forEach(function (line) {
      var t = line.textContent;
      line.textContent = '';
      line.setAttribute('aria-hidden', 'true');
      t.split('').forEach(function (ch) {
        var s = document.createElement('span');
        s.textContent = ch;
        line.appendChild(s);
      });
    });
  }
  function count(el, to, dur) {
    var o = { v: 0 };
    return gsap.to(o, { v: to, duration: dur || 1.4, ease: 'power2.out', onUpdate: function () { el.textContent = Math.round(o.v); } });
  }

  /* ---------- Per-mode animation ---------- */
  function build(m) {
    if (ctx) ctx.revert();
    if (mm) mm.revert();
    cleanups.forEach(function (f) { f(); });
    cleanups = [];
    if (!hasG) { root.classList.add('ready'); return; }
    var main = mains[m];
    $$('.cover__title', main).forEach(splitTitle);

    ctx = gsap.context(function () {
      if (reduce) { gsap.set('.cover__copy > *, .cover__art', { autoAlpha: 1 }); return; }
      if (m === 'design') designCover(main); else analystCover(main);

      // Chapter headers: crop marks close in, then the title rises
      $$('.ch-head', main).forEach(function (h) {
        var tl = gsap.timeline({ scrollTrigger: { trigger: h, start: 'top 85%', once: true } });
        tl.from($$('.crop', h), { autoAlpha: 0, x: function (i) { return i % 2 ? -26 : 26; }, y: function (i) { return i < 2 ? 26 : -26; }, duration: 0.9, ease: 'expo.out' })
          .from($$('.ch-row, .ch-kicker', h), { autoAlpha: 0, y: 12, duration: 0.6, stagger: 0.06 }, 0.1)
          .from($('.ch-title', h), { autoAlpha: 0, yPercent: 35, duration: 1.1, ease: 'expo.out' }, 0.15)
          .from($$('.ch-intro, .ch-meta', h), { autoAlpha: 0, y: 18, duration: 0.8, stagger: 0.08, ease: 'power3.out' }, 0.35);
      });

      // Generic blocks
      $$('.reveal', main).forEach(function (el) {
        if (el.classList.contains('ch-head')) return;
        gsap.from(el, { autoAlpha: 0, y: 36, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 88%', once: true } });
      });

      // Work, in batches as it scrolls in
      var items = $$('.fig, .g-astro li, .g-sanju li', main).filter(function (el) { return !el.closest('.ntg'); });
      gsap.set(items, { autoAlpha: 0, y: 44 });
      ScrollTrigger.batch(items, {
        start: 'top 92%', once: true,
        onEnter: function (b) { gsap.to(b, { autoAlpha: 1, y: 0, duration: 0.95, ease: 'power3.out', stagger: 0.07, overwrite: true }); }
      });

      // Slow drift inside the big frames
      $$('.g-logos .shot, .bella-boards .shot', main).forEach(function (s) {
        var im = $('img', s);
        s.classList.add('par');
        gsap.fromTo(im, { yPercent: -2, scale: 1.05 }, { yPercent: 2, scale: 1.05, ease: 'none', scrollTrigger: { trigger: s, start: 'top bottom', end: 'bottom top', scrub: true } });
      });

      // Counters
      $$('[data-count]', main).forEach(function (el) {
        var to = +el.dataset.count;
        el.textContent = '0';
        ScrollTrigger.create({ trigger: el, start: 'top 90%', once: true, onEnter: function () { count(el, to, 1.6); } });
      });

      // Process bars grow in
      $$('[data-flow]', main).forEach(function (f) {
        gsap.from($$('.bar i', f), { scaleX: 0, transformOrigin: '0 50%', duration: 1.1, ease: 'power3.out', stagger: 0.08, scrollTrigger: { trigger: f, start: 'top 80%', once: true } });
      });
    }, main);

    mm = gsap.matchMedia();
    mm.add('(min-width: 901px) and (prefers-reduced-motion: no-preference)', function () {
      // Calendar pages start as a pile and spread into a row
      $$('[data-fan]', main).forEach(function (list) {
        var lis = $$('li', list), mid = Math.floor(lis.length / 2);
        lis.forEach(function (li, i) { li.style.zIndex = String(lis.length - Math.abs(i - mid)); });
        gsap.timeline({ scrollTrigger: { trigger: list, start: 'top 85%', end: 'top 30%', scrub: 0.6, invalidateOnRefresh: true } })
          .fromTo(lis, {
            x: function (i, el) { return lis[mid].offsetLeft - el.offsetLeft; },
            y: function (i) { return Math.abs(i - mid) * -6; },
            rotation: function (i) { return (i - mid) * 3.2; }
          }, { x: 0, y: 0, rotation: 0, duration: 1, ease: 'power2.inOut' })
          .fromTo($$('.label', list), { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.2, stagger: 0.03 }, 0.85);
      });
    });
    mm.add('(max-width: 900px)', function () {
      $$('[data-fan]', main).forEach(function (list) {
        gsap.from(list, { autoAlpha: 0, x: 60, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: list, start: 'top 90%', once: true } });
      });
    });

    root.classList.add('ready');
    requestAnimationFrame(function () { ScrollTrigger.refresh(); });
  }

  /* ---------- Designer cover: the C, drawn then exploded ---------- */
  function designCover(main) {
    var cover = $('.cover', main), draw = $('[data-draw]', main), stack = $('[data-stack]', main);
    if (!cover || !draw || !stack) return;
    var lines = $$('.draw__lines circle, .draw__lines rect, .draw__lines line, .draw__lines path', draw);
    var labels = $$('.draw__lines text', draw);
    var layers = $$('.layer', stack).filter(function (l) { return !l.classList.contains('outline'); });
    var outline = $('.outline', stack);
    var Z = layers.map(function (l) { return +l.dataset.z || 0; });
    var OZ = +outline.dataset.z || 31;
    var st = { px: 0, py: 0, sp: 0, open: 0 };

    function render() {
      var spread = 1 + st.sp * 3.2;
      gsap.set(stack, { rotationY: -20 + st.px * 12 - st.sp * 22, rotationX: 13 - st.py * 9 + st.sp * 16 });
      layers.forEach(function (l, i) { gsap.set(l, { z: Z[i] * st.open * spread }); });
      gsap.set(outline, { z: OZ * st.open * spread + st.sp * 60 });
    }

    lines.forEach(function (el) {
      var len = 0;
      try { len = el.getTotalLength(); } catch (e) { len = 1200; }
      gsap.set(el, { strokeDasharray: len, strokeDashoffset: len });
    });
    gsap.set(labels, { autoAlpha: 0 });
    gsap.set(layers, { autoAlpha: 0 });
    gsap.set(outline, { strokeDashoffset: 837, autoAlpha: 1 });
    gsap.set($$('.cover__copy > *', main), { autoAlpha: 0, y: 24 });
    gsap.set($$('.cover__title .split > span', main), { yPercent: 110 });
    gsap.set($('.cover__title', main), { autoAlpha: 1, y: 0 });
    gsap.set($('.cover__art', main), { autoAlpha: 1 });
    gsap.set($('.cover__index', main), { autoAlpha: 0 });
    render();

    var tl = gsap.timeline({ delay: busy ? 0.75 : 0.25 });
    tl.to(lines, { strokeDashoffset: 0, duration: 1.5, ease: 'power2.inOut', stagger: 0.07 }, 0)
      .to(labels, { autoAlpha: 1, duration: 0.5, stagger: 0.1 }, 0.9)
      .to(outline, { strokeDashoffset: 0, duration: 1.4, ease: 'power2.inOut' }, 0.5)
      .to(layers, { autoAlpha: 1, duration: 0.4, stagger: 0.025 }, 1.1)
      .to(st, { open: 1, duration: 1.4, ease: 'expo.out', onUpdate: render }, 1.25)
      .to($$('.cover__title .split > span', main), { yPercent: 0, duration: 1.1, ease: 'expo.out', stagger: 0.035 }, 0.2)
      .to($$('.cover__copy > *:not(.cover__title)', main), { autoAlpha: 1, y: 0, duration: 0.9, ease: 'power3.out', stagger: 0.08 }, 0.55)
      .to($('.cover__index', main), { autoAlpha: 1, duration: 0.8 }, 1.4);

    // Scroll: the C comes apart into its layers, like an exploded drawing
    ScrollTrigger.create({
      trigger: cover, start: 'top top', end: 'bottom top', scrub: true,
      onUpdate: function (self) { st.sp = self.progress; render(); }
    });
    gsap.to($('.draw__lines', main), { autoAlpha: 0.25, ease: 'none', scrollTrigger: { trigger: cover, start: 'top top', end: 'bottom top', scrub: true } });
    gsap.to($('.cover__copy', main), { y: -70, ease: 'none', scrollTrigger: { trigger: cover, start: 'top top', end: 'bottom top', scrub: true } });

    // Pointer tilt (mouse) or a slow idle sway (touch)
    if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
      var onMove = function (e) {
        gsap.to(st, { px: (e.clientX / window.innerWidth - 0.5) * 2, py: (e.clientY / window.innerHeight - 0.5) * 2, duration: 1, ease: 'power3.out', overwrite: 'auto', onUpdate: render });
      };
      window.addEventListener('pointermove', onMove, { passive: true });
      cleanups.push(function () { window.removeEventListener('pointermove', onMove); });
    } else {
      gsap.fromTo(st, { px: -0.35 }, { px: 0.35, duration: 4.5, ease: 'sine.inOut', yoyo: true, repeat: -1, onUpdate: render });
    }
  }

  /* ---------- Analyst cover: the report settles flat as you scroll ---------- */
  function analystCover(main) {
    var cover = $('.cover', main), screen = $('[data-screen]', main);
    if (!cover || !screen) return;
    var small = window.innerWidth <= 900;
    var ry = small ? -8 : -14, rx = small ? 4 : 6;
    gsap.set($$('.cover__copy > *', main), { autoAlpha: 0, y: 24 });
    gsap.set($$('.cover__title .split > span', main), { yPercent: 110 });
    gsap.set($('.cover__title', main), { autoAlpha: 1, y: 0 });
    gsap.set($('.cover__art', main), { autoAlpha: 1 });
    gsap.set(screen, { transformOrigin: '0% 50%', rotationY: ry, rotationX: rx });
    var tl = gsap.timeline({ delay: busy ? 0.75 : 0.25 });
    tl.to($$('.cover__title .split > span', main), { yPercent: 0, duration: 1.1, ease: 'expo.out', stagger: 0.03 }, 0)
      .to($$('.cover__copy > *:not(.cover__title)', main), { autoAlpha: 1, y: 0, duration: 0.9, ease: 'power3.out', stagger: 0.08 }, 0.35)
      .from(screen, { rotationY: ry - 26, rotationX: rx + 8, x: 80, autoAlpha: 0, duration: 1.6, ease: 'expo.out' }, 0.2)
      .from($('.screen__note', main), { autoAlpha: 0, duration: 0.6 }, 1.1);
    gsap.to(screen, { rotationY: 0, rotationX: 0, scale: small ? 1 : 1.03, ease: 'none', scrollTrigger: { trigger: cover, start: 'top top', end: 'bottom 35%', scrub: true } });
    gsap.to($('.cover__copy', main), { y: -60, ease: 'none', scrollTrigger: { trigger: cover, start: 'top top', end: 'bottom top', scrub: true } });
  }

  /* ---------- Tabs (Thinex report pages) ---------- */
  $$('.tabs').forEach(function (t) {
    var tabs = $$('[data-tab]', t), panes = $$('[data-pane]', t);
    function select(i, focus) {
      tabs.forEach(function (b, j) { b.setAttribute('aria-selected', String(i === j)); b.tabIndex = i === j ? 0 : -1; });
      panes.forEach(function (p, j) { p.hidden = i !== j; });
      if (focus) tabs[i].focus();
      if (hasG && !reduce) gsap.fromTo(panes[i], { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.5, ease: 'power2.out' });
      if (hasG) ScrollTrigger.refresh();
    }
    tabs.forEach(function (b, i) {
      b.tabIndex = i === 0 ? 0 : -1;
      b.addEventListener('click', function () { select(i); });
      b.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') { e.preventDefault(); select((i + 1) % tabs.length, true); }
        if (e.key === 'ArrowLeft') { e.preventDefault(); select((i - 1 + tabs.length) % tabs.length, true); }
      });
    });
  });

  /* ---------- Before / after process ---------- */
  $$('[data-flow]').forEach(function (f) {
    var btns = $$('[data-state]', f), total = $('[data-total]', f), rows = $$('.flow__rows li', f);
    var cur = 180;
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var s = b.dataset.state, sum = 0;
        btns.forEach(function (x) { var on = x === b; x.classList.toggle('on', on); x.setAttribute('aria-pressed', String(on)); });
        rows.forEach(function (li) {
          var v = +(s === 'a' ? li.dataset.a : li.dataset.b);
          sum += v;
          $('.bar i', li).style.setProperty('--w', (v / 60 * 100).toFixed(1) + '%');
          $('.min', li).textContent = v + 'm';
          var em = $('em', li); if (em) em.textContent = s === 'a' ? 'fixed' : 'bottleneck';
        });
        f.classList.toggle('after', s === 'a');
        if (hasG && !reduce) {
          var o = { v: cur };
          gsap.to(o, { v: sum, duration: 0.9, ease: 'power2.out', onUpdate: function () { total.textContent = Math.round(o.v); } });
        } else total.textContent = sum;
        cur = sum;
      });
    });
  });

  /* ---------- Reel ---------- */
  $$('[data-reel]').forEach(function (v) {
    var frame = v.parentNode, btn = $('[data-reel-btn]', frame), userPaused = false;
    function sync() { var p = !v.paused; frame.classList.toggle('playing', p); btn.textContent = p ? 'Pause' : 'Play'; }
    v.addEventListener('play', sync); v.addEventListener('pause', sync);
    btn.addEventListener('click', function () {
      if (v.paused) { userPaused = false; v.play().catch(function () {}); } else { userPaused = true; v.pause(); }
    });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting && e.intersectionRatio > 0.1) v.preload = 'auto';
          if (e.intersectionRatio >= 0.55 && !reduce && !userPaused) v.play().catch(function () {});
          else if (e.intersectionRatio < 0.55 && !v.paused) v.pause();
        });
      }, { threshold: [0, 0.1, 0.55, 1] }).observe(v);
    }
  });

  /* ---------- Lightbox ---------- */
  var lb = $('.lb'), lbImg = $('[data-lb-img]'), lbCap = $('[data-lb-cap]'), lbCount = $('[data-lb-count]');
  var set = [], idx = 0, lastFocus = null;
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function show(i) {
    idx = (i + set.length) % set.length;
    var s = set[idx], im = $('img', s);
    lbImg.src = s.dataset.src;
    lbImg.alt = im ? im.alt : '';
    lbCap.innerHTML = s.dataset.cap || '';
    lbCount.textContent = pad(idx + 1) + ' / ' + pad(set.length);
    var nx = set[(idx + 1) % set.length];
    if (nx) { var pre = new Image(); pre.src = nx.dataset.src; }
    var multi = set.length > 1;
    $('[data-lb-prev]').hidden = !multi; $('[data-lb-next]').hidden = !multi;
  }
  function openLb(shot) {
    var g = shot.dataset.gallery;
    set = $$('.shot[data-gallery="' + g + '"]', mains[mode]);
    lastFocus = shot;
    show(set.indexOf(shot));
    lb.hidden = false;
    requestAnimationFrame(function () { lb.classList.add('open'); });
    if (lenis) lenis.stop();
    body.style.overflow = 'hidden';
    $('[data-lb-close]').focus();
  }
  function closeLb() {
    lb.classList.remove('open');
    setTimeout(function () { lb.hidden = true; lbImg.removeAttribute('src'); }, 250);
    if (lenis) lenis.start();
    body.style.overflow = '';
    if (lastFocus) lastFocus.focus({ preventScroll: true });
  }
  document.addEventListener('click', function (e) {
    var shot = e.target.closest('.shot[data-src]');
    if (shot) { e.preventDefault(); openLb(shot); }
  });
  $('[data-lb-close]').addEventListener('click', closeLb);
  $('[data-lb-prev]').addEventListener('click', function () { show(idx - 1); });
  $('[data-lb-next]').addEventListener('click', function () { show(idx + 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
  document.addEventListener('keydown', function (e) {
    if (lb.hidden) return;
    if (e.key === 'Escape') closeLb();
    else if (e.key === 'ArrowRight') show(idx + 1);
    else if (e.key === 'ArrowLeft') show(idx - 1);
    else if (e.key === 'Tab') {
      var f = $$('button:not([hidden])', lb);
      var a = f.indexOf(document.activeElement);
      e.preventDefault();
      f[(a + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus();
    }
  });
  var tx = 0, ty = 0;
  lb.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; ty = e.touches[0].clientY; }, { passive: true });
  lb.addEventListener('touchend', function (e) {
    var dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) show(idx + (dx < 0 ? 1 : -1));
    else if (dy > 90 && Math.abs(dy) > Math.abs(dx)) closeLb();
  }, { passive: true });

  /* ---------- Anchors ---------- */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = a.getAttribute('href').slice(1);
    if (a.hasAttribute('data-top') || id === 'top' || id === '') { e.preventDefault(); scrollToY(0); return; }
    if (a.classList.contains('skip')) return;
    var t = document.getElementById(id);
    if (t && !t.closest('[hidden]')) { e.preventDefault(); scrollToY(t); }
  });

  /* ---------- Copy email ---------- */
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var wrap = b.closest('.contact'), mail = $('[data-email]', wrap).textContent.trim(), msg = $('[data-copymsg]', wrap);
      function done(ok) { msg.textContent = ok ? 'Copied' : 'Select the address to copy'; setTimeout(function () { msg.textContent = ''; }, 2400); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(mail).then(function () { done(true); }, function () { fallback(); });
      else fallback();
      function fallback() {
        try {
          var r = document.createRange(); r.selectNodeContents($('[data-email]', wrap));
          var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
          done(document.execCommand('copy'));
        } catch (err) { done(false); }
      }
    });
  });

  $$('[data-year]').forEach(function (y) { y.textContent = new Date().getFullYear(); });

  /* ---------- Boot ---------- */
  if (mode === 'analyst') applyMode('analyst');
  else { body.dataset.mode = 'design'; placeBar(); build('design'); onScroll(); }
})();
