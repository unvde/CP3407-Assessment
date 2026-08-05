# Reading Compass Figma Prototype Builder

This development plugin creates the current Reading Compass visual system directly inside an editable Figma Design file. It does not make network requests and does not use Figma MCP calls.

## What it creates

- Primitive, semantic and layout variables with CSS names
- Text styles and elevation styles
- A visual foundations page
- Reusable Button, Tag, Reading Status, Site Header and Book Card components
- Desktop Explore, Dashboard and Community Book screens built from component instances

The generator owns only pages whose names begin with `RC •`. Running it again refreshes those generated pages while leaving all other pages untouched.

## Run it in Figma

1. Open the Reading Compass Figma file. If the file is view-only, use **File → Duplicate to your drafts** and open the editable copy.
2. Open **Plugins → Development → Import plugin from manifest…**.
3. Choose `design/figma-plugin/manifest.json` from this repository.
4. Run **Plugins → Development → Reading Compass Prototype Builder**.
5. Wait for the completion message showing the page, component, variable and instance counts.

Expected generated pages:

- `RC • Foundations`
- `RC • Components`
- `RC • Explore`
- `RC • Dashboard`
- `RC • Community Book`

The plugin is repeatable: rerun it whenever the production visual system changes.
