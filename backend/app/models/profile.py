from app import db

class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), default="博主")
    bio = db.Column(db.String(512), default="热爱技术，热爱生活。")
    avatar = db.Column(db.String(512), default="")  # url

    def to_dict(self):
        return {"nickname": self.nickname, "bio": self.bio, "avatar": self.avatar}
