# Agentic Gamedev Skills

[English](README.md) | 日本語

このリポジトリは、ゲーム開発と agentic workflow の研究から抽出した agent skill 集である。各 skill は `.agents/skills/` 以下に置き、`SKILL.md` を入口とする。必要に応じて `references/`、`assets/`、`scripts/`、`tools/`、`agents/` を含む。

主な用途は、ミニゲームの制作である。一ボタン操作、強い視覚フィードバック、手続き型音声、テレメトリによる調整、任意のピクセルアート素材生成を扱う。補助的に、skill 抽出、実行成果物からの workflow 改善、高コストな agent 作業のゲートとディスパッチも扱う。

これらの skill を使って制作したゲームは [agentic-gamedev-games](https://github.com/abagames/agentic-gamedev-games) にある。

## 使い方

- skill 名を指定するか、タスク内容を `description` にマッチさせて使う。
- 各 `SKILL.md` をその機能の標準手順とする。
- リポジトリ管理ルールは `AGENTS.md` に従う。

## プラグイン配布

Codex と Claude Code 向けに、6つのリポジトリ配布プラグインを用意している。各 `0.1.0` の導入可能なルートとカタログは、このリポジトリの canonical skill と composition から生成される。レビュー済みの変更を commit して GitHub に push すると利用可能になる。GitHub 配布と OpenAI / Anthropic の curated directory への申請は別の操作である。再生成、検証、versioning、公開境界は [maintainer guide](PLUGIN_RELEASE.md) を参照。

| Plugin | Skills |
| --- | ---: |
| [One-Button Game Builder](plugins/one-button-game-builder/README.md) | 7 |
| [Gameplay Verification & Debugging Toolkit](plugins/gameplay-debugging-toolkit/README.md) | 5 |
| [Retro Arcade Game Finisher](plugins/retro-arcade-game-finisher/README.md) | 5 |
| [Godot Mini-Game Builder](plugins/godot-mini-game-builder/README.md) | 4 |
| [Web Mini-Game Kit](plugins/web-mini-game-kit/README.md) | 4 |
| [Agent Workflow Engineering](plugins/agent-workflow-engineering/README.md) | 9 |

32のローカルスキルを延べ34件収録し、外部参照スキルは同梱しない。

GitHub 公開後、Claude Code では `abagames/agentic-gamedev-skills` を marketplace として追加し、`<plugin>@agentic-gamedev-skills` をインストールできる。Codex CLI でも同じ `owner/repo` marketplace を追加し、available plugin を確認して `<plugin>@agentic-gamedev-skills` をインストールできる。workspace admin は plugin management から GitHub repository を import できる。リポジトリには標準 Codex catalog、API key login 用 Codex catalog、Claude Code catalog があり、maintainer は `python3 tools/plugin-bundles/published.py --repo . --write` で再生成する。

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
| [`generating-retro-arcade-concepts`](.agents/skills/generating-retro-arcade-concepts/SKILL.md) | 1978〜1985 年代の固定画面アーケードゲームコンセプトを複数一括生成・評価し、上位コンセプトの実装仕様を書く。 |
| [`verifying-turn-based-games`](.agents/skills/verifying-turn-based-games/SKILL.md) | 二人用の厳密な交互ターンゲームを、純粋関数エンジン契約と bot ladder、緊張度、判断密度で検証する。          |

### ゲーム実装

| Skill                            | 用途                                                                                                              |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| [`scaffolding-godot-mini-games`](.agents/skills/scaffolding-godot-mini-games/SKILL.md)     | Godot 4.2+ ミニゲームの最小構成を作る。Web export、テスト、テレメトリ、手続き型音声を含む。                       |
| [`running-headless-godot`](.agents/skills/running-headless-godot/SKILL.md)                 | Godot の headless CLI、ログ、スクリプトによるシーン編集、テスト、Web export を再現可能にする。                    |
| [`developing-with-crisp-game-lib`](.agents/skills/developing-with-crisp-game-lib/SKILL.md) | `crisp-game-lib` のブラウザミニゲームを実装または修復する。セットアップ、ループ、描画順、衝突、得点、検証を扱う。 |
| [`arcadifying-mini-games`](.agents/skills/arcadifying-mini-games/SKILL.md) | 動作確認済みのミニゲームに、ラウンド構造、儀式画面（READY・クリア・ミス・ゲームオーバー）、スコア経済（エクステンド、イニシャル入力、ハイスコア表）、アトラクトモードを加え、完成したアーケードゲームに仕上げる。 |
| [`implementing-gameplay-invariants`](.agents/skills/implementing-gameplay-invariants/SKILL.md) | ゲーム設計上の約束を、エンジン非依存の実装不変条件と検証項目に変換する。放置、長押し固定、連打、反復得点の優位を防ぐ。 |

### ゲーム演出

| Skill                             | 用途                                                                                                  |
| --------------------------------- | ----------------------------------------------------------------------------------------------------- |
| [`directing-game-visuals`](.agents/skills/directing-game-visuals/SKILL.md)                   | HUD 説明に頼らず、視覚階層、パレット役割、画面構成、イベントフィードバックを定義する。                |
| [`maximizing-game-feel`](.agents/skills/maximizing-game-feel/SKILL.md)                       | squash/stretch、傾き、パーティクル、軌跡、ヒット演出で操作感を高める。                                |
| [`creating-godot-procedural-audio`](.agents/skills/creating-godot-procedural-audio/SKILL.md) | Godot の組み込み API で手続き型音声を設計・実装する。ゲームイベントや状態変化ごとに音を分ける。       |
| [`building-era-authentic-game-audio`](.agents/skills/building-era-authentic-game-audio/SKILL.md) | BGM、SE、ジングル、イベント配線、ボイス競合制御を含むゲーム固有の手続き型音声システムを、時代風または対象ハード準拠の制約で設計・実装・検証する。 |
| [`styling-web-game-typography`](.agents/skills/styling-web-game-typography/SKILL.md)         | 配布ゲーム向けの読みやすくライセンス上問題ないタイポグラフィを実装する。Godot 4.2+ の実装例を含む。   |
| [`designing-retro-arcade-sound-kits`](.agents/skills/designing-retro-arcade-sound-kits/SKILL.md) | ゲームコードが抽象イベント名を発火し、アダプター層が音を解決・再生するアーキテクチャで、レトロアーケードのサウンドキット（SE・ジングル）を設計・検証する。エンジン非依存。 |
| [`generating-dot-assets`](.agents/skills/generating-dot-assets/SKILL.md)                     | 画像生成、クロマキー除去、ピクセル化、キャンバス調整、検証により透明 PNG のピクセルアート素材を作る。 |

### 評価と調整

| Skill                         | 用途                                                                                   |
| ----------------------------- | -------------------------------------------------------------------------------------- |
| [`evaluating-gameplay-balance`](.agents/skills/evaluating-gameplay-balance/SKILL.md) | テレメトリでゲームバランスを評価する。単調な方策と探索的または意図した方策を比較する。 |
| [`gating-intent-legibility`](.agents/skills/gating-intent-legibility/SKILL.md) | 記録済みプレイから抽出した場面画像だけを見る隔離agentに、目的・選択肢・リスクを言わせて画面の伝達力を測る。伏せた後続フレームをoracleとし、劣化版controlで計器そのものを検証したうえで、意図・判断多様性・入口の各verdictを返す。 |

### ゲームプレイの検証とデバッグ

安価なゲートから高価な計測手段の順に並べる。動作健全性、仕様適合、挙動ファミリの網羅、欠陥の局所化、修正の検証、そして計測手段そのものの測定。

| Skill | 用途 |
| --- | --- |
| [`smoke-testing-web-games`](.agents/skills/smoke-testing-web-games/SKILL.md) | ブラウザゲームを headless で起動し、放置と入力バーストを与えて console エラー・未捕捉例外・クラッシュを検出する。モックやシミュレータは通るがブラウザで落ちるコードを機械検出する。 |
| [`probing-web-game-mechanics`](.agents/skills/probing-web-game-mechanics/SKILL.md) | 稼働中の headless ブラウザにゲーム状態を注入し、フェーズ遷移、得点式、ゲート、リセットが仕様どおりかを検証する。スモークテスト（動作健全性）とバランス評価（プレイ品質）の中間層を担う。 |
| [`auditing-gameplay-implementation-coverage`](.agents/skills/auditing-gameplay-implementation-coverage/SKILL.md) | 仕様、実装、演出、テストを横断して範囲を限定した監査を行い、兄弟ケースの実装漏れや具体的なprobe不足を検出する。 |
| [`localizing-game-state-divergence`](.agents/skills/localizing-game-state-divergence/SKILL.md) | 決定的に再現できる不具合をリプレイし、機械判定可能な状態不変条件が最初に破れるeventを特定する。 |
| [`adversarially-validating-game-repairs`](.agents/skills/adversarially-validating-game-repairs/SKILL.md) | 既存のゲーム修正を、patchが到達しうる敵対条件と逆ケースで検証し、再現可能な修正根拠を返す。 |
| [`generating-semantic-game-mutants`](.agents/skills/generating-semantic-game-mutants/SKILL.md) | 制御されたゲームプレイ欠陥、clean control、equivalent mutantを生成し、テストやagent workflowの検出・修復能力を測定する。 |

### Agent Workflow

| Skill                     | 用途                                                                                                     |
| ------------------------- | -------------------------------------------------------------------------------------------------------- |
| [`extracting-agent-skills`](.agents/skills/extracting-agent-skills/SKILL.md) | 完了、停止、放棄、失敗したプロジェクトから再利用可能な手順、検証ループ、デバッグ法、判断規則を抽出する。 |
| [`extracting-spec-design-ladders`](.agents/skills/extracting-spec-design-ladders/SKILL.md) | ソースコードを「再現仕様」と「抽象設計書」の二層アーティファクトに逆工学する。両層の役割を重複させず、抽出ログで監査可能にする。 |
| [`gating-by-blind-restoration`](.agents/skills/gating-by-blind-restoration/SKILL.md) | 仕様、設計書、スキーマ、契約などの抽象層が自己完結しているかを、その層のみを渡した独立サブエージェントによる盲目的再構築で検証する。判定は pass / weak-pass / fail。 |
| [`gating-expensive-batch-work`](.agents/skills/gating-expensive-batch-work/SKILL.md) | 高コストなアイテム単位作業のバッチを、全アイテムを対象とする安価で可逆なパスと、高コストで不可逆なパスに分割し、その間に手法凍結チェックポイントを置く。fresh seed、held-out データ、一度きりのクォータを消費する前に、誤ったルーブリックや変換規則を検出する。 |
| [`migrating-agents-md-to-control-flow`](.agents/skills/migrating-agents-md-to-control-flow/SKILL.md) | 大きな repo agent 指示ファイルを監査し、反復 workflow を skill へ、必須 check を script/hook/CI へ、安定 policy を簡潔な repo 指示へ移す。 |
| [`refining-workflows-from-artifacts`](.agents/skills/refining-workflows-from-artifacts/SKILL.md) | 実行結果の artifact をもとに再利用可能な agent workflow を改善する。失敗原因を分類してから、根拠のある最小の workflow 差分を提案する。 |
| [`critiquing-own-response`](.agents/skills/critiquing-own-response/SKILL.md) | 直前の自分の応答を、前提、論理の飛躍、代替案、未検証の主張という観点で見直す advisory pass。明示的に呼び出して使う。批判対象と盲点を共有するため、独立した品質保証ではない。 |
| [`dispatching-agent-work`](.agents/skills/dispatching-agent-work/SKILL.md) | 実作業を適切な実行境界へ委譲し、既存 worker の再利用には objective、artifact、authority、lifecycle、model role、reasoning effort の継続性を必須とする。永続 dispatch mode は明示的に選択した場合のみ有効になる。 |

## 補助ディレクトリ

- `references/`: 詳細ガイド、チェックリスト、設計テンプレート、実装パターン。
- `assets/`: 再利用可能なテンプレート、Godot script、フォント、素材。
- `scripts/`: 素材生成、検証、関連 workflow の自動化。
- `tools/`: README と skill 一覧の照合、外部 skill 取得などのリポジトリ保守用ツール。
- `agents/`: skill 用の任意のモデル別・agent 別設定。

## 外部 Skill 参照

次の個別 skill は、特定のローカル workflow を補完するため、他リポジトリから取り込むか参照する。`.gitignore` に含め、ローカルで評価・利用してもこのリポジトリにはコミットしない。`tools/install-external-skills.sh` は対応済みの対象を取得する。参照のみの skill は上流 collection を全量導入せず、個別に評価・調整する。

- [`empirical-prompt-tuning`](https://github.com/mizchi/skills/blob/main/meta/empirical-prompt-tuning/SKILL.md): prompt、skill、slash command、`AGENTS.md` 形式の指示を評価・改善する反復手法。
- [`writing-for-agents`](https://github.com/mattpocock/skills/blob/main/docs/productivity/writing-for-agents.md): agent 向けの skill、指示、仕様、prompt を予測可能にするため、完了条件、context load、no-op・重複・陳腐化した記述の剪定を扱うリファレンス。`extracting-agent-skills` と `refining-workflows-from-artifacts` に組み合わせ、上流の invocation metadata が異なる場合もこのリポジトリの frontmatter 規約を維持する。
- [`source-driven-development`](https://github.com/addyosmani/agent-skills/blob/main/skills/source-driven-development/SKILL.md): 公式ドキュメントに基づくバージョン対応の実装 workflow。現行の engine・browser・library API に依存する場合、`developing-with-crisp-game-lib`、`running-headless-godot`、`scaffolding-godot-mini-games` に組み合わせる。これらの domain workflow を置き換えず、プロジェクト固有の検証を補完する。
- [`browser-testing-with-devtools`](https://github.com/addyosmani/agent-skills/blob/main/skills/browser-testing-with-devtools/SKILL.md): console、network、DOM、performance の実測による live browser 診断。`smoke-testing-web-games` または `probing-web-game-mechanics` がブラウザゲームの問題範囲を絞った後、より深い runtime 調査が必要な場合に組み合わせる。Chrome DevTools MCP が利用できない場合は workflow を調整する。
- [`performance-optimization`](https://github.com/addyosmani/agent-skills/blob/main/skills/performance-optimization/SKILL.md): 計測優先の performance 調査と変更前後の検証。`smoke-testing-web-games` または `maximizing-game-feel` に performance gate を拡張する素材とし、汎用 Web application 向け指標は frame time、入力遅延、memory 増加、load size、代表的な device の budget などゲーム向け指標に置き換える。
- [`systematic-debugging`](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md): バグ、テスト失敗、想定外挙動に対する根本原因優先のデバッグ workflow。既定ではインストールしない。あらゆる技術的問題を trigger として主張するため、`localizing-game-state-divergence`、`adversarially-validating-game-repairs`、`smoke-testing-web-games`、`probing-web-game-mechanics` を補完せず上書きしてしまい、Phase 4 がこのリポジトリに存在しない `superpowers:` 系 skill を参照する。ゲーム以外の作業や、ローカルのデバッグ skill が意図的に対象外としている crash・build 失敗・多コンポーネント境界の切り分けが必要な場合に、名前を指定して取得する(`install-external-skills.sh systematic-debugging`)。

## リポジトリツール

- `tools/install-external-skills.sh`: 対応済みの外部 skill を段階配置先へ取得・検証してから `.agents/skills/<name>/` を置き換える。失敗時は導入済み版を保持する。参照のみの項目は自動取得の対象外。
- `tools/check-readme-skills.sh`: ローカル skill ディレクトリと `.gitignore` の外部 skill を README と照合する。不一致なら非ゼロ終了する。
- `tools/tests/test-repository-tools.sh`: ネットワークや導入済み skill を変更せず、installer の成功・失敗復元・path containment・README 整合性を検証する。
- `python3 tools/plugin-bundles/build.py plugin-bundles/<bundle>.json --target codex|claude`: スキルと資産から自己完結した plugin を生成する。全ペイロードの hash・実行権限を lock v3 に記録する。`--publishable` は clean input のゲートであり、完全再現性や公式承認は意味しない。生成された `dist/` は直接編集・commit せず再生成する。
- `tools/tests/test-plugin-bundles.sh`: composition、生成 artifact、決定的な skill hash、不正または危険な入力の拒否を検証する。
- `python3 tools/plugin-bundles/published.py --write|--check`: composition と canonical skill から、追跡対象の6つの plugin root と Codex、Codex API key、Claude catalog を再生成または検証する。stale payload、root の不足・過剰、path escape、identity / version drift を拒否する。
- `python3 tools/plugin-bundles/package.py --output <new-dir>`: 全6構成をZIP化して展開後も検証し、checksum と結果レポートを生成する。公式 validator の指定方法は公開ガイドを参照。
