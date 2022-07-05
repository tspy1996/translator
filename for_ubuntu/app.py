import streamlit as st
# from translator_google import googleTranslator
from translator_argo import argoTranslator
# from execute_translator import exe


# streamlit run app.py
st.set_page_config(layout="wide")
def _max_width_():
    max_width_str = f"max-width: 1400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

_max_width_()

st.title("🔠 Offline Translator")

# translator default setting
with st.container():
    col11, col12 = st.columns([1, 1])
    with col11:
        src = st.radio(
            "指定輸入語言",
            # ["自動偵測", "英文","日文","中文"],
            ["英文","日文","中文"],
            horizontal =True,
            help="",
        )
        # 顯示偵測語言或輸入語言

    with col12:
        dest = st.radio(
            '指定翻譯語言',
            options=["中文", "英文","日文"],
            horizontal =True,
            help="",
        )
# language map
lang_dict = {"自動偵測":"auto","中文":"zh-TW", "英文":"en", "日文":"ja"}

with st.form("input_form"):
    col21, col22 = st.columns([1, 1])
    with col21:
        doc = st.text_area(
            "",
            placeholder ="請輸入欲翻譯文字",
            height=200,
        )

        MAX_WORDS = 5000
        import re
        res = len(re.findall(r"\w+", doc))
        if res > MAX_WORDS:
            st.warning(
                "⚠️ Your text contains "
                + str(res)
                + " words."
                + " Only the first 500 words will be reviewed. Stay tuned as increased allowance is coming! 😊"
            )
            doc = doc[:MAX_WORDS]
        md_words_num = f"""<p style="font-family:Courier; color:Gray; font-size: 15px;">字數：{str(res)}/5000</p>"""
        st.markdown(md_words_num, unsafe_allow_html=True)
        # st.write("字數："+str(res)+"/5000")
        submitted = st.form_submit_button("✨Translate!")
            

    with col22:
        if submitted:
            # translate_result = googleTranslator(doc, lang_dict[src], lang_dict[dest])
            translate_result = argoTranslator(doc, lang_dict[src], lang_dict[dest])
#             translate_result = exe(doc, lang_dict[src], lang_dict[dest])
            st.write(" ")
            st.write(" ")
            st.write(translate_result)
        else:
            st.write("翻譯結果...")
