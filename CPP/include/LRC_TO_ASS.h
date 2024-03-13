#pragma once
#include <cstdio>

// 将LRC文件转化为ASS文件
// LRC格式要求：
//  1. 时间戳: [min:second.ms], 如[00:14.01]
//  2. 最后一行: 空语句, 表示整首歌的结束时间
class LRC_TO_ASS {
public:
    // 程序入口
    static bool Main(const char* path = "../doc/source.lrc", const char* output = "../doc/target.ass");

private:
    // 将LRC文件逐行转化为ASS文件
    static void GetText(FILE* fin, FILE* fout);

    // 处理其中的一行, 改行数据在buffer中
    static void GetOneRow(FILE* fout);
};
