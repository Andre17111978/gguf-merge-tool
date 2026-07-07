GGUF Merge Tool v10.0
https://badge.fury.io/py/gguf-merge-tool.svg
https://img.shields.io/badge/python-3.8+-blue.svg
https://img.shields.io/badge/License-MIT-yellow.svg

专业的图形界面 + 命令行工具，用于从 Hugging Face 下载、验证和合并分片的 GGUF 模型。

✨ 10.0 版本新功能
功能	说明
修复进度条	在哈希验证和合并操作期间，进度显示平滑且正确
本地文件加载	“本地”按钮允许您选择磁盘上的 GGUF 文件夹，无需下载即可使用
仓库历史记录	仓库输入框中的下拉列表 — 保存最近 10 次查询
🚀 主要功能
下载 来自 Hugging Face 的 GGUF 文件，支持断点续传。

完整性验证 已下载文件的 SHA-256 校验。

合并 使用 llama-gguf-split 将分片合并为一个完整的 GGUF 文件。

分组 按量化和基础文件名对文件进行分组。

多线程 下载（自动检测 CPU 核心数）。

实时预估 下载期间的剩余时间 (ETA) 和速度 (MB/s)。

命令行模式 便于自动化操作。

持久化 跨会话保存令牌和 llama.cpp 路径。

📦 安装
从 PyPI 安装（推荐）
bash
pip install gguf-merge-tool
安装完成后，可以使用以下两个命令：

gguf-merge-gui — 启动图形界面

gguf-merge — 启动命令行模式

从源码安装
bash
git clone https://github.com/Andre17111978/gguf-merge-tool.git
cd gguf-merge-tool
pip install -r requirements.txt
python gguf_merge_tool.py
🖥️ 使用方法（图形界面）
bash
gguf-merge-gui
# 或
python gguf_merge_tool.py
界面分步说明：
字段	说明
仓库 (Repository)	输入 Hugging Face 仓库 ID（例如：unsloth/Qwen3.5-122B-A10B-GGUF）。
历史记录自动保存最近 10 次查询。
分支 (Branch)	通常为 main。
令牌 (Token)	可选，用于私有仓库（格式：hf_xxxxxxxxxxxxxxxxxx）。
下载文件夹	文件保存位置。
llama.cpp 路径	指定包含 llama-gguf-split 的文件夹（合并时需要）。
文件列表	带复选框的 GGUF 文件列表，按量化类型自动分组。
控制按钮：
按钮	功能
加载 (Load)	从仓库获取文件列表。
本地 (Local)	选择磁盘上的 GGUF 文件夹。
全选 / 全部下载	批量操作。
下载 (Download)	下载选中的文件。
验证 (Verify)	检查 SHA-256 哈希值。
合并 (Merge)	合并选中的分片。
⌨️ 使用方法（命令行）
下载指定文件
bash
gguf-merge download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models -f model-00001-of-00003.gguf model-00002-of-00003.gguf
下载整个仓库
bash
gguf-merge download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models
使用令牌下载（私有仓库）
bash
gguf-merge download -r your-username/your-private-model -d ./models -t hf_xxxxxxxxxxxxxxxxxx
合并分片
bash
gguf-merge merge -d ./models -o ./models/merged_model.gguf -f
命令行参数
download 命令：

参数	说明
-d, --dir	保存文件夹（必填）
-r, --repo	仓库 ID（必填）
-b, --branch	分支名称（默认：main）
-t, --token	Hugging Face 令牌
-f, --files	要下载的文件列表
merge 命令：

参数	说明
-d, --dir	分片所在文件夹（必填）
-o, --output	输出文件路径
-f, --force	覆盖已存在的文件
⚙️ 系统要求
Python >= 3.8

依赖项（自动安装）：
huggingface_hub >= 0.20.0

tqdm >= 4.60.0

requests >= 2.28.0

gguf >= 0.1.0（可选，用于读取元数据）

需要额外工具：
llama-gguf-split（从 llama.cpp 发布页面 下载）

🛠️ 故障排除
找不到 llama-gguf-split
从 llama.cpp 发布页面 下载

将其放入 tools/ 文件夹，或在图形界面设置中指定路径

HTTP 401/403（未授权/禁止访问）
输入有效的 Hugging Face 令牌

确保令牌具有访问该仓库的权限

磁盘空间不足
释放空间或更改下载文件夹

可以在代码中修改 DISK_SPACE_MARGIN（默认：1.1 = 预留 10% 空间）

在 Linux 上无法启动图形界面
bash
sudo apt-get install python3-tk  # Debian/Ubuntu
brew install python-tk           # macOS
📝 许可证
采用 MIT 许可证分发。详情请参阅 LICENSE 文件。

🙏 致谢
llama.cpp — 合并工具

Hugging Face — 模型托管平台

社区用户 — 测试和反馈建议

⭐ 支持项目
如果您觉得这个工具有用，请在 GitHub 上给它点个星！

❤️ 为 AI 社区精心打造