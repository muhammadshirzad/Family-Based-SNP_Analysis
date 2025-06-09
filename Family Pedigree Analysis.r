# Family Pedigree Analysis

# Install R dependencies
!apt-get install -y libcurl4-openssl-dev libssl-dev libxml2-dev
%load_ext rpy2.ipython

%%R
install.packages("BiocManager", repos="https://cloud.r-project.org")
BiocManager::install("kinship2", update=FALSE, ask=FALSE)

from google.colab import files
import pandas as pd

uploaded = files.upload()
file_name = list(uploaded.keys())[0]
df = pd.read_excel(file_name)
df.to_csv("pedigree.csv", index=False)

%%R
library(kinship2)

# 📥 Load and filter
df <- read.csv("pedigree.csv", stringsAsFactors=FALSE)
df <- df[df$FID == 36, ]

# ✅ Validate parent IDs
valid_ids <- df$IID
df <- df[df$PAT == "0" | df$PAT %in% valid_ids, ]
df <- df[df$MAT == "0" | df$MAT %in% valid_ids, ]

# 🧬 Build pedigree object
ped <- pedigree(id = df$IID,
                dadid = df$PAT,
                momid = df$MAT,
                sex = df$SEX)

# 🎨 Define color (light blue tone)
my_color <- rep("#1f78b4", length(df$IID))  # One color for all

# 📌 Save High-Resolution PDF
pdf("pedigree_highres.pdf", width = 30, height = 20)
plot(ped, id = df$IID, col = my_color, cex = 0.6, symbolsize = 2.8, packed = FALSE, align = FALSE)
dev.off()

# 📌 Save High-Resolution PNG
png("pedigree_highres.png", width = 4000, height = 3000, res = 300)
plot(ped, id = df$IID, col = my_color, cex = 0.6, symbolsize = 2.8, packed = FALSE, align = FALSE)
dev.off()

# 📊 Display inline in notebook
plot(ped, id = df$IID, col = my_color, cex = 0.6, symbolsize = 2.8, packed = FALSE, align = FALSE)

from google.colab import files
files.download("pedigree_highres.pdf")
files.download("pedigree_highres.png")