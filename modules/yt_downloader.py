import yt_dlp
import os


def download_video(url, quality="1080", format="mp4"):
    # Carpeta temporal dentro de tu proyecto
    download_dir = os.environ.get('DOWNLOAD_DIR', os.path.join(os.getcwd(), "Downloads"))
    os.makedirs(download_dir, exist_ok=True)

    # Plantilla para nombre de archivo
    outtmpl = os.path.join(download_dir, "%(title).80s.%(ext)s")

    ydl_opts = {
        "outtmpl": outtmpl,
        "quiet": True,
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

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            title = info.get("title") if info else "firedownloader_video"
            ext = "mp3" if format == "mp3" else format
            filename = f"{title}.{ext}"
            full_path = os.path.join(download_dir, filename)

            if info and (info.get("height", 0) or 0) < int(quality) and format != "mp3":
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

    except yt_dlp.utils.ExtractorError:
        return {"success": False, "error": "❌ Error al extraer el video"}
    except yt_dlp.utils.DownloadError:
        return {"success": False, "error": "❌ Video no encontrado o URL inválida"}
    except ValueError as e:
        return {"success": False, "error": f"❌ {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"❌ Error inesperado: {str(e)}"}


if __name__ == "__main__":
    # Ejemplo de uso
    url = "https://www.youtube.com/watch?v=example"
    result = download_video(url, quality="1080", format="mp4")
    print(result)