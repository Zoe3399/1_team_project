import streamlit as st
from streamlit.components.v1 import html

def show():
    st.markdown(
        '''
        <style>
        .big-title { font-size:2.5rem; font-weight:700; margin-bottom:0.7em; }
        .desc { font-size:1.2rem; color:#aaa; margin-bottom:2em; }
        .search-row { display:flex; gap:8px; align-items:center; margin-bottom: 1em; }
        .filter-row { display:flex; gap:12px; margin: 1em 0 1.5em 0;}
        .filter-btn {
            background: #222; color:#eee; border-radius:20px; padding:7px 22px;
            border:none; font-weight:600; font-size:1.02rem; transition:0.2s;
            cursor:pointer;
        }
        .filter-btn.selected { background:#ff5252; color:white; }
        .info-window { padding:10px 12px; font-size:0.95rem; }
        </style>
        ''', unsafe_allow_html=True
    )

    # 타이틀, 설명
    st.markdown('<div class="big-title">🗺️ 교통사고 위험 지도</div>', unsafe_allow_html=True)
    st.markdown('<div class="desc">실시간 교통사고 위험정보를 지도에서 한눈에 확인하세요.<br>위험도/사고유형 등 다양한 조건으로 검색·필터가 가능합니다.</div>', unsafe_allow_html=True)

    # 1. 검색창
    search_col1, search_col2 = st.columns([6,1])
    with search_col1:
        search = st.text_input("검색", value=st.session_state.get("search", ""), placeholder="지역, 주소, 장소를 입력하세요 (예: 강남역)", label_visibility="collapsed")
    with search_col2:
        search_btn = st.button("검색")
    # 검색어 세션에 저장 (검색버튼 안눌러도 바로 저장)
    st.session_state["search"] = search

    if search_btn:
        st.info(f"‘{search}’ 위치로 이동 (예시, 실제 이동은 미구현)")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. 위험도 필터 토글(단일 선택)
    st.markdown("#### 🔍 위험도 색상 안내:  🔴 고  🟠 중  🟢 저", unsafe_allow_html=True)
    filter_options = ["전체", "고", "중", "저"]
    selected = st.session_state.get("risk_filter", "전체")

    filter_cols = st.columns(len(filter_options))
    for idx, opt in enumerate(filter_options):
        is_selected = (selected == opt)
        if filter_cols[idx].button(opt, key=f"risk_{opt}", help=f"{opt} 위험도만 보기", use_container_width=True):
            st.session_state["risk_filter"] = opt
            selected = opt

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. 카카오맵 Embed
    js_key = "04ffcee5b4d4d2b87fca2e94cd2d4e69"
    markers = [
        {"lat": 37.5665, "lng": 126.9780, "risk": "고", "title": "서울시청", "desc": "사고다발, 위험도: 고"},
        {"lat": 37.5700, "lng": 126.9830, "risk": "중", "title": "북촌", "desc": "위험도: 중"},
        {"lat": 37.5600, "lng": 126.9750, "risk": "저", "title": "명동", "desc": "위험도: 저"},
    ]
    color_map = {"고":"red", "중":"orange", "저":"green"}
    if selected and selected != "전체":
        filtered_markers = [m for m in markers if m["risk"] == selected]
    else:
        filtered_markers = markers

    marker_js = ""
    for m in filtered_markers:
        color = color_map.get(m["risk"], "blue")
        marker_js += f"""
            var marker = new kakao.maps.Marker({{
                position: new kakao.maps.LatLng({m['lat']},{m['lng']}),
                map: map,
                title: "{m['title']}"
            }});
            var iwContent = '<div class="info-window"><b>{m['title']}</b><br>{m['desc']}</div>';
            var infowindow = new kakao.maps.InfoWindow({{ content: iwContent }});
            kakao.maps.event.addListener(marker, 'click', function() {{
                infowindow.open(map, marker);
            }});
        """

    map_html = f"""
    <div style="margin-top:20px; border-radius:12px; overflow:hidden;">
      <div id="map" style="width:100%; height:560px;"></div>
    </div>
    <script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey={js_key}&autoload=false"></script>
    <script>
        kakao.maps.load(function() {{
            var container = document.getElementById('map');
            var options = {{
                center: new kakao.maps.LatLng(37.5665, 126.9780),
                level: 5
            }};
            var map = new kakao.maps.Map(container, options);
            {marker_js}
        }});
    </script>
    """
    html(map_html, height=500, scrolling=False)

    st.caption("🛈 지도 위 마커를 클릭하면 해당 위치의 위험도 정보를 확인할 수 있습니다. 현재는 더미 데이터를 기반으로 표시됩니다.")

    st.markdown("<br>", unsafe_allow_html=True)

    # 초기화 버튼 - 검색어, 필터 모두 초기화
    def reset_filters():
        st.session_state["risk_filter"] = "전체"
        st.session_state["search"] = ""

    st.button("초기화", on_click=reset_filters)