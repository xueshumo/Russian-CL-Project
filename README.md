# Russian-CL-Project
## Day4 成果
- 开发工具格检测规则，准确率达100%(存疑)
- 发现主要错误类型：
  1. 形容词工具格误判（如"красивой дорогой"）
  2. 并列结构漏检（如"ножом и вилкой"）
  3. 长距离依赖错误（如"Он говорит, что использовал этим методом"中methodом未被识别）