# -*- coding: utf-8 -*-
"""Génère toutes les pages statiques du site EdEx.
Sources de contenu : Cahier de contenu V2 (pages, pôles, tarifs, contacts) et Livre de marque.
Usage : python3 _build/build.py   (depuis la racine du site)
"""
import os, html, urllib.parse
from PIL import Image

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT_DIR)

WA = "2290142016326"
MAIL = "edexcorporation229@gmail.com"
PHONE = "01\u00a042\u00a001\u00a063\u00a026"
SOCIAL = "EdEx-Corporation"

LOGO_W, LOGO_H = Image.open("assets/img/logo-white.webp").size
HAS_HERO_IMG = os.path.exists("assets/img/hero.jpg")

import re
def _fr(t):
    t = re.sub(r" ([?!;:»])", "\u00a0\\1", t)
    return t.replace("« ", "«\u00a0")
esc = lambda t: _fr(html.escape(t, quote=False))
attr = lambda t: html.escape(t, quote=True)
NB = "\u00a0"


def money(n):
    return f"{n:,}".replace(",", NB)


# ---------------------------------------------------------------- composants
def star(cls=""):
    return f'<svg class="star {cls}" viewBox="0 0 60 100" aria-hidden="true" focusable="false"><use href="#star"/></svg>'


def arrow_icon():
    return '<svg viewBox="0 0 14 12" aria-hidden="true" focusable="false"><use href="#arrow"/></svg>'


def btn(label, href, kind="gold", small=False, extra=""):
    cls = f"btn btn--{kind}" + (" btn--sm" if small else "")
    return (f'<a class="{cls}" href="{attr(href)}"{(" " + extra) if extra else ""}><span class="btn__label">{esc(label)}</span>'
            f'<span class="btn__icon" aria-hidden="true">{arrow_icon()}{arrow_icon()}</span></a>')


def btnb(label, kind="gold", extra="", small=False):
    cls = f"btn btn--{kind}" + (" btn--sm" if small else "")
    return (f'<button type="button" class="{cls}" {extra}><span class="btn__label">{esc(label)}</span>'
            f'<span class="btn__icon" aria-hidden="true">{arrow_icon()}{arrow_icon()}</span></button>')


def link_arrow(label):
    return f'<span class="link-arrow"><span>{esc(label)}</span><span class="ic" aria-hidden="true">{arrow_icon()}</span></span>'


def eyebrow(text):
    return f'<p class="eyebrow">{star()}<span>{esc(text)}</span></p>'


STATUS = {"ops": ("Opérationnel", "badge--ops"), "dev": ("En développement", "badge--dev"), "vision": ("Vision à terme", "badge--vision")}


def badge(st, label=None):
    l, c = STATUS[st]
    return f'<span class="badge {c}">{esc(label or l)}</span>'


def P(t):
    return f"<p>{esc(t)}</p>"


def UL(items):
    return '<ul class="dash-list">' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def PH(t):
    return f'<span class="placeholder">[{esc(t)}]</span>'


# ---------------------------------------------------------------- données
NAV = [("", "Accueil"), ("qui-sommes-nous/", "Qui sommes-nous ?"), ("ecosysteme/", "Notre écosystème"),
       ("comment-ca-marche/", "Comment ça marche ?"), ("prestations/", "Prestations & tarifs"),
       ("diagnostic/", "Diagnostic"), ("contact/", "Contact")]

POLES = [
    dict(n=1, slug="pole-1", title="Éducation", status="dev", public="Élèves et lycéens préparant notamment le CEP, le BEPC ou le BAC.",
         cta="Découvrir le pôle", kind="Enfant / élève",
         lede="Accompagner les jeunes élèves dans leur parcours scolaire et dans leur recherche de réussite aux différents examens.",
         desc="Pôle 1 EdEx — Éducation : accompagnement des élèves et lycéens (CEP, BEPC, BAC) vers de meilleures méthodes d’apprentissage. Pôle en développement."),
    dict(n=2, slug="pole-2", title="Jeune adulte post-bac", status="ops", public="Étudiants et jeunes adultes en parcours universitaire, notamment en fin de cycle.",
         cta="Découvrir nos prestations", kind="Étudiant / jeune adulte",
         lede="Accompagner les étudiants dans la dernière étape de leur parcours universitaire : méthodologie, statistiques, rédaction et soutenance du mémoire.",
         desc="Pôle 2 EdEx — Jeune adulte post-bac : accompagnement du mémoire et de la soutenance (méthodologie, statistiques, chapitre 3, PowerPoint, coaching). Pôle opérationnel."),
    dict(n=3, slug="pole-3", title="Insertion professionnelle et incubation de projets", status="dev", public="Jeunes diplômés et porteurs de projets.",
         cta="Découvrir notre vision", kind="Jeune diplômé et porteur de projet",
         lede="Une passerelle entre les jeunes diplômés et les opportunités professionnelles, et un accompagnement pour transformer une idée en projet structuré.",
         desc="Pôle 3 EdEx — Insertion professionnelle et incubation de projets : première expérience professionnelle et structuration d’un projet. Pôle en développement."),
    dict(n=4, slug="pole-4", title="Entrepreneuriat & développement professionnel", status="dev", public="Entreprises déjà en activité, PME, grandes entreprises et acteurs opérationnels.",
         cta="Découvrir notre approche", kind="Professionnel / entrepreneur / organisation",
         lede="Accompagner les entreprises déjà lancées dans l’amélioration de leur fonctionnement, de leur organisation et de leur performance.",
         desc="Pôle 4 EdEx — Entrepreneuriat & développement professionnel : audit, optimisation des processus, marketing et prospection pour les entreprises en activité. Pôle en développement."),
    dict(n=5, slug="pole-5", title="EdEx Private Equity", status="vision", public="Porteurs de projets et entrepreneurs présentant des projets structurés à potentiel de développement.",
         cta="Découvrir notre vision", kind="Projets à potentiel",
         lede="Une ambition à plus long terme : permettre à des projets à potentiel de disposer des ressources nécessaires pour devenir des activités concrètes.",
         desc="Pôle 5 EdEx — EdEx Private Equity : vision à terme d’accompagnement de projets à potentiel par la mise à disposition de ressources. Ce pôle n’est pas encore accessible."),
]

# Blocs de contenu des pages de pôles : (titre, [éléments])  — éléments : ("p", txt) ("ul", [..]) ("notice", txt) ("badge", st, label) ("btn", label, href)
POLE_BLOCKS = {
    1: [
        ("Public cible", [("p", "Élèves et lycéens préparant notamment le CEP, le BEPC ou le BAC.")]),
        ("Vocation", [
            ("notice", "Pôle en cours de développement : les éléments ci-dessous décrivent l’offre envisagée."),
            ("p", "Le Pôle 1 a pour vocation d’accompagner les jeunes élèves dans leur parcours scolaire et dans leur recherche de réussite aux différents examens."),
            ("p", "L’objectif d’EdEx ne consiste cependant pas uniquement à aider l’élève à obtenir une bonne note ou à réussir un examen. L’examen constitue une étape concrète permettant de développer chez l’enfant de meilleures méthodes d’apprentissage, davantage d’autonomie et de confiance dans ses capacités."),
        ]),
        ("Offre envisagée", [
            ("p", "Le pôle reposera notamment sur :"),
            ("ul", ["la mise en place d’un programme personnel de révision et d’apprentissage ;",
                    "un accompagnement permettant à l’élève de savoir quoi apprendre, comment travailler et à quel rythme progresser ;",
                    "l’intervention éventuelle d’un maître d’étude chargé de suivre physiquement l’élève ;",
                    "une plateforme numérique intégrant des fonctionnalités d’intelligence artificielle ;",
                    "la possibilité de charger ses cours afin de bénéficier de révisions intelligentes et interactives ;",
                    "le traitement et l’exploitation d’épreuves des années antérieures ;",
                    "des fonctionnalités permettant de suivre la progression de l’élève ;",
                    "un espace ou système permettant aux parents de suivre l’évolution de leur enfant."]),
            ("p", "L’accompagnement sera conçu selon une logique semi-directive : l’élève conserve une part d’autonomie dans son apprentissage, tout en bénéficiant d’un cadre et d’un suivi adaptés."),
            ("p", "Le suivi pourra être assuré par les parents eux-mêmes ou renforcé par l’intervention d’un maître d’étude physique."),
        ]),
    ],
    2: [
        ("Public cible", [("p", "Étudiants et jeunes adultes en parcours universitaire, notamment en fin de cycle.")]),
        ("Vocation", [
            ("notice", "Pôle actuellement opérationnel : c’est le pôle développé et commercialisé par EdEx."),
            ("p", "Le Pôle 2 intervient actuellement principalement à la fin du parcours universitaire, lorsque l’étudiant doit réaliser son mémoire et faire face aux différentes exigences méthodologiques, statistiques, rédactionnelles et logistiques liées à cette étape."),
            ("p", "Le mémoire constitue une étape importante du parcours universitaire puisqu’il permet à l’étudiant de confronter ses connaissances théoriques à une problématique réelle identifiée au sein d’une entreprise, d’une organisation ou de son environnement de stage."),
            ("p", "EdEx intervient donc pour accompagner l’étudiant dans les différentes dimensions de cette démarche."),
        ]),
        ("Offre actuelle", [
            ("p", "Le pôle propose notamment un accompagnement autour :"),
            ("ul", ["de la méthodologie de recherche ;", "de la collecte des données ;", "du traitement et de l’analyse statistique ;",
                    "de l’interprétation des résultats ;", "des recommandations ;", "de l’accompagnement du chapitre 3 ;",
                    "de l’optimisation du mémoire ;", "de la préparation du PowerPoint ;", "de la préparation du speech ;",
                    "du coaching et de la préparation à la soutenance ;", "de l’impression et de la reliure du mémoire."]),
            ("p", "Le détail des prestations, des formules et des tarifs est présenté sur la page Prestations & tarifs."),
            ("btn", "Découvrir nos prestations", "prestations/"),
        ]),
        ("Vision à moyen terme", [
            ("badge", "vision", "Pas encore disponible"),
            ("p", "EdEx ambitionne progressivement d’intervenir beaucoup plus tôt dans le parcours universitaire."),
            ("p", "À terme, l’accompagnement pourra commencer dès la première année afin d’aider l’étudiant à :"),
            ("ul", ["mieux s’organiser ;", "comprendre les exigences de l’enseignement supérieur ;", "faire face aux réalités des différents modules ;",
                    "développer de bonnes méthodes de travail ;", "structurer son apprentissage ;", "développer progressivement les compétences nécessaires à son évolution."]),
            ("p", "L’objectif est donc de ne pas attendre le mémoire pour intervenir, mais de pouvoir accompagner progressivement l’étudiant dans son parcours universitaire."),
        ]),
    ],
    3: [
        ("Public cible", [("ul", ["Jeunes diplômés ;", "porteurs de projets."])]),
        ("Premier volet : insertion professionnelle", [
            ("notice", "Pôle en cours de développement : la vision ci-dessous n’est pas encore une offre disponible."),
            ("p", "EdEx souhaite créer une passerelle entre les jeunes diplômés et les opportunités professionnelles."),
            ("p", "L’objectif est de faciliter l’accès du jeune diplômé à une première expérience professionnelle en s’appuyant notamment sur la notoriété, le réseau et les relations d’EdEx avec différents acteurs professionnels."),
            ("p", "Avant cette mise en relation, EdEx souhaite contribuer à mettre en valeur les compétences réelles du candidat. Cela pourra notamment passer par :"),
            ("ul", ["l’optimisation de son CV ;", "la présentation claire de ses compétences ;", "l’identification de ce qu’il sait réellement faire ;",
                    "la mise en évidence de ce qu’il peut apporter à une entreprise ;", "la préparation à la recherche et à l’obtention d’une première expérience professionnelle."]),
            ("p", "Le stage pourra constituer une première étape permettant au jeune diplômé de démontrer ses capacités au sein de l’entreprise."),
            ("p", "Lorsque l’expérience est concluante, elle pourra éventuellement déboucher sur une opportunité professionnelle sous la forme d’un CDD ou d’un CDI."),
        ]),
        ("Second volet : porteurs de projets", [
            ("p", "Le second volet du Pôle 3 concerne les jeunes porteurs de projets."),
            ("p", "EdEx souhaite les accompagner dans la transformation d’une idée en un projet structuré, clair et exploitable."),
            ("p", "L’objectif est notamment de transformer l’idée initiale du porteur en un document administratif et opérationnel de projet, permettant de comprendre le projet, d’en apprécier la faisabilité et, lorsqu’il est réalisable, de disposer d’une base directement exploitable pour son pilotage."),
        ]),
    ],
    4: [
        ("Public cible", [("ul", ["Entreprises déjà en activité ;", "PME ;", "grandes entreprises ;", "acteurs opérationnels."])]),
        ("Vocation", [
            ("notice", "Pôle en cours de développement : il s’agit d’une composante future de l’écosystème EdEx."),
            ("p", "Le Pôle 4 a vocation à accompagner les entreprises déjà lancées dans l’amélioration de leur fonctionnement, de leur organisation et de leur performance."),
            ("p", "L’objectif est d’agir directement sur les processus et les méthodes de travail afin d’améliorer le rendement, la productivité et l’efficacité de l’entreprise."),
        ]),
        ("Domaines d’intervention envisagés", [
            ("p", "L’intervention pourra notamment porter sur :"),
            ("ul", ["l’audit interne ;", "l’identification des dysfonctionnements ;", "l’optimisation des processus internes ;", "l’amélioration des méthodes de travail ;",
                    "la conception et la mise en place de manuels de procédures ;", "la structuration des modes de fonctionnement ;", "l’optimisation de l’organisation ;",
                    "la mise en place d’actions marketing ;", "l’élaboration de plans de communication ;", "les actions de prospection ;",
                    "la mobilisation du réseau et de la notoriété d’EdEx pour faciliter certaines mises en relation."]),
            ("p", "L’objectif n’est pas simplement de produire des recommandations, mais de pouvoir accompagner leur mise en œuvre opérationnelle lorsque cela est prévu dans la mission."),
        ]),
    ],
    5: [
        ("Public cible", [("p", "Porteurs de projets et entrepreneurs présentant des projets structurés et un potentiel de développement.")]),
        ("Vocation", [
            ("notice", "Ce pôle n’est pas un service actuellement accessible : il présente une vision à terme."),
            ("p", "Le Pôle 5 représente une ambition à plus long terme d’EdEx."),
            ("p", "La logique est de permettre à des porteurs de projets de disposer des ressources nécessaires pour transformer leurs ambitions en activités concrètes lorsque leur projet présente les caractéristiques nécessaires."),
            ("p", "EdEx pourra ainsi envisager de mettre à disposition différentes ressources, notamment :"),
            ("ul", ["des ressources financières ;", "des ressources humaines ;", "des compétences ;", "un accompagnement stratégique et opérationnel."]),
        ]),
        ("Mécanisme envisagé", [
            ("p", "Le mécanisme envisagé repose sur une logique de mise à disposition de ressources avec un fonctionnement différé et une contrepartie pouvant prendre la forme d’une participation au capital social de l’entreprise accompagnée."),
            ("p", "Cette participation permettrait à EdEx de bénéficier d’un retour sur la création de valeur générée par les entreprises accompagnées."),
            ("p", "Cependant, EdEx souhaite conserver une philosophie d’accompagnement et d’alliance plutôt que de contrôle. L’intervention au capital serait donc pensée de manière à ce que l’implication d’EdEx ne conduise pas à retirer au fondateur la maîtrise de son entreprise."),
        ]),
        ("Philosophie", [
            ("p", "Ce pôle n’est pas « le sommet » du parcours EdEx. Il représente plutôt un outil permettant de réinvestir les capacités accumulées par l’écosystème afin d’aider davantage de personnes et de projets."),
            ("p", "Le capital devient ainsi un moyen de prolonger la mission d’EdEx et non une finalité en soi."),
        ]),
    ],
}

# Tarifs : (slug, nom, licence, master, [contenu]) — Cahier V2 §10
SVC_STATS = [
    ("methodologie-donnees", "Méthodologie de collecte et traitement de données", 25000, 40000, [
        "Cadrage de la recherche : thème, problématique, objectifs, hypothèses, variables et indicateurs", "Définition de la population mère et de l’échantillon",
        "Choix et conception du dispositif de collecte adapté", "Élaboration du protocole de collecte",
        "Plan de saisie, codification, nettoyage et organisation des données", "Élaboration du plan d’analyse statistique"]),
    ("analyse-donnees", "Analyse et traitement des données collectées", 35000, 45000, [
        "Contrôle, nettoyage et préparation de la base de données", "Choix et application des méthodes statistiques adaptées",
        "Traitement des données et production des résultats statistiques", "Élaboration des tableaux statistiques",
        "Création des représentations graphiques", "Mise en forme des résultats selon les normes académiques"]),
    ("interpretation-recommandations", "Interprétation des résultats obtenus et recommandations", 20000, 35000, [
        "Interprétation des résultats statistiques", "Mise en relation des résultats avec les objectifs, questions et hypothèses de recherche",
        "Identification des tendances, relations significatives et résultats majeurs", "Confrontation et mise en perspective des résultats",
        "Formulation de recommandations adaptées aux résultats et au contexte de l’étude"]),
    ("chapitre-3", "Accompagnement complet du chapitre 3", 50000, 65000, [
        "Accompagnement à la construction et à la rédaction du chapitre 3", "Discussion des résultats et confrontation aux travaux antérieurs",
        "Vérification des hypothèses et réponse aux questions de recherche", "Élaboration des conclusions et recommandations"]),
]
SVC_MEM = [
    ("optimisation-memoire", "Optimisation du mémoire", 20000, 25000, [
        "Correction orthographique, grammaticale et syntaxique", "Amélioration de la formulation et de la cohérence rédactionnelle",
        "Harmonisation de la mise en forme selon les normes académiques"]),
    ("powerpoint", "PowerPoint de soutenance", 15000, 20000, [
        "Conception du support de soutenance", "Structuration et synthèse du contenu du mémoire", "Mise en forme professionnelle et visuelle",
        "Intégration des tableaux, graphiques et éléments essentiels"]),
    ("speech", "Speech de soutenance", 10000, 15000, [
        "Élaboration du discours de soutenance", "Structuration de la présentation orale", "Synthèse des points essentiels du mémoire",
        "Adaptation au temps de passage et au niveau d’étude"]),
]
SVC_FORM = [
    ("accompagnement-statistique", "Accompagnement statistique complet", 70000, 90000, [
        "Méthodologie de collecte et de traitement des données", "Analyse et traitement statistique", "Interprétation des résultats et recommandations",
        "Accompagnement des chapitres 2 (section 2) et 3"]),
    ("formule-essentiel", "Formule Essentiel", 55000, 65000, [
        "Optimisation du mémoire", "Préparation du PowerPoint", "Élaboration du speech de soutenance", "Coaching semi-permanent"]),
    ("formule-complete", "Formule complète (sans formule statistique ni impressions)", 95000, 110000, [
        "Accompagnement des chapitres 2 et 3", "Optimisation du mémoire", "PowerPoint et speech", "Préparation à la soutenance", "Coaching permanent"]),
    ("formule-complete-plus", "Formule complète (avec formule statistique, impression et ebook guide)", 155000, 185000, [
        "Accompagnement statistique complet", "Accompagnement des chapitres 2 et 3", "Optimisation du mémoire", "PowerPoint et speech",
        "Préparation à la soutenance", "Coaching permanent", "Impression d’un exemplaire du mémoire", "Ebook « Guide ultime pour la soutenance orale »"]),
]
SVC_COACH = [
    ("coaching-ponctuel", "Coaching ponctuel", 20000, [
        "Séances ciblées selon les besoins de l’étudiant", "Résolution de difficultés précises liées au mémoire ou à la soutenance"]),
    ("coaching-semi-permanent", "Coaching semi-permanent", 35000, [
        "Suivi régulier de l’avancement du mémoire", "Points de contrôle et orientations méthodologiques", "Assistance sur les difficultés rencontrées"]),
    ("coaching-permanent", "Coaching permanent", 55000, [
        "Accompagnement continu jusqu’à la finalisation du mémoire", "Suivi de l’avancement et corrections / orientations régulières",
        "Assistance méthodologique, rédactionnelle et statistique", "Préparation à la soutenance (simulation de soutenance, astuces et conseils)"]),
]
SOUTENANCE = {"powerpoint", "speech", "coaching-ponctuel", "coaching-semi-permanent", "coaching-permanent"}


# ---------------------------------------------------------------- gabarit
SPRITE = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">'
          '<symbol id="star" viewBox="0 0 60 100"><path fill="currentColor" d="M30 0C32 30 44 45 60 50 44 55 32 70 30 100 28 70 16 55 0 50 16 45 28 30 30 0Z"/></symbol>'
          '<symbol id="arrow" viewBox="0 0 14 12"><path d="M1 6h11M8 1.5 12.5 6 8 10.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></symbol></svg>')


def layout(slug, title, desc, main, *, current=None, solid=False, pole_mark=None, home=False, root_override=None):
    depth = slug.count("/")
    root = root_override if root_override is not None else "../" * depth
    L = lambda s: (root + s) if s else (root or "./")
    A = lambda s: root + s
    nav_li = "".join(
        f'<li><a href="{L(s)}"{" aria-current=\"page\"" if s == current else ""}>{esc(t)}</a></li>' for s, t in NAV)
    menu_li = "".join(
        f'<li style="--i:{i}"><a href="{L(s)}"{" aria-current=\"page\"" if s == current else ""}>{esc(t)}</a></li>' for i, (s, t) in enumerate(NAV))
    mark = f'<span class="pole-mark">{esc(pole_mark)}</span>' if pole_mark else ""
    hcls = "site-header" + (" is-scrolled is-solid" if solid else "")
    header = f'''<header class="{hcls}" data-header>
  <div class="container site-header__in">
    <div class="logo-wrap">
      <a class="logo" href="{L("")}" aria-label="EdEx — L’allié des esprits brillants, accueil">
        <img class="logo__img logo__img--white" src="{A("assets/img/logo-white.webp")}" width="{LOGO_W}" height="{LOGO_H}" alt="">
        <img class="logo__img logo__img--color" src="{A("assets/img/logo-color.webp")}" width="{LOGO_W}" height="{LOGO_H}" alt="">
      </a>{mark}
    </div>
    <nav class="nav" aria-label="Navigation principale"><ul>{nav_li}</ul></nav>
    <div class="header__right">
      {btn("Faire mon diagnostic", L("diagnostic/"), "gold", small=True, extra='class-extra="header__cta"').replace('class="btn btn--gold btn--sm"', 'class="btn btn--gold btn--sm header__cta"').replace(' class-extra="header__cta"', '')}
      <button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<nav class="menu" id="menu" aria-label="Menu principal">
  <ul>{menu_li}</ul>
  <div class="menu__foot">
    {btn("Faire mon diagnostic", L("diagnostic/"), "gold")}
    <p style="margin-top:1rem">WhatsApp : <a href="https://wa.me/{WA}">{PHONE}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p>
  </div>
</nav>'''
    pole_links = "".join(f'<li><a href="{L("ecosysteme/" + p["slug"] + "/")}">Pôle {p["n"]} — {esc(p["title"])}</a></li>' for p in POLES)
    footer = f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{A("assets/img/logo-white.webp")}" width="{LOGO_W}" height="{LOGO_H}" alt="EdEx — L’allié des esprits brillants" loading="lazy">
        <p>Changer les codes. Éveiller les esprits. Élever les générations.</p>
      </div>
      <div class="footer-col"><h2>Navigation</h2><ul>{"".join(f'<li><a href="{L(s)}">{esc(t)}</a></li>' for s, t in NAV)}</ul></div>
      <div class="footer-col footer-col--wide"><h2>Écosystème</h2><ul>{pole_links}</ul></div>
      <div class="footer-col footer-col--wide"><h2>Contact</h2><ul>
        <li><a href="https://wa.me/{WA}">WhatsApp : {PHONE}</a></li>
        <li><a href="mailto:{MAIL}">{MAIL}</a></li>
        <li>En ligne · sur rendez-vous</li>
        <li>Réseaux sociaux : <span class="nw">{SOCIAL}</span></li></ul></div>
    </div>
    <div class="footer-bottom">
      <span>© EdEx 2026. Tous droits réservés.</span>
      <ul><li><a href="{L("mentions-legales/")}">Mentions légales</a></li><li><a href="{L("politique-confidentialite/")}">Politique de confidentialité</a></li></ul>
    </div>
  </div>
</footer>'''
    curtain = (f'<div class="curtain" aria-hidden="true"><img class="curtain__logo curtain__logo--white" src="{A("assets/img/logo-white.webp")}" width="{LOGO_W}" height="{LOGO_H}" alt="">'
               f'<img class="curtain__logo curtain__logo--gold" src="{A("assets/img/logo-gold.webp")}" width="{LOGO_W}" height="{LOGO_H}" alt=""></div>')
    boot = ("<script>(function(d){var r=d.documentElement;r.classList.add('js');"
            "var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;"
            "if(rm){r.classList.add('rm')}else{try{if(sessionStorage.getItem('edex-t')==='1'){r.setAttribute('data-transitioning','1')}"
            + ("else if(!sessionStorage.getItem('edex-seen')){r.setAttribute('data-transitioning','first')}" if home else "")
            + "}catch(e){}}"
            "setTimeout(function(){if(!window.__edex){r.classList.remove('js');r.removeAttribute('data-transitioning')}},5000)})(document)</script>")
    full_title = title if title.startswith("EdEx") else f"{title} — EdEx"
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{attr(desc)}">
<meta name="theme-color" content="#0A3A4E">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="EdEx">
<meta property="og:title" content="{attr(full_title)}">
<meta property="og:description" content="{attr(desc)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="48x48" href="{A("assets/img/favicon-48.png")}">
<link rel="apple-touch-icon" href="{A("assets/img/apple-touch-icon.png")}">
<link rel="preload" href="{A("assets/fonts/cormorant-garamond-latin-700-normal.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{A("assets/fonts/inter-latin-wght-normal.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{A("assets/css/main.css")}">
{boot}
</head>
<body>
<a class="skip-link" href="#main">Aller au contenu</a>
{SPRITE}
{curtain}
{header}
<main id="main">
{main}
</main>
{footer}
<script src="{A("assets/vendor/gsap.min.js")}" defer></script>
<script src="{A("assets/vendor/ScrollTrigger.min.js")}" defer></script>
<script src="{A("assets/vendor/lenis.min.js")}" defer></script>
<script src="{A("assets/vendor/split-type.min.js")}" defer></script>
<script src="{A("assets/js/config.js")}" defer></script>
<script src="{A("assets/js/main.js")}" defer></script>
</body>
</html>
'''


def _typo(content):
    parts = re.split(r"(<script.*?</script>|<[^>]+>)", content, flags=re.S)
    return "".join(x if x.startswith("<") else _fr(x) for x in parts)


def write(slug, content):
    content = _typo(content)
    path = os.path.join(ROOT_DIR, slug + "index.html") if slug.endswith("/") or slug == "" else os.path.join(ROOT_DIR, slug)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def page_hero(h1, lede=None, meta=None, light=False, extra=""):
    cls = "page-hero " + ("page-hero--light" if light else "bg-deep")
    return f'''<section class="{cls}">
  {star("page-hero__star")}
  <div class="container">
    {meta or ""}
    <h1 data-hero data-hero-title>{esc(h1)}</h1>
    {f'<p class="lede" data-hero>{esc(lede)}</p>' if lede else ""}
    {extra}
  </div>
</section>'''


def cta_card(root, title="Vous ne savez pas encore quelle solution vous correspond ?", text="Expliquez-nous votre besoin. EdEx vous orientera vers la solution la plus pertinente.", label="Faire mon diagnostic", href=None):
    return f'''<section class="section" aria-labelledby="cta-title">
  <div class="container">
    <div class="cta-card">
      {star()}
      <h2 id="cta-title" data-reveal>{esc(title)}</h2>
      <p>{esc(text)}</p>
      <div>{btn(label, href or (root + "diagnostic/"), "gold")}</div>
    </div>
  </div>
</section>'''


def pole_card(p, root):
    href = root + f"ecosysteme/{p['slug']}/"
    return f'''<li><article class="pole-card">
  {star("pole-card__star")}
  <div class="pole-card__top"><span class="pole-tag">Pôle {p["n"]}</span>{badge(p["status"])}</div>
  <h3><a class="stretch" href="{href}">{esc(p["title"])}</a></h3>
  <p class="pole-card__pub">{esc(p["public"])}</p>
  <div class="pole-card__foot">{link_arrow(p["cta"])}</div>
</article></li>'''


# ---------------------------------------------------------------- pages
def build_home():
    root = ""
    hero_img = '<img class="hero__img" src="assets/img/hero.jpg" alt="" fetchpriority="high">' if HAS_HERO_IMG else ""
    hero = f'''<section class="hero bg-deep" aria-labelledby="hero-title">
  <div class="hero__bg" data-hero-bg aria-hidden="true">{hero_img}{star("hero__star")}</div>
  <div class="container hero__inner">
    <h1 id="hero-title" class="hero__title" data-hero data-hero-title>L’allié des esprits brillants.</h1>
    <p class="lede hero__lede" data-hero>EdEx construit un écosystème d’accompagnement pour aider chacun à développer son potentiel, avancer dans son parcours et transformer ses ambitions en actions concrètes.</p>
    <div class="btn-group hero__actions" data-hero>{btn("Faire mon diagnostic", "diagnostic/", "gold")}{btn("Découvrir EdEx", "qui-sommes-nous/", "line-light")}</div>
  </div>
</section>'''
    intro = '''<section class="section" aria-labelledby="intro-title">
  <div class="container statement">
    <h2 id="intro-title" data-reveal>Tout commence par l’éducation. Rien ne s’y arrête.</h2>
    <p>EdEx est un écosystème d’accompagnement qui se construit progressivement autour de plusieurs étapes de la trajectoire individuelle. Aujourd’hui, EdEx propose une première offre opérationnelle dédiée aux jeunes adultes post-bac, tout en développant progressivement ses autres pôles.</p>
  </div>
</section>'''
    eco = f'''<section class="section" id="ecosysteme" aria-labelledby="eco-title" style="padding-top:0">
  <div class="container">
    <div class="section-head">
      <h2 id="eco-title" data-reveal>Une seule philosophie, cinq portes d’entrée.</h2>
      <p>Les pôles ne sont ni des sous-marques, ni des étapes : ils coexistent, s’entrecroisent et ne se succèdent pas. Le statut de chacun est indiqué.</p>
    </div>
    <ul class="pole-rail" tabindex="0" aria-label="Les cinq pôles EdEx">{"".join(pole_card(p, root) for p in POLES)}</ul>
    <p class="center mt-m">{btn("Voir tout l’écosystème", "ecosysteme/", "line")}</p>
  </div>
</section>'''
    cards = [
        ("Le constat", "Un savoir sans usage.", "On a longtemps enseigné à réussir un examen. Rarement à penser, à décider, à tenir. Le diplôme referme un chapitre ; il n’ouvre pas toujours une vie."),
        ("Le manque", "Personne à côté de soi.", "Le potentiel d’une personne ne devrait pas être limité par le manque d’information, de méthode, de ressources ou d’accompagnement."),
        ("Le point de départ", "Agir sur l’humain, un par un.", "Un être humain est façonné par quatre choses : son éducation, son niveau de conscience, ses valeurs et son environnement. Tout le reste en découle. Le seul moyen de changer le monde est donc d’agir sur l’humain, un par un."),
        ("La réponse", "Un allié, aussi longtemps qu’il le faut.", "Identifier les besoins, mobiliser les compétences pertinentes et proposer un accompagnement adapté afin de transformer les difficultés ou ambitions individuelles en actions concrètes."),
    ]
    stack_items = "".join(f'''<li class="stack-card" style="--i:{i}"><div class="stack-card__inner">
  <div class="stack-face stack-face--front"><span class="stack-label">{star()}{esc(lab)}</span><p class="stack-big">{esc(big)}</p>
    <button type="button" class="stack-btn" data-flip aria-expanded="false">Lire la suite</button></div>
  <div class="stack-face stack-face--back"><span class="stack-label">{star()}{esc(lab)}</span><p class="stack-text">{esc(txt)}</p>
    <button type="button" class="stack-btn" data-unflip>Revenir</button></div>
</div></li>''' for i, (lab, big, txt) in enumerate(cards))
    constat = f'''<section class="section bg-deep" aria-labelledby="constat-title">
  <div class="container">
    <div class="stack-layout">
      <div class="stack-intro">{eyebrow("Le point de départ")}<h2 id="constat-title" data-reveal>L’éducation n’est pas la destination.</h2></div>
      <ul class="stack">{stack_items}</ul>
    </div>
    <p class="vision-lines" data-reveal>Changer les codes.<br>Éveiller les esprits.<br>Élever les générations.</p>
  </div>
</section>'''
    why_items = ["Approche centrée sur le besoin réel.", "Mobilisation des compétences pertinentes selon chaque problématique.",
                 "Logique d’accompagnement au-delà de la prestation ponctuelle.", "Construction progressive d’un écosystème de talents, projets et opportunités."]
    why = f'''<section class="section" aria-labelledby="why-title">
  <div class="container why-layout">
    <div class="sticky"><h2 id="why-title" data-reveal>Pourquoi EdEx ?</h2>
      <p class="lede muted mt-s" style="max-width:24ch">Le produit, ce n’est pas une prestation. C’est une personne.</p></div>
    <ul class="rule-list rule-list--gold">{"".join(f'<li><p class="why-item">{esc(t)}</p></li>' for t in why_items)}</ul>
  </div>
</section>'''
    tiles = [("Statistiques", "statistiques"), ("Mémoire / soutenance", "memoire-soutenance"), ("Formules d’accompagnement", "formules"), ("Coaching", "coaching"), ("Impression", "impression")]
    now = f'''<section class="section bg-gray" aria-labelledby="now-title">
  <div class="container">
    <div class="grid-12">
      <div class="span-6">{badge("ops", "Pôle 2 — Opérationnel")}<h2 id="now-title" data-reveal style="margin-top:var(--sp-xs)">Aujourd’hui, l’offre EdEx est concentrée sur le pôle 2.</h2></div>
      <div class="span-5 start-8" style="align-self:end"><p class="measure">À ce jour, notre offre opérationnelle est concentrée sur le Pôle 2 — Jeune adulte post-bac, avec un accompagnement particulièrement orienté vers les étudiants et jeunes adultes dans leurs travaux académiques, leur mémoire et leur soutenance. Les autres pôles sont actuellement en cours de structuration et seront progressivement déployés.</p></div>
    </div>
    <ul class="tiles mt-m">{"".join(f'<li><a class="tile" href="prestations/#{a}"><span>{esc(t)}</span><span class="ic" aria-hidden="true">{arrow_icon()}</span></a></li>' for t, a in tiles)}</ul>
    <p class="mt-m">{btn("Découvrir nos prestations", "prestations/", "navy")}</p>
  </div>
</section>'''
    main = hero + intro + eco + constat + why + now + cta_card(root)
    write("", layout("", "L’allié des esprits brillants", "EdEx est un écosystème d’accompagnement humain : éducation, formation, insertion, entrepreneuriat. Offre opérationnelle pour les étudiants post-bac : mémoire et soutenance.", main, current="", home=True))


def build_about():
    root = "../"
    vals = ["Excellence", "Transmission", "Intégrité", "Innovation", "Responsabilité", "Impact"]
    main = page_hero("Qui sommes-nous ?", "EdEx est né d’une conviction : le potentiel d’une personne ne devrait pas être limité par le manque d’information, de méthode, de ressources ou d’accompagnement.")
    main += f'''<section class="section" aria-labelledby="amb-title">
  <div class="container grid-12">
    <div class="span-5">{eyebrow("Notre ambition")}<h2 id="amb-title" data-reveal>Créer des passerelles.</h2></div>
    <div class="span-6 start-7"><p class="lede">Notre ambition est de construire progressivement un écosystème capable d’accompagner les individus à différents moments de leur parcours et de créer des passerelles entre éducation, formation, insertion, entrepreneuriat et développement professionnel.</p></div>
  </div>
</section>
<section class="section bg-gray" aria-label="Vision et mission">
  <div class="container">
    <div class="doc-block" style="border-top:0;padding-top:0"><h2 data-reveal>Vision</h2><div class="doc-body"><p class="lede" style="max-width:34ch">Construire un écosystème d’accompagnement humain permettant à chacun de mieux comprendre son potentiel, développer ses compétences, concrétiser ses projets et accéder aux bonnes ressources.</p></div></div>
    <div class="doc-block" style="padding-bottom:0"><h2 data-reveal>Mission</h2><div class="doc-body"><p class="lede" style="max-width:34ch">Identifier les besoins, mobiliser les compétences pertinentes et proposer un accompagnement adapté afin de transformer les difficultés ou ambitions individuelles en actions concrètes.</p></div></div>
  </div>
</section>
<section class="section" aria-labelledby="val-title">
  <div class="container">
    <div class="section-head" style="text-align:left;margin-left:0"><h2 id="val-title" data-reveal>Nos valeurs</h2></div>
    <ul class="values">{"".join(f"<li>{v}</li>" for v in vals)}</ul>
  </div>
</section>
<section class="section bg-deep" aria-labelledby="eco-about">
  <div class="container grid-12">
    <div class="span-5">{eyebrow("L’écosystème")}<h2 id="eco-about" data-reveal>Cinq pôles, un même écosystème.</h2></div>
    <div class="span-6 start-7">
      <p class="lede" style="margin-bottom:var(--sp-s)">Les pôles appartiennent au même écosystème : il n’y a pas d’ordre obligatoire pour les parcourir.</p>
      <ul class="rule-list" style="border-color:rgba(255,255,255,.25)">{"".join(f'<li style="border-color:rgba(255,255,255,.25);display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap"><a href="../ecosysteme/{p["slug"]}/" style="font-family:var(--font-display);font-weight:700;font-size:1.7rem;text-decoration:none;line-height:1.1">Pôle {p["n"]} — {esc(p["title"])}</a>{badge(p["status"])}</li>' for p in POLES)}</ul>
      <p class="mt-m">{btn("Découvrir notre approche", "../comment-ca-marche/", "line-light")}</p>
    </div>
  </div>
</section>'''
    main += cta_card(root)
    write("qui-sommes-nous/", layout("qui-sommes-nous/", "Qui sommes-nous ?", "EdEx est né d’une conviction : le potentiel d’une personne ne devrait pas être limité par le manque d’information, de méthode, de ressources ou d’accompagnement.", main, current="qui-sommes-nous/"))


def build_eco():
    root = "../"
    rows = "".join(f'''<li class="pole-row">
  <div class="pole-row__side"><span class="pole-tag">Pôle {p["n"]}</span>{badge(p["status"])}</div>
  <div><h3><a class="stretch" href="{p["slug"]}/">{esc(p["title"])}</a></h3><p>{esc(p["public"])}</p></div>
  <div class="pole-row__side">{link_arrow(p["cta"])}</div>
</li>''' for p in POLES)
    main = page_hero("Notre écosystème", "Cinq pôles, un même accompagnement humain. Ils ne sont ni des sous-marques, ni des étapes : ils coexistent, s’entrecroisent et ne se succèdent pas.")
    main += f'''<section class="section" aria-labelledby="poles-title">
  <div class="container">
    <h2 id="poles-title" class="sr-only">Les cinq pôles</h2>
    <ul>{rows}</ul>
    <div class="legend" aria-label="Signification des statuts">
      <div>{badge("ops")}<span>Offre disponible aujourd’hui.</span></div>
      <div>{badge("dev")}<span>Pôle en cours de structuration.</span></div>
      <div>{badge("vision")}<span>Ambition à plus long terme, pas encore accessible.</span></div>
    </div>
  </div>
</section>'''
    main += cta_card(root)
    write("ecosysteme/", layout("ecosysteme/", "Notre écosystème", "Les cinq pôles de l’écosystème EdEx et leur statut : éducation, jeune adulte post-bac, insertion professionnelle, entrepreneuriat, private equity.", main, current="ecosysteme/"))


def build_poles():
    for p in POLES:
        root = "../../"
        blocks = ""
        for title, items in POLE_BLOCKS[p["n"]]:
            body = ""
            for it in items:
                k = it[0]
                if k == "p": body += P(it[1])
                elif k == "ul": body += UL(it[1])
                elif k == "notice": body += f'<p class="notice">{esc(it[1])}</p>'
                elif k == "badge": body += f"<p>{badge(it[1], it[2])}</p>"
                elif k == "btn": body += f'<p>{btn(it[1], root + it[2], "navy")}</p>'
            blocks += f'<div class="doc-block"><h2 data-reveal>{esc(title)}</h2><div class="doc-body">{body}</div></div>'
        meta = f'<div class="page-hero__meta"><span class="pole-tag">Pôle {p["n"]} — {esc(p["kind"])}</span>{badge(p["status"])}</div>'
        main = page_hero(p["title"], p["lede"], meta=meta, light=True)
        main += f'<section class="section" style="padding-top:var(--sp-m)"><div class="container">{blocks}</div></section>'
        others = "".join(f'<a class="chip-link" href="{root}ecosysteme/{o["slug"]}/">Pôle {o["n"]} · {esc(o["title"])}</a>' for o in POLES if o["n"] != p["n"])
        main += f'''<section class="section bg-gray" aria-labelledby="others-title">
  <div class="container">
    <h2 id="others-title" style="font-size:var(--fs-h3);margin-bottom:var(--sp-xs)">Les autres pôles de l’écosystème</h2>
    <div class="doc-nav">{others}</div>
  </div>
</section>'''
        if p["n"] == 1:
            main += cta_card(root, "Une question sur les examens de votre enfant ?", "Expliquez-nous votre besoin. EdEx vous orientera vers la solution la plus pertinente.")
        else:
            main += cta_card(root)
        write(f"ecosysteme/{p['slug']}/", layout(f"ecosysteme/{p['slug']}/", f"Pôle {p['n']} — {p['title']}", p["desc"], main, current="ecosysteme/", solid=True, pole_mark=f"Pôle {p['n']}"))


def build_how():
    root = "../"
    steps = [("Vous identifiez votre besoin", "Vous expliquez votre situation, votre objectif ou la difficulté rencontrée."),
             ("Nous réalisons le diagnostic", "EdEx analyse le besoin afin d’identifier la solution pertinente."),
             ("Nous vous orientons", "Proposition adaptée : prestation, accompagnement ou orientation."),
             ("Nous mettons en œuvre", "Le bon profil ou la bonne équipe est mobilisé."),
             ("Nous assurons le suivi", "Suivi de l’avancement et de la satisfaction selon la mission.")]
    lis = "".join(f'<li class="step"><span class="step__n" aria-hidden="true">{i + 1}</span><h2>{esc(t)}</h2><p>{esc(d)}</p></li>' for i, (t, d) in enumerate(steps))
    main = page_hero("Comment ça marche ?", "Un parcours simple en cinq étapes, du besoin exprimé au suivi de la mission.")
    main += f'<section class="section"><div class="container"><ol class="steps">{lis}</ol><p class="mt-m">{btn("Commencer mon diagnostic", root + "diagnostic/", "gold")}</p></div></section>'
    write("comment-ca-marche/", layout("comment-ca-marche/", "Comment ça marche ?", "Identifier votre besoin, réaliser le diagnostic, vous orienter, mettre en œuvre et assurer le suivi : le parcours EdEx en cinq étapes.", main, current="comment-ca-marche/"))


def svc_row(slug, name, lic, mas, items, besoin, root):
    q = f"?prestation={urllib.parse.quote(name)}&besoin={urllib.parse.quote(besoin)}&situation={urllib.parse.quote('Étudiant')}"
    base = root + "diagnostic/" + q
    return f'''<article class="svc" id="{slug}">
  <div><h3>{esc(name)}</h3>
    <p class="price"><span class="price__n" data-price data-licence="{lic}" data-master="{mas}">{money(lic)}</span><span class="price__u">FCFA</span></p>
    <span class="price__lvl">Tarif indicatif · <span data-lvl-label>Licence</span></span></div>
  <div>{UL(items)}<p class="svc__cta">{btn("Demander cette prestation", base + "&niveau=Licence", "line", small=True, extra=f'data-svc-link="{attr(base)}"')}</p></div>
</article>'''


def svc_fixed(slug, name, price_txt, unit, items, besoin, root, items_html=None):
    q = f"?prestation={urllib.parse.quote(name)}&besoin={urllib.parse.quote(besoin)}&situation={urllib.parse.quote('Étudiant')}"
    return f'''<article class="svc" id="{slug}">
  <div><h3>{esc(name)}</h3><p class="price"><span class="price__n">{price_txt}</span><span class="price__u">{esc(unit)}</span></p><span class="price__lvl">Tarif indicatif</span></div>
  <div>{items_html if items_html is not None else UL(items)}<p class="svc__cta">{btn("Demander cette prestation", root + "diagnostic/" + q, "line", small=True)}</p></div>
</article>'''


def group(gid, title, rows, lead=None):
    return f'''<section class="svc-group" id="{gid}" aria-labelledby="{gid}-t"><div class="container">
  <div class="svc-group__head"><h2 id="{gid}-t" data-reveal>{esc(title)}</h2>{f'<p class="muted measure">{esc(lead)}</p>' if lead else ""}</div>
  {rows}</div></section>'''


def build_prestations():
    root = "../"
    M, S = "Mémoire / recherche", "Soutenance"
    stats = "".join(svc_row(s, n, l, m, it, M, root) for s, n, l, m, it in SVC_STATS)
    mem = "".join(svc_row(s, n, l, m, it, S if s in SOUTENANCE else M, root) for s, n, l, m, it in SVC_MEM)
    form = "".join(svc_row(s, n, l, m, it, M, root) for s, n, l, m, it in SVC_FORM)
    coach = "".join(svc_fixed(s, n, money(pr), "FCFA", it, S, root) for s, n, pr, it in SVC_COACH)
    imp = (svc_fixed("impression", "Impression", "65", "FCFA / page", [], M, root, items_html=P("Impression du mémoire, au tarif de 65 FCFA par page.")) +
           svc_fixed("reliure", "Reliure", f"500{NB}/{NB}1{NB}000", "FCFA", [], M, root, items_html=P("Reliure du mémoire, à 500 FCFA ou 1 000 FCFA selon la formule.")))
    chips = [("Statistiques", "statistiques"), ("Mémoire / soutenance", "memoire-soutenance"), ("Formules d’accompagnement", "formules"), ("Coaching", "coaching"), ("Impression", "impression")]
    main = page_hero("Prestations & tarifs", "Le catalogue de l’offre actuellement opérationnelle du Pôle 2 — Jeune adulte post-bac.",
                     meta=f'<div class="page-hero__meta">{badge("ops", "Pôle 2 — Opérationnel")}</div>')
    main += f'''<section class="section section--tight" aria-label="Introduction">
  <div class="container grid-12"><div class="span-7"><p class="lede">EdEx développe progressivement un écosystème d’accompagnement couvrant plusieurs étapes de la trajectoire individuelle. À ce jour, notre offre opérationnelle est concentrée sur le Pôle 2 — Jeune adulte post-bac, avec un accompagnement particulièrement orienté vers les étudiants et jeunes adultes dans leurs travaux académiques, leur mémoire et leur soutenance.</p>
  <p class="muted mt-s">Les autres pôles sont actuellement en cours de structuration et seront progressivement déployés.</p></div></div>
</section>
<div class="tarif-bar"><div class="container">
  <div class="level-switch" role="radiogroup" aria-label="Niveau d’étude" data-level-switch>
    <label><input type="radio" name="level" value="licence" checked><span>Licence</span></label>
    <label><input type="radio" name="level" value="master"><span>Master</span></label></div>
  <p class="tarif-bar__note">Tarifs indicatifs en FCFA, affichés selon le niveau choisi.</p>
</div></div>
<div class="container section--tight"><nav class="subnav" aria-label="Catégories de prestations">{"".join(f'<a class="chip-link" href="#{a}">{esc(t)}</a>' for t, a in chips)}</nav></div>
{group("statistiques", "Statistiques", stats)}
{group("memoire-soutenance", "Mémoire / soutenance", mem)}
{group("formules", "Formules d’accompagnement", form, "Des formules qui regroupent plusieurs prestations.")}
{group("coaching", "Coaching", coach, "Un tarif unique, quel que soit le niveau d’étude.")}
{group("impression", "Impression", imp)}
<div style="height:var(--sp-l)"></div>'''
    main += cta_card(root, "Vous hésitez sur la prestation à choisir ?", "Expliquez-nous votre besoin. EdEx vous orientera vers la solution la plus pertinente.")
    write("prestations/", layout("prestations/", "Prestations & tarifs", "Catalogue des prestations du Pôle 2 EdEx : statistiques, mémoire, soutenance, formules d’accompagnement, coaching, impression. Tarifs indicatifs Licence / Master.", main, current="prestations/"))


def chip(name, val, label=None, checked=False):
    return f'<label class="chip"><input type="radio" name="{name}" value="{attr(val)}"{" checked" if checked else ""}><span>{esc(label or val)}</span></label>'


def build_diag():
    root = "../"
    situations = ["Élève", "Étudiant", "Diplômé", "Professionnel", "Entrepreneur", "Entreprise", "Autre"]
    besoins = ["Examens nationaux", "Mémoire / recherche", "Soutenance", "Formation", "Insertion professionnelle", "Entrepreneuriat", "Accompagnement professionnel", "Autre"]
    err = '<p class="error-msg" hidden></p>'
    def field(label, name, typ="text", req=True, autocomplete=None, hint=None):
        return (f'<div class="field"><label for="f-{name}">{esc(label)}{"" if not req else ""}</label>'
                f'<input type="{typ}" id="f-{name}" name="{name}"{f" autocomplete={chr(34)}{autocomplete}{chr(34)}" if autocomplete else ""}>'
                f'{f"<p class={chr(34)}hint{chr(34)}>{esc(hint)}</p>" if hint else ""}{err}</div>')
    form = f'''<form class="diag" data-diag novalidate aria-label="Formulaire de diagnostic">
  <div data-diag-steps>
    <div class="banner" data-presta-banner hidden>{star()}<p>Prestation demandée : <strong data-presta-text></strong>. Complétez votre diagnostic pour que nous puissions vous répondre.</p></div>
    <div class="progress" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
    <p class="progress-label" aria-live="polite">Étape 1 sur 5</p>

    <section class="panel is-current" aria-labelledby="p1">
      <h2 id="p1">Votre profil</h2>
      <div class="row-2">{field("Nom", "nom", autocomplete="family-name")}{field("Prénom", "prenom", autocomplete="given-name")}</div>
      <div class="row-2">{field("Téléphone", "telephone", "tel", autocomplete="tel", hint="Au moins un téléphone ou un e-mail.")}{field("E-mail", "email", "email", autocomplete="email")}</div>
      <div class="form-nav"><span></span>{btnb("Continuer", "navy", "data-next")}</div>
    </section>

    <section class="panel" aria-labelledby="p2">
      <h2 id="p2">Votre situation et votre besoin</h2>
      <fieldset class="fieldset" data-fs="situation"><legend>Vous êtes</legend><div class="chips">{"".join(chip("situation", s) for s in situations)}</div>{err}</fieldset>
      <fieldset class="fieldset" data-fs="besoin"><legend>Votre besoin principal</legend><div class="chips">{"".join(chip("besoin", b) for b in besoins)}</div>{err}</fieldset>
      <div class="form-nav"><button type="button" class="btn-text" data-prev>Retour</button>{btnb("Continuer", "navy", "data-next")}</div>
    </section>

    <section class="panel" aria-labelledby="p3">
      <h2 id="p3">Décrivez votre besoin</h2>
      <div class="field"><label for="f-description">Votre problème ou votre objectif</label><textarea id="f-description" name="description" rows="6"></textarea>{err}</div>
      <div class="row-2">
        <div class="field"><label for="f-echeance">Échéance</label><input type="date" id="f-echeance" name="echeance"><p class="hint">Date souhaitée, si vous en avez une.</p></div>
        <div class="field"><label for="f-urgence">Niveau d’urgence</label><select id="f-urgence" name="urgence"><option value="">Non précisé</option><option>Pas urgent</option><option>Dans le mois</option><option>Cette semaine</option><option>Très urgent</option></select></div>
      </div>
      <div class="field"><label for="f-budget">Budget</label><select id="f-budget" name="budget"><option value="">Non précisé</option><option>Moins de 25 000 FCFA</option><option>25 000 à 50 000 FCFA</option><option>50 000 à 100 000 FCFA</option><option>100 000 à 200 000 FCFA</option><option>Plus de 200 000 FCFA</option></select><p class="hint">Facultatif : une fourchette nous aide à vous proposer la bonne solution.</p></div>
      <div class="form-nav"><button type="button" class="btn-text" data-prev>Retour</button>{btnb("Continuer", "navy", "data-next")}</div>
    </section>

    <section class="panel" aria-labelledby="p4">
      <h2 id="p4">Documents et canal de contact</h2>
      <div class="field" data-files hidden><label for="f-docs">Ajouter un document (facultatif)</label><input type="file" id="f-docs" name="documents" multiple></div>
      <p class="hint" data-files-hint>Si nécessaire, vous pourrez joindre vos documents directement dans la conversation WhatsApp ou dans l’e-mail.</p>
      <fieldset class="fieldset" data-fs="canal"><legend>Comment souhaitez-vous être recontacté ?</legend><div class="chips">{chip("canal", "WhatsApp", checked=True)}{chip("canal", "Téléphone")}{chip("canal", "E-mail")}</div></fieldset>
      <div class="form-nav"><button type="button" class="btn-text" data-prev>Retour</button>{btnb("Voir le récapitulatif", "navy", "data-next")}</div>
    </section>

    <section class="panel" aria-labelledby="p5">
      <h2 id="p5">Votre diagnostic est prêt</h2>
      <p class="muted">Vérifiez vos informations, puis envoyez-les à l’équipe EdEx.</p>
      <dl class="recap" data-recap></dl>
      <div class="send-row">
        {btnb("Envoyer mon diagnostic par WhatsApp", "gold", 'data-send="wa"')}
        {btnb("Envoyer par e-mail", "line", 'data-send="mail"')}
        <button type="button" class="btn-text" data-send="copy">Copier le message</button>
        <button type="submit" class="btn btn--gold" data-submit hidden><span class="btn__label">Envoyer mon diagnostic</span><span class="btn__icon" aria-hidden="true">{arrow_icon()}{arrow_icon()}</span></button>
      </div>
      <p class="form-status" data-send-status role="status" hidden></p>
      <div class="form-nav"><button type="button" class="btn-text" data-prev>Retour</button><span></span></div>
    </section>
  </div>
  <div class="done" data-diag-done hidden><h3>Merci !</h3><p>Votre demande a bien été reçue. L’équipe EdEx reviendra vers vous après analyse de votre besoin.</p></div>
  <p class="hp" aria-hidden="true"><label>Ne pas remplir <input type="text" name="website" tabindex="-1" autocomplete="off"></label></p>
</form>'''
    main = page_hero("Faire mon diagnostic", "Expliquez-nous votre besoin. EdEx analyse votre situation, puis vous oriente vers la solution la plus pertinente : prestation, accompagnement ou orientation.")
    main += f'''<section class="section section--tight"><div class="container form-shell">
  <aside class="form-aside"><h2 style="font-size:var(--fs-h3)">Un diagnostic, pas un simple formulaire.</h2>
    <p class="muted mt-s">Cinq courts écrans pour comprendre votre situation avant de vous orienter. Comptez deux à trois minutes.</p>
    <p class="mt-s">Vous préférez en parler directement ?<br><a class="link-arrow" href="https://wa.me/{WA}" style="margin-top:.6rem"><span>Écrire sur WhatsApp</span><span class="ic" aria-hidden="true">{arrow_icon()}</span></a></p></aside>
  <div>{form}</div>
</div></section>'''
    write("diagnostic/", layout("diagnostic/", "Faire mon diagnostic", "Décrivez votre besoin à EdEx : situation, objectif, échéance, budget. Nous analysons votre demande et vous orientons vers la solution la plus pertinente.", main, current="diagnostic/"))


def build_contact():
    root = "../"
    err = '<p class="error-msg" hidden></p>'
    main = page_hero("Contact", "Une question, un besoin ? Écrivez-nous : nous vous répondons sur rendez-vous, en ligne.")
    main += f'''<section class="section"><div class="container form-shell">
  <div class="form-aside">
    <dl class="contact-list">
      <div><dt>Téléphone / WhatsApp</dt><dd><a href="https://wa.me/{WA}">{PHONE}</a></dd></div>
      <div><dt>E-mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
      <div><dt>Adresse</dt><dd>En ligne</dd></div>
      <div><dt>Réseaux sociaux</dt><dd>{SOCIAL}</dd></div>
      <div><dt>Horaires</dt><dd>Sur rendez-vous</dd></div>
    </dl>
    <div class="btn-group mt-m">{btn("Nous contacter sur WhatsApp", "https://wa.me/" + WA, "gold", extra='target="_blank" rel="noopener"')}{btn("Envoyer un e-mail", "mailto:" + MAIL, "line")}</div>
  </div>
  <form data-contact-form novalidate aria-label="Formulaire de contact" class="stack" style="display:grid;gap:var(--sp-s)">
    <h2 style="font-size:clamp(2rem,1.4rem + 2.4vw,3.4rem)">Écrivez-nous</h2>
    <div class="row-2"><div class="field"><label for="c-nom">Nom</label><input type="text" id="c-nom" name="nom" autocomplete="name">{err}</div>
    <div class="field"><label for="c-contact">E-mail ou téléphone</label><input type="text" id="c-contact" name="contact" autocomplete="email">{err}</div></div>
    <div class="field"><label for="c-msg">Votre message</label><textarea id="c-msg" name="message" rows="6"></textarea>{err}</div>
    <p class="hp" aria-hidden="true"><label>Ne pas remplir <input type="text" name="website" tabindex="-1" autocomplete="off"></label></p>
    <div class="send-row">{btnb("Envoyer par WhatsApp", "gold", 'data-send="wa"')}{btnb("Envoyer par e-mail", "line", 'data-send="mail"')}<button type="button" class="btn-text" data-send="copy">Copier le message</button></div>
    <p class="form-status" data-send-status role="status" hidden></p>
  </form>
</div></section>'''
    write("contact/", layout("contact/", "Contact", "Contacter EdEx par WhatsApp, téléphone ou e-mail. Échanges en ligne, sur rendez-vous.", main, current="contact/"))


def build_legal():
    root = "../"
    note = '<p class="notice">Cette page est un cadre à compléter et à faire valider par EdEx avant la mise en ligne. Les éléments entre crochets sont à renseigner.</p>'
    ml = f'''{note}
<div class="doc-block"><h2>Éditeur du site</h2><div class="doc-body">
<p>Le site est édité par EdEx.</p>
<ul class="dash-list"><li>Dénomination : EdEx</li><li>Forme juridique : {PH("à compléter")}</li><li>Siège / adresse : En ligne</li><li>Immatriculation (RCCM / IFU) : {PH("à compléter")}</li>
<li>Directeur de la publication : {PH("à compléter")}</li><li>Téléphone / WhatsApp : {PHONE}</li><li>E-mail : <a href="mailto:{MAIL}">{MAIL}</a></li></ul></div></div>
<div class="doc-block"><h2>Hébergement</h2><div class="doc-body"><p>Hébergeur : {PH("nom, adresse et contact de l’hébergeur — à compléter")}</p></div></div>
<div class="doc-block"><h2>Propriété intellectuelle</h2><div class="doc-body"><p>Le logo, l’identité visuelle, les textes et les contenus de ce site sont la propriété d’EdEx, sauf mention contraire. {PH("formulation à valider par EdEx")}</p></div></div>
<div class="doc-block"><h2>Contact</h2><div class="doc-body"><p>Pour toute question relative au site : <a href="mailto:{MAIL}">{MAIL}</a>.</p></div></div>'''
    pc = f'''{note}
<div class="doc-block"><h2>Données collectées</h2><div class="doc-body"><p>Lorsque vous utilisez le formulaire de diagnostic ou le formulaire de contact, vous pouvez nous communiquer : nom, prénom, téléphone, adresse e-mail, situation, description de votre besoin, échéance, budget et canal de contact préféré.</p></div></div>
<div class="doc-block"><h2>Finalité</h2><div class="doc-body"><p>Ces informations servent uniquement à analyser votre demande et à vous répondre.</p></div></div>
<div class="doc-block"><h2>Transmission de votre demande</h2><div class="doc-body"><p>Selon la configuration du site, votre message est transmis à EdEx par WhatsApp ou par e-mail, ou par un service d’envoi de formulaires {PH("nom du service, si activé")}. Ces services ont leurs propres règles de confidentialité.</p></div></div>
<div class="doc-block"><h2>Cookies et mesure d’audience</h2><div class="doc-body"><p>Le site n’utilise pas de cookies de suivi et aucun outil de mesure d’audience n’est actuellement installé {PH("à mettre à jour si un outil est ajouté")}.</p></div></div>
<div class="doc-block"><h2>Conservation et vos droits</h2><div class="doc-body"><p>Durée de conservation : {PH("à compléter")}.</p><p>Vous pouvez demander l’accès, la rectification ou la suppression de vos données en écrivant à <a href="mailto:{MAIL}">{MAIL}</a>. {PH("références légales applicables à préciser par EdEx")}</p></div></div>'''
    for slug, t, d, body in [("mentions-legales/", "Mentions légales", "Mentions légales du site EdEx.", ml), ("politique-confidentialite/", "Politique de confidentialité", "Politique de confidentialité du site EdEx : données collectées, finalité, droits.", pc)]:
        main = page_hero(t) + f'<section class="section section--tight"><div class="container">{body}</div></section>'
        write(slug, layout(slug, t, d, main, current=None, solid=True))


def build_404():
    main = f'''<section class="nf bg-deep"><div>
  <p class="eyebrow" style="justify-content:center">{star()}<span>Erreur 404</span></p>
  <h1>Page introuvable</h1>
  <p class="lede" style="margin:var(--sp-xs) auto var(--sp-s);max-width:34ch">Cette page n’existe pas ou a été déplacée. Reprenons depuis l’accueil.</p>
  {btn("Retour à l’accueil", "/", "gold")}
</div></section>'''
    write("404.html", layout("404.html", "Page introuvable", "Page introuvable.", main, root_override="/"))


if __name__ == "__main__":
    build_home(); build_about(); build_eco(); build_poles(); build_how(); build_prestations(); build_diag(); build_contact(); build_legal(); build_404()
    with open("robots.txt", "w") as f:
        f.write("User-agent: *\nAllow: /\n")
    print("Pages générées.")
