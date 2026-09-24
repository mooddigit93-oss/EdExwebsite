/* ==========================================================================
   EdEx — comportements du site
   Mécaniques conservées du site de référence : rideau de transition, en-tête qui
   s'efface, hero orchestré + parallaxe, révélation de titres par lignes masquées,
   boutons à défilement de caractères, scroll fluide, pile de cartes qui se retournent.
   Tout est désactivé proprement si l'utilisateur demande moins de mouvement.
   ========================================================================== */
(function () {
  "use strict";

  var d = document, root = d.documentElement, body = d.body;
  var RM = root.classList.contains("rm") || window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var CFG = window.EDEX_CONFIG || {};
  var $ = function (s, c) { return (c || d).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };
  var hasGSAP = typeof window.gsap !== "undefined";
  if (hasGSAP && window.ScrollTrigger) gsap.registerPlugin(ScrollTrigger);

  window.__edex = true; // signal : le script a bien démarré (voir garde-fou dans <head>)

  /* ---------- Aperçu en local (file://) : liens de dossier -> index.html ---------- */
  if (location.protocol === "file:") {
    $$("a[href]").forEach(function (a) {
      var h = a.getAttribute("href");
      if (!h || /^([a-z]+:|#)/i.test(h)) return;
      var m = h.match(/^([^?#]*\/)?(\?[^#]*)?(#.*)?$/);
      if (m && (h.charAt(h.length - 1) === "/" || /\/(\?|#)/.test(h) || h === "." )) {
        a.setAttribute("href", (m[1] || "") + "index.html" + (m[2] || "") + (m[3] || ""));
      }
    });
  }

  /* ---------- Scroll fluide (Lenis) ---------- */
  var lenis = null;
  if (!RM && window.Lenis && hasGSAP) {
    lenis = new Lenis({ lerp: 0.12, wheelMultiplier: 1.05, smoothWheel: true });
    if (window.ScrollTrigger) lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
  }
  $$('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var id = a.getAttribute("href");
      if (id.length < 2) return;
      var t = $(id);
      if (!t) return;
      e.preventDefault();
      var bar = $(".tarif-bar");
      if (lenis) lenis.scrollTo(t, { offset: -(parseInt(getComputedStyle(root).getPropertyValue("--hh"), 10) || 80) - 16 - (bar ? bar.offsetHeight : 0) });
      else t.scrollIntoView({ behavior: RM ? "auto" : "smooth", block: "start" });
      history.replaceState(null, "", id);
      t.setAttribute("tabindex", "-1");
      t.focus({ preventScroll: true });
    });
  });

  /* ---------- Outils d'animation ---------- */
  function splitLines(el) {
    if (!window.SplitType) return null;
    var s = new SplitType(el, { types: "lines", lineClass: "split-line", tagName: "span" });
    s.lines.forEach(function (l) {
      var w = d.createElement("span");
      w.className = "line-mask";
      l.parentNode.insertBefore(w, l);
      w.appendChild(l);
    });
    return s;
  }

  /* ---------- Rideau de transition de page ---------- */
  var curtain = $(".curtain");
  var internal = function (a) {
    if (!a || a.target === "_blank" || a.hasAttribute("download")) return false;
    var h = a.getAttribute("href");
    if (!h || /^(mailto:|tel:|#|javascript:)/i.test(h)) return false;
    var u;
    try { u = new URL(a.href, location.href); } catch (e) { return false; }
    if (u.origin !== location.origin && location.protocol !== "file:") return false;
    if (u.protocol !== location.protocol) return false;
    if (u.pathname === location.pathname && u.search === location.search) return false;
    return true;
  };

  function startPage() {
    heroIntro();
    initReveals();
  }

  function initCurtain() {
    if (!curtain || RM) {
      if (curtain) curtain.hidden = true;
      root.removeAttribute("data-transitioning");
      return startPage();
    }
    // Départ : le rideau se ferme, puis on navigue
    d.addEventListener("click", function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      var a = e.target.closest && e.target.closest("a");
      if (!internal(a)) return;
      e.preventDefault();
      curtain.classList.remove("is-out", "is-first");
      curtain.classList.add("is-active");
      void curtain.offsetWidth;
      curtain.classList.add("is-in");
      try { sessionStorage.setItem("edex-t", "1"); } catch (err) {}
      setTimeout(function () { location.href = a.href; }, 650);
    });
    window.addEventListener("pageshow", function (e) {
      if (e.persisted) { curtain.classList.remove("is-in", "is-active", "is-out"); }
    });
    // Arrivée : le rideau s'ouvre puis le hero démarre (avec 330 ms d'avance sur la fin)
    var t = root.getAttribute("data-transitioning");
    if (!t) return startPage();
    try {
      sessionStorage.removeItem("edex-t");
      if (t === "first") sessionStorage.setItem("edex-seen", "1");
    } catch (e) {}
    curtain.classList.add("is-active");
    if (t === "first") curtain.classList.add("is-first");
    setTimeout(function () {
      curtain.classList.add("is-out");
      root.removeAttribute("data-transitioning");
      setTimeout(startPage, 330);
      setTimeout(function () { curtain.classList.remove("is-active", "is-out", "is-first"); }, 700);
    }, t === "first" ? 1100 : 60);
  }

  /* ---------- En-tête : état, masquage au scroll, menu plein écran ---------- */
  var header = $(".site-header");
  var burger = $(".burger");
  var menu = $("#menu");
  if (header) {
    var solid = header.classList.contains("is-solid");
    var last = 0;
    var onScroll = function () {
      var y = window.scrollY || window.pageYOffset;
      header.classList.toggle("is-scrolled", solid || y > 10);
      if (!body.classList.contains("menu-open") && y > window.innerHeight * 0.8 && y > last + 2) header.classList.add("is-hidden");
      else if (y < last - 2 || y <= window.innerHeight * 0.8) header.classList.remove("is-hidden");
      last = Math.max(0, y);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    header.addEventListener("focusin", function () { header.classList.remove("is-hidden"); });
  }
  if (burger && menu) {
    var links = $$("a", menu);
    menu.inert = true;
    var setMenu = function (open) {
      body.classList.toggle("menu-open", open);
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      burger.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
      menu.inert = !open;
      if (lenis) open ? lenis.stop() : lenis.start();
      if (open) setTimeout(function () { links[0] && links[0].focus(); }, 60);
      else burger.focus();
    };
    burger.addEventListener("click", function () { setMenu(!body.classList.contains("menu-open")); });
    d.addEventListener("keydown", function (e) {
      if (!body.classList.contains("menu-open")) return;
      if (e.key === "Escape") { setMenu(false); return; }
      if (e.key === "Tab") {
        var f = [burger].concat(links.filter(function (l) { return l.offsetParent !== null; }));
        var i = f.indexOf(d.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
      }
    });
    window.matchMedia("(min-width:1320px)").addEventListener("change", function (m) { if (m.matches && body.classList.contains("menu-open")) setMenu(false); });
  }

  /* ---------- Hero : révélation orchestrée + parallaxe ---------- */
  function heroIntro() {
    var els = $$("[data-hero]");
    if (!els.length) return;
    var title = $("[data-hero-title]");
    var rest = els.filter(function (e) { return e !== title; });
    if (RM || !hasGSAP) { els.forEach(function (e) { e.style.visibility = "visible"; }); return; }
    var split = title ? splitLines(title) : null;
    var tl = gsap.timeline({ defaults: { ease: "expo.out" } });
    els.forEach(function (e) { e.style.visibility = "visible"; });
    if (split) {
      gsap.set(split.lines, { yPercent: 118 });
      tl.to(split.lines, { yPercent: 0, duration: 1.25, stagger: 0.1, onComplete: function () { split.revert(); } });
    }
    if (rest.length) {
      gsap.set(rest, { autoAlpha: 0, y: 22 });
      tl.to(rest, { autoAlpha: 1, y: 0, duration: 0.95, stagger: 0.12 }, split ? "-=0.75" : 0);
    }
    var bg = $("[data-hero-bg]");
    var hero = $(".hero");
    if (bg && hero) {
      gsap.fromTo(bg, { scale: 1.06 }, { scale: 1, duration: 2, ease: "expo.out" });
      if (window.ScrollTrigger) gsap.to(bg, { yPercent: 10, ease: "none", scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true } });
    }
  }

  /* ---------- Titres : révélation par lignes masquées au scroll ---------- */
  function initReveals() {
    if (RM || !hasGSAP || !window.ScrollTrigger || !window.SplitType) return;
    var items = [];
    var prepare = function (el) {
      var s = splitLines(el);
      if (!s) return;
      gsap.set(s.lines, { yPercent: 118 });
      var it = { el: el, split: s, played: false };
      it.st = ScrollTrigger.create({
        trigger: el, start: "top 86%", once: true,
        onEnter: function () {
          it.played = true;
          gsap.to(s.lines, { yPercent: 0, duration: 1.1, ease: "expo.out", stagger: 0.08, onComplete: function () { s.revert(); } });
        }
      });
      items.push(it);
    };
    $$("[data-reveal]").forEach(prepare);
    var t;
    window.addEventListener("resize", function () {
      clearTimeout(t);
      t = setTimeout(function () {
        items.filter(function (i) { return !i.played; }).forEach(function (i) {
          i.st.kill(); i.split.revert();
          items.splice(items.indexOf(i), 1);
          prepare(i.el);
        });
        ScrollTrigger.refresh();
      }, 250);
    });
  }

  /* ---------- Boutons : texte à défilement de caractères ---------- */
  $$(".btn").forEach(function (btn) {
    var lab = $(".btn__label", btn);
    if (!lab || RM || !hasGSAP) return;
    var text = lab.textContent.replace(/\s+/g, " ").trim();
    lab.textContent = "";
    var sr = d.createElement("span"); sr.className = "sr-only"; sr.textContent = text;
    var mk = function (cls) {
      var r = d.createElement("span"); r.className = "btn__row " + cls; r.setAttribute("aria-hidden", "true");
      text.split("").forEach(function (c) { var s = d.createElement("span"); s.textContent = c === " " ? "\u00a0" : c; r.appendChild(s); });
      return r;
    };
    var a = mk(""), b = mk("btn__row--b");
    lab.appendChild(sr); lab.appendChild(a); lab.appendChild(b);
    var chars = $$("span", a).concat($$("span", b));
    var tl = gsap.timeline({ paused: true, defaults: { ease: "power3.inOut", duration: 0.5 } });
    tl.to(chars, { yPercent: -100, stagger: { each: 0.012, from: "start" } });
    btn.addEventListener("mouseenter", function () { tl.play(); });
    btn.addEventListener("mouseleave", function () { tl.reverse(); });
    btn.addEventListener("focus", function () { if (btn.matches(":focus-visible")) tl.play(); });
    btn.addEventListener("blur", function () { tl.reverse(); });
  });

  /* ---------- Pile de cartes qui se retournent ---------- */
  $$(".stack-card").forEach(function (card, i, all) {
    var front = $(".stack-face--front", card), back = $(".stack-face--back", card);
    var open = $("[data-flip]", card), close = $("[data-unflip]", card);
    if (!front || !back) return;
    back.inert = true;
    var set = function (flipped) {
      card.classList.toggle("is-flipped", flipped);
      front.inert = flipped; back.inert = !flipped;
      open.setAttribute("aria-expanded", flipped ? "true" : "false");
      setTimeout(function () { (flipped ? close : open).focus({ preventScroll: true }); }, RM ? 0 : 380);
    };
    open.addEventListener("click", function () { set(true); });
    close.addEventListener("click", function () { set(false); });
    if (!RM && hasGSAP && window.ScrollTrigger && i < all.length - 1) {
      gsap.to(card, {
        scale: 0.94, ease: "none",
        scrollTrigger: { trigger: all[i + 1], start: "top 82%", end: "top 24%", scrub: true }
      });
    }
  });

  /* ---------- Tarifs : bascule Licence / Master ---------- */
  var sw = $("[data-level-switch]");
  if (sw) {
    var fmt = function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, "\u00a0"); };
    var apply = function (lvl) {
      $$("[data-price]").forEach(function (el) { el.textContent = fmt(el.getAttribute("data-" + lvl)); });
      $$("[data-lvl-label]").forEach(function (el) { el.textContent = lvl === "master" ? "Master" : "Licence"; });
      $$("[data-svc-link]").forEach(function (a) {
        var base = a.getAttribute("data-svc-link");
        a.href = base + "&niveau=" + (lvl === "master" ? "Master" : "Licence");
      });
    };
    $$("input[name=level]", sw).forEach(function (r) { r.addEventListener("change", function () { apply(r.value); }); });
    var chk = $("input[name=level]:checked", sw);
    apply(chk ? chk.value : "licence");
  }

  /* ---------- Formulaires (diagnostic + contact) ---------- */
  var waUrl = function (msg) { return "https://wa.me/" + (CFG.whatsapp || "") + "?text=" + encodeURIComponent(msg); };
  var mailUrl = function (subject, msg) { return "mailto:" + (CFG.email || "") + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(msg); };
  var copyText = function (txt, btn) {
    var done = function () { var o = btn.textContent; btn.textContent = "Message copié"; setTimeout(function () { btn.textContent = o; }, 2200); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done, function () {});
    else { var ta = d.createElement("textarea"); ta.value = txt; d.body.appendChild(ta); ta.select(); try { d.execCommand("copy"); done(); } catch (e) {} ta.remove(); }
  };
  var setErr = function (field, msg) {
    var box = field.closest(".field, .fieldset");
    if (!box) return;
    var err = $(".error-msg", box);
    box.classList.toggle("has-error", !!msg);
    if (err) { err.textContent = msg || ""; err.hidden = !msg; }
    $$("input,textarea,select", box).forEach(function (i) { if (msg) i.setAttribute("aria-invalid", "true"); else i.removeAttribute("aria-invalid"); });
  };
  var val = function (form, name) {
    var f = form.elements[name];
    if (!f) return "";
    if (f.length !== undefined && f.tagName !== "SELECT") { var v = ""; Array.prototype.forEach.call(f, function (i) { if (i.checked) v = i.value; }); return v; }
    return (f.value || "").trim();
  };
  var validEmail = function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v); };
  var validPhone = function (v) { return v.replace(/\D/g, "").length >= 8; };

  var send = function (mode, form, subject, msg, btn, statusEl) {
    if (mode === "copy") return copyText(msg, btn);
    var url = mode === "wa" ? waUrl(msg) : mailUrl(subject, msg);
    window.open(url, mode === "wa" ? "_blank" : "_self", mode === "wa" ? "noopener" : "");
    if (statusEl) { statusEl.hidden = false; statusEl.textContent = mode === "wa" ? "WhatsApp s'ouvre avec votre message déjà rédigé : il vous suffit de l'envoyer." : "Votre messagerie s'ouvre avec votre message déjà rédigé : il vous suffit de l'envoyer."; }
  };
  var post = function (form, data, ok, ko) {
    var fd = new FormData(form);
    fetch(CFG.formEndpoint, { method: "POST", body: fd, headers: { Accept: "application/json" } })
      .then(function (r) { return r.ok ? ok() : ko(); }).catch(ko);
  };

  /* Diagnostic — 5 écrans, 8 rubriques du cahier */
  var diag = $("[data-diag]");
  if (diag) {
    var panels = $$(".panel", diag), bars = $$(".progress i", diag), plabel = $(".progress-label", diag);
    var cur = 0;
    var params = new URLSearchParams(location.search);
    var presta = params.get("prestation"), niveau = params.get("niveau");
    if (presta) {
      var bn = $("[data-presta-banner]", diag);
      if (bn) { bn.hidden = false; $("[data-presta-text]", bn).textContent = presta + (niveau ? " (" + niveau + ")" : ""); }
      var setRadio = function (name, v) { $$("input[name=" + name + "]", diag).forEach(function (i) { if (i.value === v) i.checked = true; }); };
      if (params.get("besoin")) setRadio("besoin", params.get("besoin"));
      if (params.get("situation")) setRadio("situation", params.get("situation"));
    }
    var show = function (n, focus) {
      cur = n;
      panels.forEach(function (p, i) { p.classList.toggle("is-current", i === n); });
      bars.forEach(function (b, i) { b.classList.toggle("is-done", i < n); b.classList.toggle("is-current", i === n); });
      plabel.textContent = "Étape " + (n + 1) + " sur " + panels.length;
      if (n === panels.length - 1) buildRecap();
      if (focus) { var h = $("h2", panels[n]); if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); } var top = diag.getBoundingClientRect().top + window.scrollY - 110; if (lenis) lenis.scrollTo(top, { immediate: RM }); else window.scrollTo({ top: top, behavior: RM ? "auto" : "smooth" }); }
    };
    var validate = function (n) {
      var ok = true, first = null;
      var bad = function (el, m) { setErr(el, m); ok = false; if (!first) first = el; };
      var f = diag;
      if (n === 0) {
        ["nom", "prenom"].forEach(function (k) { var el = f.elements[k]; if (!el.value.trim()) bad(el, "Ce champ est nécessaire."); else setErr(el, ""); });
        var em = f.elements.email, tel = f.elements.telephone;
        var hasE = em.value.trim(), hasT = tel.value.trim();
        if (!hasE && !hasT) { bad(tel, "Indiquez au moins un téléphone ou un e-mail."); setErr(em, ""); }
        else {
          if (hasT && !validPhone(hasT)) bad(tel, "Numéro de téléphone incomplet."); else setErr(tel, "");
          if (hasE && !validEmail(hasE)) bad(em, "Adresse e-mail invalide."); else if (hasE || hasT) setErr(em, "");
        }
      }
      if (n === 1) {
        ["situation", "besoin"].forEach(function (k) {
          var fs = $("[data-fs=" + k + "]", f);
          if (!val(f, k)) { bad(fs, "Choisissez une réponse."); } else setErr(fs, "");
        });
      }
      if (n === 2) {
        var ds = f.elements.description;
        if (ds.value.trim().length < 10) bad(ds, "Décrivez votre situation en quelques mots (10 caractères minimum)."); else setErr(ds, "");
      }
      if (first) { var target = first.matches && first.matches("input,textarea,select") ? first : $("input", first); if (target) target.focus(); }
      return ok;
    };
    var LABELS = [["Nom", "nom"], ["Prénom", "prenom"], ["Téléphone", "telephone"], ["E-mail", "email"], ["Situation", "situation"], ["Besoin", "besoin"], ["Description", "description"], ["Échéance", "echeance"], ["Urgence", "urgence"], ["Budget", "budget"], ["Canal préféré", "canal"]];
    var message = function () {
      var lines = ["Bonjour EdEx, voici mon diagnostic :", ""];
      if (presta) lines.push("Prestation demandée : " + presta + (niveau ? " (" + niveau + ")" : ""));
      LABELS.forEach(function (p) { var v = val(diag, p[1]); if (v) lines.push(p[0] + " : " + v); });
      lines.push("", "Merci de revenir vers moi après analyse de mon besoin.");
      return lines.join("\n");
    };
    var buildRecap = function () {
      var dl = $("[data-recap]", diag); dl.textContent = "";
      var rows = presta ? [["Prestation demandée", presta + (niveau ? " (" + niveau + ")" : "")]] : [];
      LABELS.forEach(function (p) { var v = val(diag, p[1]); if (v) rows.push([p[0], v]); });
      rows.forEach(function (r) { var w = d.createElement("div"), t = d.createElement("dt"), v = d.createElement("dd"); t.textContent = r[0]; v.textContent = r[1]; w.appendChild(t); w.appendChild(v); dl.appendChild(w); });
      var canal = val(diag, "canal");
      $$("[data-send]", diag).forEach(function (b) {
        var pref = (canal === "E-mail" && b.dataset.send === "mail") || (canal !== "E-mail" && b.dataset.send === "wa");
        if (b.dataset.send !== "copy") b.classList.toggle("btn--gold", pref), b.classList.toggle("btn--line", !pref);
      });
    };
    diag.addEventListener("click", function (e) {
      var n = e.target.closest("[data-next]"), p = e.target.closest("[data-prev]"), s = e.target.closest("[data-send]");
      if (n) { if (validate(cur)) show(cur + 1, true); }
      if (p) show(cur - 1, true);
      if (s) send(s.dataset.send, diag, "Diagnostic EdEx — " + val(diag, "prenom") + " " + val(diag, "nom"), message(), s, $("[data-send-status]", diag));
    });
    diag.addEventListener("submit", function (e) {
      e.preventDefault();
      if (val(diag, "website")) return; // anti-spam (champ piège)
      if (!CFG.formEndpoint) return;
      var btn = $("[data-submit]", diag); if (btn) btn.disabled = true;
      post(diag, null, function () {
        $("[data-diag-steps]", diag).hidden = true;
        var okb = $("[data-diag-done]", diag); okb.hidden = false; okb.setAttribute("tabindex", "-1"); okb.focus();
      }, function () { if (btn) btn.disabled = false; var st = $("[data-send-status]", diag); st.hidden = false; st.textContent = "L'envoi a échoué. Utilisez WhatsApp ou l'e-mail ci-dessous."; });
    });
    if (CFG.formEndpoint) { var sb = $("[data-submit]", diag); if (sb) sb.hidden = false; }
    var files = $("[data-files]", diag);
    if (files) { files.hidden = !CFG.formEndpoint; var fh = $("[data-files-hint]", diag); if (fh) fh.hidden = !!CFG.formEndpoint; }
    show(0, false);
  }

  /* Contact */
  var cf = $("[data-contact-form]");
  if (cf) {
    cf.addEventListener("submit", function (e) { e.preventDefault(); });
    cf.addEventListener("click", function (e) {
      var s = e.target.closest("[data-send]");
      if (!s) return;
      var ok = true;
      var nm = cf.elements.nom, rc = cf.elements.contact, ms = cf.elements.message;
      if (val(cf, "website")) return;
      if (!nm.value.trim()) { setErr(nm, "Ce champ est nécessaire."); ok = false; } else setErr(nm, "");
      var v = rc.value.trim();
      if (!v || !(validEmail(v) || validPhone(v))) { setErr(rc, "Indiquez un e-mail ou un téléphone valide."); ok = false; } else setErr(rc, "");
      if (ms.value.trim().length < 5) { setErr(ms, "Écrivez votre message."); ok = false; } else setErr(ms, "");
      if (!ok) { var f = $(".has-error input, .has-error textarea", cf); if (f) f.focus(); return; }
      var msg = "Bonjour EdEx,\n\n" + ms.value.trim() + "\n\nNom : " + nm.value.trim() + "\nContact : " + v;
      if (CFG.formEndpoint && s.dataset.send !== "copy" && s.dataset.send !== "wa" && s.dataset.send !== "mail") return;
      send(s.dataset.send, cf, "Message via le site EdEx — " + nm.value.trim(), msg, s, $("[data-send-status]", cf));
    });
  }

  /* ---------- Démarrage ---------- */
  var boot = function () { initCurtain(); };
  if (d.fonts && d.fonts.ready) d.fonts.ready.then(boot); else boot();
})();
