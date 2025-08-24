# /bot_portal/services.py
import os
import hmac
import hashlib
import time
import logging
from flask import session
from .models import EditorModel, AppealModel # <-- 1. Импортируем AppealModel

# ... (Код AuthService остается без изменений) ...
log = logging.getLogger(__name__)

class AuthService:
    # ... (весь код AuthService) ...
    pass

# --- НАЧАЛО ИЗМЕНЕНИЙ ---
class AppealService:
    @staticmethod
    def _format_status(status_code):
        """
        Преобразует код статуса в человекочитаемый текст и CSS-класс для цвета.
        """
        status_map = {
            "collecting": {"text": "Сбор аргументов", "color": "yellow"},
            "reviewing": {"text": "На рассмотрении ИИ", "color": "blue"},
            "closed": {"text": "Закрыто", "color": "green"},
            "closed_after_review": {"text": "Закрыто (Пересмотр)", "color": "green"},
            "closed_invalid": {"text": "Отклонено (Невалидно)", "color": "gray"},
            "review_poll_pending": {"text": "Голосование", "color": "purple"},
        }
        default = {"text": status_code or "Неизвестно", "color": "gray"}
        return status_map.get(status_code, default)

    @staticmethod
    def get_all_appeals_for_display():
        """
        Получает и форматирует список всех апелляций для отображения в панели.
        """
        raw_appeals = AppealModel.get_all()
        formatted_appeals = []
        for appeal in raw_appeals:
            formatted_appeals.append({
                "case_id": appeal['case_id'],
                "decision_text": (appeal['decision_text'] or "Нет данных")[:100] + "...", # Обрезаем длинный текст
                "status": AppealService._format_status(appeal['status']),
                "created_at": appeal['created_at'].strftime("%Y-%m-%d %H:%M") if appeal['created_at'] else "Нет данных"
            })
        return formatted_appeals
# --- КОНЕЦ ИЗМЕНЕНИЙ ---