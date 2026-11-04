

# ================================================================== ponte com o app Medidor
# Modelos que nasceram no app (desenho em peças, o mesmo do app) e a ida/volta dos eletros.
# Frame do app: x da esquerda, y saindo da parede (0 = costas, D = frente), z para cima.
# Frame daqui:  x da esquerda, y = 0 na frente e +y para trás  ->  y_aqui = D - y_app.
ELETROS.update({
    "geladeira_im8s": dict(nome="Geladeira Electrolux Multidoor IM8S 590L", tipo="geladeira", desenho="app", k="geladeira",
                           L=835, A=1900, P=742, cor="#c3c7cc", nicho="50 mm livres em cima e 25 mm nas laterais"),
    "fogao_76gs": dict(nome="Fogão Electrolux 76GS 5 bocas", tipo="fogao", desenho="app", k="fogao",
                       L=763, A=949, P=674, cor="#c3c7cc", nicho="altura com a tampa de vidro fechada"),
    "cooktop_ie60p": dict(nome="Cooktop Electrolux indução IE60P", tipo="cooktop", desenho="app", k="cooktop",
                          L=590, A=6, P=520, cor="#17181a", recorte=(560, 490), bocas=4,
                          nicho="recorte 560 x 490; corpo desce uns 40 mm abaixo do tampo"),
    "forno_oe8eh": dict(nome="Forno de embutir Electrolux 80L OE8EH", tipo="forno", desenho="app", k="forno",
                        L=596, A=596, P=613, cor="#b9bdc2", nicho="vão 600 x 600, altura interna 610, prof. do móvel 600"),
    "micro_me3ep": dict(nome="Micro-ondas de embutir Electrolux ME3EP 34L", tipo="micro", desenho="app", k="micro",
                        L=540, A=366, P=395, cor="#2a2c2f", nicho="medida sem moldura: confira o nicho no manual"),
    "coifa_60cts": dict(nome="Coifa de parede Electrolux 60CTS", tipo="coifa", desenho="app", k="coifa",
                        L=600, A=830, P=500, cor="#c3c7cc", nicho="altura regulável de 830 a 1145"),
    "lavaloucas_ll14x": dict(nome="Lava-louças Electrolux LL14X 14 serviços", tipo="lava_loucas", desenho="app",
                             k="lava_loucas", L=598, A=845, P=610, cor="#c3c7cc", nicho="vão de 600"),
    "lavadora_lda13": dict(nome="Lavadora Electrolux LDA13 13 kg", tipo="lavadora", desenho="app", k="lavadora",
                           L=590, A=1040, P=667, cor="#eef0f2", nicho="abre em cima: deixe a tampa livre"),
})
for _k in ("forno_oe8eh", "micro_me3ep", "cooktop_ie60p", "geladeira_im8s", "fogao_76gs", "coifa_60cts",
           "lavaloucas_ll14x", "lavadora_lda13"):
    if _k not in ORDEM:
        ORDEM.append(_k)
# tipo do app de cada modelo nativo daqui (para mandar o catálogo para o app)
_TIPO_APP = {"forno": "forno", "micro": "micro", "cooktop": "cooktop", "geladeira": "geladeira"}
_NIVEL_EMBUTIR = ("forno", "micro", "cooktop")       # os que encaixam dentro de um módulo


def _hex(c, padrao="#9e8fb2"):
    c = (c or padrao).lstrip("#")
    if len(c) != 6:
        c = padrao.lstrip("#")
    return tuple(int(c[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def _mix(a, b, t):
    a, b = _hex(a), _hex(b)
    return "#" + "".join("%02x" % int(round((a[i] + (b[i] - a[i]) * t) * 255)) for i in range(3))


def pecas_app(k, W, H, Dp, cor=None, est=None, nome=None):
    """Mesmo desenho do app (pecasObjeto), em sólidos. Devolve [(shape, cor, transp, sufixo)]."""
    import Part
    W, H, Dp = float(W), float(H), float(Dp)
    c = cor or "#9e8fb2"
    out = []
    PRETO, VID, INOXc, ESC = "#1a1c1f", "#2b3540", "#d3d6da", "#4a4e53"
    esc_, cl = _mix(c, "#000000", .25), _mix(c, "#ffffff", .35)

    def B(x0, x1, y0, y1, z0, z1, cr, v=None, suf=""):
        if x1 - x0 > .5 and y1 - y0 > .5 and z1 - z0 > .5:
            out.append((_cx(x0, Dp - y1, z0, x1 - x0, y1 - y0, z1 - z0), _hex(cr), 60 if v else 0, suf))

    def Dc(x, y, z, r, cr, eixo="z", suf=""):
        if eixo == "z":
            s = _cil(r, 2, x, Dp - y, z)
        else:
            s = _cil(r, 2, x, Dp - y, z, (0, -1, 0))
        out.append((s, _hex(cr), 0, suf))

    if k == "geladeira":
        pt, gap = 40, 8
        yb = Dp - pt - 25
        B(0, W, 0, yb, 0, H, esc_, suf=" gabinete"); B(30, W - 30, yb, yb + 20, 0, 70, ESC, suf=" grade")
        if est == "sbs":
            xm = W * .443
            B(0, xm - gap / 2, yb, Dp - 25, 70, H, c, suf=" porta freezer"); B(xm + gap / 2, W, yb, Dp - 25, 70, H, c, suf=" porta refrigerador")
            B(xm - 45, xm - 12, Dp - 25, Dp, H * .17, H * .76, ESC, suf=" puxador"); B(xm + 12, xm + 45, Dp - 25, Dp, H * .17, H * .76, ESC, suf=" puxador")
            B(xm - 45, xm - 12, Dp - 26, Dp - 24, H * .78, H * .95, PRETO, suf=" painel")
        elif W >= 760:
            zf = H * .36
            B(0, W, yb, Dp - 25, 70, zf - gap / 2, c, suf=" gaveta freezer")
            B(0, W / 2 - gap / 2, yb, Dp - 25, zf + gap / 2, H, c, suf=" porta esquerda")
            B(W / 2 + gap / 2, W, yb, Dp - 25, zf + gap / 2, H, c, suf=" porta direita")
            B(60, W - 60, Dp - 25, Dp, zf - 120, zf - 100, INOXc, suf=" puxador gaveta")
            B(W / 2 - 50, W / 2 - 30, Dp - 25, Dp, zf + 150, zf + 150 + H * .4, INOXc, suf=" puxador")
            B(W / 2 + 30, W / 2 + 50, Dp - 25, Dp, zf + 150, zf + 150 + H * .4, INOXc, suf=" puxador")
            B(W * .62, W * .62 + 140, Dp - 26, Dp - 24, H - 330, H - 260, PRETO, suf=" painel")
        else:
            zf = H * .7
            B(0, W, yb, Dp - 25, 70, zf - gap / 2, c, suf=" porta refrigerador"); B(0, W, yb, Dp - 25, zf + gap / 2, H, c, suf=" porta freezer")
            B(W - 70, W - 50, Dp - 25, Dp, zf - 120 - H * .35, zf - 120, INOXc, suf=" puxador")
            B(W - 70, W - 50, Dp - 25, Dp, zf + 60, zf + 60 + H * .15, INOXc, suf=" puxador")
    elif k == "fogao":
        zm, ns = H - 60, (5 if W >= 700 else 4)
        B(40, W - 40, 0, Dp - 60, 0, 70, PRETO, suf=" rodapé"); B(0, W, 0, Dp - 30, 70, zm, c, suf=" corpo")
        B(40, W - 40, Dp - 30, Dp - 10, 110, zm - 170, PRETO, suf=" porta do forno"); B(90, W - 90, Dp - 12, Dp - 9, 170, zm - 240, VID, suf=" visor")
        B(60, W - 60, Dp - 10, Dp, zm - 210, zm - 190, INOXc, suf=" puxador")
        B(0, W, Dp - 30, Dp - 5, zm - 150, zm, ESC, suf=" painel")
        for i in range(ns):
            Dc(W * (i + 1) / (ns + 1), Dp - 5, zm - 75, 22, INOXc, "n", " botão")
        B(0, W, 0, Dp, zm, zm + 12, PRETO, suf=" mesa")
        bc = [(.22, .27, 1), (.78, .27, 1), (.22, .73, 1), (.78, .73, 1), (.5, .5, 1.25)] if ns == 5 else \
            [(.28, .28, 1), (.72, .28, 1), (.28, .72, 1), (.72, .72, 1)]
        for fx, fy, kk in bc:
            Dc(W * fx, Dp * (1 - fy), zm + 12, 45 * kk, "#3c3f43", suf=" queimador")
            Dc(W * fx, Dp * (1 - fy), zm + 14, 26 * kk, "#111214", suf=" capa")
        B(0, W, 0, 20, zm + 12, H, "#2c3036", True, " tampa de vidro")
    elif k == "cooktop":
        ind = bool(nome and "indu" in nome.lower()) or H < 20
        gv = min(H, 6)
        B(0, W, 0, Dp, 0, gv, PRETO, suf=" vidro")
        B(45, W - 45, 30, Dp - 30, -40, 0, ESC, suf=" corpo (abaixo do tampo)")
        zs = [(.2, .3, .7), (.8, .3, .7), (.2, .72, .8), (.8, .72, .8), (.5, .5, 1.2)] if W >= 700 else \
            [(.27, .3, 1), (.73, .3, .8), (.27, .72, .8), (.73, .72, 1)]
        for fx, fy, kk in zs:
            x, y, r = W * fx, Dp * (1 - fy), min(W, Dp) * .17 * kk
            if ind:
                Dc(x, y, gv, r, "#5d6166", suf=" zona"); Dc(x, y, gv + 1, r - 10, PRETO, suf=" zona")
            else:
                Dc(x, y, gv, r * .6, "#7d8186", suf=" queimador"); Dc(x, y, gv + 10, r * .42, "#111214", suf=" capa")
                if H > 15:
                    g, zt = r * 1.45, max(gv + 10, H - 8)
                    B(x - g, x + g, y - 5, y + 5, zt, H, "#202124", suf=" grade"); B(x - 5, x + 5, y - g, y + g, zt, H, "#202124", suf=" grade")
    elif k == "forno":
        pn = 95
        B(0, W, 0, Dp - 50, 0, H, esc_, suf=" corpo"); B(0, W, Dp - 50, Dp - 25, H - pn, H, ESC, suf=" painel")
        B(W * .42, W * .58, Dp - 26, Dp - 24, H - pn + 28, H - 28, "#0c3b52", suf=" display")
        Dc(W * .18, Dp - 25, H - pn / 2, 20, INOXc, "n", " botão"); Dc(W * .82, Dp - 25, H - pn / 2, 20, INOXc, "n", " botão")
        B(0, W, Dp - 50, Dp - 25, 0, H - pn - 4, PRETO, suf=" porta de vidro"); B(70, W - 70, Dp - 26, Dp - 24, 60, H - pn - 80, VID, suf=" visor")
        B(50, W - 50, Dp - 25, Dp, H - pn - 55, H - pn - 38, c, suf=" puxador")
    elif k == "micro":
        pw = min(130, W * .24)
        B(0, W, 0, Dp - 25, 0, H, esc_, suf=" corpo"); B(0, W - pw, Dp - 25, Dp, 0, H, PRETO, suf=" porta")
        B(45, W - pw - 45, Dp - 1, Dp, 45, H - 45, VID, suf=" visor")
        B(W - pw, W, Dp - 25, Dp, 0, H, "#33363a", suf=" painel"); B(W - pw + 20, W - 20, Dp - 1, Dp, H - 80, H - 40, "#0c3b52", suf=" display")
        for i in range(3):
            B(W - pw + 20, W - 20, Dp - 1, Dp, H - 130 - i * 45, H - 100 - i * 45, ESC, suf=" tecla")
    elif k == "coifa":
        hc, cw, cd = 80, min(280, W * .45), min(250, Dp * .5)
        B(0, W, 0, Dp, 0, hc, c, suf=" corpo"); B(W * .08, W * .92, 0, Dp * .85, hc, hc + 90, c, suf=" corpo")
        B(W * .18, W * .82, 0, Dp * .65, hc + 90, hc + 150, c, suf=" corpo"); B(W / 2 - cw / 2, W / 2 + cw / 2, 0, cd, hc + 150, H, c, suf=" chaminé")
        for i in range(4):
            B(W * .3 + i * W * .1, W * .3 + i * W * .1 + W * .05, Dp - 1, Dp, 25, 45, "#3a6ea5", suf=" tecla")
    elif k == "lava_loucas":
        B(40, W - 40, 0, Dp - 60, 0, 80, PRETO, suf=" rodapé"); B(0, W, 0, Dp - 30, 80, H, esc_, suf=" corpo")
        B(0, W, Dp - 30, Dp, 90, H - 100, c, suf=" porta"); B(0, W, Dp - 30, Dp, H - 98, H, ESC, suf=" painel")
        B(W * .62, W * .85, Dp - 1, Dp, H - 70, H - 35, "#0c3b52", suf=" display"); B(W * .25, W * .75, Dp, Dp + 1, H - 150, H - 130, INOXc, suf=" puxador")
    elif k == "lavadora":
        if H >= 950:
            zt = H - 170
            B(0, W, 0, Dp, 0, zt, c, suf=" corpo"); B(10, W - 10, 140, Dp - 15, zt, zt + 15, cl, suf=" tampa")
            Dc(W / 2, (140 + Dp) / 2, zt + 15, min(W, Dp - 180) * .32, "#aeb9c4", suf=" visor da tampa")
            B(0, W, 0, 130, zt, H, cl, suf=" painel"); B(W * .35, W * .65, 129, 131, zt + 60, H - 40, "#0c3b52", suf=" display")
        else:
            B(0, W, 0, Dp, 0, H, c, suf=" corpo"); B(0, W, Dp - 2, Dp, H - 120, H, cl, suf=" painel")
            B(25, W * .35, Dp - 1, Dp + 1, H - 100, H - 30, "#d9dcdf", suf=" gaveta sabão")
            r, zc = min(W, H) * .33, (H - 120) * .5
            Dc(W / 2, Dp, zc, r, "#b9bdc2", "n", " porta"); Dc(W / 2, Dp + 1, zc, r * .78, VID, "n", " visor")
    elif k in ("cuba", "lavatorio"):
        e = 18 if k == "cuba" else 22
        cc = c if k == "cuba" else "#f4f4f2"
        try:
            s = _cx(0, 0, 0, W, Dp, H).cut(_cx(e, e, e, W - 2 * e, Dp - 2 * e, H))
            out.append((s, _hex(cc), 0, " cuba"))
        except Exception:
            B(0, W, 0, Dp, 0, H, cc, suf=" cuba")
        Dc(W / 2, Dp / 2, e, 22, ESC, suf=" ralo")
    elif k == "torneira":
        t = min(W, 50)
        B(W / 2 - t / 2, W / 2 + t / 2, 0, t, 0, H, c, suf=" corpo"); B(W / 2 - t * .35, W / 2 + t * .35, t, Dp, H - 35, H, c, suf=" bica")
        B(W / 2 - t * .3, W / 2 + t * .3, Dp - 35, Dp, H - 90, H - 35, c, suf=" bica"); B(W / 2 - 8, W / 2 + 8, 0, t, H, H + 50, _mix(c, "#000000", .15), suf=" alavanca")
    elif k == "vaso":
        zs = min(400, H * .52)
        B(W * .22, W * .78, 180, Dp - 140, 0, zs - 150, c, suf=" pé"); B(15, W - 15, 170, Dp, zs - 150, zs - 20, c, suf=" bacia")
        B(10, W - 10, 165, Dp + 5, zs - 20, zs, _mix(c, "#000000", .06), suf=" assento"); B(5, W - 5, 0, 175, zs, H, c, suf=" caixa acoplada")
        Dc(W / 2, 90, H, 28, "#c9ccd0", suf=" botão")
    elif k == "tv":
        B(0, W, 0, Dp, 0, H, c, suf=" corpo"); B(12, W - 12, Dp - 1, Dp + 1, 30, H - 12, "#22303d", suf=" tela")
    elif k == "ar":
        B(0, W, 0, Dp, 0, H, c, suf=" corpo"); B(25, W - 25, Dp - 1, Dp + 1, 25, 70, "#c9ccd0", suf=" saída de ar")
    elif k == "cama":
        zc, cab = min(500, H * .46), 60
        B(0, W, 0, cab, 0, H, _mix(c, "#000000", .15), suf=" cabeceira"); B(30, W - 30, cab, Dp - 30, 0, zc - 230, "#3b3d40", suf=" base")
        B(0, W, cab, Dp, zc - 230, zc - 200, c, suf=" estrado"); B(10, W - 10, cab + 5, Dp - 10, zc - 200, zc, "#f1eee8", suf=" colchão")
        B(10, W - 10, cab + 500, Dp - 10, zc, zc + 25, _mix(c, "#ffffff", .25), suf=" edredom")
        np_ = 2 if W >= 1200 else 1
        lp = (W - 60 - (np_ - 1) * 40) / np_
        for i in range(np_):
            x = 30 + i * (lp + 40)
            B(x, x + lp, cab + 40, cab + 400, zc, zc + 110, "#fbfaf7", suf=" travesseiro")
    elif k == "sofa":
        br, enc, zs = min(170, W * .12), min(230, Dp * .28), min(430, H * .5)
        ns = 3 if W >= 1800 else 2
        lw, cor2 = (W - 2 * br) / ns, _mix(c, "#ffffff", .12)
        for x, y in ((40, 40), (W - 80, 40), (40, Dp - 80), (W - 80, Dp - 80)):
            B(x, x + 40, y, y + 40, 0, 80, "#3b3d40", suf=" pé")
        B(0, W, 0, Dp, 80, zs - 140, _mix(c, "#000000", .1), suf=" base")
        B(0, br, 0, Dp, 80, min(H, zs + 200), c, suf=" braço"); B(W - br, W, 0, Dp, 80, min(H, zs + 200), c, suf=" braço")
        B(br, W - br, 0, enc, zs - 140, H, c, suf=" encosto")
        for i in range(ns):
            x = br + i * lw
            B(x + 4, x + lw - 4, enc, Dp - 10, zs - 140, zs, cor2, suf=" assento"); B(x + 4, x + lw - 4, enc, enc + 170, zs, H - 60, cor2, suf=" almofada")
    elif k == "mesa":
        e, pe, r = min(40, H * .06), 55, 40
        B(0, W, 0, Dp, H - e, H, c, suf=" tampo")
        for x, y in ((r, r), (W - r - pe, r), (r, Dp - r - pe), (W - r - pe, Dp - r - pe)):
            B(x, x + pe, y, y + pe, 0, H - e, _mix(c, "#000000", .15), suf=" pé")
    else:
        B(0, W, 0, Dp, 0, H, c, suf=" caixa")
    return out


_pecas_nativas = pecas_do_eletro


def pecas_do_eletro(chave):
    m = ELETROS[chave]
    if m.get("desenho") == "app":
        return pecas_app(m["k"], m["L"], m["A"], m["P"], m.get("cor"), m.get("est"), m["nome"])
    return _pecas_nativas(chave)


def _desenhar_lista(cont, pecas, tag, nome):
    doc = cont.Document
    g = _grupo(cont)
    for i, (shp, cor, tr, suf) in enumerate(pecas):
        o = doc.addObject("Part::Feature", "%s_EL_%s_%d" % (cont.Name, tag, i))
        o.Label = "%s %s%s" % (cont.Name, nome, suf)
        o.Shape = shp
        o.addProperty("App::PropertyString", "Eletro", "Marcenaria")
        o.Eletro = tag
        g.addObject(o)
        try:
            o.ViewObject.ShapeColor = cor
            o.ViewObject.Transparency = tr
        except Exception:
            pass


def catalogo_para_app():
    """Lista de eletros desta bancada no formato do app (vai junto com 'Enviar preços para o tablet')."""
    out = []
    for k in ORDEM:
        m = ELETROS[k]
        tipo = m.get("k") or _TIPO_APP.get(m["tipo"])
        if not tipo:
            continue
        alt = m["A"]
        if m["tipo"] == "cooktop" and m.get("desenho") != "app":
            alt = 47                                   # no app conta só o que fica acima do tampo (vidro + grades)
        e = {"id": k, "k": tipo, "n": m["nome"], "larg": m["L"], "alt": alt, "prof": m["P"], "obs": m.get("nicho", "")}
        if k == "geladeira_is4s":
            e["est"] = "sbs"
        out.append(e)
    return out


def do_app(doc, o, parede, nivel=0.0):
    """Cria no FreeCAD um eletro/objeto que veio do app, na parede e posição medidas."""
    W, H, P = float(o.get("larg") or 0), float(o.get("alt") or 0), float(o.get("prof") or 0)
    if W <= 0 or H <= 0 or P <= 0:
        return None
    ch = o.get("mod") if o.get("mod") in ELETROS else None
    if ch and (abs(ELETROS[ch]["L"] - W) > 5 or abs(ELETROS[ch]["P"] - P) > 5):
        ch = None                                    # medida mudada no app: desenha com a medida do app
    n = 1
    while doc.getObject("EL%02d" % n) is not None:
        n += 1
    p = doc.addObject("App::Part", "EL%02d" % n)
    nome = (o.get("nome") or "").strip() or (ELETROS[ch]["nome"] if ch else o.get("k", "objeto"))
    p.Label = "EL%02d_%s" % (n, nome.replace(" ", "_"))
    for prop, tp, v in (("Marcenaria", "App::PropertyString", "eletro"), ("AppId", "App::PropertyString", o.get("id", "")),
                        ("AppTipo", "App::PropertyString", o.get("k", "")),
                        ("EletroParede", "App::PropertyString", parede.Name),
                        ("EletroDist", "App::PropertyFloat", float(o.get("dist") or 0)),
                        ("EletroAfast", "App::PropertyFloat", float(o.get("afast") or 0)),
                        ("EletroZ", "App::PropertyFloat", float(o.get("z") or 0))):
        p.addProperty(tp, prop, "Marcenaria")
        setattr(p, prop, v)
    if ch:
        definir(p, [ch])
        desenhar(p, ch, 0, 0, 0)
    else:
        definir(p, [])
        _desenhar_lista(p, pecas_app(o.get("k"), W, H, P, o.get("cor"), None, nome), "app", nome)
    th = parede.Direcao
    r = math.radians(th)
    u, nn = V(math.cos(r), math.sin(r), 0), V(-math.sin(r), math.cos(r), 0)
    Pp = ELETROS[ch]["P"] if ch else P
    base = V(parede.InicioX, parede.InicioY, 0) + u * p.EletroDist - nn * (p.EletroAfast + Pp)
    p.Placement = App.Placement(base + V(0, 0, p.EletroZ + nivel), App.Rotation(V(0, 0, 1), th))
    return p
