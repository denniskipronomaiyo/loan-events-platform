from app.services.loan_event_service import get_events_by_application


def test_empty_events():
    class MockDB:
        def query(self, model):
            return self

        def filter(self, *args):
            return self

        def order_by(self, *args):
            return self

        def all(self):
            return []

    db = MockDB()
    result = get_events_by_application(db, "fake-id")

    assert result == []