#pragma once
#include <cstdio>

// 将epub文件解压出来的HTML文件批量转化为TXT文件
class EPUB_TO_TXT {
public:
    static bool Main(const char* sourcePath = "../doc", const char* output = "../doc/target.txt");

private:
    enum Type {
        title,
        text
    };

    // 将<h3></h3>、<p></p>删除
    // buffer==>txt
    static void Delete_Angle_Brackets(Type type);

    // 将标题改成第xxx章
    // txt==>header
    static void Convert_Header();


    // 将HTML中的文字提取出来
    static void GetText(FILE* fin, FILE* fout);
};