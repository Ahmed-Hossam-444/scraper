from bs4 import BeautifulSoup
import requests
import streamlit as st

st.set_page_config(
    page_title="استخراج اسم وسعر المنتج", page_icon="🛍️", layout="centered"
)

st.title("🛍️ استخراج بيانات المنتجات أونلاين")
st.write("أدخل رابط المنتج أدناه لمعرفة اسمه وسعره:")

url = st.text_input("ألقِ رابط المنتج هنا:")

if st.button("استعلام"):
  if url:
    with st.spinner("جاري جلب البيانات..."):
      try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                " (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # 1. جلب اسم المنتج من العنوان أو وسم h1 الرئيسي
        product_name = "غير معروف"
        if soup.find("h1"):
          product_name = soup.find("h1").get_text().strip()
        elif soup.title:
          product_name = soup.title.string.strip()

        # 2. محاولات متعددة للبحث عن السعر بناءً على الأنماط الشهيرة في المتاجر
        product_price = None

        # محاولة البحث عن كلاسات تحتوي على كلمة price أو amount أو current-price
        price_tags = soup.find_all(
            ["span", "div", "p"],
            class_=lambda x: x
            and any(
                p in x.lower() for p in ["price", "amount", "curprice", "sum"]
            ),
        )

        for tag in price_tags:
          text = tag.get_text().strip()
          # التأكد أن النص يحتوي على أرقام أو رموز عملات ليكون سعراً حقيقياً
          if any(char.isdigit() for char in text) and len(text) < 20:
            product_price = text
            break

        if not product_price:
          product_price = (
              "تعذر استخراج السعر تلقائياً (الموقع محمي أو متغير التصميم)"
          )

        st.success("تم فحص الرابط بنجاح!")
        st.markdown(f"اسم المنتج: {product_name}")
        st.markdown(f"السعر المستنتج: {product_price}")

      except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال بالرابط: {e}")
  else:
    st.warning("الرجاء إدخال رابط صالح أولاً.")
