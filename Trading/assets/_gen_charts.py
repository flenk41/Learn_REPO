# -*- coding: utf-8 -*-
"""Генератор реалистичных свечных графиков (SVG) для трека Trading.
Стиль: тёплый янтарный фон, зелёные/красные свечи, золотой акцент.
Запуск: python _gen_charts.py  -> создаёт *.svg в этой папке.
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# палитра
BG = "#fffbeb"; PANEL = "#ffffff"; GRID = "#f3e8c8"
UP = "#22c55e"; UPD = "#166534"; DN = "#ef4444"; DND = "#991b1b"
GOLD = "#ca8a04"; INK = "#713f12"; SUB = "#92400e"; MUTE = "#a8a29e"
FONT = "Segoe UI, Arial, sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Chart:
    """Холст с пересчётом цена->координаты в заданной панели."""
    def __init__(self, w, h):
        self.w = w; self.h = h; self.s = []

    def add(self, frag): self.s.append(frag)

    def panel(self, x, y, pw, ph, pmin, pmax):
        self.px, self.py, self.pw, self.ph = x, y, pw, ph
        self.pmin, self.pmax = pmin, pmax

    def X(self, i, n):  # индекс свечи -> x (центр)
        step = self.pw / (n + 1)
        return self.px + step * (i + 1)

    def Y(self, price):
        return self.py + (self.pmax - price) / (self.pmax - self.pmin) * self.ph

    def grid(self, n, ticks):
        self.add(f'<rect x="{self.px}" y="{self.py}" width="{self.pw}" height="{self.ph}" rx="8" fill="{PANEL}"/>')
        for t in ticks:
            yy = self.Y(t)
            self.add(f'<line x1="{self.px}" y1="{yy:.1f}" x2="{self.px+self.pw}" y2="{yy:.1f}" stroke="{GRID}" stroke-width="1"/>')
            self.add(f'<text x="{self.px+self.pw+6}" y="{yy+4:.1f}" font-size="10.5" fill="{MUTE}">{t}</text>')

    def candles(self, data, n=None):
        """data: list of (o,h,l,c). Рисует свечи."""
        n = n or len(data)
        bw = max(6, self.pw / (n + 1) * 0.55)
        for i, (o, hi, lo, c) in enumerate(data):
            x = self.X(i, n)
            up = c >= o
            col = UP if up else DN; cold = UPD if up else DND
            self.add(f'<line x1="{x:.1f}" y1="{self.Y(hi):.1f}" x2="{x:.1f}" y2="{self.Y(lo):.1f}" stroke="{cold}" stroke-width="1.5"/>')
            top = self.Y(max(o, c)); bot = self.Y(min(o, c))
            bh = max(2, bot - top)
            self.add(f'<rect x="{x-bw/2:.1f}" y="{top:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="1.5" fill="{col}" stroke="{cold}" stroke-width="1"/>')

    def hline(self, price, color, label="", dash="", width=2):
        yy = self.Y(price)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{self.px}" y1="{yy:.1f}" x2="{self.px+self.pw}" y2="{yy:.1f}" stroke="{color}" stroke-width="{width}"{d}/>')
        if label:
            self.add(f'<rect x="{self.px+4}" y="{yy-16:.1f}" width="{8+6.2*len(label):.0f}" height="15" rx="3" fill="{color}"/>')
            self.add(f'<text x="{self.px+8}" y="{yy-4:.1f}" font-size="10.5" fill="#fff" font-weight="700">{esc(label)}</text>')

    def polyline(self, pts, color, width=2.5, dash=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.add(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{width}"{d}/>')

    def ma(self, data, period, color, n=None, width=2.2):
        n = n or len(data)
        closes = [c for (_, _, _, c) in data]
        pts = []
        for i in range(len(closes)):
            if i + 1 < period:
                continue
            avg = sum(closes[i + 1 - period:i + 1]) / period
            pts.append((self.X(i, n), self.Y(avg)))
        self.polyline(pts, color, width)
        return pts

    def text(self, x, y, s, size=12, color=INK, anchor="start", weight="400", style="normal"):
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}" font-style="{style}">{esc(s)}</text>')

    def title(self, s, sub=""):
        self.text(self.w/2, 30, s, 19, INK, "middle", "700")
        if sub:
            self.text(self.w/2, 50, sub, 12.5, SUB, "middle")

    def svg(self):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'font-family="{FONT}">\n<rect width="{self.w}" height="{self.h}" rx="16" fill="{BG}"/>\n')
        return head + "\n".join(self.s) + "\n</svg>\n"


def save(name, chart):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(chart.svg())
    print("wrote", name)


# ---------- генерация рядов цен (детерминированно) ----------
def candle(o, c, wick=1.0, tail=1.0):
    hi = max(o, c) + wick
    lo = min(o, c) - tail
    return (o, hi, lo, c)


# ============== 1. Как читать реальный график ==============
def chart_reading():
    ch = Chart(760, 430)
    ch.title("Реальный график: тренд, откат, объём", "фьючерс · таймфрейм 1H · цена в пунктах")
    seq = [  # (open, close)
        (100, 103), (103, 102), (102, 106), (106, 108), (108, 107),
        (107, 111), (111, 114), (114, 113), (113, 117), (117, 120),
        (120, 118), (118, 115), (115, 116), (116, 113), (113, 117),
        (117, 121), (121, 124), (124, 123), (123, 127), (127, 130),
    ]
    data = [candle(o, c, 1.4, 1.4) for o, c in seq]
    ch.panel(70, 64, 600, 250, 96, 134)
    ch.grid(len(data), [100, 110, 120, 130])
    ch.candles(data)
    # подписи фаз
    ch.text(150, 300, "восходящий тренд", 11.5, UPD, weight="700")
    ch.text(330, 150, "откат (коррекция)", 11.5, DND, weight="700")
    ch.text(560, 95, "новый максимум", 11.5, GOLD, weight="700")
    # объёмы
    vols = [3, 2, 4, 5, 3, 6, 7, 3, 6, 8, 5, 6, 3, 4, 5, 7, 8, 4, 7, 9]
    vx0, vy0, vh = 70, 330, 60
    ch.add(f'<text x="64" y="{vy0+10}" font-size="10.5" fill="{MUTE}" text-anchor="end">Объём</text>')
    for i, v in enumerate(vols):
        x = ch.X(i, len(data)); bw = 9
        up = seq[i][1] >= seq[i][0]
        col = "#86efac" if up else "#fca5a5"
        bh = v / 9 * vh
        ch.add(f'<rect x="{x-bw/2:.1f}" y="{vy0+vh-bh:.1f}" width="{bw}" height="{bh:.1f}" fill="{col}"/>')
    ch.text(380, 415, "Цена слева, время слева→направо. Внизу — объём (сколько наторговали за свечу).",
            11.5, SUB, "middle", style="italic")
    save("chart-real.svg", ch)


# ============== 2. Линия тренда и канал ==============
def chart_trendline():
    ch = Chart(760, 420)
    ch.title("Восходящий канал на реальных свечах", "цена идёт между двумя параллельными линиями")
    seq = [
        (100, 104), (104, 101), (101, 106), (106, 109), (109, 105),
        (105, 110), (110, 113), (113, 109), (109, 114), (114, 117),
        (117, 113), (113, 118), (118, 121), (121, 117), (117, 122),
        (122, 125), (125, 121), (121, 126),
    ]
    data = [candle(o, c, 1.3, 1.3) for o, c in seq]
    n = len(data)
    ch.panel(70, 64, 620, 290, 96, 130)
    ch.grid(n, [100, 110, 120, 130])
    ch.candles(data)
    # нижняя линия поддержки тренда (по минимумам) и верхняя (по максимумам)
    x0, x1 = ch.X(0, n), ch.X(n - 1, n)
    ch.polyline([(x0, ch.Y(99)), (x1, ch.Y(120))], GOLD, 2.5)
    ch.polyline([(x0, ch.Y(106)), (x1, ch.Y(128))], GOLD, 2.5, dash="6 4")
    ch.text(x1 - 4, ch.Y(120) + 18, "линия поддержки (покупай у неё)", 11, UPD, "end", "700")
    ch.text(x1 - 4, ch.Y(128) - 6, "линия сопротивления (фиксируй)", 11, DND, "end", "700")
    # отметки касаний
    for i in (2, 7, 13):
        x = ch.X(i, n); y = ch.Y(data[i][2])
        ch.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="none" stroke="{UPD}" stroke-width="2"/>')
    ch.text(380, 405, "Чем больше касаний — тем надёжнее линия. Пробой канала = смена настроения рынка.",
            11.5, SUB, "middle", style="italic")
    save("trendline-real.svg", ch)


# ============== 3. Свечные паттерны в контексте ==============
def chart_candle_patterns():
    ch = Chart(760, 420)
    ch.title("Свечные паттерны разворота — где они работают", "сигнал силён только НА УРОВНЕ, не в пустоте")

    def mini(x0, title, data, pmin, pmax, mark_i, note, ncolor):
        sub = Chart(0, 0)  # reuse methods via temp? simpler inline
        pw, ph, py = 180, 210, 80
        ch.panel(x0, py, pw, ph, pmin, pmax)
        ch.grid(len(data), [])
        ch.text(x0 + pw/2, py - 10, title, 12.5, INK, "middle", "700")
        ch.candles(data)
        # подсветка ключевой свечи
        x = ch.X(mark_i, len(data))
        ch.add(f'<rect x="{x-16:.1f}" y="{py+4}" width="32" height="{ph-8}" rx="4" fill="none" stroke="{ncolor}" stroke-width="2" stroke-dasharray="4 3"/>')
        ch.text(x0 + pw/2, py + ph + 22, note, 11, ncolor, "middle", "700")

    # Молот (пин-бар) у поддержки
    d1 = [candle(120, 116, 1, 1), candle(116, 112, 1, 1), candle(112, 108, 1, 1),
          (108, 109, 100, 108.5), candle(108.5, 113, 1, 1), candle(113, 117, 1, 1)]
    mini(60, "Молот (пин-бар)", d1, 98, 124, 3, "длинная нижняя тень = откуп", UPD)
    # Бычье поглощение
    d2 = [candle(118, 115, 1, 1), candle(115, 112, 1, 1), candle(112, 109, 1, 1),
          candle(110, 117, 1, 1), candle(117, 120, 1, 1), candle(120, 122, 1, 1)]
    mini(290, "Бычье поглощение", d2, 106, 125, 3, "зелёная съела красную", UPD)
    # Доджи на вершине
    d3 = [candle(108, 112, 1, 1), candle(112, 116, 1, 1), candle(116, 120, 1, 1),
          (120, 121.5, 118.5, 120.2), candle(120, 116, 1, 1), candle(116, 112, 1, 1)]
    mini(520, "Доджи (нерешительность)", d3, 106, 124, 3, "крест на вершине = стоп роста", DND)

    ch.text(380, 405, "Паттерн — это подсказка о развороте, а не гарантия. Подтверждай следующей свечой и объёмом.",
            11.5, SUB, "middle", style="italic")
    save("candle-patterns-real.svg", ch)


# ============== 4. Скользящие средние + золотой крест ==============
def chart_moving_averages():
    ch = Chart(760, 420)
    ch.title("Скользящие средние и «золотой крест»", "MA(50) пересекает MA(200) снизу вверх — сигнал тренда")
    seq = [
        (100, 98), (98, 96), (96, 97), (97, 95), (95, 94), (94, 96), (96, 95),
        (95, 97), (97, 99), (99, 98), (98, 101), (101, 100), (100, 103), (103, 105),
        (105, 104), (104, 107), (107, 110), (110, 109), (109, 112), (112, 115),
        (115, 114), (114, 117), (117, 120), (120, 119), (119, 122),
    ]
    data = [candle(o, c, 1.1, 1.1) for o, c in seq]
    n = len(data)
    ch.panel(70, 64, 620, 290, 90, 126)
    ch.grid(n, [90, 100, 110, 120])
    ch.candles(data)
    fast = ch.ma(data, 5, "#2563eb", n)      # «быстрая» (имитация MA50)
    slow = ch.ma(data, 10, "#dc2626", n)     # «медленная» (имитация MA200)
    ch.text(90, 80, "— MA «быстрая» (50)", 11.5, "#2563eb", weight="700")
    ch.text(90, 96, "— MA «медленная» (200)", 11.5, "#dc2626", weight="700")
    # точка золотого креста (примерно там где fast пересекает slow вверх)
    if fast and slow:
        cx, cy = fast[len(fast)//2]
        ch.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="9" fill="none" stroke="{GOLD}" stroke-width="2.5"/>')
        ch.text(cx, cy - 14, "золотой крест ↑", 11.5, GOLD, "middle", "700")
    ch.text(380, 405, "Цена выше MA — тренд вверх. Пересечение быстрой и медленной MA = ранний сигнал смены тренда.",
            11.5, SUB, "middle", style="italic")
    save("moving-averages-real.svg", ch)


# ============== 5. Осцилляторы: цена + RSI + MACD ==============
def chart_oscillators():
    ch = Chart(760, 520)
    ch.title("Мультипанель: цена + RSI + MACD", "как выглядит терминал с индикаторами под графиком")
    seq = [
        (100, 103), (103, 106), (106, 109), (109, 112), (112, 115),
        (115, 117), (117, 119), (119, 118), (118, 116), (116, 113),
        (113, 111), (111, 113), (113, 116), (116, 119), (119, 121),
    ]
    data = [candle(o, c, 1.2, 1.2) for o, c in seq]
    n = len(data)
    # панель цены
    ch.panel(70, 60, 620, 180, 96, 124)
    ch.grid(n, [100, 110, 120])
    ch.candles(data)
    ch.text(78, 76, "ЦЕНА", 11, MUTE, weight="700")
    # RSI панель
    rsi_y, rsi_h = 270, 90
    ch.add(f'<rect x="70" y="{rsi_y}" width="620" height="{rsi_h}" rx="8" fill="{PANEL}"/>')
    ch.text(78, rsi_y + 16, "RSI (14)", 11, MUTE, weight="700")
    def rsi_to_y(v): return rsi_y + (100 - v) / 100 * rsi_h
    for lvl, col, lab in [(70, "#dc2626", "70 перекуплен"), (30, "#16a34a", "30 перепродан")]:
        yy = rsi_to_y(lvl)
        ch.add(f'<line x1="70" y1="{yy:.1f}" x2="690" y2="{yy:.1f}" stroke="{col}" stroke-width="1" stroke-dasharray="5 3"/>')
        ch.text(694, yy + 4, lab, 9.5, col)
    rsi_vals = [50, 58, 64, 70, 75, 78, 80, 76, 68, 58, 48, 52, 60, 68, 74]
    ch.polyline([(ch.X(i, n), rsi_to_y(v)) for i, v in enumerate(rsi_vals)], "#7c3aed", 2.2)
    # отметка перекупленности
    xi = ch.X(6, n)
    ch.add(f'<circle cx="{xi:.1f}" cy="{rsi_to_y(80):.1f}" r="6" fill="none" stroke="#dc2626" stroke-width="2"/>')
    # MACD панель
    m_y, m_h = 390, 100
    ch.add(f'<rect x="70" y="{m_y}" width="620" height="{m_h}" rx="8" fill="{PANEL}"/>')
    ch.text(78, m_y + 16, "MACD", 11, MUTE, weight="700")
    mid = m_y + m_h / 2
    ch.add(f'<line x1="70" y1="{mid}" x2="690" y2="{mid}" stroke="{GRID}" stroke-width="1.5"/>')
    hist = [1, 2, 3, 4, 4, 3, 2, 0, -2, -3, -3, -1, 1, 3, 4]
    for i, hgt in enumerate(hist):
        x = ch.X(i, n); bw = 12
        col = "#86efac" if hgt >= 0 else "#fca5a5"
        bh = abs(hgt) * 8
        yy = mid - bh if hgt >= 0 else mid
        ch.add(f'<rect x="{x-bw/2:.1f}" y="{yy:.1f}" width="{bw}" height="{bh:.1f}" fill="{col}"/>')
    macd_line = [(ch.X(i, n), mid - hist[i] * 7) for i in range(n)]
    ch.polyline(macd_line, "#2563eb", 2)
    ch.text(380, 508, "RSI>70 = перекуплен (рискованно покупать). MACD-гистограмма меняет знак = сдвиг импульса.",
            11.5, SUB, "middle", style="italic")
    save("oscillators-real.svg", ch)


# ============== 6. Полный разбор сделки (вход/стоп/тейк) ==============
def chart_trade():
    ch = Chart(760, 440)
    ch.title("Разбор сделки: вход, стоп-лосс, тейк-профит, R:R", "лонг от поддержки · риск 1:3")
    seq = [
        (110, 107), (107, 104), (104, 101), (101, 100), (100, 102),
        (102, 101), (101, 104), (104, 106), (106, 105), (105, 108),
        (108, 111), (111, 110), (110, 113), (113, 116), (116, 119),
        (119, 118), (118, 121), (121, 124),
    ]
    data = [candle(o, c, 1.2, 1.2) for o, c in seq]
    n = len(data)
    ch.panel(70, 64, 540, 300, 94, 128)
    ch.grid(n, [100, 110, 120])
    ch.candles(data)
    entry, stop, target = 103, 99, 121
    # зоны риска/прибыли
    ye, ys, yt = ch.Y(entry), ch.Y(stop), ch.Y(target)
    ch.add(f'<rect x="70" y="{ye:.1f}" width="540" height="{ys-ye:.1f}" fill="#fee2e2" opacity="0.7"/>')
    ch.add(f'<rect x="70" y="{yt:.1f}" width="540" height="{ye-yt:.1f}" fill="#dcfce7" opacity="0.6"/>')
    ch.hline(entry, "#2563eb", "ВХОД 103", width=2)
    ch.hline(stop, DND, "СТОП 99", dash="5 3")
    ch.hline(target, UPD, "ТЕЙК 121", dash="5 3")
    # подписи зон справа
    ch.text(618, (ye+ys)/2 + 4, "риск", 12, DND, weight="700")
    ch.text(618, (ye+ys)/2 + 20, "−4", 11, DND)
    ch.text(618, (yt+ye)/2 + 4, "прибыль", 12, UPD, weight="700")
    ch.text(618, (yt+ye)/2 + 20, "+18", 11, UPD)
    # стрелка к точке входа
    xi = ch.X(5, n)
    ch.add(f'<path d="M{xi:.1f},{ch.Y(101)+30:.1f} L{xi:.1f},{ch.Y(101)+8:.1f}" stroke="{GOLD}" stroke-width="2" marker-end="url(#ar)"/>')
    ch.text(xi, ch.Y(101) + 46, "сигнал: молот у поддержки", 10.5, GOLD, "middle", "700")
    ch.add(f'<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{GOLD}"/></marker></defs>')
    ch.text(380, 410, "R:R = риск 4 к прибыли 18 ≈ 1:4.5. Даже при 40% удачных сделок такой R:R оставляет в плюсе.",
            11.5, SUB, "middle", style="italic")
    ch.text(380, 428, "⚠️ Учебный пример. Стоп ставится ДО входа и не двигается против себя.",
            11, "#b91c1c", "middle", "700")
    save("trade-example-real.svg", ch)


if __name__ == "__main__":
    chart_reading()
    chart_trendline()
    chart_candle_patterns()
    chart_moving_averages()
    chart_oscillators()
    chart_trade()
    print("done")
