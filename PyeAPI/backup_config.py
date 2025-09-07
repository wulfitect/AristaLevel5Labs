import os
import sys
import yaml
import pyeapi

DEFAULT_YAML = "switches.yaml"
OUTPUT_DIR = "configs"
EAPI_CONF = "eapi.conf"

def load_switches(yaml_path: str):
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    switches = data.get("switches")
    if not isinstance(switches, list) or not switches:
        raise ValueError(f"No switches found in {yaml_path}. Expected key 'switches' with a list.")
    return switches

def main():
    yaml_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_YAML

    # Load eAPI connection profiles
    pyeapi.load_config(EAPI_CONF)

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load switch list from YAML
    switches = load_switches(yaml_path)

    for sw in switches:
        try:
            node = pyeapi.connect_to(sw)
            running_config = node.get_config(as_string=True)  # Note: boolean True (not a string)
            out_file = os.path.join(OUTPUT_DIR, f"{sw}.cfg")
            with open(out_file, "w", encoding="utf-8") as fh:
                fh.write(running_config)
            print(f"Backed up {sw} -> {out_file}")
        except Exception as e:
            print(f"[ERROR] Failed backing up {sw}: {e}")

if __name__ == "__main__":
    main()
