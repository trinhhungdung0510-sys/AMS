#!/usr/bin/env python3
"""Build TIN NGHIA AMS Sales Deck — professional 16:9 PowerPoint."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

# Brand palette
GREEN = RGBColor(0x0B, 0x6B, 0x1B)
ORANGE = RGBColor(0xF3, 0x6A, 0x10)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x6B, 0x72, 0x80)
LIGHT_GRAY = RGBColor(0xF3, 0xF4, 0xF6)
DARK = RGBColor(0x1F, 0x29, 0x37)
MID_GRAY = RGBColor(0xE5, 0xE7, 0xEB)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
IMG_DIR = Path(__file__).parent / "images"
OUTPUT = Path(__file__).parent / "TIN_NGHIA_AMS_Sales_Deck.pptx"

FONT = "Arial"
FONT_TITLE = "Arial"


def rgb(hex_str: str) -> RGBColor:
    h = hex_str.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def blank_slide(prs: Presentation):
    layout = prs.slide_layouts[6]  # blank
    return prs.slides.add_slide(layout)


def set_bg(slide, color=WHITE):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, left, top, width, height, fill_color, line_color=None, radius=False):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(shape_type, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape


def add_text_box(slide, left, top, width, height, text, size=18, bold=False,
                 color=DARK, align=PP_ALIGN.LEFT, font=FONT):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.name = font
    p.font.color.rgb = color
    p.alignment = align
    return box


def add_bullet_list(slide, left, top, width, height, items, size=16, color=DARK,
                    bullet="▸", spacing=1.2):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"{bullet}  {item}"
        p.font.size = Pt(size)
        p.font.name = FONT
        p.font.color.rgb = color
        p.space_after = Pt(size * spacing * 0.45)
    return box


def add_brand_header(slide, title: str):
    """Green accent bar + slide title."""
    add_rect(slide, Inches(0), Inches(0), SLIDE_W, Inches(0.12), GREEN)
    add_text_box(
        slide, Inches(0.6), Inches(0.35), Inches(10), Inches(0.7),
        title, size=28, bold=True, color=GREEN, font=FONT_TITLE,
    )
    add_rect(slide, Inches(0.6), Inches(1.05), Inches(1.2), Inches(0.06), ORANGE)


def add_brand_footer(slide):
    add_rect(slide, Inches(0), Inches(7.15), SLIDE_W, Inches(0.35), LIGHT_GRAY)
    add_text_box(
        slide, Inches(0.6), Inches(7.18), Inches(4), Inches(0.3),
        "TIN NGHIA ", size=11, bold=True, color=GREEN,
    )
    # AMS in orange — combined in one box for simplicity
    add_text_box(
        slide, Inches(0.6), Inches(7.18), Inches(12), Inches(0.3),
        "TIN NGHIA AMS  |  AI Giám sát An toàn Sinh học 24/7", size=11, bold=False, color=GRAY,
    )


def add_image(slide, filename, left, top, width, height):
    path = IMG_DIR / filename
    if path.exists():
        slide.shapes.add_picture(str(path), left, top, width, height)
    return path.exists()


def add_icon_card(slide, left, top, width, label, icon="●", accent=GREEN):
    card = add_rect(slide, left, top, width, Inches(1.1), WHITE, accent, radius=True)
    card.shadow.inherit = False
    add_text_box(slide, left + Inches(0.15), top + Inches(0.15), width - Inches(0.3), Inches(0.4),
                 icon, size=22, bold=True, color=accent, align=PP_ALIGN.CENTER)
    add_text_box(slide, left + Inches(0.1), top + Inches(0.55), width - Inches(0.2), Inches(0.5),
                 label, size=13, bold=True, color=DARK, align=PP_ALIGN.CENTER)


def build_slide_01(prs):
    slide = blank_slide(prs)
    set_bg(slide)
    add_image(slide, "slide01_cover.png", Inches(0), Inches(0), SLIDE_W, SLIDE_H)
    # White overlay panel
    panel = add_rect(slide, Inches(0.5), Inches(1.2), Inches(5.8), Inches(5.2), WHITE, radius=True)
    panel.shadow.inherit = False

    add_text_box(slide, Inches(0.9), Inches(1.6), Inches(5), Inches(0.5),
                 "TIN NGHIA", size=22, bold=True, color=GREEN)
    add_text_box(slide, Inches(0.9), Inches(2.1), Inches(5), Inches(1.0),
                 "AMS", size=72, bold=True, color=ORANGE, font=FONT_TITLE)
    add_text_box(slide, Inches(0.9), Inches(3.2), Inches(5.2), Inches(0.8),
                 "AI GIÁM SÁT AN TOÀN SINH HỌC 24/7", size=20, bold=True, color=DARK)
    add_rect(slide, Inches(0.9), Inches(4.1), Inches(2.5), Inches(0.06), ORANGE)
    add_text_box(slide, Inches(0.9), Inches(4.4), Inches(5.2), Inches(0.6),
                 "Bảo vệ đàn heo – Bảo vệ lợi nhuận", size=18, color=GRAY)

    cta = add_rect(slide, Inches(0.9), Inches(5.3), Inches(3.2), Inches(0.65), ORANGE, radius=True)
    add_text_box(slide, Inches(0.9), Inches(5.42), Inches(3.2), Inches(0.5),
                 "Khám phá ngay →", size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)


def build_slide_02(prs):
    slide = blank_slide(prs)
    set_bg(slide, LIGHT_GRAY)
    add_brand_header(slide, "THỰC TRẠNG AN TOÀN SINH HỌC TẠI TRẠI HEO")

    items = [
        "Giám sát thủ công",
        "Không thể theo dõi liên tục",
        "Dễ bỏ sót vi phạm",
        "Nguy cơ dịch bệnh",
    ]
    for i, item in enumerate(items):
        y = Inches(1.5 + i * 1.15)
        card = add_rect(slide, Inches(0.6), y, Inches(5.5), Inches(0.95), WHITE, ORANGE, radius=True)
        add_text_box(slide, Inches(1.0), y + Inches(0.25), Inches(5), Inches(0.5),
                     f"⚠  {item}", size=18, bold=True, color=DARK)

    add_image(slide, "slide02_manual_monitoring.png", Inches(6.5), Inches(1.3), Inches(6.3), Inches(5.5))
    add_brand_footer(slide)


def build_slide_03(prs):
    slide = blank_slide(prs)
    set_bg(slide)
    add_image(slide, "slide03_disease_impact.png", Inches(6.2), Inches(0.8), Inches(6.5), Inches(5.8))
    add_brand_header(slide, "THIỆT HẠI DO DỊCH BỆNH")

    banner = add_rect(slide, Inches(0.6), Inches(1.4), Inches(5.3), Inches(1.4), ORANGE, radius=True)
    add_text_box(slide, Inches(0.8), Inches(1.6), Inches(4.9), Inches(1.1),
                 "THIỆT HẠI CÓ THỂ\nLÊN ĐẾN HÀNG TỶ ĐỒNG",
                 size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    items = ["Giảm năng suất", "Tăng tỷ lệ chết", "Tăng chi phí điều trị", "Mất lợi nhuận"]
    for i, item in enumerate(items):
        y = Inches(3.1 + i * 0.85)
        add_rect(slide, Inches(0.6), y, Inches(5.3), Inches(0.7), LIGHT_GRAY, radius=True)
        add_text_box(slide, Inches(0.9), y + Inches(0.15), Inches(5), Inches(0.5),
                     f"✕  {item}", size=16, bold=True, color=DARK)
    add_brand_footer(slide)


def build_slide_04(prs):
    slide = blank_slide(prs)
    set_bg(slide)
    add_brand_header(slide, "CÁC HÀNH VI VI PHẠM AMS PHÁT HIỆN")

    groups = [
        ("👤", "CON NGƯỜI", GREEN),
        ("🚶", "DI CHUYỂN", ORANGE),
        ("🚛", "PHƯƠNG TIỆN", GREEN),
        ("🐾", "ĐỘNG VẬT", ORANGE),
    ]
    for i, (icon, label, color) in enumerate(groups):
        x = Inches(0.6 + i * 3.1)
        add_icon_card(slide, x, Inches(1.4), Inches(2.8), label, icon, color)

    add_image(slide, "slide04_detection_groups.png", Inches(0.6), Inches(2.8), Inches(12.1), Inches(4.0))
    add_brand_footer(slide)


def build_content_slide(prs, title, items, image, subtitle=None, highlight_msg=None):
    slide = blank_slide(prs)
    set_bg(slide)
    add_brand_header(slide, title)
    if subtitle:
        add_text_box(slide, Inches(0.6), Inches(1.15), Inches(5.5), Inches(0.4),
                     subtitle, size=14, color=GRAY)

    add_bullet_list(slide, Inches(0.6), Inches(1.6 if not subtitle else 1.9),
                    Inches(5.4), Inches(4.5), items, size=17)

    if highlight_msg:
        box = add_rect(slide, Inches(0.6), Inches(5.8), Inches(5.4), Inches(0.85), ORANGE, radius=True)
        add_text_box(slide, Inches(0.8), Inches(5.95), Inches(5.0), Inches(0.6),
                     highlight_msg, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    add_image(slide, image, Inches(6.3), Inches(1.3), Inches(6.5), Inches(5.5))
    add_brand_footer(slide)


def build_slide_05(prs):
    build_content_slide(prs, "CON NGƯỜI – HÀNH VI", [
        "Không tắm trước khi vào trại",
        "Không sát trùng tay",
        "Không sát trùng chân",
        "Sai màu quần áo",
        "Người lạ vào khu sản xuất",
        "Công nhân tiếp xúc người lạ",
    ], "slide05_human_behavior.png", subtitle="AMS phát hiện:")


def build_slide_06(prs):
    build_content_slide(prs, "DI CHUYỂN – LUỒNG ĐI", [
        "Đi từ vùng bẩn sang vùng sạch",
        "Đi sai tuyến ATSH",
        "Xâm nhập vùng cấm",
    ], "slide06_movement_flow.png", subtitle="AMS phát hiện:")


def build_slide_07(prs):
    build_content_slide(prs, "XE CỘ – PHƯƠNG TIỆN", [
        "Xe chưa sát trùng",
        "Sát trùng không đủ thời gian",
        "Công nhân tiếp xúc xe bắt heo",
        "Công nhân tiếp xúc xe cám",
    ], "slide07_vehicles.png", subtitle="AMS phát hiện:")


def build_slide_08(prs):
    build_content_slide(prs, "ĐỘNG VẬT XÂM NHẬP", [
        "Chó", "Mèo", "Chim", "Chuột",
    ], "slide08_animal_intrusion.png", subtitle="AMS phát hiện:",
       highlight_msg="Động vật là nguồn mang mầm bệnh nguy hiểm")


def build_slide_09(prs):
    slide = blank_slide(prs)
    set_bg(slide)
    add_brand_header(slide, "LỘ TRÌNH PHÁT TRIỂN AMS")

    stages = [
        ("GIAI ĐOẠN 1", "AMS AN TOÀN\nSINH HỌC", [
            "Giám sát ATSH", "Phát hiện vi phạm", "Cảnh báo thời gian thực",
        ], GREEN),
        ("GIAI ĐOẠN 2", "AMS THEO DÕI\nSỨC KHỎE HEO", [
            "Heo sốt", "Heo ho", "Heo bất thường", "Heo chết",
        ], ORANGE),
        ("GIAI ĐOẠN 3", "AMS 360\nAI THAY BẠN LÀM CHỦ TRẠI", [
            "Chấm điểm công nhân", "Đánh giá rủi ro",
            "Khuyến nghị vận hành", "Trợ lý AI",
        ], GREEN),
    ]

    for i, (phase, name, items, color) in enumerate(stages):
        x = Inches(0.5 + i * 4.2)
        card = add_rect(slide, x, Inches(1.4), Inches(3.9), Inches(5.3), WHITE, color, radius=True)
        add_rect(slide, x, Inches(1.4), Inches(3.9), Inches(0.55), color, radius=True)
        add_text_box(slide, x + Inches(0.2), Inches(1.5), Inches(3.5), Inches(0.4),
                     phase, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text_box(slide, x + Inches(0.2), Inches(2.1), Inches(3.5), Inches(0.9),
                     name, size=16, bold=True, color=color, align=PP_ALIGN.CENTER)
        add_bullet_list(slide, x + Inches(0.25), Inches(3.2), Inches(3.4), Inches(3.2),
                        items, size=14, color=DARK)

    add_brand_footer(slide)


def build_feature_slide(prs, title, items, image):
    slide = blank_slide(prs)
    set_bg(slide)
    add_brand_header(slide, title)

    for i, item in enumerate(items):
        y = Inches(1.5 + i * 1.3)
        dot = add_rect(slide, Inches(0.7), y + Inches(0.15), Inches(0.35), Inches(0.35), ORANGE, radius=True)
        add_text_box(slide, Inches(1.3), y, Inches(5), Inches(0.7),
                     item, size=20, bold=True, color=DARK)

    add_image(slide, image, Inches(6.3), Inches(1.2), Inches(6.5), Inches(5.6))
    add_brand_footer(slide)


def build_slide_10(prs):
    build_feature_slide(prs, "VẼ VÙNG ATSH TRÊN CAMERA", [
        "Vùng sạch · Vùng bẩn · Vùng cấm",
        "Vùng sát trùng · Vùng cách ly",
        "Khách hàng tự vẽ — AMS tự động giám sát",
    ], "slide10_zone_drawing.png")


def build_slide_11(prs):
    build_feature_slide(prs, "PHÁT HIỆN VI PHẠM THỜI GIAN THỰC", [
        "Phát hiện ngay lập tức",
        "Chụp ảnh bằng chứng",
        "Cảnh báo tức thời",
    ], "slide11_realtime_detection.png")


def build_slide_12(prs):
    slide = blank_slide(prs)
    set_bg(slide)
    add_brand_header(slide, "ẢNH VI PHẠM – BẰNG CHỨNG RÕ RÀNG")

    items = ["Lưu ảnh vi phạm", "Dễ truy xuất", "Dễ đánh giá"]
    for i, item in enumerate(items):
        y = Inches(1.5 + i * 1.0)
        add_rect(slide, Inches(0.6), y, Inches(5.2), Inches(0.75), LIGHT_GRAY, radius=True)
        add_text_box(slide, Inches(0.9), y + Inches(0.18), Inches(4.8), Inches(0.5),
                     f"📷  {item}", size=18, bold=True, color=DARK)

    note = add_rect(slide, Inches(0.6), Inches(4.8), Inches(5.2), Inches(1.0), ORANGE, radius=True)
    add_text_box(slide, Inches(0.8), Inches(4.95), Inches(4.8), Inches(0.8),
                 "Không sử dụng video\nChỉ lưu ảnh vi phạm",
                 size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    add_image(slide, "slide12_violation_evidence.png", Inches(6.3), Inches(1.2), Inches(6.5), Inches(5.6))
    add_brand_footer(slide)


def build_slide_13(prs):
    build_feature_slide(prs, "DASHBOARD QUẢN LÝ THÔNG MINH", [
        "Tổng vi phạm theo thời gian",
        "Phân tích theo camera",
        "Phân tích theo khu vực",
    ], "slide13_dashboard.png")


def build_slide_14(prs):
    slide = blank_slide(prs)
    set_bg(slide)
    add_brand_header(slide, "CẢNH BÁO THÔNG MINH")

    channels = [("💬", "Zalo"), ("✉", "Email"), ("📱", "SMS"), ("📲", "App")]
    for i, (icon, label) in enumerate(channels):
        x = Inches(0.6 + i * 1.45)
        card = add_rect(slide, x, Inches(1.5), Inches(1.25), Inches(1.4), WHITE, ORANGE, radius=True)
        add_text_box(slide, x, Inches(1.65), Inches(1.25), Inches(0.5),
                     icon, size=28, align=PP_ALIGN.CENTER)
        add_text_box(slide, x, Inches(2.2), Inches(1.25), Inches(0.4),
                     label, size=14, bold=True, color=DARK, align=PP_ALIGN.CENTER)

    add_text_box(slide, Inches(0.6), Inches(3.2), Inches(5.5), Inches(0.5),
                 "Gửi cảnh báo tức thì qua mọi kênh", size=16, color=GRAY)

    add_image(slide, "slide14_smart_alerts.png", Inches(6.3), Inches(1.2), Inches(6.5), Inches(5.6))
    add_brand_footer(slide)


def build_slide_15(prs):
    slide = blank_slide(prs)
    set_bg(slide)
    add_brand_header(slide, "BẢO MẬT TUYỆT ĐỐI")

    items = ["Mã hóa dữ liệu", "Phân quyền truy cập", "Sao lưu tự động"]
    for i, item in enumerate(items):
        y = Inches(1.5 + i * 1.1)
        add_rect(slide, Inches(0.6), y, Inches(5.2), Inches(0.85), WHITE, GREEN, radius=True)
        add_text_box(slide, Inches(0.9), y + Inches(0.2), Inches(4.8), Inches(0.5),
                     f"🔒  {item}", size=18, bold=True, color=DARK)

    banner = add_rect(slide, Inches(0.6), Inches(5.0), Inches(5.2), Inches(0.9), GREEN, radius=True)
    add_text_box(slide, Inches(0.8), Inches(5.15), Inches(4.8), Inches(0.65),
                 "Dữ liệu trang trại là tài sản của khách hàng",
                 size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    add_image(slide, "slide15_security.png", Inches(6.3), Inches(1.2), Inches(6.5), Inches(5.6))
    add_brand_footer(slide)


def build_slide_16(prs):
    slide = blank_slide(prs)
    set_bg(slide)
    add_brand_header(slide, "LỢI ÍCH VƯỢT TRỘI")

    benefits = [
        ("24/7", "Giám sát liên tục"),
        ("✓", "Không bỏ sót vi phạm"),
        ("🛡", "Giảm nguy cơ dịch bệnh"),
        ("📈", "Tăng tính tuân thủ"),
    ]
    for i, (icon, text) in enumerate(benefits):
        col = i % 2
        row = i // 2
        x = Inches(0.6 + col * 3.0)
        y = Inches(1.5 + row * 1.5)
        card = add_rect(slide, x, y, Inches(2.7), Inches(1.2), LIGHT_GRAY, radius=True)
        add_text_box(slide, x + Inches(0.2), y + Inches(0.15), Inches(0.8), Inches(0.6),
                     icon, size=26, bold=True, color=ORANGE)
        add_text_box(slide, x + Inches(0.9), y + Inches(0.35), Inches(1.6), Inches(0.5),
                     text, size=15, bold=True, color=DARK)

    add_image(slide, "slide16_benefits.png", Inches(6.3), Inches(1.2), Inches(6.5), Inches(5.6))
    add_brand_footer(slide)


def build_slide_17(prs):
    slide = blank_slide(prs)
    set_bg(slide)
    add_brand_header(slide, "PHÙ HỢP MỌI MÔ HÌNH TRANG TRẠI")

    models = ["Trại nhỏ", "Trại vừa", "Trại lớn", "Nhiều trại"]
    for i, model in enumerate(models):
        x = Inches(0.6 + i * 1.45)
        card = add_rect(slide, x, Inches(1.4), Inches(1.25), Inches(0.9), ORANGE if i % 2 else GREEN, radius=True)
        add_text_box(slide, x, Inches(1.6), Inches(1.25), Inches(0.5),
                     model, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    add_image(slide, "slide17_farm_models.png", Inches(0.6), Inches(2.5), Inches(12.1), Inches(4.3))
    add_brand_footer(slide)


def build_slide_18(prs):
    slide = blank_slide(prs)
    set_bg(slide)
    add_image(slide, "slide18_guarantee.png", Inches(0), Inches(0), SLIDE_W, SLIDE_H)

    panel = add_rect(slide, Inches(1.5), Inches(1.8), Inches(10.3), Inches(3.8), WHITE, radius=True)
    add_text_box(slide, Inches(1.8), Inches(2.2), Inches(9.7), Inches(1.5),
                 "ĐẢM BẢO AN TOÀN CHO\nTRANG TRẠI TỚI 99,99%",
                 size=40, bold=True, color=GREEN, align=PP_ALIGN.CENTER, font=FONT_TITLE)
    add_rect(slide, Inches(5.5), Inches(3.9), Inches(2.3), Inches(0.08), ORANGE)
    add_text_box(slide, Inches(1.8), Inches(4.2), Inches(9.7), Inches(0.8),
                 "Giúp bạn sản xuất bền vững và gia tăng lợi nhuận",
                 size=20, color=GRAY, align=PP_ALIGN.CENTER)


def build_slide_19(prs):
    slide = blank_slide(prs)
    set_bg(slide, LIGHT_GRAY)
    add_brand_header(slide, "BẢNG GIÁ DỊCH VỤ AMS")

    # Standard
    std = add_rect(slide, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.0), WHITE, GREEN, radius=True)
    add_rect(slide, Inches(0.8), Inches(1.5), Inches(5.6), Inches(0.7), GREEN, radius=True)
    add_text_box(slide, Inches(1.0), Inches(1.6), Inches(5.2), Inches(0.5),
                 "AMS STANDARD", size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text_box(slide, Inches(1.0), Inches(2.4), Inches(5.2), Inches(0.8),
                 "1,5 – 2 TRIỆU / THÁNG", size=24, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
    std_items = [
        "Tối đa 20 camera",
        "Các hành vi vi phạm ATSH",
        "Dashboard quản lý",
        "Cảnh báo thời gian thực",
        "Báo cáo ATSH",
    ]
    add_bullet_list(slide, Inches(1.2), Inches(3.3), Inches(4.8), Inches(3.0), std_items, size=15)

    # Professional
    pro = add_rect(slide, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.0), WHITE, ORANGE, radius=True)
    add_rect(slide, Inches(6.9), Inches(1.5), Inches(5.6), Inches(0.7), ORANGE, radius=True)
    add_text_box(slide, Inches(7.1), Inches(1.6), Inches(5.2), Inches(0.5),
                 "AMS PROFESSIONAL", size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text_box(slide, Inches(7.1), Inches(2.4), Inches(5.2), Inches(0.8),
                 "3 – 6 TRIỆU / THÁNG", size=24, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
    pro_items = [
        "Trên 20 camera",
        "Các hành vi vi phạm ATSH",
        "Dashboard nâng cao",
        "Báo cáo chuyên sâu",
        "Hỗ trợ ưu tiên",
    ]
    add_bullet_list(slide, Inches(7.3), Inches(3.3), Inches(4.8), Inches(3.0), pro_items, size=15)

    # CTA
    cta = add_rect(slide, Inches(4.5), Inches(6.7), Inches(4.3), Inches(0.55), ORANGE, radius=True)
    add_text_box(slide, Inches(4.5), Inches(6.78), Inches(4.3), Inches(0.45),
                 "Liên hệ tư vấn ngay →", size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_brand_footer(slide)


def build_slide_20(prs):
    slide = blank_slide(prs)
    set_bg(slide)
    add_image(slide, "slide20_contact.png", Inches(0), Inches(0), SLIDE_W, SLIDE_H)

    panel = add_rect(slide, Inches(2.0), Inches(1.5), Inches(9.3), Inches(4.5), WHITE, radius=True)
    add_text_box(slide, Inches(2.4), Inches(1.9), Inches(8.5), Inches(0.5),
                 "TIN NGHIA", size=24, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    add_text_box(slide, Inches(2.4), Inches(2.4), Inches(8.5), Inches(0.9),
                 "AMS", size=56, bold=True, color=ORANGE, align=PP_ALIGN.CENTER, font=FONT_TITLE)
    add_rect(slide, Inches(5.5), Inches(3.4), Inches(2.3), Inches(0.06), ORANGE)
    add_text_box(slide, Inches(2.4), Inches(3.6), Inches(8.5), Inches(0.5),
                 "31 Hoa Viên, KĐT Đặng Xá, Thuận An, TP Hà Nội",
                 size=16, color=DARK, align=PP_ALIGN.CENTER)
    add_text_box(slide, Inches(2.4), Inches(4.2), Inches(8.5), Inches(0.6),
                 "0964106955", size=28, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
    add_text_box(slide, Inches(2.4), Inches(4.9), Inches(8.5), Inches(0.5),
                 "AI GIÁM SÁT AN TOÀN SINH HỌC 24/7",
                 size=14, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    add_text_box(slide, Inches(2.4), Inches(5.3), Inches(8.5), Inches(0.4),
                 "Bảo vệ đàn heo – Bảo vệ lợi nhuận",
                 size=14, color=GRAY, align=PP_ALIGN.CENTER)


def main():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    builders = [
        build_slide_01, build_slide_02, build_slide_03, build_slide_04,
        build_slide_05, build_slide_06, build_slide_07, build_slide_08,
        build_slide_09, build_slide_10, build_slide_11, build_slide_12,
        build_slide_13, build_slide_14, build_slide_15, build_slide_16,
        build_slide_17, build_slide_18, build_slide_19, build_slide_20,
    ]

    for builder in builders:
        builder(prs)

    prs.save(str(OUTPUT))
    print(f"✓ Saved: {OUTPUT}")
    print(f"  Slides: {len(prs.slides)}")


if __name__ == "__main__":
    main()
