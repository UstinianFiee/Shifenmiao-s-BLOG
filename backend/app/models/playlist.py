from app import db

class PlaylistItem(db.Model):
    __tablename__ = "playlist"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    artist = db.Column(db.String(128), default="")
    url = db.Column(db.String(512), nullable=False)   # 音频文件路径
    cover = db.Column(db.String(512), default="")     # 封面图路径
    sort = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "url": self.url,
            "cover": self.cover,
            "sort": self.sort,
        }
