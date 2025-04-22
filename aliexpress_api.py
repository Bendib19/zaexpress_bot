import os

def get_product_info(url):
    # نموذج بسيط فقط، لازم تربط API حقيقي هنا
    return f"معلومات المنتج: {url}\n\nسعر: 10.99$\nتخفيض: 5%\nرابط مخفض: {url}?aff_id=" + os.getenv("APP_KEY")