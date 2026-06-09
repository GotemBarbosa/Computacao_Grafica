# =========================================================================
# Parâmetros de iluminação por objeto (Projeto 3).
#
# Cada objeto define explicitamente seus próprios coeficientes de reflexão.
# NENHUM valor vem de arquivo .mtl (requisito 7 do enunciado).
#
#   Ka  = coeficiente ambiente   (quanto a luz ambiente afeta o objeto)
#   Kd  = coeficiente difuso     (quão fosco / opaco é o material)
#   Ks  = coeficiente especular  (quão brilhante / polido é o material)
#   shi = shininess              (foco do brilho — maior = brilho mais pontual)
# =========================================================================

MATERIALS = {
    # --- Cenário externo ---
    "sky":          {"Ka": 1.00, "Kd": 0.00, "Ks": 0.00, "shi": 1.0},   # skybox: não sombreia
    "sol":          {"Ka": 1.00, "Kd": 0.00, "Ks": 0.00, "shi": 1.0},   # emissivo
    "lua":          {"Ka": 0.10, "Kd": 0.85, "Ks": 0.05, "shi": 4.0},   # planeta (superfície)
    "marte":        {"Ka": 0.10, "Kd": 0.85, "Ks": 0.05, "shi": 4.0},
    "pineTree":     {"Ka": 0.20, "Kd": 0.90, "Ks": 0.02, "shi": 4.0},
    "treeStump":    {"Ka": 0.20, "Kd": 0.80, "Ks": 0.05, "shi": 4.0},
    "rockTiles":    {"Ka": 0.15, "Kd": 0.75, "Ks": 0.10, "shi": 8.0},
    "cartoonHouse": {"Ka": 0.20, "Kd": 0.70, "Ks": 0.10, "shi": 8.0},
    "forge":        {"Ka": 0.10, "Kd": 0.60, "Ks": 0.40, "shi": 32.0},
    "rocket":       {"Ka": 0.10, "Kd": 0.50, "Ks": 0.70, "shi": 64.0},
    "telescope":    {"Ka": 0.10, "Kd": 0.50, "Ks": 0.70, "shi": 64.0},
    "satelite":     {"Ka": 0.10, "Kd": 0.55, "Ks": 0.65, "shi": 48.0},
    "outerWilds":   {"Ka": 0.10, "Kd": 0.55, "Ks": 0.50, "shi": 32.0},
    "campfire":     {"Ka": 0.40, "Kd": 0.60, "Ks": 0.00, "shi": 1.0},
    "caixa":        {"Ka": 0.20, "Kd": 0.75, "Ks": 0.10, "shi": 8.0},
    "woodPlanks":   {"Ka": 0.20, "Kd": 0.75, "Ks": 0.05, "shi": 4.0},
    "ground":       {"Ka": 0.15, "Kd": 0.80, "Ks": 0.05, "shi": 4.0},
    "snowTerrain":  {"Ka": 0.25, "Kd": 0.80, "Ks": 0.15, "shi": 16.0},
    "jeep":         {"Ka": 0.10, "Kd": 0.55, "Ks": 0.65, "shi": 48.0},
    "wallBox":      {"Ka": 0.20, "Kd": 0.75, "Ks": 0.05, "shi": 4.0},

    # --- Ambiente interno (casa) ---
    "bed":          {"Ka": 0.25, "Kd": 0.75, "Ks": 0.05, "shi": 4.0},
    "chair":        {"Ka": 0.20, "Kd": 0.70, "Ks": 0.10, "shi": 8.0},
    "table":        {"Ka": 0.20, "Kd": 0.70, "Ks": 0.15, "shi": 8.0},
    "shelf":        {"Ka": 0.20, "Kd": 0.70, "Ks": 0.10, "shi": 8.0},
    "shelfWall":    {"Ka": 0.20, "Kd": 0.70, "Ks": 0.10, "shi": 8.0},
    "door":         {"Ka": 0.20, "Kd": 0.70, "Ks": 0.10, "shi": 8.0},
    "barrel":       {"Ka": 0.20, "Kd": 0.65, "Ks": 0.15, "shi": 8.0},
    "candle":       {"Ka": 0.50, "Kd": 0.50, "Ks": 0.00, "shi": 1.0},   # emissivo
    "lantern":      {"Ka": 0.50, "Kd": 0.50, "Ks": 0.30, "shi": 16.0},  # emissivo
    "chandelier":   {"Ka": 0.50, "Kd": 0.50, "Ks": 0.30, "shi": 16.0},
    "axe":          {"Ka": 0.10, "Kd": 0.50, "Ks": 0.80, "shi": 64.0},
    "hammer":       {"Ka": 0.10, "Kd": 0.50, "Ks": 0.80, "shi": 64.0},
    "gun":          {"Ka": 0.10, "Kd": 0.45, "Ks": 0.85, "shi": 96.0},
    "foodCan":      {"Ka": 0.15, "Kd": 0.50, "Ks": 0.75, "shi": 64.0},
    "mug":          {"Ka": 0.20, "Kd": 0.60, "Ks": 0.50, "shi": 32.0},
    "plate":        {"Ka": 0.20, "Kd": 0.55, "Ks": 0.60, "shi": 48.0},
    "jar":          {"Ka": 0.20, "Kd": 0.60, "Ks": 0.55, "shi": 32.0},
    "knife":        {"Ka": 0.10, "Kd": 0.40, "Ks": 0.90, "shi": 128.0},
    "bascket":      {"Ka": 0.20, "Kd": 0.80, "Ks": 0.05, "shi": 4.0},
    "apple":        {"Ka": 0.20, "Kd": 0.85, "Ks": 0.20, "shi": 16.0},
    "pear":         {"Ka": 0.20, "Kd": 0.85, "Ks": 0.20, "shi": 16.0},
    "pileOfBooks":  {"Ka": 0.20, "Kd": 0.75, "Ks": 0.05, "shi": 4.0},
    "globe":        {"Ka": 0.20, "Kd": 0.65, "Ks": 0.50, "shi": 32.0},
    "map":          {"Ka": 0.20, "Kd": 0.80, "Ks": 0.05, "shi": 4.0},
    "painting":     {"Ka": 0.25, "Kd": 0.75, "Ks": 0.05, "shi": 4.0},
    "oxygen":       {"Ka": 0.10, "Kd": 0.50, "Ks": 0.80, "shi": 64.0},
}

# Material padrão para qualquer objeto sem entrada específica.
DEFAULT_MATERIAL = {"Ka": 0.20, "Kd": 0.75, "Ks": 0.10, "shi": 8.0}


def get_material(name):
    return MATERIALS.get(name, DEFAULT_MATERIAL)
