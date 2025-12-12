# cinnamon-rolls

利用 Google 地圖肉桂捲資料自動產生 GitHub Pages 靜態網站。

## 使用方式

1. 確認資料檔 `google-2025-12-12.csv` 位於 repo 根目錄。
2. 執行產生腳本：

   ```bash
   python scripts/generate_sites.py
   ```

   產出的靜態頁面會寫入 `docs/`，包含首頁與每個店家的獨立頁面。
3. 將 `docs/` 設定為 GitHub Pages 的發佈路徑即可直接上線。
