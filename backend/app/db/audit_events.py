from app.db.models.audit_log import AuditLog


def log_event(db, decision_id, event_type, payload=None):
    event = AuditLog(
        decision_id=decision_id,
        event_type=event_type,
        payload=payload or {},
    )
    db.add(event)
