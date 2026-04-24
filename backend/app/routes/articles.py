from flask import Blueprint, request, jsonify
from app import db
from app.models.article import Article
from app.models.tag import Tag
from app.utils.jwt_helper import jwt_required

articles_bp = Blueprint("articles", __name__)

@articles_bp.get("")
def list_articles():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    category_id = request.args.get("category_id", type=int)
    tag_id = request.args.get("tag_id", type=int)
    keyword = request.args.get("keyword", "")

    q = Article.query.filter_by(status="published")
    if category_id:
        q = q.filter_by(category_id=category_id)
    if tag_id:
        q = q.filter(Article.tags.any(id=tag_id))
    if keyword:
        q = q.filter(Article.title.contains(keyword))

    pagination = q.order_by(Article.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "items": [a.to_dict() for a in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "page": page,
    })

@articles_bp.get("/timeline")
def timeline():
    articles = Article.query.filter_by(status="published").order_by(Article.created_at.desc()).all()
    result = {}
    for a in articles:
        year = a.created_at.strftime("%Y")
        result.setdefault(year, []).append({
            "id": a.id,
            "title": a.title,
            "created_at": a.created_at.isoformat(),
        })
    return jsonify(result)

@articles_bp.get("/admin/all")
@jwt_required
def admin_list():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    pagination = Article.query.order_by(Article.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "items": [a.to_dict() for a in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
    })

@articles_bp.get("/<int:aid>")
def get_article(aid):
    a = Article.query.get_or_404(aid)
    if a.status != "published":
        return jsonify({"msg": "not found"}), 404
    a.views += 1
    db.session.commit()
    return jsonify(a.to_dict(full=True))

@articles_bp.post("/admin")
@jwt_required
def create_article():
    data = request.get_json()
    a = Article(
        title=data["title"],
        content=data["content"],
        summary=data.get("summary", ""),
        cover=data.get("cover", ""),
        status=data.get("status", "draft"),
        category_id=data.get("category_id"),
    )
    _sync_tags(a, data.get("tag_ids", []))
    db.session.add(a)
    db.session.commit()
    return jsonify(a.to_dict(full=True)), 201

@articles_bp.put("/admin/<int:aid>")
@jwt_required
def update_article(aid):
    a = Article.query.get_or_404(aid)
    data = request.get_json()
    for field in ("title", "content", "summary", "cover", "status", "category_id"):
        if field in data:
            setattr(a, field, data[field])
    if "tag_ids" in data:
        _sync_tags(a, data["tag_ids"])
    db.session.commit()
    return jsonify(a.to_dict(full=True))

@articles_bp.delete("/admin/<int:aid>")
@jwt_required
def delete_article(aid):
    a = Article.query.get_or_404(aid)
    db.session.delete(a)
    db.session.commit()
    return jsonify({"msg": "deleted"})

def _sync_tags(article, tag_ids):
    article.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
