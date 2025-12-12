# cinnamon-rolls

roll roll roll roll roll !!!

## GitHub Pages 肉桂捲地圖

專案會把 `google-2025-12-12.csv` 的資料轉成 `docs/data/rolls.json`，並在 `docs/` 內提供靜態頁面，部署到 GitHub Pages 後即可瀏覽每一顆肉桂捲的獨立頁面。

### 如何更新資料
1. 覆寫或更新 `google-2025-12-12.csv`。 
2. 執行產生腳本：
   ```bash
   python scripts/generate_rolls.py
   ```
3. 將 `docs` 目錄推送到 GitHub（預設 Pages 會使用 `docs/` 目錄）。

### 本地預覽
使用任一靜態伺服器（例如 `python -m http.server`），在專案根目錄執行後於瀏覽器開啟 `http://localhost:8000/docs/` 即可預覽。
