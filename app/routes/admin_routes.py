from flask import render_template, request, redirect, url_for, flash
from . import admin_bp
from app.models.event import Event
from app.models.registration import Registration

@admin_bp.route('/')
def dashboard():
    """
    處理: GET /admin
    邏輯: 取得所有活動列表及各自的報名人數統計
    輸出: 渲染 admin/dashboard.html
    """
    pass

@admin_bp.route('/event/new', methods=['GET', 'POST'])
def create_event():
    """
    處理: GET & POST /admin/event/new
    邏輯 (GET): 顯示建立活動的表單
    邏輯 (POST): 接收表單資料並建立新活動 (Event.create)
    輸出: GET 渲染 admin/event_form.html，POST 儲存後重導向至 /admin
    """
    pass

@admin_bp.route('/event/<int:event_id>/edit', methods=['GET', 'POST'])
def edit_event(event_id):
    """
    處理: GET & POST /admin/event/<id>/edit
    邏輯 (GET): 根據 event_id 取得活動資料並代入表單
    邏輯 (POST): 接收表單修改資料並更新活動 (Event.update)
    輸出: GET 渲染 admin/event_form.html，POST 儲存後重導向至 /admin
    """
    pass

@admin_bp.route('/event/<int:event_id>/delete', methods=['POST'])
def delete_event(event_id):
    """
    處理: POST /admin/event/<id>/delete
    邏輯: 根據 event_id 刪除該活動 (Event.delete)
    輸出: 刪除後重導向至 /admin
    """
    pass

@admin_bp.route('/event/<int:event_id>/participants')
def participants_list(event_id):
    """
    處理: GET /admin/event/<id>/participants
    邏輯: 根據 event_id 取得該活動所有報名名單 (registrations)
    輸出: 渲染 admin/participants.html
    """
    pass
