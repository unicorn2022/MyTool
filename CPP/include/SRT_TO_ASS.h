#pragma once
#include <cstdio>

// 将SRT文件转化为ASS文件
class SRT_TO_ASS {
public:
    // 程序入口
    static bool Main(const char* path = "../doc/source.srt", const char* output = "../doc/target.ass");

private:
    // 将LRC文件逐行转化为ASS文件
    static void GetText(FILE* fin, FILE* fout);

    // 处理其中的一行, 改行数据在buffer中
    static void GetOneRow(FILE* fout);
};
