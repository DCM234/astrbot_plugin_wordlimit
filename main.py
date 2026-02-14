from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import LLMResponse
from astrbot.api import AstrBotConfig, logger


@register("astrbot_plugin_wordlimit","lingyu","LLM 回复字数限制插件，超过设定字数自动缩短","0.1.0",)
class WordLimitPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    @filter.on_llm_response()
    async def on_llm_response(self, event: AstrMessageEvent, resp: LLMResponse):
        '''LLM 回复后检查字数，超限则自动缩短'''
        if not self.config.get("enabled", True):
            return

        max_char_count = self.config.get("max_char_count", 500)
        text = resp.completion_text

        if not text or len(text) <= max_char_count:
            return

        logger.info(
            f"[WordLimit] 回复字数 {len(text)} 超过限制 {max_char_count}，正在缩短..."
        )

        # 确定使用的 LLM 提供商
        provider_id = self.config.get("provider_id", "")
        if not provider_id:
            provider_id = await self.context.get_current_chat_provider_id(
                umo=event.unified_msg_origin
            )

        summary_prompt = self.config.get("summary_prompt", "")
        user_prompt = f"请将以下文本精简到 {max_char_count} 字以内：\n\n{text}"

        try:
            llm_resp = await self.context.llm_generate(
                chat_provider_id=provider_id,
                prompt=user_prompt,
                system_prompt=summary_prompt,
            )
            shortened = llm_resp.completion_text
            if shortened:
                resp.completion_text = shortened
                logger.info(
                    f"[WordLimit] 缩短完成，字数: {len(text)} -> {len(shortened)}"
                )
        except Exception as e:
            logger.error(f"[WordLimit] 缩短回复时出错: {e}")
