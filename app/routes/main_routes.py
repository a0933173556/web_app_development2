from flask import render_template, request, redirect, url_for, flash
from . import main_bp
from app.models.event import Event
from app.models.registration import Registration

@main_bp.route('/')
def index():
    """
    處理: GET /
    邏輯: 取得所有開放報名的活動列表
    輸出: 渲染 index.html
    """
    pass

@main_bp.route('/event/<int:event_id>')
def event_detail(event_id):
    """
    處理: GET /event/<id>
    邏輯: 根據 event_id 取得活動詳細資料，若找不到回傳 404
    輸出: 渲染 event_detail.html (含報名表單)
    """
    pass

@main_bp.route('/event/<int:event_id>/register', methods=['POST'])
def register_event(event_id):
    """
    處理: POST /event/<id>/register
    邏輯: 接收表單資料 (name, email, phone)，驗證資料後存入 Registration Model
    輸出: 成功/失敗後設定 flash 訊息，並重導向回 /event/<id>
    """
    pass
