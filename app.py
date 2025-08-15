import streamlit as st
import base64
import time

# セッション状態の初期化
if "hp" not in st.session_state:
    st.session_state.hp = 30
if "previous_hp" not in st.session_state:
    st.session_state.previous_hp = 30
if "uploaded_music" not in st.session_state:
    st.session_state.uploaded_music = {}
if "music_enabled" not in st.session_state:
    st.session_state.music_enabled = False
if "auto_start_music" not in st.session_state:
    st.session_state.auto_start_music = False

def get_status_info(hp):
    """HPに基づいてステータス情報を返す"""
    if hp >= 26:
        return {
            "title": "司令部機能正常「黎明の静寂」",
            "restriction": "完全な情報共有可能",
            "consultation_time": "無制限",
            "description": "光が洞窟を照らし、魔道士たちの連携は完璧だ。防衛陣形は保たれ、まだ希望の灯は消えていない。",
            "color": "#4CAF50",  # 緑
            "music_key": "normal"
        }
    elif hp >= 16:
        return {
            "title": "通信障害発生「響く警鐘」",
            "restriction": "呪文カードのみ公開可能",
            "consultation_time": "制限あり",
            "description": "警鐘が鳴り響く。瓦礫が司令部の一部を塞ぎ、補給路が寸断された。魔道士たちは戦闘計画だけを必死に共有する。『呪文の準備状況を報告しろ！』",
            "color": "#FF9800",  # オレンジ
            "music_key": "warning"
        }
    elif hp >= 6:
        return {
            "title": "司令部半壊「崩れゆく防壁」",
            "restriction": "手札公開禁止、数値のコミュニケーションのみ",
            "consultation_time": "数値のみ",
            "description": "天井が崩落し、煙と粉塵が視界を奪う。もはや互いの顔も見えない。声だけが頼りだ。",
            "color": "#F44336",  # 赤
            "music_key": "danger"
        }
    elif hp >= 1:
        return {
            "title": "陥落寸前「最後の抵抗」",
            "restriction": "一切の相談禁止",
            "consultation_time": "禁止",
            "description": "もはや声も届かない。轟音と絶叫のみ。各魔道士は孤立し、本能と経験だけを頼りに呪文を紡ぐ。これが、グレイブホールド最後の時かもしれない…",
            "color": "#9C27B0",  # 紫
            "music_key": "critical"
        }
    else:
        return {
            "title": "GAME OVER",
            "restriction": "ゲーム終了",
            "consultation_time": "ゲーム終了",
            "description": "グレイブホールドは陥落した。魔道士たちの抵抗も虚しく、ネメシスの支配が始まった…",
            "color": "#000000",  # 黒
            "music_key": "gameover"
        }

def create_persistent_music_system(music_data, current_status_key, music_enabled, auto_start, status_color):
    """永続的な音楽切り替えシステム（境界値問題修正版・色統一対応）"""
    
    # 音楽データをJavaScript用に準備
    js_music_data = {}
    for key, file_obj in music_data.items():
        if file_obj:
            if hasattr(file_obj, 'read'):
                audio_bytes = file_obj.read()
                file_obj.seek(0)
                js_music_data[key] = base64.b64encode(audio_bytes).decode()
            else:
                js_music_data[key] = file_obj
    
    # 一意のタイムスタンプ
    timestamp = int(time.time() * 1000)
    
    html_code = f"""
    <div id="persistent-music-system">
        <div id="music-controls" style="text-align: center; margin: 20px 0; padding: 20px; background: linear-gradient(135deg, #e3f2fd, #bbdefb); border-radius: 10px; border: 2px solid #2196F3;">
            <h3 style="margin-top: 0;">🎵 永続的音楽切り替えシステム</h3>
            <button id="enable-music" onclick="enableMusicSystem()" style="padding: 10px 20px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 5px; font-size: 16px;">
                🎵 音楽システム有効化
            </button>
            <button id="disable-music" onclick="disableMusicSystem()" style="padding: 10px 20px; background: #f44336; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 5px; font-size: 16px; display: none;">
                🔇 音楽システム無効化
            </button>
            <div id="music-status" style="margin-top: 10px; font-weight: bold; font-size: 18px;">🔇 音楽: 無効</div>
            <div id="current-track" style="margin-top: 5px; color: #666; font-size: 16px;">再生中: なし</div>
        </div>
        
        <!-- 永続化された音楽要素 -->
        <div id="persistent-audio-elements" style="display: none;">
    """
    
    # 各音楽要素を追加
    for key, b64_data in js_music_data.items():
        html_code += f"""
            <audio id="persistent-audio-{key}" loop preload="auto" data-key="{key}">
                <source src="data:audio/mp3;base64,{b64_data}" type="audio/mp3">
            </audio>
        """
    
    html_code += f"""
        </div>
    </div>

    <script>
    // グローバル状態をlocalStorageで永続化（ページ再描画に影響されない）
    if (!window.musicSystemInitialized) {{
        window.musicSystemEnabled = localStorage.getItem('aeons_music_enabled') === 'true';
        window.currentPlayingAudio = null;
        window.currentStatus = localStorage.getItem('aeons_current_status') || '{current_status_key}';
        window.musicSystemInitialized = true;
        
        console.log('音楽システム初期化 - 有効:', window.musicSystemEnabled, '現在ステータス:', window.currentStatus);
    }}
    
    // 音楽システム有効化
    function enableMusicSystem() {{
        window.musicSystemEnabled = true;
        localStorage.setItem('aeons_music_enabled', 'true');
        
        document.getElementById('enable-music').style.display = 'none';
        document.getElementById('disable-music').style.display = 'inline-block';
        document.getElementById('music-status').innerHTML = '🎵 音楽: 有効';
        document.getElementById('music-status').style.color = '{status_color}';
        
        // 現在のステータスの音楽を再生
        playStatusMusic('{current_status_key}');
        
        console.log('音楽システムが有効化されました');
    }}
    
    // 音楽システム無効化
    function disableMusicSystem() {{
        window.musicSystemEnabled = false;
        localStorage.setItem('aeons_music_enabled', 'false');
        
        document.getElementById('enable-music').style.display = 'inline-block';
        document.getElementById('disable-music').style.display = 'none';
        document.getElementById('music-status').innerHTML = '🔇 音楽: 無効';
        document.getElementById('music-status').style.color = '{status_color}';
        document.getElementById('current-track').innerHTML = '再生中: なし';
        document.getElementById('current-track').style.color = '{status_color}AA';
        
        // 全ての音楽を停止
        stopAllMusic();
        
        console.log('音楽システムが無効化されました');
    }}
    
    // 全ての音楽を停止
    function stopAllMusic() {{
        document.querySelectorAll('[id^="persistent-audio-"]').forEach(function(audio) {{
            audio.pause();
            audio.currentTime = 0;
        }});
        window.currentPlayingAudio = null;
    }}
    
    // ステータス音楽を再生（境界値問題修正版）
    function playStatusMusic(statusKey) {{
        if (!window.musicSystemEnabled) return;
        
        console.log('音楽切り替え要求:', 'Current:', window.currentStatus, 'Requested:', statusKey);
        
        const targetAudio = document.getElementById('persistent-audio-' + statusKey);
        if (!targetAudio) {{
            console.log('音楽ファイルが見つかりません:', statusKey);
            document.getElementById('current-track').innerHTML = '⚠️ 音楽ファイルなし: ' + statusKey;
            return;
        }}
        
        // 同じステータスの場合
        if (window.currentStatus === statusKey) {{
            console.log('同じステータス:', statusKey);
            
            // 音楽が停止している場合は再開
            if (targetAudio.paused || targetAudio.ended) {{
                console.log('音楽が停止していたため再開:', statusKey);
                targetAudio.play().then(() => {{
                    window.currentPlayingAudio = targetAudio;
                    
                    const statusNames = {{
                        'normal': '司令部機能正常',
                        'warning': '通信障害発生',
                        'danger': '司令部半壊',
                        'critical': '陥落寸前',
                        'gameover': 'ゲームオーバー'
                    }};
                    
                    document.getElementById('current-track').innerHTML = '🎵 再生中: ' + (statusNames[statusKey] || statusKey);
            document.getElementById('current-track').style.color = '{status_color}AA';
                    document.getElementById('current-track').style.color = '{status_color}AA';
                    console.log('音楽再開成功:', statusNames[statusKey]);
                }}).catch(e => {{
                    console.log('音楽再開エラー:', e);
                    document.getElementById('current-track').innerHTML = '⚠️ 再生エラー';
                }});
            }} else {{
                console.log('音楽は正常に再生中 - 何もしない');
                // 現在再生中のオーディオ参照を更新（DOM再作成対応）
                window.currentPlayingAudio = targetAudio;
            }}
            return;
        }}
        
        console.log('ステータス変更検出 - 音楽切り替え:', window.currentStatus, '->', statusKey);
        
        // 現在の音楽を停止（ステータスが実際に変わった場合のみ）
        if (window.currentPlayingAudio) {{
            window.currentPlayingAudio.pause();
            window.currentPlayingAudio.currentTime = 0;
            console.log('前の音楽を停止');
        }}
        
        // 新しい音楽を再生
        targetAudio.play().then(() => {{
            window.currentPlayingAudio = targetAudio;
            window.currentStatus = statusKey;
            localStorage.setItem('aeons_current_status', statusKey);
            
            // ステータス表示を更新
            const statusNames = {{
                'normal': '司令部機能正常',
                'warning': '通信障害発生',
                'danger': '司令部半壊',
                'critical': '陥落寸前',
                'gameover': 'ゲームオーバー'
            }};
            
            document.getElementById('current-track').innerHTML = '🎵 再生中: ' + (statusNames[statusKey] || statusKey);
            console.log('新しい音楽再生開始:', statusNames[statusKey]);
        }}).catch(e => {{
            console.log('音楽再生エラー:', e);
            document.getElementById('current-track').innerHTML = '⚠️ 再生エラー - ブラウザが音楽をブロックしています';
        }});
    }}
    
    // ページ読み込み時の状態復元
    window.addEventListener('load', function() {{
        console.log('音楽システム状態復元開始');
        
        // UI状態を復元
        if (window.musicSystemEnabled) {{
            document.getElementById('enable-music').style.display = 'none';
            document.getElementById('disable-music').style.display = 'inline-block';
            document.getElementById('music-status').innerHTML = '🎵 音楽: 有効';
            document.getElementById('music-status').style.color = '{status_color}';
            
            // 音楽を自動再開
            setTimeout(function() {{
                playStatusMusic('{current_status_key}');
            }}, 500);
        }} else {{
            document.getElementById('enable-music').style.display = 'inline-block';
            document.getElementById('disable-music').style.display = 'none';
            document.getElementById('music-status').innerHTML = '🔇 音楽: 無効';
            document.getElementById('music-status').style.color = '{status_color}';
        }}
    }});
    
    // 即座に状態復元（loadイベントを待たない）
    setTimeout(function() {{
        if (window.musicSystemEnabled) {{
            document.getElementById('enable-music').style.display = 'none';
            document.getElementById('disable-music').style.display = 'inline-block';
            document.getElementById('music-status').innerHTML = '🎵 音楽: 有効';
            document.getElementById('music-status').style.color = '{status_color}';
            
            // 自動開始が設定されている場合
            if ({str(auto_start).lower()}) {{
                playStatusMusic('{current_status_key}');
            }}
        }}
    }}, 100);
    
    // グローバル関数として公開
    window.playStatusMusic = playStatusMusic;
    window.enableMusicSystem = enableMusicSystem;
    window.disableMusicSystem = disableMusicSystem;
    
    // ステータス変更時のみ音楽切り替え（Streamlit側から呼び出し）
    // DOM再作成対応：常に音楽状態をチェックして必要に応じて再開
    setTimeout(function() {{
        if (window.musicSystemEnabled) {{
            console.log('Streamlit再描画後の音楽状態チェック:', '{current_status_key}');
            playStatusMusic('{current_status_key}');
        }}
    }}, 200);
    
    // 現在のステータスを前回ステータスとして保存
    localStorage.setItem('aeons_previous_status', '{current_status_key}');
    
    console.log('音楽システム設定完了 - 現在ステータス: {current_status_key}');
    </script>
    """
    
    return html_code

def display_status_card(status_info, hp):
    """ステータスカードを表示"""
    if hp == 0:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #000000, #333333);
            border: 3px solid {status_info['color']};
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            text-align: center;
            color: white;
            box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        ">
            <h1 style="color: #ff4444; font-size: 3em; margin-bottom: 20px;">💀 {status_info['title']} 💀</h1>
            <p style="font-size: 1.5em; margin: 15px 0;">{status_info['description']}</p>
            <p style="font-size: 2em; color: #ff4444; margin-top: 30px;">ゲームを再開するにはリセットしてください</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {status_info['color']}22, {status_info['color']}11);
            border: 2px solid {status_info['color']};
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        ">
            <h2 style="color: {status_info['color']}; margin-bottom: 15px;">⚔️ {status_info['title']}</h2>
            <p style="margin: 10px 0;"><strong>制限:</strong> {status_info['restriction']}</p>
            <p style="margin: 10px 0;"><strong>相談時間:</strong> {status_info['consultation_time']}</p>
            <p style="margin: 10px 0; font-style: italic;">"{status_info['description']}"</p>
        </div>
        """, unsafe_allow_html=True)

# メインタブ
main_tabs = st.tabs(["⚔️ ゲーム", "🎵 BGM設定"])

# ゲームタブ
with main_tabs[0]:
    # 永続的音楽システム
    if st.session_state.uploaded_music:
        current_status = get_status_info(st.session_state.hp)
        previous_status = get_status_info(st.session_state.previous_hp)
        
        # ステータスが変わった場合に自動開始フラグを設定
        if current_status["music_key"] != previous_status["music_key"]:
            st.session_state.auto_start_music = True
        else:
            st.session_state.auto_start_music = False
        
        # 音楽システムのHTML
        music_system_html = create_persistent_music_system(
            st.session_state.uploaded_music, 
            current_status["music_key"],
            st.session_state.music_enabled,
            st.session_state.auto_start_music,
            current_status["color"]
        )
        st.components.v1.html(music_system_html, height=250)

    else:
        st.info("🎵 BGMを使用するには、「BGM設定」タブで音楽ファイルをアップロードしてください。")

    st.markdown("---")

    # HP表示
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        current_status = get_status_info(st.session_state.hp)
        hp_color = current_status["color"]
        
        if st.session_state.hp > 0:
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <h1 style="font-size: 5em; margin: 0; color: {hp_color}; text-shadow: 0 0 10px {hp_color}66;">
                    {st.session_state.hp}
                </h1>
                <p style="font-size: 1.5em; margin: 10px 0; color: {hp_color};">HP / 30</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <h1 style="font-size: 5em; margin: 0; color: {hp_color}; text-shadow: 0 0 15px #FF0000;">
                    0
                </h1>
                <p style="font-size: 1.5em; margin: 10px 0; color: {hp_color};">DEFEATED</p>
            </div>
            """, unsafe_allow_html=True)

    # ステータス表示
    display_status_card(current_status, st.session_state.hp)

    # コントロールボタン
    st.markdown("---")
    current_status = get_status_info(st.session_state.hp)
    
    # ステータス色に応じた動的スタイル
    button_style = f"""
    <style>
    .stButton > button {{
        background: linear-gradient(135deg, {current_status["color"]}, {current_status["color"]}CC) !important;
        color: white !important;
        border: 2px solid {current_status["color"]} !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 12px {current_status["color"]}44 !important;
        transition: all 0.3s ease !important;
    }}
    .stButton > button:hover {{
        background: linear-gradient(135deg, {current_status["color"]}EE, {current_status["color"]}) !important;
        box-shadow: 0 6px 16px {current_status["color"]}66 !important;
        transform: translateY(-2px) !important;
        border-color: {current_status["color"]} !important;
    }}
    .stButton > button:active {{
        background: linear-gradient(135deg, {current_status["color"]}, {current_status["color"]}DD) !important;
        box-shadow: 0 2px 8px {current_status["color"]}66 !important;
        transform: translateY(0px) !important;
        border-color: {current_status["color"]} !important;
        color: white !important;
    }}
    .stButton > button:focus {{
        background: linear-gradient(135deg, {current_status["color"]}, {current_status["color"]}CC) !important;
        box-shadow: 0 4px 12px {current_status["color"]}44 !important;
        border-color: {current_status["color"]} !important;
        color: white !important;
        outline: none !important;
    }}
    .stButton > button:disabled {{
        background: #666666 !important;
        color: #999999 !important;
        border-color: #666666 !important;
        box-shadow: none !important;
    }}
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🩸 ダメージ -1", use_container_width=True, disabled=(st.session_state.hp <= 0)):
            st.session_state.previous_hp = st.session_state.hp
            st.session_state.hp = max(0, st.session_state.hp - 1)
            st.rerun()

    with col2:
        if st.button("💖 回復 +1", use_container_width=True, disabled=(st.session_state.hp >= 30)):
            st.session_state.previous_hp = st.session_state.hp
            st.session_state.hp = min(30, st.session_state.hp + 1)
            st.rerun()

    with col3:
        if st.button("🔄 リセット", use_container_width=True):
            st.session_state.previous_hp = st.session_state.hp
            st.session_state.hp = 30
            st.rerun()

# BGM設定タブ
with main_tabs[1]:
    st.subheader("🎵 ステータス別BGM設定")
    st.info("💡 **初期設定**: 各ステージ用の音楽ファイルをアップロードしてください。設定後は「ゲーム」タブでプレイしてください。")
    
    music_tabs = st.tabs(["司令部正常", "通信障害", "司令部半壊", "陥落寸前", "ゲームオーバー"])

    music_keys = ["normal", "warning", "danger", "critical", "gameover"]
    music_labels = [
        "司令部機能正常 (HP 26-30)",
        "通信障害発生 (HP 16-25)", 
        "司令部半壊 (HP 6-15)",
        "陥落寸前 (HP 1-5)",
        "ゲームオーバー (HP 0)"
    ]

    for i, (tab, key, label) in enumerate(zip(music_tabs, music_keys, music_labels)):
        with tab:
            uploaded_file = st.file_uploader(
                f"MP3ファイルをアップロード", 
                type=['mp3'], 
                key=f"music_{key}"
            )
            if uploaded_file is not None:
                # ファイルをセッション状態に保存
                st.session_state.uploaded_music[key] = uploaded_file
                st.success(f"✅ {label} 用の音楽がアップロードされました")                
            elif key in st.session_state.uploaded_music:
                st.info(f"📁 {label} 用の音楽ファイルが設定済み")
    
    # 設定完了状況
    st.markdown("---")
    st.subheader("📊 設定状況")
    
    total_files = len(music_keys)
    uploaded_files = len(st.session_state.uploaded_music)
    
    progress = uploaded_files / total_files
    st.progress(progress)
    st.write(f"**設定済み**: {uploaded_files}/{total_files} ファイル ({progress*100:.0f}%)")
    
    if uploaded_files == total_files:
        st.success("🎉 **全ての音楽ファイルが設定完了しました！** 「ゲーム」タブでプレイを開始してください。")
    elif uploaded_files > 0:
        st.info(f"⚠️ **{total_files - uploaded_files}個のファイルが未設定です。** 残りのファイルもアップロードすることをお勧めします。")
    else:
        st.warning("🎵 **音楽ファイルがアップロードされていません。** 上記のタブでファイルをアップロードしてください。")
