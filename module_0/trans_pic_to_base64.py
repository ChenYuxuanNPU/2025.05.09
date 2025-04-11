import base64


def image_to_base64(image_path):
    """
    将图像文件转换为Base64编码字符串

    参数:
        image_path (str): 图像文件的路径

    返回:
        str: Base64编码的字符串 (格式: "data:image/[类型];base64,...")
    """
    # 获取文件扩展名确定MIME类型
    ext = image_path.split('.')[-1].lower()
    mime_type = f"image/{ext}" if ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'] else "image/jpeg"

    try:
        with open(image_path, "rb") as image_file:
            # 读取文件内容并编码
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:{mime_type};base64,{encoded_string}"
    except FileNotFoundError:
        raise FileNotFoundError(f"图像文件未找到: {image_path}")
    except Exception as e:
        raise Exception(f"转换失败: {str(e)}")

print(image_to_base64(image_path="static/1.png"))