from bs4 import BeautifulSoup
import requests
import streamlit as st

st.set_page_config(
    page_title="استخراج اسم وسعر المنتج", page_icon="🛍️", layout="centered"
)

st.title("🛍️ استخراج بيانات المنتجات أونلاين")
st.write("أدخل رابط المنتج أدناه لمعرفة اسمه وسعره:")

# مربع ادخال الرابط
url = st.text_input("ألقِ رابط المنتج هنا:")

if st.button("استعلام"):
  if url:
    with st.spinner("جاري جلب البيانات..."):
      try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # جلب عنوان الصفحة كاسم للمنتج
        product_name = (
            soup.title.string.strip() if soup.title else "غير معروف"
        )

        # محاولة البحث عن السعر باستخدام العناصر الشائعة
        price_element = soup.find(class_=lambda x: x and "price" in x.lower())
        product_price = (
            price_element.get_text().strip()
            if price_element
            else "لم يتم العثور على السعر تلقائياً"
        )

        st.success("تم جلب البيانات بنجاح!")
        st.markdown(f"اسم المنتج: {product_name}")
        st.markdown(f"السعر: {product_price}")

      except Exception as e:
        st.error(f"حدث خطأ أثناء جلب البيانات: {e}")
  else:
    st.warning("الرجاء إدخال رابط صالح أولاً.")