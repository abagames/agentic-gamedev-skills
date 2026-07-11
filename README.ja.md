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
| [`designing-mini-games`](.agents/skills/designing-mini-games/SKILL.md)             | 任意の入力構成(タップ、長押し、リリースの一ボタンゲームを含む)のミニゲームのルール、操作、得点、危険、難度曲線を設計する。放置、長押し固定、連打の最適化を防ぐ。 |
| [`designing-minimal-game-rules`](.agents/skills/designing-minimal-game-rules/SKILL.md) | 抽象的なゲーム設計の種から、離散状態の最小ルール体系を作る。対立軸の候補生成、単純戦略による攻撃、最小核への削減を行う。 |
| [`generating-retro-arcade-concepts`](.agents/skills/generating-retro-arcade-concepts/SKILL.md) | 1978〜1983 年代の固定画面アーケードゲームコンセプトを複数一括生成・評価し、上位コンセプトの実装仕様を書く。 |
| [`verifying-turn-based-games`](.agents/skills/verifying-turn-based-games/SKILL.md) | 二人用の厳密な交互ターンゲームを、純粋関数エンジン契約と bot ladder、緊張度、判断密度で検証する。          |

### ゲーム実装

| Skill                            | 用途                                                                                                              |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| [`scaffolding-godot-mini-games`](.agents/skills/scaffolding-godot-mini-games/SKILL.md)     | Godot 4.2+ ミニゲームの最小構成を作る。Web export、テスト、テレメトリ、手続き型音声を含む。                       |
| [`running-headless-godot`](.agents/skills/running-headless-godot/SKILL.md)                 | Godot の headless CLI、ログ、スクリプトによるシーン編集、テスト、Web export を再現可能にする。                    |
| [`developing-with-crisp-game-lib`](.agents/skills/developing-with-crisp-game-lib/SKILL.md) | `crisp-game-lib` のブラウザミニゲームを実装または修復する。セットアップ、ループ、描画順、衝突、得点、検証を扱う。 |
| [`arcadifying-mini-games`](.agents/skills/arcadifying-mini-games/SKILL.md) | 動作確認済みのミニゲームに、ラウンド構造、儀式画面（READY・クリア・ミス・ゲームオーバー）、スコア経済（エクステンド、イニシャル入力、ハイスコア表）、アトラクトモードを加え、完成したアーケードゲームに仕上げる。 |
| [`implementing-gameplay-invariants`](.agents/skills/implementing-gameplay-invariants/SKILL.md) | ゲーム設計上の約束を、エンジン非依存の実装不変条件と検証項目に変換する。放置、長押し固定、連打、反復得点の優位を防ぐ。 |
| [`smoke-testing-web-games`](.agents/skills/smoke-testing-web-games/SKILL.md) | ブラウザゲームを headless で起動し、放置と入力バーストを与えて console エラー・未捕捉例外・クラッシュを検出する。モックやシミュレータは通るがブラウザで落ちるコードを機械検出する。 |
| [`probing-web-game-mechanics`](.agents/skills/probing-web-game-mechanics/SKILL.md) | 稼働中の headless ブラウザにゲーム状態を注入し、フェーズ遷移、得点式、ゲート、リセットが仕様どおりかを検証する。スモークテスト（動作健全性）とバランス評価（プレイ品質）の中間層を担う。 |

### ゲーム演出

| Skill                             | 用途                                                                                                  |
| --------------------------------- | ----------------------------------------------------------------------------------------------------- |
| [`directing-game-visuals`](.agents/skills/directing-game-visuals/SKILL.md)                   | HUD 説明に頼らず、視覚階層、パレット役割、画面構成、イベントフィードバックを定義する。                |
| [`maximizing-game-feel`](.agents/skills/maximizing-game-feel/SKILL.md)                       | squash/stretch、傾き、パーティクル、軌跡、ヒット演出で操作感を高める。                                |
| [`creating-godot-procedural-audio`](.agents/skills/creating-godot-procedural-audio/SKILL.md) | Godot の組み込み API で手続き型音声を設計・実装する。ゲームイベントや状態変化ごとに音を分ける。       |
| [`styling-web-game-typography`](.agents/skills/styling-web-game-typography/SKILL.md)         | 配布ゲーム向けの読みやすくライセンス上問題ないタイポグラフィを実装する。Godot 4.2+ の実装例を含む。   |
| [`designing-retro-arcade-sound-kits`](.agents/skills/designing-retro-arcade-sound-kits/SKILL.md) | ゲームコードが抽象イベント名を発火し、アダプター層が音を解決・再生するアーキテクチャで、レトロアーケードのサウンドキット（SE・ジングル）を設計・検証する。エンジン非依存。 |
| [`generating-dot-assets`](.agents/skills/generating-dot-assets/SKILL.md)                     | 画像生成、クロマキー除去、ピクセル化、キャンバス調整、検証により透明 PNG のピクセルアート素材を作る。 |

### 評価と調整

| Skill                         | 用途                                                                                   |
| ----------------------------- | -------------------------------------------------------------------------------------- |
| [`evaluating-gameplay-balance`](.agents/skills/evaluating-gameplay-balance/SKILL.md) | テレメトリでゲームバランスを評価する。単調な方策と探索的または意図した方策を比較する。 |

### Agent Workflow

| Skill                     | 用途                                                                                                     |
| ------------------------- | -------------------------------------------------------------------------------------------------------- |
| [`extracting-agent-skills`](.agents/skills/extracting-agent-skills/SKILL.md) | 完了、停止、放棄、失敗したプロジェクトから再利用可能な手順、検証ループ、デバッグ法、判断規則を抽出する。 |
| [`extracting-spec-design-ladders`](.agents/skills/extracting-spec-design-ladders/SKILL.md) | ソースコードを「再現仕様」と「抽象設計書」の二層アーティファクトに逆工学する。両層の役割を重複させず、抽出ログで監査可能にする。 |
| [`gating-by-blind-restoration`](.agents/skills/gating-by-blind-restoration/SKILL.md) | 仕様、設計書、スキーマ、契約などの抽象層が自己完結しているかを、その層のみを渡した独立サブエージェントによる盲目的再構築で検証する。判定は pass / weak-pass / fail。 |
| [`migrating-agents-md-to-control-flow`](.agents/skills/migrating-agents-md-to-control-flow/SKILL.md) | 大きな repo agent 指示ファイルを監査し、反復 workflow を skill へ、必須 check を script/hook/CI へ、安定 policy を簡潔な repo 指示へ移す。 |
| [`refining-workflows-from-artifacts`](.agents/skills/refining-workflows-from-artifacts/SKILL.md) | 実行結果の artifact をもとに再利用可能な agent workflow を改善する。失敗原因を分類してから、根拠のある最小の workflow 差分を提案する。 |
| [`critiquing-own-response`](.agents/skills/critiquing-own-response/SKILL.md) | 直前の応答を構造的に自己批判する。前提、論理、AI 特有の失敗、リスク、信頼度を点検する。                  |

## 補助ディレクトリ

- `references/`: 詳細ガイド、チェックリスト、設計テンプレート、実装パターン。
- `assets/`: 再利用可能なテンプレート、Godot script、フォント、素材。
- `scripts/`: 素材生成、検証、関連 workflow の自動化。
- `tools/`: README と skill 一覧の照合、外部 skill 取得などのリポジトリ保守用ツール。
- `agents/`: skill 用の任意のモデル別・agent 別設定。

## 外部 Skill 参照

次の skill は他リポジトリから取り込む。`.gitignore` に含め、ローカル利用してもこのリポジトリにはコミットしない。取得には `tools/install-external-skills.sh` を使う。引数で対象名を指定できる。

- [`empirical-prompt-tuning`](https://github.com/mizchi/skills/blob/main/meta/empirical-prompt-tuning/SKILL.md): prompt、skill、slash command、`AGENTS.md` 形式の指示を評価・改善する反復手法。
- [`godot-master`](https://github.com/thedivergentai/gd-agentic-skills): `gd-agentic-skills` の Godot 4 アーキテクチャと実装リファレンス。エンジン固有トピックのスキル(例: `godot-tweening`、`godot-particles`、`godot-debugging-profiling`)だけを `install-external-skills.sh` の `install_subtree` で個別に取得する。アーキテクチャ教義とジャンル別スキルはプロダクション規模の Godot 4.7+ ゲームが対象で、このリポジトリの最小構成ミニゲーム方針と衝突するため、全量インストールはしない(スクリプトも意図的に自動取得しない)。
- [`systematic-debugging`](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md): バグ、テスト失敗、想定外挙動に対する根本原因優先のデバッグ workflow。

## リポジトリツール

- `tools/install-external-skills.sh`: 外部 skill を `.agents/skills/<name>/` に取得する。
- `tools/check-readme-skills.sh`: `.agents/skills/` の skill ディレクトリと README の記載を照合する。不一致なら非ゼロ終了する。
