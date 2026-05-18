"""Category normalization for public benchmark reporting."""

LEGACY_TO_PUBLIC = {
    "barrier": "obstructed",
    "crosstalk": "recording",
    "stutter": "dropout",
}

PUBLIC_CATEGORIES = [
    "noise",
    "far_field",
    "obstructed",
    "strong_echo",
    "recording",
    "distortion",
    "dropout",
    "mixed",
]


def normalize_scene(scene: str) -> str:
    return LEGACY_TO_PUBLIC.get(scene, scene)


def public_source_scenes(record: dict) -> list[str]:
    scenes = record.get("source_scenes") or []
    return [normalize_scene(str(scene)) for scene in scenes]


def public_category(record: dict) -> str:
    subset = str(record.get("subset", "")).lower()
    scenes = public_source_scenes(record)
    combination = str(record.get("combination", "")).lower()

    if "mixed" in subset or len(set(scenes)) > 1 or "_" in combination:
        return "mixed"
    if scenes:
        return scenes[0]
    return normalize_scene(combination)


def split_type(record: dict) -> str:
    subset = str(record.get("subset", "")).lower()
    if subset.startswith("real-"):
        return "real"
    if subset.startswith("sim-"):
        return "sim"
    return "unknown"
