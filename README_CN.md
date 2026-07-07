GGUF Merge Tool v9.2

用于从Hugging Face下载、验证和合并分片GGUF模型的专业GUI + CLI工具。
目录

    功能特点

    快速开始

    安装

    CLI使用

    GUI使用

    配置

    系统要求

    故障排除

    性能建议

    技术细节

    许可证

    致谢

    支持

功能特点

现代化GUI - 基于Tkinter的界面，支持滚动文件列表和鼠标滚轮

智能分组 - 根据量化类型自动分组文件 (Q4_K_M, Q5_K_S等)

断点续传 - HTTP Range请求，智能降级保护 (200 vs 206处理)

并行下载 - 可配置线程数 (自动检测CPU核心)

哈希验证 - 使用HF LFS元数据验证SHA256

智能合并 - 使用llama-gguf-split工具

CLI支持 - download和merge子命令，便于自动化

智能检测 - 自动在常见位置查找llama-gguf-split

路径持久化 - 保存llama.cpp路径，跨会话使用

重试逻辑 - 自动重试，指数退避 (3次尝试)

实时ETA - 显示速度(MB/s)和预计剩余时间

多语言 - 支持6种语言文档
快速开始
Windows

安装依赖:
pip install huggingface_hub tqdm requests

从以下地址下载llama-gguf-split: https://github.com/ggerganov/llama.cpp/releases

运行工具:
python gguf_merge_tool.py
Linux / macOS

安装依赖:
pip install huggingface_hub tqdm requests

运行工具:
python3 gguf_merge_tool.py
安装
从源码安装 (推荐)

克隆仓库:
git clone https://github.com/yourusername/gguf-merge-tool.git
cd gguf-merge-tool

安装依赖:
pip install -r requirements.txt

运行工具:
python src/gguf_merge_tool.py
从PyPI安装 (即将推出)

pip install gguf-merge-tool
gguf-merge-gui
Windows用户: 需要二进制文件

从llama.cpp版本下载llama-gguf-split.exe
放置在以下位置之一:

    tools/llama-gguf-split.exe

    bin/llama-gguf-split.exe

    或在GUI设置中指定路径

CLI使用
下载特定文件

python src/gguf_merge_tool.py download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models -f Qwen3.5-122B-A10B-Q4_K_M-00001-of-00008.gguf Qwen3.5-122B-A10B-Q4_K_M-00002-of-00008.gguf
下载整个仓库

python src/gguf_merge_tool.py download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models
使用认证下载 (私有仓库)

python src/gguf_merge_tool.py download -r your-username/your-private-model -d ./models -t hf_xxxxxxxxxxxxxxxxxx
合并分片

python src/gguf_merge_tool.py merge -d ./models -o ./models/merged_model.gguf -f
CLI参数参考

命令: download
-d, --dir - 保存文件的目录 - 必填: 是
-r, --repo - Hugging Face仓库ID - 必填: 是
-b, --branch - 仓库分支 (默认: main) - 必填: 否
-t, --token - HF访问令牌 - 必填: 否
-f, --files - 要下载的文件列表 - 必填: 否

命令: merge
-d, --dir - 包含分片的目录 - 必填: 是
-o, --output - 输出文件路径 - 必填: 否
-f, --force - 覆盖现有文件 - 必填: 否
GUI使用
步骤1: 加载仓库

输入Hugging Face仓库ID (例如: unsloth/Qwen3.5-122B-A10B-GGUF)
输入分支 (默认: main)
输入HF令牌 (私有仓库需要)
点击"加载"按钮
步骤2: 选择文件

文件自动按量化类型分组
点击"全选"选择所有文件
或使用复选框选择单个文件
步骤3: 下载

点击"下载"或"全部下载"
实时监控进度:

    进度条显示百分比

    状态栏显示: [1/4] filename.gguf: 45% | 4.5 MB/s | ETA: 2h 15m

步骤4: 验证 (可选但推荐)

点击"验证"按钮
工具根据HF元数据验证SHA256哈希
如果所有哈希匹配则显示成功消息
步骤5: 合并 (可选)

选择至少2个分片 (复选框)
点击"合并"按钮
工具调用llama-gguf-split --merge
输出文件以正确的基名保存
配置
llama.cpp路径

在GUI中找到"Path to llama.cpp":
点击"查找"自动检测
或点击"浏览"手动选择
路径保存到llama_path.txt以便跨会话使用
线程设置

修改代码中的JOBS常量 (默认: min(4, os.cpu_count() or 2)):
在gguf_merge_tool.py中
JOBS = min(4, os.cpu_count() or 2) - 更改此值
磁盘空间余量

更改DISK_SPACE_MARGIN (默认: 1.1 = 10%余量):
DISK_SPACE_MARGIN = 1.1
下载块大小

更改CHUNK_SIZE (默认: 1 MB):
CHUNK_SIZE = 1024 * 1024
系统要求

Python >= 3.8
huggingface_hub >= 0.20.0
tqdm >= 4.60.0
requests >= 2.28.0
gguf >= 0.1.0 (可选，用于读取元数据)
llama-gguf-split (来自llama.cpp)
验证安装

python -c "import huggingface_hub, tqdm, requests; print('所有依赖已安装')"
故障排除
llama-gguf-split未找到

从llama.cpp版本下载
放置在tools/文件夹或在GUI中指定路径
HTTP 401 Unauthorized或HTTP 403 Forbidden

输入您的Hugging Face令牌
确保令牌对仓库有读取权限
令牌格式: hf_xxxxxxxxxxxxxxxxxx
磁盘空间不足

释放磁盘空间 (合并需要10%余量)
更改下载目录到其他驱动器
使用DISK_SPACE_MARGIN调整余量
下载卡在0%

检查网络连接
验证令牌是否正确
检查仓库是否为私有
检查仓库是否存在
恢复后文件损坏

工具内置Range降级保护
如果服务器不支持Range (返回200而不是206)，从头开始下载
这是为了防止文件损坏
GUI无法启动

检查Tkinter是否已安装 (通常随Python一起安装)
在Linux上: sudo apt-get install python3-tk
在macOS上: brew install python-tk
性能建议

许多小文件 - 保持默认线程(4)
少数大文件 - 增加线程到8
网络慢 - 减少线程到2
快速NVMe SSD - 保持默认或增加
网络中断 - 工具自动恢复下载
技术细节
下载流程

从HF仓库获取文件列表及其大小和哈希值
用户选择要下载的文件
检查磁盘空间 - 不足则中止
使用Range请求并行下载并支持断点续传
智能Range降级处理 (200 vs 206)
实时进度和速度计算
下载后SHA256验证
通过llama-gguf-split合并
ETA计算

ETA = (总字节 - 已下载字节) / 当前速度
支持的量化类型

F16, F32, Q8_0, Q6_K, Q5_K_M, Q5_K_S, Q4_K_M, Q4_K_S, Q3_K_M, Q3_K_S, Q2_K, IQ4_XS, IQ3_XS, IQ2_XS, IQ1_S
许可证

MIT许可证 - 详见LICENSE文件。
致谢

llama.cpp提供的合并工具
Hugging Face提供的模型托管
Python Tkinter提供的GUI
支持

问题反馈: GitHub Issues
讨论: GitHub Discussions
为项目加星

如果您觉得这个工具有用，请在GitHub上给它一颗星！

为AI社区献上❤️