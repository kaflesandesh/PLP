from datetime import datetime
from back.system_utilities.dbmanage import get_db, Log
from back.system_utilities.user import User

class System:
    def __init__(self, db):
        self.db = db

    def log_activity(self, user_id, activity_type, description):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log = Log(timestamp=timestamp, user_id=user_id, activity_type=activity_type, description=description)
        self.db.add(log)
        self.db.commit()

    def get_logs(self):
        return self.db.query(Log).all()

    def system_diagnostics(self):
        diagnostics = {
            "user_count": self.db.query(User).count(),
            "log_count": self.db.query(Log).count(),
            "last_log": self.db.query(Log).order_by(Log.timestamp.desc()).first()
        }
        return diagnostics

    def report_issue(self, user_id, description):
        self.log_activity(user_id, 'bug_report', description)
        return "Issue reported successfully"

    def get_bug_reports(self):
        return self.db.query(Log).filter(Log.activity_type == 'bug_report').all()
