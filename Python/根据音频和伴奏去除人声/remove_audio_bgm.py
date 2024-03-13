from pydub import AudioSegment
import numpy as np

def interference_cancellation(source, bgm):
    # 将音频文件转换为numpy数组
    source_signal = np.array(source.get_array_of_samples())
    bgm_signal = np.array(bgm.get_array_of_samples())

    # 进行干涉相消处理，这里只是一个简单的例子，实际情况可能需要更复杂的处理
    result_signal = source_signal - bgm_signal

    # 创建一个新的AudioSegment对象
    result_audio = AudioSegment(
        result_signal.tobytes(),
        frame_rate=source.frame_rate,
        sample_width=source.sample_width,
        channels=source.channels
    )

    return result_audio

# 读取两个文件
source = AudioSegment.from_wav("原曲.wav")
bgm = AudioSegment.from_wav("伴奏.wav")

# 进行干涉相消处理
result_audio = interference_cancellation(source, bgm)

# 保存处理后的音频文件
result_audio.export("result.wav", format="wav")
