import json
import requests
from flask import Blueprint, request, jsonify, Response, stream_with_context
from app import db
from app.models.ai_config import AiConfig
from app.models.article import Article
from app.models.category import Category
from app.models.tag import Tag
from app.models.media import Media
from app.utils.jwt_helper import jwt_required

ai_bp = Blueprint("ai", __name__)

def _get_config():
    cfg = AiConfig.query.first()
    if not cfg:
        cfg = AiConfig()
        db.session.add(cfg)
        db.session.commit()
    return cfg

def _call_api(cfg, messages, stream=False, max_tokens=4000):
    headers = {"Authorization": f"Bearer {cfg.api_key}", "Content-Type": "application/json"}
    payload = {"model": cfg.model, "messages": messages, "stream": stream, "max_tokens": max_tokens}
    api_url = cfg.api_base.rstrip("/") + "/chat/completions"
    return requests.post(api_url, headers=headers, json=payload,
                         stream=stream, timeout=120,
                         proxies={"http": None, "https": None})

@ai_bp.get("/config")
@jwt_required
def get_config():
    return jsonify(_get_config().to_dict(hide_key=True))

@ai_bp.put("/config")
@jwt_required
def update_config():
    data = request.get_json()
    cfg = _get_config()
    for field in ("api_base", "api_key", "model", "prompt_template"):
        if field in data and data[field] != "":
            if field == "api_key" and data[field].startswith("*"):
                continue
            setattr(cfg, field, data[field])
    db.session.commit()
    return jsonify(cfg.to_dict(hide_key=True))

@ai_bp.get("/public/analysis")
def public_analysis():
    cfg = _get_config()
    return jsonify({"content": cfg.last_analysis or "", "updated_at": cfg.analysis_updated_at or ""})

@ai_bp.post("/save-analysis")
@jwt_required
def save_analysis():
    data = request.get_json()
    cfg = _get_config()
    cfg.last_analysis = data.get("content", "")
    from datetime import datetime
    cfg.analysis_updated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    db.session.commit()
    return jsonify({"msg": "saved"})

@ai_bp.post("/analyze")
@jwt_required
def analyze():
    cfg = _get_config()
    if not cfg.api_key:
        return jsonify({"msg": "请先配置 API Key"}), 400

    articles = Article.query.filter_by(status="published") \
        .order_by(Article.created_at.desc()).limit(20).all()
    if not articles:
        return jsonify({"msg": "暂无已发布文章，无法分析"}), 400

    article_text = "\n\n".join([
        f"【{a.title}】（{a.created_at.strftime('%Y-%m-%d')}）\n{a.summary or a.content[:200]}"
        for a in articles
    ])
    prompt = cfg.prompt_template.replace("{articles}", article_text)

    def generate():
        try:
            resp = _call_api(cfg, [{"role": "user", "content": prompt}], stream=True, max_tokens=1000)
            if resp.status_code != 200:
                yield f"data: {json.dumps({'error': f'API 错误 {resp.status_code}: {resp.text[:200]}'})}\n\n"
                return
            for line in resp.iter_lines():
                if not line:
                    continue
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    d = line[6:]
                    if d == "[DONE]":
                        yield "data: [DONE]\n\n"
                        return
                    try:
                        chunk = json.loads(d)
                        delta = chunk["choices"][0]["delta"].get("content", "")
                        if delta:
                            yield f"data: {json.dumps({'text': delta})}\n\n"
                    except Exception:
                        pass
        except requests.exceptions.Timeout:
            yield f"data: {json.dumps({'error': '请求超时'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@ai_bp.post("/generate-article")
@jwt_required
def generate_article():
    """
    根据用户描述自动生成文章并发布。
    请求体：
      description: 文章描述，如"帮我写一篇关于Flask学习的文章"
      cover_filename: 封面文件名（媒体库中的文件名，可选）
      category_name: 分类名（不存在则自动创建）
      tag_names: 标签名列表（不存在则自动创建）
      status: draft | published（默认 draft）
    """
    cfg = _get_config()
    if not cfg.api_key:
        return jsonify({"msg": "请先配置 API Key"}), 400

    data = request.get_json()
    description = data.get("description", "").strip()
    if not description:
        return jsonify({"msg": "请输入文章描述"}), 400

    cover_filename = data.get("cover_filename", "").strip()
    category_name = data.get("category_name", "").strip()
    tag_names = [t.strip() for t in data.get("tag_names", []) if t.strip()]
    status = data.get("status", "draft")

    # 1. 构建 prompt，要求 AI 返回 JSON 格式
    system_prompt = (
        "你是一个专业的技术博客写手。用户会给你一个文章主题描述，"
        "请生成一篇高质量的 Markdown 格式博客文章。\n"
        "要求：\n"
        "1. 返回严格的 JSON 格式，不要有任何多余内容\n"
        "2. JSON 结构：{\"title\": \"文章标题\", \"summary\": \"摘要（50字以内）\", \"content\": \"完整Markdown内容\"}\n"
        "3. content 中的 Markdown 要有标题、正文、代码块等丰富格式\n"
        "4. 文章长度适中，1000-3000字"
    )
    user_prompt = f"请根据以下描述生成文章：{description}"

    try:
        resp = _call_api(cfg, [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], stream=False, max_tokens=4000)

        if resp.status_code != 200:
            return jsonify({"msg": f"API 错误 {resp.status_code}: {resp.text[:200]}"}), 500

        result = resp.json()
        raw = result["choices"][0]["message"]["content"].strip()

        # 清理可能的 markdown 代码块包裹
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1]
            if raw.endswith("```"):
                raw = raw.rsplit("```", 1)[0]

        article_data = json.loads(raw)
        title = article_data.get("title", "AI 生成文章")
        summary = article_data.get("summary", "")
        content = article_data.get("content", "")

    except json.JSONDecodeError:
        # AI 没有严格返回 JSON，把整个内容当作文章正文
        title = description[:50]
        summary = ""
        content = raw if 'raw' in dir() else ""
    except Exception as e:
        return jsonify({"msg": f"生成失败：{str(e)}"}), 500

    # 2. 处理封面（从媒体库查找）
    cover_url = ""
    if cover_filename:
        media = Media.query.filter(Media.name.like(f"%{cover_filename}%")).first()
        if not media:
            # 也尝试按 url 匹配
            media = Media.query.filter(Media.url.like(f"%{cover_filename}%")).first()
        if media:
            cover_url = media.url

    # 3. 处理分类（不存在则创建）
    category_id = None
    if category_name:
        cat = Category.query.filter_by(name=category_name).first()
        if not cat:
            cat = Category(name=category_name)
            db.session.add(cat)
            db.session.flush()
        category_id = cat.id

    # 4. 处理标签（不存在则创建）
    tag_objs = []
    for tname in tag_names:
        tag = Tag.query.filter_by(name=tname).first()
        if not tag:
            tag = Tag(name=tname)
            db.session.add(tag)
            db.session.flush()
        tag_objs.append(tag)

    # 5. 创建文章
    article = Article(
        title=title,
        content=content,
        summary=summary,
        cover=cover_url,
        status=status,
        category_id=category_id,
    )
    article.tags = tag_objs
    db.session.add(article)
    db.session.commit()

    return jsonify({
        "msg": "文章生成成功",
        "article": article.to_dict(full=False),
        "created_tags": [t for t in tag_names],
        "created_category": category_name if category_id else None,
    }), 201
