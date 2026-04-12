import os
import urllib.request

from kernels import KERNELS

class KernelDownloader:
    def __init__(self, dir: str):
        self.save_dir: str = dir


    def download_kernel(self, fname: str, url: str) -> bool:
        output = os.path.join(self.save_dir, fname)
        os.makedirs(os.path.dirname(output), exist_ok=True)

        if os.path.exists(output) is True:
            print(f"Kernel: [{fname}] already exists - Skipping download")
            return True

        print(f"Downloading: [{fname}]...")

        try:
            urllib.request.urlretrieve(url, output)
        except Exception as e:
            print(f"\nError - {str(e)}")
            return False

        print(f"Saved: [{fname}] to [{output}]\n")

        return True


    def download_kernels(self) -> bool:
        print("Downloading Kernels...")

        for fname, url in KERNELS.items():
            if self.download_kernel(fname, url) is False:
                return False

        print("Download of Kernels complete!")

        return True


if __name__ == "__main__":
    save_dir = os.path.dirname(os.path.abspath(__file__))

    downloader = KernelDownloader(save_dir)
    if downloader.download_kernels() is False:
        print("Failed to download kernels!")
        os._exit(100)

    print("Done!")
