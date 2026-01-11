import streamlit as st

import re

st.set_page_config(page_title="Table Extractor", layout="centered")

st.title("📄 استخراج أسماء الجداول")

st.write("ارفع ملف نصي (TXT) وسيتم عرض أسماء الجداول الموجودة فيه مباشرة")

uploaded_file = st.file_uploader("📤 اختر ملف txt", type=["txt"])

if uploaded_file is not None:

    text = uploaded_file.read().decode("utf-8")

    text_clean = re.sub(r'--.*', '', text)

    text_clean = re.sub(r'/\*.*?\*/', '', text_clean, flags=re.DOTALL)

    tables = []

    def clean_table_name(name):

        name = name.split()[0]

        name = re.split(r'[#"(\}]', name)[0]

        return name.strip()

    from_pattern = r'\bFROM\s+([^\s;]+(?:\s*,\s*[^\s;]+)*)'

    from_matches = re.findall(from_pattern, text_clean, re.IGNORECASE)

    for part in from_matches:

        for t in part.split(','):

            t = t.strip()

            if t and not t.startswith('('):

                tables.append(clean_table_name(t))

    join_pattern = r'\bJOIN\s+([^\s\(\);]+)'

    join_matches = re.findall(join_pattern, text_clean, re.IGNORECASE)

    for t in join_matches:

        if not t.startswith('('):

            tables.append(clean_table_name(t))

    tables_unique = list(dict.fromkeys(tables))

    st.success(f"✅ تم استخراج {len(tables_unique)} جدول")

    st.subheader("📋 أسماء الجداول")

    for table in tables_unique:

        st.write(table)

    st.download_button(

        label="⬇️ تحميل أسماء الجداول",

        data="\n".join(tables_unique),

        file_name="tables_list.txt",

        mime="text/plain"

    )
 