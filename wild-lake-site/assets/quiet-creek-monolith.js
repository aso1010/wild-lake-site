/* The letters start off screen on every side, each at its own angle, and fly straight in, turning as they come.
   They meet in the middle and collide: they knock each other back and spin off. Then every letter snaps to its
   place in the block, like a magnet, and the block stands still and straight. The whole run is worked out before
   it plays, at 240 steps a second, and each frame is drawn by the page itself so the edges stay hard in motion.
   Tap to run it again. No motion if the system asks for less. */
(function () {
  var root = document.documentElement, svg = document.querySelector('.quiet-creek-monolith svg');
  if (!svg || !window.requestAnimationFrame || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    
    return;
  }

  var DT = 1 / 240, ARRIVE = .95, SNAP = 1.45, END = 2.5;     /* seconds */
  var E = .88, DRAG = 1.6, SPIN_DRAG = 1.4, KICK = .45;     /* restitution, damping after first contact, spin from glancing blows */
  var W0 = 2 * Math.PI * 3.4, Z = .6;                         /* the snap: a spring at 3.4 Hz, damping ratio 0.6 */
  var D2R = Math.PI / 180;

  var L = Array.prototype.map.call(svg.querySelectorAll('use'), function (u) {
    var d = u.dataset;
    return { u: u, tx: +d.x, ty: +d.y, s: +d.s, r: d.r * .8, d: +d.d, m: d.r * d.r };
  });
  var n = L.length, track = null, start = null, playing = false;

  function rnd(a, b) { return a + Math.random() * (b - a); }
  function draw(l, x, y, a) {
    l.u.setAttribute('transform', 'translate(' + x.toFixed(2) + ' ' + y.toFixed(2) + ') rotate(' + a.toFixed(2) + ') scale(' + l.s + ')');
  }
  function rest() { L.forEach(function (l) { draw(l, l.tx, l.ty, 0); }); }

  function simulate() {
    var vb = svg.viewBox.baseVal, box = svg.getBoundingClientRect(), k = vb.width / (box.width || 1);
    var vw = document.documentElement.clientWidth, vh = document.documentElement.clientHeight;
    var x0 = (0 - box.left) * k, x1 = (vw - box.left) * k, y0 = (0 - box.top) * k, y1 = (vh - box.top) * k;
    var cx = vb.width / 2, cy = vb.height / 2;

    /* every side: the directions are spread evenly round the circle and dealt out at random */
    var deal = L.map(function (_, i) { return i; });
    for (var i = n - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = deal[i]; deal[i] = deal[j]; deal[j] = t; }
    var turn = Math.random() * 2 * Math.PI;

    var B = L.map(function (l, i) {
      var a = turn + deal[i] / n * 2 * Math.PI + rnd(-.1, .1), dx = Math.cos(a), dy = Math.sin(a);
      var ex = dx > 0 ? (x1 - cx) / dx : dx < 0 ? (x0 - cx) / dx : Infinity;
      var ey = dy > 0 ? (y1 - cy) / dy : dy < 0 ? (y0 - cy) / dy : Infinity;
      var far = Math.min(ex, ey) + l.d + rnd(13, 144);
      var x = cx + dx * far, y = cy + dy * far;
      var pa = rnd(0, 2 * Math.PI), pr = Math.sqrt(Math.random()) * vb.width * .08;
      var px = cx + Math.cos(pa) * pr, py = cy + Math.sin(pa) * pr * .6, T = ARRIVE + rnd(-.06, .06);
      var spin = rnd(90, 300) * (Math.random() < .5 ? -1 : 1);
      return { l: l, x: x, y: y, vx: (px - x) / T, vy: (py - y) / T, a: rnd(-180, 180), va: spin, hit: false,
               snap: SNAP + i * .009, ta: 0 };
    });

    var steps = Math.ceil(END / DT), out = new Float32Array((steps + 1) * n * 3);
    for (var s = 0; s <= steps; s++) {
      var now = s * DT;
      /* contact: circles push apart, trade momentum, and a glancing blow sets them spinning */
      for (var p = 0; p < n; p++) {
        var A = B[p];
        if (now >= A.snap) continue;
        for (var q = p + 1; q < n; q++) {
          var C = B[q];
          if (now >= C.snap) continue;
          var dx = C.x - A.x, dy = C.y - A.y, R = A.l.r + C.l.r, d2 = dx * dx + dy * dy;
          if (d2 >= R * R || d2 === 0) continue;
          var d = Math.sqrt(d2), nx = dx / d, ny = dy / d, ia = 1 / A.l.m, ic = 1 / C.l.m;
          var push = (R - d) / (ia + ic) * .5;
          A.x -= nx * push * ia; A.y -= ny * push * ia; C.x += nx * push * ic; C.y += ny * push * ic;
          var rvx = C.vx - A.vx, rvy = C.vy - A.vy, vn = rvx * nx + rvy * ny;
          if (vn < 0) {
            var jn = -(1 + E) * vn / (ia + ic);
            A.vx -= jn * nx * ia; A.vy -= jn * ny * ia; C.vx += jn * nx * ic; C.vy += jn * ny * ic;
            var vt = -rvx * ny + rvy * nx;
            A.va += KICK * vt / A.l.r / D2R * (C.l.m / (A.l.m + C.l.m));
            C.va -= KICK * vt / C.l.r / D2R * (A.l.m / (A.l.m + C.l.m));
            A.hit = C.hit = true;
          }
        }
      }
      for (var b = 0; b < n; b++) {
        var o = B[b], l = o.l;
        if (now >= o.snap) {
          /* the snap: pulled to its place and upright, carrying the speed it had */
          if (!o.locked) { o.locked = true; o.ta = Math.round(o.a / 360) * 360; }
          o.vx += (-W0 * W0 * (o.x - l.tx) - 2 * Z * W0 * o.vx) * DT;
          o.vy += (-W0 * W0 * (o.y - l.ty) - 2 * Z * W0 * o.vy) * DT;
          o.va += (-W0 * W0 * (o.a - o.ta) - 2 * Z * W0 * o.va) * DT;
        } else if (o.hit) {
          var f = Math.exp(-DRAG * DT);
          o.vx *= f; o.vy *= f; o.va *= Math.exp(-SPIN_DRAG * DT);
        }
        o.va = Math.max(-900, Math.min(900, o.va));
        o.x += o.vx * DT; o.y += o.vy * DT; o.a += o.va * DT;
        var at = (s * n + b) * 3;
        out[at] = o.x; out[at + 1] = o.y; out[at + 2] = o.a;
      }
    }
    return { steps: steps, pos: out };
  }

  function frame(now) {
    if (start === null) start = now;
    var f = (now - start) / 1000 / DT;
    if (f >= track.steps) { rest(); playing = false; return; }
    var s = Math.floor(f), u = f - s, P = track.pos;
    for (var b = 0; b < n; b++) {
      var i = (s * n + b) * 3, j = ((s + 1) * n + b) * 3;
      draw(L[b], P[i] + (P[j] - P[i]) * u, P[i + 1] + (P[j + 1] - P[i + 1]) * u, P[i + 2] + (P[j + 2] - P[i + 2]) * u);
    }
    requestAnimationFrame(frame);
  }

  function play() {
    if (playing) return;
    playing = true; start = null; track = simulate();
    var P = track.pos;
    L.forEach(function (l, b) { draw(l, P[b * 3], P[b * 3 + 1], P[b * 3 + 2]); });
    requestAnimationFrame(frame);
  }

  play();
  
  document.querySelector('.qc-replay').addEventListener('click', play);
})();
