# Agentic Gamedev Skills

[English](README.md) | 日本語

このリポジトリは、ゲーム開発と agentic workflow の研究から抽出した agent skill 集である。各 skill は `.agents/skills/` 以下に置き、`SKILL.md` を入口とする。必要に応じて `references/`、`assets/`、`scripts/`、`tools/`、`agents/` を含む。

主な用途は、ミニゲームの制作である。一ボタン操作、強い視覚フィードバック、手続き型音声、テレメトリによる調整、任意のピクセルアート素材生成を扱う。補助的に、skill 抽出、プロンプトや工程のレビュー、英日文書の自然化も扱う。

## 使い方

- skill 名を指定するか、タスク内容を `description` にマッチさせて使う。
- 各 `SKILL.md` をその機能の標準手順とする。
- リポジトリ管理ルールは `AGENTS.md` に従う。

## Skill 作成規約

ローカル skill は、実用上可能な範囲で [Anthropic の Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) に従う。

- 名前は小文字英数字とハイフンを使う。
- 新しいローカル skill 名は `designing-mini-games` のような gerund 形式を優先する。
- `description` は、何をする skill か、いつ使うかを三人称で書く。
- `SKILL.md` は簡潔にし、必要な詳細は `references/`、`assets/`、`scripts/`、`tools/`、`agents/` に置く。

外部から取り込む skill は、上流の名前と構成を維持してよい。

## 同梱 Skill

### ゲーム設計

| Skill                        | 用途                                                                                                       |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `designing-mini-games`       | 小規模ゲームのルール、操作、得点、危険、報酬、終了条件を設計する。放置、長押し固定、連打の最適化を防ぐ。   |
| `designing-one-button-games` | タップ、長押し、リリースを使う一ボタンミニゲームを設計する。新規性、リスクと報酬、短い難度曲線を重視する。 |
| `verifying-turn-based-games` | 二人用の厳密な交互ターンゲームを、純粋関数エンジン契約と bot ladder、緊張度、判断密度で検証する。          |

### ゲーム実装

| Skill                            | 用途                                                                                                              |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `scaffolding-godot-mini-games`   | Godot 4.2+ ミニゲームの最小構成を作る。Web export、テスト、テレメトリ、手続き型音声を含む。                       |
| `running-headless-godot`         | Godot の headless CLI、ログ、スクリプトによるシーン編集、テスト、Web export を再現可能にする。                    |
| `developing-with-crisp-game-lib` | `crisp-game-lib` のブラウザミニゲームを実装または修復する。セットアップ、ループ、描画順、衝突、得点、検証を扱う。 |

### ゲーム演出

| Skill                             | 用途                                                                                                  |
| --------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `directing-game-visuals`          | HUD 説明に頼らず、視覚階層、パレット役割、画面構成、イベントフィードバックを定義する。                |
| `maximizing-game-feel`            | squash/stretch、傾き、パーティクル、軌跡、ヒット演出で操作感を高める。                                |
| `creating-godot-procedural-audio` | Godot の組み込み API で手続き型音声を設計・実装する。ゲームイベントや状態変化ごとに音を分ける。       |
| `styling-web-game-typography`     | 配布ゲーム向けの読みやすくライセンス上問題ないタイポグラフィを実装する。Godot 4.2+ の実装例を含む。   |
| `generating-dot-assets`           | 画像生成、クロマキー除去、ピクセル化、キャンバス調整、検証により透明 PNG のピクセルアート素材を作る。 |

### 評価と調整

| Skill                         | 用途                                                                                   |
| ----------------------------- | -------------------------------------------------------------------------------------- |
| `evaluating-gameplay-balance` | テレメトリでゲームバランスを評価する。単調な方策と探索的または意図した方策を比較する。 |

### Agent Workflow

| Skill                     | 用途                                                                                                     |
| ------------------------- | -------------------------------------------------------------------------------------------------------- |
| `extracting-agent-skills` | 完了、停止、放棄、失敗したプロジェクトから再利用可能な手順、検証ループ、デバッグ法、判断規則を抽出する。 |
| `critiquing-own-response` | 直前の応答を構造的に自己批判する。前提、論理、AI 特有の失敗、リスク、信頼度を点検する。                  |

### 文書とローカライズ

| Skill                             | 用途                                                                           |
| --------------------------------- | ------------------------------------------------------------------------------ |
| `humanizing-bilingual-ai-writing` | 英語・日本語の AI 的な文章を自然な文に直す。事実、意図、読者、英日整合を保つ。 |

## 補助ディレクトリ

- `references/`: 詳細ガイド、チェックリスト、設計テンプレート、実装パターン。
- `assets/`: 再利用可能なテンプレート、Godot script、フォント、素材。
- `scripts/`: 素材生成、検証、関連 workflow の自動化。
- `tools/`: 補助ツール。主に安全な headless Godot 作業用。
- `agents/`: skill 用の任意のモデル別・agent 別設定。

## 外部 Skill 参照

次の skill は他リポジトリから取り込む。`.gitignore` に含め、ローカル利用してもこのリポジトリにはコミットしない。取得には `tools/install-external-skills.sh` を使う。引数で対象名を指定できる。

- `empirical-prompt-tuning`: prompt、skill、slash command、`AGENTS.md` 形式の指示を評価・改善する反復手法。Source: https://github.com/mizchi/skills/blob/main/empirical-prompt-tuning/SKILL.md
- `karpathy-guidelines`: coding agent 向けの簡潔、限定的、前提明示、検証重視の指針。Source: https://github.com/forrestchang/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md
- `develop-web-game`: ブラウザ・canvas ゲーム向けの Playwright 検証つき反復 workflow。非 Godot Web game の参考に使う。Source: https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/creative-design/develop-web-game
- `godot-master`: `gd-agentic-skills` の Godot 4 アーキテクチャと実装リファレンス。必要時だけ使う。`install-external-skills.sh` は意図的に自動取得しない。Source: https://github.com/thedivergentai/gd-agentic-skills
- `systematic-debugging`: バグ、テスト失敗、想定外挙動に対する根本原因優先のデバッグ workflow。Source: https://github.com/mxyhi/ok-skills/blob/main/systematic-debugging/SKILL.md

## リポジトリツール

- `tools/install-external-skills.sh`: 外部 skill を `.agents/skills/<name>/` に取得する。
- `tools/check-readme-skills.sh`: `.agents/skills/` の skill ディレクトリと README の記載を照合する。不一致なら非ゼロ終了する。
