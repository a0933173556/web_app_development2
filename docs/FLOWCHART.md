# 流程圖與路由設計 (Flowchart) - 活動報名系統

根據產品需求文件 (PRD) 與系統架構文件 (Architecture)，以下規劃了使用者操作流程、系統運作序列，以及功能與路由的對照表。

## 1. 使用者流程圖 (User Flow)

本系統有兩種主要使用者：「一般參與者」與「計畫經理人（管理員）」。

### 一般參與者流程

```mermaid
flowchart LR
    A([開啟網站首頁]) --> B[瀏覽活動列表]
    B --> C[點擊感興趣的活動]
    C --> D[查看活動詳細說明]
    D --> E{是否報名？}
    E -->|是| F[填寫報名資料]
    F --> G[送出表單]
    G --> H([報名成功提示與返回首頁])
    E -->|否| B
```

### 計畫經理人 (管理員) 流程

```mermaid
flowchart LR
    A([進入後台]) --> B{是否已登入？}
    B -->|否| C[登入頁面]
    C --> B
    B -->|是| D[後台總覽 Dashboard]
    D --> E{要執行什麼操作？}
    
    E -->|建立新活動| F[填寫活動內容表單]
    F --> G[送出儲存] --> D
    
    E -->|檢視或編輯活動| H[點擊現有活動]
    H --> I[編輯活動內容] --> G
    
    E -->|查看報名狀況| J[檢視報名統計人數]
    J --> K[點擊進入確認人員名單]
    K --> D
```

## 2. 系統序列圖 (Sequence Diagram)

以下以 **「參與者提交活動報名」** 的情境為例，說明從瀏覽器發出請求到資料存入 SQLite 的完整運作流程。

```mermaid
sequenceDiagram
    actor User as 參與者
    participant Browser as 瀏覽器
    participant Flask as Flask (Route & Controller)
    participant Model as SQLAlchemy (Registration Model)
    participant DB as SQLite (Database)

    User->>Browser: 在活動頁面填寫報名資料並點擊送出
    Browser->>Flask: POST /event/1/register (夾帶表單資料)
    
    Flask->>Flask: 1. 驗證表單資料 (如必填欄位)
    
    alt 資料格式錯誤
        Flask-->>Browser: 回傳錯誤訊息與原表單頁面
        Browser-->>User: 顯示錯誤提示，請重新填寫
    else 資料正確
        Flask->>Model: 2. 建立 Registration 物件
        Model->>DB: 3. 執行 INSERT INTO registrations...
        DB-->>Model: 4. 資料庫寫入成功
        Model-->>Flask: 回傳建立成功狀態
        
        Flask->>Flask: 5. 設定 Flash 成功訊息
        Flask-->>Browser: 6. 重導向 (Redirect) 至首頁或成功頁
        Browser-->>User: 顯示「報名成功」提示
    end
```

## 3. 功能與路由對照表 (Route Map)

以下列出所有 PRD 提到的核心功能，以及對應的 URL 路徑與 HTTP 方法。

### 前台 (一般參與者)

| 功能說明 | HTTP 方法 | URL 路徑 | 負責的 View/Controller |
| :--- | :---: | :--- | :--- |
| 首頁 (活動列表) | `GET` | `/` | `main_routes.index` |
| 檢視活動詳細說明 | `GET` | `/event/<id>` | `main_routes.event_detail` |
| 送出報名資料 | `POST` | `/event/<id>/register` | `main_routes.register_event` |

### 後台 (計畫經理人)

| 功能說明 | HTTP 方法 | URL 路徑 | 負責的 View/Controller |
| :--- | :---: | :--- | :--- |
| 後台總覽 (含統計人數) | `GET` | `/admin` | `admin_routes.dashboard` |
| 建立活動表單頁面 | `GET` | `/admin/event/new` | `admin_routes.create_event` |
| 送出建立活動 | `POST` | `/admin/event/new` | `admin_routes.create_event` |
| 編輯活動表單頁面 | `GET` | `/admin/event/<id>/edit` | `admin_routes.edit_event` |
| 送出編輯活動 | `POST` | `/admin/event/<id>/edit` | `admin_routes.edit_event` |
| 刪除/下架活動 | `POST` | `/admin/event/<id>/delete` | `admin_routes.delete_event` |
| 確認報名人員名單 | `GET` | `/admin/event/<id>/participants`| `admin_routes.participants_list` |

> **備註**：所有的 `/admin` 路由未來都應加上 `@login_required` 裝飾器來保護後台安全。
