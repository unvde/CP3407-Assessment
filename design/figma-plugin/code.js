const OWNER_KEY = "reading-compass-prototype-builder";
const PAGE_PREFIX = "RC • ";

const palette = {
  ink: "#18231c",
  muted: "#647066",
  paper: "#f2f0e7",
  surface: "#fffdf8",
  white: "#ffffff",
  line: "#d7dcd1",
  green: "#376b50",
  greenDark: "#173d2a",
  greenSoft: "#dfeadf",
  gold: "#b8833d",
  goldSoft: "#f3e7ce",
  danger: "#a2382d",
  blueSoft: "#dceef6",
  purpleSoft: "#ebe3f6",
  amberSoft: "#f6e9c8"
};

const spacingValues = [4, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64];
const radiusValues = [8, 10, 11, 14, 16, 18, 20, 26, 999];

function hexToRgba(hex) {
  const value = hex.replace("#", "");
  return {
    r: parseInt(value.slice(0, 2), 16) / 255,
    g: parseInt(value.slice(2, 4), 16) / 255,
    b: parseInt(value.slice(4, 6), 16) / 255,
    a: 1
  };
}

function rgb(hex) {
  const { r, g, b } = hexToRgba(hex);
  return { r, g, b };
}

function solid(hex, opacity = 1) {
  return { type: "SOLID", color: rgb(hex), opacity };
}

async function getOrCreateCollection(name, modeName) {
  const collections = await figma.variables.getLocalVariableCollectionsAsync();
  let collection = collections.find((candidate) => candidate.name === name);
  if (!collection) {
    collection = figma.variables.createVariableCollection(name);
  }
  if (collection.modes[0].name !== modeName) {
    collection.renameMode(collection.modes[0].modeId, modeName);
  }
  return collection;
}

async function upsertVariable(collection, name, type, value, scopes, cssSyntax) {
  const variables = await figma.variables.getLocalVariablesAsync();
  let variable = variables.find(
    (candidate) =>
      candidate.variableCollectionId === collection.id && candidate.name === name
  );
  if (!variable) {
    variable = figma.variables.createVariable(name, collection, type);
  }
  variable.setValueForMode(collection.modes[0].modeId, value);
  variable.scopes = scopes;
  variable.setVariableCodeSyntax("WEB", cssSyntax);
  return variable;
}

async function createFoundations() {
  const primitives = await getOrCreateCollection(
    "Reading Compass / Primitives",
    "Value"
  );
  const semantic = await getOrCreateCollection(
    "Reading Compass / Semantic",
    "Light"
  );
  const layout = await getOrCreateCollection(
    "Reading Compass / Layout",
    "Value"
  );

  const primitiveVariables = {};
  for (const [name, hex] of Object.entries(palette)) {
    primitiveVariables[name] = await upsertVariable(
      primitives,
      `color/${name}`,
      "COLOR",
      hexToRgba(hex),
      [],
      `var(--rc-${name.replace(/[A-Z]/g, (letter) => `-${letter.toLowerCase()}`)})`
    );
  }

  const semantics = [
    ["color/text/primary", "ink", ["TEXT_FILL"], "var(--ink)"],
    ["color/text/muted", "muted", ["TEXT_FILL"], "var(--muted)"],
    ["color/text/inverse", "white", ["TEXT_FILL"], "var(--surface-raised)"],
    ["color/text/brand", "greenDark", ["TEXT_FILL"], "var(--green-dark)"],
    ["color/background/page", "paper", ["FRAME_FILL", "SHAPE_FILL"], "var(--paper)"],
    ["color/background/surface", "surface", ["FRAME_FILL", "SHAPE_FILL"], "var(--surface)"],
    ["color/background/raised", "white", ["FRAME_FILL", "SHAPE_FILL"], "var(--surface-raised)"],
    ["color/background/brand", "greenDark", ["FRAME_FILL", "SHAPE_FILL"], "var(--green-dark)"],
    ["color/background/brand-action", "green", ["FRAME_FILL", "SHAPE_FILL"], "var(--green)"],
    ["color/background/brand-soft", "greenSoft", ["FRAME_FILL", "SHAPE_FILL"], "var(--green-soft)"],
    ["color/background/accent-soft", "goldSoft", ["FRAME_FILL", "SHAPE_FILL"], "var(--rc-gold-soft)"],
    ["color/border/default", "line", ["STROKE_COLOR"], "var(--line)"],
    ["color/border/brand", "green", ["STROKE_COLOR"], "var(--green)"],
    ["color/status/danger", "danger", ["FRAME_FILL", "SHAPE_FILL", "TEXT_FILL"], "var(--danger)"]
  ];

  const semanticVariables = {};
  for (const [name, primitiveName, scopes, syntax] of semantics) {
    semanticVariables[name] = await upsertVariable(
      semantic,
      name,
      "COLOR",
      figma.variables.createVariableAlias(primitiveVariables[primitiveName]),
      scopes,
      syntax
    );
  }

  const layoutVariables = {};
  for (const value of spacingValues) {
    layoutVariables[`space/${value}`] = await upsertVariable(
      layout,
      `space/${value}`,
      "FLOAT",
      value,
      ["GAP"],
      `var(--rc-space-${value})`
    );
  }
  for (const value of radiusValues) {
    layoutVariables[`radius/${value}`] = await upsertVariable(
      layout,
      `radius/${value}`,
      "FLOAT",
      value,
      ["CORNER_RADIUS"],
      `var(--rc-radius-${value})`
    );
  }

  return {
    collections: { primitives, semantic, layout },
    primitives: primitiveVariables,
    semantic: semanticVariables,
    layout: layoutVariables
  };
}

async function resolveFonts() {
  const available = await figma.listAvailableFontsAsync();
  const find = (families, styles) => {
    for (const family of families) {
      for (const style of styles) {
        const match = available.find(
          (font) => font.fontName.family === family && font.fontName.style === style
        );
        if (match) return match.fontName;
      }
    }
    return available[0].fontName;
  };
  const fonts = {
    body: find(["Inter", "SF Pro Text", "Arial"], ["Regular"]),
    bodyStrong: find(["Inter", "SF Pro Text", "Arial"], ["Semi Bold", "Bold", "Medium"]),
    heading: find(["Georgia", "Merriweather", "Source Serif 4", "Inter"], ["Bold", "Regular"])
  };
  await Promise.all(Object.values(fonts).map((font) => figma.loadFontAsync(font)));
  return fonts;
}

async function upsertTextStyle(name, fontName, fontSize, lineHeight, letterSpacing = 0) {
  const styles = await figma.getLocalTextStylesAsync();
  let style = styles.find((candidate) => candidate.name === name);
  if (!style) style = figma.createTextStyle();
  style.name = name;
  style.fontName = fontName;
  style.fontSize = fontSize;
  style.lineHeight = { value: lineHeight, unit: "PIXELS" };
  style.letterSpacing = { value: letterSpacing, unit: "PIXELS" };
  return style;
}

async function upsertEffectStyle(name, effects) {
  const styles = await figma.getLocalEffectStylesAsync();
  let style = styles.find((candidate) => candidate.name === name);
  if (!style) style = figma.createEffectStyle();
  style.name = name;
  style.effects = effects;
  return style;
}

async function createStyles(fonts) {
  const textStyles = {
    display: await upsertTextStyle("Reading Compass / Display", fonts.heading, 64, 68, -1.4),
    h1: await upsertTextStyle("Reading Compass / Heading / H1", fonts.heading, 48, 52, -0.8),
    h2: await upsertTextStyle("Reading Compass / Heading / H2", fonts.heading, 30, 36, -0.3),
    h3: await upsertTextStyle("Reading Compass / Heading / H3", fonts.heading, 21, 27),
    body: await upsertTextStyle("Reading Compass / Body", fonts.body, 16, 25),
    bodySmall: await upsertTextStyle("Reading Compass / Body / Small", fonts.body, 14, 21),
    label: await upsertTextStyle("Reading Compass / Label", fonts.bodyStrong, 13, 18, 0.4),
    eyebrow: await upsertTextStyle("Reading Compass / Eyebrow", fonts.bodyStrong, 12, 16, 1.5)
  };
  const effects = {
    card: await upsertEffectStyle("Reading Compass / Shadow / Card", [
      {
        type: "DROP_SHADOW",
        color: { r: 32 / 255, g: 51 / 255, b: 39 / 255, a: 0.08 },
        offset: { x: 0, y: 10 },
        radius: 28,
        spread: 0,
        visible: true,
        blendMode: "NORMAL"
      }
    ]),
    hero: await upsertEffectStyle("Reading Compass / Shadow / Hero", [
      {
        type: "DROP_SHADOW",
        color: { r: 32 / 255, g: 51 / 255, b: 39 / 255, a: 0.1 },
        offset: { x: 0, y: 22 },
        radius: 60,
        spread: 0,
        visible: true,
        blendMode: "NORMAL"
      }
    ])
  };
  return { textStyles, effects };
}

function bindFill(node, variable, fallback = palette.surface) {
  node.fills = [
    figma.variables.setBoundVariableForPaint(solid(fallback), "color", variable)
  ];
}

function bindStroke(node, variable, fallback = palette.line) {
  node.strokes = [
    figma.variables.setBoundVariableForPaint(solid(fallback), "color", variable)
  ];
  node.strokeWeight = 1;
}

function bindRadius(node, variable, fallback = 16) {
  node.cornerRadius = fallback;
  for (const property of [
    "topLeftRadius",
    "topRightRadius",
    "bottomLeftRadius",
    "bottomRightRadius"
  ]) {
    node.setBoundVariable(property, variable);
  }
}

function bindPadding(node, variable, fallback = 16) {
  node.paddingTop = fallback;
  node.paddingBottom = fallback;
  node.paddingLeft = fallback;
  node.paddingRight = fallback;
  for (const property of ["paddingTop", "paddingBottom", "paddingLeft", "paddingRight"]) {
    node.setBoundVariable(property, variable);
  }
}

function bindGap(node, variable, fallback = 16) {
  node.itemSpacing = fallback;
  node.setBoundVariable("itemSpacing", variable);
}

function frame(name, direction = "VERTICAL") {
  const node = figma.createFrame();
  node.name = name;
  node.layoutMode = direction;
  node.primaryAxisSizingMode = "AUTO";
  node.counterAxisSizingMode = "AUTO";
  node.primaryAxisAlignItems = "MIN";
  node.counterAxisAlignItems = "MIN";
  node.fills = [];
  node.clipsContent = false;
  return node;
}

function fixedWidth(node, width) {
  node.resize(width, Math.max(1, node.height));
  if (node.layoutMode === "VERTICAL") node.counterAxisSizingMode = "FIXED";
  if (node.layoutMode === "HORIZONTAL") node.primaryAxisSizingMode = "FIXED";
  return node;
}

function fixedSize(node, width, height) {
  node.resize(width, height);
  if (node.layoutMode === "VERTICAL") {
    node.counterAxisSizingMode = "FIXED";
    node.primaryAxisSizingMode = "FIXED";
  } else {
    node.primaryAxisSizingMode = "FIXED";
    node.counterAxisSizingMode = "FIXED";
  }
  return node;
}

async function textNode(ctx, value, kind = "body", options = {}) {
  const node = figma.createText();
  node.name = options.name || "text";
  const definitions = {
    display: [ctx.fonts.heading, 64, 68, ctx.foundations.semantic["color/text/primary"]],
    h1: [ctx.fonts.heading, 48, 52, ctx.foundations.semantic["color/text/primary"]],
    h2: [ctx.fonts.heading, 30, 36, ctx.foundations.semantic["color/text/primary"]],
    h3: [ctx.fonts.heading, 21, 27, ctx.foundations.semantic["color/text/primary"]],
    body: [ctx.fonts.body, 16, 25, ctx.foundations.semantic["color/text/primary"]],
    small: [ctx.fonts.body, 14, 21, ctx.foundations.semantic["color/text/muted"]],
    label: [ctx.fonts.bodyStrong, 13, 18, ctx.foundations.semantic["color/text/primary"]],
    eyebrow: [ctx.fonts.bodyStrong, 12, 16, ctx.foundations.semantic["color/text/brand"]]
  };
  const [fontName, fontSize, lineHeight, colorVariable] = definitions[kind];
  node.fontName = fontName;
  node.fontSize = options.fontSize || fontSize;
  node.lineHeight = { value: options.lineHeight || lineHeight, unit: "PIXELS" };
  node.characters = value;
  node.textAutoResize = options.width ? "HEIGHT" : "WIDTH_AND_HEIGHT";
  if (options.width) node.resize(options.width, Math.max(lineHeight, node.height));
  bindFill(node, options.color || colorVariable, options.fallback || palette.ink);
  if (options.align) node.textAlignHorizontal = options.align;
  if (options.opacity !== undefined) node.opacity = options.opacity;
  return node;
}

async function makePage(name) {
  const page = figma.createPage();
  page.name = `${PAGE_PREFIX}${name}`;
  page.setPluginData("owner", OWNER_KEY);
  await figma.setCurrentPageAsync(page);
  return page;
}

async function removeOwnedPages() {
  await figma.loadAllPagesAsync();
  const owned = figma.root.children.filter(
    (page) => page.getPluginData("owner") === OWNER_KEY
  );
  if (!owned.length) return;
  let safePage = figma.root.children.find(
    (page) => page.getPluginData("owner") !== OWNER_KEY
  );
  if (!safePage) {
    safePage = figma.createPage();
    safePage.name = "Working file";
  }
  await figma.setCurrentPageAsync(safePage);
  for (const page of owned) page.remove();
}

async function createFoundationsPage(ctx) {
  const page = await makePage("Foundations");
  const root = frame("Foundations");
  fixedWidth(root, 1440);
  root.paddingTop = 80;
  root.paddingBottom = 120;
  root.paddingLeft = 80;
  root.paddingRight = 80;
  root.itemSpacing = 72;
  bindFill(root, ctx.foundations.semantic["color/background/page"], palette.paper);
  page.appendChild(root);

  const intro = frame("Introduction");
  intro.itemSpacing = 12;
  intro.appendChild(await textNode(ctx, "READING COMPASS", "eyebrow"));
  intro.appendChild(await textNode(ctx, "Visual foundations", "h1"));
  intro.appendChild(
    await textNode(
      ctx,
      "A warm editorial system for finding books through mood, pace, themes and community context.",
      "body",
      { width: 720 }
    )
  );
  root.appendChild(intro);

  const colors = frame("Colors");
  colors.itemSpacing = 20;
  colors.appendChild(await textNode(ctx, "Colors", "h2"));
  colors.appendChild(
    await textNode(ctx, "Primitive palette and semantic roles used by the production interface.", "small")
  );
  const colorGrid = frame("Color tokens", "HORIZONTAL");
  colorGrid.layoutWrap = "WRAP";
  colorGrid.itemSpacing = 16;
  colorGrid.counterAxisSpacing = 16;
  fixedWidth(colorGrid, 1280);
  for (const [name, variable] of Object.entries(ctx.foundations.primitives)) {
    const swatch = frame(`Swatch/${name}`);
    fixedWidth(swatch, 144);
    swatch.itemSpacing = 10;
    const chip = figma.createRectangle();
    chip.name = "variable-bound color";
    chip.resize(144, 92);
    bindRadius(chip, ctx.foundations.layout["radius/14"], 14);
    bindFill(chip, variable, palette[name]);
    swatch.appendChild(chip);
    swatch.appendChild(await textNode(ctx, name, "label"));
    swatch.appendChild(await textNode(ctx, `--rc-${name.replace(/[A-Z]/g, (m) => `-${m.toLowerCase()}`)}`, "small", { width: 144 }));
    colorGrid.appendChild(swatch);
  }
  colors.appendChild(colorGrid);
  root.appendChild(colors);

  const typography = frame("Typography");
  typography.itemSpacing = 18;
  typography.appendChild(await textNode(ctx, "Typography", "h2"));
  const samples = [
    ["Display / 64", "The next book starts here", "display"],
    ["Heading / 30", "Community catalogue", "h2"],
    ["Body / 16", "Describe the reading experience you want, not just a genre.", "body"],
    ["Label / 13", "CURRENTLY READING", "label"]
  ];
  for (const [label, sample, kind] of samples) {
    const specimen = frame(`Type/${label}`);
    specimen.itemSpacing = 8;
    fixedWidth(specimen, 1280);
    specimen.paddingBottom = 18;
    specimen.appendChild(await textNode(ctx, label, "small"));
    specimen.appendChild(await textNode(ctx, sample, kind, { width: 1100 }));
    typography.appendChild(specimen);
  }
  root.appendChild(typography);

  const measures = frame("Spacing and radius", "HORIZONTAL");
  measures.itemSpacing = 64;
  const spacing = frame("Spacing");
  spacing.itemSpacing = 12;
  spacing.appendChild(await textNode(ctx, "Spacing", "h2"));
  for (const value of spacingValues) {
    const row = frame(`space/${value}`, "HORIZONTAL");
    row.counterAxisAlignItems = "CENTER";
    row.itemSpacing = 16;
    const bar = figma.createRectangle();
    bar.resize(value * 2, 12);
    bindFill(bar, ctx.foundations.semantic["color/background/brand-action"], palette.green);
    bar.setBoundVariable("height", ctx.foundations.layout["space/12"]);
    row.appendChild(bar);
    row.appendChild(await textNode(ctx, `space/${value} · ${value}px · --rc-space-${value}`, "small"));
    spacing.appendChild(row);
  }
  measures.appendChild(spacing);
  const radii = frame("Radius and elevation");
  radii.itemSpacing = 18;
  radii.appendChild(await textNode(ctx, "Radius & elevation", "h2"));
  const radiusRow = frame("Radius tokens", "HORIZONTAL");
  radiusRow.itemSpacing = 18;
  for (const value of [8, 14, 20, 26, 999]) {
    const item = frame(`radius/${value}`);
    item.itemSpacing = 8;
    const demo = figma.createRectangle();
    demo.resize(72, 72);
    bindFill(demo, ctx.foundations.semantic["color/background/brand-soft"], palette.greenSoft);
    bindStroke(demo, ctx.foundations.semantic["color/border/brand"], palette.green);
    bindRadius(demo, ctx.foundations.layout[`radius/${value}`], Math.min(value, 36));
    item.appendChild(demo);
    item.appendChild(await textNode(ctx, value === 999 ? "pill" : `${value}px`, "small"));
    radiusRow.appendChild(item);
  }
  radii.appendChild(radiusRow);
  const shadowRow = frame("Elevation", "HORIZONTAL");
  shadowRow.itemSpacing = 24;
  for (const [name, style] of Object.entries(ctx.styles.effects)) {
    const card = frame(`Shadow/${name}`);
    fixedSize(card, 180, 110);
    card.primaryAxisAlignItems = "CENTER";
    card.counterAxisAlignItems = "CENTER";
    bindFill(card, ctx.foundations.semantic["color/background/raised"], palette.white);
    bindRadius(card, ctx.foundations.layout["radius/16"], 16);
    card.effects = style.effects;
    card.appendChild(await textNode(ctx, name, "label"));
    shadowRow.appendChild(card);
  }
  radii.appendChild(shadowRow);
  measures.appendChild(radii);
  root.appendChild(measures);
  return page;
}

async function makeButtonComponents(ctx, parent) {
  const components = [];
  const byVariant = {};
  for (const size of ["Default", "Small"]) {
    for (const style of ["Primary", "Secondary"]) {
      const component = figma.createComponent();
      component.name = `Style=${style}, Size=${size}`;
      component.layoutMode = "HORIZONTAL";
      component.primaryAxisSizingMode = "AUTO";
      component.counterAxisSizingMode = "AUTO";
      component.primaryAxisAlignItems = "CENTER";
      component.counterAxisAlignItems = "CENTER";
      bindPadding(component, ctx.foundations.layout[size === "Small" ? "space/10" : "space/12"], size === "Small" ? 10 : 12);
      component.paddingLeft = size === "Small" ? 16 : 20;
      component.paddingRight = size === "Small" ? 16 : 20;
      bindRadius(component, ctx.foundations.layout["radius/999"], 999);
      bindFill(
        component,
        ctx.foundations.semantic[style === "Primary" ? "color/background/brand" : "color/background/raised"],
        style === "Primary" ? palette.greenDark : palette.white
      );
      if (style === "Secondary") bindStroke(component, ctx.foundations.semantic["color/border/brand"], palette.green);
      const label = await textNode(ctx, "Find my next read", "label", {
        name: "label",
        color: ctx.foundations.semantic[style === "Primary" ? "color/text/inverse" : "color/text/brand"],
        fallback: style === "Primary" ? palette.white : palette.greenDark
      });
      component.appendChild(label);
      components.push(component);
      byVariant[`${style}/${size}`] = component;
    }
  }
  const set = figma.combineAsVariants(components, parent);
  set.name = "Button";
  set.description = "Primary and secondary actions in default and compact sizes.";
  set.fills = [];
  set.resizeWithoutConstraints(480, 210);
  set.children.forEach((child, index) => {
    child.x = 32 + (index % 2) * 220;
    child.y = 32 + Math.floor(index / 2) * 80;
  });
  const labelKey = set.addComponentProperty("Label", "TEXT", "Find my next read");
  for (const child of set.children) {
    const label = child.findOne((node) => node.name === "label");
    if (label) label.componentPropertyReferences = { characters: labelKey };
  }
  return { set, byVariant };
}

async function makeTagComponent(ctx, parent) {
  const component = figma.createComponent();
  component.name = "Tag";
  component.layoutMode = "HORIZONTAL";
  component.primaryAxisSizingMode = "AUTO";
  component.counterAxisSizingMode = "AUTO";
  component.primaryAxisAlignItems = "CENTER";
  component.counterAxisAlignItems = "CENTER";
  bindPadding(component, ctx.foundations.layout["space/8"], 8);
  component.paddingLeft = 12;
  component.paddingRight = 12;
  bindRadius(component, ctx.foundations.layout["radius/999"], 999);
  bindFill(component, ctx.foundations.semantic["color/background/brand-soft"], palette.greenSoft);
  const label = await textNode(ctx, "Reflective", "label", { name: "label", color: ctx.foundations.semantic["color/text/brand"] });
  component.appendChild(label);
  const labelKey = component.addComponentProperty("Label", "TEXT", "Reflective");
  label.componentPropertyReferences = { characters: labelKey };
  parent.appendChild(component);
  return component;
}

async function makeStatusComponents(ctx, parent) {
  const definitions = {
    "Want to Read": ["Want to read", "color/background/accent-soft", palette.goldSoft],
    "Currently Reading": ["Currently reading", "color/background/brand-soft", palette.greenSoft],
    Paused: ["Paused", "color/background/raised", palette.white],
    Completed: ["Completed", "color/background/brand", palette.greenDark]
  };
  const components = [];
  const byVariant = {};
  for (const [status, [labelValue, colorName, fallback]] of Object.entries(definitions)) {
    const component = figma.createComponent();
    component.name = `Status=${status}`;
    component.layoutMode = "HORIZONTAL";
    component.primaryAxisSizingMode = "AUTO";
    component.counterAxisSizingMode = "AUTO";
    bindPadding(component, ctx.foundations.layout["space/8"], 8);
    component.paddingLeft = 12;
    component.paddingRight = 12;
    bindRadius(component, ctx.foundations.layout["radius/999"], 999);
    bindFill(component, ctx.foundations.semantic[colorName], fallback);
    const inverse = status === "Completed";
    component.appendChild(await textNode(ctx, labelValue, "label", {
      name: "label",
      color: ctx.foundations.semantic[inverse ? "color/text/inverse" : "color/text/brand"],
      fallback: inverse ? palette.white : palette.greenDark
    }));
    components.push(component);
    byVariant[status] = component;
  }
  const set = figma.combineAsVariants(components, parent);
  set.name = "Reading Status";
  set.description = "Reading-list states shared by cards, detail views and the dashboard.";
  set.fills = [];
  set.resizeWithoutConstraints(690, 100);
  set.children.forEach((child, index) => {
    child.x = 24 + index * 165;
    child.y = 28;
  });
  return { set, byVariant };
}

async function makeNavComponent(ctx, parent) {
  const component = figma.createComponent();
  component.name = "Site Header";
  component.layoutMode = "HORIZONTAL";
  component.primaryAxisSizingMode = "FIXED";
  component.counterAxisSizingMode = "FIXED";
  component.resize(1280, 76);
  component.primaryAxisAlignItems = "SPACE_BETWEEN";
  component.counterAxisAlignItems = "CENTER";
  component.paddingLeft = 28;
  component.paddingRight = 28;
  bindFill(component, ctx.foundations.semantic["color/background/raised"], palette.white);
  bindRadius(component, ctx.foundations.layout["radius/20"], 20);
  component.effects = ctx.styles.effects.card.effects;
  const brand = frame("Brand", "HORIZONTAL");
  brand.counterAxisAlignItems = "CENTER";
  brand.itemSpacing = 12;
  const mark = figma.createEllipse();
  mark.resize(34, 34);
  bindFill(mark, ctx.foundations.semantic["color/background/brand"], palette.greenDark);
  brand.appendChild(mark);
  brand.appendChild(await textNode(ctx, "Reading Compass", "h3"));
  component.appendChild(brand);
  const links = frame("Navigation", "HORIZONTAL");
  links.counterAxisAlignItems = "CENTER";
  links.itemSpacing = 28;
  for (const value of ["Explore", "Dashboard", "Community", "Lists"]) {
    links.appendChild(await textNode(ctx, value, "label"));
  }
  component.appendChild(links);
  parent.appendChild(component);
  return component;
}

async function makeBookCardComponent(ctx, parent, tagComponent) {
  const component = figma.createComponent();
  component.name = "Book Card";
  component.layoutMode = "VERTICAL";
  component.primaryAxisSizingMode = "AUTO";
  component.counterAxisSizingMode = "FIXED";
  component.resize(368, 1);
  bindPadding(component, ctx.foundations.layout["space/20"], 20);
  bindGap(component, ctx.foundations.layout["space/16"], 16);
  bindRadius(component, ctx.foundations.layout["radius/20"], 20);
  bindFill(component, ctx.foundations.semantic["color/background/raised"], palette.white);
  bindStroke(component, ctx.foundations.semantic["color/border/default"], palette.line);
  component.effects = ctx.styles.effects.card.effects;
  const cover = frame("cover");
  fixedSize(cover, 328, 214);
  cover.primaryAxisAlignItems = "CENTER";
  cover.counterAxisAlignItems = "CENTER";
  bindFill(cover, ctx.foundations.semantic["color/background/brand"], palette.greenDark);
  bindRadius(cover, ctx.foundations.layout["radius/14"], 14);
  cover.appendChild(await textNode(ctx, "RC", "display", { fontSize: 38, lineHeight: 44, color: ctx.foundations.semantic["color/text/inverse"], fallback: palette.white }));
  component.appendChild(cover);
  const tag = tagComponent.createInstance();
  const tagLabel = tag.findOne((node) => node.name === "label");
  if (tagLabel) tagLabel.characters = "Slow-burn mystery";
  component.appendChild(tag);
  const title = await textNode(ctx, "The Cartographer's Quiet", "h3", { name: "title", width: 328 });
  const author = await textNode(ctx, "Mara Ellison", "small", { name: "author", width: 328 });
  const reason = await textNode(ctx, "Atmospheric, character-led, and ideal for an unhurried weekend.", "small", { name: "reason", width: 328 });
  component.appendChild(title);
  component.appendChild(author);
  component.appendChild(reason);
  const titleKey = component.addComponentProperty("Title", "TEXT", title.characters);
  const authorKey = component.addComponentProperty("Author", "TEXT", author.characters);
  const reasonKey = component.addComponentProperty("Reason", "TEXT", reason.characters);
  title.componentPropertyReferences = { characters: titleKey };
  author.componentPropertyReferences = { characters: authorKey };
  reason.componentPropertyReferences = { characters: reasonKey };
  parent.appendChild(component);
  return component;
}

async function createComponentsPage(ctx) {
  const page = await makePage("Components");
  const canvas = frame("Component library");
  fixedWidth(canvas, 1440);
  canvas.paddingTop = 72;
  canvas.paddingBottom = 120;
  canvas.paddingLeft = 80;
  canvas.paddingRight = 80;
  canvas.itemSpacing = 52;
  bindFill(canvas, ctx.foundations.semantic["color/background/page"], palette.paper);
  page.appendChild(canvas);
  canvas.appendChild(await textNode(ctx, "Reusable components", "h1"));
  canvas.appendChild(await textNode(ctx, "Production-aligned building blocks with editable properties and compact variants.", "body"));

  const buttonSection = frame("Buttons");
  buttonSection.itemSpacing = 16;
  buttonSection.appendChild(await textNode(ctx, "Buttons", "h2"));
  canvas.appendChild(buttonSection);
  const buttons = await makeButtonComponents(ctx, buttonSection);

  const smallSection = frame("Tags and status");
  smallSection.itemSpacing = 16;
  smallSection.appendChild(await textNode(ctx, "Tags & reading status", "h2"));
  canvas.appendChild(smallSection);
  const tag = await makeTagComponent(ctx, smallSection);
  const statuses = await makeStatusComponents(ctx, smallSection);

  const navSection = frame("Navigation");
  navSection.itemSpacing = 16;
  navSection.appendChild(await textNode(ctx, "Navigation", "h2"));
  canvas.appendChild(navSection);
  const nav = await makeNavComponent(ctx, navSection);

  const cardSection = frame("Book cards");
  cardSection.itemSpacing = 16;
  cardSection.appendChild(await textNode(ctx, "Book cards", "h2"));
  canvas.appendChild(cardSection);
  const bookCard = await makeBookCardComponent(ctx, cardSection, tag);
  return { page, buttons, tag, statuses, nav, bookCard };
}

function setInstanceText(instance, name, value) {
  const node = instance.findOne((candidate) => candidate.type === "TEXT" && candidate.name === name);
  if (node) node.characters = value;
}

async function addScreenShell(ctx, pageName, components) {
  const page = await makePage(pageName);
  const screen = frame(`${pageName} / Desktop`);
  fixedWidth(screen, 1440);
  screen.paddingTop = 32;
  screen.paddingBottom = 96;
  screen.paddingLeft = 80;
  screen.paddingRight = 80;
  screen.itemSpacing = 44;
  bindFill(screen, ctx.foundations.semantic["color/background/page"], palette.paper);
  page.appendChild(screen);
  screen.appendChild(components.nav.createInstance());
  return { page, screen };
}

async function addButtonInstance(parent, component, label) {
  const instance = component.createInstance();
  setInstanceText(instance, "label", label);
  parent.appendChild(instance);
  return instance;
}

async function createExploreScreen(ctx, components) {
  const { screen } = await addScreenShell(ctx, "Explore", components);
  const hero = frame("Explore hero", "HORIZONTAL");
  fixedWidth(hero, 1280);
  hero.primaryAxisAlignItems = "SPACE_BETWEEN";
  hero.counterAxisAlignItems = "CENTER";
  hero.paddingTop = 56;
  hero.paddingBottom = 56;
  hero.paddingLeft = 56;
  hero.paddingRight = 56;
  bindFill(hero, ctx.foundations.semantic["color/background/brand"], palette.greenDark);
  bindRadius(hero, ctx.foundations.layout["radius/26"], 26);
  hero.effects = ctx.styles.effects.hero.effects;
  const copy = frame("Hero copy");
  fixedWidth(copy, 650);
  copy.itemSpacing = 16;
  copy.appendChild(await textNode(ctx, "FIND A BOOK BY FEELING", "eyebrow", { color: ctx.foundations.primitives.goldSoft, fallback: palette.goldSoft }));
  copy.appendChild(await textNode(ctx, "What kind of reading experience do you want?", "h1", { width: 650, color: ctx.foundations.semantic["color/text/inverse"], fallback: palette.white }));
  copy.appendChild(await textNode(ctx, "Search by mood, pace, themes and the way you want a story to stay with you.", "body", { width: 600, color: ctx.foundations.semantic["color/text/inverse"], fallback: palette.white, opacity: 0.82 }));
  hero.appendChild(copy);
  const search = frame("Trait search");
  fixedWidth(search, 410);
  search.itemSpacing = 14;
  bindPadding(search, ctx.foundations.layout["space/24"], 24);
  bindFill(search, ctx.foundations.semantic["color/background/raised"], palette.white);
  bindRadius(search, ctx.foundations.layout["radius/20"], 20);
  search.appendChild(await textNode(ctx, "Try “quiet, hopeful, coastal”", "small"));
  const field = frame("Search field", "HORIZONTAL");
  fixedWidth(field, 362);
  field.counterAxisAlignItems = "CENTER";
  field.paddingTop = 14;
  field.paddingBottom = 14;
  field.paddingLeft = 16;
  field.paddingRight = 16;
  bindFill(field, ctx.foundations.semantic["color/background/surface"], palette.surface);
  bindStroke(field, ctx.foundations.semantic["color/border/default"], palette.line);
  bindRadius(field, ctx.foundations.layout["radius/14"], 14);
  field.appendChild(await textNode(ctx, "Describe your next read…", "body"));
  search.appendChild(field);
  await addButtonInstance(search, components.buttons.byVariant["Primary/Default"], "Find matching books");
  hero.appendChild(search);
  screen.appendChild(hero);

  const quick = frame("Quick paths");
  quick.itemSpacing = 16;
  quick.appendChild(await textNode(ctx, "Start with a reading mood", "h2"));
  const tags = frame("Mood tags", "HORIZONTAL");
  tags.itemSpacing = 12;
  for (const value of ["Hopeful", "Quiet", "Fast-paced", "Character-led", "Escapist", "Thought-provoking"]) {
    const instance = components.tag.createInstance();
    setInstanceText(instance, "label", value);
    tags.appendChild(instance);
  }
  quick.appendChild(tags);
  screen.appendChild(quick);

  screen.appendChild(await textNode(ctx, "Community catalogue", "h2"));
  const cards = frame("Book grid", "HORIZONTAL");
  cards.itemSpacing = 28;
  const books = [
    ["The Cartographer's Quiet", "Mara Ellison", "A reflective mystery with a gentle, coastal pace."],
    ["Lanterns at Low Tide", "Jun Park", "Hopeful found-family fiction with luminous settings."],
    ["The Orchard Between Us", "Iris Bell", "Tender literary fiction about memory and belonging."]
  ];
  for (const [title, author, reason] of books) {
    const instance = components.bookCard.createInstance();
    setInstanceText(instance, "title", title);
    setInstanceText(instance, "author", author);
    setInstanceText(instance, "reason", reason);
    cards.appendChild(instance);
  }
  screen.appendChild(cards);
}

async function createDashboardScreen(ctx, components) {
  const { screen } = await addScreenShell(ctx, "Dashboard", components);
  const heading = frame("Dashboard heading", "HORIZONTAL");
  fixedWidth(heading, 1280);
  heading.primaryAxisAlignItems = "SPACE_BETWEEN";
  heading.counterAxisAlignItems = "END";
  const copy = frame("Heading copy");
  copy.itemSpacing = 8;
  copy.appendChild(await textNode(ctx, "YOUR READING HOME", "eyebrow"));
  copy.appendChild(await textNode(ctx, "Good afternoon, Alex", "h1"));
  copy.appendChild(await textNode(ctx, "Keep your current reads moving and discover what fits next.", "body"));
  heading.appendChild(copy);
  await addButtonInstance(heading, components.buttons.byVariant["Secondary/Default"], "View all lists");
  screen.appendChild(heading);

  const current = frame("Currently reading");
  current.itemSpacing = 20;
  current.appendChild(await textNode(ctx, "Currently reading", "h2"));
  const progressCard = frame("Progress card", "HORIZONTAL");
  fixedWidth(progressCard, 1280);
  progressCard.itemSpacing = 28;
  progressCard.counterAxisAlignItems = "CENTER";
  bindPadding(progressCard, ctx.foundations.layout["space/24"], 24);
  bindFill(progressCard, ctx.foundations.semantic["color/background/raised"], palette.white);
  bindStroke(progressCard, ctx.foundations.semantic["color/border/default"], palette.line);
  bindRadius(progressCard, ctx.foundations.layout["radius/20"], 20);
  const cover = frame("Current book cover");
  fixedSize(cover, 150, 210);
  cover.primaryAxisAlignItems = "CENTER";
  cover.counterAxisAlignItems = "CENTER";
  bindFill(cover, ctx.foundations.semantic["color/background/brand"], palette.greenDark);
  bindRadius(cover, ctx.foundations.layout["radius/14"], 14);
  cover.appendChild(await textNode(ctx, "LALT", "h2", { color: ctx.foundations.semantic["color/text/inverse"], fallback: palette.white }));
  progressCard.appendChild(cover);
  const detail = frame("Current book detail");
  fixedWidth(detail, 790);
  detail.itemSpacing = 12;
  detail.appendChild(components.statuses.byVariant["Currently Reading"].createInstance());
  detail.appendChild(await textNode(ctx, "Lanterns at Low Tide", "h2"));
  detail.appendChild(await textNode(ctx, "Jun Park · 42% complete", "small"));
  const track = figma.createRectangle();
  track.resize(760, 10);
  bindFill(track, ctx.foundations.semantic["color/background/brand-soft"], palette.greenSoft);
  track.cornerRadius = 999;
  detail.appendChild(track);
  detail.appendChild(await textNode(ctx, "Next note: look for the shift in Mina's relationship with the harbour community.", "body", { width: 760 }));
  progressCard.appendChild(detail);
  await addButtonInstance(progressCard, components.buttons.byVariant["Primary/Default"], "Update progress");
  current.appendChild(progressCard);
  screen.appendChild(current);

  screen.appendChild(await textNode(ctx, "Recommended for your current mood", "h2"));
  const recommendations = frame("Recommendations", "HORIZONTAL");
  recommendations.itemSpacing = 28;
  for (const [title, author, reason] of [
    ["The Orchard Between Us", "Iris Bell", "Matches your preference for reflective, character-led stories."],
    ["Weather for Small Rooms", "Noor Vance", "A concise, hopeful read with an intimate emotional scale."],
    ["After the Last Ferry", "Tomas Reed", "Coastal atmosphere with a slightly quicker mystery arc."]
  ]) {
    const instance = components.bookCard.createInstance();
    setInstanceText(instance, "title", title);
    setInstanceText(instance, "author", author);
    setInstanceText(instance, "reason", reason);
    recommendations.appendChild(instance);
  }
  screen.appendChild(recommendations);
}

async function createBookScreen(ctx, components) {
  const { screen } = await addScreenShell(ctx, "Community Book", components);
  const hero = frame("Book detail", "HORIZONTAL");
  fixedWidth(hero, 1280);
  hero.itemSpacing = 52;
  hero.counterAxisAlignItems = "CENTER";
  bindPadding(hero, ctx.foundations.layout["space/40"], 40);
  bindFill(hero, ctx.foundations.semantic["color/background/raised"], palette.white);
  bindRadius(hero, ctx.foundations.layout["radius/26"], 26);
  hero.effects = ctx.styles.effects.hero.effects;
  const cover = frame("Book cover");
  fixedSize(cover, 290, 410);
  cover.primaryAxisAlignItems = "CENTER";
  cover.counterAxisAlignItems = "CENTER";
  bindFill(cover, ctx.foundations.semantic["color/background/brand"], palette.greenDark);
  bindRadius(cover, ctx.foundations.layout["radius/18"], 18);
  cover.appendChild(await textNode(ctx, "THE\nCARTOGRAPHER'S\nQUIET", "h2", { width: 230, align: "CENTER", color: ctx.foundations.semantic["color/text/inverse"], fallback: palette.white }));
  hero.appendChild(cover);
  const detail = frame("Book information");
  fixedWidth(detail, 850);
  detail.itemSpacing = 16;
  detail.appendChild(await textNode(ctx, "COMMUNITY BOOK", "eyebrow"));
  detail.appendChild(await textNode(ctx, "The Cartographer's Quiet", "h1", { width: 850 }));
  detail.appendChild(await textNode(ctx, "Mara Ellison · 336 pages · Literary mystery", "body"));
  detail.appendChild(await textNode(ctx, "A retired mapmaker returns to a fogbound island and finds the coastline—and the community's shared memory—quietly changing around her.", "body", { width: 780 }));
  const tagRow = frame("Book traits", "HORIZONTAL");
  tagRow.itemSpacing = 10;
  for (const value of ["Reflective", "Atmospheric", "Slow pace", "Coastal", "Character-led"]) {
    const instance = components.tag.createInstance();
    setInstanceText(instance, "label", value);
    tagRow.appendChild(instance);
  }
  detail.appendChild(tagRow);
  const actions = frame("Book actions", "HORIZONTAL");
  actions.itemSpacing = 12;
  await addButtonInstance(actions, components.buttons.byVariant["Primary/Default"], "Want to read");
  await addButtonInstance(actions, components.buttons.byVariant["Secondary/Default"], "Add to a list");
  detail.appendChild(actions);
  hero.appendChild(detail);
  screen.appendChild(hero);

  const lower = frame("Book community content", "HORIZONTAL");
  lower.itemSpacing = 32;
  const reviews = frame("Community reviews");
  fixedWidth(reviews, 820);
  reviews.itemSpacing = 18;
  reviews.appendChild(await textNode(ctx, "Community reviews", "h2"));
  for (const [name, body] of [
    ["Sam · 4.5", "The atmosphere is the strongest part: patient without becoming distant, and quietly hopeful by the end."],
    ["Priya · 4.0", "Best read slowly. The mapping motif becomes a thoughtful way to talk about memory and belonging."]
  ]) {
    const review = frame("Review");
    fixedWidth(review, 820);
    review.itemSpacing = 10;
    bindPadding(review, ctx.foundations.layout["space/20"], 20);
    bindFill(review, ctx.foundations.semantic["color/background/raised"], palette.white);
    bindStroke(review, ctx.foundations.semantic["color/border/default"], palette.line);
    bindRadius(review, ctx.foundations.layout["radius/16"], 16);
    review.appendChild(await textNode(ctx, name, "label"));
    review.appendChild(await textNode(ctx, body, "body", { width: 770 }));
    reviews.appendChild(review);
  }
  lower.appendChild(reviews);
  const discussion = frame("Discussion callout");
  fixedWidth(discussion, 428);
  discussion.itemSpacing = 14;
  bindPadding(discussion, ctx.foundations.layout["space/24"], 24);
  bindFill(discussion, ctx.foundations.semantic["color/background/brand-soft"], palette.greenSoft);
  bindRadius(discussion, ctx.foundations.layout["radius/20"], 20);
  discussion.appendChild(await textNode(ctx, "Continue the conversation", "h3"));
  discussion.appendChild(await textNode(ctx, "Join the community thread for spoiler-aware chapter discussion and reading notes.", "body", { width: 370 }));
  await addButtonInstance(discussion, components.buttons.byVariant["Primary/Default"], "Open discussion");
  lower.appendChild(discussion);
  screen.appendChild(lower);
}

async function validateBuild() {
  const pages = figma.root.children.filter((page) => page.getPluginData("owner") === OWNER_KEY);
  const variables = (await figma.variables.getLocalVariablesAsync()).filter((variable) => variable.name.startsWith("color/") || variable.name.startsWith("space/") || variable.name.startsWith("radius/"));
  let components = 0;
  let instances = 0;
  for (const page of pages) {
    components += page.findAll((node) => node.type === "COMPONENT" || node.type === "COMPONENT_SET").length;
    instances += page.findAll((node) => node.type === "INSTANCE").length;
  }
  const expectedPages = ["Foundations", "Components", "Explore", "Dashboard", "Community Book"].map((name) => `${PAGE_PREFIX}${name}`);
  const missing = expectedPages.filter((name) => !pages.some((page) => page.name === name));
  if (missing.length) throw new Error(`Missing pages: ${missing.join(", ")}`);
  if (components < 10 || instances < 20 || variables.length < 30) {
    throw new Error(`Validation failed (${components} components, ${instances} instances, ${variables.length} variables)`);
  }
  return { pages: pages.length, components, instances, variables: variables.length };
}

async function buildPrototype(ctx) {
  await removeOwnedPages();
  await createFoundationsPage(ctx);
  const components = await createComponentsPage(ctx);
  await createExploreScreen(ctx, components);
  await createDashboardScreen(ctx, components);
  await createBookScreen(ctx, components);
  const result = await validateBuild();
  const explorePage = figma.root.children.find((page) => page.name === `${PAGE_PREFIX}Explore`);
  if (explorePage) await figma.setCurrentPageAsync(explorePage);
  figma.viewport.scrollAndZoomIntoView(figma.currentPage.children);
  figma.closePlugin(`Reading Compass ready · ${result.pages} pages · ${result.components} components · ${result.variables} variables · ${result.instances} instances`);
}

async function main() {
  const foundations = await createFoundations();
  const fonts = await resolveFonts();
  const styles = await createStyles(fonts);
  await buildPrototype({ foundations, fonts, styles });
}

main().catch((error) => {
  figma.closePlugin(`Reading Compass build failed: ${error.message}`);
});
