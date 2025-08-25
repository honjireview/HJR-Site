# /bot_portal/services/stats_service.py
import logging
from datetime import datetime, timedelta
# ЗАМЕНА: импортируем модели напрямую из их модулей, а не из пакета
from ..models.appeal_model import AppealModel
from ..models.message_log_model import MessageLogModel
from ..models.rate_limit_model import RateLimitModel

log = logging.getLogger(__name__)

class StatsService:
    @staticmethod
    def get_dashboard_stats():
        """
        Собирает всю необходимую статистику для главной панели управления.
        """
        log.debug("[STATS_SERVICE] Запрос на получение статистики для дашборда...")
        try:
            appeal_stats = AppealModel.get_stats()
            total_logs = MessageLogModel.get_total_count()
            total_ai_requests = RateLimitModel.get_total_count()

            stats = {
                "total_appeals": appeal_stats.get("total", 0),
                "closed_appeals": appeal_stats.get("statuses", {}).get("closed", 0) + appeal_stats.get("statuses", {}).get("closed_after_review", 0),
                "reviewing_appeals": appeal_stats.get("statuses", {}).get("reviewing", 0),
                "total_logs": total_logs,
                "total_ai_requests": total_ai_requests
            }
            log.debug(f"[STATS_SERVICE] Статистика успешно собрана: {stats}")
            return stats
        except Exception as e:
            log.error(f"[STATS_SERVICE] Ошибка при сборе статистики: {e}")
            # Возвращаем пустые данные в случае ошибки, чтобы не сломать страницу
            return {
                "total_appeals": "N/A",
                "closed_appeals": "N/A",
                "reviewing_appeals": "N/A",
                "total_logs": "N/A",
                "total_ai_requests": "N/A"
            }