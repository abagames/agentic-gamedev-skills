# Prompt Patterns

Use built-in `image_gen` by default. Substitute an equivalent generator only when the host does not
provide it.

## Opaque Object on Chroma Key

```text
Use case: stylized-concept
Asset type: transparent pixel-art source image for a game object
Primary request: Create one <subject>.
Subject: <single object only>, readable silhouette, clean edges.
Style: <project style>, pixel-art friendly source image, simplified forms, broad color areas, low detail clustering.
Composition: centered isolated object, generous padding, no cropped important edges.
Background: perfectly flat solid <key-color> chroma-key background. The background must be one uniform color with no floor plane, no shadow, no gradient, no texture, and no lighting variation. Do not use <key-color> anywhere in the subject.
Color/detail constraints: compatible with reduction to <N> colors and final size <WxH>.
Avoid: photorealism, text, logos, watermark, extra props, background clutter, contact shadow, cast shadow, reflection, UI, frame, border.
```

## Green Subject

Use `#00ff00` by default. Use `#ff00ff` instead for plants, slime, grass, leaves, green bottles, green clothing, or any subject that needs green pixels.
