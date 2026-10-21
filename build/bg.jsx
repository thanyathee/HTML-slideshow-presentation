// Animated gradient background: ShaderGradient (which runs on react-three-fiber / three.js).
// Exposes window.DeckBG so the slideshow can change the mood per slide.
import React, { useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { ShaderGradientCanvas, ShaderGradient } from '@shadergradient/react'

const MOODS = {
  cover: ['#FFFFFF', '#CFF0FE', '#F2FBFF'],
  blue: ['#F3FBFF', '#B9E7FB', '#FFFFFF'],
  navy: ['#EAF8FF', '#A9E2FA', '#FAFDFF'],
  warm: ['#FFF8EC', '#BDE8FB', '#FFFFFF'],
  red: ['#FFF1F3', '#BFE6FB', '#FFFFFF'],
  green: ['#EDFCF6', '#B3EAF6', '#FFFFFF']
}

const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16))
const toHex = a => '#' + a.map(v => Math.round(v).toString(16).padStart(2, '0')).join('')
const mix = (a, b, t) => toHex(hex(a).map((v, i) => v + (hex(b)[i] - v) * t))

let setColors = null
let current = MOODS.cover
let raf = 0

function App({ lite }) {
  const [colors, set] = useState(current)
  useEffect(() => {
    setColors = set
    return () => { setColors = null }
  }, [])
  return (
    <ShaderGradientCanvas
      lazyLoad={false}
      pixelDensity={lite ? 0.6 : 1}
      fov={45}
      preserveDrawingBuffer
      style={{ position: 'absolute', inset: 0 }}
    >
      <ShaderGradient
        control="props"
        type="plane"
        animate="on"
        uSpeed={0.05}
        uStrength={3.4}
        uDensity={1.3}
        uFrequency={5.5}
        color1={colors[0]}
        color2={colors[1]}
        color3={colors[2]}
        lightType="3d"
        brightness={1.25}
        reflection={0.1}
        grain="off"
        cAzimuthAngle={180}
        cPolarAngle={80}
        cDistance={3.6}
        cameraZoom={9.1}
        positionX={-1.4}
        positionY={0}
        positionZ={0}
        rotationX={0}
        rotationY={10}
        rotationZ={50}
      />
    </ShaderGradientCanvas>
  )
}

function webglOk() {
  try {
    const c = document.createElement('canvas')
    return !!(c.getContext('webgl2') || c.getContext('webgl'))
  } catch (e) { return false }
}

window.DeckBG = {
  ok: false,
  mount(el, opts = {}) {
    if (!webglOk()) return false
    try {
      createRoot(el).render(<App lite={!!opts.lite} />)
      this.ok = true
    } catch (e) { return false }
    return true
  },
  setMood(name, instant) {
    const to = MOODS[name] || MOODS.blue
    const from = current
    cancelAnimationFrame(raf)
    if (instant) { current = to; if (setColors) setColors(to); return }
    const t0 = performance.now(), D = 1100
    let last = 0
    const step = now => {
      const p = Math.min(1, (now - t0) / D)
      const e = p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2
      if (now - last > 33 || p === 1) {
        last = now
        current = from.map((c, i) => mix(c, to[i], e))
        if (setColors) setColors(current)
      }
      if (p < 1) raf = requestAnimationFrame(step)
    }
    raf = requestAnimationFrame(step)
  }
}
