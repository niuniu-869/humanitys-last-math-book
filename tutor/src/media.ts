/** manim 产物的命名约定：宿主端（渲染、/api/hlmb/media）和浏览器端（图卡）共用，不依赖 Node。 */

/** 媒体文件名：24 位十六进制 id，加上可选的 `-sheet`，扩展名 png 或 mp4。 */
export const MEDIA_FILE = /^[0-9a-f]{24}(-sheet)?\.(png|mp4)$/

/** 图卡从工具结果里认出媒体文件的标记行：`[manim <id> <png|mp4> <宽>x<高>]`。 */
export const MEDIA_MARK = /^\[manim ([0-9a-f]{24}) (png|mp4) (\d+)x(\d+)\]$/m

/** 回执里的分步说明行：`[step <开始秒数>] <文字>`，图卡把它们列在图下方。 */
export const STEP_MARK = /^\[step (\d+(?:\.\d+)?)\] (.+)$/gm
