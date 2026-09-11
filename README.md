# ISO/IEC 27001 Lead Auditor Mock Exam Simulator

一個為 ISO/IEC 27001 主導稽核員考試而設計的模擬考試網站。

## 功能特性

✅ 完整的模擬考試系統
✅ 章節練習模式
✅ 自動批改和成績評估
✅ 用戶進度追蹤
✅ 響應式設計（桌面、平板、手機）
✅ 管理後台

## 技術堆棧

**後端:**
- Django 4.2+
- Django REST Framework
- PostgreSQL
- Python 3.10+

**前端:**
- React 18+
- Tailwind CSS
- Axios
- React Router

**部署:**
- Docker & Docker Compose
- GitHub Actions (CI/CD)

## 快速開始

### 前提條件
- Docker & Docker Compose
- Python 3.10+ (本地開發)
- Node.js 16+ (本地開發)

### 使用 Docker 運行

```bash
# 複製倉庫
git clone https://github.com/Maxium1997/iso27001-exam-simulator.git
cd iso27001-exam-simulator

# 構建並啟動容器
docker-compose up --build

# 執行數據庫遷移
docker-compose exec backend python manage.py migrate

# 建立超級用戶
docker-compose exec backend python manage.py createsuperuser
```

訪問:
- 前端: http://localhost:3000
- 後端 API: http://localhost:8000
- 管理後台: http://localhost:8000/admin

## 項目結構

```
iso27001-exam-simulator/
├── backend/              # Django 後端
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/          # 項目配置
│   ├── apps/            # Django 應用
│   │   ├── users/       # 用戶管理
│   │   ├── exams/       # 考試管理
│   │   └── questions/   # 題目管理
│   └── tests/           # 測試
├── frontend/             # React 前端
│   ├── public/
│   ├── src/
│   │   ├── components/  # React 組件
│   │   ├── pages/       # 頁面
│   │   ├── services/    # API 服務
│   │   └── App.js
│   └── package.json
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

## 開發指南

### 後端開發

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

### 前端開發

```bash
cd frontend
npm install
npm start
```

## API 文檔

API 文檔可在 http://localhost:8000/api/docs 查看 (使用 drf-spectacular)

## 貢獻指南

1. Fork 本倉庫
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推動到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 許可證

MIT License - 詳見 [LICENSE](LICENSE) 文件

## 聯絡方式

如有任何問題或建議，請開啟 Issue 或 Pull Request。
