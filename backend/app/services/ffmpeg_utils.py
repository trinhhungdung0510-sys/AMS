from __future__ import annotations


def normalize_ffmpeg_error(stderr: str, returncode: int) -> str:
    text = (stderr or "").strip()
    lowered = text.lower()

    if "401" in text or "unauthorized" in lowered:
        return "Xác thực RTSP thất bại — kiểm tra username và password"
    if "403" in text or "forbidden" in lowered:
        return "Camera từ chối truy cập RTSP (403 Forbidden)"
    if "connection refused" in lowered:
        return "Không kết nối được tới camera — port hoặc IP không đúng"
    if "timed out" in lowered or "timeout" in lowered:
        return "Hết thời gian chờ kết nối RTSP"
    if "invalid data found when processing input" in lowered:
        return "URL RTSP không hợp lệ hoặc stream không khả dụng"
    if "no such file or directory" in lowered and "rtsp" not in lowered:
        return "Không tìm thấy ffmpeg — cần cài FFmpeg trên server"

    if text:
        return text.splitlines()[0][:240]
    return f"ffmpeg thất bại (mã {returncode})"
