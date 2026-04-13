Need to make this a Python package for easy re-use. There is too much copy paste
Example:
```python3
def load_config(self, config_file: str) -> bool:
    try:
        with open(config_file, "r") as file:
            config = json.load(file)
    except Exception as e:
        print(f"\nError - {str(e)}")
        return False

    try:
        self.spice.furnsh(config["time_kernel"])
        self.spice.furnsh(config["spk_kernel"])
        self.spice.furnsh(config["pck_kernel"])
    except Exception as e:
        print(f"\nError loading kernels - {str(e)}")
        return False

    print("Kernels loaded successfully\n")

    return True
```
