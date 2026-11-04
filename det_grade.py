

# ------------------------------------------------------------------ ferro quadriculado / topo inclinado
# Mesmo desenho do app Medidor (pecasGrade): marco, vidro, montantes e travessas; topo pode ser inclinado.
FERRO = (0.10, 0.10, 0.11)


def _pxz(pts, y0, y1):
    """Polígono no plano x-z (lista de (x, z)) extrudado de y0 a y1."""
    pol = Part.makePolygon([V(x, y0, z) for x, z in pts] + [V(pts[0][0], y0, pts[0][1])])
    return Part.Face(pol).extrude(V(0, y1 - y0, 0))


def eh_ferro(e):
    t = e.get("tipo")
    if t == "Janela":
        return str(e.get("modelo", "")).lower() == "ferro"
    return t == "Porta" and str(e.get("acab", "")).lower() == "ferro"


def grade(doc, part, feat, cod, ix, rot, e, p0, th, t, z0, z1, z1f):
    d, L = float(e["dist"]), float(e["larg"])
    u0, u1 = d, d + L
    porta_ = e.get("tipo") == "Porta"
    fe = eh_ferro(e)
    fw, b = (40.0, 15.0) if fe else (45.0, 22.0)
    ym = t / 2.0
    k0 = 20.0 if fe else 30.0

    def top(u):
        return z1 + (z1f - z1) * (u - u0) / (L or 1.0)
    perf, vid, peit = [], [], []
    Y0, Y1 = ym - k0, ym + k0
    perf.append(_pxz([(u0, z0), (u1, z0), (u1, z0 + fw), (u0, z0 + fw)], Y0, Y1))
    perf.append(_pxz([(u0, top(u0) - fw), (u1, top(u1) - fw), (u1, top(u1)), (u0, top(u0))], Y0, Y1))
    perf.append(_pxz([(u0, z0 + fw), (u0 + fw, z0 + fw), (u0 + fw, top(u0 + fw) - fw), (u0, top(u0) - fw)], Y0, Y1))
    perf.append(_pxz([(u1 - fw, z0 + fw), (u1, z0 + fw), (u1, top(u1) - fw), (u1 - fw, top(u1 - fw) - fw)], Y0, Y1))
    ia, ib, za = u0 + fw, u1 - fw, z0 + fw

    def tp(u):
        return top(u) - fw
    vid.append(_pxz([(ia, za), (ib, za), (ib, tp(ib)), (ia, tp(ia))], ym - 3, ym + 3))
    if fe:
        hm = max(tp(ia), tp(ib)) - za
        cols = int(float(e.get("cols") or 0)) or max(1, int(round((ib - ia) / (420.0 if porta_ else 450.0))))
        lins = int(float(e.get("lins") or 0)) or max(1, int(round(hm / (450.0 if porta_ else 520.0))))
        km = 12.0
    else:
        modelo = str(e.get("modelo", "")).lower()
        correr = modelo != "fixa" and (modelo == "correr" or (not modelo and L >= 900))
        cols, lins, km = (2 if correr else 1), 1, 26.0
    for i in range(1, cols):
        u = ia + (ib - ia) * i / cols
        perf.append(_pxz([(u - b / 2, za), (u + b / 2, za), (u + b / 2, tp(u + b / 2)), (u - b / 2, tp(u - b / 2))],
                         ym - km, ym + km))
    hmax = max(tp(ia), tp(ib))
    for j in range(1, lins):
        z = za + (hmax - za) * j / lins
        ua, ub = ia, ib
        ta, tb = tp(ia), tp(ib)
        if ta < z + b:
            if tb < z + b:
                continue
            ua = ia + (ib - ia) * (z + b - ta) / (tb - ta)
        if tb < z + b:
            ub = ia + (ib - ia) * (z + b - ta) / (tb - ta)
        if ub - ua > 5:
            perf.append(_bx(ua, ym - 12, z - b / 2, ub - ua, 24, b))
    if porta_:
        dob_dir = str(e.get("dob", "e")).lower().startswith("d")
        hx = u0 + fw + 60 if dob_dir else u1 - fw - 60
        perf.append(_bx(hx - 12, ym - k0 - 40, 950, 24, 40, 300))          # puxador do lado de dentro
    elif z0 > 50:
        peit.append(_bx(d - 20, -25, z0 - 20, L + 40, t / 2.0 + 25, 20))
    nome = ("Esquadria de ferro quadriculada" if fe else "Esquadria alumínio preto") + (" (topo inclinado)" if abs(z1f - z1) > 1 else "")
    feat(doc, part, "%s_V%d" % (cod, ix + 1), rot, _comp(vid, p0, th), VIDRO, 60, idx=ix)
    feat(doc, part, "%s_V%dM" % (cod, ix + 1), nome, _comp(perf, p0, th), FERRO if fe else PRETO, 0, idx=ix)
    if peit:
        feat(doc, part, "%s_V%dP" % (cod, ix + 1), "Peitoril granito", _comp(peit, p0, th), GRANITO, 0, idx=ix)


_janela_alu = janela
_porta_madeira = porta


def janela(doc, part, feat, cod, ix, rot, e, p0, th, t, H):
    z0 = float(e.get("chao", 0) or 0)
    z1 = z0 + min(float(e["alt"]), H - z0)
    z1f = float(e.get("_z1f", z1) or z1)
    if eh_ferro(e) or abs(z1f - z1) > 1:
        return grade(doc, part, feat, cod, ix, rot, e, p0, th, t, z0, z1, z1f)
    return _janela_alu(doc, part, feat, cod, ix, rot, e, p0, th, t, H)


def porta(doc, part, feat, cod, ix, rot, e, p0, th, t, H):
    if eh_ferro(e):
        z1 = min(float(e["alt"]), H)
        z1f = float(e.get("_z1f", z1) or z1)
        return grade(doc, part, feat, cod, ix, rot, e, p0, th, t, 0.0, z1, z1f)
    return _porta_madeira(doc, part, feat, cod, ix, rot, e, p0, th, t, H)


_campos_base = campos


def campos(QtW, form, tipo, e=None):
    """Campos de detalhe + ferro quadriculado e topo inclinado (iguais aos do app)."""
    e = e or {}
    if tipo not in ("Porta", "Janela"):
        return _campos_base(QtW, form, tipo, e)
    import marcenaria_conta as _CT
    pegar = {}
    if tipo == "Porta":
        c1 = QtW.QComboBox(); c1.addItems(["Esquerda", "Direita"])
        c1.setCurrentIndex(1 if str(e.get("dob", "e")).startswith("d") else 0)
        c2 = QtW.QComboBox(); c2.addItems(["Para dentro do ambiente", "Para fora"])
        c2.setCurrentIndex(1 if str(e.get("abre", "")).startswith("f") else 0)
        acs = ["madeira", "branca", "ferro"]
        c3 = QtW.QComboBox(); c3.addItems(["Madeira", "Branca", "Ferro e vidro quadriculado"])
        a_ = str(e.get("acab", "")).lower()
        c3.setCurrentIndex(2 if a_ == "ferro" else 1 if a_.startswith("bran") else 0)
        form.addRow("Dobradiça (olhando de dentro)", c1)
        form.addRow("Abre", c2)
        form.addRow("Acabamento", c3)
        pegar["dob"] = lambda: "d" if c1.currentIndex() else "e"
        pegar["abre"] = lambda: "fora" if c2.currentIndex() else "dentro"
        pegar["acab"] = lambda: acs[c3.currentIndex()]
    else:
        ops = ["", "correr", "maximar", "fixa", "ferro"]
        c = QtW.QComboBox()
        c.addItems(["Alumínio preto (automático)", "Alumínio de correr (2 folhas)", "Alumínio maxim-ar", "Alumínio fixa",
                    "Ferro quadriculado (serralheria)"])
        c.setCurrentIndex(ops.index(e.get("modelo")) if e.get("modelo") in ops else 0)
        form.addRow("Modelo", c)
        pegar["modelo"] = lambda: ops[c.currentIndex()]

    def sp(v, mx=20000):
        s_ = _CT.SpinConta(); s_.setRange(0, mx); s_.setValue(int(round(float(v or 0)))); return s_
    cols, lins, af = sp(e.get("cols"), 50), sp(e.get("lins"), 50), sp(e.get("alt_fim"))
    seg = QtW.QCheckBox("Topo acompanha a inclinação da parede")
    seg.setChecked(bool(e.get("segue")))
    form.addRow("Quadros na largura (ferro; 0 = auto)", cols)
    form.addRow("Quadros na altura (ferro; 0 = auto)", lins)
    form.addRow("Altura no fim (0 = topo reto)", af)
    form.addRow("", seg)
    pegar["cols"] = lambda: cols.value()
    pegar["lins"] = lambda: lins.value()
    pegar["alt_fim"] = lambda: af.value()
    pegar["segue"] = lambda: seg.isChecked()
    return lambda: {k: f() for k, f in pegar.items()}
