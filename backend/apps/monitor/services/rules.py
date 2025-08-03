def evaluate_violation(detections):
    """
    detections: [{"label":"person","conf":0.9,"xyxy":[...]}, {"label":"helmet",...}]
    Regra simples: se há 'person' e NÃO há 'helmet' -> 'sem_capacete'
    """
    labels = [d.get("label") for d in detections]
    has_person = "person" in labels
    has_helmet = "helmet" in labels
    violations = []
    if has_person and not has_helmet:
        violations.append("sem_capacete")
    return (len(violations) > 0), violations
