# /bot_portal/services/stats_service.py
import logging
from datetime import datetime, timedelta
from ..models.message_log_model import MessageLogModel
from ..models.rate_limit_model import RateLimitModel
from .appeal_service import get_appeals_stats

logger = logging.getLogger(__name__)

class StatsService:
    @staticmethod
    def get_dashboard_stats():
        logger.debug("[STATS_SERVICE] Запрос на получение статистики для дашборда...")
        try:
            appeals_stats = get_appeals_stats()
            # ... existing code ...
            # Здесь далее используйте MessageLogModel и RateLimitModel по вашей логике,
            # а appeals_stats берите из сервиса:
            # total = appeals_stats["total"], statuses = appeals_stats["statuses"]
            return {
                "total_appeals": appeals_stats["total"],
                "closed_appeals": appeals_stats["statuses"].get("closed", 0),
                "reviewing_appeals": appeals_stats["statuses"].get("reviewing", 0),
                # заглушки/пример: подставьте вашу фактическую логику для логов и ai-запросов
                "total_logs": MessageLogModel.count_all() if hasattr(MessageLogModel, "count_all") else 0,
                "total_ai_requests": RateLimitModel.count_requests_last_days(30) if hasattr(RateLimitModel, "count_requests_last_days") else 0,
            }
        except Exception as e:
            logger.error(f"[STATS_SERVICE] Ошибка при сборе статистики: {e}")
            raise