# Agentic Gamedev Skills

[English](README.md) | 日本語

このリポジトリは、ゲーム開発と agentic workflow の研究から抽出した agent skill 集である。各 skill は `.agents/skills/` 以下に置き、`SKILL.md` を入口とする。必要に応じて `references/`、`assets/`、`scripts/`、`tools/`、`agents/` を含む。

主な用途は、ミニゲームの制作である。一ボタン操作、強い視覚フィードバック、手続き型音声、テレメトリによる調整、任意のピクセルアート素材生成を扱う。実装前の concept exploration、敵対的な concept review、mechanism の多様性を保つ portfolio curation も扱う。補助的に、skill 抽出、実行成果物からの workflow 改善、高コストな agent 作業のゲートとディスパッチも扱う。

これらの skill を使って制作したゲームは [agentic-gamedev-games](https://github.com/abagames/agentic-gamedev-games) にある。

## 使い方

- skill 名を指定するか、タスク内容を `description` にマッチさせて使う。
- 各 `SKILL.md` をその機能の標準手順とする。
- リポジトリ管理ルールは `AGENTS.md` に従う。

## プラグイン配布

Codex と Claude Code 向けに、7つのリポジトリ配布プラグインを用意している。バージョン付きの導入可能なルートとカタログは、このリポジトリの canonical skill と composition から生成される。GitHub 配布と OpenAI / Anthropic の curated directory への申請は別の操作である。再生成、検証、versioning、公開境界は [maintainer guide](PLUGIN_RELEASE.md) を参照。

| Plugin | Skills |
| --- | ---: |
| [Game Concept Workbench](plugins/game-concept-workbench/README.md) | 3 |
| [One-Button Game Builder](plugins/one-button-game-builder/README.md) | 9 |
| [Gameplay Verification & Debugging Toolkit](plugins/gameplay-debugging-toolkit/README.md) | 5 |
| [Retro Arcade Game Finisher](plugins/retro-arcade-game-finisher/README.md) | 5 |
| [Godot Mini-Game Builder](plugins/godot-mini-game-builder/README.md) | 4 |
| [Web Mini-Game Kit](plugins/web-mini-game-kit/README.md) | 4 |
| [Agent Workflow Engineering](plugins/agent-workflow-engineering/README.md) | 9 |

37のローカルスキルを延べ39件収録し、外部参照スキルは同梱しない。

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
| [`exploring-game-design-space`](.agents/skills/exploring-game-design-space/SKILL.md) | 多様なゲームの仕組みを探索し、検証可能なコンセプト候補を作る。設計候補を絞り込む前に使う。 |
| [`designing-mini-games`](.agents/skills/designing-mini-games/SKILL.md) | 一ボタンを含む任意の入力構成で、ミニゲームのルール、操作、得点、危険、難度の進行を設計する。 |
| [`designing-minimal-game-rules`](.agents/skills/designing-minimal-game-rules/SKILL.md) | 抽象的な設計の種から、単純戦略に耐える最小の離散状態ルール体系を作る。 |
| [`generating-retro-arcade-concepts`](.agents/skills/generating-retro-arcade-concepts/SKILL.md) | 1978〜1985年の固定画面アーケードを題材に複数のコンセプトを生成・評価し、選んだ案の実装仕様を書く。 |
| [`curating-game-concept-portfolio`](.agents/skills/curating-game-concept-portfolio/SKILL.md) | 既存のゲーム案を仕組みと根拠で比較し、仕組みの異なる少数の案に絞る。 |
| [`verifying-turn-based-games`](.agents/skills/verifying-turn-based-games/SKILL.md) | 二人用の厳密な交互ターンゲームを、純粋関数のエンジン契約とボットによる品質計測で検証する。 |

### ゲーム実装

| Skill                            | 用途                                                                                                              |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| [`scaffolding-godot-mini-games`](.agents/skills/scaffolding-godot-mini-games/SKILL.md) | Web出力、テスト、テレメトリ、手続き型音声の基盤を備えたGodot 4.2+ミニゲームの最小構成を作る。 |
| [`running-headless-godot`](.agents/skills/running-headless-godot/SKILL.md) | Godotをヘッドレスで実行し、シーン編集、テスト、Web出力を再現可能にする。 |
| [`developing-with-crisp-game-lib`](.agents/skills/developing-with-crisp-game-lib/SKILL.md) | `crisp-game-lib`固有の入力、描画、衝突、ゲームループに沿って、ブラウザミニゲームを制作・修復する。 |
| [`arcadifying-mini-games`](.agents/skills/arcadifying-mini-games/SKILL.md) | 動作するミニゲームにラウンド、開始・終了演出、スコア経済、ランキング、アトラクトモードを加え、アーケードゲームに仕上げる。 |
| [`implementing-gameplay-invariants`](.agents/skills/implementing-gameplay-invariants/SKILL.md) | ゲーム設計上の約束を、エンジン非依存の実装不変条件と検証項目に変換する。 |

### ゲーム演出

| Skill                             | 用途                                                                                                  |
| --------------------------------- | ----------------------------------------------------------------------------------------------------- |
| [`directing-game-visuals`](.agents/skills/directing-game-visuals/SKILL.md) | 視覚階層、配色、画面構成、イベントの反応を定め、画面からゲームの状況を読み取れるようにする。 |
| [`maximizing-game-feel`](.agents/skills/maximizing-game-feel/SKILL.md) | 動作するアクションゲームの反応と手応えを、アニメーションやエフェクトで高める。 |
| [`creating-godot-procedural-audio`](.agents/skills/creating-godot-procedural-audio/SKILL.md) | Godotの組み込み音声APIで、ゲームイベントや状態変化に対応する手続き型音声を設計・実装する。 |
| [`building-era-authentic-game-audio`](.agents/skills/building-era-authentic-game-audio/SKILL.md) | 初期アーケードの音源を参考に、音楽・効果音・ジングルを含むゲーム全体の手続き型音声システムを作る。 |
| [`styling-web-game-typography`](.agents/skills/styling-web-game-typography/SKILL.md) | 配布ゲーム向けに、読みやすくライセンス上問題のない文字表示を実装する。Godotの実装例を含む。 |
| [`designing-retro-arcade-sound-kits`](.agents/skills/designing-retro-arcade-sound-kits/SKILL.md) | エンジン非依存のゲームイベントから鳴らす、レトロアーケード風の効果音とジングルを設計・検証する。 |
| [`generating-dot-assets`](.agents/skills/generating-dot-assets/SKILL.md) | 指定したキャンバスサイズで、背景が透明なピクセルアートの物体素材を生成・検証する。 |

### 評価と調整

| Skill                         | 用途                                                                                   |
| ----------------------------- | -------------------------------------------------------------------------------------- |
| [`stress-testing-game-concepts`](.agents/skills/stress-testing-game-concepts/SKILL.md) | 既存のコンセプト、ルール、初期プロトタイプを敵対的に検査し、実証済みの欠陥と未確認事項を分ける。 |
| [`evaluating-gameplay-balance`](.agents/skills/evaluating-gameplay-balance/SKILL.md) | テレメトリと単純戦略・意図したプレイの比較でバランスを評価する。抜け道を検出し、プレイ報告で較正した模擬プレイヤーを使って難度を調整する。 |
| [`refining-game-prototypes`](.agents/skills/refining-game-prototypes/SKILL.md) | 動作するプロトタイプを、構造・難度と進行・演出・仕上げの順に自律的に改善する。ゲームの意図と観測した根拠に基づいて修正を選び、改訂記録と未解決事項を残す。 |
| [`auditing-game-screen-readability`](.agents/skills/auditing-game-screen-readability/SKILL.md) | ゲームイベントや通知が重なる場面の画像を調べ、読みにくい、隠れた、不要な表示を検出する。 |
| [`gating-intent-legibility`](.agents/skills/gating-intent-legibility/SKILL.md) | ルールを知らない独立した読み手が、プレイ画像だけから目的・選択肢・リスクを読み取れるかを検証する。 |

### ゲームプレイの検証とデバッグ

安価なゲートから高価な計測手段の順に並べる。動作健全性、仕様適合、挙動ファミリの網羅、欠陥の局所化、修正の検証、そして計測手段そのものの測定。

| Skill | 用途 |
| --- | --- |
| [`smoke-testing-web-games`](.agents/skills/smoke-testing-web-games/SKILL.md) | ブラウザゲームを放置と入力の両方で動かし、コンソールエラー、未捕捉例外、クラッシュを検出する。 |
| [`probing-web-game-mechanics`](.agents/skills/probing-web-game-mechanics/SKILL.md) | ブラウザゲームに状態を注入して遷移を検査し、仕組み・表示・入力の接続が仕様どおりかを検証する。 |
| [`auditing-gameplay-implementation-coverage`](.agents/skills/auditing-gameplay-implementation-coverage/SKILL.md) | 仕様・実装・演出・テストを横断し、関連するゲーム挙動の中で対応が漏れたケースを検出する。 |
| [`localizing-game-state-divergence`](.agents/skills/localizing-game-state-divergence/SKILL.md) | 再現可能なゲーム不具合をリプレイし、状態不変条件が最初に破れるイベントを特定する。 |
| [`adversarially-validating-game-repairs`](.agents/skills/adversarially-validating-game-repairs/SKILL.md) | 既存のゲーム修正を、変更が影響する敵対的なケースと、影響すべきでないケースで検証する。 |
| [`generating-semantic-game-mutants`](.agents/skills/generating-semantic-game-mutants/SKILL.md) | 制御されたゲームの欠陥を注入し、テストの検出能力やエージェントの修復能力を測る。 |

### Agent Workflow

| Skill                     | 用途                                                                                                     |
| ------------------------- | -------------------------------------------------------------------------------------------------------- |
| [`extracting-agent-skills`](.agents/skills/extracting-agent-skills/SKILL.md) | 完了・停止・放棄・失敗したプロジェクトから、再利用可能なエージェントの手順と判断規則を抽出する。 |
| [`extracting-spec-design-ladders`](.agents/skills/extracting-spec-design-ladders/SKILL.md) | ソースコードから、具体的な再現仕様と抽象的な設計書の二層を抽出する。 |
| [`gating-by-blind-restoration`](.agents/skills/gating-by-blind-restoration/SKILL.md) | 仕様などの抽象層だけを独立したエージェントに渡して再構築させ、情報が自己完結しているかを検証する。 |
| [`gating-expensive-batch-work`](.agents/skills/gating-expensive-batch-work/SKILL.md) | 安価な試行と高コストな一括実行を分け、取り戻せない資源を使う前に手法を確定する。 |
| [`migrating-agents-md-to-control-flow`](.agents/skills/migrating-agents-md-to-control-flow/SKILL.md) | 肥大化したエージェント指示から、反復手順をスキルへ、必須チェックをスクリプト・フック・CIへ移す。 |
| [`refining-workflows-from-artifacts`](.agents/skills/refining-workflows-from-artifacts/SKILL.md) | 実際の実行結果から失敗原因を特定し、再利用可能なエージェントの手順に必要な変更を提案する。 |
| [`critiquing-own-response`](.agents/skills/critiquing-own-response/SKILL.md) | 直前の自分の応答を、前提・推論の抜け・未検証の主張から見直す。明示的に呼び出して使い、独立したレビューとは区別する。 |
| [`dispatching-agent-work`](.agents/skills/dispatching-agent-work/SKILL.md) | 文脈と権限を引き継ぎながら、作業を適切なタスク・エージェント・自動化に振り分ける。継続的な委譲モードは明示的に選択する。 |

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
- `python3 tools/plugin-bundles/published.py --write|--check`: composition と canonical skill から、追跡対象の7つの plugin root と Codex、Codex API key、Claude catalog を再生成または検証する。stale payload、root の不足・過剰、path escape、identity / version drift を拒否する。
- `python3 tools/plugin-bundles/package.py --output <new-dir>`: 全7構成をZIP化して展開後も検証し、checksum と結果レポートを生成する。公式 validator の指定方法は公開ガイドを参照。
