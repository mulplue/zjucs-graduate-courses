import kagglehub
import os

# Download latest version
path = kagglehub.dataset_download("hirunkulphimsiri/fullbody-anime-girls-datasets")

os.system(f"mv {path} ./data")
print(f"move dataset from '{path}' to './data'")