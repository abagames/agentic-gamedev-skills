# Prompt Patterns

## Opaque Object On Chroma Key

```text
Use case: stylized-concept
Asset type: transparent pixel-art source image for a game object
Primary request: Create one <subject>.
Subject: <single object only>, readable silhouette, clean edges.
Style: handcrafted miniature, pixel-art friendly source image, simplified forms, broad color areas, low detail clustering.
Composition: centered isolated object, generous padding, no cropped important edges.
Background: perfectly flat solid #00ff00 chroma-key background. The background must be one uniform color with no floor plane, no shadow, no gradient, no texture, and no lighting variation. Do not use #00ff00 anywhere in the subject.
Color/detail constraints: compatible with reduction to 16 to 32 colors and final size <WxH>.
Avoid: photorealism, text, logos, watermark, extra props, background clutter, contact shadow, cast shadow, reflection, UI, frame, border.
```

## Green Subject

Use `#ff00ff` instead of `#00ff00` for plants, slime, grass, leaves, green bottles, or green clothing.
