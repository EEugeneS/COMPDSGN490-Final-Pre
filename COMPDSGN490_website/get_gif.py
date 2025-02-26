from PIL import Image, ImageDraw, ImageOps
import imageio

# 读取原始logo
logo_path = "./logo.png"  # 确保你的logo路径正确
logo = Image.open(logo_path).convert("RGBA")

# 创建圆形遮罩
def create_circle_mask(size):
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    # 在遮罩上画一个圆形
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    return mask

# 创建旋转效果的动画帧
frames = []
num_frames = 20  # 动画帧数

for i in range(num_frames):
    # 计算旋转角度
    angle = (i / num_frames) * 360  # 让logo完整旋转一圈
    
    # 旋转图像（使用旧版 BICUBIC 兼容方式）
    rotated_frame = logo.rotate(angle, resample=Image.BICUBIC, expand=True)
    
    # 创建与原始logo大小相同的画布，并居中放置旋转后的图像
    frame = Image.new("RGBA", logo.size, (0, 0, 0, 0))  # 创建透明背景
    position = ((logo.width - rotated_frame.width) // 2, (logo.height - rotated_frame.height) // 2)
    frame.paste(rotated_frame, position, rotated_frame)
    
    # 创建圆形遮罩并应用到当前帧
    circle_mask = create_circle_mask(frame.size)
    
    # 使用圆形遮罩裁剪帧，确保透明背景
    frame = Image.composite(frame, Image.new("RGBA", frame.size, (0, 0, 0, 0)), circle_mask)
    
    # 添加到帧列表
    frames.append(frame)

# 添加最后的透明背景帧（不旋转）
for j in range(10):
    frame = Image.new("RGBA", logo.size, (0, 0, 0, 0))  # 创建透明背景
    frame.paste(logo, (0, 0), logo)  # 贴上原始 logo
    
    # 创建圆形遮罩并应用到当前帧
    circle_mask = create_circle_mask(frame.size)
    
    # 使用圆形遮罩裁剪帧，确保透明背景
    frame = Image.composite(frame, Image.new("RGBA", frame.size, (0, 0, 0, 0)), circle_mask)
    
    frames.append(frame)

# 保存为GIF时，确保使用透明背景
rotate_gif_path = "./logo_rotate_circle_transparent.gif"
imageio.mimsave(rotate_gif_path, frames, duration=0.1, loop=0, format='GIF')

print(f"GIF 动画已保存: {rotate_gif_path}")
