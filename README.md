# astrbot_plugin_wordlimit

AstrBot 插件 — 自动限制 LLM 回复字数。

当 LLM 回复的字符数超过设定阈值时，自动调用 LLM 将内容精简到字数范围内，保留核心信息。

## 功能

- 在每次 LLM 回复后自动检查字符数
- 超过限制时调用指定的 LLM 提供商缩短回复
- 可自定义最大字符数、LLM 提供商、精简提示词
- 支持在 AstrBot 管理面板中可视化配置

## 配置项

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `enabled` | bool | `true` | 是否启用字数限制功能 |
| `max_char_count` | int | `40` | 最大字符数，超过此值将触发缩短 |
| `provider_id` | string | 空 | 用于缩短文本的 LLM 提供商，留空则使用当前会话默认提供商 |
| `summary_prompt` | text | (内置提示词) | 缩短回复时发送给 LLM 的系统提示词 |

## 工作原理

1. 通过 `on_llm_response` 钩子拦截 LLM 回复
2. 检查回复文本的字符数是否超过 `max_char_count`
3. 若超过，构造精简请求发送给指定的 LLM 提供商
4. 将精简后的文本替换原始回复
