#pragma once
#include <cstdio>

// 将原本TXT文件中的xxx改为第xxx章
// 注意,只能在标题中出现空格
class TXT_TO_TXT {
public:
    // 程序入口
    static bool Main(const char* path = "../doc/source.txt", const char* output = "../doc/target.txt");

private:
    // 如果是数字,则返回数字的值,并将source指针后移
    // 否则返回0
    static int GetDigit(char*& source);


    // 以回车分割将文本内容全部读取出来
    // 如果是数字,则添加第xxx章
    static void GetText(FILE* fin, FILE* fout);
    
};
