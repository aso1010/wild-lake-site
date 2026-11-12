/* Native, opt-in renderer for Paper Shaders' Apache-2.0 Water GLSL.
 * No React, packages, network services, or external runtime assets.
 * Preview: /?water=1. The original SVG remains the accessible fallback. */
(async function () {
  if (new URLSearchParams(location.search).get('water') !== '1') return;
  const host = document.querySelector('.home .cap .mark');
  const lines = host && host.querySelector('.mark-a');
  if (!host || !lines) return;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  if (motion.matches) return;
  const canvas = document.createElement('canvas');
  canvas.className = 'monolith-water-canvas';
  canvas.setAttribute('aria-hidden', 'true');
  const gl = canvas.getContext('webgl2', { alpha: true, antialias: false, powerPreference: 'low-power' });
  if (!gl) return;
  const waterSpeed = 1 / 8; // Fibonacci divisor: eight times slower than the original.
  let frame = 0, elapsed = 0, last = 0, paused = false, visible = true, ready = false, revision = 0;
  let program, texture, observer, resizeObserver;
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'monolith-water-toggle';
  button.textContent = 'Pause water';
  button.setAttribute('aria-pressed', 'false');
  function fallback() {
    ready = false;
    cancelAnimationFrame(frame);
    host.classList.remove('has-water');
    if (observer) observer.disconnect();
    if (resizeObserver) resizeObserver.disconnect();
    canvas.remove();
    button.remove();
    if (texture) gl.deleteTexture(texture);
    if (program) gl.deleteProgram(program);
  }
  try {
    const sources = await import('./monolith-water-source.js');
    function compile(type, source) {
      const shader = gl.createShader(type);
      gl.shaderSource(shader, source);
      gl.compileShader(shader);
      if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(shader));
      return shader;
    }
    const vertex = compile(gl.VERTEX_SHADER, sources.vertex);
    const fragment = compile(gl.FRAGMENT_SHADER, sources.fragment);
    program = gl.createProgram();
    gl.attachShader(program, vertex); gl.attachShader(program, fragment); gl.linkProgram(program);
    gl.deleteShader(vertex); gl.deleteShader(fragment);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(program));
    gl.useProgram(program);
    const buffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, -1,1, 1,-1, 1,1]), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
    const location = name => gl.getUniformLocation(program, name);
    const uniforms = {};
    ['u_time','u_resolution','u_pixelRatio','u_imageAspectRatio'].forEach(name => { uniforms[name] = location(name); });
    const settings = { u_size:1, u_highlights:.07, u_layering:.5, u_edges:.8, u_waves:.3, u_caustic:.1,
      u_fit:1, u_scale:1, u_originX:.5, u_originY:.5, u_rotation:0, u_offsetX:0, u_offsetY:0,
      u_worldWidth:0, u_worldHeight:0 };
    Object.keys(settings).forEach(name => gl.uniform1f(location(name), settings[name]));
    gl.uniform4f(location('u_colorBack'), 0, 0, 0, 0);
    gl.uniform4f(location('u_colorHighlight'), 1, 1, 1, 1);
    texture = gl.createTexture();
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.uniform1i(location('u_image'), 0);
    host.append(canvas, button);
    function draw() {
      gl.uniform1f(uniforms.u_time, elapsed / 1000);
      gl.drawArrays(gl.TRIANGLES, 0, 6);
    }
    function tick(now) {
      frame = 0;
      if (!ready || paused || !visible || document.hidden || motion.matches) { last = 0; return; }
      if (!last) last = now;
      if (now - last >= 1000/30) {
        elapsed += Math.min(now - last, 100) * waterSpeed;
        last = now;
        draw();
      }
      frame = requestAnimationFrame(tick);
    }
    function resume() {
      if (!frame && ready && !paused && visible && !document.hidden && !motion.matches) frame = requestAnimationFrame(tick);
    }
    async function resize() {
      const current = ++revision;
      const box = lines.getBoundingClientRect();
      if (box.width < 1 || box.height < 1) return;
      const ratio = Math.min(devicePixelRatio || 1, 1.5, Math.sqrt(1800000 / (box.width * box.height)));
      const width = Math.max(1, Math.round(box.width * ratio)), height = Math.max(1, Math.round(box.height * ratio));
      const svgNS = 'http://www.w3.org/2000/svg';
      const svg = document.createElementNS(svgNS, 'svg');
      svg.setAttribute('width', width); svg.setAttribute('height', height);
      svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
      svg.setAttribute('fill', '#ffffff');
      lines.querySelectorAll(':scope > svg').forEach(line => {
        const rect = line.getBoundingClientRect(), clone = line.cloneNode(true);
        clone.setAttribute('x', (rect.left - box.left) * ratio); clone.setAttribute('y', (rect.top - box.top) * ratio);
        clone.setAttribute('width', rect.width * ratio); clone.setAttribute('height', rect.height * ratio);
        clone.setAttribute('fill', '#ffffff');
        clone.querySelectorAll('[transform]').forEach(n => n.removeAttribute('transform'));
        svg.append(clone);
      });
      const url = URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(svg)], { type:'image/svg+xml' }));
      const image = new Image();
      try {
        image.src = url; await image.decode();
        if (current !== revision || !canvas.isConnected) return;
        canvas.width = width; canvas.height = height;
        gl.viewport(0, 0, width, height);
        gl.uniform2f(uniforms.u_resolution, width, height); gl.uniform1f(uniforms.u_pixelRatio, ratio);
        gl.uniform1f(uniforms.u_imageAspectRatio, width / height);
        gl.bindTexture(gl.TEXTURE_2D, texture);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
        ready = true; draw(); host.classList.add('has-water'); resume();
      } finally { URL.revokeObjectURL(url); }
    }
    button.addEventListener('click', () => {
      paused = !paused; button.textContent = paused ? 'Play water' : 'Pause water';
      button.setAttribute('aria-pressed', String(paused));
      if (paused) { cancelAnimationFrame(frame); frame = 0; last = 0; } else resume();
    });
    document.addEventListener('visibilitychange', () => { last = 0; resume(); });
    motion.addEventListener('change', () => { host.classList.toggle('has-water', !motion.matches && ready); last = 0; resume(); });
    canvas.addEventListener('webglcontextlost', event => { event.preventDefault(); fallback(); });
    observer = new IntersectionObserver(entries => { visible = entries[0].isIntersecting; last = 0; resume(); });
    observer.observe(host);
    resizeObserver = new ResizeObserver(() => { resize().catch(fallback); });
    resizeObserver.observe(lines);
    await resize();
  } catch (error) {
    console.warn('Water preview unavailable; retaining the SVG monolith.', error);
    fallback();
  }
})();
