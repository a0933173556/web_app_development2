# 路由設計文件 (Routes) - 活動報名系統

根據 PRD、系統架構及資料庫設計，以下規劃了 Flask 的路由與頁面對照表。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :---: | :--- | :--- | :--- |
| **前台功能** | | | | |
| 活動列表 (首頁) | `GET` | `/` | `index.html` | 顯示所有開放報名的活動 |
| 活動詳情與報名 | `GET` | `/event/<id>` | `event_detail.html` | 顯示單筆活動內容與報名表單 |
| 送出報名 | `POST` | `/event/<id>/register`| — | 接收報名資料，存入資料庫後重導向 |
| **後台功能** | | | | |
| 後台總覽 | `GET` | `/admin` | `admin/dashboard.html` | 顯示活動列表與報名人數統計 |
| 新增活動頁面 | `GET` | `/admin/event/new` | `admin/event_form.html`| 顯示新增活動表單 |
| 建立活動 | `POST`| `/admin/event/new` | — | 接收表單，存入 DB，重導向至總覽 |
| 編輯活動頁面 | `GET` | `/admin/event/<id>/edit`| `admin/event_form.html`| 顯示帶有原資料的編輯表單 |
| 更新活動 | `POST`| `/admin/event/<id>/edit`| — | 接收表單，更新 DB，重導向至總覽 |
| 刪除活動 | `POST`| `/admin/event/<id>/delete`| — | 刪除活動與報名資料，重導向至總覽 |
| 確認人員名單 | `GET` | `/admin/event/<id>/participants`| `admin/participants.html`| 顯示指定活動的所有報名人員 |

## 2. 每個路由的詳細說明

### 前台路由 (`main_routes`)

- **`GET /` (活動列表)**
  - 輸入：無
  - 處理邏輯：呼叫 `Event.get_all()` 取得所有活動
  - 輸出：渲染 `index.html`

- **`GET /event/<id>` (活動詳情與報名)**
  - 輸入：URL 參數 `id`
  - 處理邏輯：呼叫 `Event.get_by_id(id)`，若找不到回傳 404
  - 輸出：渲染 `event_detail.html`

- **`POST /event/<id>/register` (送出報名)**
  - 輸入：URL 參數 `id`，表單欄位 (`name`, `email`, `phone`)
  - 處理邏輯：
    1. 驗證必填欄位。
    2. (選用) 驗證活動是否已達 `capacity` 人數上限。
    3. 呼叫 `Registration.create()`。
  - 輸出：設定 flash 成功訊息，重導向至 `/event/<id>` 或首頁
  - 錯誤處理：資料錯誤則設定 flash 錯誤訊息，重導向回 `/event/<id>`

### 後台路由 (`admin_routes`)

- **`GET /admin` (後台總覽)**
  - 輸入：無
  - 處理邏輯：呼叫 `Event.get_all()`，透過 `event.registrations` 屬性計算目前報名人數
  - 輸出：渲染 `admin/dashboard.html`

- **`GET /admin/event/new` (新增活動頁面)**
  - 輸入：無
  - 處理邏輯：無
  - 輸出：渲染 `admin/event_form.html`

- **`POST /admin/event/new` (建立活動)**
  - 輸入：表單欄位 (`title`, `description`, `location`, `start_time`, `end_time`, `capacity`)
  - 處理邏輯：呼叫 `Event.create()`
  - 輸出：重導向至 `/admin`
  - 錯誤處理：驗證失敗則重新渲染表單並提示錯誤

- **`GET /admin/event/<id>/edit` (編輯活動頁面)**
  - 輸入：URL 參數 `id`
  - 處理邏輯：呼叫 `Event.get_by_id(id)`
  - 輸出：將取得的 `event` 傳給 `admin/event_form.html` 作為預設值

- **`POST /admin/event/<id>/edit` (更新活動)**
  - 輸入：URL 參數 `id`，與表單欄位
  - 處理邏輯：呼叫 `event.update()`
  - 輸出：重導向至 `/admin`

- **`POST /admin/event/<id>/delete` (刪除活動)**
  - 輸入：URL 參數 `id`
  - 處理邏輯：呼叫 `event.delete()`
  - 輸出：重導向至 `/admin`

- **`GET /admin/event/<id>/participants` (確認人員名單)**
  - 輸入：URL 參數 `id`
  - 處理邏輯：呼叫 `Event.get_by_id(id)` 及取得其 `registrations`
  - 輸出：渲染 `admin/participants.html`

## 3. Jinja2 模板清單

以下為後續需要建立的 HTML 模板檔案：

- `base.html`: 共用版型（Header, Footer，Flash 訊息區塊）
- `index.html` (繼承 `base.html`): 首頁活動列表
- `event_detail.html` (繼承 `base.html`): 活動細節與報名表單
- `admin/dashboard.html` (繼承 `base.html`): 後台活動管理列表
- `admin/event_form.html` (繼承 `base.html`): 新增與編輯共用表單
- `admin/participants.html` (繼承 `base.html`): 報名人員名單頁面

## 4. 路由骨架程式碼
Python 路由骨架檔案（使用 Blueprint）已建立於 `app/routes/` 資料夾下，詳情請參考原始碼。
