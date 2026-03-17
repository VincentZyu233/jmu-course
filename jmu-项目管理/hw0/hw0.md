# 大学学习与项目管理思维

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/VincentZyu233/jmu-course)
[![Gitee](https://img.shields.io/badge/Gitee-C71D23?style=for-the-badge&logo=gitee&logoColor=white)](https://gitee.com/vincent-zyu/jmu-course)

在大学学习生活，别死记硬背，像做项目一样管它，成长速度直接起飞！

我自己就是这么干的：课程作业、笔记全扔进 Git 仓库管理。比如这个 https://gitee.com/vincent-zyu/jmu-course，把一学期课程拆成文件夹（计算机网络、数值分析、大数据、软件体系结构啥的），每次写笔记、改作业、做实验都 commit + push，当成个人代码库备份+版本回溯。写错了？直接 revert 或 branch 试新思路，超级安心。

平时开发习惯也带进学习：像 winload 用 Rust+Python 双写、Koishi 插件小步迭代（从文本输出 → 加图片渲染 → 实时监控 → 多平台适配），大学课也这样——syllabus 先拉成里程碑，周任务拆 issue 或 TODO list；卡点就 debug（Stack Overflow + 写 demo）；期末复习像"移植插件"，把知识点优化成思维导图或小工具（uni-app 练手那种）；最后"上线"——做个实战项目或考试复盘。

这样刷课从被动变主动，技能像我的插件仓库一样，从 TS/Vue 到 Go/Rust，一点点堆成全栈。大学四年用项目思维管自己，毕业直接不是小白，是能独立搞东西的人！

---

## 工程化学习模式

既然你已经在用 Git 管理 jmu-course 了，那你的大学生活本质上就是一个正在运行的分布式系统。这种"所学即所得"的思维非常硬核，我们可以把这种模式进一步工程化：

### 1. 完善你的"课程仓库（Repo）"规范

别只把 jmu-course 当成云盘，要把它做成一个 Monorepo。

- **Issue Tracking**：把老师布置的作业、甚至是一次期末考，都开成一个 Issue。标记 priority: high 或 deadline: 2026-06。
- **Pull Request**：每次完成一个大作业，通过 PR 的形式合并到主分支。这种"仪式感"能让你直观看到知识的增量。

### 2. 构建"自动化构建（CI/CD）"学习流

既然你玩转了 VitePress 和 Action，完全可以给你的笔记加上 Auto-Deploy。

- 当你在本地通过 Obsidian 或 VS Code 更新了某门专业课的 .md，直接 Push。
- 触发 Action 自动同步到你的个人静态站点。**"写完即发布"**的即时反馈，会极大地刺激你的学习动力，这比单纯存在本地硬盘里要有成就感得多。

### 3. "跨端兼容"你的专业知识

你做过 winload 这种多语言/跨平台的监控工具，学习也一样。

- **底层优化**：基础课（离散、数据结构）是你的 Runtime。
- **上层应用**：专业课是你的 Framework。
- 试着用你熟悉的 Rust 或 Go 去重构课程里的 C/C++ 示例代码。在不同"语言环境"下的迁移过程，才是真正消化知识点的过程。

### 4. 社区贡献与"LTS 服务"

把 jmu-course 保持 Public，本质上是在做开源共建。这不仅是你的备份，也是给学弟学妹留下的 Technical Support。

---

**核心观点**：要把每门课当成一次"版本迭代"，而不是为了拿学分的"一次性脚本"。
