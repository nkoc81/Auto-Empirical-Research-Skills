#!/usr/bin/env bash
# Ham verileri yeniden indirir (OECD SDMX ve Eurostat SDMX API; açık erişim).
set -euo pipefail
cd "$(dirname "$0")/../data/raw"
O=https://sdmx.oecd.org/public/rest/data
E=https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data
H="Accept: application/vnd.sdmx.data+csv; charset=utf-8; labels=both"
curl -sf -H "$H" "$O/OECD.ELS.JAI,DSD_TAXBEN_IA@DF_IA,1.0/all" | gzip -9 > DF_IA.csv.gz
curl -sf -H "$H" "$O/OECD.ELS.JAI,DSD_TAXBEN_PTR@DF_PTRSA,1.0/all" | gzip -9 > DF_PTRSA.csv.gz
curl -sf "$E/lfst_hheredty/A.T.Y25-54.ED0-2.A1_NCH+A1_CH+A_CPL_CH.RT./?format=SDMX-CSV" > lfst_hheredty.csv
curl -sf "$E/lfsa_ergaed/A.PC.T.Y25-64.ED0-2+ED5-8./?format=SDMX-CSV" > lfsa_ergaed.csv
curl -sf "$E/nama_10_gdp/A.CLV_PCH_PRE.B1GQ./?format=SDMX-CSV" > nama_10_gdp.csv
# Kırılma düzeltilmiş (IESS 2021) LFS ana gösterge serisi ve eğitim bileşimi kontrolü
curl -sf "$E/lfsi_educ_a/A.ED0-2+ED5-8.T.Y25-54+Y20-64.PC_POP./?format=SDMX-CSV" > lfsi_educ_a.csv
curl -sf "$E/edat_lfse_03?format=SDMX-CSV&sex=T&age=Y25-64&isced11=ED0-2&unit=PC" > edat_lfse_03.csv
