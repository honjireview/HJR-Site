# /bot_portal/services/appeal_service.py
import logging
from ..models import AppealModel

log = logging.getLogger(__name__)

class AppealService:
    @staticmethod
    def _format_status(status_code):
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
    def get_all_appeals_for_display(sort_by='created_at', order='desc'):
        log.debug(f"[APPEAL_SERVICE] Запрос на получение всех дел (сортировка: {sort_by} {order})...")
        raw_appeals = AppealModel.get_all(sort_by=sort_by, order=order)
        log.debug(f"[APPEAL_SERVICE] Получено {len(raw_appeals)} дел из БД.")

        formatted_appeals = []
        for appeal in raw_appeals:
            formatted_appeals.append({
                "case_id": appeal['case_id'],
                "decision_text": (appeal['decision_text'] or "Нет данных")[:100] + "...",
                "status": AppealService._format_status(appeal['status']),
                "created_at": appeal['created_at'].strftime("%Y-%m-%d %H:%M") if appeal['created_at'] else "Нет данных"
            })
        log.debug("[APPEAL_SERVICE] Форматирование дел для отображения завершено.")
        return formatted_appeals

    @staticmethod
    def get_appeal_details(case_id):
        log.debug(f"[APPEAL_SERVICE] Запрос на получение деталей дела #{case_id}...")
        appeal_data = AppealModel.find_by_id(case_id)

        if not appeal_data:
            log.warning(f"[APPEAL_SERVICE] Дело #{case_id} не найдено в БД.")
            return None

        applicant_answers = appeal_data.get('applicant_answers') or {}
        applicant_position = {
            'main_arguments': appeal_data.get('applicant_arguments', 'Не указано'),
            'violated_rule': applicant_answers.get('q1', 'Не указано'),
            'desired_outcome': applicant_answers.get('q2', 'Не указано'),
            'context': applicant_answers.get('q3', 'Не указано')
        }

        council_answers = appeal_data.get('council_answers') or []
        council_position = []
        for answer in council_answers:
            council_position.append({
                'responder': answer.get('responder_info', 'Редактор Совета'),
                'counter_arguments': answer.get('main_arg', 'Не указано'),
                'rule_basis': answer.get('q1', 'Не указано'),
                'applicant_assessment': answer.get('q2', 'Не указано')
            })

        formatted_details = {
            "case_id": appeal_data['case_id'],
            "decision_text": appeal_data.get('decision_text', 'Нет данных'),
            "status": AppealService._format_status(appeal_data['status']),
            "created_at": appeal_data['created_at'].strftime("%Y-%m-%d %H:%M UTC") if appeal_data.get('created_at') else "Нет данных",
            "applicant_position": applicant_position,
            "council_position": council_position,
            "ai_verdict": appeal_data.get('ai_verdict', 'Вердикт еще не вынесен.')
        }
        log.debug(f"[APPEAL_SERVICE] Детали для дела #{case_id} успешно отформатированы.")
        return formatted_details