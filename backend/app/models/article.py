from app import db
from datetime import datetime

article_tags = db.Table(
    "article_tags",
    db.Column("article_id", db.Integer, db.ForeignKey("articles.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)

class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=False)       # raw markdown
    summary = db.Column(db.String(512), default="")
    cover = db.Column(db.String(512), default="")      # cover image url
    status = db.Column(db.String(16), default="draft") # draft | published
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    category = db.relationship("Category", backref="articles")
    tags = db.relationship("Tag", secondary=article_tags, backref="articles")

    def to_dict(self, full=False):
        d = {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "cover": self.cover,
            "status": self.status,
            "views": self.views,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "category": {"id": self.category.id, "name": self.category.name} if self.category else None,
            "tags": [{"id": t.id, "name": t.name} for t in self.tags],
        }
        if full:
            d["content"] = self.content
        return d
