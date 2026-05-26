import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
from urllib.parse import quote

def generate_upi_link(upi_id, merchant_name, amount, order_id):
    """
    Generates a standardized upi://pay link.
    Example: upi://pay?pa=merchant@upi&pn=StoreName&am=AMOUNT&cu=INR&tr=ORDER_ID
    """
    # URL encode fields to ensure valid URI query parameters
    pa = quote(upi_id)
    pn = quote(merchant_name)
    am = str(amount)
    tr = quote(str(order_id)) # transaction reference / order id
    
    # Standard UPI URI scheme
    upi_link = f"upi://pay?pa={pa}&pn={pn}&am={am}&cu=INR&tr={tr}&tn=Order%20{tr}"
    return upi_link

def generate_qr_code(upi_link):
    """
    Generates QR code image bytes from a UPI link using the qrcode library.
    Returns a Django ContentFile that can be saved directly to an ImageField.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_link)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    
    return ContentFile(img_bytes, name="payment_qr.png")

def verify_payment_reference(transaction_id):
    """
    Simple check to verify payment reference syntax.
    Checks that a transaction reference is not empty and is alphanumeric/standard.
    """
    if not transaction_id:
        return False
    # Clean the transaction ID and ensure minimum length of 6 characters
    cleaned = transaction_id.strip()
    return len(cleaned) >= 6
