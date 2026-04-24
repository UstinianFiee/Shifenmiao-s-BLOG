from app import db

class AiConfig(db.Model):
    __tablename__ = "ai_config"
    id = db.Column(db.Integer, primary_key=True)
    api_base = db.Column(db.String(512), default="https://api.openai.com/v1")
    api_key = db.Column(db.String(512), default="")
    model = db.Column(db.String(128), default="gpt-3.5-turbo")
    prompt_template = db.Column(db.Text, default=(
        "你是一个博客分析助手。以下是博主最近发布的文章摘要，请根据这些内容分析博主最近的状态、"
        "关注的话题、情绪倾向，并给出一段温暖有趣的近况总结（200字以内，中文）。\n\n{articles}"
    ))
    last_analysis = db.Column(db.Text, default="")        # 最近一次分析结果
    analysis_updated_at = db.Column(db.String(32), default="")  # 更新时间

    def to_dict(self, hide_key=True):
        return {
            "api_base": self.api_base,
            "api_key": ("*" * 8 + self.api_key[-4:]) if hide_key and self.api_key else self.api_key,
            "model": self.model,
            "prompt_template": self.prompt_template,
            "last_analysis": self.last_analysis,
            "analysis_updated_at": self.analysis_updated_at,
        }
