from apps.monitor.services.rules import evaluate_violation


def test_violation_when_person_without_helmet():
    det = [{"label": "person", "conf": 0.9}]
    has, types = evaluate_violation(det)
    assert has and "sem_capacete" in types


def test_no_violation_when_person_with_helmet():
    det = [{"label": "person", "conf": 0.9}, {"label": "helmet", "conf": 0.8}]
    has, types = evaluate_violation(det)
    assert not has and types == []
