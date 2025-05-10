import yt_dlp
import os
import random
import time
from urllib.parse import quote

def get_random_user_agent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
    ]
    return random.choice(agents)

def download_video(url, quality="1080", format="mp4", max_retries=5):
    download_dir = os.path.join(os.getcwd(), "Downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    for attempt in range(max_retries):
        try:
            ydl_opts = {
                "outtmpl": os.path.join(download_dir, "%(title).80s.%(ext)s"),
                "quiet": True,
                "no_warnings": True,
                "http_headers": {
                    "User-Agent": get_random_user_agent(),
                    "Accept-Language": "en-US,en;q=0.5",
                    "Referer": "https://www.youtube.com/",
                    "Origin": "https://www.youtube.com",
                    "DNT": "1"
                },
                "extract_flat": False,
                "socket_timeout": 60,
                "retries": 10,
                "fragment_retries": 10,
                "extractor_args": {
                    "youtube": {
                        "skip": ["dash", "hls"]
                    }
                },
                "throttled_rate": "1M",
                "proxy": get_random_proxy() if attempt > 2 else None,
                "wait_for_video": (10, 30) if attempt > 1 else None,
                "ignoreerrors": True
            }

            if format == "mp3":
                ydl_opts["format"] = "bestaudio/best"
                ydl_opts["postprocessors"] = [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ]
            else:
                ydl_opts["format"] = (
                    f"bestvideo[height<={quality}][ext={format}]+bestaudio/best[height<={quality}]"
                )
                ydl_opts["merge_output_format"] = format

                if format != "webm":
                    ydl_opts["postprocessors"] = [
                        {"key": "FFmpegVideoConvertor", "preferedformat": format}
                    ]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if attempt > 0:
                    time.sleep(random.uniform(5, 15))
                    
                info = ydl.extract_info(url, download=True)

                title = info.get("title") if info else "firedownloader_video"
                ext = "mp3" if format == "mp3" else format
                filename = f"{title}.{ext}"
                full_path = os.path.join(download_dir, filename)

                if (
                    info
                    and (info.get("height", 0) or 0) < int(quality)
                    and format != "mp3"
                ):
                    max_quality = f"{info['height']}p"
                    return {
                        "success": True,
                        "error": f"⚠️ Calidad máxima disponible: {max_quality}",
                        "file_path": full_path,
                        "file_name": filename,
                        "title": title,
                    }

                # Asegura que el archivo existe
                if not os.path.isfile(full_path):
                    return {
                        "success": False,
                        "error": "❌ Archivo no encontrado tras descarga",
                    }

                return {
                    "success": True,
                    "file_path": full_path,
                    "file_name": filename,
                    "title": title,
                }
        except yt_dlp.utils.DownloadError as e:
            if "bot" in str(e).lower() and attempt < max_retries - 1:
                continue
            return {"success": False, "error": f"❌ Error de YouTube (intento {attempt + 1}): {str(e)}"}
        except yt_dlp.utils.ExtractorError:
            return {"success": False, "error": "❌ Error al extraer el video"}
        except ValueError as e:
            return {"success": False, "error": f"❌ {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"❌ Error inesperado: {str(e)}"}

def get_random_proxy():
    """Obtiene un proxy aleatorio de una lista verificada"""
    verified_proxies = [
        "http://45.95.147.122:8080",
        "http://193.122.71.184:3128",
        "http://154.16.202.22:3128",
        "http://51.158.68.68:8811",
        "http://20.210.113.32:80"
    ]
    return random.choice(verified_proxies)

if __name__ == "__main__":
    # Ejemplo de uso
    url = "https://www.youtube.com/watch?v=example"
    result = download_video(url, quality="1080", format="mp4")
    print(result)
