"""Category normalization for public benchmark reporting."""

LEGACY_TO_PUBLIC = {
    "barrier": "obstructed",
    "crosstalk": "recording",
    "stutter": "dropout",
    "strong_echo": "echo",
}

PUBLIC_CATEGORIES = [
    "noise",
    "far_field",
    "obstructed",
    "echo",
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

    if "mixed" in subset or len(set(scenes)) > 1:
        return "mixed"
    if scenes:
        return scenes[0]
    if combination:
        return normalize_scene(combination)

    for category in PUBLIC_CATEGORIES:
        if category != "mixed" and f"-{category}" in subset:
            return category
    path_bits = str(record.get("audio_path", "")).lower().replace("\\", "/").split("/")
    for bit in path_bits:
        normalized = normalize_scene(bit)
        if normalized in PUBLIC_CATEGORIES:
            return normalized
    return ""


def split_type(record: dict) -> str:
    subset = str(record.get("subset", "")).lower()
    if subset.startswith("real-"):
        return "real"
    if subset.startswith("sim-"):
        return "sim"
    return "unknown"


PRIVATE_PUBLIC_FIELDS = {
    "combination",
    "source_scenes",
    "aug_params_m",
    "global_severity",
    "speed_factor",
}


def _replace_legacy_token(text: str) -> str:
    output = str(text)
    replacements = {
        "strong_echo": "echo",
        "crosstalk": "recording",
        "barrier": "obstructed",
        "stutter": "dropout",
    }
    for legacy, public in replacements.items():
        output = output.replace(legacy, public)
    return output


def sanitize_public_record(record: dict) -> dict:
    public = {}
    metadata_fields = {"audio_path", "subset", "name"}
    for key, value in record.items():
        if key in PRIVATE_PUBLIC_FIELDS:
            continue
        if key in metadata_fields and isinstance(value, str):
            public[key] = _replace_legacy_token(value)
        else:
            public[key] = value
    return public
