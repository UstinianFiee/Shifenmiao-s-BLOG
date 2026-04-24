from app import db
from datetime import datetime

class Media(db.Model):
    __tablename__ = "media"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), default="")       # 原始文件名
    url = db.Column(db.String(512), nullable=False)    # 访问路径
    file_type = db.Column(db.String(16), default="image")  # image | video
    caption = db.Column(db.String(512), default="")    # 说明文字
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "file_type": self.file_type,
            "caption": self.caption,
            "created_at": self.created_at.isoformat(),
        }
