package main

// The Quiet Creek deck: 78 original cards drawn as solid geometry.
// Every card lives in a 233 x 377 box (phi). Ink is currentColor and the ground is the
// card itself, so nothing is ever painted black and any card inverts cleanly.
// Names only. The deck carries no meanings: the querent reads the image.

import (
	"fmt"
	"math"
	"strconv"
	"strings"
)

const (
	vw, vh = 233.0, 377.0
	cx     = 116.5
	top    = 21.0
	ground = 310.0 // the name strip sits below this line
	left   = 21.0
	right  = 212.0
	cy     = (top + ground) / 2
	span   = right - left
)

type card struct {
	ID, Name string
	Art      string
}

func n(v float64) string { return strconv.FormatFloat(math.Round(v*100)/100, 'f', -1, 64) }

type art struct{ b strings.Builder }

func (a *art) fill(ds ...string) {
	for _, d := range ds {
		fmt.Fprintf(&a.b, `<path d="%s"/>`, d)
	}
}

func (a *art) trace(sw float64, ds ...string) {
	for _, d := range ds {
		fmt.Fprintf(&a.b, `<path d="%s" fill="none" stroke="currentColor" stroke-width="%s"/>`, d, n(sw))
	}
}

func (a *art) ring(x, y, r, sw float64) {
	fmt.Fprintf(&a.b, `<circle cx="%s" cy="%s" r="%s" fill="none" stroke="currentColor" stroke-width="%s"/>`, n(x), n(y), n(r), n(sw))
}

func (a *art) raw(s string) { a.b.WriteString(s) }

// path data

func dRect(x, y, w, h float64) string {
	return fmt.Sprintf("M%s %sh%sv%sh%sZ", n(x), n(y), n(w), n(h), n(-w))
}

func dDisc(x, y, r float64) string {
	return fmt.Sprintf("M%s %sa%s %s 0 1 1 %s 0a%s %s 0 1 1 %s 0Z", n(x-r), n(y), n(r), n(r), n(2*r), n(r), n(r), n(-2*r))
}

func dPoly(pts ...float64) string {
	var b strings.Builder
	for i := 0; i+1 < len(pts); i += 2 {
		if i == 0 {
			b.WriteString("M")
		} else {
			b.WriteString("L")
		}
		b.WriteString(n(pts[i]) + " " + n(pts[i+1]))
	}
	b.WriteString("Z")
	return b.String()
}

func dLine(pts ...float64) string { return strings.TrimSuffix(dPoly(pts...), "Z") }

// a sine meander laid along the segment (x1,y1)-(x2,y2)
func dWave(x1, y1, x2, y2, amp, waves float64) string {
	dx, dy := x2-x1, y2-y1
	l := math.Hypot(dx, dy)
	px, py := -dy/l, dx/l
	pts := make([]float64, 0, 130)
	for i := 0; i <= 64; i++ {
		t := float64(i) / 64
		o := amp * math.Sin(2*math.Pi*waves*t)
		pts = append(pts, x1+dx*t+px*o, y1+dy*t+py*o)
	}
	return dLine(pts...)
}

// two arcs through the same chord: outer radius r, inner radius r2 (> r)
func dCrescent(x, y, r, r2 float64) string {
	return fmt.Sprintf("M%s %sA%s %s 0 0 0 %s %sA%s %s 0 0 1 %s %sZ",
		n(x), n(y-r), n(r), n(r), n(x), n(y+r), n(r2), n(r2), n(x), n(y-r))
}

func dDiamond(x, y, r float64) string { return dPoly(x, y-r, x+r, y, x, y+r, x-r, y) }

// suit glyphs, centred on (x,y), h tall

func dCup(x, y, h float64) []string {
	r := h / 1.5
	t := y - h/2
	bowl := fmt.Sprintf("M%s %sH%sA%s %s 0 0 1 %s %sZ", n(x-r), n(t), n(x+r), n(r), n(r), n(x-r), n(t))
	return []string{bowl, dRect(x-r*0.09, t+r-1, r*0.18, r*0.35+2), dRect(x-r*0.45, t+r*1.35, r*0.9, r*0.15)}
}

func dBlade(tx, ty, px, py, w float64) []string {
	l := math.Hypot(tx-px, ty-py)
	ux, uy := (tx-px)/l, (ty-py)/l
	nx, ny := -uy, ux
	at := func(s, o float64) (float64, float64) { return px + ux*s + nx*o, py + uy*s + ny*o }
	hilt := l * 0.17
	g := w * 0.28
	gx1, gy1 := at(0, g)
	gx2, gy2 := at(hilt, g)
	gx3, gy3 := at(hilt, -g)
	gx4, gy4 := at(0, -g)
	c := w * 1.7
	q := w * 0.35
	cx1, cy1 := at(hilt-q, c)
	cx2, cy2 := at(hilt+q, c)
	cx3, cy3 := at(hilt+q, -c)
	cx4, cy4 := at(hilt-q, -c)
	b := w / 2
	bx1, by1 := at(hilt+q, b)
	bx2, by2 := at(hilt+q+(l-hilt-q)*0.84, b)
	bx3, by3 := at(l, 0)
	bx4, by4 := at(hilt+q+(l-hilt-q)*0.84, -b)
	bx5, by5 := at(hilt+q, -b)
	return []string{
		dPoly(gx1, gy1, gx2, gy2, gx3, gy3, gx4, gy4),
		dPoly(cx1, cy1, cx2, cy2, cx3, cy3, cx4, cy4),
		dPoly(bx1, by1, bx2, by2, bx3, by3, bx4, by4, bx5, by5),
		dDisc(px, py, w*0.55),
	}
}

type suit int

const (
	wands suit = iota
	cups
	swords
	pentacles
)

var suitName = [...]string{"Wands", "Cups", "Swords", "Pentacles"}
var suitID = [...]string{"w", "c", "s", "p"}
var rankName = [...]string{"", "Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Page", "Knight", "Queen", "King"}

func glyph(s suit, x, y, h float64) []string {
	switch s {
	case wands:
		w := math.Max(5, h*0.16)
		return []string{dRect(x-w/2, y-h/2, w, h)}
	case cups:
		return dCup(x, y, h)
	case swords:
		return dBlade(x, y-h/2, x, y+h/2, math.Max(4.5, h*0.075))
	}
	return []string{dDisc(x, y, h/2)}
}

func lemniscate(a *art, y float64) {
	a.ring(cx-17, y, 17, 3)
	a.ring(cx+17, y, 17, 3)
}

// major arcana

func majors() []card {
	type m struct {
		name string
		draw func(a *art)
	}
	list := []m{
		{"The Fool", func(a *art) {
			a.fill(dRect(left, 241, 110, ground-241))
			a.fill(dDisc(120, 230, 11))
			a.ring(170, 76, 21, 3)
		}},
		{"The Magician", func(a *art) {
			lemniscate(a, 51)
			a.fill(dRect(cx-4, 76, 8, 165), dRect(34, 241, 165, 13), dRect(44, 254, 8, ground-254), dRect(181, 254, 8, ground-254))
			a.fill(dDisc(52, 232, 9), dRect(72, 213, 6, 28))
			a.fill(dCup(160, 230.5, 21)...)
			a.fill(dBlade(186, 207, 186, 241, 4)...)
		}},
		{"The High Priestess", func(a *art) {
			a.fill(dRect(34, 34, 34, 276))
			a.trace(3, dRect(166.5, 35.5, 31, 273))
			for x := 84.0; x <= 149; x += 13 {
				a.trace(1.5, dLine(x, 55, x, 200))
			}
			a.fill(dCrescent(cx, 252, 26, 34))
		}},
		{"The Empress", func(a *art) {
			a.fill(dDisc(cx, 130, 34))
			a.ring(cx, 130, 55, 3)
			a.ring(cx, 130, 76, 3)
			a.ring(cx, 130, 95, 1.5)
			for _, y := range []float64{252, 270, 288} {
				for x := 34.0; x <= 200; x += 15 {
					a.fill(dRect(x-1.25, y, 2.5, 13))
				}
			}
		}},
		{"The Emperor", func(a *art) {
			a.fill(dRect(44.5, 98, 144, 8), dRect(44.5, 119, 144, 144), dRect(left, 276, span, ground-276))
		}},
		{"The Hierophant", func(a *art) {
			a.trace(8, "M47 310V140A69.5 69.5 0 0 1 186 140V310")
			a.fill(dRect(cx-2.5, 110, 5, ground-110), dRect(cx-13, 128, 26, 5), dRect(cx-21, 148, 42, 5), dRect(cx-29, 168, 58, 5))
		}},
		{"The Lovers", func(a *art) {
			a.ring(89, 150, 55, 3)
			a.ring(144, 150, 55, 3)
			h := math.Sqrt(55*55 - 27.5*27.5)
			a.fill(fmt.Sprintf("M%s %sA55 55 0 0 1 %s %sA55 55 0 0 1 %s %sZ", n(cx), n(150-h), n(cx), n(150+h), n(cx), n(150-h)))
			a.fill(dDisc(89, 228, 8), dDisc(144, 228, 8), dRect(86, 241, 6, ground-241), dRect(141, 241, 6, ground-241))
		}},
		{"The Chariot", func(a *art) {
			a.fill(dRect(55, 96, 123, 8), dRect(60, 104, 4, 49), dRect(169, 104, 4, 49), dRect(55, 153, 123, 89))
			a.ring(81, 268, 26, 8)
			a.ring(152, 268, 26, 8)
			a.fill(dDisc(81, 268, 5), dDisc(152, 268, 5))
			a.fill(dRect(left, 172, 21, 2), dRect(left, 192, 29, 2), dRect(left, 212, 21, 2))
		}},
		{"Strength", func(a *art) {
			lemniscate(a, 62)
			a.fill("M44 238A72.5 72.5 0 0 1 189 238Z")
			pts := []float64{}
			for i := 0; i <= 8; i++ {
				y := 250.0
				if i%2 == 1 {
					y = 271
				}
				pts = append(pts, 44+float64(i)*145/8, y)
			}
			a.trace(3, dLine(pts...))
		}},
		{"The Hermit", func(a *art) {
			a.fill(dPoly(left, ground, right, ground, right, 190))
			sy := ground - (100-left)*(120/span)
			a.trace(4, dLine(100, 120, 100, sy))
			a.trace(3, dLine(98, 122, 120, 122))
			a.trace(1.5, dLine(118, 122, 118, 132))
			a.fill(dRect(111, 132, 14, 18))
			for _, deg := range []float64{-45, 0, 45, 90} {
				r := deg * math.Pi / 180
				a.trace(1.5, dLine(118+math.Cos(r)*17, 141+math.Sin(r)*17, 118+math.Cos(r)*30, 141+math.Sin(r)*30))
			}
		}},
		{"Wheel of Fortune", func(a *art) {
			a.raw(`<g class="spin">`)
			a.ring(cx, cy, 89, 8)
			a.ring(cx, cy, 55, 3)
			for k := 0; k < 8; k++ {
				r := float64(k) * math.Pi / 4
				a.trace(3, dLine(cx+math.Cos(r)*13, cy+math.Sin(r)*13, cx+math.Cos(r)*85, cy+math.Sin(r)*85))
			}
			a.fill(dDisc(cx, cy, 13))
			for k := 0; k < 4; k++ {
				r := float64(k)*math.Pi/2 + math.Pi/4
				a.fill(dDiamond(cx+math.Cos(r)*72, cy+math.Sin(r)*72, 6))
			}
			a.raw(`</g>`)
		}},
		{"Justice", func(a *art) {
			a.fill(dBlade(cx, 34, cx, 300, 10)...)
			a.fill(dRect(40, 120, 153, 5))
			a.trace(1.5, dLine(48, 125, 48, 185), dLine(185, 125, 185, 185))
			a.fill(dRect(31, 185, 34, 6), dRect(168, 185, 34, 6))
		}},
		{"The Hanged Man", func(a *art) {
			a.fill(dRect(34, 34, 165, 13))
			a.trace(3, dLine(cx, 47, cx, 110))
			a.fill(dPoly(cx-34, 110, cx+34, 110, cx, 236), dDisc(cx, 257, 17))
		}},
		{"Death", func(a *art) {
			a.fill(dPoly(left, top, right, top, right, 130, left, 206))
			a.fill(dPoly(left, 227, right, 151, right, ground, left, ground))
		}},
		{"Temperance", func(a *art) {
			a.fill(dCup(70, 95, 55)...)
			a.fill(dCup(163, 245, 55)...)
			a.trace(4, dWave(96, 82, 150, 214, 13, 2))
			a.trace(3, dWave(left, 300, right, 300, 4, 4))
		}},
		{"The Devil", func(a *art) {
			a.fill(dPoly(66, 40, 167, 40, cx, 100), dRect(60, 112, 113, 89))
			a.raw(`<path d="` + dLine(75, 201, 75, 262) + `M158 201L158 262" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="5 3"/>`)
			a.fill(dDisc(75, 275, 13), dDisc(158, 275, 13))
		}},
		{"The Tower", func(a *art) {
			off := []float64{4, -13, 11, -9, 13, -11, 8, -6, 3}
			var lp, rp []float64
			lp = append(lp, 78, 34)
			for k, o := range off {
				y := 34 + float64(k)*(ground-34)/8
				lp = append(lp, cx+o-3.5, y)
			}
			lp = append(lp, 78, ground)
			rp = append(rp, 155, 34, 155, ground)
			for k := len(off) - 1; k >= 0; k-- {
				y := 34 + float64(k)*(ground-34)/8
				rp = append(rp, cx+off[k]+3.5, y)
			}
			a.fill(dPoly(lp...), dPoly(rp...))
			for _, f := range [][3]float64{{52, 70, 7}, {40, 118, 5}, {60, 160, 4}, {184, 58, 6}, {196, 104, 7}, {176, 150, 4}} {
				a.fill(dDiamond(f[0], f[1], f[2]))
			}
		}},
		{"The Star", func(a *art) {
			d := 68 / math.Sqrt2
			a.fill(dRect(cx-34, 86, 68, 68), dDiamond(cx, 120, d))
			for _, s := range [][3]float64{{40, 50, 6}, {190, 60, 7}, {36, 170, 5}, {196, 180, 6}, {60, 230, 7}, {175, 240, 5}, {cx, 210, 8}} {
				a.fill(dDiamond(s[0], s[1], s[2]))
			}
			a.trace(3, dWave(left, 285, right, 285, 5, 4))
			a.trace(1.5, dWave(left, 300, right, 300, 3, 5))
		}},
		{"The Moon", func(a *art) {
			a.fill(dCrescent(cx, 75, 34, 44))
			a.fill(dRect(34, 175, 21, 110), dRect(178, 175, 21, 110))
			a.trace(3, dLine(86, ground, cx, 190), dLine(147, ground, cx, 190))
			a.trace(3, dWave(left, 298, right, 298, 4, 4))
		}},
		{"The Sun", func(a *art) {
			a.fill(dDisc(cx, 130, 47))
			for k := 0; k < 21; k++ {
				r := float64(k)*2*math.Pi/21 - math.Pi/2
				l := 21.0
				if k%2 == 0 {
					l = 34
				}
				a.trace(3, dLine(cx+math.Cos(r)*58, 130+math.Sin(r)*58, cx+math.Cos(r)*(58+l), 130+math.Sin(r)*(58+l)))
			}
			a.fill(dRect(left, 262, span, 13), dRect(left, 279, span, 13), dRect(left, 296, span, 14))
		}},
		{"Judgement", func(a *art) {
			a.fill(dDisc(cx, 34, 13))
			a.trace(3, dLine(cx, 47, 58, 160), dLine(cx, 47, cx, 170), dLine(cx, 47, 175, 160))
			a.fill(dRect(52-6.5, 200, 13, 88), dRect(cx-6.5, 176, 13, 112), dRect(168-6.5, 200, 13, 88))
			a.fill(dRect(left, 288, span, 5), dRect(left, 300, span, 10))
		}},
		{"The World", func(a *art) {
			fmt.Fprintf(&a.b, `<ellipse cx="%s" cy="%s" rx="68" ry="110" fill="none" stroke="currentColor" stroke-width="8"/>`, n(cx), n(cy))
			a.fill(dDisc(cx, 125, 11), dRect(cx-4, 140, 8, 76))
			a.fill(dDisc(36, 36, 11), dDisc(197, 36, 11), dDisc(36, 295, 11), dDisc(197, 295, 11))
		}},
	}
	out := make([]card, len(list))
	for i, c := range list {
		a := &art{}
		c.draw(a)
		out[i] = card{ID: fmt.Sprintf("m%02d", i), Name: c.name, Art: a.b.String()}
	}
	return out
}

// minor arcana

var cupRows = map[int][]int{2: {2}, 3: {1, 2}, 4: {2, 2}, 5: {2, 1, 2}, 6: {3, 3}, 7: {2, 3, 2}, 8: {3, 2, 3}, 9: {3, 3, 3}, 10: {1, 2, 3, 4}}

func pips(a *art, s suit, k int) {
	switch s {
	case wands:
		pitch := span / float64(k)
		w := math.Min(21, pitch*0.55)
		hmax := ground - top - 21
		a.fill(dRect(left, ground-3, span, 3))
		for i := 0; i < k; i++ {
			x := left + pitch*(float64(i)+0.5)
			d := math.Abs(float64(i)-float64(k-1)/2) / (float64(k+1) / 2)
			h := hmax * (0.382 + 0.618*(1-d))
			a.fill(dRect(x-w/2, ground-3-h, w, h))
		}
	case pentacles:
		cols := 1
		if k > 3 {
			cols = 2
		}
		rows := (k + cols - 1) / cols
		cw, ch := span/float64(cols), (ground-top)/float64(rows)
		r := math.Min(cw, ch) / 2 * 0.78
		for i := 0; i < k; i++ {
			row, col := i/cols, i%cols
			in := cols
			if row == rows-1 && k%cols != 0 {
				in = k % cols
			}
			a.fill(dDisc(cx+(float64(col)-float64(in-1)/2)*cw, top+ch*(float64(row)+0.5), r))
		}
	case swords: // every blade driven tip-down into one point; the hilts fan out above, countable
		spread := math.Min(40, 8*float64(k-1)) * math.Pi / 180
		const l = 270.0
		tx, ty := cx, ground-3
		w := math.Max(4.5, 9-0.4*float64(k))
		for i := 0; i < k; i++ {
			t := -spread/2 + spread*float64(i)/float64(k-1)
			a.fill(dBlade(tx, ty, tx+math.Sin(t)*l, ty-math.Cos(t)*l, w)...)
		}
	case cups:
		rows := cupRows[k]
		most := 0
		for _, m := range rows {
			most = max(most, m)
		}
		pitch := span / float64(most)
		rh := (ground - top) / float64(len(rows))
		h := math.Min(pitch*0.82/1.333, rh*0.8)
		for j, m := range rows {
			for i := 0; i < m; i++ {
				a.fill(dCup(cx+(float64(i)-float64(m-1)/2)*pitch, top+rh*(float64(j)+0.5), h)...)
			}
		}
	}
}

func minor(s suit, rank int) string {
	a := &art{}
	switch rank {
	case 1:
		switch s {
		case wands:
			a.fill(dRect(cx-17, top, 34, ground-top))
		case cups:
			y := cy - 21
			a.fill(dCup(cx, y, 135)...)
			t := y - 135.0/2
			a.trace(3, dWave(cx-90, t, cx-90, ground, 4, 3), dWave(cx+90, t, cx+90, ground, 4, 3))
		case swords:
			a.fill(dBlade(cx, top, cx, ground, 13)...)
		case pentacles:
			a.fill(dDisc(cx, cy, 89))
		}
	case 11: // page: small, on the ground, void above
		a.fill(dRect(left, ground-3, span, 3))
		a.fill(glyph(s, cx, ground-3-44.5-8, 89)...)
	case 12: // knight: the glyph in motion, two traces and the lead
		a.trace(3, glyph(s, cx-48, cy+48, 89)...)
		a.trace(3, glyph(s, cx, cy, 89)...)
		a.fill(glyph(s, cx+48, cy-48, 89)...)
	case 13: // queen: held inside a ring
		a.ring(cx, cy, 89, 5)
		a.fill(glyph(s, cx, cy, 96)...)
	case 14: // king: raised on a plinth, crowned by a bar
		a.fill(dRect(cx-61.5, 232, 123, ground-232), dRect(cx-44.5, 51, 89, 8))
		a.fill(glyph(s, cx, 152, 144)...)
	default:
		pips(a, s, rank)
	}
	return a.b.String()
}

func deck() []card {
	out := majors()
	for s := wands; s <= pentacles; s++ {
		for r := 1; r <= 14; r++ {
			out = append(out, card{ID: fmt.Sprintf("%s%02d", suitID[s], r), Name: rankName[r] + " of " + suitName[s], Art: minor(s, r)})
		}
	}
	return out
}

// the card back is the Quiet Creek mark: a 2:3 standing stone split by two whole waves of creek
func back() string {
	const sw, sh = 144.0, 216.0
	amp, cw := 50*sw/460, 34*sw/460
	x0, y0 := cx-sw/2, vh/2-sh/2
	pts := []float64{}
	for i := 0; i <= 200; i++ {
		t := float64(i) / 200
		y := y0 - 13 + (sh+26)*t
		pts = append(pts, cx+amp*math.Sin(2*math.Pi*2*(y-y0)/sh), y)
	}
	return fmt.Sprintf(`<mask id="qc-cut" maskUnits="userSpaceOnUse" x="0" y="0" width="%s" height="%s"><rect width="%s" height="%s" fill="#fff"/><path d="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round"/></mask><rect x="%s" y="%s" width="%s" height="%s" mask="url(#qc-cut)"/>`,
		n(vw), n(vh), n(vw), n(vh), dLine(pts...), n(cw), n(x0), n(y0), n(sw), n(sh))
}

func sprite(cards []card) string {
	var b strings.Builder
	b.WriteString(`<svg class="sprite" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">`)
	sym := func(id, body string) {
		fmt.Fprintf(&b, "\n"+`<symbol id="%s" viewBox="0 0 %s %s" fill="currentColor">%s</symbol>`, id, n(vw), n(vh), body)
	}
	sym("back", back())
	for _, c := range cards {
		sym(c.ID, c.Art)
	}
	b.WriteString("\n</svg>")
	return b.String()
}
