import streamlit as st
import base64
import time

# セッション状態の初期化

if “hp” not in st.session_state:
st.session_state.hp = 30
if “previous_hp” not in st.session_state:
st.session_state.previous_hp = 30
if “uploaded_music” not in st.session_state:
st.session_state.uploaded_music = {}
if “music_enabled” not in st.session_state:
st.session_state.music_enabled = False
if “auto_start_music” not in st.session_state:
st.session_state.auto_start_music = False

def get_status_info(hp):
“”“HPに基づいてステータス情報を返す”””
if hp >= 26:
return {
“title”: “グレーブホールド機能正常「黎明の静寂」”,
“restriction”: “すべて公開”,
“consultation_time”: “無制限”,
“description”: “破孔魔術による防衛システムは万全、破孔魔術師たちの連携も完璧だ。グレーブホールドの防衛は保たれ、希望の灯は消えていない。”,
“color”: “#4CAF50”,  # 緑
“music_key”: “normal”
}
elif hp >= 16:
return {
“title”: “ネメシス襲来「響く警鐘」”,
“restriction”: “呪文カードのみ公開”,
“consultation_time”: “攻撃対象の相談のみ”,
“description”: “ネメシスたちによる損害が出始めた。辺りで警鐘が鳴り響く。瓦礫がグレーブホールドの一部を塞ぎ、補給路が寸断された。破孔魔術師たちは戦闘計画だけを必死に共有する”,
“color”: “#FF9800”,  # オレンジ
“music_key”: “warning”
}
elif hp >= 6:
return {
“title”: “グレーブホールド半壊「崩れゆく防壁」”,
“restriction”: “手札公開なし”,
“consultation_time”: “数値のコミュニケーションのみ”,
“description”: “ネメシスたちの攻撃により天井が崩落し、煙と粉塵が視界を奪う。もはや互いの顔も見えない。声だけが頼りだ。”,
“color”: “#F44336”,  # 赤
“music_key”: “danger”
}
elif hp >= 1:
return {
“title”: “グレーブホールド陥落寸前「最後の抵抗」”,
“restriction”: “手札公開なし”,
“consultation_time”: “一切の相談禁止”,
“description”: “もはや声は届かない。轟音と絶叫のみ。破孔魔術師たちは孤立し、本能と経験を頼りに呪文を紡ぐ。これが、グレイブホールド最後かもしれない…”,
“color”: “#9C27B0”,  # 紫
“music_key”: “critical”
}
else:
return {
“title”: “GAME OVER”,
“restriction”: “ゲーム終了”,
“consultation_time”: “ゲーム終了”,
“description”: “グレイブホールドは陥落した。破孔魔術師たちの抵抗も虚しく、ネメシスの支配が始まった…”,
“color”: “#000000”,  # 黒
“music_key”: “gameover”
}

def create_persistent_music_system(music_data, current_status_key, music_enabled, auto_start, status_color):
“”“iOS対応永続的音楽切り替えシステム”””

```
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
        
        <!-- iOS対応：初期化ボタン -->
        <button id="init-audio" onclick="initializeAudioContext()" style="padding: 10px 20px; background: #2196F3; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 5px; font-size: 16px;">
            🎵 音楽システム初期化 (iOS対応)
        </button>
        
        <!-- フォールバック：シンプル初期化 -->
        <button id="simple-init" onclick="simpleInitialization()" style="padding: 10px 20px; background: #9C27B0; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 5px; font-size: 16px; display: none;">
            🔧 シンプル初期化
        </button>
        
        <button id="enable-music" onclick="enableMusicSystem()" style="padding: 10px 20px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 5px; font-size: 16px; display: none;">
            🎵 音楽システム有効化
        </button>
        <button id="disable-music" onclick="disableMusicSystem()" style="padding: 10px 20px; background: #f44336; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 5px; font-size: 16px; display: none;">
            🔇 音楽システム無効化
        </button>
        
        <!-- 手動再生ボタン (iOS用フォールバック) -->
        <button id="manual-play" onclick="manualPlayCurrentMusic()" style="padding: 10px 20px; background: #FF9800; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 5px; font-size: 16px; display: none;">
            🔄 手動再生
        </button>
        
        <div id="music-status" style="margin-top: 10px; font-weight: bold; font-size: 18px;">🔇 音楽: 未初期化</div>
        <div id="current-track" style="margin-top: 5px; color: #666; font-size: 16px;">再生中: なし</div>
        <div id="debug-info" style="margin-top: 5px; color: #666; font-size: 12px; font-family: monospace;">デバッグ情報: 待機中</div>
        <div id="ios-notice" style="margin-top: 10px; color: #FF9800; font-size: 14px;">📱 iOS/iPadの場合：まず「音楽システム初期化」をタップしてください</div>
    </div>
    
    <!-- 永続化された音楽要素 -->
    <div id="persistent-audio-elements" style="display: none;">
"""

# 各音楽要素を追加
for key, b64_data in js_music_data.items():
    html_code += f"""
        <audio id="persistent-audio-{key}" loop preload="auto" data-key="{key}" muted>
            <source src="data:audio/mp3;base64,{b64_data}" type="audio/mp3">
        </audio>
    """

html_code += f"""
    </div>
</div>

<script>
// グローバル状態管理
if (!window.musicSystemInitialized) {{
    window.musicSystemEnabled = localStorage.getItem('aeons_music_enabled') === 'true';
    window.audioContextInitialized = false;
    window.currentPlayingAudio = null;
    window.currentStatus = localStorage.getItem('aeons_current_status') || '{current_status_key}';
    window.musicSystemInitialized = true;
    window.pendingStatusChange = null;
    
    console.log('音楽システム初期化完了');
}}

// iOS対応：Audio Context初期化
function initializeAudioContext() {{
    console.log('Audio Context初期化開始');
    
    // 全てのオーディオ要素を取得
    const audioElements = document.querySelectorAll('[id^="persistent-audio-"]');
    let initSuccessCount = 0;
    
    // 各オーディオ要素を順次初期化
    audioElements.forEach((audio, index) => {{
        // ミュートを解除
        audio.muted = false;
        
        // 短時間再生して停止（iOS Audio Context有効化）
        const playPromise = audio.play();
        if (playPromise !== undefined) {{
            playPromise.then(() => {{
                console.log(`オーディオ ${{audio.id}} 初期化成功`);
                setTimeout(() => {{
                    audio.pause();
                    audio.currentTime = 0;
                }}, 100);
                
                initSuccessCount++;
                if (initSuccessCount === audioElements.length) {{
                    onAudioInitializationComplete();
                }}
            }}).catch(error => {{
                console.error(`オーディオ ${{audio.id}} 初期化失敗:`, error);
                initSuccessCount++;
                if (initSuccessCount === audioElements.length) {{
                    onAudioInitializationComplete();
                }}
            }});
        }}
    }});
    
    if (audioElements.length === 0) {{
        console.log('音楽ファイルが見つかりません');
        document.getElementById('music-status').innerHTML = '⚠️ 音楽ファイルが見つかりません';
        return;
    }}
    
    window.audioContextInitialized = true;
}}

// 初期化完了時の処理
function onAudioInitializationComplete() {{
    console.log('全音楽ファイル初期化完了');
    
    // UIを更新
    document.getElementById('init-audio').style.display = 'none';
    document.getElementById('enable-music').style.display = 'inline-block';
    document.getElementById('manual-play').style.display = 'inline-block';
    document.getElementById('ios-notice').style.display = 'none';
    document.getElementById('music-status').innerHTML = '✅ 初期化完了 - 音楽システムを有効化してください';
    document.getElementById('music-status').style.color = '{status_color}';
    
    // 自動的に音楽システムを有効化
    setTimeout(() => {{
        enableMusicSystem();
    }}, 500);
}}

// 音楽システム有効化
function enableMusicSystem() {{
    if (!window.audioContextInitialized) {{
        document.getElementById('music-status').innerHTML = '⚠️ 先に音楽システムを初期化してください';
        return;
    }}
    
    window.musicSystemEnabled = true;
    localStorage.setItem('aeons_music_enabled', 'true');
    
    document.getElementById('enable-music').style.display = 'none';
    document.getElementById('disable-music').style.display = 'inline-block';
    document.getElementById('music-status').innerHTML = '🎵 音楽: 有効';
    document.getElementById('music-status').style.color = '{status_color}';
    
    // 現在のステータスの音楽を再生
    playStatusMusic('{current_status_key}');
    
    console.log('音楽システム有効化完了');
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
    
    stopAllMusic();
    console.log('音楽システム無効化完了');
}}

// 全音楽停止
function stopAllMusic() {{
    document.querySelectorAll('[id^="persistent-audio-"]').forEach(function(audio) {{
        audio.pause();
        audio.currentTime = 0;
    }});
    window.currentPlayingAudio = null;
}}

// 手動再生（iOS用フォールバック）
function manualPlayCurrentMusic() {{
    if (!window.musicSystemEnabled) {{
        document.getElementById('music-status').innerHTML = '⚠️ 音楽システムが無効です';
        return;
    }}
    
    console.log('手動再生実行:', '{current_status_key}');
    playStatusMusic('{current_status_key}', true);
}}

// ステータス音楽再生（iOS対応版）
function playStatusMusic(statusKey, forcePlay = false) {{
    if (!window.audioContextInitialized) {{
        console.log('Audio Context未初期化');
        window.pendingStatusChange = statusKey;
        return;
    }}
    
    if (!window.musicSystemEnabled && !forcePlay) {{
        console.log('音楽システム無効');
        return;
    }}
    
    console.log('音楽切り替え要求:', statusKey);
    
    const targetAudio = document.getElementById('persistent-audio-' + statusKey);
    if (!targetAudio) {{
        console.log('音楽ファイルが見つかりません:', statusKey);
        document.getElementById('current-track').innerHTML = '⚠️ 音楽ファイルなし: ' + statusKey;
        return;
    }}
    
    // 同じステータスで既に再生中の場合
    if (window.currentStatus === statusKey && window.currentPlayingAudio === targetAudio && !targetAudio.paused) {{
        console.log('同じ音楽が既に再生中');
        return;
    }}
    
    // 現在の音楽を停止
    if (window.currentPlayingAudio && window.currentPlayingAudio !== targetAudio) {{
        window.currentPlayingAudio.pause();
        window.currentPlayingAudio.currentTime = 0;
        console.log('前の音楽停止');
    }}
    
    // 新しい音楽を再生
    targetAudio.muted = false;
    const playPromise = targetAudio.play();
    
    if (playPromise !== undefined) {{
        playPromise.then(() => {{
            window.currentPlayingAudio = targetAudio;
            window.currentStatus = statusKey;
            localStorage.setItem('aeons_current_status', statusKey);
            
            const statusNames = {{
                'normal': '黎明の静寂',
                'warning': '響く警鐘',
                'danger': '崩れゆく防壁',
                'critical': '最後の抵抗',
                'gameover': 'ゲームオーバー'
            }};
            
            document.getElementById('current-track').innerHTML = '🎵 再生中: ' + (statusNames[statusKey] || statusKey);
            document.getElementById('current-track').style.color = '{status_color}AA';
            console.log('音楽再生成功:', statusNames[statusKey]);
        }}).catch(error => {{
            console.error('音楽再生エラー:', error);
            document.getElementById('current-track').innerHTML = '⚠️ 再生エラー - 手動再生ボタンをお試しください';
            document.getElementById('current-track').style.color = '#FF0000';
            
            // 手動再生ボタンを表示
            document.getElementById('manual-play').style.display = 'inline-block';
        }});
    }}
}}

// ページ読み込み時の処理
window.addEventListener('load', function() {{
    console.log('ページ読み込み完了');
    restoreUIState();
}});

// UI状態復元
function restoreUIState() {{
    if (window.audioContextInitialized) {{
        document.getElementById('init-audio').style.display = 'none';
        document.getElementById('ios-notice').style.display = 'none';
        document.getElementById('manual-play').style.display = 'inline-block';
        
        if (window.musicSystemEnabled) {{
            document.getElementById('enable-music').style.display = 'none';
            document.getElementById('disable-music').style.display = 'inline-block';
            document.getElementById('music-status').innerHTML = '🎵 音楽: 有効';
            document.getElementById('music-status').style.color = '{status_color}';
            
            // 音楽を再開（iOS対応）
            setTimeout(() => {{
                if (window.pendingStatusChange) {{
                    playStatusMusic(window.pendingStatusChange);
                    window.pendingStatusChange = null;
                }} else {{
                    playStatusMusic('{current_status_key}');
                }}
            }}, 1000);
        }} else {{
            document.getElementById('enable-music').style.display = 'inline-block';
            document.getElementById('disable-music').style.display = 'none';
            document.getElementById('music-status').innerHTML = '🔇 音楽: 無効';
            document.getElementById('music-status').style.color = '{status_color}';
        }}
    }} else {{
        document.getElementById('init-audio').style.display = 'inline-block';
        document.getElementById('enable-music').style.display = 'none';
        document.getElementById('disable-music').style.display = 'none';
        document.getElementById('manual-play').style.display = 'none';
        document.getElementById('music-status').innerHTML = '🔇 音楽: 未初期化';
        document.getElementById('music-status').style.color = '{status_color}';
    }}
}}

// 即座に状態復元
setTimeout(restoreUIState, 100);

// HP変更時の音楽切り替え（Streamlit側から呼び出し）
setTimeout(function() {{
    console.log('Streamlit再描画後チェック:', '{current_status_key}');
    if (window.musicSystemEnabled && window.audioContextInitialized) {{
        playStatusMusic('{current_status_key}');
    }}
}}, 300);

// グローバル関数として公開
window.playStatusMusic = playStatusMusic;
window.enableMusicSystem = enableMusicSystem;
window.disableMusicSystem = disableMusicSystem;
window.initializeAudioContext = initializeAudioContext;
window.simpleInitialization = simpleInitialization;
window.manualPlayCurrentMusic = manualPlayCurrentMusic;

console.log('音楽システム設定完了 - iOS対応版');
</script>
"""

return html_code
```

def display_status_card(status_info, hp):
“”“ステータスカードを表示”””
if hp == 0:
st.markdown(f”””
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
<h1 style="color: #ff4444; font-size: 3em; margin-bottom: 20px;">💀 {status_info[‘title’]} 💀</h1>
<p style="font-size: 1.5em; margin: 15px 0;">{status_info[‘description’]}</p>
<p style="font-size: 2em; color: #ff4444; margin-top: 30px;">ゲームを再開するにはリセットしてください</p>
</div>
“””, unsafe_allow_html=True)
else:
st.markdown(f”””
<div style="
background: linear-gradient(135deg, {status_info['color']}22, {status_info['color']}11);
border: 2px solid {status_info['color']};
border-radius: 10px;
padding: 20px;
margin: 20px 0;
box-shadow: 0 4px 16px rgba(0,0,0,0.1);
">
<h2 style="color: {status_info['color']}; margin-bottom: 15px;">⚔️ {status_info[‘title’]}</h2>
<p style="margin: 10px 0;"><strong>制限:</strong> {status_info[‘restriction’]}</p>
<p style="margin: 10px 0;"><strong>相談時間:</strong> {status_info[‘consultation_time’]}</p>
<p style="margin: 10px 0; font-style: italic;">”{status_info[‘description’]}”</p>
</div>
“””, unsafe_allow_html=True)

# メインタブ

main_tabs = st.tabs([“⚔️ ゲーム”, “🎵 BGM設定”])

# ゲームタブ

with main_tabs[0]:
# iOS対応音楽システム
if st.session_state.uploaded_music:
current_status = get_status_info(st.session_state.hp)
previous_status = get_status_info(st.session_state.previous_hp)

```
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
    st.components.v1.html(music_system_html, height=350)

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
```

# BGM設定タブ

with main_tabs[1]:
st.subheader(“🎵 ステータス別BGM設定”)
st.info(“💡 **初期設定**: 各ステージ用の音楽ファイルをアップロードしてください。設定後は「ゲーム」タブでプレイしてください。”)

```
# iOS使用時の注意事項
st.warning("📱 **iOS/iPad使用時の注意**: BGMを使用するには、ゲームタブで「音楽システム初期化」ボタンを最初にタップしてください。")

music_tabs = st.tabs(["黎明の静寂", "響く警鐘", "崩れゆく防壁", "最後の抵抗", "ゲームオーバー"])

music_keys = ["normal", "warning", "danger", "critical", "gameover"]
music_labels = [
    "黎明の静寂 (HP 26-30)",
    "響く警鐘 (HP 16-25)", 
    "崩れゆく防壁 (HP 6-15)",
    "最後の抵抗 (HP 1-5)",
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
```